'''
술래 위치 : 정중앙
1. m명의 도망자가 먼저 동시에 움직인다.
2. 술래가 움직인다.
3. 시야에 있는 도망자를 잡는다.

술래와의 거리가 3 이하인 도망자만 움직인다.
    - 거리는 절댓값으로 따진다.
    - 현재 바라보고 있는 방향으로 한 칸 움직인다 했을 때 격자를 벗어나지 않는 경우
        - 움직이려는 칸에 술래가 있으면 움직이지 않는다.
        - 훔직이려는 칸에 술래가 있지 않다면, 해당 칸으로 이동. 나무가 있어도 ㄱㅊ
    - 격자를 벗어나는 경우
        - 방향을 반대로 틀어준다.
        - 바라보는 방향으로 한 칸 움직인다 했을 때, 술래가 없다면 한 칸 이동
술래는 위 오 아 왼 방향으로 달팽이 모양으로 움직인다.
    끝에 도달하게 되면 다시 거꾸로 중심으로 이동.
    술래는 무조건 한 칸 이동한다. (방향을 바로 틀어준다)
술래는 턴을 넘기기 전에 도망자를 잡는다
    - 현재 칸을 포함하여 총 3 칸
    - 나무가 있으면 잡히지 않는다.
점수 산정 방법 : 턴 x 잡힌 도망자의 수

풀이:
술래 움직임
    올라갈때 :
        위 우 : 홀수
        아래 왼 : 짝수
        돌았을 때 마다 +1 해주기
        (0, 0) 방문했을 때 방향 바꾸기
    내려갈떄 :
        visited 사용해서 만약 방문했다면 방향 바꾸기

'''

import sys
input = sys.stdin.readline

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
def thief_move():
    for thief_num in range(len(thiefs)):
        # 이미 잡힌 경우
        if not thiefs[thief_num]:
            continue
        r, c, d = thiefs[thief_num]
        if abs(r - police_r) + abs(c - police_c) <= 3:
            nr, nc = r + dr[d], c + dc[d]
            # 범위 초과 시, 방향 바꿔주고 다시 갈 수 있는지 확인
            if not (0 <= nr < n and 0 <= nc < n):
                d = (d + 2) % 4
                nr, nc = r + dr[d], c + dc[d]
            # 움직이려는 칸에 술래가 없다면, 이동
            if (nr, nc) != (police_r, police_c):
                thiefs[thief_num] = (nr, nc, d)
    # 도둑 위치 업데이트
    for thief_num in range(len(thiefs)):
        if not thiefs[thief_num]:
            continue
        r, c, d = thiefs[thief_num]
        if grid[r][c] == -1:
            continue

def police_move(pr, pc, pd):
    global spin
    if not spin:
        nr, nc, nd = path[pr][pc]
        if (nr, nc) == (0, 0):
            spin = (spin + 1) % 2
            visited[0][0] = 1
            return 0, 0, 2
        else:
            visited[nr][nc] = 0
            return nr, nc, nd
    else:
        # 이동 한 다음 바로 방향을 체크해주어야 함
        nr, nc = pr + dr[pd], pc + dc[pd]
        visited[nr][nc] = 1
        # 다음 방향 체크하기
        nnr, nnc = nr + dr[pd], nc + dc[pd]
        if not (0 <= nnr < n and 0 <= nnc < n) or visited[nnr][nnc]:
            pd = (pd - 1) % 4
        if (nr, nc) == (n // 2, n // 2):
            pd = 0
            visited[nr][nc] = 0
            spin = (spin + 1) % 2
        return nr, nc, pd


def catch_thief():
    x1, x2, y1, y2 = police_r + dr[police_d], police_r + dr[police_d] * 2, police_c + dc[police_d], police_c + dc[police_d] * 2
    tmp = 0
    for i in range(len(thiefs)):
        if not thiefs[i]:
            continue
        tr, tc, _ = thiefs[i]
        if grid[tr][tc] == -1:
            continue
        if (tr, tc) == (police_r, police_c) or (tr, tc) == (x1, y1) or (tr, tc) == (x2, y2):
            thiefs[i] = 0
            tmp += 1

    return tmp


n, m, h, k = map(int, input().split())
grid = [[0] * n for _ in range(n)]
thiefs = [0]
for i in range(1, m + 1):
    sx, sy, sd = map(int, input().split())
    if sd == 1:
        thiefs.append((sx - 1, sy - 1, 1))
    else:
        thiefs.append((sx - 1, sy - 1, 2))
for _ in range(h):
    sx, sy = map(int, input().split())
    grid[sx - 1][sy - 1] = -1
path = [[0] * n for _ in range(n)]
visited = [[0] * n for _ in range(n)]
# 나갈 때 path 미리 설정해두기
move_cnt = 0
sr, sc, sd = n // 2, n // 2, 0
while True:
    if sd == 0:
        move_cnt += 1
    if sd == 0 or sd == 1:
        d_len = 2 * move_cnt - 1
    else:
        d_len = 2 * move_cnt

    for i in range(d_len):
        nr, nc = sr + dr[sd], sc + dc[sd]
        if i == d_len - 1:
            path[sr][sc] = (nr, nc, (sd + 1) % 4)
        else:
            path[sr][sc] = (nr, nc, sd)
        sr, sc = nr, nc
    if (sr, sc) == (-1, 0):
        break
    sd = (sd + 1) % 4


police_r, police_c, police_d = n // 2, n // 2, 0
move_cnt, spin = -1, 0

ans = 0
for game_cnt in range(1,k + 1):
    # 1. 도망자 도망
    thief_move()

    # 2. 경찰 이동
    police_r, police_c, police_d = police_move(police_r, police_c, police_d)

    # 3. 도망자 잡기
    ans += game_cnt * catch_thief()

print(ans)