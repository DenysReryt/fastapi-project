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


    async def put_user_result(self, score: str, result: float, quiz_id: int, user_id: int, company_id: int) -> float:
        query = result_quiz.insert().values(score=score, result=result, time=datetime.datetime.now(), quiz=quiz_id, company=company_id,
                                            user=user_id)
        await database.execute(query=query)
        query2 = result_quiz.select().where(user_id == result_quiz.c.user)
        main = await database.fetch_all(query2)
        list_of_score = [dict(aba) for aba in main]
        user_answer = 0
        all_question = 0
        for i in list_of_score:
            answer, question = i['score'].split('/')
            user_answer += int(answer)
            all_question += int(question)
        my_rating = round((user_answer / all_question), 2)
        query3 = rating.delete().where(user_id == rating.c.user_id)
        await database.execute(query=query3)
        query4 = rating.insert().values(rating=my_rating, user_id=user_id)
        await database.execute(query=query4)

        return result

    # async def user_rating(self, user_id: int):
    #     query = result_quiz.select().where(user_id == result_quiz.c.user)
    #     await database.fetch_all(query)


res_crud = ResultCrud()
