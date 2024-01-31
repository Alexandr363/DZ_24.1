from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='admin@mail.com',
            is_staff=True,
            is_active=True,
            is_superuser=False,
            first_name='admin',
            last_name='admin'

        )
        self.user.set_password('admin')
        self.user.save()
        self.course = Course.objects.create(
            title='test',
            description='test',

        )
        self.lesson_data = Lesson.objects.create(
            title='test',
            description='test',
            link_video='youtube.com',
            user=self.user,
            course=self.course
            )

    def test_lesson_create(self):
        response = self.client.post(
            '/education/lesson/create/',
            data={'pk': 2, 'title': 'test', 'description': 'test', 'course': self.course.pk, 'user': self.user.id, 'link_video': 'youtube.com'}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'pk': 4, 'title': 'test', 'description': 'test', 'course': self.course.pk, 'user': self.user.pk, 'link_video': 'youtube.com'}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_lesson(self):

        response = self.client.get(
            '/education/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
           {'count': 1, 'next': None, 'previous': None, 'results': [{'pk': 2, 'title': 'test', 'description': 'test', 'course': self.course.pk, 'user': self.user.pk, 'link_video': 'youtube.com'}]})

    def test_delete(self):

        response = self.client.delete(
            '/education/lesson/delete/1/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        data = {'pk': 1, 'title': 'test1', 'description': 'test1', 'course': self.course.pk, 'user': self.user.id,
                'link_video': 'youtube.com'}

        response = self.client.put(
            '/education/lesson/update/5/',
            data=data
        )

        self.assertEquals(response.json(),
                          {'pk': 1
                              , 'title': 'test1', 'description': 'test1', 'course':  self.course.pk, 'user': self.user.id, 'link_video': 'youtube.com'}
                          )


class SubscribeTestCase(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='test1',
            description='test1',

        )

        self.user = User.objects.create(
            email='admin@mail.com',
            is_staff=True,
            is_active=True,
            is_superuser=False,
            first_name='admin',
            last_name='admin'

        )
        self.user.set_password('admin')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.subscribe = Subscription.objects.create(
            user=self.user,
            is_active=True,
            course=self.course
        )

    def test_create_subscribe(self):

        response = self.client.post(
            '/lesson/subscribe/',
            data={'user': self.user.pk, 'is_active': True, 'course': self.course.pk}
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': 2, 'is_active': True, 'user': self.user.pk, 'course': self.course.pk}

        )

    def test_subscribe_list(self):

        response = self.client.get(
            '/lesson/subscribe/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
           [{'id': 5, 'is_active': True, 'user': self.user.pk, 'course': self.user.pk}]
        )

    def test_update(self):
        response = self.client.post(
            '/lesson/subscribe/',
            data={'user': self.user.pk, 'is_active': True, 'course': self.course.pk}
        )
        print(response.json())
        response = self.client.put(
            '/lesson/subscribe/7/',

        )

        self.assertEquals(response.json(),
                          {'id':7, 'is_active': True, 'user': 8, 'course': 8}

                          )

    def test_delete_subscribe(self):
        response = self.client.post(
            '/lesson/subscribe/',
            data={'user': self.user.pk, 'is_active': True, 'course': self.course.pk}
        )
        print(response.json())
        response = self.client.delete(
            '/lesson/subscribe/2/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)