from django.test import TestCase

from .serializers import TokenSerializer, RefreshEmailSerializer, RefreshPasswordSerializer


class TestSerializersApp(TestCase):
    def test_token_serializer(self):
        data = {}

        serializer = TokenSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        data["token"] = "34231543tw3gfw363456534tge45h357673776"
        serializer = TokenSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_refresh_email_serializer(self):
        data = {
            "token": "34231543tw3gfw363456534tge45h357673776",
            "newEmail": "fake"
        }

        serializer = RefreshEmailSerializer(data=data)

        # фейковый эмайл не пройдет валидацию
        self.assertFalse(serializer.is_valid())

        data["newEmail"] = "test@test.kz"
        serializer = RefreshEmailSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_refresh_password_serializer(self):
        data = {
            "token": "34231543tw3gfw363456534tge45h357673776",
            "oldPassword": "password",
            "newPassword": ""
        }

        serializer = RefreshPasswordSerializer(data=data)

        # пустой пароль не пройдет
        self.assertFalse(serializer.is_valid())

        data["newPassword"] = "password_newPassword"
        serializer = RefreshPasswordSerializer(data=data)

        self.assertTrue(serializer.is_valid())
