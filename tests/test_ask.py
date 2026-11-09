from my_project.api import deps
from my_project.api.deps import get_openai_service
from my_project.core.config import Settings
from my_project.main import app
from my_project.schemas.ask import AskResponse
from my_project.services.openai_service import LLMServiceError


class FakeOpenAIService:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    def ask(self, question: str) -> AskResponse:
        if self.fail:
            raise LLMServiceError("boom")
        return AskResponse(question=question, answer="42", model="fake-model")


def test_ask_returns_answer(client):
    app.dependency_overrides[get_openai_service] = FakeOpenAIService
    resp = client.post("/ask", json={"question": " What is Docker? "})
    assert resp.status_code == 200
    assert resp.json() == {
        "question": "What is Docker?",
        "answer": "42",
        "model": "fake-model",
    }


def test_ask_rejects_empty_question(client):
    app.dependency_overrides[get_openai_service] = FakeOpenAIService
    assert client.post("/ask", json={"question": "   "}).status_code == 422


def test_ask_upstream_error_returns_502(client):
    app.dependency_overrides[get_openai_service] = lambda: FakeOpenAIService(fail=True)
    assert client.post("/ask", json={"question": "hi"}).status_code == 502


def test_ask_without_key_returns_503(client, monkeypatch):
    monkeypatch.setattr(deps, "get_settings", lambda: Settings(openai_api_key=""))
    assert client.post("/ask", json={"question": "hi"}).status_code == 503
