from src.app.database import database
from src.app.models import quizzes, questions, answers, result_quiz, rating
from src.app import schemas
import datetime

from src.app.schemas import BaseQuiz, BaseQuestion, QuizResult


class ResultCrud():

    async def get_questions(self, quiz_id) -> BaseQuestion:
        query = questions.select().where(quiz_id == questions.c.quiz_id)
        return await database.fetch_all(query=query)

    async def get_right_answers(self, quiz_id: int) -> list:
        query = answers.select().join(questions).where(answers.c.question_id == questions.c.question_id, questions.c.quiz_id == quiz_id)
        question = await database.fetch_all(query=query)
        return [dict(result) for result in question]


    async def put_user_result(self, my_rating: float, result: float, quiz_id: int, user_id: int, company_id: int) -> float:
        query1 = result_quiz.delete().where(result_quiz.c.user == user_id, result_quiz.c.quiz == quiz_id)
        await database.execute(query=query1)
        query2 = result_quiz.insert().values(result=result, time=datetime.datetime.now(), quiz=quiz_id, company=company_id,
                                            user=user_id)
        await database.execute(query=query2)
        query3 = rating.delete().where(user_id == rating.c.user_id)
        await database.execute(query3)
        query4 = rating.insert().values(rating=my_rating, user_id=user_id)
        await database.execute(query=query4)
        return result



res_crud = ResultCrud()
