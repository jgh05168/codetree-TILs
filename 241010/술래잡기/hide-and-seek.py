'''
19:45

n x n, 술래 시작점은 정중앙
m명의 도망자 존재 : 도망자는 좌우 또는 상하로만 움직인다.
    - 좌우 : 오른쪽 보고 시작
    - 상하 : 아래쪽 보고 시작
나무 : 나무가 도망자와 초기에 겹쳐서 주어질 수 있음
m명의 도망자가 먼저 동시에 움직이고, 술래가 움직인다

[도망자 움직임]
- 현재 술래와의 거리가 3이하인 도망자만 움직인다.
    - 격자를 벗어나지 않는 경우
        - 움직이려는 칸에 술래가 있는 경우 움직이지 않는다.
        - 술래가 없다면 해당 칸으로 이동. 나무가 있어도 ok
    - 격자를 벗어나는 경우
        - 반대로 방향을 틀어주고 이동
        - 해당 칸에 술래가 없을 경우만 이동 가능

[술래 움직임]
달팽이 모양으로 움직인다.
- 만약 끝에 도달하게 되면, 다시 거꾸로 중심까지 이동
- 1번의 턴 동안 정확히 한 칸 해당하는 방향으로 이동한다.
    - 이동 후 방향이 틀어지는 지점이라면 방향을 바로 틀어준다.
    - (0, 0), 중앙 에 도달하는 경우에도 방향을 바로 틀어준다.

[술래잡기]
술래는 턴을 넘기기 전에 시야 내에 있는 도망자를 잡게된다.
- 시야 : 현재 바라보고 있는 방향을 기준으로 현재 칸 포함 3칸
- 나무가 놓여있는 칸이라면 잡히지 않는다
- 도망자가 잡힌 경우, 사라진다
현재 턴 x 잡힌 도망자 수 만큼 점수 획득

미리 달팽이맵 만들어두기

'''

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

path = []
tree = []
runners = [0]


def get_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def make_path():
    global path
    r, c = 0, 0
    d = 1
    idx = n * n
    while (r, c) != catcher:
        path[r][c] = idx
        idx -= 1
        r, c = r + dr[d], c + dc[d]
        if not (0 <= r < n and 0 <= c < n) or path[r][c]:
            r, c = r - dr[d], c - dc[d]
            d = (d - 1) % 4
            r, c = r + dr[d], c + dc[d]
    path[r][c] = idx


def move_runners():
    global grid, runners
    for runner in range(1, m + 1):
        if not runners[runner]:
            continue
        r, c, d = runners[runner]
        # 술래와의 거리 계산하기
        dist = get_distance(r, c, catcher[0], catcher[1])
        # 거리가 3 이하인 애들만 움직인다.
        if dist <= 3:
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n:
                if (nr, nc) != catcher:
                    grid[r][c].remove(runner)
                    grid[nr][nc].append(runner)
                    runners[runner] = (nr, nc, d)
            else:
                nd = (d + 2) % 4
                nr, nc = r + dr[nd], c + dc[nd]
                if (nr, nc) != catcher:
                    grid[r][c].remove(runner)
                    grid[nr][nc].append(runner)
                    runners[runner] = (nr, nc, nd)

def move_catcher():
    global catcher
    r, c = catcher
    cur_loc = path[r][c]
    if not reverse:
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n:
                if path[nr][nc] == cur_loc + 1:
                    catcher = (nr, nc)
                    return
    else:
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n:
                if path[nr][nc] == cur_loc - 1:
                    catcher = (nr, nc)
                    return


def update_catcher(catcher):
    global reverse, catcher_d
    r, c = catcher
    if (r, c) == (0, 0) or (r, c) == (n // 2, n // 2):
        reverse = True if not reverse else False
        catcher_d = (catcher_d + 2) % 4
    else:
        cur_loc = path[r][c]
        if not reverse:
            for d in range(len(dr)):
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < n and 0 <= nc < n and path[nr][nc] == cur_loc + 1:
                    catcher_d = d
                    return
        else:
            for d in range(len(dr)):
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < n and 0 <= nc < n and path[nr][nc] == cur_loc - 1:
                    catcher_d = d
                    return


def catch(t, catcher):
    r, c = catcher
    tmp, idx = 0, 0
    while 0 <= r < n and 0 <= c < n and idx < 3:
        # 술래를 잡은 경우
        if grid[r][c] and not tree[r][c]:
            while grid[r][c]:
                runner = grid[r][c].pop()
                runners[runner] = 0
                tmp += 1
        r, c = r + dr[catcher_d], c + dc[catcher_d]
        idx += 1

    return t * tmp


n, m, h, k = map(int, input().split())
path = [[0] * n for _ in range(n)]
tree = [[0] * n for _ in range(n)]
grid = [[[] for _ in range(n)] for _ in range(n)]
for r in range(1, m + 1):
    x, y, d = map(int, input().split())
    runners.append((x - 1, y - 1, d - 1))
    grid[x - 1][y - 1].append(r)
for _ in range(h):
    x, y = map(int, input().split())
    tree[x - 1][y - 1] = 1

catcher = (n // 2, n // 2)
make_path()
reverse = False
catcher_d = 3
ans = 0

for t in range(1, k + 1):
    # 1. 도망자 이동
    move_runners()

    # 2. 술래 이동
    move_catcher()
    update_catcher(catcher)

    # 3. 술래잡기
    ans += catch(t, catcher)

print(ans)