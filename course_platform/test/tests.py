import json
from django.test import TestCase
from course_platform.models import *
from rest_framework import status
from rest_framework.test import APIClient


class UserTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_basic_userop(self):
        data = {
            'username': "Tom",
            "password": "1234567",
            "confirmpwd": "1234567",
            "email": "725641242@qq.com",
            "tel": "13652362397",
            "age": "18",
            "sex": "M"
        }
        response = self.client.post("/api/v1/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {"username": "Tom", "password": "1234567", "isAdmin": False}
        response = self.client.post("/api/v1/login/", data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        tmpdata = data
        tmpdata["password"] = "ewnufwrg"
        response = self.client.post("/api/v1/login/", tmpdata)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data["isAdmin"] = True
        response = self.client.post("/api/v1/login/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        data = {"username": "Tom"}
        response = self.client.put("/api/v1/register/", data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        user = User.objects.get(username="Tom")
        self.assertEqual(user.status, "Locked")

        response = self.client.put("/api/v1/register/", data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        user = User.objects.get(username="Tom")
        self.assertEqual(user.status, "Normal")

    def test_extra_userop(self):
        data = [{
            'username': "Tom",
            "password": "1234567",
            "confirmpwd": "1234567",
            "email": "725641242@qq.com",
            "tel": "13652362397",
            "age": "18",
            "sex": "M"
        }, {
            'username': "Alice",
            "password": "1234567",
            "confirmpwd": "1234567",
            "email": "725641242@qq.com",
            "tel": "13652362397",
            "age": "19",
            "sex": "F"
        }]
        for i in range(len(data)):
            self.client.post("/api/v1/register/", data[i])
        response = self.client.get("/api/v1/user_service/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        print(response.__dict__['data'])
        data2 = {'username': 'Tom', 'newpwd': 'qazwsxedcrfv', 'confirmpwd': 'qazwsxedcrfv'}
        response = self.client.post("/api/v1/user_service/", data2)
        self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
        del data2['newpwd']
        del data2['confirmpwd']
        data2['password'] = 'qazwsxedcrfv'
        data2['isAdmin'] = False
        response = self.client.post("/api/v1/login/", data2)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        pass


class CourseTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_basic_course(self):
        data = {"name": "第三套中学生广播体操", "description": "广播体操官方授权", "tag": '健美'}
        response = self.client.post("/api/v1/course/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/v1/course/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.__dict__['data'])
