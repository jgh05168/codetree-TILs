'''
15:20

4 x 4 상하좌우대각선

1. 몬스터 복제 시도 : 현재 위치에서 자신과 같은 방향을 가진 몬스터 복제
    - 부화된 몬스터는 움직이지 못함
2. 몬스터 이동 : 현재 자신이 가진 방향대로 한 칸 이동
    - 움직이려는 칸에 몬스터 시체가 있거나, 팩맨이 있는 경우, 격자를 벗어나는 경우, 반시계 방향으로 45도 회전 후 판단
    - 8방향 다 봤는데도 움직일 수 없다면 움직이지 않는다.
    - 몬스터는 한번에 같이 이동한다
3. 팩맨 이동 : 총 세 칸을 이동한다.
    - 상좌하우 총 세 칸씩 이동 가능하다.
    - 격자 밖을 나가는 경우는 고려 x
    - 팩맨의 알은 먹지 않으며, 움직이기 전에 함께 있던 몬스터도 먹지 않는다.
4. 몬스터 시체 소멸 : 몬스터의 시체는 2턴동안 유지.
5. 몬스터 복제 완성 : 알 형태였던 몬스터 부화. (현재 그리드에 append)해주기

필요 grid : 몬스터
알은 1차원 배열로 지정하여 업데이트해주기
팩맨은 dfs로 이동시키며 최적의 루트 찾기 ( 전역변수로 설정해주기 )

'''

#     상     좌     하    우
dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, -1, -1, -1, 0, 1, 1, 1]

n = 4
grid = [[[] * n for _ in range(n)] for _ in range(n)]
egg_list = []
packman_move = []
packman = tuple()
dead = [[0] * n for _ in range(n)]
visited = []
monster_list = []


def get_eggs():
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                for d in grid[i][j]:
                    egg_list.append((i, j, d))
                    monster_list.append((i, j, d))


def monster_move():
    new_grid = [[[] * n for _ in range(n)] for _ in range(n)]
    for r, c, d in monster_list:
        for turn in range(len(dr)):
            nd = (d + turn) % 8
            nr, nc = r + dr[nd], c + dc[nd]
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) != packman and not dead[nr][nc]:
                new_grid[nr][nc].append(nd)
                break
        else:
            new_grid[r][c].append(d)
    return new_grid


def dfs(depth, r, c, catch, visited_loc):
    global max_catch, packman_move, packman
    if depth == 3:
        if max_catch < catch:
            packman_move = visited_loc[:]
            max_catch = catch
            packman = (r, c)
        return
    for d in range(0, len(dr), 2):
        nr, nc = r + dr[d], c + dc[d]
        if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
            visited[nr][nc] = 1
            dfs(depth + 1, nr, nc, catch + len(grid[nr][nc]), visited_loc + [(nr, nc)])
            visited[nr][nc] = 0



m, t = map(int, input().split())
ir, ic = map(int, input().split())
packman = (ir - 1, ic - 1)
for _ in range(m):
    ir, ic, id = map(int, input().split())
    grid[ir - 1][ic - 1].append(id - 1)

for _ in range(t):

    # 1. 알낳기
    monster_list = []
    egg_list = []
    get_eggs()

    # 2. 몬스터 이동
    grid = monster_move()

    # 3. 팩맨 이동
    max_catch = 0
    visited = [[0] * n for _ in range(n)]
    dfs(0, packman[0], packman[1], 0, [])       # depth, catch, visited

    # 4. 몬스터 죽이기
    for r, c in packman_move:
        if grid[r][c]:
            grid[r][c] = []
            dead[r][c] = 2 + 1

    # 5. 몬스터 시체 소멸
    for r in range(n):
        for c in range(n):
            if dead[r][c]:
                dead[r][c] -= 1

    # 6. 알 깨어나기
    for r, c, d in egg_list:
        grid[r][c].append(d)

ans = 0
for i in range(n):
    for j in range(n):
        ans += len(grid[i][j])
print(ans)