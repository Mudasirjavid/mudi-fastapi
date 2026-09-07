from app import schemas
import pytest
from jose import jwt
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("data"))
#     assert res.json().get("data") == "Bind mount working fine and working!"


def test_create_user(client):
    res = client.post(
        "/users/",
        json={"email": "testkhan@gamil.com", "password": "testpassword"},
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "testkhan@gamil.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("testkhan@gamil.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "testpassword", 403),
        ("testkhan@gamil.com", "wrongpassword", 403),
        (None, "testpassword", 422),
        ("testkhan@gamil.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"


def test_delete_post_success(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
