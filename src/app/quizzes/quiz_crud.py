from src.app.database import database
from src.app.models import quizzes, questions
from src.app import schemas
import datetime

from src.app.schemas import BaseQuiz, BaseQuestion


class QuizCrud():

    async def post_quiz(self, quiz: schemas.CreateQuiz, company: int) -> BaseQuiz:
        db_quiz = quizzes.insert().values(
            name=quiz.name, description=quiz.description, frequency=quiz.frequency, company_id=company)
        quiz_id = await database.execute(db_quiz)
        return schemas.BaseQuiz(**quiz.dict(), id=quiz_id, company_id=company, created_at=datetime.datetime.now())


    async def post_question(self, question: schemas.CreateQuestion, quiz_id: int) -> BaseQuestion:
        db_question = questions.insert().values(question=question.question, answer_1=question.answer_1, answer_2=question.answer_2,
                                                answer_3=question.answer_3, answer_4=question.answer_4, answer_5=question.answer_5,
                                                right_answer=question.right_answer, quiz_id=quiz_id)
        question_id = await database.execute(db_question)
        return schemas.BaseQuestion(**question.dict(), question_id=question_id, quiz_id=quiz_id)

    async def check_quiz(self, quiz_id) -> BaseQuiz:
        query = quizzes.select().where(quiz_id == quizzes.c.id)
        return await database.fetch_one(query=query)

    async def get_company_id(self, quiz_id: int) -> BaseQuiz:
        db_company = quizzes.select().where(quiz_id == quizzes.c.id)
        return await database.fetch_one(db_company)

    async def check_quiz_owner(self, quiz_id: int, company_id: int) -> BaseQuiz:
        db_check = quizzes.select().where(quiz_id == quizzes.c.id, company_id == quizzes.c.company_id)
        return await database.fetch_one(db_check)
quiz_crud = QuizCrud()
