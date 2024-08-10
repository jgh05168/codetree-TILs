'''
n x n
제초제 : k범위만큼 대각선으로 퍼짐
    - 벽이 있는 경우 가로막힘
1. 인접한 네 칸 중 나무가 있는 칸의 수만큼 나무 성장
    - 성장은 모든 나무에게 동시에 일어남
2. 기존에 있던 나무들은 인접한 4개의 칸에 번식 진행
    - 벽, 다른 나무, 제초제 모두 없는 칸에 번식 진행
    - 나무 그루 수 // 총 번식이 가능한 칸의 개수
    - 번식 과정은 모든 나무에서 동시에 일어남 ( 새로 자란 나무는 이후에 적용하기 )
3. 각 칸 중 제초제를 뿌렸을 떄 나무가 가장 많이 박멸되는 칸에 제초제 뿌리머
    - 나무가 있는 칸에 뿌리면 4개의 대각선 방향으로 k 칸만큼 전파된다.
    - 전파 도중 벽이 있거나, 나무가 없는 칸이 있다면 칸까지 뿌려지고, 전파 중지
    - c년만큼 제초제가 남아있다가 c + 1일 때 사라짐
    - 제초제가 뿌려진 곳에 다시 뿌려지는 경우, c년으로 초기화
주의:
    - 박멸시키는 나무의 수가 동일한 경우,
        - 행, 열 순으로 우선순의를 갖는다.

풀이:
grid, 제초제 grid 생성
나무 위치 배열
초반 나무 위치 알아두기
'''

from collections import deque
import sys
input = sys.stdin.readline

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

ddr = [1, 1, -1, -1]
ddc = [1, -1, -1, 1]


def growup():
    for i in range(len(tree_loc)):
        r, c = tree_loc[i]
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < N and 0 <= nc < N and grid[nr][nc] > 0 and not herbicide_grid[nr][nc]:
                grid[r][c] += 1

def breeding():
    new_tree = []
    new_grid = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if grid[i][j] == -1:
                new_grid[i][j] = grid[i][j]

    for i in range(len(tree_loc)):
        r, c = tree_loc[i]
        tree_level = grid[r][c]
        new_grid[r][c] = tree_level
        tmp_new_tree = []
        can_grow = 0
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < N and 0 <= nc < N and not grid[nr][nc] and not herbicide_grid[nr][nc]:
                can_grow += 1
                tmp_new_tree.append((nr, nc))
        for nr, nc in tmp_new_tree:
            new_grid[nr][nc] += tree_level // can_grow
        new_tree.extend(tmp_new_tree)
    tree_loc.extend(new_tree)

    return new_grid


def remove_tree(sr, sc):
    global rm_tree_cnt, herbicide
    tmp_rm_cnt = grid[sr][sc]
    queue = deque([(sr, sc, 0, 0), (sr, sc, 1, 0), (sr, sc, 2, 0), (sr, sc, 3, 0)])
    tmp_herbicide = [(sr, sc)]

    while queue:
        r, c, d, spread = queue.popleft()

        nr, nc = r + ddr[d], c + ddc[d]
        nspread = spread + 1
        if 0 <= nr < N and 0 <= nc < N and nspread <= K:
            if grid[nr][nc] > 0:
                tmp_rm_cnt += grid[nr][nc]
                queue.append((nr, nc, d, spread + 1))
            tmp_herbicide.append((nr, nc))
    # 새 위치 계산
    if rm_tree_cnt < tmp_rm_cnt:
        rm_tree_cnt = tmp_rm_cnt
        herbicide = tmp_herbicide


def spread_herbicide():
    for r, c in herbicide:
        herbicide_grid[r][c] = C + 1
        grid[r][c] = 0
    new_tree_loc = list(set(tree_loc).difference(set(herbicide)))
    return new_tree_loc


def decrease_herbicide():
    for i in range(N):
        for j in range(N):
            if herbicide_grid[i][j] > 0:
                herbicide_grid[i][j] -= 1


N, M, K, C = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
herbicide_grid = [[0] * N for _ in range(N)]
tree_loc = []

for i in range(N):
    for j in range(N):
        if grid[i][j] > 0:
            tree_loc.append((i, j))

herbicide = []
ans = 0
for _ in range(M):
    # 0. 초기 세팅
    rm_tree_cnt = 0

    # 1. 주변 나무 파악 후 나무 성장
    growup()

    # 2. 번식 진행
    grid = breeding()

    # 3 - 1. 제초제 살포 확인
    tree_loc.sort(key=lambda x: (x[0], x[1]))
    for i, j in tree_loc:
        remove_tree(i, j)

    # 3 - 2. 제초제 살포
    tree_loc = spread_herbicide()
    ans += rm_tree_cnt

    # 3 - 3. 제초제 죽이기
    decrease_herbicide()


print(ans)