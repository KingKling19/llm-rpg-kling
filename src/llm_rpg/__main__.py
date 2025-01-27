from dotenv import load_dotenv

from llm_rpg.game.game import Game

load_dotenv("config/.env")

if __name__ == "__main__":
    game = Game()
    game.run()
