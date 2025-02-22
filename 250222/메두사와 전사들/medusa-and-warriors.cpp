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

전사의 위치는 구조체로 생성해두기
전사 정보 : 위치, 스턴, 죽은 경우
*/

#include <iostream>
#include <cstring>
#include <queue>

using namespace std;

struct warrior {
	int r, c, stun, dead;
};

int n, m;
int medusa_r, medusa_c, end_r, end_c;
int medusa_grid[51][51];
pair<int, int> path[51][51];
int warrior_grid[51][51];
warrior warrior_list[301];

int sight[51][51];
int safe_zone[51][51];

int dr[4] = { -1, 1, 0, 0 };
int dc[4] = { 0, 0, -1, 1 };

int msr[4][3] = { {-1, -1, -1}, {1, 1, 1}, {-1, 0, 1}, {-1, 0, 1} };
int msc[4][3] = { {-1, 0, 1}, {-1, 0, 1}, {-1, -1, -1}, {1, 1, 1} };

bool isValid(int r, int c) {
	return 0 <= r && r < n && 0 <= c && c < n;
}

bool checkSight(int d, int wr, int wc, int r, int c) {
	switch (d) {
		// 상
	case 0:
		if ((wc < c && c <= medusa_c) || (c < wc && c >= medusa_c))
			return false;
		return true;
		// 하
	case 1:
		if ((wc < c && c <= medusa_c) || (c < wc && c >= medusa_c))
			return false;
		return true;
		// 좌
	case 2:
		if ((r > wr && r <= medusa_r) || (r < wr && r >= medusa_r))
			return false;
		return true;
		// 우
	case 3:
		if ((r > wr && r <= medusa_r) || (r < wr && r >= medusa_r))
			return false;
		return true;
	}
}


int get_distance(int r1, int c1, int r2, int c2) {
	return abs(r1 - r2) + abs(c1 - c2);
}


int find_path(int sr, int sc) {
	queue<pair<int, int>> q;
	q.push({ sr, sc });
	int visited[51][51] = { 0, };
	visited[sr][sc] = 1;

	pair<int, int> tmp_path[51][51];	// 이전에 왔던 경로를 저장
	int arrival = 0;

	while (!q.empty()) {
		int r = q.front().first, c = q.front().second;
		q.pop();

		for (int d = 0; d < 4; d++) {
			int nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && !visited[nr][nc] && !medusa_grid[nr][nc]) {
				tmp_path[nr][nc] = { r, c };
				if (nr == end_r && nc == end_c) {
					arrival = 1;
					break;
				}
				q.push({ nr, nc });
				visited[nr][nc] = 1;
			}
		}
		if (arrival)
			break;
	}

	if (!arrival)
		return 1;

	// 경로 생성
	int br, bc;
	int nr = end_r, nc = end_c;
	while (1) {
		br = tmp_path[nr][nc].first, bc = tmp_path[nr][nc].second;
		path[br][bc] = { nr, nc };
		nr = br;
		nc = bc;
		if (nr == medusa_r && nc == medusa_c)
			break;
	}

	return 0;
}


int init() {
	cin >> n >> m;
	cin >> medusa_r >> medusa_c >> end_r >> end_c;
	for (int i = 0; i < m; i++) {
		cin >> warrior_list[i].r >> warrior_list[i].c;
		warrior_grid[warrior_list[i].r][warrior_list[i].c]++;
	}
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			cin >> medusa_grid[i][j];
		}
	}

	// 0. 메두사 길 찾기
	if (find_path(medusa_r, medusa_c))
		return 0;
	return 1;
}



