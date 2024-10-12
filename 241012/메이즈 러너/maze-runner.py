'''
20:42

n x n
벽 : 참가자가 이동 불가능한 칸
    - 1 ~ 9 내구도
    - 회전할때마다 내구도 깎음
    - 내구도 0이면 빈칸으로 변함

[참가자 이동]
최단거리 : 절댓값 합으로 결정
- 모든 참가자는 동시에 움직임
- 상하좌우, 벽이 없는 곳으로
- 움직인 칸은 출구까지의 최단거리가 가까워야 한다.
- 움직일 수 있는 칸이 2개 이상이라면 상하움직임 우선시
- 움직일 수 없다면 가만히있기
- 한 칸에 2명 이상의 참가자 존재 가능

[미로 회전]
- 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형
- 같은 크기라면 r, c 작은 순
- 선택된 정사각형은 시계방향 90도 회전
- 회전된 벽은 내구도 1씩 깎임

모든 참가자들의 이동거리합과 출구좌표 출력
n < 10
참가자 < 10 : 큐에 넣을 수 있음

필요한 메모리
참가자들 이동거리 배열
참가자 grid
'''

from collections import deque

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

maze = []
participants = []
ans = 0


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def bfs(sr, sc, er, ec, cur_dist):
    queue = deque([(sr, sc)])
    visited = [[-1] * n for _ in range(n)]
    visited[sr][sc] = 0

    while queue:
        r, c = queue.popleft()
        for d in range(len(dr) - 1, -1, -1):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and visited[nr][nc] == -1 and (type(maze[nr][nc]) == list or not maze[nr][nc]):
                if (nr, nc) == (er, ec):
                    return True, (r, c)
                if visited[r][c] + 1 >= cur_dist:
                    continue
                queue.append((nr, nc))
                visited[nr][nc] = visited[r][c] + 1

    return False, (-1, -1)


def participant_move():
    global ans, participants
    new_maze = [row[:] for row in maze]
    for p in range(m):
        if not participants[p]:
            continue
        # 최단경로찾기
        r, c = participants[p]
        cur_dist = distance(r, c, exit[0], exit[1])
        # 현재 위치에서 최단경로 찾기
        check_move, new_loc = bfs(exit[0], exit[1], r, c, cur_dist)
        if check_move:
            ans += 1
            new_maze[r][c] = 0
            if new_loc == exit:
                participants[p] = 0
                new_maze[new_loc[0]][new_loc[1]] = 0
            else:
                participants[p] = new_loc
                if not new_maze[new_loc[0]][new_loc[1]]:
                    new_maze[new_loc[0]][new_loc[1]] = [p]
                else:
                    new_maze[new_loc[0]][new_loc[1]].append(p)



    return new_maze


def check_possible(i, j, n):
    find_exit, find_participant = 0, 0
    for r in range(i, i + n):
        for c in range(j, j + n):
            if exit == (r, c):
                find_exit = 1
            elif type(maze[r][c]) == list:
                find_participant = 1

    if find_exit and find_participant:
        return True
    return False


def rotate(si, sj, n):
    global maze, participants, exit
    new_maze = [row[:] for row in maze]
    for i in range(si, si + n):
        for j in range(sj, sj + n):
            oi, oj = i - si, j - sj
            ni, nj = oj, n - 1 - oi
            new_maze[ni + si][nj + sj] = maze[i][j]
            if type(new_maze[ni + si][nj + sj]) == int and new_maze[ni + si][nj + sj]:
                new_maze[ni + si][nj + sj] -= 1
            elif type(new_maze[ni + si][nj + sj]) == list:
                for p in new_maze[ni + si][nj + sj]:
                    participants[p] = (ni + si, nj + sj)
            elif (i, j) == exit:
                exit = (ni + si, nj + sj)

    return new_maze



def maze_move():
    for nn in range(2, n):
        for i in range(0, n - nn):
            for j in range(n - nn):
                # 정사각형 안에 출구와 참가자 존재하는지 확인
                if check_possible(i, j, nn):
                    return rotate(i, j, nn)



n, m, k = map(int, input().split())
maze = [list(map(int, input().split())) for _ in range(n)]
for p in range(m):
    r, c = map(int, input().split())
    if not maze[r - 1][c - 1]:
        maze[r - 1][c - 1] = [p]
    else:
        maze[r - 1][c - 1].append(p)
    participants.append((r - 1, c - 1))
er, ec = map(int, input().split())
exit = (er - 1, ec - 1)

# 게임시작
for _ in range(k):
    # 1. 참가자 이동
    maze = participant_move()

    # 2. 미로 이동
    maze = maze_move()

    # 3. 게임종료
    if participants.count(0) == m:
        break

print(ans)
print(exit[0] + 1, exit[1] + 1)