'''
[맵]
북쪽을 통해서 들어올 수 있음
[골렘]
- 골렘은 십자모양을 갖고 있음
- 중앙을 제외한 나머지 칸은 골렘의 출구
- i번째로 숲을 탐색하는 골렘은 숲의 가장 북쪽에서 시작해 골렘의 중앙이 c열이 되도록 하는 위치에서 내려온다
이동 우선순위
1. 남쪽으로 한 칸 내려온다
    - 아래 칸들이 비어있을 때 내려올 수 있음
2. 1의 방법이 불가능하면 서쪽 방향으로 회전한 뒤 내려간다
3. 동짝 방향으로 회전하며 내려간다.

- 골렘이 이동할 수 있는 가장 남쪽에 도달해 더이상 이동이 불가능하면 정령이 이동한다
    - 만약 현재 위치하는 골렘의 출구가 다른 골렘과 인접하다면, 해당 출구를 통해 이동 가능
정령의 최종 위치를 누적한 값을 출력하기

- 골렘이 격자 내부에 존재하지 않는다면, 격자를 텅 빈 상태로 만들고
    - 다음 골렘이 탐색을 시작함
    - 정령이 도달하는 최종 위치를 답에 포함시키지 않음

70 x 70
'''

from collections import deque, defaultdict
import sys
input = sys.stdin.readline

#     북  동  남  서
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

down = [(1, -1), (2, 0), (1, 1)]
left = [(-1, -1), (0, -2), (1, -1), (1, -2), (2, -1)]
right = [(-1, 1), (0, 2), (1, 1), (1, 2), (2, 1)]


def golem_move(golem, r, c):      # 골렘 중앙을 인자로 받기
    # 골렘 한 칸 내리기
    while True:
        flag = 0
        # 아래로 한 칸 내리기
        for ndr, ndc in down:
            nr, nc = r + ndr, c + ndc
            # 만약 머가 있다면 break
            if not (0 <= nr < n and 0 <= nc < m) or grid[nr][nc]:
                break
        else:
            # 내려갈 수 있다는 뜻이므로 한 칸 이동하고 continue
            r, c = r + dr[2], c + dc[2]
            continue
        # 왼쪽으로 한 칸 돌리기
        for ndr, ndc in left:
            nr, nc = r + ndr, c + ndc
            # 만약 머가 있다면 break
            if not (0 <= nr < n and 0 <= nc < m) or grid[nr][nc]:
                break
        else:
            # 내려갈 수 있다는 뜻이므로 한 칸 이동하고 continue
            r, c = r + 1, c - 1
            golem_dir[golem] = (golem_dir[golem] - 1) % 4
            continue
        # 오른쪽으로 한 칸 돌리기
        for ndr, ndc in right:
            nr, nc = r + ndr, c + ndc
            # 만약 머가 있다면 break
            if not (0 <= nr < n and 0 <= nc < m) or grid[nr][nc]:
                break
        else:
            # 내려갈 수 있다는 뜻이므로 한 칸 이동하고 continue
            r, c = r + 1, c + 1
            golem_dir[golem] = (golem_dir[golem] + 1) % 4
            continue

        # 다 못돌리는 경우 빠져나오기
        break

    # 만약 골렘이 이동하지 못한다면 이동불가 판정 후 비워주기
    if r < 3:
        return True, -1, -1
    # 현재 위치에 대해 골렘 생성하기
    grid[r][c] = golem
    for d in range(len(dr)):
        nr, nc = r + dr[d], c + dc[d]
        grid[nr][nc] = golem
        if d == golem_dir[golem]:
            golem_exit[golem] = (nr, nc)
    return False, r, c


def bfs(sr, sc):
    queue = deque([(sr, sc)])
    visited = [[0] * m for _ in range(n)]
    visited[sr][sc] = 1
    tmp = sr

    while queue:
        r, c = queue.popleft()
        golem = grid[r][c]

        for d in range(len(dr)):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and grid[nr][nc] > 0:
                if golem == grid[nr][nc] or (r, c) == golem_exit[golem]:
                    queue.append((nr, nc))
                    visited[nr][nc] = 1
                    tmp = max(tmp, nr)

    return tmp - 2


n, m, k = map(int, input().split())
n += 3
grid = [[0] * m for _ in range(n)]

ans = 0
golem_dir = defaultdict(int)
golem_exit = defaultdict(tuple)
for golem in range(1, k + 1):
    c, d = map(int, input().split())

    # 0. 골렘 생성
    golem_dir[golem] = d

    # 1. 골렘 이동
    clean_map, r, c = golem_move(golem, 1, c - 1)
    
    # 2-1. 만약 골렘이 이동 불가능한 경우, 맵 비워주기
    if clean_map:
        grid = [[0] * m for _ in range(n)]
    # 2-2. 정령 이동시키기
    else:
        ans += bfs(r, c)

print(ans)