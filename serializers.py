from rest_framework import serializers
from .models import Blog, ContactRequest, ModelCourse, Question, ModelSession, Section

class Blogserializer(serializers.ModelSerializer):
    class Meta: 
        model = Blog
        fields = '__all__'
class CustomBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'url', 'img', 'description', 'created']

class ModelSessionserializer(serializers.ModelSerializer):
    class Meta: 
        model = ModelSession
        fields = ['course', 'overview', 'PPTFileUrl', 'CPTUrl']
class Sectionserializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields ='__all__'

class ContactRequestserializer(serializers.ModelSerializer):
    class Meta: 
        model = ContactRequest
        fields = '__all__'


class ModelCourseserializer(serializers.ModelSerializer):
    
      
    class Meta:
        model = ModelCourse
        fields ='__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['incorrect_answers'] = instance.incorrect_answers.get('incorrect_answers', [])  # JSONField will be serialized automatically
        return data

from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model= User
        fields ='__all__'
    def create(self, validated_data):
        user = User.objects.create(
            username  = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user