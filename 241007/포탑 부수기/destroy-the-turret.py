'''
17:40

N x M
- 각 포탑에는 공격력이 존재
- 공격력이 0 이하이면 해당 포탑은 부숴진다
- 최초에 공격력이 0인 포탑이 존재할 수 있음

[공격자 선정]
부서지지 않은 포탑 중 가장 약한 포탑이 공격자로 선정
- 선정되면 N + M 만큼의 공격력이 증가한다.
선정기준
1. 공격력이 가장 낮은 포탑
2. 가장 최근에 공격한 포탑이 가장 약한 포탑으로 선정
3. 행과 열의 합이 큰 순서
4. 열 값이 가장 큰 포탑

[공격자의 공격]
- 자신을 제외한 가장 강한 포탑 공격
선정기준
1. 공격력이 가장 높은 포탑
2. 공격한지 가장 오래된 포탑
3. 행과 열의 합이 가장 작은 포탑
4. 열 값이 가장 작은 포탑

[공격 방식]
1) 레이저 공격
1. 상하좌우
2. 부서진 포탑이 있는 경우 break
3. 가장자리에서 막힌 방향으로 진행하는 경우 반대편으로 나온다.
- 공격자의 위치에서 최단 경로로 공격한다 ( dfs )
    -> 이런 경우가 존재하지 않는다면, 포탄 공격 진행
    - 우 하 좌 상 우선순위
공격 대상에는 공격자의 공격력만큼 피해를 입히고, 피해입은 포탑은 해당 수치만큼 줄어든다
레이저 경로의 포탑은 공격자 공격력의 절반만큼 공격받는다 (value // 2)
2) 포탄 공격
공격자의 공격력만큼 피해를 받는다
주위 8개 방향에 있는 포탑도 피해를 입는다(절반)
가장자리의 경우 반대편 격자에 추가 피해가 미친다

[포탑 파괴]
공격을 받아 공격력이 0이하인 포탑은 부숴진다

[포탑 정비]
부서지지 않은 포탑 중 공격과 무관했던 포탑은 공격력 1씩 증가 ( 공격 경로는 set으로 저장하기 )

남아있는 포탑 중 가장 강한 포탑의 공격력을 출력


사용 알고리즘:
우선순위큐 - 포탑 정보 저장(공격력, 최근 공격, -(행 + 열), -열)
        - 행은 세번쨰 정보에서 열 정보 빼서 확인
dfs - 최단경로 찾기 ( 우선순위가 존재하기 떄문 )
    - 이동 경로는 set으로 업데이트하기
'''

from collections import defaultdict
import heapq

# init()
dr = [0, 1, 0, -1, 1, 1, -1, -1]
dc = [1, 0, -1, 0, 1, -1, -1, 1]
path = set()
visited = []
turret_pq = []
move_cnt = 0
laser = 0


def laser_attack(r, c, tmp_path):
    global laser, move_cnt, path
    # 도착했다면, 레이저 경로 체크하기
    if (r, c) == (er, ec):
        tmp_move = len(tmp_path)
        if tmp_move < move_cnt:
            move_cnt = tmp_move
            path = set(tmp_path)
            laser = 1
        return
    if len(tmp_path) >= move_cnt:
        return
    for d in range(4):
        nr, nc = (r + dr[d]) % N, (c + dc[d]) % M
        if not visited[nr][nc] and grid[nr][nc]:
            visited[nr][nc] = 1
            laser_attack(nr, nc, tmp_path + [(nr, nc)])
            visited[nr][nc] = 0


def bomb_attack(r, c):
    global path
    path.add((r, c))
    for d in range(len(dr)):
        nr, nc = (r + dr[d]) % N, (c + dc[d]) % M
        if grid[nr][nc]:
            path.add((nr, nc))


N, M, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
for i in range(N):
    for j in range(M):
        if grid[i][j]:
            # 공격력 작은, 최근 공격(값 낮게), 행 + 열 큰, 열 큰
            heapq.heappush(turret_pq, (grid[i][j], 0, -(i + j), -j))

for _ in range(K):
    # 1. 공격자, 공격받을자 선정
    attacker = heapq.heappop(turret_pq)
    if not turret_pq:
        heapq.heappush(turret_pq, attacker)
        continue
    defender = heapq.nlargest(1, turret_pq)[0]

    # 2. 공격자와의 최단거리 찾기
    sr, sc = (-attacker[2]) + attacker[3], -attacker[3]
    er, ec = (-defender[2]) + defender[3], -defender[3]
    visited = [[0] * M for _ in range(N)]
    visited[sr][sc] = 1
    laser = 0
    path = set()
    move_cnt = N * M
    # 2-1. 레이저 공격
    laser_attack(sr, sc, [])      # 행, 열, 경로

    # 2-2. 포탄 공격(레이저 공격 실패 시)
    if not laser:
        bomb_attack(er, ec)

    # 3. 포탑 공격하기
    damage = attacker[0] + N + M
    grid[sr][sc] = damage
    for r, c in path:
        if (r, c) == (er, ec):
            grid[r][c] -= damage
        else:
            grid[r][c] -= damage // 2
        if grid[r][c] < 0:
            grid[r][c] = 0

    # 4. 포탑 재정비
    for i in range(N):
        for j in range(M):
            if (i, j) not in path and grid[i][j] and (i, j) != (sr, sc):
                grid[i][j] += 1

    # 5. 포탑 리스트 재정비
    new_turret = []
    while turret_pq:
        _, time, rowcol, col = heapq.heappop(turret_pq)
        row = (-rowcol) + col
        if grid[row][-col]:
            heapq.heappush(new_turret, (grid[row][-col], time + 1, rowcol, col))
    heapq.heappush(new_turret, (damage, 0, -(sr + sc), -sc))
    turret_pq = new_turret[:]
    heapq.heapify(turret_pq)

print(heapq.nlargest(1, turret_pq)[0][0])