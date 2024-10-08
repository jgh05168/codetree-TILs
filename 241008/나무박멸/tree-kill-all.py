'''
17:06

제초제
- k범위만큼 대각선으로 퍼진다
- 벽이 있는 경우 가로막혀 전파되지 않는다.

1. 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 성장한다
    - 모든 나무에서 동시에 일어난다.
2. 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식 진행
    - 각 칸의 나무 그루 수 // 번식 가능 카느이 개수
    - 모든 나무에서 동시에 일어난다.
3. 각 칸 중 나무가 가장 많이 박멸되는 칸에 제초제를 뿌린다.
    - 나무가 있는 칸에 뿌리기
    - 전파되는 도중, 벽이 있거나 나무가 없는 칸인 경우 그 칸까지는 뿌려지고 그 뒤로는 안뿌려진다.
    - 제초제가 뿌려진 칸에는 c만큼 남아있고, c + 1년째 사라진다.
    - 다시 제초제가 뿌려지는 경우 c년동안 유지된다.
'''

dr = [0, 1, 0, -1, 1, 1, -1, -1]
dc = [1, 0, -1, 0, 1, -1, -1, 1]


def growup():
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                tmp = 0
                for d in range(4):
                    ni, nj = i + dr[d], j + dc[d]
                    if 0 <= ni < n and 0 <= nj < n and grid[ni][nj] > 0:
                        tmp += 1
                grid[i][j] += tmp


def spread():
    new_grid = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if grid[r][c] > 0:

                can_spread = 0
                for d in range(4):
                    nr, nc = r + dr[d], c + dc[d]
                    if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc] and not dead[nr][nc]:
                        can_spread += 1
                if can_spread:
                    for d in range(4):
                        nr, nc = r + dr[d], c + dc[d]
                        if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc] and not dead[nr][nc]:
                            new_grid[nr][nc] += grid[r][c] // can_spread
            if not new_grid[r][c]:
                new_grid[r][c] = grid[r][c]

    return new_grid


def kill_tree(r, c, test=1):
    kill_tree = grid[r][c]
    if not test:
        dead[r][c] = C + 1
        grid[r][c] = 0
    for d in range(4, len(dr)):
        for power in range(1, k + 1):
            nr, nc = r + dr[d] * power, c + dc[d] * power
            if 0 <= nr < n and 0 <= nc < n:
                kill_tree += grid[nr][nc]
                if not test:
                    dead[nr][nc] = C + 1
                    if grid[nr][nc] <= 0:
                        kill_tree -= grid[nr][nc]
                        break
                    grid[nr][nc] = 0
                # 만약 나무가 없거나 벽이거나, 제초제가 뿌려진 칸이였다면, 종료
                else:
                    if dead[nr][nc]:
                        break
                    if grid[nr][nc] <= 0:
                        kill_tree -= grid[nr][nc]
                        break

    return kill_tree


n, m, k, C = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
dead = [[0] * n for _ in range(n)]

ans = 0
for _ in range(m):
    # 1. 나무 성장시키기
    growup()

    # 2. 번식 진행
    grid = spread()

    # 3. 제초제 뿌리기
    kill = 0
    kr, kc = -1, -1
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                tmp_kill = kill_tree(i, j)
                if tmp_kill > kill:
                    kill = tmp_kill
                    kr, kc = i, j

    # 4. 가장 많이 죽는 곳에 제초제 뿌리기
    if (kr, kc) != (-1, -1):
        ans += kill_tree(kr, kc, 0)

    # 5. 제초제 년수 줄이기
    for i in range(n):
        for j in range(n):
            if dead[i][j] > 0:
                dead[i][j] -= 1

print(ans)