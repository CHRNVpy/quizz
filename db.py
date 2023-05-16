from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('postgresql://postgres:postgres@db/quizdb')


class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    question_text = Column(String)
    answer_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)


def add_to_db(question_id: int, question_text: str, answer_text: str, created_at: datetime):
    """
    Добавление вопросов в базу данных

    :param question_id:
    :param question_text:
    :param answer_text:
    :param created_at:
    :return:
    """

    Session = sessionmaker(bind=engine)
    session = Session()

    quiz_question = QuizQuestion(
        question_id=question_id,
        question_text=question_text,
        answer_text=answer_text,
        created_at=created_at
    )
    session.add(quiz_question)
    session.commit()

    # Close the session
    session.close()


def find_question_by_id(question_id: int):
    """
    Поиск вопроса в БД по question_id

    :param question_id:
    :return:
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    question = session.query(QuizQuestion).filter_by(question_id=question_id).first()
    session.close()

    return question


def get_last_saved_item():
    """
    Получение последнего добавленного вопроса из БД

    :return:
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    max_id_item = session.query(QuizQuestion).order_by(QuizQuestion.id.desc()).first()

    session.close()

    return max_id_item.question_text
