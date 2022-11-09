from src.app.database import database
from src.app.models import quizzes, questions
from src.app import schemas
import datetime

from src.app.schemas import BaseQuiz, BaseQuestion


class QuizCrud():

    async def get_quizzes(self, skip: int, limit: int) -> BaseQuiz:
        query = quizzes.select().offset(skip).limit(limit)
        return await database.fetch_all(query=query)

    async def get_company_by_quiz_id(self, quiz_id: int) -> BaseQuiz:
        query = quizzes.select().where(quiz_id == quizzes.c.id)
        return await database.fetch_one(query=query)

    async def post_quiz(self, quiz: schemas.CreateQuiz, company: int) -> BaseQuiz:
        db_quiz = quizzes.insert().values(
            name=quiz.name, description=quiz.description, frequency=quiz.frequency, company_id=company)
        quiz_id = await database.execute(db_quiz)
        return schemas.BaseQuiz(**quiz.dict(), id=quiz_id, company_id=company, created_at=datetime.datetime.now())

    async def put_quiz(self, quiz: schemas.CreateQuiz, quiz_id: int, company_id: int) -> BaseQuiz:
        query = quizzes.update().where(quiz_id == quizzes.c.id).values(
            name=quiz.name, description=quiz.description, frequency=quiz.frequency).returning(quizzes.c.id)
        ex = await database.execute(query=query)
        quiz_get_time = await database.fetch_one(quizzes.select().where(quiz_id == quizzes.c.id))
        return schemas.BaseQuiz(**quiz.dict(), id=ex, company_id=company_id, created_at=quiz_get_time.created_at)

    async def post_question(self, question: schemas.CreateQuestion, quiz_id: int) -> BaseQuestion:
        db_question = questions.insert().values(question=question.question, answers=question.answers,
                                                right_answer=question.right_answer, quiz_id=quiz_id)
        question_id = await database.execute(db_question)
        return schemas.BaseQuestion(**question.dict(), question_id=question_id, quiz_id=quiz_id)

    async def delete(self, quiz_id: int) -> BaseQuiz:
        query1 = questions.delete().where(quiz_id == questions.c.quiz_id)
        await database.execute(query=query1)
        query2 = quizzes.delete().where(quiz_id == quizzes.c.id)
        return await database.execute(query=query2)

    async def check_quiz(self, quiz_id) -> BaseQuiz:
        query = quizzes.select().where(quiz_id == quizzes.c.id)
        return await database.fetch_one(query=query)


quiz_crud = QuizCrud()
