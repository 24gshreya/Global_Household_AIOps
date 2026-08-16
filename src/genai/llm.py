import os
from dataclasses import dataclass

from dotenv import load_dotenv
from google import genai

from src.genai.prompts import load_prompt


@dataclass
class LLMResponse:
    text: str
    model: str
    prompt_version: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None


class HouseholdLLM:
    """Hosted LLM used for grounded household-domain answers."""

    def __init__(self):
        load_dotenv()

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.model_name = os.getenv(
            "LLM_MODEL",
            "gemini-3.6-flash",
        )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(
        self,
        query: str,
        context: str | None = None,
    ) -> LLMResponse:

        if not context:
            return LLMResponse(
                text=(
                    "I do not have enough retrieved "
                    "household context to answer."
                ),
                model=self.model_name,
            )

        system_prompt, prompt_version = (
            load_prompt(
                "household_system"
            )
        )

        prompt = f"""
            {system_prompt}

            Context:
            {context}

            Question:
            {query}

            Answer:
        """

        response = (
            self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
        )

        usage = getattr(
            response,
            "usage_metadata",
            None,
        )

        input_tokens = getattr(
            usage,
            "prompt_token_count",
            None,
        )

        output_tokens = getattr(
            usage,
            "candidates_token_count",
            None,
        )

        return LLMResponse(
            text=response.text,
            model=self.model_name,
            prompt_version=prompt_version,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )