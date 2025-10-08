import json
import os

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_dict(self):
        return {"question": self.question, "answer": self.answer}

    @staticmethod
    def from_dict(data):
        return Flashcard(data["question"], data["answer"])

class Deck:
    def __init__(self, name):
        self.name = name
        self.flashcards = []

    def add_flashcard(self, question, answer):
        self.flashcards.append(Flashcard(question, answer))

    def delete_flashcard(self, index):
        if 0 <= index < len(self.flashcards):
            self.flashcards.pop(index)
        else:
            print("Invalid index!")

    def study(self):
        for fc in self.flashcards:
            input(f"Q: {fc.question} (press Enter to see the answer)")
            print(f"A: {fc.answer}\n")

    def save(self):
        data = [fc.to_dict() for fc in self.flashcards]
        os.makedirs("decks", exist_ok=True)
        with open(f"decks/{self.name}.json", "w") as f:
            json.dump(data, f)

    @staticmethod
    def load(name):
        path = f"decks/{name}.json"
        deck = Deck(name)
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                deck.flashcards = [Flashcard.from_dict(fc) for fc in data]
        return deck

def list_decks():
    if not os.path.exists("decks"):
        return []
    return [f.replace(".json", "") for f in os.listdir("decks") if f.endswith(".json")]

def main():
    while True:
        print("\n--- Flashcard App ---")
        print("1. Create a new deck")
        print("2. Load a deck")
        print("3. List decks")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter deck name: ")
            deck = Deck(name)
            deck.save()
            print(f"Deck '{name}' created!")

        elif choice == "2":
            decks = list_decks()
            if not decks:
                print("No decks found!")
                continue
            print("Available decks:", ", ".join(decks))
            name = input("Enter deck to load: ")
            if name not in decks:
                print("Deck not found!")
                continue
            deck = Deck.load(name)

            while True:
                print(f"\n--- Deck: {deck.name} ---")
                print("1. Study flashcards")
                print("2. Add flashcard")
                print("3. Delete flashcard")
                print("4. Back to main menu")
                sub_choice = input("Choose an option: ")

                if sub_choice == "1":
                    deck.study()
                elif sub_choice == "2":
                    q = input("Question: ")
                    a = input("Answer: ")
                    deck.add_flashcard(q, a)
                    deck.save()
                    print("Flashcard added!")
                elif sub_choice == "3":
                    for i, fc in enumerate(deck.flashcards):
                        print(f"{i}: {fc.question}")
                    idx = int(input("Enter index to delete: "))
                    deck.delete_flashcard(idx)
                    deck.save()
                    print("Flashcard deleted!")
                elif sub_choice == "4":
                    break
                else:
                    print("Invalid choice.")

        elif choice == "3":
            decks = list_decks()
            print("Decks available:", ", ".join(decks) if decks else "None")

        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
