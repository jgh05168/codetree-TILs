'''
11:10
꼬리잡기놀이
3명 이상이 한 팀이 된다.
맨 앞사람 : 머리사람, 맨 뒤사람 : 꼬리사람

1. 각 팀은 머리사람을 따라서 한 칸 이동한다.
2. 각 라운드마다 공이 정해진 선을 따라 던져진다.
    행 열 방향 유의
3. 공이 던져지는 경우, 해당 선에 최초로 만나는 사람이 공을 얻게 되어 점수를 얻는다.
    - 팀 내 k번째 사람이라면, k**2만큼 얻는다.

원형 큐, 사전에 모든 라인 정보를 저장해두기
원형큐 업데이트

'''

from collections import deque

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

teams = [0]
ans = 0

def bfs(sr, sc, team_idx):
    global teams
    queue = deque([(sr, sc)])
    team_grid[sr][sc] = team_idx
    tmp_team = deque([(sr, sc)])
    check_three = 0

    while queue:
        r, c = queue.popleft()

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not team_grid[nr][nc]:
                if grid[r][c] + 1 == grid[nr][nc] or grid[nr][nc] == 2:
                    queue.append((nr, nc))
                    team_grid[nr][nc] = team_idx
                    tmp_team.append((nr, nc))
                    if grid[nr][nc] == 3:
                        check_three = 1
                elif check_three and grid[nr][nc] == 4:
                    queue.append((nr, nc))
                    team_grid[nr][nc] = team_idx
                    tmp_team.append((nr, nc))
    teams.append(tmp_team)


def team_move():
    global teams
    for t in range(1, team_idx):
        # 마지막 인덱스에 맨 앞 친구 값 넣어주기
        for i in range(1, len(teams[t])):
            r, c = teams[t][i]
            nr, nc = teams[t][i - 1]
            if grid[nr][nc] == 4:
                break
            grid[nr][nc] = grid[r][c]
        nr, nc = teams[t][-1]
        grid[nr][nc] = 1
        teams[t].appendleft(teams[t].pop())


def get_score(team_num):
    global ans
    for idx in range(len(teams[team_num])):
        if teams[team_num][idx] == (r, c):
            ans += (idx + 1) ** 2
            break
    change_heading(team_num)
    return 1


def change_heading(team_num):
    global teams
    reverse_team = deque()
    for i in range(len(teams[team_num])):
        r, c = teams[team_num][i]

        reverse_team.appendleft((r, c))
        if grid[r][c] == 3:
            grid[r][c] = 1
            break
        if not i:
            grid[r][c] = 3
    for j in range(len(teams[team_num]) - 1, i, -1):
        reverse_team.append((teams[team_num][j]))
    teams[team_num] = reverse_team


n, m, k = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

# 0. init()
team_grid = [[0] * n for _ in range(n)]
team_idx = 1
for i in range(n):
    for j in range(n):
        if grid[i][j] == 1 and not team_grid[i][j]:
            bfs(i, j, team_idx)
            team_idx += 1

# 게임시작
for time in range(k):
    # 1. 머리사람 따라서 한 칸 이동
    team_move()

    # 2. 공 던지기
    ball_num = time % (4 * n)
    if 0 <= ball_num < n:
        r = time % n
        for c in range(n):
            # 맞는 놈을 찾았다면, 점수 계산
            if 1 <= grid[r][c] < 4:
                if get_score(team_grid[r][c]):
                    break
    elif n <= ball_num < 2 * n:
        c = time % n
        for r in range(n - 1, -1, -1):
            if 1 <= grid[r][c] < 4:
                if get_score(team_grid[r][c]):
                    break
    elif 2 * n <= ball_num < 3 * n:
        r = n - 1 - time % n
        for c in range(n - 1, -1, -1):
            # 맞는 놈을 찾았다면, 점수 계산
            if 1 <= grid[r][c] < 4:
                if get_score(team_grid[r][c]):
                    break
    else:
        c = n - 1 - time % n
        for r in range(n):
            if 1 <= grid[r][c] < 4:
                if get_score(team_grid[r][c]):
                    break

print(ans)