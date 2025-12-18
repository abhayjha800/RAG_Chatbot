from pydantic import BaseModel


class QueryRequest(BaseModel):
    user_id: int
    text: str

class HistoryRequest(BaseModel):
    user_id: int

class UserRequest(BaseModel):
    username: str