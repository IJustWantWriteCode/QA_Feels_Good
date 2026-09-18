import pytest
import requests
import responses
from pydantic import BaseModel, Field, field_validator, ConfigDict

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
            raise ValueError("Text must not contain 'lorem ipsum'")
        return v


@responses.activate
@pytest.mark.parametrize(
    ("post_id", "title", "status_code"),
    [
        (1, "Mocked", 200),
        (2, "Maybe_Mocked", 201),
    ],
)
def test_get_post_success(api_session, post_id, title, status_code):
    responses.add(
        responses.GET,
        f"{BASE_URL}/posts/{post_id}",
        json={"userId": 1, "id": post_id, "title": title, "body": "Test"},
        status=status_code,
    )

    response = api_session.get(f"{BASE_URL}/posts/{post_id}", timeout=TIMEOUT)

    assert response.status_code == status_code
    post = Post.model_validate(response.json())
    assert post.title == title


@responses.activate
@pytest.mark.parametrize(
    ("post_id", "status_code"),
    [
        (3, 400),
        (4, 404),
        (5, 500),
    ],
)
def test_get_post_errors(api_session, post_id, status_code):
    responses.add(
        responses.GET,
        f"{BASE_URL}/posts/{post_id}",
        json={"error": "Client/Server Error"},
        status=status_code,
    )

    response = api_session.get(f"{BASE_URL}/posts/{post_id}", timeout=TIMEOUT)
    assert response.status_code == status_code


def test_get_post_with_mocker(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "userId": 1,
        "id": 10,
        "title": "title",
        "body": "body",
    }

    mock_get = mocker.patch("requests.get", return_value=mock_response)

    response = requests.get(f"{BASE_URL}/posts/10", timeout=TIMEOUT)

    assert response.status_code == 200
    post = Post.model_validate(response.json())
    assert post.title == "title"

    mock_get.assert_called_once_with(f"{BASE_URL}/posts/10", timeout=TIMEOUT)
