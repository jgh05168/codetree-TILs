'''
병원 거리 최소화하기

dfs : 조합을 사용하여 병원을 선택한다.
병원을 모두 선택하면, 거리를 계산한다.
거리 합의 최소를 저장한다.

- 장애물 없음
- 이동 거리는 절대거리로 계산

------- 시초 -------
bfs로 거리 구하면 시초난다.

-> 그냥 방문했다면 abs 를 통해 거리를 구해서 더하자.(사람별로)
'''

from collections import deque
import sys
input = sys.stdin.readline

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def calc_path():
    queue = deque()
    visited = [[-1] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if selec_hospitals[i][j]:
                queue.append((i, j))
                visited[i][j] = 0
    patients = people
    tmp_ans = 0

    while queue:
        r, c = queue.popleft()

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and visited[nr][nc] == -1:
                visited[nr][nc] = visited[r][c] + 1
                queue.append((nr, nc))
                # 사람을 발견한 경우
                if grid[nr][nc] == 1:
                    patients -= 1
                    tmp_ans += visited[nr][nc]
        if not patients:
            break

    return tmp_ans

def dfs(choose, idx):
    global ans
    if choose == m:
        ans = min(ans, calc_path())
    else:
        for i in range(idx, len(hospitals)):
            if not selected[i]:
                selected[i] = 1
                selec_hospitals[hospitals[i][0]][hospitals[i][1]] = 1
                dfs(choose + 1, i)
                selec_hospitals[hospitals[i][0]][hospitals[i][1]] = 0
                selected[i] = 0


n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

people = 0
hospitals = []
for i in range(n):
    for j in range(n):
        if grid[i][j] == 1:
            people += 1
        elif grid[i][j] == 2:
            hospitals.append((i, j))
selected = [0] * len(hospitals)
selec_hospitals = [[0] * n for _ in range(n)]
ans = int(1e9)
dfs(0, 0)

print(ans)