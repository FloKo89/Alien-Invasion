import pickle

HIGHSCORE_FILE = "highscores.dat"
MAX_HIGHSCORES = 10


def load_highscores():
    try:
        with open(HIGHSCORE_FILE, "rb") as file:
            highscores = pickle.load(file)
            print(f"Loaded highscores: {highscores}")  # Debug-Ausgabe
            return highscores
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return []


def save_highscores(highscores):
    print(f"Attempting to save highscores: {highscores}")  # Debug-Ausgabe
    with open(HIGHSCORE_FILE, "wb") as file:
        pickle.dump(highscores, file)
    print(f"Highscores saved to {HIGHSCORE_FILE}")  # Debug-Ausgabe


def add_highscore(name, score):
    highscores = load_highscores()
    highscores.append((name, score))
    highscores.sort(
        key=lambda x: x[1], reverse=True
    )  # Sort by score in descending order
    highscores = highscores[:MAX_HIGHSCORES]  # Keep only the top scores
    print(f"Saving highscores: {highscores}")
    save_highscores(highscores)


def display_highscores():
    highscores = load_highscores()
    for name, score in highscores:
        print(f"{name}: {score}")
