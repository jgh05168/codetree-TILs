'''
1. 현재 방향을 기준으로 왼쪽 방향으로 한번도 간 적이 없다면
    좌회전 후 해당 방향으로 이동
2. 만약 왼쪽 방향이 인도거나 이미 방문핸 도로인 경우
    좌회전해서 1번 과정 시도

풀이:
방향 벡터 : 시계 반대방향으로 설정(d - 1) % 4
이동을 체크하는 키를 하나 둔다. -> 얘로 3번 확인
후진할 때는 visited 상관없이 이동하기.
while 문으로 조건 설정하기.
'''

from collections import deque
import sys
input = sys.stdin.readline

#    북  동  남  서
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

def check_move(r, c, direction):
    global sr, sc, sd
    for i in range(1, len(dr) + 1):
        nd = (direction - i) % 4
        nr, nc = r + dr[nd], c + dc[nd]
        if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and not grid[nr][nc]:
            visited[nr][nc] = 1
            sr, sc, sd = nr, nc, nd
            return True
    else:
        return False


n, m = map(int, input().split())
sr, sc, sd = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
visited = [[0] * m for _ in range(n)]
visited[sr][sc] = 1

gameover = False
while True:
    # 1, 2. 왼쪽으로 이동 가능한지 확인
    check_one = check_move(sr, sc, sd)

    # 3. 한 칸 후진 후 다시 1번 과정 시도
    if not check_one:
        while True:
            # 한 칸 후진
            nr, nc = sr + dr[(sd - 2) % 4], sc + dc[(sd - 2) % 4]
            if grid[nr][nc]:
                gameover = True
                break
            # 다시 1번부터 시도
            check_two = check_move(nr, nc, sd)
            if check_two:
                break
            else:
                sr, sc = nr, nc

    if gameover:
        break

ans = 0
for i in range(n):
    ans += sum(visited[i])

print(ans)