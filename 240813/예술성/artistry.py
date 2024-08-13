'''
n x n

상하좌우로 같은 숫자라면 동일한 그룹
1. 예술 점수 : 모든 그룹 싸으이 조화로움의 합
    - (그룹 a 칸 수 + 그룹 b 칸 수) x 그룹 a 숫자 x 그룹 b 숫자 x 맞닿아있는 변의 수(딕셔너리)
조합으로 모든 조화로움 값을 더하자 = 초기 예술 점수
2. 그림에 대한 회전 진행
    - 십자 모양 : 반시계 방향으로 회전
    - 나머지 부분 : 개별적으로 시계 방향으로 회전

위를 3번 진행했을 때 예술 점수의 합을 구하자

풀이:
1. bfs 사용하여 각 그룹 나누기
2. 그룹 별로 dict 사용하여 인접한 부분 체크
3. 조합 사용하여 모든 점수 구하기
4. 회전 진행
'''

from collections import defaultdict
from collections import deque
import sys
input = sys.stdin.readline

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def bfs(group, sr, sc, number):
    queue = deque([(sr, sc)])
    visited[sr][sc] = group
    tmp_border = []
    group_cnt = 1

    while queue:
        r, c = queue.popleft()

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n:
                # 만약 경계면이라면,
                if grid[nr][nc] != number:
                    tmp_border.append((nr, nc))
                if visited[nr][nc] == -1 and grid[nr][nc] == number:
                    queue.append((nr, nc))
                    visited[nr][nc] = group
                    group_cnt += 1

    return tmp_border, group_cnt


def check_border():
    for i in range(len(all_group_borders)):
        border_dict[i] = [0] * group_num
        for j in range(len(all_group_borders[i])):
            br, bc = all_group_borders[i][j]
            border_dict[i][visited[br][bc]] += 1


def get_value(cnt, idx, adj_num):
    global tmp_ans
    if cnt == 2:
        a, b = adj_num[0], adj_num[1]
        # (그룹 a 칸 수 + 그룹 b 칸 수) x 그룹 a 숫자 x 그룹 b 숫자 x 맞닿아있는 변의 수
        tmp_ans += (group_cnts[a] + group_cnts[b]) * group_values[a] * group_values[b] * border_dict[a][b]
    else:
        for i in range(idx + 1, group_num):
            if idx >= 0 and not border_dict[idx][i]:
                continue
            get_value(cnt + 1, i, adj_num + [i])


def rotate():
    new_grid = [[0] * n for _ in range(n)]
    center = n // 2

    # 구역 나눠서 돌리기
    for i in range(n):
        for j in range(n):
            if i == center or j == center:
                new_grid[n - j - 1][i] = grid[i][j]
    # 첫번째 구역
    for i in range(center):
        for j in range(center):
            new_grid[j][center - i - 1] = grid[i][j]
    # 두번째 구역
    for i in range(center):
        for j in range(center + 1, n):
            new_grid[j - center - 1][n - i - 1] = grid[i][j]
    # 세번째 구역
    for i in range(center + 1, n):
        for j in range(center):
            new_grid[center + j + 1][n - i - 1] = grid[i][j]
    # 네번째 구역
    for i in range(center + 1, n):
        for j in range(center + 1, n):
            new_grid[j][n - i + center] = grid[i][j]

    return new_grid


n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]

ans_list = []
for _ in range(4):
    # 0. 사용할 초기 배열 세팅
    visited = [[-1] * n for _ in range(n)]
    all_group_borders = []
    group_cnts = []
    group_values = []
    border_dict = defaultdict(list)

    # 1. 그룹 나누기
    group_num = 0
    for i in range(n):
        for j in range(n):
            if visited[i][j] == -1:
                group_values.append(grid[i][j])
                g_border, g_cnt = bfs(group_num, i, j, grid[i][j])
                all_group_borders.append(g_border)
                group_cnts.append(g_cnt)
                group_num += 1

    # 2. 인접한 부분 체크하기
    check_border()

    tmp_ans = 0
    # 3. 조합 짜서 계산하기
    get_value(0, -1, [])
    ans_list.append(tmp_ans)

    # 4. rotate
    grid = rotate()

print(sum(ans_list))