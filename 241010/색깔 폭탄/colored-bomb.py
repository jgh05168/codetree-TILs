'''
21:35

-1(검정돌), 0(빨간색폭탄), 1 ~ m(서로다른 폭탄) 숫자로 이루어진 n x n격자가 주어진다.

1. 현재 격자에서 크기가 가장 큰 폭탄 묶음을 찾는다.
    - 2개 이상의 폭탄으로 이루어져 있어야 한다.
        우선순위 :
            1) 빨간색 폭탄이 가장 적게 포함된 것부터 선택
            2) 묶음의 기준점 행이 큰, 열이 가장 작은 순서
    - 모두 같은 색깔 or 빨간색 포함하여 2개의 색깔로만 이루어진 폭탄
    - 빨간색 폭탄으로만 이루어져 있을 수는 없다.
    - 상하좌우 인접 폭탄
2. 폭탄 묶음에 해당되는 폭탄 전부 제거. & 중력 작용
    - 검정 돌은 중력 작용 안된다.
3. 반시계 방향으로 회전
4. 다시 중력 작용

더이상 폭탄 묶음이 없을 때까지 반복한다.
폭탄 묶음을 이루는 폭탄 개수  c * c  만큼 점수를 얻는다.
'''

from collections import deque

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

cur_bomb = []
red_cnt = 0
ans = 0


def get_bomb(sr, sc, color):
    global cur_bomb, red_cnt
    queue = deque([(sr, sc)])
    visited[sr][sc] = 1
    tmp_red = 0
    tmp_bomb = [(sr, sc)]

    while queue:
        r, c = queue.popleft()
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n:
                if grid[nr][nc] == color and not visited[nr][nc]:
                    queue.append((nr, nc))
                    tmp_bomb.append((nr, nc))
                    visited[nr][nc] = 1
                elif not grid[nr][nc]:
                    queue.append((nr, nc))
                    tmp_bomb.append((nr, nc))
                    tmp_red += 1
    # 현재 최고 찾기
    bomb_cnt = len(tmp_bomb)
    if bomb_cnt >= 2:
        if bomb_cnt > len(cur_bomb):
            cur_bomb = tmp_bomb[:]
        elif bomb_cnt == len(cur_bomb) and red_cnt > tmp_red:
            red_cnt = tmp_red
            cur_bomb = tmp_bomb[:]
    return bomb_cnt


def gravity():
    for i in range(n - 1, -1, -1):
        for j in range(n):
            if grid[i][j] >= 0:
                # 중력 작용
                r, c = i, j
                nr, nc = i + 1, j
                while 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == -2:
                    grid[r][c], grid[nr][nc] = grid[nr][nc], grid[r][c]
                    r, c = nr, nc
                    nr += 1


def rotate():
    new_grid = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            new_grid[n - 1 - j][i] = grid[i][j]

    return new_grid


n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

while True:
    gameover = 1
    cur_bomb = []
    red_cnt = 0

    # 1. 폭탄 묶음 생성
    visited = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(n):
            if grid[i][j] > 0 and not visited[i][j]:
                cnt = get_bomb(i, j, grid[i][j])
                if cnt > 1:
                    gameover = 0

    # [게임오버]
    if gameover:
        break

    # 2. 해당 폭탄 전부 제거 & 중력 작용
    for r, c in cur_bomb:
        grid[r][c] = -2
    gravity()

    # 3. 반시계방향으로 회전
    grid = rotate()

    # 4. 다시 중력 작용
    gravity()

    # 5. 점수 계산
    ans += len(cur_bomb) ** 2

print(ans)