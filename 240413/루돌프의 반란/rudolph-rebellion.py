'''
코드트리: 루돌프의 반란

[게임판]
- 게임은 총 m개의 턴에 걸쳐 진행. 매 턴마다 루돌프와 산타들이 한 번씩 움직인다.
- 루돌프가 한 번 움직인 뒤 1번 산타부터 순차적으로 움직인다.
    - 기절해있거나 격자 밖으로 빠져나간 산타는 continue
- 게임판에서 두 칸 사이 거리는 맨해튼거리로 계산

[루돌프]
- 루돌프는 가장 가까운 산타를 향해 한 칸 돌진(8칸 가능) -> 루돌프와 산타들의 위치를 for문 돌며 계산
- 가까운 산타가 2명 이상일 경우 r이 큰 산타, r이 동일하다면 c가 큰 산타로 돌진

[산타]
- 산타는 루돌프에게 거리가 가까워지는 방향으로 한 칸 이동
- 다른 산타가 있는 칸으로는 움직일 수 없음
- 움직일 수 있더라도 루돌프와 가까워질 방법이 없다면 이동 x
- 상 우 하 좌 순으로 이동

[충돌]
- 루돌프가 움직여서 충돌이 일어난 경우, 해당 산타는 c만큼 점수를 얻게 됨
    -> 산타 점수 dictionary 사용
    - 이와 동시에 루돌프가 이동해온 방향으로 c칸 만큼 밀려남
        -> 산타 위치는 전역변수 사용
- 산타가 움직여서 충돌이 난 경우, d만큼의 점수를 얻게 된다.
    - 자신의 이동 반대방향으로 d칸만큼 밀려남
- 이동 도중에는 충돌이 일어나지 않고 쭉 이동 가능
- 만약에 이동한 칸에 다른 산타가 있으면 상호작용 발생

[상호작용]
- 굴러온 돌이 박힌 돌 뺴낸다.
-> 현재 이동 중인 방향으로 한 칸씩 밀려남 -> 만약 격자 밖으로 나가는 산타가 있으면 게임 탈락

[기절]
- 한 턴 기절. -> 기절 dict 사용
- 기절 도중 충돌이나 상호작용으로 인해 밀려날 수는 있다.
- 기절한 산타를 돌진 대상으로 선택할 수 있음

[게임 종료]
- p명의 산타 모두 게임 탈락이라면 그 게임은 즉시 종료
- 매 턴 이후 아직 탈락하지 않은 산타들에게는 1점씩 추가 부여

출력 : 각 산타가 얻은 최종 점수

풀이:
필요 변수 : 루돌프 방향, 산타 방향, 산타 점수 dict, 산타 기절 배열
루돌프의 이동 : 나이트처럼 산타한테 다가갈 경우, 대각선으로 우선 이동.
다른 산타가 있는 칸으로는 이동 x에 유의하기
산타는 턴을 돌면서 루돌프와 본인의 예측 이동 위치값에 대해 계산 수행. 한 칸 이동

산타 배열을 따로 두기(시뮬레이션)

루돌프가 이동하며 동일한 경우, heapq에 산타 배열 저장, 산타발견 flag 지정
루돌프가 한 번만 이동해서 잡을 수 있는 경우를 판단해야 한다.
-> 아닌 경우 자신의 예측 이동과 산타의 거리를 계산하여 이동 위치값과 함께 heapq에 저장. 이후 이동

굳이 bfs를 사용하지 않아도 된다.
'''

import sys, heapq, math
input = sys.stdin.readline

#             5  6  7  3  9   1  12  11
rudolph_dr = [1, 1, 1, 0, 0, -1, -1, -1]
rudolph_dc = [1, 0, -1, 1, -1, 1, 0, -1]
#           상  우 하  좌
santa_dr = [-1, 0, 1, 0]
santa_dc = [0, 1, 0, -1]


