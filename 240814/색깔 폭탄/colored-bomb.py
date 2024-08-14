'''
-1, 0, 1이상 숫자로 이루어진 n x n

-1 : 검은색 돌
0 : 빨간색 폭탄
>1 : 빨간색과는 다른 서로 다른 색의 폭탄

더 이상 폭탄 묶음이 없을 떄까지 반복
1. 현재 격자에서 가장 큰 폭탄 묶음 찾기
    - 2개 이상의 폭탄으로 이루어져 있어야 한다.
    - 모두 같은 색 or 빨간색 폭탄을 포함하여 정확히 2개의 색깔로만 이루어진 폭탄
    - 빨간색 폭탄으로만 이루어져 있는 경우는 폭탄 묶음이 아니다.
    - 모든 폭탄 묶음은 인접해 잇어야 한다.
    선택 방법 :
        1. 크기가 큰 폭탄 묶음들 중 빨간색 폭탄이 가장 적게 포함된 것
        2. 기준점 중 행이 큰 순
        3. 기준점 중 열이 작은 순
2. 폭탄 제거
    - 중력 작용.
    - 돌은 떨어지지 않음
3. 회전 : 반시계방향 90도
4. 다시 중력이 작용

폭탄은 터지면서 폭탄의 개수 c * c 만큼 점수를 얻는다.

풀이:
시뮬레이션
'''

from collections import deque
import sys
input = sys.stdin.readline

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]


def get_bomb_list(sr, sc, color):
    queue = deque([(sr, sc)])
    visited[sr][sc] = 1
    tmp_bomb_list = [(sr, sc)]
    tmp_red_bombs = 0

    while queue:
        r, c = queue.popleft()

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] in [color, 0]:
                tmp_bomb_list.append((nr, nc))
                # 같은 색깔인 경우에만 방문 처리
                if grid[nr][nc] == color:
                    visited[nr][nc] = 1
                else:
                    tmp_red_bombs += 1
                queue.append((nr, nc))

    return tmp_bomb_list, tmp_red_bombs


def rotate():
    new_grid = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            new_grid[n - 1 - j][i] = grid[i][j]

    return new_grid



def gravity():
    for j in range(n):
        for i in range(n - 2, -1, -1):
            if grid[i][j] > 0:
                tmp_i = i + 1
                while tmp_i < n and grid[tmp_i][j] < -1:
                    tmp_i += 1
                grid[tmp_i - 1][j], grid[i][j] = grid[i][j], grid[tmp_i - 1][j]


n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

bomb_list = []
ans = 0
while True:
    # 0. 사전 준비
    visited = [[0] * n for _ in range(n)]
    red_bombs = n * n

    # 1-1. 폭탄 고르기
    for i in range(n - 1, -1, -1):
        for j in range(n):
            if not visited[i][j] and grid[i][j] > 0:
                new_bomb_list = []
                new_bomb_list, new_red_bombs = get_bomb_list(i, j, grid[i][j])
                if len(new_bomb_list) > len(bomb_list):
                    bomb_list = new_bomb_list
                    red_bombs = new_red_bombs
                elif len(new_bomb_list) == len(bomb_list):
                    if red_bombs > new_red_bombs:
                        bomb_list = new_bomb_list
                        red_bombs = new_red_bombs
    # (종료 조건) 터질 폭탄이 없는 경우
    if len(bomb_list) < 2:
        break

    # 1-3. 폭탄 터트리기
    bomb_size = len(bomb_list)
    while bomb_list:
        i, j = bomb_list.pop()
        grid[i][j] = -2

    # 2. 중력 작용
    gravity()

    # 3. 반시계 방향으로 회전
    grid = rotate()

    # 4. 한 번 더 중력 작용
    gravity()

    # 5. 점수 산출
    ans += bomb_size * bomb_size

print(ans)