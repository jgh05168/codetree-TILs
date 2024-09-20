from collections import deque
import sys
input = sys.stdin.readline

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

def rotate(sr, sc):
    global relics, min_rotate, get_relics_list
    copy_grid = [row[:] for row in grid]  # 얕은 복사
    tmp_grid = [[0] * n for _ in range(n)]
    
    for r in range(3):
        for i in range(sr, sr + 3):
            for j in range(sc, sc + 3):
                oi, oj = i - sr, j - sc
                ni, nj = oj, 3 - oi - 1
                tmp_grid[ni + sr][nj + sc] = copy_grid[i][j]
        
        if not r:
            for i in range(n):
                for j in range(n):
                    if not tmp_grid[i][j]:
                        tmp_grid[i][j] = grid[i][j]

        visited = [[0] * n for _ in range(n)]
        tmp_relics = []
        for i in range(n):
            for j in range(n):
                if not visited[i][j]:
                    tmp_relics.extend(get_relics(i, j, visited, tmp_grid[i][j], tmp_grid))

        if len(tmp_relics) > relics:
            relics = len(tmp_relics)
            min_rotate = r
            for i in range(n):
                for j in range(n):
                    new_grid[i][j] = tmp_grid[i][j]
            get_relics_list = tmp_relics[:]
        elif len(tmp_relics) == relics and r < min_rotate:
            min_rotate = r
            for i in range(n):
                for j in range(n):
                    new_grid[i][j] = tmp_grid[i][j]
            get_relics_list = tmp_relics[:]

        copy_grid = [row[:] for row in tmp_grid]  # 얕은 복사


def get_relics(sr, sc, visited, num, grid):
    queue = deque([(sr, sc)])
    visited[sr][sc] = 1
    tmp = [(sr, sc)]
    while queue:
        r, c = queue.popleft()

        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] == num:
                queue.append((nr, nc))
                visited[nr][nc] = 1
                tmp.append((nr, nc))

    if len(tmp) > 2:
        return tmp
    else:
        return []


k, m = map(int, input().split())
n = 5
grid = [list(map(int, input().split())) for _ in range(n)]
piece_list = deque(list(map(int, input().split())))

for _ in range(k):
    ans = 0

    new_grid = [[0] * n for _ in range(n)]
    relics = 0
    min_rotate = 4
    get_relics_list = []
    for j in range(n - 2):
        for i in range(n - 2):
            rotate(i, j)

    get_relics_list.sort(key=lambda x: (x[1], -x[0]))
    for r, c in get_relics_list:
        new_piece = piece_list.popleft()
        new_grid[r][c] = new_piece

    ans += relics

    while True:
        visited = [[0] * n for _ in range(n)]
        tmp_relics = []
        for i in range(n):
            for j in range(n):
                if not visited[i][j]:
                    tmp_relics.extend(get_relics(i, j, visited, new_grid[i][j], new_grid))
        if not tmp_relics:
            break

        ans += len(tmp_relics)

        tmp_relics.sort(key=lambda x: (x[1], -x[0]))
        for r, c in tmp_relics:
            new_piece = piece_list.popleft()
            new_grid[r][c] = new_piece

    if not ans:
        break
    print(ans, end=' ')
    grid = [row[:] for row in new_grid]  # 얕은 복사