def interaction(row, col, d, first_santa, order):
    # 일단 밀고 시작하기
    wait_santa = santa_grid[row][col]
    santa_locs[first_santa] = [row, col]
    santa_grid[row][col] = first_santa
    while True:
        # 밀린 뒤 다음 위치부터 체크해보기
        if order == 1:
            nrow, ncol = row + rudolph_dr[d], col + rudolph_dc[d]
        else:
            nrow, ncol = row + santa_dr[d], col + santa_dc[d]
        if 0 <= nrow < N and 0 <= ncol < N:
            # 산타가 멈출 수 있는 경우라면
            if not santa_grid[nrow][ncol]:
                # 밀린 산타의 값만 업데이트 해 주면 된다.
                santa_grid[nrow][ncol] = wait_santa
                santa_locs[wait_santa] = [nrow, ncol]
                break
            # 아니라면 새로운 산타를 위해서 값 재설정이 필요하다
            else:
                # 일단 밀린 곳 위치의 산타 값 빼기
                tmp_santa = santa_grid[nrow][ncol]
                # 밀린 산타 값 업데이트
                santa_grid[nrow][ncol] = wait_santa
                santa_locs[wait_santa] = [nrow, ncol]
                wait_santa = tmp_santa
                row, col = nrow, ncol
        # 산타가 격자 밖으로 밀려난다면,
        else:
            santa_alive[wait_santa] = 0
            break


def collision(santa, d, order):        # 산타 번호, direction
    if order == 1:
        santa_points[santa] += C
        santa_r, santa_c = santa_locs[santa][0], santa_locs[santa][1]
        santa_num = santa_grid[santa_r][santa_c]
        santa_grid[santa_r][santa_c] = 0
        # 일단 밀려나보기
        santa_r, santa_c = santa_r + rudolph_dr[d] * C, santa_c + rudolph_dc[d] * C
        # 만약 격자 밖이라면,
        if not (0 <= santa_r < N and 0 <= santa_c < N):
            santa_alive[santa_num] = 0
        # 만약 도착 위치에 다른 산타가 있다면,
        elif santa_grid[santa_r][santa_c]:
            interaction(santa_r, santa_c, d, santa_num, 1)
        else:
            santa_grid[santa_r][santa_c] = santa_num
            santa_locs[santa_num] = [santa_r, santa_c]
    else:
        santa_points[santa] += D
        santa_r, santa_c = santa_locs[santa][0], santa_locs[santa][1]
        santa_num = santa_grid[santa_r][santa_c]
        santa_grid[santa_r][santa_c] = 0
        # 산타 위치를 루돌프와 박은 뒤이기 때문에 루돌프의 위치로 설정
        santa_r, santa_c = rudolph[0], rudolph[1]
        # 일단 밀려나보기
        santa_r, santa_c = santa_r + santa_dr[d] * D, santa_c + santa_dc[d] * D
        # 만약 격자 밖이라면,
        if not (0 <= santa_r < N and 0 <= santa_c < N):
            santa_alive[santa_num] = 0
        # 만약 도착 위치에 다른 산타가 있다면,
        elif santa_grid[santa_r][santa_c]:
            interaction(santa_r, santa_c, d, santa_num, 2)
        else:
            santa_grid[santa_r][santa_c] = santa_num
            santa_locs[santa_num] = [santa_r, santa_c]



def rudolph_move():
    global rudolph
    # 우선 여덟 방향 돌면서 잡을 수 있는 산타가 존재하는지 확인
    for d in range(8):
        nrr, nrc = rudolph[0] + rudolph_dr[d], rudolph[1] + rudolph_dc[d]
        if 0 <= nrr < N and 0 <= nrc < N:
            # 만약 잡을 수 있다면(r, c 큰 순서대로 탐색했으므로 한 번 찾으면 바로 break 해도 된다.
            if santa_grid[nrr][nrc]:
                santa_down[santa_grid[nrr][nrc]] = 1
                cur_santa_down[santa_grid[nrr][nrc]] = 1
                collision(santa_grid[nrr][nrc], d, 1)
                rudolph = [nrr, nrc]
                break
    # 잡을 산타가 없으면
    else:
        # 산타의 위치를 순회하면서 가장 가까운 산타 찾기
        santa_pq = []
        for santa_idx in range(1, P + 1):
            # 산타 탈락이라면 continue
            if not santa_alive[santa_idx]:
                continue
            # 산타와 루돌프 사이 거리 구하기
            rudolph_r, rudolph_c = rudolph
            santa_r, santa_c = santa_locs[santa_idx]
            calc_dir = math.pow(rudolph_r - santa_r, 2) + math.pow(rudolph_c - santa_c, 2)
            heapq.heappush(santa_pq, (calc_dir, -santa_r, -santa_c))
        # 루돌프 이동
        # 4분면으로 나누어서 이동하기
        _, dest_r, dest_c = heapq.heappop(santa_pq)
        dest_r, dest_c = -dest_r, -dest_c
        # 1사분면
        if rudolph_r > dest_r and rudolph_c < dest_c:
            rudolph = [rudolph_r - 1, rudolph_c + 1]
        # 2사분면
        elif rudolph_r > dest_r and rudolph_c > dest_c:
            rudolph = [rudolph_r - 1, rudolph_c - 1]
        # 3사분면
        elif rudolph_r < dest_r and rudolph_c > dest_c:
            rudolph = [rudolph_r + 1, rudolph_c - 1]
        # 4사분면
        elif rudolph_r < dest_r and rudolph_c < dest_c:
            rudolph = [rudolph_r + 1, rudolph_c + 1]
        # 90도
        elif rudolph_r > dest_r and rudolph_c == dest_c:
            rudolph = [rudolph_r - 1, rudolph_c]
        # 180도
        elif rudolph_r == dest_r and rudolph_c > dest_c:
            rudolph = [rudolph_r, rudolph_c - 1]
        # 270도
        elif rudolph_r < dest_r and rudolph_c == dest_c:
            rudolph = [rudolph_r + 1, rudolph_c]
        # 0도
        else:
            rudolph = [rudolph_r, rudolph_c + 1]


