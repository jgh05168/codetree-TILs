'''
15:08

n x n의 미지의 공간에 갇혀버림 !
공간 :
한 변의 길이가 N인 2차원평면, 그 사이 어딘가에는 한 변의 길이가 M인 정육명체 형태의 벽이 존재함

[타임머신의 스캔 기능]
1. 미지의 공간의 평면도 : 위에서 내려다본 전체 맵
2. 시간의 벽의 단면도 : 시간의 벽의 윗면과, 동서남북 네 면의 단면도
- 평면도와 단면도는 빈공간과 장애물로 구성
- 빈공간만 이동가능. 장애물은 이동 불가능

처음 위치 : 시간의 벽의 윗면 어딘가에 위치함. (2로 표시됨)
미지 공간 평면도에서는 시간의 벽은 3으로 표현된다.
탈출구 : 4로 표현된다.
시간의벽의 바닥은 모두 2로 표시되지만, 단 한 칸만 빈공간으로 뚫려있기 떄문에 출구는 하나이다.

[미지의 공간 바닥은 총 F개의 시간 이상 현상이 존재함.]
- 각 시간 이상 현상은 바닥의 빈 공간(r, c)에서 시작하며,
- 매 v의 배수 턴마다 방향 d로 한 칸씩 확산된다.
- 확산 이후에도 기존 이상 현상은 사라지지 않는다.
= 빈 공간으로만 확산되며, 더이상 확산할 수 없으면 멈춘다.
= 동시에 확산하며, 방향은 동서남북

타임머신은 매 턴 상하좌우로 한 칸씩 이동.
출구까지 이동하는 최소시간 출력
탈출 불가능하면 -1 출력

풀이:
순서
1. 시간 이상 현상 확산
2. 타임머신 이동

bfs를 기본으로 사용한다.

설계 :
시간의벽 : 0, 1, 2, 3, 4 인덱스를 각각 동 서 남 북 윗면 으로 설정
    => N x N x 5의 3차원 배열
grid : N x N의 2차원 배열
시간 이상 현상 : 1차원 배열에 정보 저장
    => 시간 확산을 일으키며 새로운 위치는 업데이트
    => 못움직이는 확산은 0으로 처리

'''

from collections import deque, defaultdict

#    동  서  남  북
dr = [0, 0, 1, -1]
dc = [1, -1, 0, 0]

grid = []
symptom_list = []
# 이동할 수 잇는 벽 연결짓기
link_wall = [
    [0, 0, 0, 0],
    [4, 3, 0, 5],
    [3, 4, 0, 5],
    [1, 2, 0, 5],
    [2, 1, 0, 5],
    [1, 2, 3, 4]
]
# 바닥과 연결되는 부분 찾기
wall_bottom = []
escape_loc = (0, 0)


def move_symptom(t, n):
    new_grid = [row[:] for row in grid[0]]
    for s in range(len(symptom_list)):
        if not symptom_list[s]:
            continue
        r, c, d, v = symptom_list[s]
        if not t % v:
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not grid[0][nr][nc]:
                new_grid[nr][nc] = 1
                symptom_list[s] = (nr, nc, d, v)
            else:
                symptom_list[s] = 0
    return new_grid


def check_new_loc(cur_dim, r, c, m):
    # 동쪽
    if cur_dim == 1:
        return m - c - 1, r
    # 서쪽
    elif cur_dim == 2:
        return c, 0
    # 남쪽
    elif cur_dim == 3:
        return r, c
    # 북쪽
    else:
         return 0, m - c - 1


def check_up_loc(way, cur_dim, r, c, m):
    if not way:
        if cur_dim == 1:
            return m - c - 1, 2
        elif cur_dim == 2:
            return c, 0
        elif cur_dim == 3:
            return 2, c
        else:
            return 0, m - c - 1
    # 이 때는 위에서 cur_dim으로 가는거임
    else:
        if cur_dim == 1:
            return 0, m - r - 1
        elif cur_dim == 2:
            return 0, r
        elif cur_dim == 3:
            return 0, c
        else:
            return 0, m - c - 1


