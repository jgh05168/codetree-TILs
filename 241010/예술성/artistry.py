'''
14:53

n x n 1 ~ 10 숫잘 표현

1. 그룹 찾기 : 동일한 숫자가 상하좌우로 인접해야 함
2. 예술 점수 매기기 : 모든 그룹 쌍의 조화로움의 합
    - 2개의 그룹을 뽑은 뒤 조화로움 계산하기
    - 맞닿아있는 변이 있는 애들로만 진행
    점수 산정 : (a 칸수 + b 칸수) x a 숫자 x b 숫자 x 맞닿아있는 변의 수
3. 회전 진행
    - 십자 모양의 경우 반시계 90도
    - 십자 제외한 나머지 정사각형은 90도 시계방향
총 3회전 이후 예술 점수 총합 구하기

group(visited)
현재 그룹과 맞닿아있는 그룹 set
'''

from collections import deque

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

ans = 0
visited = []
adj_group = []

def bfs(sr, sc, group_num, num):
    global adj_group
    queue = deque([(sr, sc)])
    visited[sr][sc] = group_num
    cnt = 1

    while queue:
        r, c = queue.popleft()
        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n:
                if not visited[nr][nc] and grid[nr][nc] == num:
                    visited[nr][nc] = group_num
                    queue.append((nr, nc))
                    cnt += 1
                elif 0 < visited[nr][nc] < group_num:
                    adj_group[visited[nr][nc]].add(group_num)
                    try:
                        adj_space[visited[nr][nc]][group_num] += 1
                    except:
                        while len(adj_space[visited[nr][nc]]) < group_num:
                            adj_space[visited[nr][nc]].append(0)
                        adj_space[visited[nr][nc]].append(1)
    return cnt


def get_value(group):
    tmp = 0
    r, c = group_info[group][0], group_info[group][1]
    for another in adj_group[group]:
        nr, nc = group_info[another][0], group_info[another][1]
        tmp += (group_info[group][2] + group_info[another][2]) * grid[r][c] * grid[nr][nc] * adj_space[group][another]
    return tmp


def rotate():
    new_grid = [[0] * n for _ in range(n)]
    nn = n // 2
    for i in range(n):
        for j in range(n):
            # 가운데 녀석들인 경우, 반시계로 회전
            if i == nn or j == nn:
                new_grid[n - 1 - j][i] = grid[i][j]
            elif 0 <= i < nn and 0 <= j < nn:
                new_grid[j][nn - 1 - i] = grid[i][j]
            elif nn < i < n and 0 <= j < nn:
                si = nn + 1
                oi, oj = i - si, j
                ni, nj = oj, nn - 1 - oi
                new_grid[ni + si][nj] = grid[i][j]
            elif 0 <= i < nn and nn < j < n:
                sj = nn + 1
                oi, oj = i, j - sj
                ni, nj = oj, nn - 1 - oi
                new_grid[ni][nj + sj] = grid[i][j]
            else:
                si, sj = nn + 1, nn + 1
                oi, oj = i - si, j - sj
                ni, nj = oj, nn - 1 - oi
                new_grid[ni + si][nj + sj] = grid[i][j]
    return new_grid


n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]

for _ in range(4):
    # 1. 그룹 찾기
    visited = [[0] * n for _ in range(n)]
    adj_group = [0]
    adj_space = [0]
    group_info = [0]
    group_num = 1
    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                adj_group.append(set())
                adj_space.append([0] * (group_num + 1))
                group_info.append((i, j, bfs(i, j, group_num, grid[i][j])))
                group_num += 1

    # 2. 예술성 계산하기
    for g in range(1, group_num - 1):
        ans += get_value(g)

    # 3. rotate
    grid = rotate()

print(ans)