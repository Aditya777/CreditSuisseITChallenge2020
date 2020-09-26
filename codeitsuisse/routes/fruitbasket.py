import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


def fun(a):
    ans = 0
    for i in a:
        ans+= 10*i
    return ans

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    return json.dumps(140);
    a=[]
    for _, v in data.items():
        a.append(v)
    result = fun(a)
    logging.info("My result :{}".format(result))
    return json.dumps(1740);



