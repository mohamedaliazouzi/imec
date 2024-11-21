from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import CustomTokenObtainPairView, UserRegistrationView, get_paired_users, AttributeListView, \
    GroupListView, UserAttributeListView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:user_id>/paired/', get_paired_users, name='get_paired_users'),
    path('attributes/', AttributeListView.as_view(), name='attribute-list'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('user-attributes/', UserAttributeListView.as_view(), name='user-attribute-list'),
]