import pytest
from django.test import RequestFactory

from central_database.users.api.views import UserViewSet
from central_database.users.models import User

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "url": f"http://testserver/api/users/{user.username}/",
            "client": {
                "client_name": user.client.client_name,
                "city": user.client.city,
            },
        }
