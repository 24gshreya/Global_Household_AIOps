import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class AzureFoundryResponse:
    text: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None


class AzureFoundryLLM:

    def __init__(self):
        base_url = os.getenv(
            "AZURE_FOUNDRY_OPENAI_BASE_URL"
        )

        api_key = os.getenv(
            "AZURE_FOUNDRY_API_KEY"
        )

        deployment_name = os.getenv(
            "AZURE_FOUNDRY_DEPLOYMENT"
        )

        if not base_url:
            raise ValueError(
                "AZURE_FOUNDRY_OPENAI_BASE_URL is missing."
            )

        if not api_key:
            raise ValueError(
                "AZURE_FOUNDRY_API_KEY is missing."
            )

        if not deployment_name:
            raise ValueError(
                "AZURE_FOUNDRY_DEPLOYMENT is missing."
            )

        self.deployment_name = deployment_name

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def generate(
        self,
        query: str,
        context: str,
    ) -> AzureFoundryResponse:

        completion = (
            self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer only from the supplied "
                            "household context. Do not invent facts."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Context:\n{context}\n\n"
                            f"Question:\n{query}"
                        ),
                    },
                ],
            )
        )

        usage = completion.usage

        return AzureFoundryResponse(
            text=completion.choices[0].message.content,
            model=self.deployment_name,
            input_tokens=(
                usage.prompt_tokens
                if usage
                else None
            ),
            output_tokens=(
                usage.completion_tokens
                if usage
                else None
            ),
        )