from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = "flashcard"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer)


class DbInterface:
    def __init__(self, url, echo=False):
        self.url = url
        engine = create_engine(self.url, echo=echo)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.flashcard_query = self.session.query(Flashcard)

    def add_flashcard_row(self, question, answer, commit=False):
        new_data = Flashcard(question=question, answer=answer, box_number=1)
        self.session.add(new_data)
        if commit:
            self.commit()

    def get_all_rows(self):
        return self.flashcard_query.all()

    def delete_all_rows(self, commit=False):
        self.flashcard_query.delete()
        if commit:
            self.commit()

    def get_session_rows(self, max_box):
        return self.flashcard_query.filter(Flashcard.box_number <= max_box)

    def update_row(self, id, question, answer, box_number, commit=False):
        by_id = self.flashcard_query.filter(Flashcard.id == id)
        by_id.update({"question": question, "answer": answer, "box_number": box_number})
        if commit:
            self.commit()

    def delete_row(self, id, commit=False):
        self.flashcard_query.filter(Flashcard.id == id).delete()
        if commit:
            self.commit()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


if __name__ == "__main__":
    db = DbInterface("sqlite:///test.db?check_same_thread=False", echo=True)
    # db.delete_all_rows()
    pairs = [("what?", "elephant", 1), ("how many?", "seventeen", 1)]
    for pair in pairs:
        question, answer, box_number = pair
        db.add_flashcard_row(question, answer, box_number)
    db.delete_row(1)
    db.update_row(2, "excuse me?", "that's right", 2)
    for row in db.get_all_rows():
        print(f"{row.id}, {row.question}, {row.answer}, {row.box_number}")
    for row in db.get_session_rows(1):
        print(f"{row.id}, {row.question}, {row.answer}, {row.box_number}")
    for row in db.get_session_rows(2):
        print(f"{row.id}, {row.question}, {row.answer}, {row.box_number}")
    db.commit()
