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

def calc_path(hospitals):
    queue = deque(hospitals)
    visited = [[-1] * n for _ in range(n)]
    for sr, sc in hospitals:
        visited[sr][sc] = 0
    patients = people
    tmp_ans = 0
    count_time = 0
    while True:
        new_queue = deque()
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
        count_time += 1
        if not patients:
            break
        # 가지치기
        if count_time > ans or tmp_ans > ans:
            return int(1e9)

    return tmp_ans

def dfs(choose, chosen):
    global ans
    if choose == m:
        ans = min(ans, calc_path(chosen))
    else:
        for i in range(choose, len(hospitals)):
            if not selected[i]:
                selected[i] = 1
                dfs(choose + 1, chosen + [hospitals[i]])
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

ans = int(1e9)
dfs(0, [])

print(ans)