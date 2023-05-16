import requests
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from db import QuizQuestion, add_to_db, find_question_by_id, get_last_saved_item

Base = declarative_base()
engine = create_engine('postgresql://postgres:postgres@db/quizdb')

app = FastAPI()


@app.post("/quiz")
async def quiz(questions_num: dict):
    if questions_num.get('questions_num') <= 0:
        raise HTTPException(status_code=400, detail="Number of questions must be greater than zero")

    response = requests.get(f"https://jservice.io/api/random?count={questions_num['questions_num']}")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch questions from API")

    questions = response.json()
    for question in questions:
        question_id = question.get('id')
        question_text = question.get('question')
        answer_text = question.get('answer')
        created_at = question.get('created_at')
        while find_question_by_id(question_id):
            response = requests.get(f"https://jservice.io/api/random?count=1")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch questions from API")
            res = response.json()[0]
            add_to_db(res['id'], res['question'], res['answer'], res['created_at'])
        else:
            add_to_db(question_id, question_text, answer_text, created_at)
    if get_last_saved_item():
        return get_last_saved_item()
    else:
        return ''

