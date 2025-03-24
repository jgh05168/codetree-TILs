/*
14:30 시작

코드트리 빵을 사고싶다 ~!!

m명의 사람은 각자 m분에 베이스캠프에서 출발하여 편의점으로 이동함
사람들은 출발시간이 되기 전에는 격자 밖에 존재함 & 목표 편의점은 모두 다르다.
n x n 크기 격자 위에서 진행됨

1. 본인이 가고싶은 편의점 방향을 향해 한 칸 움직인다
	- 최단거리로 이동(상하좌우 인접한 칸 중 최소 이동 가능 횟수
	- 상 좌 우 하 우선순위
2. 편의점에 도착한다면, 해당 편의점에서 멈추고 다른 사람들은 해당 편의점 칸을 지날 수 없다.
	- 격자에 있는 모든 사람들이 지나간 뒤 해당 칸을 지날 수 없게 된다.
3. t <= m을 만족한다면, t번 사람은 자신의 도착지와 가장 가까운 베이스캠프에 들어감
	- 행이 작은 순 & 열이 작은 순으로 들어감
	- 베이스캠프에 들어가는 데는 시간이 소요되지 않음
	- 이때부터 해당 베이스캠프가 있는 칸을 지날 수 없음

모든 사람들이 몇 분 후에 도착하는지 구하자.

풀이 : BFS
- 시간이 늘어날수록 최단경로는 바뀐다. == 사람이 움직일때마다 BFS 진행
- 필요 정보 : grid, visited, person 구조체

*/

#include <iostream>
#include <cstring>
#include <queue>
#include <algorithm>

using namespace std;

struct person {
	int sr, sc, er, ec, arrive;
};

int n, m;
int grid[16][16] = { 0, };
int basecamp[16][16];
int visited[16][16];
pair<int, int> path[31][16][16];
pair<int, int> tmp_path[16][16];
person people[31];

int dr[4] = { -1, 0, 0, 1 };
int dc[4] = { 0, -1, 1, 0 };


bool isValid(int r, int c) {
	return 0 <= r && r < n && 0 <= c && c < n;
}


void init() {
	cin >> n >> m;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++)
			cin >> basecamp[i][j];
	}
	for (int i = 0; i < m; i++) {
		cin >> people[i].er >> people[i].ec;
		people[i].er--, people[i].ec--;
		people[i].sr = -1, people[i].sc = -1;
	}
}


pair<int, int> move_people(int time) {
	int change = 0;
	int arrive_cnt = 0;
	int idx = min(time, m);
	for (int i = 0; i < idx; i++) {
		if (people[i].arrive)
			continue;

		int nr = path[i][people[i].sr][people[i].sc].first;
		int nc = path[i][people[i].sr][people[i].sc].second;
		people[i].sr = nr;
		people[i].sc = nc;
		// 2. 편의점에 도착했는지 확인
		if (people[i].sr == people[i].er && people[i].sc == people[i].ec) {
			change = 1;
			arrive_cnt++;
			people[i].arrive = 1;
			grid[people[i].sr][people[i].sc] = 1;
		}
	}

	return { change, arrive_cnt };
}


void update_people(int idx) {
	memset(visited, 0, sizeof(visited));
	queue < pair<int, int>> q;
	visited[people[idx].er][people[idx].ec] = 1;
	q.push({ people[idx].er , people[idx].ec });
	int move = 150000, er = 31, ec = 31;

	while (!q.empty()) {
		int r = q.front().first, c = q.front().second;
		q.pop();

		for (int d = 0; d < 4; d++) {
			int nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && !visited[nr][nc] && !grid[nr][nc]) {
				int new_cost = visited[r][c] + 1;
				// 최단거리 베이스캠프가 아닌 경우 continue
				if (new_cost > move)
					continue;
				// 베이스캠프를 찾은 경우
				if (basecamp[nr][nc]) {
					if (new_cost < move) {
						move = new_cost;
						er = nr;
						ec = nc;
					}
					else if (new_cost == move) {
						if (nr < er) {
							er = nr;
							ec = nc;
						}
						else if (nr == er) {
							if (nc < ec) {
								er = nr;
								ec = nc;
							}
						}
					}
				}
				q.push({ nr, nc });
				visited[nr][nc] = new_cost;
			}
		}
	}

	// 베이스캠프 찾은 뒤, 좌표 업데이트 및 이동 차단
	people[idx].sr = er;
	people[idx].sc = ec;
	grid[er][ec] = 1;
}


void make_path(int idx) {
	int sr = people[idx].sr, sc = people[idx].sc;
	memset(visited, -1, sizeof(visited));
	memset(tmp_path, 0, sizeof(tmp_path));
	queue < pair<int, int>> q;
	visited[sr][sc] = 0;
	q.push({ sr, sc });

	while (!q.empty()) {
		int r = q.front().first, c = q.front().second;
		q.pop();

		// 편의점 찾았다면 바로 종료
		if (r == people[idx].er && c == people[idx].ec)
			break;

		for (int d = 0; d < 4; d++) {
			int nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && visited[nr][nc] == -1 && !grid[nr][nc]) {
				tmp_path[nr][nc] = { r, c };
				q.push({ nr, nc });
				visited[nr][nc] = visited[r][c] + 1;
			}
		}
	}

	// 역으로 추적해가며 path 저장하기
	int r = people[idx].er, c = people[idx].ec;
	while (1) {
		if (r == people[idx].sr && c == people[idx].sc)
			break;
		int nr = tmp_path[r][c].first, nc = tmp_path[r][c].second;
		path[idx][nr][nc] = { r, c };
		r = nr;
		c = nc;
	}

}


void update_path(int idx) {
	for (int i = 0; i < idx; i++) {
		if (!people[i].arrive)
			// 사람마다 새로운 경로 찾기
			make_path(i);
	}
}


int simulation() {
	int time = 0;
	int gameover = 0;
	pair<int, int> move_result;
	while (1) {
		// 1. 가고싶은 편의점 방향으로 한 칸 이동
		move_result = move_people(time);
		gameover += move_result.second;
		// ### 게임 종료 ###
		if (gameover == m)
			break;

		// 3. 베이스캠프에 인원 넣기
		if (time < m) {
			update_people(time);
			move_result.first = 1;
		}

		// 4. 길 업데이트가 필요하다면 업데이트하기
		if (move_result.first)
			update_path(time + 1);

		time++;
	}

	return time + 1;
}

int main() {
	init();

	cout << simulation() << '\n';

	return 0;
}
