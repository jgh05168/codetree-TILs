'''
10:46

박치기게임

[게임판 구성]
n x n
m 개의 턴에 걸쳐 진행된다.
루돌프가 한 번 움직인 뒤, 산타들이 순서대로 움직인다.
게임에서 칸 사이의 거리는 절댓값 합으로 계산

[루돌프 움직임]
가장 가까운 산타를 향해 한 칸 돌진
- 게임에서 탈락하지 않은 산타 중 가장 가까운 산타를 선택
- 2명 이상이라면, r, c 큰 순서대로 돌진
- 루돌프는 8방향 이동 가능.

[산타 움직임]
1 ~ p 번 순서대로 움직인다.
- 기절했거나 이미 탈락한 산타는 움직일 수 없음
- 다른 산타가 있거나 격자 밖으로는 이동 불가능
- 움직일 수 없다면 이동하지 않음
- 루돌프와 가까워지는 방법이 없다면 이동 불가
- 상우하좌 우선순위

[충돌]
같은 칸에 있으면 충돌 발생
- 루돌프가 박은 경우 : 해당 산타는 c만큼 점수 획득
    - 산타는 루돌프가 이동한 방향으로 c칸 밀려남
- 산타가 박은 경우 : 해당 산타는 d만큼 점수 획득
    - 자신의 반대 방향으로 d칸 밀려난다.
- 밀려나는 도중에는 충돌이 일어나지 않음
- 밀려난 위치가 게임판 밖이라면 산타는 탈락
- 밀려난 칸에 다른 산타가 있는 경우, 상호작용 발생

[상호작용]
- 착지하는 칸에서만 상호작용이 발생함
- 맞은 산타는 충돌한 산타가 온 방향으로 한 칸 밀려남
- 또다른 산타가 존재한다면, 연쇄적으로 밀려난다.
- 게임판 밖으로 밀려나면 탈락

[기절]
k번째 턴에 기절했다면, k + 2부터 정상상태가 된다.
- 기절한 산타는 움직일 수 없다
- 충돌이나 상호작용으로 밀려날 수는 있다.
- 루돌프는 기절산타를 돌진 상대로 지목할 수 있다.

[게임 종료]
p명의 산타가 모두 탈락하면 게임 종료
매 턴 이후 탈락하지 않은 산타들에겐 1점 추가부여

각 산타가 얻은 최종 점수를 구하자

필요 메모리:
1차원배열
 - 산타 위치
 - 산타 점수
 - 산타 스턴
 2차원배열
- 해당 칸에 산타 번호 입력

산타를 순회하며 루돌프에서 이동할 수 있는 가장 가까운 산타를 고른다.
고른 뒤 해당 방향으로 돌진하기
'''

dr = [-1, 0, 1, 0, -1, 1, 1, -1]
dc = [0, 1, 0, -1, 1, 1, -1, -1]
santa_loc = [0]
score = [0]
stun = [0]


