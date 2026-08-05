from quiz_game import QuizGame
from constants import FINAL_CONFIG_PATH, FINAL_QUIZ_DATA_PATH


def main():
    game = QuizGame(FINAL_CONFIG_PATH, FINAL_QUIZ_DATA_PATH)
    game.run()


if __name__ == "__main__":
    main()