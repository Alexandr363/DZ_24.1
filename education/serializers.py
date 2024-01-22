from rest_framework import serializers

from education.models import Course, Lesson, Payments


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, source='lesson_set', many=True)

    def get_lesson_count(self, instance):
        return instance.lesson_set.all().count()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'