def get_distance(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def find_next_sant():
    global rudolph
    rr, rc = rudolph
    cur_dist = N**2 * N**2
    santa_idx, santa_r, santa_c = 0, -1, -1
    for santa in range(1, P + 1):
        if not santa_loc[santa]:
            continue
        sr, sc = santa_loc[santa]
        new_dist = get_distance(rr, rc, sr, sc)
        if cur_dist > new_dist:
            cur_dist = new_dist
            santa_idx = santa
            santa_r, santa_c = sr, sc
        elif cur_dist == new_dist and sr > santa_r:
            cur_dist = new_dist
            santa_idx = santa
            santa_r, santa_c = sr, sc
        elif cur_dist == new_dist and sr == santa_r and sc > santa_c:
            cur_dist = new_dist
            santa_idx = santa
            santa_r, santa_c = sr, sc
    return santa_idx


def rudolph_move(santa):
    global rudolph
    rr, rc = rudolph
    sr, sc = santa_loc[santa]
    new_r, new_c, new_d = rr, rc, -1
    cur_dist = get_distance(rr, rc, sr, sc)
    for d in range(len(dr)):
        nr, nc = rr + dr[d], rc + dc[d]
        if 0 <= nr < N and 0 <= nc < N:
            new_dist = get_distance(nr, nc, sr, sc)
            if new_dist < cur_dist:
                new_r, new_c, new_d = nr, nc, d
                cur_dist = new_dist

    # 산타와 충돌했는지 확인하기
    rudolph = (new_r, new_c)
    if (new_r, new_c) == (sr, sc):
        # 충돌
        crash(santa, 0, new_d)



def santa_move():
    for santa in range(1, P + 1):
        if not santa_loc[santa] or stun[santa]:
            continue
        rr, rc = rudolph
        sr, sc = santa_loc[santa]
        cur_dist = get_distance(rr, rc, sr, sc)
        # 루돌프와 가까워지는 방향으로 한 칸 이동
        new_r, new_c, new_d = sr, sc, -1
        for d in range(4):
            nr, nc = sr + dr[d], sc + dc[d]
            if 0 <= nr < N and 0 <= nc < N and not grid[nr][nc]:
                new_dist = get_distance(nr, nc, rr, rc)
                if cur_dist > new_dist:
                    cur_dist = new_dist
                    new_r, new_c, new_d = nr, nc, d
        # 움직였다면,
        if (new_r, new_c) != (sr, sc):
            # 충돌 확인하기
            santa_loc[santa] = (new_r, new_c)
            grid[new_r][new_c], grid[sr][sc] = grid[sr][sc], grid[new_r][new_c]
            if (rr, rc) == (new_r, new_c):
                crash(santa, 1, new_d)


def crash(santa, attacker, d):
    global score, santa_loc, stun
    # 박은 산타는 점수를 얻는다.
    sr, sc = santa_loc[santa]
    stun[santa] = 2
    grid[sr][sc] = 0
    if not attacker:
        score[santa] += C
        r, c = sr + dr[d] * C, sc + dc[d] * C
        # 산타 죽음
        if not (0 <= r < N and 0 <= c < N):
            santa_loc[santa] = 0
        else:
            santa_loc[santa] = (r, c)
            # 산타가 없다면 입력하고 끝
            if not grid[r][c]:
                grid[r][c] = santa
            else:
                # 상호작용
                new_santa = grid[r][c]
                grid[r][c] = santa
                interaction(new_santa, r, c, d)
    else:
        score[santa] += D
        r, c = sr + dr[(d + 2) % 4] * D, sc + dc[(d + 2) % 4] * D
        # 산타 죽음
        if not (0 <= r < N and 0 <= c < N):
            santa_loc[santa] = 0
        else:
            santa_loc[santa] = (r, c)
            # 산타가 없다면 입력하고 끝
            if not grid[r][c]:
                grid[r][c] = santa
            else:
                # 상호작용
                new_santa = grid[r][c]
                grid[r][c] = santa
                interaction(new_santa, r, c, (d + 2) % 4)


def interaction(santa, r, c, d):
    global santa_loc, grid
    nr, nc = r + dr[d], c + dc[d]
    new_santa = santa
    while 0 <= nr < N and 0 <= nc < N and grid[nr][nc]:
        new_santa = grid[nr][nc]
        santa_loc[santa] = (nr, nc)
        grid[nr][nc] = santa
        nr, nc = nr + dr[d], nc + dc[d]
    if 0 <= nr < N and 0 <= nc < N:
        grid[nr][nc] = new_santa
        santa_loc[new_santa] = (nr, nc)
    else:
        grid[nr][nc] = 0
        santa_loc[new_santa] = 0


N, M, P, C, D = map(int, input().split())
grid = [[0] * N for _ in range(N)]
rr, rc = map(int, input().split())
rudolph = (rr - 1, rc - 1)
santa_loc = [0] * (P + 1)
score = [0] * (P + 1)
stun = [0] * (P + 1)
for ts in range(1, P + 1):
    p, sr, sc = map(int, input().split())
    santa_loc[p] = (sr - 1, sc - 1)
    grid[sr - 1][sc - 1] = p

for _ in range(M):
    # 1-1. 잡을 산타 찾기
    target_santa = find_next_sant()

    # 1-2. 산타를 향해 이동
    rudolph_move(target_santa)

    # 2. 산타 이동
    santa_move()

    # 3. 기절 해제
    for i in range(1, P + 1):
        if stun[i]:
            stun[i] -= 1

    # 4. 살아남은 산타들 1점 추가
    for i in range(1, P + 1):
        if santa_loc[i]:
            score[i] += 1

    # 5. 게임종료
    if santa_loc.count(0) == P + 1:
        break

print(*score[1:])

# 점수 산정