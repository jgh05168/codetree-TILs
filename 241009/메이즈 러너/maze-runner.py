'''
10:55

n x n, 빈칸(이동가능), 벽(이동불가, 내구도 존재, 회전할때 1씩 깎임, 0이되면 빈칸으로 변경), 출구(즉시탈출)
[이동]
- 모든 참가자 동시 이동
- 상하좌우, 벽이 없는 곳으로 이동
- 움직인 칸은 현재 칸보다 출구까지의 최단거리가 가까워야 함
- 움직일 수 없는 상황이라면 이동 불가
- 한 칸에 2명 이상의 참가자가 있을 수 있음

[회전]
- 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 잡는다
- 가장 작은 크기를 갖는 정사각형이 2개 이상이라면, r, c 작은 순으로 우선
- 90도 회전하고, 내구도가 깎인다.

k초 전에 모든 참가자가 탈출하면 게임 종료
모든 참가자들의 이동거리 합과 출구 좌표를 출력하라

풀이:
벽 상관없이 최단거리로만 계산된다 : bfs 필요없이 네 방향만 체크해도 된다.
참가자 grid 갖기
'''

from collections import deque, defaultdict

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

visited = []

def get_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def find_stuff(r, c, n):
    person_valid = 0
    exit = 0
    for i in range(r, r + n):
        for j in range(c, c + n):
            if grid[i][j]:
                person_valid = 1
            if (i, j) == (er, ec):
                exit = 1

    if person_valid and exit:
        return True
    return False


def people_move():
    global total_move
    for p in range(1, m + 1):
        # 이미 빠져나간 경우 예외처리
        if not person_loc[p]:
            continue
        r, c = person_loc[p]
        grid[r][c].popleft()
        cur_distance = get_distance(r, c, er, ec)
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not wall[nr][nc]:
                new_distance = get_distance(nr, nc, er, ec)
                if new_distance < cur_distance:
                    total_move += 1
                    # 출구 나갔는지 체크
                    if (nr, nc) == (er, ec):
                        person_loc[p] = 0
                    else:
                        grid[nr][nc].append(p)
                        person_loc[p] = (nr, nc)

                    break
        else:
            grid[r][c].append(p)


def rotate(si, sj, n):
    global er, ec
    new_wall = [[0] * n for _ in range(n)]
    new_person = [[0] * n for _ in range(n)]
    ner, nec = er, ec
    for i in range(si, si + n):
        for j in range(sj, sj + n):
            oi, oj = i - si, j - sj
            ni, nj = oj, n - 1 - oi
            new_wall[ni][nj] = wall[i][j]
            new_person[ni][nj] = grid[i][j]
            # 출구
            if (i, j) == (er, ec):
                ner, nec = ni + si, nj + sj

    # 내구도 깎기
    for i in range(si, si + n):
        for j in range(sj, sj + n):
            wall[i][j] = new_wall[i - si][j - sj]
            grid[i][j] = new_person[i - si][j - sj]
            if wall[i][j]:
                wall[i][j] -= 1
            if grid[i][j]:
                for p in grid[i][j]:
                    person_loc[p] = (i, j)
    er, ec = ner, nec


def maze_rotate():
    for size in range(2, n):
        for i in range(0, n - size + 1):
            for j in range(0, n - size + 1):
                if find_stuff(i, j, size):
                    rotate(i, j, size)
                    return


n, m, k = map(int, input().split())
wall = [list(map(int, input().split())) for _ in range(n)]
grid = [[deque() * n for _ in range(n)] for _ in range(n)]
person_loc = [0]
total_move = 0
for i in range(1, m + 1):
    sr, sc = map(int, input().split())
    grid[sr - 1][sc - 1].append(i)
    person_loc.append((sr - 1, sc - 1))
er, ec = map(int, input().split())
er -= 1
ec -= 1

for _ in range(k):
    # 1. 참가자 이동
    people_move()

    # 1-2. 출구로 다 빠져나갔는지 확인
    if person_loc.count(0) == m + 1:
        break

    # 2. 미로 회전
    maze_rotate()

print(total_move)
print(er + 1, ec + 1)