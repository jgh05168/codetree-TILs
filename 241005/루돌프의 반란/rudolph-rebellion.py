'''
16:20

m개의 턴에 걸쳐 진행
    - 매 턴마다 루돌프한번, 산타 한 번 움직임
    - 산타는 순번대로 움직이며, 기절해있는 녀석은 이동불가능
    - 두 칸 사이의 거리는 제곱합으로 결정

[루돌프]
- 게임에서 탈락하지 않은 가장 가까운 산타를 향해 1칸 돌진
- 가까운 산타가 2명 이상일 경우 r좌표가 큰, c 좌표가 큰 순서로 돌진
- 우선순외가 높은 산타를 향해 8방향 중 하나로 돌진 가능

[산타]
- 순차적으로 움직인다
- 기절 or 탈락한 산타는 움직일 수 없음
- 루돌프에게 거리가 가장 가까워지는 방향으로 한 칸 이동
- 다른 산타가 있는 칸 or 격자 밖으로는 이동 불가능
- 움직일 칸이 없다면 이동하지 않음
    - 움직일 칸이 있어도 루돌프에게 가까워지지 않으면 움직이지 않음
- 상우하좌 우선순위에 따라 이동. (가까워지는 경우가 여러개라면)

[충돌]
- 루돌프가 움직여서 충돌난 경우 : 해당 산타는 c만큼 점수를 얻고, 산타는 루돌프가 이동한 방향으로 c칸만큼 밀려난다.
- 산타가 움직여서 충돌난 경우 : 해당 산타는 d만큼 점수를 얻고, 산타는 자신의 반대방향으로 d칸만큼 밀려난다.
- 밀려나는 도중에는 충돌이 일어나지 않고 정확히 원하는 곳에 도달한다.
- 격자 밖으라면, 산타는 탈락. 다른 산타가 있는 경우 상호작용 발생

[상호작용]
- 다른 산타는 충돌한 산타 방향으로 한 칸 밀려난다. (연쇄적으로 작용된다.) - queue

[기절]
- 루돌프와 충돌 후 기절. 현재가 k번째 턴이라면, k + 1번째 턴까지 기절하며, k + 2부터 다시 이동 간으
- 기절한 산타는 이동불가. 단, 상호작용으로 밀려날 수는 있다.
- 루돌프는 기절 산타를 돌진 대상으로 선택할 수 있음

[게임 종료]
p명의 산타가 모두 게임에서 탈락하면, 즉시 종료
매 턴 이후 탈락하지 않은 산타들에게는 점수 1점 추가 부여
게임 종료 후 각 산타가 얻은 최종 점수를 모두 출력

풀이:
산타 < 30 : for문 돌며 산타 위치 찾아도 된다.

'''

from collections import defaultdict, deque

# 상우하좌, 대각선
dr = [-1, 0, 1, 0, -1, 1, 1, -1]
dc = [0, 1, 0, -1, 1, 1, -1, -1]


