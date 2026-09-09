import requests
from requests import Session

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10


def get_post(session: Session, post_id: int) -> dict:
    url = f"{BASE_URL}/posts/{post_id}"
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


with requests.Session() as session:
    post = get_post(session, 1)
    print(post["title"])
