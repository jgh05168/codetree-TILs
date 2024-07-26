'''
격자의 숫자들 : 지역별 인구수
대각선으로 움직인다.
    - 6시 -> 3시 -> 12시 -> 9시 -> 6시 로 이동
    - 각 방향으로 최소 한 번은 이동해야 한다.

경계와, 그 안에 지역을 갖게 된다.

1번 부족 : 경계와 그 안쪽 지역
2번 부족 : 좌측 상단 경계의 윗부분(위 꼭짓점 위 부분은 포함, 왼쪽 꼭짓점 왼쪽은 미포함)
3번 부족 : 우측 상단 경계 윗부분(오른 쪽짓점 오른쪽 포함, 위 꼭짓점 미포함)
4번 부족 : 좌측 하단 아래 부분(왼쪽 꼭짓점 왼쪽 포함, 아래 꼭짓점 아래 미포함)
5번 부족 : 우측 하단 아래 부분(아래 꼭짓점 아래 포함, 오른 꼭짓점 포함

인구수 최솟값 구하자.

풀이:
1. 경계선 그리기(완탐)
    - 시작점 : 2 <= 행 < n and 1 <= 열 < n - 1
    - 가능한 모든 경우에 대해 돌려보기
2. 구역 나눠서 부족 배열에 저장
3. 최소가 되는 값 업데이트

완탐
20 x 20이라 충분할 듯
개 삽 노 가 다 
'''

import sys
input = sys.stdin.readline

# 대각선 방향으로 움직이도록 저장
dr = [-1, -1, 1, 1]
dc = [1, -1, -1, 1]


def calc_population():
    global ans
    cities = [0] * 5
    # 꼭짓점 찾기
    start, end, low, high = (0, n), (0, -1), (-1, 0), (n, 0)
    for i in range(n):
        for j in range(n):
            if border[i][j]:
                if j < start[1]:
                    start = (i, j)
                if j > end[1]:
                    end = (i, j)
                if i > low[0]:
                    low = (i, j)
                if i < high[0]:
                    high = (i, j)

    visited = [[0] * n for _ in range(n)]
    # 부족 2
    for i in range(start[0]):
        for j in range(high[1] + 1):
            if border[i][j]:
                break
            else:
                cities[1] += grid[i][j]
                visited[i][j] = 1
    # 부족 3
    for i in range(end[0] + 1):
        for j in range(n - 1, high[1], -1):
            if border[i][j]:
                break
            else:
                cities[2] += grid[i][j]
                visited[i][j] = 1
    # 부족 4
    for i in range(start[0], n):
        for j in range(low[1]):
            if border[i][j]:
                break
            else:
                cities[3] += grid[i][j]
                visited[i][j] = 1
    # 부족 5
    for i in range(end[0] + 1, n):
        for j in range(n - 1, low[1] - 1, -1):
            if border[i][j]:
                break
            else:
                cities[4] += grid[i][j]
                visited[i][j] = 1

    # 부족 1
    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                cities[0] += grid[i][j]

    ans = min(ans, max(cities) - min(cities))

def make_border(sr ,sc, d, border_num):
    r, c = sr, sc

    if d == 4:
        if (r, c) == (start_r, start_c):
            # 2. 이 때 부족 계산하러 들어가기
            calc_population()
    else:
        tmp_border = []  # 나중에 pop해서 다 없애줄거임
        if border_num == 1 or border_num == 2:
            while 0 <= r < n and 0 <= c < n:
                # 한 번 해보고 다음 재귀로 들어가기
                nr, nc = r + dr[d], c + dc[d]
                if not (0 <= nr < n and 0 <= nc < n):
                    break
                border[nr][nc] = 1
                tmp_border.append((nr, nc))
                border_len_dict[border_num] += 1
                make_border(nr, nc, d + 1, border_num + 1)
                r, c = nr, nc
        else:
            for _ in range(border_len_dict[(border_num + 2) % 4]):
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < n and 0 <= nc < n:
                    # 이미 지나온 길이라면 잘못된 경계이므로 break
                    if border[nr][nc]:
                        break
                    border[nr][nc] = 1
                    tmp_border.append((nr, nc))
                    make_border(nr, nc, d + 1, border_num + 1)
                    r, c = nr, nc
                else:
                    break

        while tmp_border:
            br, bc = tmp_border.pop()
            border[br][bc] = 0
            border_len_dict[border_num] -= 1


n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]

border_len_dict = {1: 0, 2: 0, 3: 0, 4: 0}

ans = int(1e9)
# 1. 경계 시작점에서 완탐으로 찾아내기
for start_r in range(2, n):
    for start_c in range(1, n - 1):
        border = [[0] * n for _ in range(n)]
        make_border(start_r, start_c, 0, 1)

print(ans)