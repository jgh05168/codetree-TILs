'''
n x n, 상하좌우
빈칸 : 참가자가 이동 가능한 칸
벽 : 참가자가 이동할 수 없는 칸
    - 1 ~ 9 내구도를 갖고 있음
    - 회전할 떄 내구도가 1씩 깎인다
    - 내구도가 0이면 빈 칸으로 변경된다
출구 : 참가자가 탈출

1. 1초마다 모든 참가자는 한 칸씩 움직인다
    - 두 위치의 최단거리는 절댓값합으로 정의
    - 모든 참가자는 동시에 움직인다
    - 움직인 칸은 현재 머문 칸보다 출구에 더 가까워야 된다
    - 움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시한다
    - 안움직일수도 있다
    - 한 칸에 2명 이상이 있을 수도 잇다
2. 미로 회전
    - 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형 좌표를 잡는다.
    - 가장 작은 크기를 갖는 정사각형이 2개 이상이라면 r, c 순서
    - 시계방향으로 90도 회전, 내구도 1 감소

모든 참가자들의 이동거리 합고 출구 좌표 출력

풀이:
bfs, 시뮬
'''

from collections import deque, defaultdict
import sys
input = sys.stdin.readline

#    상  하  좌  우
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]


def move(people_loc):
    global m
    new_people_grid = [[[] * n for _ in range(n)] for _ in range(n)]
    new_people_grid[er][ec] = -1

    while people_loc:
        r, c = people_loc.popleft()
        num = people_grid[r][c].pop()
        # 현재 출구까지의 거리 계산
        cur_dist = abs(r - er) + abs(c - ec)

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            new_dist = abs(nr - er) + abs(nc - ec)
            if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc]:
                # 만약 도착점이라면 종료
                if (nr, nc) == (er, ec):
                    people_move[num] += 1
                    m -= 1
                    break
                # 현재 위치보다 새로운 곳이 거리가 더 멀면 continue
                if new_dist >= cur_dist:
                    continue
                # 이동가능하다면 이동하고 break
                else:
                    new_people_grid[nr][nc].append(num)
                    people_move[num] += 1
                    break
        # 만약 못움직이는 경우라면 이전 위치 그대로 더해주기
        else:
            new_people_grid[r][c].append(num)

    return new_people_grid


def get_square():
    for size in range(2, n):
        for i in range(0, n - size + 1):
            for j in range(0, n - size + 1):
                if check_rotate(i, j, size):
                    return i, j, size


def check_rotate(si, sj, n):
    p, e = 0, 0
    for i in range(si, si + n):
        for j in range(sj, sj + n):
            if people_grid[i][j] == -1:
                e = 1
            elif people_grid[i][j]:
                p = 1

    if p and e:
        return 1
    else:
        return 0


def rotate(si, sj, nn):
    global er, ec
    new_grid = [[0] * n for _ in range(n)]
    new_people_grid = [[[] * n for _ in range(n)] for _ in range(n)]

    chagne_exit = 0
    for i in range(si, si + nn):
        for j in range(sj, sj + nn):
            oi, oj = i - si, j - sj
            ni, nj = oj, nn - oi - 1
            new_people_grid[ni + si][nj + sj] = people_grid[i][j]
            # 벽이면 내구도 -1씩 진행
            if grid[i][j]:
                new_grid[ni + si][nj + sj] = grid[i][j] - 1
            else:
                new_grid[ni + si][nj + sj] = grid[i][j]
            # 출구 위치 업데이트
            if (i, j) == (er, ec) and not chagne_exit:
                chagne_exit = 1
                er, ec = ni + si, nj + sj


    for i in range(n):
        for j in range(n):
            if not si <= i < si + nn or not sj <= j < sj + nn:
                new_grid[i][j] = grid[i][j]
                new_people_grid[i][j] = people_grid[i][j]

    # 사람들 위치 새로 찾기
    new_queue = deque()
    for i in range(n):
        for j in range(n):
            if (i, j) == (er, ec):
                continue
            if new_people_grid[i][j]:
                for k in range(len(new_people_grid[i][j])):
                    new_queue.append((i, j))

    return new_grid, new_people_grid, new_queue


n, m, k = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
people_grid = [[[] * n for _ in range(n)] for _ in range(n)]
people_loc = deque()
people_move = defaultdict(int)
for i in range(1, m + 1):
    sr, sc = map(int, input().split())
    people_loc.append((sr - 1, sc - 1))
    people_grid[sr - 1][sc - 1].append(i)
er, ec = map(int, input().split())
er -= 1
ec -= 1
people_grid[er][ec] = -1

# 게임 시작
for _ in range(k):
    # 1. 모든 사람 이동
    people_grid = move(people_loc)

    # 1-1. 사람들 모두 탈출했는지 확인
    if not m:
        break

    # 2. 회전 반경 찾기
    si, sj, size = get_square()

    # 3. 회전하기
    grid, people_grid, people_loc = rotate(si, sj, size)

ans = 0
for val in people_move.values():
    ans += val
print(ans)
print(er + 1, ec + 1)