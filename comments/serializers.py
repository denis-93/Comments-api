from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment, Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ('id',)


class CommentSerializerDepth3(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    post = serializers.SlugRelatedField(slug_field='title', queryset=Post.objects.all())
    parent = serializers.SlugRelatedField(slug_field='id', queryset=Comment.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'post', 'parent', 'children', 'created_at')
        read_only_fields = ('id',)
        depth = 1


class CommentSerializerDepth2(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    post = serializers.SlugRelatedField(slug_field='title', queryset=Post.objects.all())
    parent = serializers.SlugRelatedField(slug_field='id', queryset=Comment.objects.all(), required=False)
    children = CommentSerializerDepth3(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'post', 'parent', 'children', 'created_at')
        read_only_fields = ('id',)
        depth = 1


class CommentSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    post = serializers.SlugRelatedField(slug_field='title', queryset=Post.objects.all())
    parent = serializers.SlugRelatedField(slug_field='id', queryset=Comment.objects.all(), required=False)
    children = CommentSerializerDepth2(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'post', 'parent', 'children', 'created_at')
        read_only_fields = ('id',)
        depth = 1


class CommentInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('user', 'text', 'post', 'parent')


class PostSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text', 'comments')
        read_only_fields = ('id',)
