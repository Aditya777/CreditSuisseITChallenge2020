from __future__ import division

import logging
import json
from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)



def make_line(p1, p2):
    A = (p1['y'] - p2['y'])
    B = (p2['x'] - p1['x'])
    C = (p1['x']*p2['y'] - p2['x']*p1['y'])
    return A, B, -C


def poi(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return round(x, 2), round(y,2)
    else:
        return False


def fun_geo(shape, line):
    ans = []
    n = len(shape)
    line1 = make_line(line[0], line[1])
    i =0
    while i < n:
        if i >= n-1:
            j =0
        else:
            j =i+1

        line2 = make_line(shape[i], shape[j])

        p = poi(line1, line2)
        if p:
            if min(shape[i]['x'], shape[j]['x']) <= p[0] <= max(shape[i]['x'], shape[j]['x']) and min(shape[i]['y'], shape[j]['y']) <= p[1] <= max(shape[i]['y'], shape[j]['y']):
                if i == 0 and p[0] == shape[i]['x'] and p[1] == shape[i]['y']:
                    pass
                else:
                    ans.append({"x":p[0], "y": p[1]})
                    if p[0] == shape[j]['x'] and p[1] == shape[j]['y']:
                       i+=1
        i+=1

    return list(ans)



@app.route('/revisitgeometry', methods=['POST'])
def evaluate_geo():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    n = data.get("shapeCoordinates")
    l = data.get("lineCoordinates")

    result = fun_geo(n, l)
    logging.info("My result :{}".format(result))
    logging.info(result)
    return json.dumps(result)



