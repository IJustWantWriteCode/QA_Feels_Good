from typing import Any, cast

import allure
import requests
from requests import Session

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10


@allure.step("Отправка GET-запроса на получение поста {post_id}")
def get_post(session: Session, post_id: int) -> dict[str, Any]:
    url = f"{BASE_URL}/posts/{post_id}"
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


with requests.Session() as session:

    def test_validate_get_post() -> None:
        with allure.step("Валидация ответа GET-запроса на получение поста {post_id}"):
            post = get_post(session, 1)
            assert len(post["title"]) > 0, "title don't should be empty"
            print(post["title"])