def distance(r1, r2, c1, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2


def interaction(santa, nr, nc, d):
    cur_santa = santa
    while 0 <= nr < n and 0 <= nc < n and grid[nr][nc]:
        new_santa = grid[nr][nc]
        grid[nr][nc] = cur_santa
        santa_list[cur_santa - 1] = (nr, nc)
        cur_santa = new_santa
        nr += dr[d]
        nc += dc[d]
    # 만약 격자 밖으로 밀려서 죽은 경우라면,
    if not (0 <= nr < n and 0 <= nc < n):
        santa_list[cur_santa - 1] = 0
    # 지정된 칸이 비어서 멈춘거라면, 이동시키기
    else:
        grid[nr][nc] = cur_santa
        santa_list[cur_santa - 1] = (nr, nc)


def rudolph_move():
    tmp_distance = n * n
    nrr, nrc, nrd = -1, -1, -1
    sr, sc = 0, 0
    # 산타를 찾고
    for santa in santa_list:  # O(30)
        # 튕겨나간 산타라면, 종료
        if not santa:
            continue
        tmp_sr, tmp_sc = santa
        new_distance = distance(rr, tmp_sr, rc, tmp_sc)
        if tmp_distance > new_distance:
            tmp_distance = new_distance
            sr, sc = tmp_sr, tmp_sc
        elif tmp_distance == new_distance and tmp_sr > sr:
            tmp_distance = new_distance
            sr, sc = tmp_sr, tmp_sc
        elif tmp_distance == new_distance and tmp_sr == sr and tmp_sc > sc:
            tmp_distance = new_distance
            sr, sc = tmp_sr, tmp_sc
    # 돌진하기
    tmp_distance = n * n
    for d in range(len(dr)):                    # O(8)
        nr, nc = rr + dr[d], rc + dc[d]
        if 0 <= nr < n and 0 <= nc < n:
            new_distance = distance(nr, sr, nc, sc)
            if tmp_distance > new_distance:
                tmp_distance = new_distance
                nrr, nrc, nrd = nr, nc, d

    return nrr, nrc, nrd


def catch_santa(r, c, d):
    # 만약 잡았다면
    if grid[r][c]:
        santa = grid[r][c]
        stun[santa] = 2
        grid[r][c] = 0
        santa_score[santa] += C
        nr, nc = r + (dr[d] * C), c + (dc[d] * C)
        # 격자 밖으로 나간 경우 탈락
        if not (0 <= nr < n and 0 <= nc < n):
            santa_list[santa - 1] = 0
        else:
            # 상호작용
            interaction(santa, nr, nc, d)


def catch_rudolph(r, c, d):
    if r == rr and c == rc:
        santa = grid[r][c]
        stun[santa] = 2
        grid[r][c] = 0
        santa_score[santa] += D
        nr, nc = r + dr[(d + 2) % 4] * D, c + dc[(d + 2) % 4] * D
        # 격자 밖으로 나간 경우 탈락
        if not (0 <= nr < n and 0 <= nc < n):
            santa_list[santa - 1] = 0
        else:
            # 상호작용
            interaction(santa, nr, nc, (d + 2) % 4)


def santa_move():
    for santa in santa_list:
        if not santa:
            continue
        r, c = santa
        if stun[grid[r][c]]:
            continue
        sr, sc, sd = -1, -1, -1
        tmp_distance = distance(r, rr, c, rc)
        flag = 0
        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc]:
                new_distance = distance(nr, rr, nc, rc)
                if tmp_distance > new_distance:
                    flag = 1
                    sr, sc, sd = nr, nc, d
                    tmp_distance = new_distance
        # 만약 가까워질 수 있는 길을 찾았다면,
        if flag:
            # 이동하기
            grid[sr][sc] = grid[r][c]
            grid[r][c] = 0
            santa_list[grid[sr][sc] - 1] = (sr, sc)

            # 2-2. 산타 충돌 확인하기
            catch_rudolph(sr, sc, sd)








# 0. init()
n, m, p, C, D = map(int, input().split())
rr, rc = map(int, input().split())
rr -= 1
rc -= 1
grid = [[0] * n for _ in range(n)]
santa_list = [(0, 0)] * p
stun = [0] * (p + 1)
for _ in range(p):
    pn, sr, sc = map(int, input().split())
    grid[sr - 1][sc - 1] = pn
    santa_list[pn - 1] = (sr - 1, sc - 1)
santa_score = defaultdict(int)


# 1. 게임 시작
for _ in range(m):
    # 1-1. 루돌프 움직임
    rr, rc, rd = rudolph_move()

    # 1-2. 산타를 잡았는지 확인
    catch_santa(rr, rc, rd)

    # 2-1. 산타 이동
    santa_move()

    # 3. 살아남은 산타들 점수 올리기
    gameover = 1
    for s in range(p):
        if santa_list[s]:
            santa_score[s + 1] += 1
            gameover = 0
    # 3-2. 모든 산타가 게임오버되었는지 확인
    if gameover:
        break

    # 4. 기절 풀기
    for i in range(1, len(stun)):
        if stun[i]:
            stun[i] -= 1



# 4. 점수 출력
ans = sorted(zip(santa_score.keys(), santa_score.values()), key=lambda x: x[0])
for i, j in ans:
    print(j, end=' ')