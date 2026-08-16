import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI


@dataclass
class SLMResponse:
    text: str
    model: str


class SmallLanguageModel:
    """Small-talk model served by Microsoft Foundry Local."""

    def __init__(self):
        load_dotenv()

        self.model_name = os.getenv(
            "SLM_MODEL",
            "phi-4-mini",
        )

        base_url = os.getenv(
            "FOUNDRY_LOCAL_BASE_URL",
            "http://127.0.0.1:64826/v1",
        )

        self.client = OpenAI(
            base_url=base_url,
            api_key="local",
        )

    def generate(
        self,
        query: str,
    ) -> SLMResponse:

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise conversational assistant. "
                        "Handle greetings, thanks, farewells, and simple "
                        "general conversation. Do not answer household "
                        "financial analysis questions."
                    ),
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            temperature=0.3,
            max_tokens=100,
        )

        response_text = (
            completion.choices[0]
            .message
            .content
        )

        return SLMResponse(
            text=response_text,
            model=self.model_name,
        )