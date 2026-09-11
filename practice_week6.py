from pydantic import BaseModel, Field, field_validator, ConfigDict, TypeAdapter

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10


class Post(BaseModel):

    model_config = ConfigDict(extra="ignore")

    userId: int = Field(..., gt=0, description="user id")
    id: int = Field(..., gt=0, description="id")
    title: str = Field(..., min_length=1, description="title")
    body: str = Field(..., min_length=1, description="body")

    @field_validator("body")
    @classmethod
    def body_must_not_be_dummy_placeholder(cls, v: str) -> str:
        if "lorem ipsum" in v.lower():
            raise ValueError("Text does not contain 'lorem ipsum'")
        return v


class User(BaseModel):

    model_config = ConfigDict(extra="ignore")

    id: int = Field(..., gt=0, description="user id")
    username: str = Field(..., min_length=1, description="username")
    email: str = Field(..., min_length=1, description="email")

    @field_validator("email")
    @classmethod
    def email_validator(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("email must be in format of ")
        return v


def test_get_post_validates_with_pydantic(api_session):
    response = api_session.get(f"{BASE_URL}/posts/1", timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()
    post = Post.model_validate(data)
    assert post.id == 1, "id should be 1"
    assert post.userId == 1, "userId should be 1"


def test_get_posts_by_user_id(api_session):
    response = api_session.get(f"{BASE_URL}/posts?userId=1", timeout=TIMEOUT)
    response.raise_for_status()
    posts_adapter = TypeAdapter(list[Post])
    posts = posts_adapter.validate_python(response.json())
    assert len(posts) > 0, "response don`t should be empty"


def test_create_post_returns_201_and_validates(api_session):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }

    body = {"title": "title", "body": "body", "userId": 1}

    response = api_session.post(f"{BASE_URL}/posts", headers=headers, json=body)
    response.raise_for_status()
    assert response.status_code == 201, "status_code should be 201"
    data = response.json()
    posts = Post.model_validate(data)
    assert posts.userId == 1, "userId should be 1"
    assert posts.title == "title", "title should be 'title'"
    assert posts.body == "body", "body should be 'body'"


def test_delete_post_returns_200_or_204(api_session):
    response = api_session.delete(f"{BASE_URL}/posts/1", timeout=TIMEOUT)
    response.raise_for_status()
    assert (
        response.status_code == 204 or response.status_code == 200
    ), "status_code should be 204 or 200"
    data = response.json()
    assert data == {}, "data should be empty"
