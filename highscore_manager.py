import pickle

HIGHSCORE_FILE = "highscores.dat"
MAX_HIGHSCORES = 10


def load_highscores():
    try:
        with open(HIGHSCORE_FILE, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return []


def save_highscores(highscores):
    with open(HIGHSCORE_FILE, "wb") as file:
        pickle.dump(highscores, file)


def add_highscore(name, score):
    highscores = load_highscores()
    highscores.append((name, score))
    highscores.sort(
        key=lambda x: x[1], reverse=True
    )  # Sort by score in descending order
    highscores = highscores[:MAX_HIGHSCORES]  # Keep only the top scores
    save_highscores(highscores)


def display_highscores():
    highscores = load_highscores()
    for name, score in highscores:
        print(f"{name}: {score}")
