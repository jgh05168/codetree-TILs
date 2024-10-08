'''
22:47

n x n
3명 이상이 한 팀
맨 앞 사람을 머리사람, 맨 뒤 사람을 꼬리사람
각 팀은 게임에서 주어진 이동 선을 따라서만 이동한다

1. 각 팀은 머리사람을 따라서 한 칸 이동한다.
2. 각 라운드마다 공이 정해진 선을 따라 던져진다
    - 0 ~ n : 열 정방향
    - n ~ 2n : 행 역방향
    - 2n ~ 3n : 열 역방향
    - 3n ~ 4n : 행 정방향
3. 공이 던져지는 경우, 해당 선에 사람이 있으면, 최초에 만나게 되는 사람만이 공을 얻어 점수를 얻게된다.
    - k번째 사람이라면, k의 제곱만큼 점수를 얻는다.
    - 공에 맞는 경우 팀의 이동 방향을 바꾼다.

풀이:
1. 각 팀 별 꼬리 리스트를 생성해야 한다.
    - 팀 별 bfs 진행하여 다음 위치 따라가기
    - 1번의 다음 좌표만 안 다음, 나머지는 그대로 이어주기
    - 이후, 맵 업데이트
2. 점수내기
'''

from collections import deque

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

team = []
ans = 0

def make_team(sr, sc):
    queue = deque()
    tmp_team = [(sr, sc)]
    visited = [[0] * n for _ in range(n)]
    queue.append((sr, sc))
    visited[sr][sc] = 1
    team_info[sr][sc] = team_num

    while queue:
        r, c = queue.popleft()

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and 0 < grid[nr][nc] <= 4:
                queue.append((nr, nc))
                visited[nr][nc] = 1
                team_info[nr][nc] = team_num
                if grid[nr][nc] < 4:
                    tmp_team.append((nr, nc))
    team.append(tmp_team)


def next_move(t, r, c):
    new_move = []
    for d in range(len(dr)):
        nr, nc = r + dr[d], c + dc[d]
        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 4:
            new_move.append((nr, nc))
            break
    for idx in range(len(team[t]) - 1):
        r, c = team[t][idx]
        new_move.append((r, c))

    team[t] = new_move


def make_new_grid():
    new_grid = [row[:] for row in grid]
    for t in range(m):
        new_grid[team[t][0][0]][team[t][0][1]] = 1
        for idx in range(1, len(team[t]) - 1):
            r, c = team[t][idx]
            new_grid[r][c] = 2
        r, c = team[t][-1][0], team[t][-1][1]
        new_grid[r][c] = 3
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 3:
                new_grid[nr][nc] = 4
                break

    return new_grid


def get_score(r, c, t):
    for i in range(1, len(team[t]) + 1):
        loc = team[t][i - 1]
        if (r, c) == loc:
            return i * i


n, m, k = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
team_info = [[-1] * n for _ in range(n)]

# 0. 팀 찾기
team_num = 0
for i in range(n):
    for j in range(n):
        if grid[i][j] == 1:
            make_team(i, j)
            team_num += 1

for game in range(k):
    # 1-1. 모든 팀 별 이동할 위치 찾기
    for t in range(m):
        next_move(t, team[t][0][0], team[t][0][1])

    # 1-2. 팀 그리드 업데이트
    grid = make_new_grid()

    # 2. 공 던지기
    direction = game % (4 * n)
    team_num = -1
    if 0 <= direction < n:
        r = direction % n
        for c in range(n):
            if 0 < grid[r][c] < 4:
                team_num = team_info[r][c]
                ans += get_score(r, c, team_num)
                team[team_num].reverse()
                break
    elif n <= direction < 2 * n:
        c = direction % n
        for r in range(n - 1, -1, -1):
            if 0 < grid[r][c] < 4:
                team_num = team_info[r][c]
                ans += get_score(r, c, team_num)
                team[team_num].reverse()
                break
    elif 2 * n <= direction < 3 * n:
        r = n - direction % n
        for c in range(n - 1, -1, -1):
            if 0 < grid[r][c] < 4:
                team_num = team_info[r][c]
                ans += get_score(r, c, team_num)
                team[team_num].reverse()
                break
    else:
        c = n - direction % n
        for r in range(n):
            if 0 < grid[r][c] < 4:
                team_num = team_info[r][c]
                ans += get_score(r, c, team_num)
                team[team_num].reverse()
                break

    # 만약 맞췄다면, 뒤집힌 그리드로 새로 업데이트
    if team_num != -1:
        grid[team[team_num][0][0]][team[team_num][0][1]] = 1
        for idx in range(1, len(team[t]) - 1):
            r, c = team[team_num][idx]
            grid[r][c] = 2
        grid[team[team_num][-1][0]][team[team_num][-1][1]] = 3


print(ans)