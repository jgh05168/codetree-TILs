'''
13:53

l x l
기사의 크기는 사각형

[기사 이동]
- 상하좌우 중 한 칸으로 이동ㄱㅏ능
- 이동하는 칸에 기사가 존재한다면, 연쇄적으로 같이 이동
- 기사가 이동하려는 방향의 끝에 벽이 존재한다면, 모든 기사는 이동 불가능
- 사라진 기사는 명령을 받을 수 없음

[대결 데미지]
- 밀려난 기사들은 피해를 입게 된다.
    - 해당 기사가 이동한 곳에서 w x h 직사각형 내에 놓여있는 함정의 수만큼 피해를 입게 된다.
- 현재 체력 이상의 데미지를 받은 기사는 죽는다
- 명령을 받은 기사는 피해를 입지 않고, 기사들은 모두 밀린 뒤 피해를 입는다.
- 밀렸더라도, 밀쳐진 위치에 함정이 없다면 피해를 입지 않는다.

생존한 기사들이 받는 총 데미지의 합 출력

풀이:
벽 구분 방법 : 한 칸 더 이동하려는 방향에 벽이 존재한다면 이동 불가능
충돌 기사 찾는 방법 : 내가 아니라 다른 기사인 경우, 이동 방향에 위치하는지 확인하는 조건 추가
'''

from collections import deque, defaultdict

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

n, m, q = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
soldier_grid = [[0] * n for _ in range(n)]
soldier_hp = [0]
damage_sum = [0]
soldier_list = [0]
move_loc = []


def find_soldier(soldier, order):
    sr, sc = soldier_list[soldier]
    queue = deque()
    queue.append((sr, sc))
    visited = [[0] * n for _ in range(n)]
    visited[sr][sc] = 1
    tmp_move = [(soldier, sr, sc)]

    while queue:
        r, c = queue.popleft()
        soldier = soldier_grid[r][c]

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            # 만약 밀려나는 방향으로 확인인데, 벽이 있다면 종료
            if d == order and (not (0 <= nr < n and 0 <= nc < n) or grid[nr][nc] == 2):
                return []
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                # 만약 같은 녀석이라면
                if soldier_grid[nr][nc] == soldier:
                    queue.append((nr, nc))
                    visited[nr][nc] = 1
                    tmp_move.append((soldier, nr, nc))
                # 만약 밀쳐지는 녀석이라면 추가하기
                elif soldier_grid[nr][nc] and d == order:
                    queue.append((nr, nc))
                    visited[nr][nc] = 1
                    tmp_move.append((soldier_grid[nr][nc], nr, nc))

    return tmp_move



# init()
for i in range(1, m + 1):
    r, c, h, w, k = map(int, input().split())
    soldier_list.append((r - 1, c - 1))
    for ni in range(h):
        for nj in range(w):
            soldier_grid[ni + r - 1][nj + c - 1] = i
    soldier_hp.append(k)
    damage_sum.append(0)

# 게임 시작

for _ in range(q):
    soldier, order = map(int, input().split())
    check_update = [0] * (q + 1)
    # 0. 이미 죽은 기사면, 이어가기
    if not soldier_list[soldier]:
        continue
    # 1. 기사 찾기
    move_loc = find_soldier(soldier, order)

    # 밀쳐지는지 안밀쳐지는지 가능여부 체크
    if not move_loc:
        continue
    else:
        cur_soldiers_loc = [[] * (q + 1) for _ in range(q + 1)]
        for _, r, c in move_loc:
            soldier_grid[r][c] = 0
        for sol, r, c in move_loc:
            nr, nc = r + dr[order], c + dc[order]
            soldier_grid[nr][nc] = sol
            # 밀쳐진 기사들은 현재 위치에 데미지를 입는지 확인해야함
            if sol != soldier:
                if not check_update[sol]:
                    check_update[sol] = 1
                    soldier_list[sol] = (nr, nc)
                cur_soldiers_loc[sol].append((nr, nc))

    # 2. 대결 데미지 입기
    for sol in range(len(cur_soldiers_loc)):
        if not cur_soldiers_loc[sol]:
            continue
        dead = 0
        for r, c in cur_soldiers_loc[sol]:
            if soldier_hp[sol] and grid[r][c] == 1:
                soldier_hp[sol] -= 1
                damage_sum[sol] += 1
            # 만약 병사 죽었다면,
            if not soldier_hp[sol]:
                dead = 1
                break
        if dead:
            for r, c in cur_soldiers_loc[sol]:
                soldier_grid[r][c] = 0
                soldier_list[sol] = 0

ans = 0
for i in range(1, q + 1):
    if soldier_hp[i]:
        ans += damage_sum[i]
print(ans)