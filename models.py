
from django.db import models
from django.contrib.postgres.fields import ArrayField
class ModelCourse(models.Model):
    name = models.CharField(max_length=100)
    serial = models.CharField(max_length=100)
    bgCardUrl = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    duration = models.IntegerField()
    description = models.TextField(default = "Follow these simple steps")
    textBook = models.CharField(max_length=100, default= "Streamline Departure")
    color = models.CharField(max_length=40, default="white")
    progress = models.IntegerField(default=0)
    bgCardUrlSecondary= models.CharField(max_length=200, default="_")
    category = models.ManyToManyField("Category", related_name="course_category")
    sale = models.IntegerField(default=0)
    #certificate = models.ImageField() #
   # totalSession= models.IntegerField(default=0)
    


    def __str__(self):
        return self.name


class Section (models.Model):
    title = models.CharField(max_length = 100, blank=False, null=False)
    description = models.TextField(blank=False)
    externalLink = models.TextField()
    timeSpan = models.IntegerField()
    questions = models.ManyToManyField('Question')
    questionsJSON = models.JSONField(default = {"questions" : []} )
    def __str__(self):
        return f"Section {self.title}"

#{"question":"In &quot;Call Of Duty: Zombies&quot;, you can upgrade the &quot;Apothicon Servant&quot; in the &quot;Shadows Of Evil&quot; map.",
# "correct_answer":"True","incorrect_answers":["False"]}


    #session = models.ForeignKey('ModelSession', on_delete=models.CASCADE)
    #icon  #foreignkey relationship


class ModelSession(models.Model):
    course = models.ForeignKey(ModelCourse, on_delete=models.CASCADE)
    overview = models.TextField(null= True, blank=True)
    PPTFileUrl = models.URLField(null= True, blank=True)
    CPTUrl = models.URLField(null= True, blank=True)
    bgCardUrl = models.CharField(max_length=200, null= True, blank=True)
    color= models.CharField(max_length=20, default= 'white', null= True, blank=True)  
    section = models.ManyToManyField(Section, related_name="Section", null=True, blank=True)
    topics = models.CharField(max_length=100, null= True, blank=True, default = "English")
    level = models.CharField(max_length = 70, null= True, blank=True, default = "Beginner")

    beforeClass = models.ManyToManyField(Section, related_name='before_class_section', blank= True)
    inClass = models.ManyToManyField(Section, related_name='in_class_section', blank=True)
    afterClass = models.ManyToManyField(Section, related_name='after_class_section',  blank=True)

     

    def __str__(self):
        return f"Session {self.id} - Course {self.course.name}"

    """
class Course(models.Model):
    model_course = models.ForeignKey(ModelCourse, on_delete=models.CASCADE)
    teacher = models.CharField(max_length=100)
    dateStart = models.DateField()
    dateEnd = models.DateField()
    gradeBookUrl = models.URLField()
    attendanceExcelUrl = models.URLField()


    
    def __init__(self) :
        return f"{self.name}"
    """

class HomeDetails(models.Model):
    backgroundImageUrl = models.CharField(max_length=200)
    firstViewLine = models.CharField(max_length=100)
    videoUrl =  models.CharField(max_length=200)
    courseBackgroundImageUrl = models.CharField(max_length=200)

#class Teacher(models.Model):
#    pass 

class Blog(models.Model):
    title = models.CharField(max_length = 100)
    url = models.CharField(max_length = 200)
    img = models.CharField(max_length = 200) #option 2 : save the img to the DB
    description = models.CharField(max_length= 100)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return f"{self.title}"

class Campus(models.Model):
    name = models.CharField(max_length= 40)
    address = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return f"{self.name}"
class ContactRequest(models.Model):
    name = models.CharField(max_length = 100)
    message = models.CharField(max_length = 200)
    gmail = models.EmailField(max_length=100)
    phone = models.CharField(max_length = 14)
    campus = models.ForeignKey(Campus, related_name='contact_requests', on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.name}"

    
class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return f"{self.name}"

class Question(models.Model):
    TYPE_CHOICES = [
        ('multiple', 'Multiple Choice'),
        ('boolean', 'True/False')
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE )
    question = models.TextField()
    correct_answer = models.CharField(max_length=100)
    incorrect_answers = models.JSONField()
    def __str__(self) -> str:
        return f"question: {self.id} {self.question}"


