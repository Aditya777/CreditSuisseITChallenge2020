import logging
import json
from flask import request, jsonify
from collections import deque

from codeitsuisse import app;

logger = logging.getLogger(__name__)


def bfs(array):
    rows = len(array)
    if rows ==0:
        return 0

    cols = len(array[0])

    visited = [[False] * cols for i in range(rows)]
    clus = []

    for i in range(rows):
        for j in range(cols):
            if array[i][j] == "1":
                clus.append([i, j])

    ans = 0
    print(clus)
    for c in clus:
        if visited[c[0]][c[1]]:
            continue
        q = deque()
        q.append(c)
        while q:
            node = q.popleft()
            direc = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

            for d in direc:
                new_dir = [node[0]+d[0], node[1]+d[1]]
                if 0 <= new_dir[0] < rows and 0 <= new_dir[1] < cols:
                    if not visited[new_dir[0]][new_dir[1]]:
                        if array[new_dir[0]][new_dir[1]] != "*":
                            q.append(new_dir)
                            array[new_dir[0]][new_dir[1]]= "1"
                            visited[new_dir[0]][new_dir[1]] = True
        ans+=1

    return ans


@app.route('/cluster', methods=['POST'])
def evaluate_cluster():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    #inputValue = data.get("input");
    result = {"answer":bfs(data)}
    logging.info("My result :{}".format(result))
    return json.dumps(result);



