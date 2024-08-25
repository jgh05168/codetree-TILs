DIR_NUM = 4
EMPTY = (401, 401)
EMPTY_NUM = 401

# 변수 선언 및 입력:
n, m, k = tuple(map(int, input().split()))
given_map = [
    list(map(int, input().split()))
    for _ in range(n)
]
next_dir = [
    [
        [0 for _ in range(DIR_NUM)]
        for _ in range(DIR_NUM)
    ]
    for _ in range(m + 1)
]

player = [
    [EMPTY for _ in range(n)]
    for _ in range(n)
]
next_player = [
    [EMPTY for _ in range(n)]
    for _ in range(n)
]

contract = [
    [EMPTY for _ in range(n)]
    for _ in range(n)
]

elapsed_time = 0


def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n


def can_go(x, y, target_num):
    if not in_range(x, y):
        return False
    
    # target 번호와 contract 번호가 일치한 
    # 경우에만 이동이 가능합니다.
    contract_num, _ = contract[x][y]
    return contract_num == target_num


def next_pos(x, y, curr_dir):
    dxs, dys = [-1, 1, 0, 0], [0, 0, -1, 1]
    num, _ = player[x][y]

    # Case 1.
    # 먼저 독점계약을 맺지 않은 공간이 있다면 
    # 우선순위에 따라 그곳으로 이동합니다.
    for move_dir in next_dir[num][curr_dir]:
        nx, ny = x + dxs[move_dir], y + dys[move_dir]
        
        if can_go(nx, ny, EMPTY_NUM):
            return (nx, ny, move_dir)
    
    # Case 2.
    # 인접한 곳이 모두 독점계약을 맺은 곳이라면
    # 우선순위에 따라 그 중 본인이 독점계약한 땅으로 이동합니다.
    for move_dir in next_dir[num][curr_dir]:
        nx, ny = x + dxs[move_dir], y + dys[move_dir]
        
        if can_go(nx, ny, num):
            return (nx, ny, move_dir)


# (x, y) 위치에 새로운 플레이어가 들어왔을 때 갱신을 진행합니다.
def update(x, y, new_player):
    # 새로 들어온 플레이어가 더 우선순위가 높을 경우에만
    # (x, y)위치에 해당 플레이어가 위치하게 됩니다.
    # Tip.
    # Empty인 위치에서는 항상 update가 되게끔
    # 미리 Empty의 num 값에 401를 셋팅해놨습니다.
    if next_player[x][y] > new_player:
        next_player[x][y] = new_player


def move(x, y):
    num, curr_dir = player[x][y]
    
    # Step1. 현재 플레이어의 다음 위치와 방향을 구합니다.
    nx, ny, move_dir = next_pos(x, y, curr_dir)
    
    # Step2. 플레이어를 옮겨줍니다.
    update(nx, ny, (num, move_dir))


def dec_contract(x, y):
    num, remaining_period = contract[x][y]
    
    # 남은 기간이 1이면 다시 Empty가 됩니다.
    if remaining_period == 1:
        contract[x][y] = EMPTY
    # 그렇지 않다면 기간이 1 줄어듭니다.
    else:
        contract[x][y] = (num, remaining_period - 1)


def add_contract(x, y):
    num, _ = player[x][y];
    contract[x][y] = (num, k)


def simulate():
    # Step1. next_player를 초기화합니다.
    for i in range(n):
        for j in range(n):
            next_player[i][j] = EMPTY
    
    # Step2. 각 플레이어들을 한 칸씩 움직여줍니다.
    for i in range(n):
        for j in range(n):
            if player[i][j] != EMPTY:
                move(i, j)

    # Step3. next_grid 값을 grid로 옮겨줍니다.
    for i in range(n):
        for j in range(n):
            player[i][j] = next_player[i][j]
    
    # Step4. 남은 contract기간을 1씩 감소시킵니다.
    for i in range(n):
        for j in range(n):
            if contract[i][j] != EMPTY:
                dec_contract(i, j)
    
    # Step5. 새로운 contract를 갱신해줍니다.
    for i in range(n):
        for j in range(n):
            if player[i][j] != EMPTY:
                add_contract(i, j)


def end():
    if elapsed_time >= 1000:
        return True
    
    for i in range(n):
        for j in range(n):
            if player[i][j] == EMPTY:
                continue
            
            num, _ = player[i][j]
            
            if num != 1:
                return False
    
    return True


# 플레이어 마다 초기 방향을 입력받아 설정해줍니다.
init_dirs = list(map(int, input().split()))
for num, move_dir in enumerate(init_dirs, start=1):
    for i in range(n):
        for j in range(n):
            if given_map[i][j] == num:
                player[i][j] = (num, move_dir - 1)
                contract[i][j] = (num, k)


# 플레이어 마다 방향 우선순위를 설정합니다.
for num in range(1, m + 1):
    for curr_dir in range(DIR_NUM):
        dirs = list(map(int, input().split()))
        for i, move_dir in enumerate(dirs):
            next_dir[num][curr_dir][i] = move_dir - 1

# 시간이 1000이 넘지 않고
# 1번이 아닌 플레이어가 남아 있다면
# 계속 시뮬레이션을 반복합니다.
while not end():
    simulate()
    elapsed_time += 1

if elapsed_time >= 1000:
    elapsed_time = -1

print(elapsed_time)