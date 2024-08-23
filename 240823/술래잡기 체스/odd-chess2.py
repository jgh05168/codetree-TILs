'''
4 x 4
술래 말이 도둑 말을 잡으면, 잡은 도둑말의 방향을 갖게 된다.
8가지 방향 존재
1. 초기 0, 0 도둑말을 잡으며 시작
2. 도둑말은 번호가 작은 순서대로 본인이 가지고 있는 이동 방향대로 이동
    - 한 칸 씩 이동
    - 빈 칸이나 다른 도둑말이 있는 칸은 이동이 가능한 칸
    - 이동할 수 있을 때까지 45도 반시계 회전
    - 이동할 수 있는 칸이 없다면, 이동하지 않기.
    - 해당 칸에 도둑말이 있다면, 해당 말과 위치를 바꾼다.
3. 술래말 이동
    - 이동 가능한 방향의 어느 칸이나 이동 가능(여러개의 칸도 가능)
    - 술래말은 무조건 도둑말이 있는 칸만 이동 가능함
4. 술래말이 이동할 수 있는 곳에 도둑말이 없다면, 종료

풀이:
술래는 잡을 수 있는 말을 모조리 잡아봐야 한다. (완전탐색)
최대 16번 재귀 들어간다.
'''

import sys, copy
input = sys.stdin.readline

dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, -1, -1, -1, 0, 1, 1, 1]


def thief_move(grid, thief_alive):
    for i in range(17):
        if not thief_alive[i]:
            continue
        r, c = thief_alive[i]
        num, sd = grid[r][c]
        for d in range(len(dr)):
            nd = (sd + d) % len(dr)
            nr, nc = r + dr[nd], c + dc[nd]
            if 0 <= nr < 4 and 0 <= nc < 4 and (nr, nc) != (pr, pc):
                if not grid[nr][nc]:
                    grid[nr][nc], grid[r][c] = (num, nd), 0
                    thief_alive[i] = (nr, nc)
                else:
                    nnum, nnd = grid[nr][nc]
                    grid[nr][nc], grid[r][c] = (i, nd), grid[nr][nc]
                    thief_alive[i], thief_alive[nnum] = thief_alive[nnum], thief_alive[i]
                break

    return grid, thief_alive


def dfs(move, val, grid, thief_locs, pr, pc, pd):
    global ans
    # 1. 도둑 움직이기
    new_grid, new_thief_locs = thief_move(grid, thief_locs)

    # 2. 술래 움직이기
    while 0 <= pr < 4 and 0 <= pc < 4:
        nr, nc = pr + dr[pd], pc + dc[pd]
        if not (0 <= nr < 4 and 0 <= nc < 4) or not new_grid[nr][nc]:
            ans = max(ans, val)
            break
        v, nd = grid[nr][nc]
        new_grid[nr][nc] = 0
        new_thief_locs[v] = 0
        dfs(move + 1, val + v, copy.deepcopy(new_grid), copy.deepcopy(new_thief_locs), nr, nc, nd)
        new_grid[nr][nc] = (v, nd)
        new_thief_locs[v] = (nr, nc)
        pr, pc = nr, nc

grid = []
thief_alive = [0] * 17
for i in range(4):
    arr = list(map(int, input().split()))
    tmp = []
    for j in range(0, 8, 2):
        tmp.append((arr[j], arr[j + 1] - 1))
        thief_alive[arr[j]] = (i, j // 2)
    grid.append(tmp)

pr, pc, pd = 0, 0, grid[0][0][1]
thief_alive[grid[0][0][0]] = 0
start = grid[0][0][0]
grid[0][0] = 0

ans = start
dfs(0, start, grid, thief_alive, pr, pc, pd)

print(ans)