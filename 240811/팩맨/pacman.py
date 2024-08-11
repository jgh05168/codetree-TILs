'''
4 x 4, 몬스터는 8방향 이동 가능

1. 몬스터 복제 시도 : 현재 위치 에서 자신과 같은 방향을 가진 몬스터를 복제
    - 복제된 몬스터는 이동 불가
2. 몬스터 이동 : 현재 자신이 가진 방향대로 한 칸 이동
    - 몬스터 시체가 있거나, 팩맨이 있거나, 격자를 벗어나는 경우
        - 이동이 가능할 때 까지 반시계 방향으로 45도 회전
        - 8방향 다 돌았는데도 못움직이면, 움직이지 않는다.
3. 팩맨 이동 : 상하좌우 합쳐서 3칸 이동한다. ( dfs)
    - 몬스터를 가장 많이 먹을 수 있는 방향으로 이동한다.
    - 상좌하우 의 우선순위를 갖는다.
        - 우선순위 맞게 dfs 돌리기
    - 알을 먹지 않으며, 움직이기 전에 함꼐 있던 몬스터도 먹지 않는다.
4. 몬스터 시체
    - 2턴동안 유지.
5. 몬스터 복제 완성 : 알 형태였던 몬스터가 부화한다.

풀이 :
만들어야 할 1차원 배열 : 몬스터, 몬스터 알,
2차원 배열 : 팩맨, 몬스터 시체
순서 :
몬스터 알 낳기 ( 배열에 저장 ) -> 몬스터 이동 push and pop, 그리드에 위치 업데이트 -> 팩맨 이동 ( dfs )
    -> 몬스터 시체  처리 -> 알 복제 완성 ( 그리드에 업데이트 )

어차피 grid 4 x 4니까, grid 안에서 처리하는 것도 방법임
'''

from collections import deque
import sys
input = sys.stdin.readline

mon_dr = [-1, -1, 0, 1, 1, 1, 0, -1]
mon_dc = [0, -1, -1, -1, 0, 1, 1, 1]
pack_dr = [-1, 0, 1, 0]
pack_dc = [0, -1, 0, 1]


def lay_eggs():
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                for d in grid[i][j]:
                    monster_eggs[i][j].append(d)


def mon_move():
    new_grid = [[deque() * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                while grid[i][j]:
                    d = grid[i][j].popleft()
                    for _ in range(8):
                        ni, nj = i + mon_dr[d], j + mon_dc[d]
                        # 몬스터 시체가 있거나, 팩맨이 있거나, 격자를 벗어나는 경우 : 방향 틀기
                        if 0 <= ni < n and 0 <= nj < n and (ni, nj) != (pack_r, pack_c) and not dead_monster[ni][nj]:
                            new_grid[ni][nj].append(d)
                            break
                        else:
                            d = (d + 1) % 8
                    # 갈 곳이 없는 경우, 가만히 있기
                    else:
                        new_grid[i][j].append(d)

    return new_grid


def pack_move(move_cnt, get_mon, r, c, mon_locs):
    global eaten_mon_cnt, eaten_mon_list, pack_r, pack_c
    if move_cnt == 3:
        if eaten_mon_cnt < get_mon:
            eaten_mon_cnt = get_mon
            eaten_mon_list = mon_locs
            pack_r, pack_c = eaten_mon_list[-1]
    else:
        for d in range(4):
            nr, nc = r + pack_dr[d], c + pack_dc[d]
            # 격자 밖으로만 안나가게 설정
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                visited[nr][nc] = 1
                pack_move(move_cnt + 1, get_mon + len(grid[nr][nc]), nr, nc, mon_locs + [(nr, nc)])
                visited[nr][nc] = 0

def goodbye_mon():
    for i in range(n):
        for j in range(n):
            if dead_monster[i][j] > 0:
                dead_monster[i][j] -= 1
    for r, c in eaten_mon_list:
        if grid[r][c]:
            dead_monster[r][c] = 2
            grid[r][c] = deque()


def baby_mon():
    for i in range(n):
        for j in range(n):
            if monster_eggs[i][j]:
                while monster_eggs[i][j]:
                    grid[i][j].append(monster_eggs[i][j].popleft())


n = 4
m, t = map(int, input().split())
pack_r, pack_c = map(int, input().split())
pack_r -= 1
pack_c -= 1
grid = [[deque() * n for _ in range(n)] for _ in range(n)]              # 팩맨 : -1 | 몬스터 : 1
monster_eggs = [[deque() * n for _ in range(n)] for _ in range(n)]
dead_monster = [[0] * n for _ in range(n)]
for mon_num in range(1, m + 1):
    sr, sc, sd = map(int, input().split())
    grid[sr - 1][sc - 1].append(sd - 1)


for _ in range(t):
    # 1. 몬스터 알 낳기
    lay_eggs()

    # 2. 몬스터 이동
    grid = mon_move()

    # 3. 팩맨 출발
    eaten_mon_cnt = 0
    eaten_mon_list = []
    visited = [[0] * n for _ in range(n)]
    visited[pack_r][pack_c] = 1
    pack_move(0, 0, pack_r, pack_c, [])

    # 4. 몬스터 시체 처리
    goodbye_mon()

    # 5. 알 태어나기
    baby_mon()


# 살아남은 몬스터 수 cnt
ans = 0
for i in range(n):
    for j in range(n):
        ans += len(grid[i][j])
print(ans)