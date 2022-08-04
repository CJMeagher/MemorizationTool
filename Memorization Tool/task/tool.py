from collections import namedtuple
from flashcard_db import DbInterface

Flashcard = namedtuple("Flashcard", "question answer")
db_url = "sqlite:///flashcard.db?check_same_thread=False"
echo = False
db = DbInterface(db_url, echo=echo)


def main_menu():
    session_number = 0
    while True:
        print()
        print("1. Add flashcards")
        print("2. Practice flashcards")
        print("3. Exit")
        option = input()
        if option == "1":
            add_card()
        elif option == "2":
            session_number += 1 if session_number < 3 else 1
            practice(session_number)
        elif option == "3":
            print("Bye!")
            return
        else:
            print(f"{option} is not an option")


def add_card():
    while True:
        print()
        print("1. Add a new flashcard")
        print("2. Exit")
        option = input()
        if option == "1":
            question = ""
            while not question or question.isspace():
                question = input("Question:\n")
            answer = ""
            while not answer or answer.isspace():
                answer = input("Answer:\n")
            db.add_flashcard_row(question, answer, commit=True)
        elif option == "2":
            break
        else:
            print(f"{option} is not an option")


def practice(session_number):
    flashcards = db.get_session_rows(session_number)
    flashcard_count = 0
    for flashcard in flashcards:
        flashcard_count += 1
        print()
        print(f"Question: {flashcard.question}")
        while True:
            print('press "y" to see the answer:')
            print('press "n" to skip:')
            print('press "u" to update:')
            response = input()
            if response == "y":
                print(f"Answer: {flashcard.answer}")
                update_box(flashcard)
                break
            elif response == "n":
                break
            elif response == "u":
                update(flashcard)
                break
            else:
                print(f"{response} is not an option")
    if not flashcard_count:
        print()
        print("There is no flashcard to practice!")


def update_box(flashcard):
    while True:
        print('press "y" if your answer is correct:')
        print('press "n" if your answer is wrong:')
        response = input()
        if response == "y":
            if flashcard.box_number == 3:
                db.delete_row(flashcard.id, commit=True)
            else:
                flashcard.box_number += 1
                db.update_row(
                    flashcard.id,
                    flashcard.question,
                    flashcard.answer,
                    flashcard.box_number,
                    commit=True,
                )
            break
        elif response == "n":
            flashcard.box_number = 1
            break
        else:
            print(f"{response} is not an option")


def update(flashcard):
    while True:
        print('press "d" to delete the flashcard:')
        print('press "e" to edit the flashcard:')
        response = input()
        if response == "d":
            db.delete_row(flashcard.id, commit=True)
            break
        elif response == "e":
            edit(flashcard)
            break
        else:
            print(f"{response} is not an option")


def edit(flashcard):
    print()
    print(f"current question: {flashcard.question}")
    print("please write a new question:")
    question = input()
    print(f"current answer: {flashcard.answer}")
    print("please write a new answer:")
    answer = input()
    if question.isspace():
        question = flashcard.question
    if answer.isspace():
        answer = flashcard.answer
    if (question, answer) != (flashcard.question, flashcard.answer):
        db.update_row(flashcard.id, question, answer, flashcard.box_number, commit=True)


if __name__ == "__main__":
    main_menu()