def move_timemachine(queue, n, m):
    new_queue = deque()
    while queue:
        r, c, dim = queue.popleft()
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            # 현재 dim에서 범위를 벗어나는지를 체크해야 한다.
            if not dim:
                if 0 <= nr < n and 0 <= nc < n:
                    # 범위 안이지만, 장애물 있으면 continue해주기
                    if grid[dim][nr][nc] == 1:
                        continue
                    if (nr, nc) == escape_loc:
                        return True, []
                    new_queue.append((nr, nc, dim))
                    grid[dim][nr][nc] = 1
                # 맨 아래 녀석이 범위를 벗어나는 경우 다른 곳으로 갈 수 없기 때문에 continue
                continue
            else:
                if 0 <= nr < m and 0 <= nc < m:
                    if grid[dim][nr][nc] == 1:
                        continue
                    new_queue.append((nr, nc, dim))
                    grid[dim][nr][nc] = 1
                    continue
            # 범위를 벗어난다면, 다시 체크해보기
            new_dim = link_wall[dim][d]
            # 바닥에 내려왔으면,
            if not new_dim:
                r, c = check_new_loc(dim, r, c, m)
                nr, nc = wall_bottom[r][c]
                for nd in range(len(dr)):
                    nnr, nnc = nr + dr[nd], nc + dc[nd]
                    if 0 <= nnr < n and 0 <= nnc < n:
                        # 범위 안이지만, 장애물 있으면 continue해주기
                        if grid[new_dim][nnr][nnc] in [1, 3]:
                            continue
                        if (nnr, nnc) == escape_loc:
                            return True, []
                        new_queue.append((nnr, nnc, new_dim))
                        grid[new_dim][nnr][nnc] = 1
            else:
                # 북쪽만 예외 처리
                # 다른 4방면 -> 북쪽
                if new_dim == 5:
                    nr, nc = check_up_loc(0, dim, r, c, m)
                elif dim == 5:
                    nr, nc = check_up_loc(1, new_dim, r, c, m)
                else:
                    nr, nc = (r + dr[d]) % m, (c + dc[d]) % m
                if 0 <= nr < m and 0 <= nc < m:
                    if grid[new_dim][nr][nc] == 1:
                        continue
                    new_queue.append((nr, nc, new_dim))
                    grid[new_dim][nr][nc] = 1

    return False, new_queue


def main():
    global grid, symptom_list, link_loc, escape_loc, wall_bottom

    timemachine = deque()
    n, m, f = map(int, input().split())
    grid.append([list(map(int, input().split())) for _ in range(n)])
    # 시간의벽 입력
    sr, sc, sdim = -1, -1, -1
    for dim in range(1, 6):
        tmp_timewall = [list(map(int, input().split())) for _ in range(m)]
        grid.append(tmp_timewall)
        # 타임머신 초기 위치 찾기
        if not timemachine:
            flag = 0;
            for i in range(m):
                for j in range(m):
                    if tmp_timewall[i][j] == 2:
                        timemachine.append((i, j, dim))
                        grid[dim][i][j] = 1     # 초기 방문처리
                        flag = 1
                        break
                if flag:
                    break
    # 이상 현상 입력
    for _ in range(f):
        r, c, d, v = map(int, input().split())
        grid[0][r][c] = 1
        symptom_list.append((r, c, d, v))
    # 벽과 공간 링킹해주기
    wall_bottom = [[0] * m for _ in range(m)]
    flag = 0
    for i in range(n):
        for j in range(n):
            if not flag and grid[0][i][j] == 3:
                for r in range(i, i + m):
                    for c in range(j, j + m):
                        wall_bottom[r - i][c - j] = (r, c)
                flag = 1
            elif grid[0][i][j] == 4:
                escape_loc = (i, j)


    # 이동 시작
    time = 1
    while True:
        # 1. 시간 이상 현상 동작
        grid[0] = [row[:] for row in move_symptom(time, n)]

        # 2. 타임머신 탈출
        isEscape, timemachine = move_timemachine(timemachine, n, m)

        if isEscape or not timemachine:
            break
        time += 1

    if isEscape:
        print(time)
    else:
        print(-1)



if __name__ == "__main__":
    main()