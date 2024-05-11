# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.throttling import ScopedRateThrottle
from .models import User, UserData,UserLoginData
from .serializers import UserSerializer, UserDataSerializer, UserNoPassSerializer, UserNoTypeSerializer, UserLoginDataSerializer
from .permission import UserSafePostOnly, UserPUTOnly, AuthPUTOnly,ManagerOnly
from board.models import SettingBoard

def getRegisterPermission(request):
    setting = SettingBoard.objects.filter(id=1)
    if len(setting) != 0:
        if setting[0].openregister is False:
            return False
        else:
            return True
    else:
        return True


class UserDataView(viewsets.ModelViewSet):
    queryset = UserData.objects.extra(select = { '_has' : 'if(rating=1500,0,rating)'}).order_by('-_has')
    serializer_class = UserDataSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username',)
    permission_classes = (UserSafePostOnly,)
    pagination_class = LimitOffsetPagination
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserNoPassSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('username',)
    search_fields = ('username', 'name','realname','course','classes','school','number','qq')
    permission_classes = (UserSafePostOnly,)
    pagination_class = LimitOffsetPagination
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class UserChangeView(APIView):

    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def put(self, request, format=None):
        data = request.data.copy()
        username = request.session.get('user_id', None)
        if username != None:
            user = User.objects.get(username=username)
            user.password = data["password"]
            user.name = data["name"]
            user.school = data["school"]
            user.course = data["course"]
            user.classes = data["classes"]
            user.number = data["number"]
            user.realname = data["realname"]
            user.qq = data["qq"]
            user.email = data["email"]
            user.save()
            user2 = UserData.objects.get(username=username)
            user2.des=data["des"]
            user2.save()

            return Response("ok", status=HTTP_200_OK)

        return Response("nologin", status=HTTP_400_BAD_REQUEST)


class UserChangeAllView(APIView):
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def put(self, request, format=None):
        if request.session.get('type',None) != 3:
            return Response("no permission", status=HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        username = data["username"]
        if username != None:
            user = User.objects.get(username=username)
            if data["password"] != ".":
                user.password = data["password"]
            user.name = data["name"]
            user.school = data["school"]
            user.course = data["course"]
            user.classes = data["classes"]
            user.number = data["number"]
            user.realname = data["realname"]
            user.qq = data["qq"]
            user.email = data["email"]
            user.type = data["type"]
            user.save()
            return Response("ok", status=HTTP_200_OK)
        return Response("username error", status=HTTP_400_BAD_REQUEST)

class UserLoginDataView(viewsets.ModelViewSet):
    queryset = UserLoginData.objects.all().order_by('-id')
    serializer_class = UserLoginDataSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('username','ip',)
    search_fields = ('username', 'ip')
    permission_classes = (ManagerOnly,)
    pagination_class = LimitOffsetPagination
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

class UserLoginDataAPIView(APIView):
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def post(self, request, format=None):
        data = request.data.copy()
        
        ip = "获取失败"
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]#所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')#这里获得代理ip
        
        data["msg"] = request.META.get("HTTP_USER_AGENT","获取失败")
        data["ip"] = ip
        print(data)
        serializer = UserLoginDataSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('ok', status=HTTP_200_OK)



class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.get(username__exact=username)
        userdata = UserData.objects.get(username__exact=username)
        if user.password == password:
            serializer = UserSerializer(user)
            new_data = serializer.data
            request.session['user_id'] = user.username
            request.session['type'] = user.type
            request.session['rating'] = userdata.rating
            return Response(new_data, status=HTTP_200_OK)
        return Response('passworderror', HTTP_200_OK)


class UserUpdateRatingAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def get(self, request, format=None):
        if request.session.get('user_id', None) is not None:
            username = request.session.get('user_id', None)
            userdata = UserData.objects.get(username__exact=username)
            request.session['rating'] = userdata.rating
            return Response('updated', HTTP_200_OK)
        else:
            return Response('ok', HTTP_200_OK)


class UserLogoutAPIView(APIView):
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def get(self, request):
        if request.session.get('user_id', None) is not None:
            del request.session['user_id']
        if request.session.get('type', None) is not None:
            del request.session['type']
        if request.session.get('rating', None) is not None:
            del request.session['rating']
        return Response('ok', HTTP_200_OK)


class UserRegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def post(self, request, format=None):
        if getRegisterPermission(request) == False:
            return Response('register is not allow on this oj !!', status=HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['type'] = 1
        username = data.get('username')
        if User.objects.filter(username__exact=username):
            return Response("usererror", HTTP_200_OK)
        serializer = UserSerializer(data=data)
        serializer2 = UserDataSerializer(data=data)
        if serializer.is_valid(raise_exception=True) and serializer2.is_valid(raise_exception=True):
            serializer.save()
            serializer2.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
