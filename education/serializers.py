from rest_framework import serializers

from education.models import Course, Lesson, Payments, Subscription
from education.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            LinkValidator(field='link_video')
        ]


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, source='lesson_set', many=True)
    is_subscription = serializers.SerializerMethodField()

    def get_lesson_count(self, instance):
        return instance.lesson_set.all().count()

    def get_subscription(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=instance).exists()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            LinkValidator(field='link_course')
        ]


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'
