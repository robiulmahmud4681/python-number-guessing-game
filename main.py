
import random
import json
from pathlib import Path

SCORE_FILE = Path(__file__).with_name("best_scores.json")

DIFFICULTIES = {
    "1": {"name": "Easy", "maximum": 20, "attempts": 10},
    "2": {"name": "Medium", "maximum": 100, "attempts": 7},
    "3": {"name": "Hard", "maximum": 500, "attempts": 8},
}


def load_scores():
    try:
        return json.loads(SCORE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_scores(scores):
    SCORE_FILE.write_text(
        json.dumps(scores, indent=4),
        encoding="utf-8"
    )


def choose_difficulty():
    print("\nChoose difficulty:")
    print("1. Easy   (1-20, 10 attempts)")
    print("2. Medium (1-100, 7 attempts)")
    print("3. Hard   (1-500, 8 attempts)")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()

        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]

        print("Invalid choice. Please enter 1, 2, or 3.")


def play_game():
    print("\n=== NUMBER GUESSING GAME ===")

    difficulty = choose_difficulty()
    maximum = difficulty["maximum"]
    max_attempts = difficulty["attempts"]
    secret_number = random.randint(1, maximum)

    print(f"\nDifficulty: {difficulty['name']}")
    print(f"Guess a number between 1 and {maximum}.")
    print(f"You have {max_attempts} attempts.")

    attempts = 0

    while attempts < max_attempts:
        try:
            guess = int(input("\nTake a guess: ").strip())
        except ValueError:
            print("Please enter a valid whole number.")
            continue

        if not 1 <= guess <= maximum:
            print(f"Enter a number between 1 and {maximum}.")
            continue

        attempts += 1
        remaining = max_attempts - attempts

        if guess < secret_number:
            print("Too low! Try higher.")
        elif guess > secret_number:
            print("Too high! Try lower.")
        else:
            print(
                f"\nCongratulations! You won in {attempts} attempts!"
            )

            scores = load_scores()
            name = difficulty["name"]
            previous = scores.get(name)

            if previous is None or attempts < previous:
                scores[name] = attempts
                save_scores(scores)
                print("New best score!")
            else:
                print(f"Best score for {name}: {previous} attempts")

            return

        if remaining > 0:
            print(f"Attempts remaining: {remaining}")

    print(f"\nGame over! The number was {secret_number}.")


def main():
    while True:
        play_game()

        again = input("\nPlay again? (y/n): ").strip().lower()

        if again != "y":
            print("Thanks for playing. Goodbye!")
            break


if __name__ == "__main__":
    main()
