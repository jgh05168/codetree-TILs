'''
14:58

1 ~ m명의 사람, 사람들은 정확히 tm에 출발하여 편의점으로 이동한다
- 사람들은 출발시간 전에 격자 밖에 위치함
- 목표 편의점은 모두 다름

[이동 순서]
1. 본인이 가고 싶은 편의점 방향을 향해 1 칸 움직인다.
    - 최단거리 (상 좌 우 하 )
2. 편의점에 도착 시, 해당 편의점에 멈추게 되고, 다른 사람들은 해당 편의점이 있는 칸을 지날 수 없다
    - 격자에 있는 사람들이 모두 이동한 뒤에 해당 편의점 칸을 지날 수 없게 된다.
3. 현재 t분이고, t <= m을 만족한다면, t번 사람은 자신이 가고싶은 편의점과 가장 가까운 베이스캠프에 들어간다
    - 베이스캠프 : 최단거리에 위치하는 것
    - 여러가지인 경우, 행이 작은, 열이 작은 순으로 선택한다
    - t번 사람이 베이스캠프로 이동하는데 시간이 전혀 소요되지 않는다.
    - 이때부터 해당 베이스캠프를 지날 수 없다.
        - 격자의 모든 사람들이 이동한 뒤에 해당 칸을 지날 수 없음에 유의

총 몇 분 뒤에 모든 사람이 편의점에 도착하는지 구하여라.

풀이:
베이스캠프는 현재 이동하고자 하는 녀석이 시작할 떄, 해당 편의점에서 시작하여 찾는다.

'''

from collections import deque, defaultdict

dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]

store_loc = defaultdict(tuple)
people = [0]
bef_people = []
arrived_person = 0
time = 0
basecamp_set = set()


def move_bfs(sr, sc, er, ec):
    if (sr, sc) == (er, ec):
        return 0
    queue = deque()
    queue.append((sr, sc))
    visited = [[-1] * n for _ in range(n)]
    visited[sr][sc] = 0

    while queue:
        r, c = queue.popleft()
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and visited[nr][nc] == -1 and grid[nr][nc] != -1:
                if (nr, nc) == (er, ec):
                    return visited[r][c] + 1
                queue.append((nr, nc))
                visited[nr][nc] = visited[r][c] + 1

    return -1

def move_person():
    global arrived_person
    arrive_person_list = []
    for p in range(1, min(time, m) + 1):
        # 이미 도착한 경우, continue
        if not people[p]:
            continue
        pr, pc = people[p]
        new_r, new_c = pr, pc
        sr, sc = store_loc[p]
        dest = n * n
        for d in range(len(dr)):
            nr, nc = pr + dr[d], pc + dc[d]
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != -1:
                tmp_dest = move_bfs(nr, nc, sr, sc)
                if tmp_dest != -1 and dest > tmp_dest:
                    dest = tmp_dest
                    new_r, new_c = nr, nc
        # 2. 목적지에 도착한 경우, 해당 편의점 이동불가로 설정하기 위해 도착한 애들 넘겨주기
        if not dest:
            arrive_person_list.append(p)
        else:
            people[p] = (new_r, new_c)

    return arrive_person_list

def find_basecamp(store, person):
    sr, sc = store
    queue = deque()
    queue.append((sr, sc))
    visited = [[0] * n for _ in range(n)]
    visited[sr][sc] = 1

    while queue:
        r, c = queue.popleft()

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and (nr, nc) not in basecamp_set and grid[nr][nc] != -1:
                if basecamp[nr][nc]:
                    people.append((nr, nc))
                    basecamp_set.add((nr, nc))
                    grid[nr][nc] = -1
                    return
                else:
                    queue.append((nr, nc))
                    visited[nr][nc] = 1


n, m = map(int, input().split())
basecamp = [list(map(int, input().split())) for _ in range(n)]
grid = [[0] * n for _ in range(n)]
for i in range(1, m + 1):
    sr, sc = map(int, input().split())
    store_loc[i] = ((sr - 1, sc - 1))
    grid[sr - 1][sc - 1] = i        # 편의점 번호


while True:
    # 1. 격자에 있는 모든 사람들 이동하기
    arrive_person_list = move_person()

    # 2. 편의점에 도착한 경우, 격자 못움직이게 설정해주기
    if arrive_person_list:
        for p in arrive_person_list:
            sr, sc = store_loc[p]
            grid[sr][sc] = -1
            arrived_person += 1
            people[p] = 0

    time += 1

    # 3. 조건을 만족한다면, 새로운 베이스캠프 지정해주기
    if time <= m:
        find_basecamp(store_loc[time], time)

    if arrived_person == m:
        break

print(time)