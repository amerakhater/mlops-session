from openai import OpenAI, OpenAIError

from my_project.core.config import Settings
from my_project.schemas.ask import AskResponse


class LLMNotConfiguredError(Exception):
    pass


class LLMServiceError(Exception):
    pass


class OpenAIService:
    def __init__(self, settings: Settings) -> None:
        api_key = settings.openai_api_key.get_secret_value() if settings.openai_api_key else ""
        if not api_key.strip():
            raise LLMNotConfiguredError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)
        self.model = settings.openai_model

    def ask(self, question: str) -> AskResponse:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question},
                ],
            )
        except OpenAIError as exc:
            raise LLMServiceError(str(exc)) from exc

        answer = completion.choices[0].message.content or ""
        return AskResponse(question=question, answer=answer, model=completion.model)
