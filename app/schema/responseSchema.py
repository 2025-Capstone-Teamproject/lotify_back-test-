# 클라측에 보낼 Response Data
# 토의되면 사용(현재 X)

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True