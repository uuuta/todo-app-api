from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(
        description="ユーザーID 1文字以上32文字以内, 使用可能な文字は英数字アンダースコア(_)ハイフン(-)ドット(.)",
        examples=["user-123"],
        pattern=r"^[a-zA-Z0-9._-]{1,32}$")

    # @validator("id")
    # def id_must_match_regex(cls, value):
    #     if not re.match(r"^[a-zA-Z0-9._-]{1,32}$", value):
    #         raise ValueError("ユーザーIDは1文字以上32文字以内で指定してください。使用可能な文字は英数字アンダースコア(_)ハイフン(-)ドット(.)です。")
    #     return value
