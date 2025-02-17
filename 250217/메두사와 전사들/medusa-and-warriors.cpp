/*
n x n
도로 : 0, 도로가 아닌 곳 : 1
메두사는 오직 도로만을 따라 최단 경로로 공원까지 이동함

M명의 전사들은 메두사를 향해 최단경로로 이동함. 어느 칸이든지 이동 가능함(맨해튼거리 써서 가장 가까운 곳으로 이동 가능)

[메두사]
도로를 따라 한 칸 이동, 최단경로를 따른다.
메두사가 이동한 칸에 전사가 있을 경우, 전사는 사라진다.
여러 최단경로가 가능하다면, 상하좌우의 우선순위를 따른다.
집으로부터 공원까지 경로가 없을 수도 있음

[메두사의 시선]
상하좌우 하나의 방향을 선택해 바라본다.
바라보는 방향으로 90도의 시야각을 가지며, 시야각 범위 전사를 볼 수 있음
다른 전사에 가려진 전사의 경우, 보이지 않음
전사가 동일한 방향으로 바라본 범위에 포함된 모든 칸은 메두사하넽 보이지 않음(그림 참조)
메두사가 본 전사들은 모두 돌로 변해 현재 턴에는 움직일 수 없음
해당 칸 전사들 모두 돌로 변함
메두사는 전사를 가장 많이 볼 수 있는 방향을 바라봄
	상하좌우 우선순위

[전사 이동] 
최대 두 칸까지 이동
이동중 칸 공유 가능
메두사의 시야에 들어오는 곳으로는 이동 불가능
1. 상하좌우 우선순위로 거리를 줄일 수 있음
2. 좌우상하 우선순위로 한 번 더 이동

[전사 공격]
전사는 메두사를 공격하고 사라진다.

모든 전사가 이동한 거리의 합 , 돌이 된 전사의 수, 공격한 전사의 수 출력
메두사가 도착하면 0 출력 후 끝

풀이 : 
메두사 이동 : BFS로 사전에 경로를 찾아둔다.
메두사 시야 : 2개의 2차원 배열을 사용. sight, safe_zone
	sight가 0이거나 sight면서 safe_zone이 1인 경우에만 생존
	sight : 상하좌우로 메두사 시야를 방향벡터 제공 -> bfs로 맵 생성하기 
	safe_zone : sight 중 사람을 만나면 재귀 bfs 들어가기
전사 이동 : 맨해튼거리로 계산

*/

#include <iostream>
#include <queue>
#include <cstring>
#include <vector>

using namespace std;


int n, m;
int grid[51][51];
int warrior_grid[51][51];
pair<int, int> medusa_route[51][51];
pair<int, int> warriors[301];
int stun[301] = { 0, };
int deadman[301] = { 0, };
int mr, mc, end_r, end_c;

int visited[51][51];
int sight[51][51];
int safe_zone[51][51];

int dr[4] = { -1, 1, 0, 0 };
int dc[4] = { 0, 0, -1, 1 };

int msr[4][3] = { {-1, -1, -1}, {1, 1, 1}, {-1, 0, 1}, {-1, 0, 1} };
int msc[4][3] = { {-1, 0, 1}, {-1, 0, 1}, {-1, -1, -1}, {1, 1, 1} };


bool isValid(int r, int c) {
	return 0 <= r && r < n && 0 <= c && c < n;
}


bool checkSight(int d, int mr, int mc, int wr, int wc, int sr, int sc) {
	switch (d) {
	// 상
	case 0:
		if ((sc > wc && sc <= mc) || (sc < wc && sc >= mc) )
			return false;
		return true;
	// 하
	case 1:
		if ((sc > wc && sc <= mc) || (sc < wc && sc >= mc))
			return false;
		return true;
	// 좌
	case 2:
		if ((sr > wr && sr <= mr) || (sr < wr && sr >= mr))
			return false;
		return true;
	// 우
	case 3:
		if ((sr > wr && sr <= mr) || (sr < wr && sr >= mr))
			return false;
		return true;
	}
}


int get_distance(int r1, int c1, int r2, int c2) {
	return abs(r1 - r2) + abs(c1 - c2);
}


