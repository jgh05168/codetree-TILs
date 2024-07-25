'''
배터리가 소진되는 경우 멈춘다.
최단거리로 이동, 한 칸 이동에 배터리 1 소모
목적지 도착 시 승객을 태워 이동하며 소모한 배터리의 2배만큼 충전한다.
    도착과 동시에 배터리가 0이 되어도 유효하다
승객이 여러 명일 경우, 최단 거리에 있는 손님을 태운다.
    여러 명인 경우, (r, c) 순서로 태움

풀이:
bfs + 완탐
1. bfs로 최단거리에 있는 승객을 찾는다.
2. 손님까지 이동한다.
3. 손님의 목적지까지 이동한다.
4. 1 ~ 3 반복
'''

from collections import deque
import sys, heapq
input = sys.stdin.readline

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def find_passenger(sr, sc):
    global battery
    # 도착지에 또다른 승객이 서있는 경우
    if grid[sr][sc] > 0 and passenger_arrivals[grid[sr][sc]]:
        return True, sr, sc

    queue = deque()
    visited = [[-1] * n for _ in range(n)]
    visited[sr][sc] = 0
    queue.append((sr, sc))
    passenger_list = []

    while True:
        new_queue = deque()
        while queue:
            r, c = queue.popleft()

            for d in range(len(dr)):
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < n and 0 <= nc < n and visited[nr][nc] == -1 and grid[nr][nc] != -1:
                    visited[nr][nc] = visited[r][c] + 1
                    new_queue.append((nr, nc))
                    # 만약 승객이라면 passenger_list에 저장
                    if grid[nr][nc] > 0 and passenger_arrivals[grid[nr][nc]]:
                        heapq.heappush(passenger_list, (nr, nc))
        if passenger_list:
            tmp_r, tmp_c = heapq.heappop(passenger_list)
            battery -= visited[tmp_r][tmp_c]
            break
        else:
            queue = new_queue

    if battery > 0:
        return True, tmp_r, tmp_c
    else:
        return False, -1, -1


def move_passenger(sr, sc, passenger):
    global battery
    queue = deque()
    visited = [[-1] * n for _ in range(n)]
    visited[sr][sc] = 0
    queue.append((sr, sc))

    while queue:
        r, c = queue.popleft()

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and visited[nr][nc] == -1 and grid[nr][nc] != -1:
                # 만약 승객의 목적지에 도착했다면 ?
                if (nr, nc) == passenger_arrivals[passenger]:
                    # 먼저 도착까지 배터리 소모량이 가능한가 체크
                    battery -= (visited[r][c] + 1)
                    if battery < 0:
                        return False, -1, -1
                    else:
                        battery += (visited[r][c] + 1) * 2
                        passenger_arrivals[passenger] = 0
                        return True, nr, nc
                visited[nr][nc] = visited[r][c] + 1
                queue.append((nr, nc))

    return False, -1, -1


## init ##
n, m, battery = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
car_r, car_c = map(int, input().split())
car_r -= 1
car_c -= 1
passenger_arrivals = [0]
for i in range(n):
    for j in range(n):
        # 장애물 값 변경
        if grid[i][j]:
            grid[i][j] = -1
for passenger in range(1, m + 1):
    r_s, c_s, r_e, c_e = map(int, input().split())
    passenger_arrivals.append((r_e - 1, c_e - 1))
    grid[r_s - 1][c_s - 1] = passenger


check_move = False
while True:
    # 1. 최단거리 승객 찾기
    check_move, car_r, car_c = find_passenger(car_r, car_c)

    # 2. 승객을 목적지까지 이동시키기
    if check_move:
        check_move, car_r, car_c = move_passenger(car_r, car_c, grid[car_r][car_c])
    else:
        # 승객 찾기 전에 배터리가 다 되었으므로 종료
        break

    # 종료 조건
    if passenger_arrivals.count(0) == m + 1 or not check_move:
        break

if passenger_arrivals.count(0) == m + 1:
    print(battery)
else:
    print(-1)