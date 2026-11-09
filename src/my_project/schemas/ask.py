from pydantic import BaseModel, ConfigDict, Field


class AskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    question: str = Field(min_length=1, max_length=4000, examples=["What is Docker?"])


class AskResponse(BaseModel):
    question: str
    answer: str
    model: str
