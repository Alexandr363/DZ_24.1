from rest_framework.test import APITestCase
from rest_framework import status


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
