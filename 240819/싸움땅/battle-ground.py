'''
n x n, 각 격자에는 무기들이 들어있음
초기에 플레이어들은 무기들이 없는 빈 격자에 위치하며, 초기 능력치를 갖는다.

1. 첫번째 플레이어부터 "순차적으로" 본인이 향하고 있는 방향대로 한 칸 이동한다.
    - 격자를 벗어나는 경우, 정반대로 이동
2-1. 이동한 방향에 플레이어가 없다면, 해당 칸에 총이 있는지 확인
    - 총이 있는 경우, 해당 플레이어는 총을 획득
    - 이미 총을 갖고 있는 경우, 공격력이 더 쎈 총을 선택하고, 나머지 총들은 해당 격자에 두고 온다.
2-2. 이동한 방향에 플레이어가 있다면, 두 플레이어가 싸운다.
    - 해당 플레이어의 초기 능력치와 갖고 있는 총의 공격력 합을 비교하여 더 큰 플레이어 승리
    - 수치가 같은 경우, 초기 능력치가 높은 플레이어가 승리
    - 이긴 플레이어는 각 플레이어의 공격력의 차이만큼 점수 획득(본인능력 + 총)
    2-2-1. 진 플레이어는 본인이 가진 총을 해당 격자에 내려놓고, 본인의 방향으로 한 칸 이동
        - 만약 이동하려는 칸에 다른 플레이어 or 격자범위 밖인 경우, 오른쪽으로 90도 회전하며 빈 칸이 보이는 순간 이동
        - 해당 칸에 총이 있다면, 총 바꾸기
    2-2-2. 이긴 플레이어는 승리한 칸에 떨어진 총들과 비교 후 더 공격력 높은 총 획득

풀이:
그냥 시뮬레이션 ..?
grid : 총, 플레이어
list 사용해서 플레이어 데이터 업데이트

'''

import sys
input = sys.stdin.readline

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


def lose_move(loser, r, c):
    sr, sc = players[loser[0]]
    _, d, s, g = loser
    if g:
        guns[r][c].append(g)
    g = 0
    for dd in range(len(dr)):
        nr, nc = r + dr[(d + dd) % 4], c + dc[(d + dd) % 4]
        if 0 <= nr < n and 0 <= nc < n and not p_grid[nr][nc]:
            if guns[nr][nc]:
                guns[nr][nc].sort()
                new_gun = guns[nr][nc].pop()
                if new_gun > g:
                    # 만약 총이 있는 상태라면, 내려놓기
                    if g:
                        guns[nr][nc].append(g)
                    g = new_gun
                else:
                    guns[nr][nc].append(new_gun)
            p_grid[sr][sc] = 0
            players[loser[0]] = (nr, nc)
            p_grid[nr][nc] = [loser[0], (d + dd) % 4, s, g]
            break


def win_move(winner, r, c):
    new_gun = guns[r][c]
    sr, sc = players[winner[0]]
    _, d, s, g = winner
    if guns[r][c]:
        guns[r][c].sort()
        new_gun = guns[r][c].pop()
        if new_gun > g:
            # 만약 총이 있는 상태라면, 내려놓기
            if g:
                guns[r][c].append(g)
            g = new_gun
        else:
            guns[r][c].append(new_gun)
    players[winner[0]] = (r, c)
    p_grid[r][c] = [winner[0], d, s, g]


def move_players():
    for i in range(1, m + 1):
        r, c = players[i]
        player, d, stat, gun = p_grid[r][c]
        nr, nc = r + dr[d], c + dc[d]
        # 만약 격자 밖으로 벗어났다면, 방향 전환
        if not (0 <= nr < n and 0 <= nc < n):
            d = (d + 2) % 4
            nr, nc = r + dr[d], c + dc[d]
        # 플레이어 체크
        # 사람이 없다면
        if not p_grid[nr][nc]:
            # 플레이어가 없다면, 총을 획득
            if guns[nr][nc]:
                guns[nr][nc].sort()
                new_gun = guns[nr][nc].pop()
                if new_gun > gun:
                    # 만약 총이 있는 상태라면, 내려놓기
                    if gun:
                        guns[nr][nc].append(gun)
                    gun = new_gun
                else:
                    guns[nr][nc].append(new_gun)
            p_grid[nr][nc] = [player, d, stat, gun]
            p_grid[r][c] = 0
            players[player] = (nr, nc)
        # 사람이 있다면,
        else:
            # 능력치 비교
            new_player, nd, nstat, ngun = p_grid[nr][nc]
            p_stat, np_stat = stat + gun, nstat + ngun
            if p_stat > np_stat:
                points[player] += (p_stat - np_stat)
                win_player = [player, d, stat, gun]
                lose_player = [new_player, nd, nstat, ngun]
            elif p_stat < np_stat:
                points[new_player] += (np_stat - p_stat)
                win_player = [new_player, nd, nstat, ngun]
                lose_player = [player, d, stat, gun]
            else:
                # 초기 눙력치 비교
                if stat > nstat:
                    points[player] += (p_stat - np_stat)
                    win_player = [player, d, stat, gun]
                    lose_player = [new_player, nd, nstat, ngun]
                else:
                    points[new_player] += (np_stat - p_stat)
                    win_player = [new_player, nd, nstat, ngun]
                    lose_player = [player, d, stat, gun]
            p_grid[r][c], p_grid[nr][nc] = 0, 0

            # 2. 총 두고 떠나기
            lose_move(lose_player, nr, nc)
            win_move(win_player, nr, nc)


n, m, k = map(int, input().split())
guns = [list(map(int, input().split())) for _ in range(n)]      # 총 여러개 가능
for i in range(n):
    for j in range(n):
        if guns[i][j]:
            guns[i][j] = [guns[i][j]]
        else:
            guns[i][j] = []
p_grid = [[0] * n for _ in range(n)]
players = [0]
points = [0] * (m + 1)
for p in range(1, m + 1):
    x, y, d, s = map(int, input().split())
    p_grid[x - 1][y - 1] = [p, d, s, 0]        # 플레이어, 방향, 초기능력치, 총 공격력
    players.append((x - 1, y - 1))             # 플레이어 위치 정보만 담기

for _ in range(k):
    # 1. 플레이어 이동
    move_players()

print(*points[1:])