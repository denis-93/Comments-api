from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from .views import CommentViewSet, RegisterAccount, LoginAccount, PostViewSet


app_name = 'comments'
router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='Comment')
router.register(r'posts', PostViewSet, basename='Post')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAccount.as_view()),
    path('login/', LoginAccount.as_view()),
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='comments:schema'), name='swagger')
]
