import time

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .serializers import (
    LoginSerializer,
    PhoneSerializer,
    LoginFromCodeSerializer,
    LoginSerializerFromAPI,
    PhoneSerializerConfirmAPI
)
from .jwt_helpers import decode_token2dict

User = get_user_model()


class SerializerTests(TestCase):
    def test_login_serializer_from_api(self):
        data = {
            "password": "123456",
            "phone": "77779001234",
            "app_name": "aqsha",
        }

        serializer = LoginSerializerFromAPI(data=data)

        self.assertTrue(serializer.is_valid())

        # test token
        token = "1234567890"
        serializer.validated_data["token"] = token

        self.assertTrue(serializer.data["token_app"])
        data_decode = decode_token2dict(serializer.data["token_app"])

        self.assertTrue(data_decode)

        self.assertEqual(data_decode["token"], serializer.data["token"])

    def test_phone_serializer_api(self):
        data = {
            "phone": "77779001234",
            "confirmCode": "1213124",
            "app_name": "aqsha",
        }

        serializer = PhoneSerializerConfirmAPI(data=data)

        self.assertTrue(serializer.is_valid())

        # test token
        token = "1234567890"
        serializer.validated_data["token"] = token

        self.assertTrue(serializer.data["token_app"])
        data_decode = decode_token2dict(serializer.data["token_app"])

        self.assertTrue(data_decode)
        print("data_decode: ", data_decode)

        # токены должны совпадать
        self.assertEqual(data_decode["token"], serializer.data["token"])

        # поле app_name должно совпадать с app
        self.assertEqual(data_decode["app"], data["app_name"])

        # проверим срок жизни токена, он составляет 60 сек, после этого
        # времени функция decode_token2dict вернет None
        time.sleep(61)
        data_decode_empty = decode_token2dict(serializer.data["token_app"])
        self.assertFalse(data_decode_empty)


class AuthTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="press.83@list.ru", email="press.83@list.ru", password="qwerty1234")
        user.profile.phone = "12345678910"
        user.save()

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_create_profile(self):
        try:
            user = User.objects.get(email="press.83@list.ru")

        except User.DoesNotExist:
            print("Not Found User")
            self.assertTrue(False)
            return

        print("Profile Created: ", user.profile.phone)
        self.assertTrue(True)

    def test_jwt_auth(self):
        data = {"username": "press.83@list.ru", "password": "qwerty1234"}
        serializer = LoginSerializer(data=data)
        res = serializer.is_valid(raise_exception=True)
        self.assertTrue(res)
        print("Auth Token", serializer.data)

    def test_phone_auth(self):
        data = {"phone": "12345678910"}
        serializer = PhoneSerializer(data=data)

        res = serializer.is_valid(raise_exception=True)
        serializer.save()
        print("Get SMS code: ", serializer.data)
        serializerCode = LoginFromCodeSerializer(data={'code': serializer.data['code'], "phone": "12345678910"})
        time.sleep(3)
        res = serializerCode.is_valid(raise_exception=True)
        print("Login from SMS: ", serializerCode.data)

        self.assertTrue(res)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
