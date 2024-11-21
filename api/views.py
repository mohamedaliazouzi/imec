from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserRegistrationSerializer, AttributeSerializer, \
    GroupSerializer, UserAttributeSerializer, UserSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from api.models import UserAttribute, Group, Attribute
from api.tasks import group_users


@permission_classes([AllowAny])
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@permission_classes([AllowAny])
class UserRegistrationView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "email", "password", "attributes"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, example="mohamedaliazouzi"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, example="mohamedali.azaouzi@esprit.tn"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, example="password123"),
                "attributes": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Profession"),
                            "value": openapi.Schema(type=openapi.TYPE_STRING, example="azouzim"),
                        },
                    ),
                    example=[
                        {"name": "Profession", "value": "Software Engineer"},
                        {"name": "Location", "value": "Tunis"},
                        {"name": "Interest", "value": "Gaming"},
                        {"name": "Level", "value": "Student"},
                    ],
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "message": "User registered successfully",
                        "user": "mohamedaliazouzi",
                    }
                },
            ),
            400: "Bad Request",
        },
    )
    @permission_classes([AllowAny])
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully", "user": user.username},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Get paired users for a given user ID",
    responses={
        200: openapi.Response(
            description="A list of paired users",
            examples={
                "application/json": [
                    {"id": 1, "name": "User 1"},
                    {"id": 2, "name": "User 2"}
                ]
            }
        ),
        404: "User not found",
    },

    security=[{'Bearer': []}],

)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_paired_users(request, user_id):
    user = get_object_or_404(User, id=user_id)
    groups = Group.objects.filter(attributes__user_attributes__user=user).distinct()
    paired_users = User.objects.filter(
        user_attributes__attribute__groups__in=groups
    ).exclude(id=user_id).distinct()
    response_data = [
        {
            "id": paired_user.id,
            "username": paired_user.username,
            "email": paired_user.email,
        }
        for paired_user in paired_users
    ]
    return JsonResponse({"paired_users": response_data})


class AttributeListView(ListAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all attributes. Requires Bearer token for authentication.",
        security=[{'Bearer': []}],
        responses={200: AttributeSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@swagger_auto_schema(security=[{'Bearer': []}])
class GroupListView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

@swagger_auto_schema(security=[{'Bearer': []}])
class UserAttributeListView(ListAPIView):
    queryset = UserAttribute.objects.all()
    serializer_class = UserAttributeSerializer
    permission_classes = [IsAuthenticated]