int get_sight() {
	// 준비물 : tmp sight 그리드, tmp safe zone 그리드 기절시킨 용사 수
	int tmp_sight[51][51];
	int tmp_safe_zone[51][51];
	int warrior_cnt = 0;

	for (int d = 0; d < 4; d++) {
		int tmp_warrior_cnt = 0;
		memset(tmp_sight, 0, sizeof(tmp_sight));
		memset(tmp_safe_zone, 0, sizeof(tmp_safe_zone));

		queue<pair<int, int>> q;
		q.push({ medusa_r, medusa_c });

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
							if (nr == medusa_r || nc == medusa_c) {
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
									if (isValid(nsr, nsc) && checkSight(d, nr, nc, nsr, nsc) && !tmp_safe_zone[nsr][nsc]) {
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

	// 돌로 변한 전사 찾기(맵에서 사라지는건 아님)
	int stone_man = 0;
	for (int i = 0; i < m; i++) {
		if (warrior_list[i].dead)
			continue;
		int r = warrior_list[i].r, c = warrior_list[i].c;
		if (sight[r][c] && !safe_zone[r][c]) {
			stone_man++;
			warrior_list[i].stun = 1;
		}
	}

	return stone_man;
}


pair<int, int> warrior_move() {
	int r, c, nr, nc, dist, new_dist, flag;
	int gr = -1, gc = -1;
	int braveman = 0, move = 0;
	for (int w = 0; w < m; w++) {
		// 죽은 애 continue
		if (warrior_list[w].dead)
			continue;
		// 스턴인 애는 풀어주고 continue
		if (warrior_list[w].stun) {
			warrior_list[w].stun = 0;
			continue;
		}

		// 나머지는 두 번 씩 이동하기
		r = warrior_list[w].r, c = warrior_list[w].c;

		dist = get_distance(r, c, medusa_r, medusa_c);
		new_dist = 2500;
		flag = 0;
		// 첫 번째 이동
		for (int d = 0; d < 4; d++) {
			nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && (!sight[nr][nc] || safe_zone[nr][nc])) {
				new_dist = get_distance(nr, nc, medusa_r, medusa_c);
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
			continue;
		}
		move++;
		// 메두사를 1트만에 잡은 경우 업데이트
		if (gr == medusa_r && gc == medusa_c) {
			warrior_list[w].dead = 1;
			braveman++;
			warrior_grid[warrior_list[w].r][warrior_list[w].c]--;	// 이전 위치 지워주기
			continue;
		}
		r = gr, c = gc;
		flag = 0;
		// 두번째 이동
		for (int d = 0; d < 4; d++) {
			nr = r + dr[(d + 4 + 2) % 4], nc = c + dc[(d + 4 + 2) % 4];
			if (isValid(nr, nc) && (!sight[nr][nc] || safe_zone[nr][nc])) {
				new_dist = get_distance(nr, nc, medusa_r, medusa_c);
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
			warrior_grid[warrior_list[w].r][warrior_list[w].c]--;	// 이전 위치 지워주기
			warrior_list[w].r = r, warrior_list[w].c = c;
			warrior_grid[r][c]++;
			continue;
		}
		move++;
		// 메두사를 2트만에 잡은 경우 업데이트
		if (gr == medusa_r && gc == medusa_c) {
			warrior_list[w].dead = 1;
			braveman++;
			warrior_grid[warrior_list[w].r][warrior_list[w].c]--;	// 이전 위치 지워주기
			continue;
		}
		// 모두 움직인 경우
		warrior_grid[warrior_list[w].r][warrior_list[w].c]--;	// 이전 위치 지워주기
		warrior_list[w].r = gr, warrior_list[w].c = gc;
		warrior_grid[gr][gc]++;
	}

	return { move, braveman };
}


void simulation() {
	int next_r, next_c;
	int total_move, stone_man, real_warriors;

	while (1) {
		// 0. 변수 초기화
		total_move = 0, stone_man = 0, real_warriors = 0;

		// 1. 메두사 이동
		int next_r = path[medusa_r][medusa_c].first, next_c = path[medusa_r][medusa_c].second;
		medusa_r = next_r, medusa_c = next_c;
		// 1-2. 메두사 도착 여부 확인
		if (medusa_r == end_r && medusa_c == end_c) {
			cout << 0 << '\n';
			break;
		}
		// 1-3. 사라지는 전사 찾기 
		for (int i = 0; i < m; i++) {
			if (warrior_list[i].r == medusa_r && warrior_list[i].c == medusa_c)
				warrior_list[i].dead = 1;
		}
		warrior_grid[medusa_r][medusa_c] = 0;


		// 2. 메두사 바라보기
		stone_man = get_sight();

		// 3. 용사 이동
		pair<int, int> val = warrior_move();
		total_move = val.first, real_warriors = val.second;

		// 4. 결과 출력
		cout << total_move << ' ' << stone_man << ' ' << real_warriors << '\n';

	}

}


int main() {
	int game_start = init();
	if (!game_start) {
		cout << -1 << '\n';
	}
	else {
		simulation();
	}
}