int shortest_path(int sr, int sc) {
	queue<pair<int, int>> q;
	memset(visited, 0, sizeof(visited));
	q.push({ sr, sc });
	visited[sr][sc] = 1;
	int flag = 0;
	int r, c, nr, nc;

	while (!q.empty()) {
		r = q.front().first;
		c = q.front().second;
		q.pop();

		for (int d = 3; d >= 0; d--) {
			nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && !visited[nr][nc] && !grid[nr][nc]) {
				medusa_route[nr][nc] = { r, c };
				if (nr == mr && nc == mc) {
					return 1;
				}
				q.push({ nr, nc });
				visited[nr][nc] = 1;
			}
		}
	}
	return 0;
}


int init() {
	cin >> n >> m;
	cin >> mr >> mc >> end_r >> end_c;
	int mr, mc;
	for (int i = 0; i < m; i++) {
		cin >> mr >> mc;
		warrior_grid[mr][mc] += 1;
		warriors[i] = { mr, mc };
	}
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++)
			cin >> grid[i][j];
	}

	// 0. 메두사 최단경로 찾기
	int flag = 0;
	flag = shortest_path(end_r, end_c);

	return flag;

}


int get_sight(int sr, int sc) {
	// 준비물 : tmp sight 그리드, tmp safe zone 그리드 기절시킨 용사 수
	int tmp_sight[51][51];
	int tmp_safe_zone[51][51];
	int warrior_cnt = 0;

	for (int d = 0; d < 4; d++) {
		int tmp_warrior_cnt = 0;
		memset(tmp_sight, 0, sizeof(tmp_sight));
		memset(tmp_safe_zone, 0, sizeof(tmp_safe_zone));

		queue<pair<int, int>> q;
		q.push({ sr, sc });

		while (!q.empty()) {
			int r = q.front().first, c = q.front().second;
			q.pop();

			for (int nd = 0; nd < 3; nd++) {
				int nr = r + msr[d][nd], nc = c + msc[d][nd];
				if (isValid(nr, nc) && !tmp_sight[nr][nc] && !tmp_safe_zone[nr][nc]) {
					// 첫 워리어를 발견한 경우
					if (warrior_grid[nr][nc]) {
						tmp_warrior_cnt += warrior_grid[nr][nc];
						// 새로운 tmp_safe_zone 생성
						queue<pair<int, int>> safe_queue;
						safe_queue.push({ nr, nc });
						int safe_r, safe_c, nsr, nsc;

						while (!safe_queue.empty()) {
							safe_r = safe_queue.front().first, safe_c = safe_queue.front().second;
							safe_queue.pop();

							// 동일 선상일 경우
							if (nr == sr || nc == sc) {
								nsr = safe_r + msr[d][1], nsc = safe_c + msc[d][1];
								if (isValid(nsr, nsc) && !tmp_safe_zone[nsr][nsc]) {
									safe_queue.push({ nsr, nsc });
									tmp_safe_zone[nsr][nsc] = 1;
								}
							}
							else {
								// 방향별로 나눠서 가능 여부 판단하기
								for (int sd = 0; sd < 3; sd++) {
									nsr = safe_r + msr[d][sd], nsc = safe_c + msc[d][sd];
									if (isValid(nsr, nsc) && checkSight(d, sr, sc, nr, nc, nsr, nsc) && !tmp_safe_zone[nsr][nsc]) {
										safe_queue.push({ nsr, nsc });
										tmp_safe_zone[nsr][nsc] = 1;
									}
								}
							}
						}
					}
					q.push({ nr, nc });
					tmp_sight[nr][nc] = 1;
				}
			}
		}
		// 모든 경우 완료하고 업데이트만을 기다리는 상황
		if (warrior_cnt < tmp_warrior_cnt) {
			// 맵 업데이트
			warrior_cnt = tmp_warrior_cnt;
			for (int i = 0; i < n; i++) {
				for (int j = 0; j < n; j++) {
					sight[i][j] = tmp_sight[i][j];
					safe_zone[i][j] = tmp_safe_zone[i][j];
				}
			}
		}
	}

	// 돌로 변한 전사 찾기 
	int stone_man = 0;
	for (int i = 0; i < m; i++) {
		if (deadman[i])
			continue;
		int r = warriors[i].first, c = warriors[i].second;
		if (sight[r][c] && !safe_zone[r][c]) {
			stone_man++;
			stun[i] = 1;
		}
	}

	return stone_man;
}


