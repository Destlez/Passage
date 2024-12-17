import json

from django.template.defaultfilters import title
from django.test import TestCase
from django.urls import reverse

from .models import *
from .serializers import *
from rest_framework.test import APITestCase
from rest_framework import status


class PassagesTests(APITestCase):
    def setUp(self):
        self.passage_1 = Passages.objects.create(
            user=User.objects.create(
                email='test@test.com',
                phone='89991112233',
                fam='Васянов',
                name='Вася',
                otc='Иванович'
            ),
            coordinates=Coordinates.objects.create(
                latitude=23,
                longitude=12,
                height=999
            ),
            level=Levels.objects.create(
                winter='1a',
                summer='1a',
                autumn='1a',
                spring='1a'
            ),
            title='Перевалов',
            beauty_title='Перевал',
            other_title='Перевальный',
            connect='Местный'
        )
        self.image_1 = Images.objects.create(
            passage=self.passage_1,
            title='any title',
            urls='date:image/jpeg;media.istockphoto.com/id/539271875/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B8%D0%B7%D0%B2%D0%B8%D0%BB%D0%B8%D1%81%D1%82%D0%B0%D1%8F-%D0%B4%D0%BE%D1%80%D0%BE%D0%B3%D0%B0-%D0%B2-%D0%B3%D0%BE%D1%80%D1%8B-%D0%B1%D0%B5%D0%B7-%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B5%D0%B9.jpg?s=612x612&w=0&k=20&c=Te0cSOBXQbhPyUGhvl6xGwgBsEfQOid4amG0_ZT-pDw='
        )

    def test_get_list(self):
        url = reverse('passages-list')
        response = self.client.get(url)
        serializer_data = PassagesSerializer([self.passage_1], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_detail(self):
        url = reverse('passage-detail', args=(self.passage_1.id,))
        response = self.client.get(url)
        serializer_data = PassagesSerializer(self.passage_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_passage_update(self):
        url = reverse('passage-detail', args=(self.passage_1.id,))
        data = {
            'user': {
                'email' : 'test@test.com',
                'phone' : '89991112233',
                'fam' : 'Васянов',
                'name' : 'Вася',
                'otc' : 'Иванович'
            },
            'coordinates': {
                'latitude': 23,
                'longitude': 12,
                'height':  999
            },
            'level': {
                'winter' : '1a',
                'summer' : '1a',
                'autumn' : '1a',
                'spring' : '1a'
            },
            'image': [
                {
                'urls': """'date:image/jpeg;media.istockphoto.com/id/539271875/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B8%D0%B7%D0%B2%D0%B8%D0%BB%D0%B8%D1%81%D1%82%D0%B0%D1%8F-%D0%B4%D0%BE%D1%80%D0%BE%D0%B3%D0%B0-%D0%B2-%D0%B3%D0%BE%D1%80%D1%8B-%D0%B1%D0%B5%D0%B7-%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B5%D0%B9.jpg?s=612x612&w=0&k=20&c=Te0cSOBXQbhPyUGhvl6xGwgBsEfQOid4amG0_ZT-pDw='""",
                'title': 'any title'
                }
            ],
            'title' : 'Перевалов',
            'beauty_title' : 'Перевал',
            'other_title' : 'Перевальный',
            'connect' : 'Местный'
        }
        json_data = json.dumps(data)
        response = self.client.patch(path=url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.passage_1.refresh_from_db()
        self.assertEqual('Перевал изменен', self.passage_1.beauty_title)
        self.assertEqual('1a', self.passage_1.level.winter)
        self.assertEqual(1000, self.passage_1.coordinates.height)

        def test_user_email(self):
            email = self.passage_1.user.email
            url = f'/passages/?user__email=<{email}>'
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_create(self):
            url = reverse('passage-list')
            data = {
                'user': {
                    'email' : 'test@test.com',
                    'phone' : '89991112233',
                    'fam' : 'Васянов',
                    'name' : 'Вася',
                    'otc' : 'Иванович'
                },
                'coordinates': {
                    'latitude': 23,
                    'longitude': 12,
                    'heitht':  999
                },
                'level': {
                    'winter' : '1a',
                    'summer' : '1a',
                    'autumn' : '1a',
                    'spring' : '1a'
                },
                'image': [
                    {
                    'urls': """'date:image/jpeg;media.istockphoto.com/id/539271875/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B8%D0%B7%D0%B2%D0%B8%D0%BB%D0%B8%D1%81%D1%82%D0%B0%D1%8F-%D0%B4%D0%BE%D1%80%D0%BE%D0%B3%D0%B0-%D0%B2-%D0%B3%D0%BE%D1%80%D1%8B-%D0%B1%D0%B5%D0%B7-%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B5%D0%B9.jpg?s=612x612&w=0&k=20&c=Te0cSOBXQbhPyUGhvl6xGwgBsEfQOid4amG0_ZT-pDw='""",
                    'title': 'any title'
                    }
                ],
                'title' : 'Перевалов',
                'beauty_title' : 'Перевал',
                'other_title' : 'Перевальный',
                'connect' : 'Местный'
            }
            json_data = json.dumps(data)
            response = self.client.post(path=url, content_type='application/json', data=json_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

class PassageSerializerTestCase(TestCase):
    def setUp(self):
        self.passage_1 = Passages.objects.create(
            user=User.objects.create(
                email='test@test.com',
                phone='89991112233',
                fam='Васянов',
                name='Вася',
                otc='Иванович'
            ),
            coordinates=Coordinates.objects.create(
                latitude=23,
                longitude=12,
                height=999
            ),
            level=Levels.objects.create(
                winter='1a',
                summer='1a',
                autumn='1a',
                spring='1a'
            ),
            title='Перевалов',
            beauty_title='Перевал',
            other_title='Перевальный',
            connect='Местный'
        )
        self.image_1 = Images.objects.create(
            passage=self.passage_1,
            title='any title',
            urls='date:image/jpeg;media.istockphoto.com/id/539271875/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B8%D0%B7%D0%B2%D0%B8%D0%BB%D0%B8%D1%81%D1%82%D0%B0%D1%8F-%D0%B4%D0%BE%D1%80%D0%BE%D0%B3%D0%B0-%D0%B2-%D0%B3%D0%BE%D1%80%D1%8B-%D0%B1%D0%B5%D0%B7-%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B5%D0%B9.jpg?s=612x612&w=0&k=20&c=Te0cSOBXQbhPyUGhvl6xGwgBsEfQOid4amG0_ZT-pDw='
            )

    def test_check(self):
        serializer_data = PassagesSerializer([self.passage_1, ], many=True).data
        expected_data = [
            {
                'id': self.passage_1.id,
                'user': {
                    'email' : 'test@test.com',
                    'phone' : '89991112233',
                    'fam' : 'Васянов',
                    'name' : 'Вася',
                    'otc' : 'Иванович'
                },
                'coordinates': {
                    'latitude': 23,
                    'longitude': 12,
                    'height':  999
                },
                'level': {
                    'winter' : '1a',
                    'summer' : '1a',
                    'autumn' : '1a',
                    'spring' : '1a'
                },
                'image': [
                    {
                    'urls': """'date:image/jpeg;media.istockphoto.com/id/539271875/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B8%D0%B7%D0%B2%D0%B8%D0%BB%D0%B8%D1%81%D1%82%D0%B0%D1%8F-%D0%B4%D0%BE%D1%80%D0%BE%D0%B3%D0%B0-%D0%B2-%D0%B3%D0%BE%D1%80%D1%8B-%D0%B1%D0%B5%D0%B7-%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B5%D0%B9.jpg?s=612x612&w=0&k=20&c=Te0cSOBXQbhPyUGhvl6xGwgBsEfQOid4amG0_ZT-pDw='""",
                    'title': 'any title'
                    }
                ],
                'title' : 'Перевалов',
                'beauty_title' : 'Перевал',
                'other_title' : 'Перевальный',
                'connect' : 'Местный'
            },
        ]

        self.assertEqual(serializer_data, expected_data)