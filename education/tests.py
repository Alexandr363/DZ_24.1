from audioop import reverse
from copy import deepcopy

from rest_framework.test import APITestCase
from rest_framework import status

from education.models import Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_lesson(self):
        data = {
            "title": "test",
            "description": "test",
            "link_video": "youtube.com"
        }

        response = self.client.post(
            '/lesson/create/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_read_lesson(self):
        response = self.client.get(
            '/lesson/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_lesson(self):
        data = {
            "title": "update_test",
            "description": "update_test",
            "link_video": "youtube.com"
        }
        response = self.client.put(
            '/lesson/update/1/',
            data=data
        )
        self.assertEqual(
            response.json(),
            {
                "title": "update_test",
                "description": "update_test",
                "link_video": "youtube.com"
            }
        )

    def test_delete_lesson(self):
        response = self.client.delete(
            '/lesson/delete/1/'
        )
        self.assertEqual(
            response.json(),
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.course = Course.objects.create(title='test', owner=self.user)
        self.auth_client = deepcopy(self.client)
        self.auth_client.force_authenticate(self.user)
        self.subscribe_url = reverse('education:subscription',
                                     args=[self.course.pk])
        self.unsubscribe_url = reverse('education:courses',
                                       args=[self.course.pk])

    def test_anonymous_user_cannot_subscribe(self):
        response = self.client.post(self.subscribe_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_cannot_unsubscribe(self):
        url = reverse('education:courses', args=[self.course.pk])
        response = self.client.post(self.unsubscribe_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_user_can_subscribe_on_course(self):
        response = self.auth_client.post(self.subscribe_url)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(self.course.subscriptions.get().user, self.user)

    def test_authenticated_client_cant_subscribe_on_not_existing_course(self):
        not_existing_course_id = self.course.pk + 1
        url = reverse('education:courses-subscribe',
                      args=[not_existing_course_id])

        response = self.auth_client.post(url)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_unsubscribe_on_course(self):
        Subscription.objects.create(course=self.course, user=self.user)

        response = self.auth_client.post(self.unsubscribe_url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(self.course.subscriptions.count(), 0)

    def test_set_flag_if_user_subscribed_on_course_or_not(self):
        url = reverse('education:courses', args=[self.course.pk])

        response = self.auth_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()['is_subscribed'])

        Subscription.objects.create(course=self.course, user=self.user)

        response = self.auth_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['is_subscribed'])
