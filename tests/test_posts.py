## Tareqa 1

# def test_create_posts(client, test_user):

#     login_res = client.post(
#         "/login",
#         data={"username": test_user["email"], "password": test_user["password"]},
#     )
#     token = login_res.json().get("access_token")

#     res = client.post(
#         "/posts/",
#         json={"title": "test title", "content": "test content"},

#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert res.status_code == 201

## Tareqa 2

import pytest
from app import schemas


def test_create_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    post_map = map(validate, res.json())
    post_list = list(post_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/888888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

    @pytest.mark.parametrize(
        "title, content, published",
        [
            ("test title 1", "test content 1", True),
            ("test title 2", "test content 2", False),
            ("test title 3", "test content 3", True),
        ],
    )
    def test_create_post(
        authorized_client, test_user, test_posts, title, content, published
    ):
        res = authorized_client.post(
            "/posts/", json={"title": title, "content": content, "published": published}
        )
        created_post = schemas.PostOut(**res.json())
        assert res.status_code == 201
        assert created_post.title == title
        assert created_post.content == content
        assert created_post.published == published
        assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"}
    )
    created_post = schemas.Posts(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_posts(client, test_posts, test_user):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"}
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_posts(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/888888")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Posts(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_posts, test_user, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_posts(client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put(f"/posts/888888", json=data)
    assert res.status_code == 404
