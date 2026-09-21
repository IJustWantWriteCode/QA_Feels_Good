from typing import Any

import allure
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, field_validator
from requests import Session

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
            raise ValueError("Text contains prohibited 'lorem ipsum' placeholder")
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
            raise ValueError("Email must contain '@' symbol")
        return v


def test_get_post_validates_with_pydantic(api_session: Session) -> None:
    POST_ID = 1

    with allure.step(f"Отправка GET-запроса на получение поста ID={POST_ID}"):
        response = api_session.get(f"{BASE_URL}/posts/{POST_ID}", timeout=TIMEOUT)
        response.raise_for_status()

    with allure.step("Валидация структуры ответа через Pydantic-схему Post"):
        data = response.json()
        post = Post.model_validate(data)

    with allure.step(f"Проверка соответствия id={POST_ID} и userId={POST_ID}"):
        assert post.id == POST_ID, f"Expected id to be {POST_ID}, got {post.id}"
        assert (
            post.userId == POST_ID
        ), f"Expected userId to be {POST_ID}, got {post.userId}"


def test_get_posts_by_user_id(api_session: Session) -> None:
    USER_ID = 1

    with allure.step(f"Отправка GET-запроса постов для userId={USER_ID}"):
        response = api_session.get(
            f"{BASE_URL}/posts?userId={USER_ID}", timeout=TIMEOUT
        )
        response.raise_for_status()

    with allure.step("Валидация списка постов через TypeAdapter(list[Post])"):
        posts_adapter = TypeAdapter(list[Post])
        posts = posts_adapter.validate_python(response.json())

    with allure.step("Проверка, что список постов не пуст"):
        assert len(posts) > 0, "Response list should not be empty"


def test_create_post_returns_201_and_validates(api_session: Session) -> None:
    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }
    body: dict[str, Any] = {"title": "title", "body": "body", "userId": 1}

    with allure.step("Отправка POST-запроса на создание поста"):
        response = api_session.post(
            f"{BASE_URL}/posts", headers=headers, json=body, timeout=TIMEOUT
        )
        response.raise_for_status()

    with allure.step("Проверка HTTP статус-кода 201 Created"):
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    with allure.step("Валидация созданного объекта через Pydantic"):
        data = response.json()
        created_post = Post.model_validate(data)

    with allure.step("Проверка соответствия отправленных и возвращённых данных"):
        assert created_post.userId == 1, "userId should be 1"
        assert created_post.title == "title", "title should be 'title'"
        assert created_post.body == "body", "body should be 'body'"


def test_delete_post_returns_200_or_204(api_session: Session) -> None:
    POST_ID = 1

    with allure.step(f"Отправка DELETE-запроса для удаления поста ID={POST_ID}"):
        response = api_session.delete(f"{BASE_URL}/posts/{POST_ID}", timeout=TIMEOUT)
        response.raise_for_status()

    with allure.step("Проверка успешного статус-кода (200 OK или 204 No Content)"):
        assert response.status_code in (
            200,
            204,
        ), f"Unexpected status code: {response.status_code}"

    with allure.step("Проверка, что тело ответа пустое"):
        data = response.json()
        assert data == {}, "Response body should be an empty dict"
