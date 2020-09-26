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
    for i in range(n):
        if i ==n-1:
            j =0
        else:
            j =i+1

        line2 = make_line(shape[i], shape[j])

        p = poi(line1, line2)
        # print(shape[i])
        # print(shape[j])
        # print(p)
        # print()
        if p:
            #print('A')
            if min(shape[i]['x'], shape[j]['x']) <= p[0] <= max(shape[i]['x'], shape[j]['x']) and min(shape[i]['y'], shape[j]['y']) <= p[1] <= max(shape[i]['y'], shape[j]['y']):
             #   print('A')
                ans.append({"x":p[0], "y": p[1]})

    flag = False
    if line[0]['x'] - line[1]['x'] ==0:
        flag = True
    else:
        m = (line[0]['y'] - line[1]['y'] / line[0]['x'] - line[1]['x'])
        c = line[0]['y'] - m * line[0]['x']
        m = round(m, 2)

    for i in range(n):
        if flag:
            if shape[i]['x'] == line[0]['x']:
                ans.append({"x": shape[i]['x'], "y": shape[i]['y']})
        else:
            #print()
            #print(shape[i])
            #print(m)
            #print(shape[i]['y'])
            #print( m * shape[i]['x'] + c)
            if shape[i]['y'] == m * shape[i]['x'] + c:
                ans.append({"x":shape[i]['y'], "y":shape[i]['y']})

    return ans



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



