import pickle
import os

HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscores.dat")
MAX_HIGHSCORES = 10


def load_highscores():
    try:
        with open(HIGHSCORE_FILE, "rb") as file:
            highscores = pickle.load(file)
        return highscores
    except (FileNotFoundError, EOFError, pickle.UnpicklingError) as e:
        print(f"Error loading highscores: {e}")
        return []


def save_highscores(highscores):
    try:
        with open(HIGHSCORE_FILE, "wb") as file:
            pickle.dump(highscores, file)
    except IOError as e:
        print(f"Error saving highscores: {e}")


def add_highscore(name, score):
    try:
        highscores = load_highscores()
        highscores.append((name, score))
        highscores.sort(
            key=lambda x: x[1], reverse=True
        )  # Sort by score in descending order
        highscores = highscores[:MAX_HIGHSCORES]  # Keep only the top scores
        save_highscores(highscores)
    except Exception as e:
        print(f"Error adding highscore: {e}")


def display_highscores():
    try:
        highscores = load_highscores()
        for name, score in highscores:
            print(f"{name}: {score}")
    except Exception as e:
        print(f"Error displaying highscores: {e}")
