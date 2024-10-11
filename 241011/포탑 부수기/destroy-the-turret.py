'''
11:20

n x m
각 포탑에는 공격력이 존재함
공겪력이 0 이하가 된다면 해당 포탑은 부서진다
부서지지 않은 포탑이 1개가 된다면 그 즉시 중지

1. 공격자 선정
- 부서지지 않은 포탑 중 가장 약한 포탑이 공격자로 선정된다.
    - n + m 만큼의 공격력이 증가된다.
    가장 약한 포탑 :
        1. 공격력이 가장 낮은 포탑
        2. 가장 최근에 공격한 포탑
        3. 행과 열의 합이 가장 큰 포탑
        4. 열 값이 가장 큰 포탑

2. 공격자 공격
    가장 강한 포탑 : 위 기준의 반대
    공격 대상은 공격자 공격력만큼 피해를 입고, 스플래시 데미지는 공격력 // 2만큼 데미지를 입는다.

    1) 레이저 공격
        - 상하좌우
        - 부서진 포탑이 있는 위치는 지날 수 없다
        - 범위를 벗어나는 경우, 반대로 나온다
        - 최단경로로 공격한다. (우하좌상 순)
    2) 포탄 공격
        - 공격 대상에 포탄을 던진다.
        - 8개의 방향에 있는 포탑도 피해를 입는다.

3. 포탑 부서짐
    - 공격력 0 이하 포탑은 부서진다.

4. 포탑 정비
    - 공격과 무관한 포탑의 공격력이 1씩 증가 ( 공격자도 아니고, 공격당하지도 않은)

풀이:
공격자, 목표 선정 : 정렬 후 deque() ->
레이저공격 : bfs
포탑 grid 존재해야함 : 만약 이전 공격에서 파괴되었다면
현재 포탑 순회하면서 파괴되었다면 next append x. 무관했다면 정비

'''

from collections import deque

dr = [0, 1, 0, -1, 1, 1, -1, -1]
dc = [1, 0, -1, 0, 1, -1, -1, 1]
turrets = []


def select_attacker():
    global turrets
    while turrets:
        a, _, r_c, c = turrets.popleft()
        if not a:
            continue
        return a, _, r_c - c, c

def select_target():
    global turrets
    return turrets.pop()


def laser(sr, sc):
    queue = deque([(sr, sc)])
    visited = [[0] * m for _ in range(n)]
    visited[sr][sc] = 1
    path = [[0] * m for _ in range(n)]
    arrive = False

    while queue:
        r, c = queue.popleft()
        for d in range(4):
            nr, nc = (r + dr[d]) % n, (c + dc[d]) % m
            if not visited[nr][nc] and grid[nr][nc]:
                path[nr][nc] = (r, c)
                if (nr, nc) == (er, ec):
                    arrive = True
                    break
                queue.append((nr, nc))
                visited[nr][nc] = 1
        if arrive:
            break
    if not arrive:
        return False, path
    else:
        new_path = set()
        r, c = er, ec
        while (r, c) != (sr, sc):
            new_path.add((r, c))
            r, c = path[r][c]
        return True, new_path


def bomb(r, c):
    path = set()
    path.add((r, c))
    visited = [[0] * m for _ in range(n)]
    for d in range(len(dr)):
        nr, nc = (r + dr[d]) % n, (c + dc[d]) % m
        if not visited[nr][nc] and grid[nr][nc] and (nr, nc) != (sr, sc):
            visited[nr][nc] = 1
            path.add((nr, nc))

    return path


n, m, k = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
for i in range(n):
    for j in range(m):
        if grid[i][j]:
            turrets.append((grid[i][j], 0, i + j, j))
            grid[i][j] = [grid[i][j], 0]

# 게임 시작
for _ in range(k):
    # 게임 종료 조건
    if len(turrets) == 1:
        break

    # 0. 공격자, 대상 선정을 위한 정렬
    turrets = deque(sorted(turrets, key=lambda x: (x[0], x[1], -x[2], -x[3])))

    # 1. 공격자 선정
    damage, _, sr, sc = select_attacker()
    damage += n + m

    # 2. 공격 대상 선정
    defence, target_time, er_ec, ec = select_target()
    er = er_ec - ec

    # 3. 레이저 공격 시도
    laser_avaliable, target_list = laser(sr, sc)

    # 4. 포탄 공격 시도
    if not laser_avaliable:
        target_list = bomb(er, ec)

    # 5. 포탑 데미지 입히기
    new_turrets = [(damage, 0, sr + sc, sc)]
    grid[sr][sc] = [damage, 0]
    for r, c in target_list:
        if (r, c) == (er, ec):
            grid[r][c][0] -= damage
        else:
            grid[r][c][0] -= damage // 2
        if grid[r][c][0] <= 0:
            grid[r][c] = 0
        else:
            grid[r][c][1] += 1
            new_turrets.append((grid[r][c][0], grid[r][c][1], r + c, c))

    # 6. 포탑 회복
    for a, time, r_c, c in turrets:
        r = r_c - c
        if (r, c) not in target_list:
            grid[r][c][0] = a + 1
            grid[r][c][1] += 1
            new_turrets.append((a + 1, time + 1, r_c, c))

    turrets = new_turrets[:]

turrets.sort(key=lambda x: x[0])
print(turrets[-1][0])