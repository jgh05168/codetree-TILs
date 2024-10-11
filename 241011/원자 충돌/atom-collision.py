'''
18:15
m개의 원자 : 질량, 방향, 속력, 초기위치(1 ~ n)
방향 : 상하좌우 대각선
격자의 모든 행, 열은 끝과끝이 연결되어있음

1. 모든 원자는 1초가 지날 때마다 자신의 방향으로 자신의 속력만큼 이동한다.
    - 동시에 이동
2. 이동이 모두 끝난 뒤에 칸에 2개 이상의 원자가 있는 경우 합성 발생
    - 같은 칸의 원자들은 각각의 질량과 속력을 모두 합한 하나의 원자로 합쳐진다
    - 이후 합쳐진 원자는 4개의 원자로 나눠진다
    - 나눠진 원자들은 해당 칸에 위치함.
        - 질량 : 합쳐진 원자의 질량 // 5
        - 속력 : 합쳐진 원자의 속력 // 합쳐진 원자의 개수
        - 방향 : 합쳐진 원자들의 방향이 십자/대각선 중 하나면 십자로 4개, 아니라면 대각선으로 4개
        - 질량이 0인 원소는 소멸
    - 이동과정중 원자가 만나는 것은 합성이 아님

k초 지났을 때, 남앙있는 원자 질량 합
'''

dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, 1, 1, 1, 0, -1, -1, -1]
grid = []


def atom_move():
    new_grid = [[[] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                # 아톰 하나만 존재하는 경우
                if len(grid[i][j]) == 1:
                    m, s, d = grid[i][j].pop()
                    ni, nj = (i + dr[d] * s) % n, (j + dc[d] * s) % n
                    new_grid[ni][nj].append((m, s, d))
                # 여러개 존재하는 경우
                else:
                    while grid[i][j]:
                        m, s, d = grid[i][j].pop()
                        ni, nj = (i + dr[d] * s) % n, (j + dc[d] * s) % n
                        new_grid[ni][nj].append((m, s, d))
    return new_grid


def check_atom():
    new_grid = [[[] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                # 아톰 하나만 존재하는 경우
                if len(grid[i][j]) == 1:
                    new_grid[i][j] = grid[i][j]
                # 여러개 존재하는 경우
                else:
                    total_m = 0
                    total_s = 0
                    total_d = [0, 0]
                    atom_num = len(grid[i][j])
                    while grid[i][j]:
                        m, s, d = grid[i][j].pop()
                        total_m += m
                        total_s += s
                        total_d[d % 2] = 1
                    nm = total_m // 5
                    # 원자가 0인 경우 소멸
                    if not nm:
                        continue
                    ns = total_s // atom_num
                    if sum(total_d) == 1:
                        for d in range(0, len(dr), 2):
                            new_grid[i][j].append((nm, ns, d))
                    else:
                        for d in range(1, len(dr), 2):
                            new_grid[i][j].append((nm, ns, d))
    return new_grid





n, m, k = map(int, input().split())
grid = [[[] for _ in range(n)] for _ in range(n)]
for _ in range(m):
    x, y, mm, s, d = map(int, input().split())
    grid[x - 1][y - 1].append((mm, s, d))

# 게임시작
for _ in range(k):
    # 1. 모든 아톰 이동
    grid = atom_move()

    # 2. 겹치는 아톰 있는지 확인
    grid = check_atom()

# 3. 남아있는 원자들 질량 합 출력
ans = 0
for i in range(n):
    for j in range(n):
        if grid[i][j]:
            for m, _, _ in grid[i][j]:
                ans += m
print(ans)