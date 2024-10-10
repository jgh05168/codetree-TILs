'''
11:10

각각의 격자에는 무기들이 존재한다.
초기에는 무기가 없는 빈 격자에 플레이어가 위치하며, 초기 능력치를 갖는다.

1. 첫번째 플레이어부터 순차적으로 본인이 향하고 있는 방향대로 한 칸 이동한다.
    - 격자를 벗어나는 경우, 반대 방향으로 한 칸 이동한다.
2-1. 이동한 방향에 플레이어가 없다면 해당 칸에 총이 있는지 확인
    - 총이 있는 경우 해당 총 획득
    - 플레이어가 이미 총을 갖고있는 경우, 놓여있는 총들과 플레이어의 총을 비교한 뒤 더 쎈 총 획득
2-2. 이동한 방향에 플레이어가 잇다면 싸운다
    - 해당 플레이어의 초기 능력치와 갖고있는 총의 공격력의 합을 비교
    - 총의 능력치가 같은 경우, 초기 능력치로 승부
    - 이긴 플레이어는 전체 능력치 합의 차만큼 포인트 획득
2-3. 진 플레이어는 본인이 갖고있는 총을 해당 격자에 내려놓고 해당 플레이어가 원래 가던 방향으로 한 칸 이동
    - 다른 플레이어가 있거나 격자 밖인 경우 오른쪽으로 90도씩 회전하여 빈 칸이 보이는 순간 이동
    - 해당 칸에 총이 있다면 해당 플레이어는 총 획득. 나머지 총은 내려놓는다.
2-4. 이긴 플레이어는 승리한 칸에 떨어진 총들과 원래있던 총 중 가장 공격력이 높은 총을 획득.
    - 나머지는 격자에 내려놓는다.

필요한 리스트
획득한 점수
플레이어 위치 격자
플레이어가 소지한 총
heapq

'''

import heapq

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


point = []
player_grid = []
player_stats = []


def change_guns(p, nr, nc):
    gun_power = heapq.heappop(guns[nr][nc])
    if not player_stats[p][1]:
        player_stats[p][1] = -gun_power
    else:
        if player_stats[p][1] < -gun_power:
            heapq.heappush(guns[nr][nc], -player_stats[p][1])
            player_stats[p][1] = -gun_power
        else:
            heapq.heappush(guns[nr][nc], gun_power)


def move(p):
    r, c, d = player_loc[p]
    nr, nc = r + dr[d], c + dc[d]
    # 범위 벗어난다면 뒤돌아서 이동
    if not (0 <= nr < n and 0 <= nc < n):
        d = (d + 2) % 4
        nr, nc = r + dr[d], c + dc[d]
    player_grid[r][c] = 0
    player_loc[p] = (nr, nc, d)

    # 만약 이동한 땅에 누군가가 있는지 확인
    if player_grid[nr][nc]:
        # 싸우기
        win, lose = fight(p, player_grid[nr][nc])
        # 이긴애 진애 처신해주기
        lose_move(lose)
        win_move(win)
    # 없다면 총 바꿔치기
    else:
        player_grid[nr][nc] = p
        if guns[nr][nc]:
            change_guns(p, nr, nc)



def fight(p1, p2):

    stat1, stat2 = sum(player_stats[p1]), sum(player_stats[p2])
    # 총 능력치가 같은 경우
    if stat1 == stat2:
        if player_stats[p1][0] > player_stats[p2][0]:
            point[p1] += stat1 - stat2
            return p1, p2
        else:
            point[p2] += stat2 - stat1
            return p2, p1
    elif stat1 > stat2:
        point[p1] += stat1 - stat2
        return p1, p2
    else:
        point[p2] += stat2 - stat1
        return p2, p1


def lose_move(p):
    r, c, d = player_loc[p]
    if player_grid[r][c] == p:
        player_grid[r][c] = 0
    # 총 내려놓기
    if player_stats[p][1]:
        heapq.heappush(guns[r][c], -player_stats[p][1])
        player_stats[p][1] = 0
    # 해당 방향으로 한 칸 이동
    for t in range(len(dr)):
        nd = (d + t) % 4
        nr, nc = r + dr[nd], c + dc[nd]
        if 0 <= nr < n and 0 <= nc < n and not player_grid[nr][nc]:
            # 플레이어 이동
            player_loc[p] = (nr, nc, nd)
            player_grid[nr][nc] = p
            if guns[nr][nc]:
                change_guns(p, nr, nc)
            else:
                player_stats[p][1] = 0
            break

def win_move(p):
    r, c, d = player_loc[p]
    if not player_grid[r][c]:
        player_grid[r][c] = p
    if guns[r][c]:
        change_guns(p, r, c)




# init()
n, m, k = map(int, input().split())
guns = [[[] for _ in range(n)] for _ in range(n)]
for i in range(n):
    gun = list(map(int, input().split()))
    for j in range(n):
        if gun[j]:
            heapq.heappush(guns[i][j], -gun[j])
player_grid = [[0 for _ in range(n)] for _ in range(n)]
player_stats = [0] * (m + 1)
player_loc = [0] * (m + 1)
point = [0] * (m + 1)
for i in range(1, m + 1):
    x, y, d, s = map(int, input().split())
    player_grid[x - 1][y - 1] = i
    player_loc[i] = (x - 1, y - 1, d)
    player_stats[i] = [s, 0]       # stat, guns


# 게임 시작
for _ in range(k):
    # 1. 플레이어 순차적으로 이동
    for p in range(1, m + 1):
        # 플레이어 이동
        move(p)

print(*point[1:])