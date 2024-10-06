'''
21:20

5 x 5, 유물조각은 1 ~ 7로 표현된다

[탐사 진행]
3 x 3 격자 선택
- 선택된 격자는 네 각도 모두 회전해야 한다.
- 가능한 회전의 방법 중
    1. 유물 1차 획득 가치를 최대화
    2. 회전한 각도가 가장 작은 방법을 선택
    3. 회전 중심 좌표의 열이 가장 작은, 행이 가장 작은 순으로 선택

[유물 획득]
유물 1차 획득
    - 상하좌우 인접한 같은 종류 조각이 3개 이상 연결되면, 유물이 되고 사라진다.
    - 유물의 가치 : 모인 조각의 개수
조각이 사라진 위치에는 유적의 벽면에 적힌 순서대로 새로운 조각이 생겨난다.
    1. 열번호가 작은 순, 행번호가 큰 순
    - 유적의 벽면 숫자는 재사용 불가능하다.
유물 연쇄 획득
    - 새로운 조각이 생겨난 이후, 3개 이상 연결되는 경우가 존재한다면, 탐사 재반복

[탐사 반복]
탐사 진행 과정에서 어떤 방법을 사용해서라도 유물을 획득할 수 없다면, 모든 탐사는 종료된다.


풀이 순서 :
1. 회전 : 5 x 5 x 3
2. 유물 1차 획득 해보기 -> 비교
3. 확정 된 다음, 조각 생겨나기
'''

from collections import deque

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]


# init()
visited = []


def rotate(si, sj, n, grid):
    new_grid = [row[:] for row in grid]
    for i in range(si, n + si):
        for j in range(sj, n + sj):
            oi, oj = i - si, j - sj
            ni, nj = oj, n - 1 - oi
            new_grid[ni + si][nj + sj] = grid[i][j]

    return new_grid


def bfs(num, grid, sr, sc):
    global visited
    queue = deque([(sr, sc)])
    visited[sr][sc] = 1

    tmp_list = []
    tmp_list.append((sr, sc))
    tmp = 1
    while queue:
        r, c = queue.popleft()

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] == num:
                queue.append((nr, nc))
                visited[nr][nc] = 1
                tmp_list.append((nr, nc))
                tmp += 1

    return tmp, tmp_list



def find_treasure():
    global visited
    max_tmp = 0
    new_grid = [row[:] for row in grid]
    max_piece = []
    min_rot = 4
    # 회전시키기
    for j in range(n - 2):
        for i in range(n - 2):
            tmp_grid = [row[:] for row in grid]
            for rot in range(3):
                tmp = 0
                tmp_list = []
                tmp_grid = rotate(i, j, 3, tmp_grid)
                # 유물 1차 획득해보기
                visited = [[0] * n for _ in range(n)]
                for r in range(n):
                    for c in range(n):
                        piece, piece_list = bfs(tmp_grid[r][c], tmp_grid, r, c)
                        if piece >= 3:
                            tmp += piece
                            tmp_list.extend(piece_list)
                if max_tmp < tmp and min_rot > rot:
                    max_tmp = tmp
                    min_rot = rot
                    max_piece = tmp_list[:]
                    new_grid = [row[:] for row in tmp_grid]

    return new_grid, max_tmp, max_piece


k, m = map(int, input().split())
n = 5
grid = [list(map(int, input().split())) for _ in range(n)]
treasure_list = deque(list(map(int, input().split())))



for _ in range(k):
    # 1. 유물 찾기
    total = 0
    grid, piece, piece_loc = find_treasure()

    # 2. 새로운 조각 놓기
    if not piece:
        break
    else:
        total += piece
        piece_loc.sort(key=lambda x: (x[1], -x[0]))
        for r, c in piece_loc:
            grid[r][c] = treasure_list.popleft()

    # 3. 연쇄작용해보기
    while True:
        tmp = []
        visited = [[0] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                piece, piece_list = bfs(grid[r][c], grid, r, c)
                if piece >= 3:
                    tmp.extend(piece_list)
        if not tmp:
            break
        total += len(tmp)
        tmp.sort(key=lambda x: (x[1], -x[0]))
        for r, c in tmp:
            grid[r][c] = treasure_list.popleft()

    # 유물 개수 출력
    print(total, end=' ')