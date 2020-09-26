import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
memo = {}


def fun(st, p, space):

    if p > st:
        return 0
    if p == 0:
        return 0
    if p==1:
        return st

    if (st, p, space) in memo:
        return memo.get((st, p, space))
    ans = 0
    for s in range(1, st+1):
        if st -s > 0 :
            if (st-s-space, p-1, space) not in memo:
                memo[(st-s-space, p-1, space)] = fun(st-s-space, p-1, space)

            ans += memo.get((st-s-space, p-1, space))

    memo[(st, p, space)] = ans
    return ans



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



