from .models import HomeDetails, Blog, ModelCourse, Question, ModelSession, Section, Category
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import Blogserializer, ModelSessionserializer, UserSerializer, Sectionserializer, ContactRequestserializer,QuestionSerializer, CustomBlogSerializer, ModelCourseserializer
from rest_framework_simplejwt.tokens import RefreshToken
@api_view(["GET", "POST"])
def index(request):
    if request.method == "GET":
        #get all the drink obj
        #serialize all
        #return json format

        # Get the three most recent blog objects based on the 'date' attribute
        blogs = Blog.objects.order_by('-created')[:3]  # Retrieve the latest three entries
        blogserializer = CustomBlogSerializer(blogs, many=True) # When serializing the blog objects, we use CustomBlogSerializer instead of Blogserializer.

        categories = Category.objects.all()
        courseCategories= {}
        for category in categories:
            courseCategories[ category.name] = ModelCourseserializer(category.course_category.all() , many=True).data

            #featureCourses[] = ModelCourseserializer(category.course_category.all() , many=True).data
        print()


        returnData  = { 'blogs' : blogserializer.data, "courseCategories" : courseCategories }
        return Response(returnData , status = status.HTTP_200_OK)
        
    if request.method == "POST":

        serializer = ContactRequestserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data , status = status.HTTP_201_CREATED) #why return response ...
@api_view(["GET", "POST", "PUT"])
@permission_classes([IsAuthenticated])
def courses(request):
    if request.method == "GET":
        courses = ModelCourse.objects.all()
        coursesserializer = ModelCourseserializer(courses, many=True)
        responseData  = { 'courses' : coursesserializer.data }
        return Response(responseData , status = status.HTTP_200_OK)
    elif request.method == "POST":
        request_data = request.data.copy()
        request_data['duration'] = int(request_data.get('duration', 0))
        request_data['sale'] = int(request_data.get('sale', 0))
        
        serializer = ModelCourseserializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status = status.HTTP_202_ACCEPTED)
        return Response(status= status.HTTP_400_BAD_REQUEST)
    elif request.method=="PUT":
        course = ModelCourse.objects.get(pk=request.data.get('id'))
        request_data = request.data.copy()
        request_data['duration'] = int(request_data.get('duration', 0)) ##
        request_data['sale'] = int(request_data.get('sale', 0))##
        serializer = ModelCourseserializer( instance=course, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(status= status.HTTP_400_BAD_REQUEST)

        
    

@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def course(request, id):
    try : 
        course = ModelCourse.objects.get(pk=id)       
    except ModelCourse.DoesNotExist: # ........
        return Response("data not found", status= status.HTTP_404_NOT_FOUND) 
    if request.method =="GET":       

        courseserializer = ModelCourseserializer(course)
        sessions = ModelSession.objects.filter(course=course)
        sessions_serializer = ModelSessionserializer(sessions, many=True)
        session_data = [{'id': session.id, **session_data} for session, session_data in zip(sessions, sessions_serializer.data)]

        responseData = {'course': courseserializer.data, 'sessions': session_data}
        return Response(responseData , status = status.HTTP_200_OK)
    elif request.method == "DELETE":
        course.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    if request.method == 'POST':
        course_id = request.data.get('course')  # Extract course ID from request data
        try:
            course = ModelCourse.objects.get(pk=course_id)
        except ModelCourse.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ModelSessionserializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['course'] = course  # Associate course with session
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "DELETE", "POST"])
@permission_classes([IsAuthenticated])
def session(request, id):
    if(request.method != "POST"):
        try : 
            session = ModelSession.objects.get(pk=id)       
        except ModelSession.DoesNotExist: # ........
            return Response("data not found", status= status.HTTP_404_NOT_FOUND) 
    if request.method == "GET":
        session_serializer = ModelSessionserializer(session)
        before_sections = session.beforeClass.all()
        before_section_serializer = Sectionserializer(before_sections, many=True)

        in_sections = session.inClass.all()
        in_section_serializer = Sectionserializer(in_sections, many=True)

        after_sections = session.afterClass.all()
        after_section_serializer = Sectionserializer(after_sections, many=True)

        response_data = {
            'sections' : {
                'beforeSection': before_section_serializer.data,
                'inSection': in_section_serializer.data,
                'afterSection': after_section_serializer.data
            },
            'session': session_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        course_id = request.data.get('course')  # Extract course ID from request data
        try:
            course = ModelCourse.objects.get(pk=course_id)
        except ModelCourse.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = ModelSessionserializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['course'] = course  # Associate course with session
            newSession = serializer.save()
            
            session_data = {'id':  newSession.id, **serializer.data}
            return Response(session_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        session.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def blogDetails(request, id):
    try : 
        blog = Blog.objects.get(pk = id)
    except Blog.DoesNotExist: # ........
        return Response("data not found", status= status.HTTP_404_NOT_FOUND) 
    
    if request.method == "DELETE":
    
        blog.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        serializer = Blogserializer(blog, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status = status.HTTP_202_ACCEPTED)
        return Response(status= status.HTTP_400_BAD_REQUEST)
        
@api_view(["GET"])
def questionView(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def section(request, id):
    try : 
        section = Section.objects.get(pk=id)   
    except Section.DoesNotExist: # ........
        return Response("data not found", status= status.HTTP_404_NOT_FOUND) 

    if request.method == "GET":
        sectionSerializer = Sectionserializer(section)
        #return the questionsJSON need the serializer ?
        return Response(sectionSerializer.data, status= status.HTTP_200_OK)
    
@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token ),
        }

        return Response(tokens, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)