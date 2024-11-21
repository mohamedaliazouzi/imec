from unittest.mock import patch

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    """Fixture to provide an APIClient instance."""
    return APIClient()


@pytest.fixture
def create_user():
    """Fixture to create a user."""
    return User.objects.create_user(username="newuser",email="newuser@example.com",password="testpassword")


@pytest.mark.django_db
@patch('api.views.group_users.delay')
def test_user_registration_view(mock_group_users, api_client):
    """Test the UserRegistrationView."""
    data = {
        "username": "newuser",
        "password": "newpassword",
        "email": "newuser@example.com",
        "attributes": [
            {"name": "Profession", "value": "engineer"},
            {"name": "Location", "value": "Belgium"},
            {"name": "Interest", "value": "Gaming"},
            {"name": "Level", "value": "starter"}
        ],
    }

    response = api_client.post("/api/register/", data, format='json')
    mock_group_users.assert_called_once()
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "User registered successfully"
    assert response.data["user"] == "newuser"

    bad_data_1 = data.copy()
    bad_data_1.pop("username")
    response = api_client.post("/api/register/", bad_data_1, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data

    bad_data_2 = data.copy()
    bad_data_2["attributes"] = "invalid_attributes"
    response = api_client.post("/api/register/", bad_data_2, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "attributes" in response.data

    bad_data_3 = data.copy()
    bad_data_3.pop("password")
    response = api_client.post("/api/register/", bad_data_3, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data

    bad_data_4 = data.copy()
    bad_data_4["email"] = "invalid-email"
    response = api_client.post("/api/register/", bad_data_4, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
    print(response.data)

@pytest.mark.django_db
def test_custom_token_obtain_pair_view(api_client, create_user):
    """Test the CustomTokenObtainPairView."""
    data = {"username": "newuser", "email": "newuser@example.com", "password": "testpassword"}

    response = api_client.post("/api/token/", data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

#
# @pytest.mark.django_db
# def test_get_paired_users(api_client, create_user):
#     """Test the get_paired_users function."""
#     # Create a dummy group and user attribute to simulate pairing logic
#     group = Group.objects.create(name="Test Group")
#     attribute = Attribute.objects.create(name="Test Attribute")
#     user_attribute = UserAttribute.objects.create(user=create_user, attribute=attribute)
#     group.attributes.add(attribute)
#
#     # Create a paired user
#     paired_user = User.objects.create_user(username="paireduser", password="testpassword")
#     UserAttribute.objects.create(user=paired_user, attribute=attribute)
#
#     response = api_client.get(f"/api/paired-users/{create_user.id}/")
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data["paired_users"]) == 1
#     assert response.data["paired_users"][0]["username"] == "paireduser"
#
#
# @pytest.mark.django_db
# def test_attribute_list_view(api_client):
#     """Test the AttributeListView."""
#     Attribute.objects.create(name="Attribute 1")
#     Attribute.objects.create(name="Attribute 2")
#
#     response = api_client.get("/api//attributes/")
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) == 2
#
#
# @pytest.mark.django_db
# def test_group_list_view(api_client):
#     """Test the GroupListView."""
#     Group.objects.create(name="Group 1")
#     Group.objects.create(name="Group 2")
#
#     response = api_client.get("/api/groups/")  # Update URL based on your URL configuration.
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) == 2
#
#
#
#
# @pytest.mark.django_db
# def test_user_attribute_list_view(api_client):
#     """Test the UserAttributeListView."""
#     attribute = Attribute.objects.create(name="Attribute 1")
#     UserAttribute.objects.create(user=User.objects.create_user(username="user1"), attribute=attribute)
#     UserAttribute.objects.create(user=User.objects.create_user(username="user2"), attribute=attribute)
#
#     response = api_client.get("/api/user-attributes/")
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) == 2
