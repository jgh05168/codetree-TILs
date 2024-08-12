'''
n x n
질량, 방향, 속력, 초기 위치
방향 : 8
격자 밖으로 벗어나면 반대편으로 간다.

1. 모든 원자는 1초가 지날 때마다 자신의 방향으로 속력만큼 이동한다.
2. 이동이 모두 끝난 뒤에 하나의 칸에 2개 이상의 원자가 있으면 합쳐진다.
    - 각각의 질량과 속력을 모두 합한다.
    - 합쳐진 원자는 4개로 나눠진다.
        - 나눠진 원자는 모두 해당 칸에 위치한다.
        - 질량 : 합쳐진 원자의 질량 // 5
        - 속력 : 합쳐진 원자의 속력 // 합쳐진 원자의 개수
        - 방향 : 모두 상하좌우 or  모두 대각선인 경우 -> 상하좌우 모두 갖는다.
                아니라면, -> 대각선 네 방향의 값을 갖는다.
    - 질량이 0인 원소는 소멸
3. 이동 과정 중 원자가 만나는 경우는 무시한다.
'''

from collections import deque
import sys
input = sys.stdin.readline

#     ↑   ↗   →  ↘  ↓  ↙  ←  ↖
dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, 1, 1, 1, 0, -1, -1, -1]


def move_atoms():
    new_grid = [[deque() * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                while grid[i][j]:
                    r, c, m, s, d = grid[i][j].popleft()
                    nr, nc = (r + dr[d] * s) % n, (c + dc[d] * s) % n
                    new_grid[nr][nc].append((nr, nc, m, s, d))
    return new_grid


def separate_atoms():
    new_grid = [[deque() * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                # 원자 질량, 개수, 스피드, 방향 확인
                atom_cnt = len(grid[i][j])
                total_m, total_speed = 0, 0
                get_dir = [0, 0]
                for k in range(atom_cnt):
                    r, c, m, s, d = grid[i][j][k]
                    total_m += m
                    total_speed += s
                    get_dir[d % 2] = 1
                new_m = total_m // 5
                # 질량이 0인 경우, 소멸
                if not new_m:
                    continue
                if sum(get_dir) == 2:
                    for nd in range(4):
                        new_grid[i][j].append((r, c, new_m, total_speed // atom_cnt, 2 * nd + 1))
                else:
                    for nd in range(4):
                        new_grid[i][j].append((r, c, new_m, total_speed // atom_cnt, 2 * nd))

    return new_grid

n, m, k = map(int, input().split())
grid = [[deque() * n for _ in range(n)] for _ in range(n)]
atom_list = []
for _ in range(m):
    sx, sy, sm, ss, sd = map(int, input().split())
    grid[sx - 1][sy - 1].append((sx - 1, sy - 1, sm, ss, sd))

for _ in range(k):
    # 1. 원자 이동
    grid = move_atoms()

    # 2. 원자 분열
    grid = separate_atoms()

ans = 0
for i in range(n):
    for j in range(n):
        ans += len(grid[i][j])

print(ans)