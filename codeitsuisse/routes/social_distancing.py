import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


def fun(seat, people, space):

    fun.ans = 0
    def recur(st, p):
        if p > st:
            return False
        if p == 0:
            return 0
        if p==1:
            return st

        for s in range(1, st+1):
            if st -s >0:
                can = recur(st-s-space, p-1)
                if can:
                    fun.ans += can

    recur(seat, people)
    return fun.ans


@app.route('/social_distancing', methods=['POST'])
def evaluate_social_distancing():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests");
    answers = {}
    for k, v in tests.items():
        answers[k] = fun(v['seats'], v['people'], v['spaces'])
    result = {"answers": answers}
    logging.info("My result :{}".format(result))
    return json.dumps(result)



