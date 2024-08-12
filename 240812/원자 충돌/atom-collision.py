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
    for i in range(len(atom_list)):
        r, c, m, s, d = atom_list[i]
        nr, nc = (r + dr[d] * s) % n, (c + dc[d] * s) % n
        if not grid[nr][nc]:
            tmp_dir = [0, 0]
            tmp_dir[d % 2] = 1
            grid[nr][nc] = [m, s, 1, tmp_dir]   # 질량, 속도, 원소 갯수, 방향
        else:
            grid[nr][nc][0] += m
            grid[nr][nc][1] += s
            grid[nr][nc][2] += 1
            grid[nr][nc][3][d % 2] = 1



def separate_atoms():
    new_list = []
    for r in range(n):
        for c in range(n):
            if grid[r][c]:
                m, s, atom_cnt, tmp_dir = grid[r][c]
                new_m = m // 5
                new_s = s // atom_cnt
                if not new_m:
                    continue
                if sum(tmp_dir) == 2:
                    for nd in range(4):
                        new_list.append((r, c, new_m, new_s, 2 * nd + 1))
                else:
                    for nd in range(4):
                        new_list.append((r, c, new_m, new_s, 2 * nd))

    return new_list

n, m, k = map(int, input().split())
atom_list = []
for _ in range(m):
    sx, sy, sm, ss, sd = map(int, input().split())
    atom_list.append((sx - 1, sy - 1, sm, ss, sd))

for _ in range(k):
    grid = [[0] * n for _ in range(n)]

    # 1. 원자 이동
    move_atoms()

    # 2. 원자 분열
    atom_list = separate_atoms()

print(len(atom_list))