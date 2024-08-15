'''
L x L, 빈칸 함정 벽

1. 기사 이동
    - 상하좌우 중 한 칸으로 이동
    - 이동하려는 위치에 기사가 존재한다면, 한 칸 씩 밀리게 된다.
    - 이동 방향의 끝에 벽이 존재한다면, 모든 기사는 이동 불가능
    - 체스판에서 사라진 기사는 아무 반응 x
2. 대결 데미지
    - 다른 기사를 밀치게 되면, 피해를 입는다.
    - 해당 기사가 이동한 곳에서 w x h 내에 놓여 있는 함정의 수만큼 피해를 입음
    - 현재 체력 이상의 데미지를 받은 경우, 체스판에서 사라짐
    - 밀렸더라도 밀쳐진 위치에 함정이 전혀 없다면, 피해를 입지 않음

풀이:
0. init
기사의 위치 정보 업데이트 (40 x 40)

1. 기사 이동
밀고자 하는 기사의 방향에 다른 기사가 있는지 체크
    만약 다른 기사가 존재한다면, 같이 밀어줘야 하는 놈에 포함

기사 위치는 dict로 주어지게 한다. dict(list) 안에 튜플로 위치 저장
이후 한 칸 씩 방향별로 업데이트 해주기
    new_list 생성해서 새로운 위치 저장
    만약 벽을 만난다면, 이동 불가능, 이전의 위치 그대로 다시 가져오기
'''

from collections import deque, defaultdict
import sys
input = sys.stdin.readline

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

def can_move(slist, d, sknight):
    queue = deque(slist)
    can_move_list = set()
    can_move_list.add(sknight)

    # 벽을 만난 순간, 움직이지 못함을 의미
    while queue:
        r, c = queue.popleft()

        nr, nc = r + dr[d], c + dc[d]
        # 다음 위치는 범ㅇ위 안에 있거나 벽을 만나면 안된다.
        if not (0 <= nr < L and 0 <= nc < L) or board[nr][nc] == 2:
            return []
        # 같은 녀석들인 경우, 이미 큐에 다 들어가 있으므로 continue
        if k_board[nr][nc] in can_move_list:
            continue
        # 다른 녀석들이 존재하는 경우, 큐에 저장
        if k_board[nr][nc] > 0:
            queue.extend(knight_dict[k_board[nr][nc]])
            can_move_list.add(k_board[nr][nc])

    return list(can_move_list)


def move_knights(can_move_list, d):
    # 보드 업데이트 & 딕셔너리 업데이트
    new_board = [[0] * L for _ in range(L)]
    for i in range(L):
        for j in range(L):
            if k_board[i][j] not in can_move_list:
                new_board[i][j] = k_board[i][j]

    for k in can_move_list:
        new_loc = []
        while knight_dict[k]:
            r, c = knight_dict[k].pop()
            nr, nc = r + dr[d], c + dc[d]
            new_board[nr][nc] = k
            new_loc.append((nr, nc))
        knight_dict[k] = new_loc

    return new_board


def get_damage(attacker, move_man):
    for i in range(L):
        for j in range(L):
            if k_board[i][j] in move_man and board[i][j] == 1:
                if k_board[i][j] == attacker:
                    continue
                knight_hp[k_board[i][j]] -= 1
                knight_damage[k_board[i][j]] += 1
                # 만약 죽었을 경우, 위치 초기화
                if knight_hp[k_board[i][j]] <= 0:
                    for r, c in knight_dict[k_board[i][j]]:
                        k_board[r][c] = 0


L, N, Q = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(L)]
knight_dict = defaultdict(list)
knight_hp = defaultdict(int)
knight_damage = defaultdict(int)
for k_idx in range(1, N + 1):
    knight_damage[k_idx] = 0
    r, c, h, w, k = map(int, input().split())
    knight_hp[k_idx] = k
    for sr in range(r - 1, r - 1 + h):
        for sc in range(c - 1, c - 1 + w):
            knight_dict[k_idx].append((sr, sc))

# 초기 기사 위치 설정 30 x 40 x 40
k_board = [[0] * L for _ in range(L)]
for k_idx in knight_dict.keys():
    if not knight_hp[k_idx]:
        continue
    for i in range(len(knight_dict[k_idx])):
        k_board[knight_dict[k_idx][i][0]][knight_dict[k_idx][i][1]] = k_idx
# 게임 시작
move_list = []
for _ in range(Q):
    knight, d = map(int, input().split())
    
    # 0. 이미 죽은 녀석이면 continue
    if not knight_hp[knight]:
        continue
        
    # 1. 기사와 붙어있는 녀석들 찾기
    move_list = can_move(knight_dict[knight], d, knight)

    # 2. 붙은 녀석들 한 칸씩 움직여주기
    if move_list:
        k_board = move_knights(move_list, d)

        # 3. 이동했을 때, 점수 산정하기
        get_damage(knight, move_list)

# 데미지 출력
ans = 0
for alive_man in range(1, N + 1):
    if knight_hp[alive_man] > 0:
        ans += knight_damage[alive_man]

print(ans)