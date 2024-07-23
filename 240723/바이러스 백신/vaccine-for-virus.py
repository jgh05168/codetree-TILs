'''
M개의 병원을 적절히 골라 최대한 빨리 바이러스를 없애고자 함
상하좌우 인접한 지역으로 백신이 공급되어 바이러스가 삭제된다.

최소 시간을 구하자.

M <= 10

selected 배열 사용 ? 순열 + bfs 로 해결하기

'''

from collections import deque
import sys
input = sys.stdin.readline

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def bfs():
    queue = deque()
    visited = [[-1] * n for _ in range(n)]
    for i in range(len(selected)):
        if selected[i]:
            queue.append(hospitals[i])
            visited[hospitals[i][0]][hospitals[i][1]] = 0

    while queue:
        r, c = queue.popleft()
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and visited[nr][nc] == -1 and grid[nr][nc] != 1:
                if not grid[nr][nc] or grid[nr][nc] == 2:
                    queue.append((nr, nc))
                    visited[nr][nc] = visited[r][c] + 1

    # 모두 없애지 못한 경우를 체크하기
    tmp_ans = 0
    for i in range(n):
        for j in range(n):
            # 없애지 못한 경우
            if not grid[i][j] and visited[i][j] == -1:
                return -1, False
            # 없앤 경우
            if visited[i][j] and not grid[i][j]:
                tmp_ans = max(tmp_ans, visited[i][j])
    return tmp_ans, True


def dfs(cnt, idx):
    global ans
    if cnt == m:
        tmp_ans, check_ans = bfs()
        if check_ans:
            ans = min(ans, tmp_ans)
        return
    else:
        for i in range(idx + 1, len(selected)):
            if not selected[i]:
                selected[i] = 1
                dfs(cnt + 1, i)
                selected[i] = 0


n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

hospitals = []
for i in range(n):
    for j in range(n):
        if grid[i][j] == 2:
            hospitals.append((i, j))

selected = [0] * len(hospitals)

ans = int(1e9)
dfs(0, -1)

if ans == int(1e9):
    print(-1)
else:
    print(ans)