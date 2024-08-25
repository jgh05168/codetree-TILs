'''
n x n
1. 턴이 한 번 진행할 때 각 플레이어들 한 칸 씩 이동
    - 해당 칸에 이동했을 때, 플레이어는 해당 칸을 독점 계약한다.
    - 초기 땅 역시 해당 플레이어의 땅
    1-1. 독점 계약은 k턴동안만 유효하다.
        - k턴이 지나면, 해당 칸은 다시 주인이 없는 땅이 된다.
2. 각 플레이어는 방향 별로 이동 우선순위를 갖는다.
    2-1. 인접한 상하좌우 4칸 중 아무도 독점계약을 맺지 않은 칸으로 이동
    2-2. 만약 그런 칸이 없는 경우, 인접 칸 중본인이 독점계약한 땅으로 이동
    2-3. 이동할 수 있는 칸이 여러개라면, 이동 우선순위를 따진다.
    - 플레이어가 보고 있는 방향은 그 직전에 이동한 방향임
3. 모든 플레이어가 이동한 후 한 칸에 여러 플레이어가 있을 경우, 가장 작은 플레이어만 살아남고, 나머진 죽는다

주의 :
- 한 칸에 여러 명이 있는 경우, 살아남은 자가 독점 계약을 한다. min()으로 판단하기
-

순서 :
1. 각 플레이어 이동
    - min 사용
2. 살아남은 자들에 대해서 땅 업데이트
3. 땅 정보 한 칸씩 줄여주기

종료 조건 : 1번 플레이어만 살아남기까지 걸리는 턴의 개수
'''

import sys
input = sys.stdin.readline

dr = [0, -1, 1, 0, 0]
dc = [0, 0, 0, -1, 1]


def move_players():
    new_grid = [[[] * n for _ in range(n)] for _ in range(n)]
    # 그냥 한 명씩 움직이기
    for i in range(1, m + 1):
        if not player_loc[i]:
            continue
        r, c = player_loc[i]
        d = player_dir[i]

        adj_monopoly_list = 0
        check_empty_space = False
        # 첫번째 조건에서는 갈 수 있는 빈 땅이 있는 지만 체크한다.
        for nd in each_player_d[i][d]:
            nr, nc = r + dr[nd], c + dc[nd]
            # 못 가는 조건 : 격자 벗어나거나, 내 땅이 아니거나, 상대방이 있는 경우
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if not monopoly[nr][nc]:
                new_grid[nr][nc].append(i)
                player_loc[i] = (nr, nc)
                player_dir[i] = nd
                break
            elif monopoly[nr][nc][0] == i and not adj_monopoly_list:
                adj_monopoly_list = (nr, nc, nd)
        else:
            # 빈 공간을 찾았었는지 확인
            nr, nc, nd = adj_monopoly_list
            new_grid[nr][nc].append(i)
            player_loc[i] = (nr, nc)
            player_dir[i] = nd

    return new_grid


def remove_players():
    global total_player
    for i in range(n):
        for j in range(n):
            if len(grid[i][j]) > 1:
                while len(grid[i][j]) > 1:
                    player = grid[i][j].pop()
                    player_loc[player] = 0
                    player_dir[player] = 0
                    total_player -= 1


def register_monopoly():
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                monopoly[i][j] = (grid[i][j][0], k)
            elif monopoly[i][j]:
                p, t = monopoly[i][j]
                t -= 1
                if not t:
                    monopoly[i][j] = 0
                else:
                    monopoly[i][j] = (p, t)


n, m, k = map(int, input().split())
grid_input = [list(map(int, input().split())) for _ in range(n)]
player_dir = [0] + list(map(int, input().split()))
each_player_d = [0]
for _ in range(m):
    each_player_d.append([0] + [list(map(int, input().split())) for _ in range(4)])
monopoly = [[0] * n for _ in range(n)]
grid = [[[] * n for _ in range(n)] for _ in range(n)]

player_loc = [0] * (m + 1)
for i in range(n):
    for j in range(n):
        if grid_input[i][j]:
            player_loc[grid_input[i][j]] = (i, j)
            grid[i][j].append(grid_input[i][j])
            monopoly[i][j] = (grid_input[i][j], k)

total_player = m
ans = 0
while ans < 1000:
    # 1. 플레이어 이동
    grid = move_players()

    # 2. 겹치는 부분 제거
    remove_players()

    # 3. 모노폴리에 등록
    register_monopoly()

    ans += 1
    if total_player == 1:
        break

if ans >= 1000:
    print(-1)
else:
    print(ans)