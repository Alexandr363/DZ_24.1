from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.permissions import AllowAny


from education.models import Course, Lesson, Payments, Subscription
from education.paginators import CoursePaginator, LessonPaginator
from education.permissions import IsModerator, IsOwner
from education.serializers import CourseSerializer, LessonSerializer, \
    PaymentsSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwner]
    pagination_class = CoursePaginator


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    # permission_classes = [IsModerator]
    permission_classes = [AllowAny]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]
    pagination_class = LessonPaginator


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('day_of_payment',)
    filterset_fields = ('course', 'lesson', 'payment_method',)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        subscription = serializer.save()
        subscription.user = self.request.user
        subscription.save()
