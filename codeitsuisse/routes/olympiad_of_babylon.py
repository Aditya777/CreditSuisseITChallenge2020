import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
memo = {}


def fun(books, days):

    if (books, days) in memo:
        return memo.get((books, days))

    if len(books) == 0:
        return 0

    if len(books) == 1:
        for d in days:
            if books[-1] < d:
                return 1
        return 0

    cur = books[-1]
    books = books[:-1]
    max_books = 0
    for i, d in enumerate(days):
        if cur > d:
            continue
        cop = list(days)
        cop[i] -= cur
        cop = tuple(cop)
        if (books, cop) not in memo:
            memo[(books, cop)] = fun(books, cop)
        max_books = max(max_books, 1 + memo.get((books, cop)))

    if (books, days) not in memo:
            memo[(books, days)] = fun(books, days)

    max_books = max(max_books, memo.get((books, days)))

    return max_books


@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_olympiad_of_babylon():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    books = data.get("books")
    days = data.get("days")
    result = {"optimalNumberOfBooks" :fun(tuple(books), tuple(days))}
    logging.info("My result :{}".format(result))
    return json.dumps(result)



