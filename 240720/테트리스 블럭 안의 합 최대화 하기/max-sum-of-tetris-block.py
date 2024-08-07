'''
테트로미노
테트리스 블럭 중 한 개를 적당히 올려 블럭이 놓인 칸 안에 숫자의 합이 최대가 될 때 결과를 출력

백트래킹

블럭만큼 이동할 수 있도록 좌표를 미리 세팅해두기 (0, 0) 기준

'''

import sys
input = sys.stdin.readline

blocks = [[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (1, 0), (2, 0), (3, 0)],
          [(0, 0), (0, 1), (1, 0), (1, 1)],
          [(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 1), (1, 1), (2, 1), (2, 0)], [(0, 0), (0, 1), (1, 0), (2, 0)], [(0, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (1, 1), (1, 2), (0, 2)], [(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 0), (1, 0), (1, 1), (1, 2)], [(0, 0), (1, 0), (0, 1), (0, 2)],
          [(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 1), (1, 1), (1, 0), (2, 0)], [(1, 0), (1, 1), (0, 1), (0, 2)], [(0, 0), (0, 1), (1, 1), (1, 2)],
          [(0, 1), (1, 0), (1, 1), (1, 2)], [(0, 0), (1, 0), (2, 0), (1, 1)], [(0, 0), (0, 1), (0, 2), (1, 1)], [(0, 1), (1, 1), (2, 1), (1, 0)]]

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

max_v = 0
for i in range(n):          # 200
    for j in range(m):      # 200
        for block in range(len(blocks)):     # 17
            tmp_v = 0
            for r, c in blocks[block]:  # 4
                nr, nc = r + i, c + j
                if not (0 <= nr < n and 0 <= nc < m):
                    break
                tmp_v += grid[nr][nc]
            else:
                max_v = max(max_v, tmp_v)

print(max_v)