'''
N * M 격자 존재
공격력이 0 이면 포탑은 부서진 것임

하나의 턴은 4가지 액션을 순서대로 수행하며, 총 K 번 반복된다.
부서지지 않은 포탑이 1개가 된다면 즉시 중지

1. 공격자 선정
    부서지지 않은 포탑 중 가장 약한 포탑이 공격자로 선정 - N + M 만큼의 공격력이 증가
    - heapq(공격력, -공격시기, -(행 + 열), -열)

2. 공격자의 공격
    가장 강한 포탑을 공격한다(공격력이 가장 높은 포탑)
    - heapq(공격력, 공격시기, 행 + 열, 열)

    (1) 레이저 공격
        1. 상하좌우 4개의 방향으로 움직인다.
        2. 부서진 포탑이 있는 위치를 마주할 시 종료
        3. 가장자리에서 막힌 방향으로 진행하고자 한다면 반대편으로 나온다. - (cur_loc + 1) % N(M)
        4. 공격 대상 포탑까지의 최단 경로로 공격한다. -> 경로가 없으면 공격 불가능.
            방향이 정해졌으므로, dfs수행.
        5. 최단 경로가 정해졌다면, 공격. 공격 경로에 있느 사람은 공격력 // 2 데미지를 입는다.
    (2) 포탄 공격
        1. 공격 대상에게 포탄을 던지면 공격력만큼 피해를 입는다.
        2. 칸을 뛰어넘을 수 있다.
        3. 공격피해는 레이저와 동일

3. 수리
    공격과 무관했던 포탑은 공격력 1 증가.
'''

from collections import deque
import heapq, copy

#    동 동남 남 남서 서 북서 북 동북
dr = [0, 1, 1, 1, 0, -1, -1, -1]
dc = [1, 1, 0, -1, -1, -1, 0, 1]

lazer_dr = [-1, 0, 1, 0]
lazer_dc = [0, -1, 0, 1]


def lazer_loc(srow, scol):
    queue = deque()
    queue.append((srow, scol, []))
    visited[srow][scol] = 1

    while queue:
        row, col, p = queue.popleft()

        if (row, col) == (defender_row, defender_col):
            return True, p

        for d in range(0, len(dr), 2):
            nrow, ncol = (row + dr[d]) % N, (col + dc[d]) % M
            if not visited[nrow][ncol] and grid[nrow][ncol]:
                visited[nrow][ncol] = visited[row][col] + 1
                if (nrow, ncol) == (defender_row, defender_col):
                    return True, p + [(nrow, ncol)]
                queue.append((nrow, ncol, p + [(nrow, ncol)]))

    return False, p

N, M, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
recent_attacks = [[0] * M for _ in range(N)]

for attack in range(1, K + 1):          # K 턴만큼 진행
    # 초기 포탑 위치 확인 - 공격자, 가장 강한 포탑 선정
    attackers = []
    defenders = []
    towers = 0
    for srow in range(N):
        for scol in range(M):
            if grid[srow][scol]:
                towers += 1
                heapq.heappush(attackers, (grid[srow][scol], -recent_attacks[srow][scol], -(srow + scol), -scol))
                heapq.heappush(defenders, (-grid[srow][scol], recent_attacks[srow][scol], (srow + scol), scol))

    if towers == 1:         # 포탑이 하나만 남은 것임
        break

    attacker = heapq.heappop(attackers)
    attacker_row, attacker_col = abs(attacker[2]) - abs(attacker[3]), abs(attacker[3])
    grid[attacker_row][attacker_col] += (N + M)
    defender = heapq.heappop(defenders)
    defender_row, defender_col = defender[2] - defender[3], defender[3]
    recent_attacks[attacker_row][attacker_col] = attack     # 공격한 횟수 업데이트(높을수록 최근에 공격함)
    # 레이저 공격 or 포탑 공격
    lazer_locs = []
    visited = [[0] * M for _ in range(N)]
    check_lazer, lazer_locs = lazer_loc(attacker_row, attacker_col)

    attacked_list = [[0] * M for _ in range(N)]
    attacked_list[attacker_row][attacker_col] = 1
    attacked_list[defender_row][defender_col] = 1

    if not check_lazer:       # 레이저 공격 불가능 -> 포탄 공격
        grid[defender_row][defender_col] -= grid[attacker_row][attacker_col]    # 포탄 맞았다!
        # 주위 포탑들 스플래시 데미지
        for d in range(len(dr)):
            nrow, ncol = (defender_row + dr[d]) % N, (defender_col + dc[d]) % M
            if not attacked_list[nrow][ncol] and grid[nrow][ncol]:
                if grid[nrow][ncol] - (grid[attacker_row][attacker_col] // 2) <= 0:
                    grid[nrow][ncol] = 0
                else:
                    grid[nrow][ncol] -= (grid[attacker_row][attacker_col] // 2)
                attacked_list[nrow][ncol] = 1

    else:           # 레이저 공격이 가능하다.
        grid[defender_row][defender_col] -= grid[attacker_row][attacker_col]    # 포탄 맞았다!

        for loc in range(len(lazer_locs) - 1):
            nrow, ncol = lazer_locs[loc]
            if not attacked_list[nrow][ncol] and grid[nrow][ncol]:
                if grid[nrow][ncol] - (grid[attacker_row][attacker_col] // 2) <= 0:
                    grid[nrow][ncol] = 0
                else:
                    grid[nrow][ncol] -= (grid[attacker_row][attacker_col] // 2)
                attacked_list[nrow][ncol] = 1

    # 포탑 정비
    for erow in range(N):
        for ecol in range(M):
            if grid[erow][ecol] and not attacked_list[erow][ecol]:      # 공격에 관여하지 않았고 살아남은 포탑들
                grid[erow][ecol] += 1
            elif grid[erow][ecol] <= 0:         # 0 이하인 값들을 0으로 설정
                grid[erow][ecol] = 0

print(max(map(max, grid)))