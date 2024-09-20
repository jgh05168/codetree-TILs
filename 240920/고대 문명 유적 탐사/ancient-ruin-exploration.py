'''
5 x 5
유물 조각은 7가지 : 각각 숫자로 표현된다.

1. 탐사 진행 : 가능한 회전 방법 중
    1) 유물 1차 획득 가치 최대화
    2) 회전한 각도가 가장 작은 방법 선택
    3) 회전 중심  좌표의 열, 행 순으로 작은 구간 선택
    - 3 x 3 격자 선택, 회전 가능
    - 시계방향으로 90, 180, 270 회전 가능
    - 선택된 격자는 항상 회전해야 한다.
2. 유물 획득
    - 같은 종류의 조각들이 3개 이상 연결되어 있다면 유물이 된다.
    - 유물의 가치는 모인 조각의 개수와 같다
    - 유적의 벽면에는 조각이 사라졌을 때 새로 생겨나는 조각에 대한 정보가 있음
        - 조각이 사라진 위치에 유적 벽면의 순서대로 새로운 조각 생성
        1) 열번호 작은 순, 행 번호 큰 순
        - 숫자가 부족한 경우는 없다
        - 벽면의 숫자는 재사용 불가능
    - 벽면의 조각을 새로 삽입한 뒤에도 유물 판별하기
3. 탐사 반복
    - 각 턴마다 획득한 유물의 가치의 총합을 출력
    - 탐사 진행 과정에서 유물을 획득하지 못했다면 모든 탐사는 존재
    - 아무 유물도 획득하지 못했다면 아무 값도 출력하지 않는다.
'''

from collections import deque
import sys, copy
input = sys.stdin.readline

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]


def rotate(sr, sc):
    global relics, min_rotate, get_relics_list
    copy_grid = copy.deepcopy(grid)
    tmp_grid = [[0] * n for _ in range(n)]
    # 3번 rotate 해봐야 한다.
    for r in range(3):
        for i in range(sr, sr + 3):
            for j in range(sc, sc + 3):
                oi, oj = i - sr, j - sc
                ni, nj = oj, 3 - oi - 1
                tmp_grid[ni + sr][nj + sc] = copy_grid[i][j]
        # 나머지 채워넣기(90도 일 때만)
        if not r:
            for i in range(n):
                for j in range(n):
                    if not tmp_grid[i][j]:
                        tmp_grid[i][j] = grid[i][j]

        ### 2-1. 유물 1차 획득을 위해 출발
        visited = [[0] * n for _ in range(n)]
        tmp_relics = []
        for i in range(n):
            for j in range(n):
                if not visited[i][j]:
                    tmp_relics.extend(get_relics(i, j, visited, tmp_grid[i][j], tmp_grid))
        # 1차 유물이 더 크다면, 업데이트
        if len(tmp_relics) > relics:
            relics = len(tmp_relics)
            min_rotate = r
            for i in range(n):
                for j in range(n):
                    new_grid[i][j] = tmp_grid[i][j]
            get_relics_list = copy.deepcopy(tmp_relics)
        elif len(tmp_relics) == relics and r < min_rotate:
            min_rotate = r
            for i in range(n):
                for j in range(n):
                    new_grid[i][j] = tmp_grid[i][j]
            get_relics_list = copy.deepcopy(tmp_relics)

        copy_grid = copy.deepcopy(tmp_grid)


def get_relics(sr, sc, visited, num, grid):
    queue = deque([(sr, sc)])
    visited[sr][sc] = 1
    tmp = [(sr, sc)]
    while queue:
        r, c = queue.popleft()

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] == num:
                queue.append((nr, nc))
                visited[nr][nc] = 1
                tmp.append((nr, nc))

    if len(tmp) > 2:
        return tmp
    else:
        return []


k, m = map(int, input().split())
n = 5
grid = [list(map(int, input().split())) for _ in range(n)]
piece_list = deque(list(map(int, input().split())))

# 탐사 반복
for _ in range(k):
    ans = 0

    ### 1. 탐사 진행
    new_grid = [[0] * n for _ in range(n)]
    relics = 0
    min_rotate = 4
    get_relics_list = []
    for j in range(n - 2):
        for i in range(n - 2):
            rotate(i, j)

    ### 2-2. 유물 비우기
    get_relics_list.sort(key=lambda x: (x[1], -x[0]))
    for r, c in get_relics_list:
        new_piece = piece_list.popleft()
        new_grid[r][c] = new_piece

    ans += relics

    ### 2-3. 유물 n차 획득
    while True:
        visited = [[0] * n for _ in range(n)]
        tmp_relics = []
        for i in range(n):
            for j in range(n):
                if not visited[i][j]:
                    tmp_relics.extend(get_relics(i, j, visited, new_grid[i][j], new_grid))
        if not len(tmp_relics):
            break

        # 값 업데이트
        ans += len(tmp_relics)

        # 새로운 유물조각 채워넣기
        tmp_relics.sort(key=lambda x: (x[1], -x[0]))
        for r, c in tmp_relics:
            new_piece = piece_list.popleft()
            new_grid[r][c] = new_piece

    if not ans:
        break
    print(ans, end=' ')
    grid = copy.deepcopy(new_grid)