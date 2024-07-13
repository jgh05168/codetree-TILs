'''
불은 상하좌우 인접한 공간으로 번진다.
방화벽 뚫을 수 없다.

기존 방화벽을 제외하고 추가로 3개의 방화벽을 설치할 수 있다.
불이 퍼지지 않는 영역 크기의 최댓값 출력하기

풀이 :
- 불의 위치를 사전에 체크한다.
- n과 m이 작으므로, 조합을 직접 작성해서 브루트포스 돌려도 될 듯 ?
- 재귀함수로 진행하기
- 방화벽을 다 놓은 뒤 불 지른다음 최댓값 업데이트
'''

from collections import deque
import sys
input = sys.stdin.readline

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def bfs(fire, grid):
    global ans
    queue = deque(fire)
    visited = [[0] * m for _ in range(n)]
    for r, c in fire:
        visited[r][c] = 1

    while queue:
        row, col = queue.popleft()
        for d in range(len(dr)):
            nr, nc = row + dr[d], col + dc[d]
            if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc]:
                if not grid[nr][nc]:
                    queue.append((nr, nc))
                    visited[nr][nc] = 1
                if grid[nr][nc] == 2:
                    visited[nr][nc] = 1

    tmp_ans = 0
    for i in range(n):
        for j in range(m):
            if not visited[i][j] and not grid[i][j]:
                tmp_ans += 1

    ans = max(ans, tmp_ans)


def recur(r, c, cnt):
    if cnt == 3:
        bfs(fire, grid)
        return

    else:
        # 2차원 배열 조합 구현
        for i in range(r, n):
            if i != 0:
                c = 0
            for j in range(c, m):
                if not grid[i][j]:
                    grid[i][j] = 1
                    recur(i, j + 1, cnt + 1)
                    grid[i][j] = 0


n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

fire = []
for i in range(n):
    for j in range(m):
        if grid[i][j] == 2:
            fire.append((i, j))

ans = 0
for i in range(n):
    for j in range(m):
        if not grid[i][j]:
            grid[i][j] = 1
            recur(i, j + 1, 1)
            grid[i][j] = 0

print(ans)