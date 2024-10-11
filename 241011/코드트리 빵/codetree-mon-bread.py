'''
14:36

1 ~ m번 사람은 각자의 번호에 맞는 시간에 출발하여 이동한다.
사람들이 목표로 하는 편의점은 모두 다르다
n x n

1. 격자에 있는 사람들 모두 본인이 가고싶은 편의점을 향해 한 칸 이동
    - 최단거리로 이동
    - 상좌우하 우선순위
2. 편의점에 도착한다면, 편의점에서 멈추고 해당 편의점을 지날 수 없다
    - 격자의 모든 사람들이 이동한 뒤 해당 편의점 문 닫는다.
3. 아직 격자 밖에 있는 사람이 있다면, 해당 사람이 베이스캠프로 이동한다
    - 베이스캠프는 1과 같이 최단거리에 위치하는 곳이다.
    - 최단거리가 여러개라면, 행, 열 작은 순으로 들어간다
    - 들어가는데 시간소요 x
    - 이 시점 이후 다른 사람들은 해당 베이스캠프를 이용할 수 없음

편의점에 모두 도착하는데 걸리는 시간 구하기

풀이:
bfs 재사용
베이스캠프는 점거한 뒤 닫아주어야 한다.
    - 베이스캠프 : 현재 인원 출발지
사용 전역변수 : 사람들 위치, 사람들 도착 위치

'''

from collections import deque

dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]

people_loc = []
cvs_loc = []


def bfs(sr, sc, cvs, p):
    global people_loc
    visited = [[0] * n for _ in range(n)]
    if cvs:
        queue = deque([cvs])
        visited[cvs[0]][cvs[1]] = 1
    else:
        queue = deque([(sr, sc)])
        visited[sr][sc] = 1
    min_dist = n * n
    basecamp_list = []

    while queue:
        r, c = queue.popleft()
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                # 최단경로 찾기
                if cvs:
                    if (nr, nc) == (sr, sc):
                        people_loc[p] = (r, c)
                        return
                # 베이스캠프 찾기
                else:
                    if not grid[nr][nc] and basecamp[nr][nc]:
                        if visited[r][c] + 1 < min_dist:
                            min_dist = visited[r][c] + 1
                            basecamp_list = [(nr, nc)]
                        elif visited[r][c] + 1 == min_dist:
                            basecamp_list.append((nr, nc))
                        continue
                if not grid[nr][nc]:
                    queue.append((nr, nc))
                    visited[nr][nc] = visited[r][c] + 1

    if not cvs:
        basecamp_list.sort()
        people_loc.append(basecamp_list[0])


def move_people():
    for p in range(min(len(people_loc), m)):
        if not people_loc[p]:
            continue
        # 편의점과 최단거리 찾기
        r, c = people_loc[p]
        bfs(r, c, cvs_loc[p], p)


def check_cvs():
    for p in range(min(len(people_loc), m)):
        if not people_loc[p]:
            continue
        r, c = people_loc[p]
        if (r, c) == cvs_loc[p]:
            grid[r][c] = 1
            people_loc[p] = 0


def find_basecamp(p):
    r, c = cvs_loc[p]
    bfs(r, c, 0, p)


n, m = map(int, input().split())
basecamp = [list(map(int, input().split())) for _ in range(n)]
grid = [[0] * n for _ in range(n)]
for _ in range(m):
    r, c = map(int, input().split())
    cvs_loc.append((r - 1, c - 1))

time = 0
while True:
    # 1. 사람들 이동
    move_people()

    # 2. 편의점에 도착한 경우 이동불가능 표시 해주기
    check_cvs()

    # 3. 베이스캠프에 들어가기
    if time < m:
        find_basecamp(time)
        grid[people_loc[time][0]][people_loc[time][1]] = 1

    # 시간 업데이트
    time += 1
    if people_loc.count(0) == m:
        break

print(time)