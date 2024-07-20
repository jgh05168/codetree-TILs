'''
- m개의 몬스터, 하나의 전투로봇
- 초기 전투로봇 레벨 : 2, 전투로봇은 1초에 상하좌우로 인접한 한 칸씩 이동
- 전투로봇은 자신보다 큰 레벨 몬스터 제외하면 모든 칸 갈 수 있음
    - 자신보다 낮은 레벨의 몬스터만 없앨 수 있음
    - 레벨이 같으면 잡지는 못하지만 해당 칸을 지날 수는 있음
- 이동 규칙
    - 없앨 수 있는 몬스터가 있다면 해당 몬스터를 없애러 간다. = 레벨 낮은 몬스터가 존재하는 경우
    - 없앨 수 있는 몬스터가 하나 이상이라면 거리가 가장 가까운 몬스터를 없애러 간다. = 유클리드 거리
        - 방향 : r, c 순서로 가까운 몬스터 제거
    - 없앨 수 있는 몬스터가 없다면 일을 끝냄
- 같은 수의 몬스터를 없앨 때마다 레벨이 상승함

풀이 :
상왼오하 순으로 이동
몬스터는 레벨을 idx로 설정하여 연결리스트로 저장
로봇이 이동할 때,
1. 우선 자신보다 낮은 레벨 로봇 몇 갠지 체크
2. 여러개라면, 각각에 대해 거리 계산
3. 잡을 로봇을 정했다면 4방향으로 이동해본 뒤 가장 가깝게 줄여지는 거리로 이동 (bfs)
4. 한 칸 이동
5. 잡은 뒤, 잡아야 하는 몬스터수 -1. 만약 몬스터를 다 잡았다면 레벨업

그냥 bfs 돌면서 잡을 수 있는 로봇이 있다면 잡기.
- 만약 여러 로봇이 잡힌다면, r, c 순으로 큰 로봇 하나만 잡기
- 움직인 vistied 만큼 cnt에 더해주기
'''

from collections import deque
import sys, copy
input = sys.stdin.readline

dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]

def bfs(sr, sc):
    global cnt, robot_level, need_monster, robot_r, robot_c
    queue = deque()
    visited = [[-1] * n for _ in range(n)]
    queue.append((sr, sc))
    visited[sr][sc] = 0

    catch_robot_list = []
    while True:
        new_queue = deque()
        while queue:
            r, c = queue.popleft()

            for d in range(len(dr)):
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < n and 0 <= nc < n and visited[nr][nc] == -1 and grid[nr][nc] <= robot_level:
                    # 로봇을 잡은 경우
                    if 0 < grid[nr][nc] < robot_level:
                        catch_robot_list.append((nr, nc))
                    visited[nr][nc] = visited[r][c] + 1
                    new_queue.append((nr, nc))
        # 잡은 로봇이 존재할 경우
        if catch_robot_list:
            check_r, check_c = n, n
            for mon_r, mon_c in catch_robot_list:
                if mon_r < check_r:
                    check_r, check_c = mon_r, mon_c
                elif mon_r == check_r and mon_c < check_c:
                    check_r, check_c = mon_r, mon_c
            break
        if not new_queue:
            break
        else:
            queue = copy.deepcopy(new_queue)

    # 잡은 로봇 처리
    if catch_robot_list:
        grid[check_r][check_c] = 0
        cnt += visited[check_r][check_c]
        need_monster -= 1
        if not need_monster:
            robot_level += 1
            need_monster = robot_level
        robot_r, robot_c = check_r, check_c
        return True
    # 잡은 로봇이 없다면 종료
    else:
        return False

n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]

for i in range(n):
    for j in range(n):
        if grid[i][j]:
            if grid[i][j] == 9:
                robot_r, robot_c = i, j

robot_level = 2
need_monster = 2

cnt = 0
while True:
    # 로봇을 잡을 수 없는 경우를 판단
    possible = bfs(robot_r, robot_c)

    # 게임 종료
    if not possible:
        break

print(cnt)