pair<int, int> warrior_move(int mr, int mc) {
	int r, c, nr, nc, dist, new_dist, flag;
	int gr = -1, gc = -1;
	int braveman = 0, move = 0;
	for (int w = 0; w < m; w++) {
		// 기절하거나 사라진 녀석은 continue
		if (stun[w] || deadman[w])
			continue;

		// 나머지는 두 번 씩 이동하기
		r = warriors[w].first, c = warriors[w].second;
		warrior_grid[r][c]--;

		dist = get_distance(r, c, mr, mc);
		new_dist = 2500;
		flag = 0;
		// 첫 번째 이동
		for (int d = 0; d < 4; d++) {
			nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && (!sight[nr][nc] || safe_zone[nr][nc])) {
				new_dist = get_distance(nr, nc, mr, mc);
				if (new_dist < dist) {
					gr = nr;
					gc = nc;
					dist = new_dist;
					flag = 1;
				}
			}
		}
		// 못움직인 경우, continue
		if (!flag) {
			warrior_grid[r][c]++;
			warriors[w] = { r, c };
			continue;
		}
		move++;
		// 메두사를 1트만에 잡은 경우 업데이트
		if (gr == mr && gc == mc) {
			deadman[w] = 1;
			braveman++;
			continue;
		}
		r = gr, c = gc;
		flag = 0;
		// 두번째 이동

		for (int d = 0; d < 4; d++) {
			nr = r + dr[(d + 4 + 2) % 4], nc = c + dc[(d + 4 + 2) % 4];
			if (isValid(nr, nc) && (!sight[nr][nc] || safe_zone[nr][nc])) {
				new_dist = get_distance(nr, nc, mr, mc);
				if (new_dist < dist) {
					gr = nr;
					gc = nc;
					dist = new_dist;
					flag = 1;
				}
			}
		}
		// 못움직인 경우, continue
		if (!flag) {
			warrior_grid[r][c]++;
			warriors[w] = { r, c };
			continue;
		}
		move++;
		// 메두사를 2트만에 잡은 경우 업데이트
		if (gr == mr && gc == mc) {
			deadman[w] = 1;
			braveman++;
			continue;
		}
		// 모두 움직인 경우
		warrior_grid[gr][gc]++;
		warriors[w] = { gr, gc };
	}

	return { move, braveman };
}


void simulation() {
	int nmr, nmc;
	int total_move, stone_man, real_warriors;
	while (1) {
		// 0. 변수 초기화
		total_move = 0, stone_man = 0, real_warriors = 0;
		memset(stun, 0, sizeof(stun));

		// 1. 메두사 이동
		nmr = medusa_route[mr][mc].first, nmc = medusa_route[mr][mc].second;
		// 1-2. 메두사 도착 여부 확인
		if (nmr == end_r && nmc == end_c) {
			cout << 0 << '\n';
			break;
		}
		// 1-3. 사라지는 전사 찾기 
		for (int i = 0; i < m; i++) {
			if (warriors[i].first == nmr && warriors[i].second == nmc) 
				deadman[i] = 1;
		}
		warrior_grid[nmr][nmc] = 0;

		// 2. 메두사 바라보기
		stone_man = get_sight(nmr, nmc);

		// 3. 용사 이동
		pair<int, int> val = warrior_move(nmr, nmc);
		total_move = val.first, real_warriors = val.second;

		// 4. 결과 출력
		cout << total_move << ' ' << stone_man << ' ' << real_warriors << '\n';

		// 5. 위치 업데이트
		mr = nmr, mc = nmc;
	}
}


int main() {
	int game_start = 0;
	game_start = init();
	
	if (!game_start)
		cout << -1 << '\n';
	else
		simulation();

	
	return 0;
}