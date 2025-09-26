from abc import ABC, abstractmethod

import openai
import os

from pydantic import BaseModel

from llm_rpg.llm.llm_cost_tracker import LLMCostTracker
from ollama import chat
from ollama import ChatResponse


class LLM(ABC):
    @abstractmethod
    def generate_completion(self, prompt: str) -> str:
        pass

    @abstractmethod
    def generate_structured_completion(
        self, prompt: str, output_schema: BaseModel
    ) -> BaseModel:
        pass



class OpenAILLM(LLM):
    def __init__(
        self,
        llm_cost_tracker: LLMCostTracker,
        model: str = "gpt-4o-mini",
    ):
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is not set")
        # Uses official OpenAI endpoint by default
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model
        # Token pricing per 1M tokens. Update as needed if you use other models.
        # Values are placeholders; adjust to current OpenAI pricing.
        self.pricing = {
            # Approximate pricing; please verify with OpenAI pricing page.
            "gpt-4o-mini": {
                "input_token_price": 0.15 / 1_000_000,
                "output_token_price": 0.60 / 1_000_000,
            },
            "gpt-4o": {
                "input_token_price": 5.00 / 1_000_000,
                "output_token_price": 15.00 / 1_000_000,
            },
        }
        self.llm_cost_tracker = llm_cost_tracker

    def generate_completion(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        self._calculate_completion_costs(response)
        return response.choices[0].message.content

    def _calculate_completion_costs(self, response):
        # Fallback to zero cost if pricing is missing for the model
        input_tokens = (response.usage.prompt_tokens if response.usage else 0) or 0
        completion_tokens = (
            response.usage.completion_tokens if response.usage else 0
        ) or 0

        pricing = self.pricing.get(
            self.model,
            {"input_token_price": 0.0, "output_token_price": 0.0},
        )

        input_cost = input_tokens * pricing["input_token_price"]
        completion_cost = completion_tokens * pricing["output_token_price"]

        self.llm_cost_tracker.add_cost(
            input_tokens, completion_tokens, input_cost, completion_cost
        )

    def generate_structured_completion(
        self, prompt: str, output_model: BaseModel
    ) -> BaseModel:
        schema = output_model.model_json_schema()
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": output_model.__name__,
                "schema": schema,
            },
        }
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format=response_format,
            )
        except Exception:
            # Fallback for models without json_schema support
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


class OllamaLLM(LLM):
    def __init__(
        self,
        llm_cost_tracker: LLMCostTracker,
        model: str,
    ):
        self.model = model
        self.llm_cost_tracker = llm_cost_tracker

    def _calculate_completion_costs(self, response: ChatResponse):
        input_tokens = response.prompt_eval_count
        completion_tokens = response.eval_count

        self.llm_cost_tracker.add_cost(input_tokens, completion_tokens, 0, 0)

    def generate_completion(self, prompt: str) -> str:
        response = chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            think=False,
        )
        self._calculate_completion_costs(response)
        return response.message.content

    def generate_structured_completion(
        self, prompt: str, output_model: BaseModel
    ) -> BaseModel:
        response = chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            format=output_model.model_json_schema(),
            think=False,
        )
        parsed_output = output_model.model_validate_json(response.message.content)
        self._calculate_completion_costs(response)
        return parsed_output
