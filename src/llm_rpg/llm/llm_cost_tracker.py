class LLMCostTracker:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_input_cost = 0
        self.total_output_cost = 0
        self.total_cost = 0
        self.total_requests = 0

    def add_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        input_cost: float,
        output_cost: float,
    ):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_input_cost += input_cost
        self.total_output_cost += output_cost
        self.total_cost += input_cost + output_cost
        self.total_requests += 1

    def display_costs(self):
        print(f"Total requests: {self.total_requests}")
        print(f"Total input tokens: {self.total_input_tokens}")
        print(f"Total output tokens: {self.total_output_tokens}")
        print(f"Total tokens: {self.total_input_tokens + self.total_output_tokens}")
        print(f"Total input cost: ${self.total_input_cost:.6f}")
        print(f"Total output cost: ${self.total_output_cost:.6f}")
        print(f"Total cost: ${self.total_cost:.6f}")
