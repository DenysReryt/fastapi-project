import csv

from aioredis.client import Redis


def make_rating(answer_input: list, right_answers: list):
    try:
        quiz_score = 0
        list_of_user_answer = [dict(user_answer) for user_answer in answer_input]
        for i in range(len(right_answers)):
            if list_of_user_answer[i]['answer'] == right_answers[i]['answer']:
                quiz_score += 1
        if quiz_score > 0:
            result = round((float(quiz_score) / len(right_answers)), 3)
        else:
            result = 0
        return quiz_score, right_answers, result
    except IndexError:
        return 'sqe'


def get_user_result_redis(user_id: int, quiz_id: int, user_answers: list):
    redis_key = f"user_id:{user_id} : quiz_id:{quiz_id}"
    res_to_save = {}
    list_of_user_answer = [dict(user_answer) for user_answer in user_answers]
    for i in list_of_user_answer:
        res_to_save[i['question_id']] = i['answer']
    return redis_key, res_to_save

