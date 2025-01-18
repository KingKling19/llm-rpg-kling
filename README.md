# LLM-RPG

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

3. Set up your environment variables. You need to set the `GROQ_API_KEY` to use the GroqLLM model. You can do this by creating a `.env` file in the `config` directory:

   ```plaintext
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

To start the game, run the following command:

```bash
poetry run python -m llm_rpg
```
