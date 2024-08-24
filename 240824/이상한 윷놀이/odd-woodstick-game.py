'''
n x n, 흰, 빨, 파 중 하나의 색을 갖고 있다.
1 ~ k번까지 번호가 지정되어 있고, 이동 방향도 미리 정해져 있다.
1 ~ k번까지 순서대로 움직인다.
1. 흰색 칸
    - 해당 칸으로 이동
    - 이동하려는 칸에 이미 말이 있는 경우, 해당 말 위에 이동하려던 말을 올려둔다.
    - 이미 말이 올려져 있는 상태에서도 올릴 수 있다.
2. 빨간 칸
    - 해당 칸으로 이동하기 전 말의 순서를 뒤집는다.
    - 이후 해당 칸에 말이 있는 경우에는, 흰색 칸과 같이 그 위에 쌓아둔다.
3. 파란 칸
    - 이동하지 않고, 반대로 방향을 전환한 뒤 이동
        - 이동하려는 말만 방향을 바꾼다
    - 만약 반대 방향도 파란색이라면 반대로 전환한 뒤 이동 금지
- 격자판을 벗어나는 경우, 파란색 이동과 똑같이 생각한다.
- 쌓여있는 말을 이동하는 경우, 본인 위에 있는 말과 함께 이동한다. (그치만 개별적으로 이동은 해야 함)

종료 : 말이 4개 이상 겹치는 경우가 생기는 경우

풀이 :
n <= 12
말을 쌓아놓을 땐 순차적으로 쌓아둔다.
- 그치만 순서대로 있을 것이란 보장이 없음
- 인덱스를 저장해 둔 다음, 슬라이딩 윈도우로 빼내기 ?
나머지는 deque로 저장한 다음 이동해보기
'''

from collections import deque
import sys
input = sys.stdin.readline

dr = [0, 0, -1, 1]
dc = [1, -1, 0, 0]
rev_d = {0: 1, 1: 0, 2: 3, 3: 2}


def player_move():
    for p in range(1, m + 1):
        dontmove = False
        if not players[p]:
            continue
        r, c, d, idx = players[p]
        nr, nc = r + dr[d], c + dc[d]
        # 범위 벗어났거나, 파란색인 경우
        if not (0 <= nr < n and 0 <= nc < n) or color[nr][nc] == 2:
            nr, nc = r + dr[rev_d[d]], c + dc[rev_d[d]]
            # 한 번 더 같은 상황이라면, 자리에 가만히 있기
            if not (0 <= nr < n and 0 <= nc < n) or color[nr][nc] == 2:
                players[p] = (r, c, rev_d[d], idx)
                dontmove = True
            else:
                bef_len = len(grid[nr][nc])
                tmp_players = grid[r][c][idx:]
                if color[nr][nc] == 1:
                    tmp_players.reverse()
                    n_idx = 0
                    for np in tmp_players:
                        _, _, pd, pidx = players[np]
                        if np == p:
                            players[np] = (nr, nc, rev_d[d], bef_len + n_idx)
                        else:
                            players[np] = (nr, nc, pd, bef_len + n_idx)
                        n_idx += 1
                    grid[nr][nc].extend(tmp_players)
                else:
                    grid[nr][nc].extend(tmp_players)
                    for i in range(len(tmp_players)):
                        np = tmp_players[i]
                        _, _, pd, pidx = players[np]
                        if np == p:
                            players[np] = (nr, nc, rev_d[d], bef_len + i)
                        else:
                            players[np] = (nr, nc, pd, bef_len + i)
                # 인자 정리
                for i in range(len(grid[r][c]) - 1, idx - 1, -1):
                    grid[r][c].pop()
        # 빨간색인 경우
        else:
            bef_len = len(grid[nr][nc])
            tmp_players = grid[r][c][idx:]
            if color[nr][nc] == 1:
                tmp_players.reverse()
                n_idx = 0
                for np in tmp_players:
                    _, _, pd, pidx = players[np]
                    players[np] = (nr, nc, pd, bef_len + n_idx)
                    n_idx += 1
                grid[nr][nc].extend(tmp_players)
            else:
                grid[nr][nc].extend(tmp_players)
                for i in range(len(tmp_players)):
                    np = tmp_players[i]
                    _, _, pd, pidx = players[np]
                    players[np] = (nr, nc, pd, bef_len + i)
            # 인자 정리
            for i in range(len(grid[r][c]) - 1, idx - 1, -1):
                grid[r][c].pop()

        if not dontmove and len(grid[nr][nc]) >= 4:
            print(ans)
            exit()


n, m = map(int, input().split())
color = [list(map(int, input().split())) for _ in range(n)]
grid = [[[] * n for _ in range(n)] for _ in range(n)]
players = [0]
for i in range(1, m + 1):
    sx, sy, sd = map(int, input().split())
    players.append((sx - 1, sy - 1, sd - 1, 0))
    grid[sx - 1][sy - 1].append(i)

ans = 1
while ans <= 1000:
    # 1. 플레이어 움직이기
    player_move()

    ans += 1

print(-1)