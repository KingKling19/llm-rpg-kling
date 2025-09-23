```

▄█        ▄█         ▄▄▄▄███▄▄▄▄           ▄████████    ▄███████▄    ▄██████▄
███       ███       ▄██▀▀▀███▀▀▀██▄        ███    ███   ███    ███   ███    ███
███       ███       ███   ███   ███        ███    ███   ███    ███   ███    █▀
███       ███       ███   ███   ███       ▄███▄▄▄▄██▀   ███    ███  ▄███
███       ███       ███   ███   ███      ▀▀███▀▀▀▀▀   ▀█████████▀  ▀▀███ ████▄
███       ███       ███   ███   ███      ▀███████████   ███          ███    ███
███▌    ▄ ███▌    ▄ ███   ███   ███        ███    ███   ███          ███    ███
█████▄▄██ █████▄▄██  ▀█   ███   █▀         ███    ███  ▄████▀        ████████▀
▀         ▀                                ███    ███
```

LLM-RPG is intended to be a role-playing game that leverages large language models to create dynamic and engaging gameplay experiences. Currently it is still in the early stages of development and only has a battle scene implemented.

## Current / future features

- **Dynamic Battles**: Engage in battles where both heroes and enemies use AI to determine actions and effects.
- **Character Customization**: Define your hero's stats and abilities.
- **AI-Powered Creativity**: Use creative language to influence battle outcomes.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/vossenwout/llm-rpg.git
   cd llm-rpg
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Set up your environment variables in `config/.env.secret`.

   - For OpenAI (ChatGPT):

     ```plaintext
     OPENAI_API_KEY=your_openai_api_key_here
     ```

   You can get an OpenAI API key from the OpenAI dashboard.

## Usage

To start the game, run the following command:

```bash
poetry run python -m llm_rpg
```

## Local LLMs with ollama

Using local llms with ollama:

1. Install ollama https://ollama.com

2. Install a model, I would recommend qwen3 models.

3. Start ollama

4. In game_config.yaml, uncomment the ollama model section and comment the groq model. Remember to select the correct model name you installed.

```bash
llm:
  model: "qwen3:4b"
  type: "ollama"
#llm:
#  model: "gpt-4o-mini"
#  type: "openai"
```

## Using OpenAI (ChatGPT)

1. Put your key in `config/.env.secret` as `OPENAI_API_KEY=...`.
2. In `config/game_config.yaml`, set:

   ```yaml
   llm:
     model: "gpt-4o-mini"   # or another OpenAI chat model
     type: "openai"         # also accepts: "gpt" or "chatgpt"
   ```
3. Run the game:

   ```bash
   poetry run python -m llm_rpg
   ```

5. Run the game

```bash
poetry run python -m llm_rpg
```

## Maintaining the codebase

Install pre-commit hooks:

```bash
pre-commit install
```

Run tests:

```bash
poetry run pytest -s -v
```
