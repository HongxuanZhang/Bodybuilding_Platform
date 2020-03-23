from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from .models import *
from .serializers import *


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def list(self, request, *args, **kwargs):
        serializer = CourseSerializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def run_create_or_update(self, request, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        return self.run_create_or_update(request, serializer)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        return self.run_create_or_update(request, serializer)


class RegList(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        res = RegSerializers(data=request.data)
        if res.is_valid():
            res.save()
            return Response(data=res.validated_data, status=status.HTTP_201_CREATED)
        return Response(res.errors)

    def put(self, request, format=None):
        username = request.data['username']
        user = User.objects.get(username=username)
        if user.status == 'Normal':
            user.status = 'Locked'
        else:
            user.status = 'Normal'
        res = UserListSerializers(user, user.__dict__())
        if res.is_valid():
            res.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(res.errors)


class LogList(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        data = request.data
        res = LogSerializers(data=data)
        if res.is_valid():
            return Response(data=res.validated_data, status=status.HTTP_202_ACCEPTED)
        return Response(res.errors)


class UserOperationSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializers
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def list(self, request, *args, **kwargs):
        serializer = UserListSerializers(self.queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        newpwd = request.data['newpwd']
        confirmpwd = request.data['confirmpwd']
        username = request.data['username']
        user = User.objects.get(username=username)
        user.password = newpwd
        userdict = user.__dict__()
        userdict['confirmpwd'] = confirmpwd
        res = RegSerializers(instance=user, data=userdict)
        if res.is_valid():
            res.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(res.errors)
