from abc import ABC, abstractmethod

import openai
import os

from pydantic import BaseModel

from llm_rpg.llm.llm_cost_tracker import LLMCostTracker


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
    def __init__(
        self,
        llm_cost_tracker: LLMCostTracker,
        model: str = "llama-3.3-70b-versatile",
    ):
        if not os.environ.get("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY is not set")
        self.client = openai.OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.model = model
        self.pricing = {
            "llama-3.3-70b-versatile": {
                "input_token_price": 0.59 / 1000000,
                "output_token_price": 0.79 / 1000000,
            }
        }
        self.llm_cost_tracker = llm_cost_tracker

    def generate_completion(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        self._calculate_completion_costs(response)
        return response.choices[0].message.content

    def _calculate_completion_costs(self, response: openai.types.Completion):
        input_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        input_cost = input_tokens * self.pricing[self.model]["input_token_price"]
        completion_cost = (
            completion_tokens * self.pricing[self.model]["output_token_price"]
        )

        self.llm_cost_tracker.add_cost(
            input_tokens, completion_tokens, input_cost, completion_cost
        )

    def generate_structured_completion(
        self, prompt: str, output_model: BaseModel
    ) -> BaseModel:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        parsed_output = output_model.model_validate_json(
            response.choices[0].message.content
        )
        self._calculate_completion_costs(response)
        return parsed_output
