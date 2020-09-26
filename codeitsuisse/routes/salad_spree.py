import logging
import json
from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)


def fun_salad(n, streets):
    min_cost = float('inf')
    for st in streets:
        l = 0
        r = 0

        street_len = len(st)
        cur_len = 0
        cur_cost = 0

        while r < street_len:
            if st[r] == 'X':
                l = r+1
                r = r+1
                cur_cost = 0
                cur_len = 0
            elif cur_len < n:
                cur_cost += int(st[r])
                cur_len+=1
                r += 1
                if cur_len ==n:
                    min_cost = min(min_cost, cur_cost)

            else:
                cur_cost += int(st[r])
                cur_cost -= int(st[l])
                r+=1
                l+=1
                min_cost = min(min_cost, cur_cost)

    if min_cost != float('inf'):
        return min_cost
    else:
        return 0

@app.route('/salad-spree', methods=['POST'])
def evaluate_salad_spree():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    n = data.get("number_of_salads")
    s = data.get("salad_prices_street_map")

    result = {"result": fun_salad(n, s)}
    logging.info("My result :{}".format(result))
    logging.info(result)
    return json.dumps(result)



