from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, CommentSerializer, CommentInputSerializer, PostSerializer
from .models import Comment, Post


class RegisterAccount(APIView):

    def post(self, request, *args, **kwargs):
        """ Регистрация пользователя """
        if {'username', 'email', 'password'}.issubset(request.data):
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                for item in password_error:
                    error_array.append(item)
                return Response({'Status': False, 'Errors': {'password': error_array}}, status=400)
            else:
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    return Response({'Status': True}, status=201)
                else:
                    return Response({'Status': False, 'Errors': user_serializer.errors}, status=400)
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'}, status=400)


class LoginAccount(APIView):

    def post(self, request, *args, **kwargs):
        """ Логинимся и получаем токен """
        if {'username', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['username'], password=request.data['password'])
            if user is not None:
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'Status': True, 'Token': token.key}, status=201)
            return Response({'Status': False, 'Errors': 'Не удалось авторизовать'}, status=400)
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'}, status=400)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Только для зарегистрированных пользователей'}, status=401)
        data = request.data
        if data.get('post') == None and data.get('parent') == None:
            return Response({'Status': False, 'Error': 'Нет необходимых аргументов'}, status=400)
        data['user'] = request.user.id
        serializer = CommentInputSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)


class PostViewSet(ModelViewSet):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Error': 'Только для зарегистрированных пользователей'}, status=401)
        data = request.data
        data['author'] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
