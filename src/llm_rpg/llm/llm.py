from abc import ABC, abstractmethod
import json
from dotenv import load_dotenv
import openai
import os

from pydantic import BaseModel, Field


# Abstract LLM class
class LLM(ABC):
    @abstractmethod
    def generate_completion(self, prompt: str) -> str:
        pass

    @abstractmethod
    def generate_structured_completion(
        self, prompt: str, output_schema: BaseModel
    ) -> BaseModel:
        pass


class GroqLLM(LLM):
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.client = openai.OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.model = model

    def generate_completion(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def generate_structured_completion(
        self, prompt: str, output_schema: BaseModel
    ) -> BaseModel:
        json_schema = json.dumps(output_schema.model_json_schema(), indent=2)

        output_format_instruction = (
            f"Output the result in the following JSON format: {json_schema}"
        )

        prompt = f"{prompt}\n\n{output_format_instruction}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return output_schema.model_validate_json(response.choices[0].message.content)
