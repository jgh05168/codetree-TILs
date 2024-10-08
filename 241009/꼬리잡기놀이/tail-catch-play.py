'''
n x n
3명 이상이 한 팀이 된다.
모든 사람들은 자신의 앞 사람을 따라 움직인다 (path 배열)
1. 머리 사람을 따라 한 칸 이동한다.
2. 공이 정해진 선을 따라 던져진다.
    - 4n 동안 우 상 좌 하 방향으로, 던져진다.
    - 시작점은 0, 0, n-1, n-1 순
    - 4n이 넘어가면 다시 반복한다.
3. 최초에 만나게 되는 사람만이 공을 얻게 되어 점수를 얻는다.
    - 해당 사람이 머리 사람을 시작으로 k번째 사람이라면(idx num), k의 제곱만큼 점수를 얻는다.
    - 공을 획득한 팀의 경우, 머리사람과 꼬리 사람이 바뀐다.(방향 반대)

풀이:
1. init()에서 bfs 사용하여 각 팀의 이동 동선을 알아낸다.
    - 원형 deck 사용
    - 방향 바뀔 때마다 pop하여 진행
    - path 정보를 저장
    - 몇 명 존재하는지도 카운트하기
2. 게임 할 때마다 path의 마지막 지점을 pop 한 다음 appendleft 한다.
3. 숫자 세주기

'''

from collections import deque


dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def bfs(sr, sc, team_num):
    queue = deque()
    visited[sr][sc] = team_num
    queue.append((sr, sc))
    team_path = deque([(sr, sc)])
    member_cnt = 1
    next_queue = deque([(sr, sc)])

    while queue:
        r, c = queue.popleft()
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc]:
                if grid[nr][nc] + 1 == grid[r][c] or grid[nr][nc] == 2:
                    team_path.appendleft((nr, nc))
                    member_cnt += 1
                    visited[nr][nc] = team_num
                    queue.append((nr, nc))
    # path 구해주기
    while next_queue:
        r, c = next_queue.popleft()
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] == 4:
                team_path.append((nr, nc))
                next_queue.append((nr, nc))
                visited[nr][nc] = team_num
                break

    return team_path, member_cnt

def init():
    team_num = 1
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 3:
                teams.append(bfs(i, j, team_num))
                team_num += 1


def move_runner():
    for team_idx in range(m):
        team, members = teams[team_idx]
        er, ec = team.pop()
        tmp_val = grid[er][ec]
        team.appendleft((er, ec))
        for idx in range(1, members + 1):
            try:
                grid[team[idx - 1][0]][team[idx - 1][1]] = grid[team[idx][0]][team[idx][1]]
            except:
                idx += 1
                break
        if idx > members:
            grid[team[-1][0]][team[-1][1]] = tmp_val
        else:
            grid[team[idx][0]][team[idx][1]] = tmp_val

def change_move(team_idx):
    team, members = teams[team_idx]
    tmp_list = deque()
    # 술래 위치 reverse
    grid[team[members - 1][0]][team[members - 1][1]] = 1
    tmp_list.append(team[members - 1])
    for idx in range(members - 2, 0, -1):
        tmp_list.append(team[idx])
        grid[team[idx][0]][team[idx][1]] = 2
    grid[team[0][0]][team[0][1]] = 3
    tmp_list.append(team[0])
    # path 위치 reverse
    for idx in range(len(team) - 1, members - 1, -1):
        tmp_list.append(team[idx])
    teams[team_idx] = (tmp_list, members)

def catch_runner(game_dir, ball_idx):
    global ans
    if not game_dir:
        for c in range(n):
            if 0 < grid[ball_idx][c] < 4:
                # 점수 내기
                for i in range(teams[visited[ball_idx][c] - 1][1]):
                    if (ball_idx, c) == teams[visited[ball_idx][c] - 1][0][i]:
                        ans += ((i + 1) ** 2)
                        break
                # 3. 술래 방향 바꾸기
                change_move(visited[ball_idx][c] - 1)
                break
    elif game_dir == 1:
        for r in range(n - 1, -1, -1):
            if 0 < grid[r][ball_idx] < 4:
                # 점수 내기
                for i in range(teams[visited[r][ball_idx] - 1][1]):
                    if (r, ball_idx) == teams[visited[r][ball_idx] - 1][0][i]:
                        ans += ((i + 1) ** 2)
                        break
                # 3. 술래 방향 바꾸기
                change_move(visited[r][ball_idx] - 1)
                break
    elif game_dir == 2:
        for c in range(n - 1, -1, -1):
            if 0 < grid[n - ball_idx - 1][c] < 4:
                # 점수 내기
                for i in range(teams[visited[n - ball_idx - 1][c] - 1][1]):
                    if (n - ball_idx - 1, c) == teams[visited[n - ball_idx - 1][c] - 1][0][i]:
                        ans += ((i + 1) ** 2)
                        break
                # 3. 술래 방향 바꾸기
                change_move(visited[n - ball_idx - 1][c] - 1)
                break
    else:
        for r in range(n):
            if 0 < grid[r][n - ball_idx - 1] < 4:
                # 점수 내기
                for i in range(teams[visited[r][n - ball_idx - 1] - 1][1]):
                    if (r, n - ball_idx - 1) == teams[visited[r][n - ball_idx - 1] - 1][0][i]:
                        ans += ((i + 1) ** 2)
                        break
                # 3. 술래 방향 바꾸기
                change_move(visited[r][n - ball_idx - 1] - 1)
                break



n, m, k = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
visited = [[0] * n for _ in range(n)]

teams = []
init()

ans = 0
game_dir = -1
for round in range(k):
    # 0. 4n 맞춰주기
    if not round % n:
        game_dir = (game_dir + 1) % 4

    # 1. 술래 이동
    move_runner()

    # 2. 게임 시작
    catch_runner(game_dir, round % n)

print(ans)