from pydantic import BaseModel, Field, field_validator, ConfigDict


class Post(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    userId: int = Field(..., gt=0, description="ID автора поста")
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Заголовок не может быть пустым или состоять из пробелов")
        return v.strip()


data = {"userId": 1, "id": 1, "title": "  Hello  ", "body": "World"}
post = Post.model_validate(data)
print(post.title)
