from rest_framework import serializers

from education.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    model = Course
    fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    model = Lesson
    fields = '__all__'
