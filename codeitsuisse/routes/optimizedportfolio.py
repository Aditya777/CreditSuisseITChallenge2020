import logging
import json
from flask import request, jsonify;
import math

from codeitsuisse import app;

logger = logging.getLogger(__name__)


def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)


def fun(port, index):
    min_ohr = float('inf')
    ans = 0
    lowest_num_fut = 0
    for j, i in enumerate(index):
        ohr = port['SpotPrcVol'] * i['CoRelationCoefficient'] / i['FuturePrcVol']
        if ohr < min_ohr:
            ans = j
            min_ohr = ohr

        if min_ohr == ohr:
            if i['FuturePrcVol'] < index[ans]['FuturePrcVol']:
                ans = j

            elif i['FuturePrcVol'] == index[ans]['FuturePrcVol']:
                num_fut = ohr * port['Value'] / (i['IndexFuturePrice'] * i['Notional'])
                if lowest_num_fut == 0:
                    lowest_num_fut = ohr * port['Value'] / (index[ans]['IndexFuturePrice'] * index[ans]['Notional'])
                if num_fut < lowest_num_fut:
                    ans = j

    lowest_num_fut = ohr * port['Value'] / (index[ans]['IndexFuturePrice'] * index[ans]['Notional'])

    min_ohr = round(min_ohr, 3)
    print(lowest_num_fut)
    lowest_num_fut = round(lowest_num_fut, 1)
    lowest_num_fut = normal_round(lowest_num_fut)

    return {"HedgePositionName": index[ans]['Name'], "OptimalHedgeRatio": min_ohr, "NumFuturesContract": lowest_num_fut}


@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_optimizedportfolio():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    data = data.get("inputs")

    out = []
    for p in data:
        out.append(fun(p['Portfolio'], p['IndexFutures']))
    result = {"outputs": out}
    logging.info("My result :{}".format(result))
    return json.dumps(result)



