/*
11:00 시작

3명 이상이 한 팀이 된다
맨 앞 사람 : 머리사람, 맨 뒤 사람 : 꼬리사람
각 팀은 게임에서 주어진 이동 선을 따라서만 이동함

1. 머리사람을 따라서 한 칸 이동
2. 각 라운드마다 공이 정해진 선을 따라 던져진다.
- 총 4n
3. 공이 던져지는 경우에 해당 선에 사람이 있으면, 최초에 만나게 되는 사람만이 점수를 얻음
- 팀 내 k번째 사람이라면 k의 제곱만큼 점수를 얻는다.
- 공을 획득한 팀의 경우에는 머리사람과 꼬리사람이 바뀐다.

풀이 : n <= 20
팀의 개수 <= 5

팀원 관리 어떻게 할 것인가 ?
	- simulation ? 
	1000 x 5 x 400 = 200만
필요 grid : 술래잡기 맵, 양방향 path 사전에 생성
deque, 팀 별 이동 방향 dat

*/

#include <iostream>
#include <cstring>
#include <queue>
#include <algorithm>
#include <vector>

using namespace std;

int n, m, k;
int grid[21][21];
int people[21][21];
int team_route[21][21] = { 0, };
int team_dir[6];
pair<int, int> path[2][6][21][21];
vector<vector<pair<int, int>>> team_list(6);

int answer = 0;

int dr[4] = { 0, 1, 0, -1 };
int dc[4] = { 1, 0, -1, 0 };

bool isValid(int r, int c) {
	return 0 <= r && r < n && 0 <= c && c < n;
}


void bfs(int sr, int sc, int num) {
	queue<pair<int, int>> q;
	team_route[sr][sc] = num;
	q.push({ sr, sc });
	int r, c, nr, nc, flag = 0;
	team_list[num].push_back({ sr, sc });

	while (!q.empty()) {
		r = q.front().first, c = q.front().second;
		q.pop();
		 

		for (int d = 0; d < 4; d++) {
			nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && !team_route[nr][nc] && grid[nr][nc] > 0) {
				// 3과 1이 만나는 경우에 대해 판단해야함 -> 초기에는 무조건 2 방향으로 가야함
				if (!flag && grid[nr][nc] > 2)
					continue;
				if (grid[nr][nc] == 2)
					flag = 1;
				// 팀 리스트 생성
				if (grid[nr][nc] < 4)
					team_list[num].push_back({ nr, nc });
				q.push({ nr, nc });
				team_route[nr][nc] = num;
				path[0][num][nr][nc] = { r, c };
			}
		}
	}
	path[0][num][sr][sc] = { r, c };

	// 정방향 path 생성
	r = sr, c = sc;
	while (1) {
		nr = path[0][num][r][c].first, nc = path[0][num][r][c].second;
		if (path[1][num][nr][nc].first != -1)
			break;
		path[1][num][nr][nc] = { r, c };
		r = nr, c = nc;
	}
}


void init() {
	cin >> n >> m >> k;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			cin >> grid[i][j];
		}
	}

	// 길 생성
	memset(path, -1, sizeof(path));
	int team_num = 1;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (grid[i][j] == 1) {
				bfs(i, j, team_num++);
			}
		}
	}

	memset(team_dir, 0, sizeof(team_dir));
	memset(people, 0, sizeof(people));

	for (int idx = 1; idx < m + 1; idx++) {
		for (int i = 0; i < team_list[idx].size(); i++) {
			int r = team_list[idx][i].first, c = team_list[idx][i].second;
			people[r][c] = idx;
		}
	}
}


void team_move() {
	for (int idx = 1; idx < m + 1; idx++) {
		people[team_list[idx].back().first][team_list[idx].back().second] = 0;
		for (int i = 0; i < team_list[idx].size(); i++) {
			int r = team_list[idx][i].first, c = team_list[idx][i].second;
			team_list[idx][i].first = path[team_dir[idx]][idx][r][c].first;
			team_list[idx][i].second = path[team_dir[idx]][idx][r][c].second;
		}
		people[team_list[idx].front().first][team_list[idx].front().second] = idx;
	}
}


void throw_ball(int sr, int sc, int side) {
	if (side == 1) {
		for (int c = 0; c < n; c++) {
			if (people[sr][c]) {
				int idx = people[sr][c];
				team_dir[idx] = (team_dir[idx] + 1) % 2;
				for (int sequence = 0; sequence < team_list[idx].size(); sequence++) {
					if (team_list[idx][sequence].first == sr && team_list[idx][sequence].second == c) {
						answer += (sequence + 1) * (sequence + 1);
						break;
					}
				}
				reverse(team_list[idx].begin(), team_list[idx].end());
				break;
			}
		}
	}
	else if (side == 2) {
		for (int r = n - 1; r >= 0; r--) {
			if (people[r][sc]) {
				int idx = people[r][sc];
				team_dir[idx] = (team_dir[idx] + 1) % 2;
				for (int sequence = 0; sequence < team_list[idx].size(); sequence++) {
					if (team_list[idx][sequence].first == r && team_list[idx][sequence].second == sc) {
						answer += (sequence + 1) * (sequence + 1);
						break;
					}
				}
				reverse(team_list[idx].begin(), team_list[idx].end());
				break;
			}
		}
	}
	else if (side == 3) {
		for (int c = n - 1; c >= 0; c--) {
			if (people[sr][c]) {
				int idx = people[sr][c];
				team_dir[idx] = (team_dir[idx] + 1) % 2;
				for (int sequence = 0; sequence < team_list[idx].size(); sequence++) {
					if (team_list[idx][sequence].first == sr && team_list[idx][sequence].second == c) {
						answer += (sequence + 1) * (sequence + 1);
						break;
					}
				}
				reverse(team_list[idx].begin(), team_list[idx].end());
				break;
			}
		}
	}
	else if (side == 4) {
		for (int r = 0; r < n; r++) {
			if (people[r][sc]) {
				int idx = people[r][sc];
				team_dir[idx] = (team_dir[idx] + 1) % 2;
				for (int sequence = 0; sequence < team_list[idx].size(); sequence++) {
					if (team_list[idx][sequence].first == r && team_list[idx][sequence].second == sc) {
						answer += (sequence + 1) * (sequence + 1);
						break;
					}
				}
				reverse(team_list[idx].begin(), team_list[idx].end());
				break;
			}
		}
	}
}


void simulation() {
	int sr = 0, sc = 0;
	for (int time=0;time<k;time++) {
		// 1. 머리사람을 따라 한 칸 이동
		team_move();

		// 2. 공 던지기
		int side = ((time / n) % 4) + 1;
		if (side == 1)
			sr = time % n, sc = 0;
		else if (side == 2)
			sr = n - 1, sc = time % n;
		else if (side == 3)
			sr = n - (time % n) - 1, sc = n - 1;
		else if (side == 4)
			sr = 0, sc = n - (time % n) - 1;
		throw_ball(sr, sc, side);
	}
}


int main() {
	init();

	simulation();

	cout << answer << '\n';

	return 0;
}