def santa_move(santa_num):
    # 산타의 예상 위치에 루돌프가 존재하는지 확인
    santa_r, santa_c = santa_locs[santa_num][0], santa_locs[santa_num][1]
    for d in range(4):
        nsr, nsc = santa_r + santa_dr[d], santa_c + santa_dc[d]
        # 루돌프를 잡은 경우
        if nsr == rudolph[0] and nsc == rudolph[1]:
            santa_down[santa_num] = 1
            cur_santa_down[santa_num] = 1
            collision(santa_num, (d + 2) % 4, 2)        # 반대방향으로 이동해야 함
            break
    # 못잡은 경우
    else:
        santa_pq = []
        # 4방향 돌아보면서 산타와 루돌프 간 최단거리를 구해보기
        # 현재 산타 위치와 루돌프 위치 구해두기
        cur_dir = math.pow(santa_r - rudolph[0], 2) + math.pow(santa_c - rudolph[1], 2)
        for d in range(4):
            nsr, nsc = santa_r + santa_dr[d], santa_c + santa_dc[d]
            if 0 <= nsr < N and 0 <= nsc < N:
                if santa_grid[nsr][nsc]:
                    continue
                calc_dir = math.pow(nsr - rudolph[0], 2) + math.pow(nsc - rudolph[1], 2)
                # 현재 거리보다 계산한 거리가 더 크다면 continue
                if cur_dir < calc_dir:
                    continue
                heapq.heappush(santa_pq, (calc_dir, d))
        # 이동할 위치가 없다면
        if santa_pq:
            _, cur_d = heapq.heappop(santa_pq)
            nsr, nsc = santa_r + santa_dr[cur_d], santa_c + santa_dc[cur_d]
            santa_locs[santa_num] = [nsr, nsc]
            santa_grid[nsr][nsc] = santa_num
            santa_grid[santa_r][santa_c] = 0




N, M, P, C, D = map(int, input().split())
rudolph_sr, rudolph_sc = map(int, input().split())
rudolph = [rudolph_sr - 1, rudolph_sc - 1]
santa_grid = [[0] * N for _ in range(N)]
santa_points = {0: 0}
santa_down = [0] * (P + 1)
cur_santa_down = [0] * (P + 1)
santa_alive = [1] * (P + 1)
santa_locs = [[-1, -1] for _ in range(P + 1)]
for _ in range(P):
    sn, sr, sc = map(int, input().split())
    santa_locs[sn] = [sr - 1, sc - 1]
    santa_grid[sr - 1][sc - 1] = sn
    santa_points.update({sn: 0})

for _ in range(M):
    # 0. 한 턴 기다린 산타들 down 풀어주기
    # 1. 루돌프부터 이동
    rudolph_move()
    # 2. 산타 이동
    for idx in range(1, P + 1):
        # 산타가 탈락했거나 기절한 경우 움직이지 못함
        if not santa_alive[idx] or cur_santa_down[idx]:
            continue
        if santa_down[idx] and not cur_santa_down[idx]:
            santa_down[idx] = 0
            continue
        santa_move(idx)
    # 3. 살아남은 산타들 점수 + 1
    for idx in range(1, P + 1):
        if santa_alive[idx]:
            santa_points[idx] += 1
        cur_santa_down[idx] = 0

for idx in range(1, P + 1):
    print(santa_points[idx], end=" ")