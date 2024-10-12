'''
19:03

4 x 4
1. 몬스터 복제 시도
    - 현재 위치에서 자신과 같은 방향을 가진 몬스터를 복제하려 함
    - 이놈들은 한 턴이 지나고 복제된다
2. 몬스터 이동
    - 자신이 가진 방향대로 한 칸 이동
    - 움직이려는 칸에 몬스터 시체가 있거나 팩맨이 있는 경우 반시계 방향으로 회전 후 판단
    - 8방향 다 돌았는데도 이동이 불가능하면 움직이지 않는다.
3. 팩맨 이동
    - 총 3칸 이동
    - 몬스터를 가장 많이 먹을 수 있는 방향으로 움직인다.
    - 상좌하우 우선순위를 갖는다.
4. 몬스터 소멸
    - 몬스터 시체는 2턴동안 유지된다.
5. 몬스터 복제 완성
    - 알형태였던 몬스터 부화

살아남은 몬스터 마리수 출력하기

풀이:
4 x 4
몬스터 복제는 무한으로 일어난다.
필요한 정보 :
1. 현재 격자에서 방향 별 몬스터 마리수 저장한 그리드
2. 새로 태어나는 몬스터 그리드
3. 죽은 몬스터 그리드

'''

dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, -1, -1, -1, 0, 1, 1, 1]
n = 4
d_len = 8
grid = [[[0] * d_len for _ in range(n)] for _ in range(n)]
egg_grid = [[[0] * d_len for _ in range(n)] for _ in range(n)]
dead = [[0] * n for _ in range(n)]
packman_path = []


def get_eggs():
    global egg_grid
    for i in range(n):
        for j in range(n):
            for d in range(d_len):
                egg_grid[i][j][d] = grid[i][j][d]


def monster_move():
    new_grid = [[[0] * d_len for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for d in range(d_len):
                if grid[i][j][d]:
                    for turn in range(d_len):
                        nd = (d + turn) % d_len
                        ni, nj = i + dr[nd], j + dc[nd]
                        if 0 <= ni < n and 0 <= nj < n and (ni, nj) != packman and not dead[ni][nj]:
                            new_grid[ni][nj][nd] += grid[i][j][d]
                            break
                    else:
                        new_grid[i][j][d] += grid[i][j][d]

    return new_grid


def packman_move(depth, r, c, catch, path):
    global max_catch, packman_path, packman
    if depth == 3:
        if catch > max_catch:
            max_catch = catch
            packman_path = path[:]
            packman = (r, c)
        return
    for d in range(0, d_len, 2):
        nr, nc = r + dr[d], c + dc[d]
        if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in path:
            packman_move(depth + 1, nr, nc, catch + sum(grid[nr][nc]), path + [(nr, nc)])


m, t = map(int, input().split())
pr, pc = tuple(map(int, input().split()))
packman = (pr - 1, pc - 1)
for _ in range(m):
    r, c, d = map(int, input().split())
    grid[r - 1][c - 1][d - 1] += 1

# 게임시작
for _ in range(t):
    max_catch = -1
    packman_path = []

    # 1. 팩맨 알 낳기
    get_eggs()

    # 2. 몬스터 이동
    grid = monster_move()

    # 3. 팩맨 이동
    packman_move(0, packman[0], packman[1], 0, [])

    # 4. 먹어치운 애들 죽이기
    for r, c in packman_path:
        grid[r][c] = [0] * d_len
        dead[r][c] = 3

    # 5. 죽은 애들 시체 업데이트
    for i in range(n):
        for j in range(n):
            if dead[i][j]:
                dead[i][j] -= 1

    # 6. 새로운 친구들 태어나기
    for i in range(n):
        for j in range(n):
            for d in range(d_len):
                grid[i][j][d] += egg_grid[i][j][d]

# 남아있는 애들 출력
ans = 0
for i in range(n):
    for j in range(n):
        ans += sum(grid[i][j])
print(ans)