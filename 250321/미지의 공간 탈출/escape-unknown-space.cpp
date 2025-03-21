/*
18:25 시작

n x n 미지의 공간에서 탈출하자 !

한 변의 길이가 N인 2차원 평면이며, 그 사이 어딘가에는 m 길이의 정육면체 형태의 시간의 벽이 세워져있음
알아낼 수 있는 정보 : 
1. 미지의 공간 평면도
2. 시간의 벽의 단면도 - 윗면과 동서남북 네 면의 단면도임
빈공간 : 0 | 장애물 : 1

타임머신은 시간의 벽 윗면 어딘가에 위치함. 타임머신의 위치 - 2
미지의 공간 평면도에는 시간의 벽의 위치 3과 탈출구 4가 표시됨

미지의 공간 바닥에는 F개의 시간 이상 현상이 존재함
- 빈공간 r, c에서 시작해 매 v의 배수 턴마다 방향 d로 한 칸씩 확산된다.
- 이상현상은 사라지지 않고 남아있음
- 모든 시간이상현상은 서로 독립적이고, 동시에 확장된다.
- 빈공간으로만 확산된다.
- 확산이 불가능하다면 멈춤

타임머신은 매 턴 상하좌우 한 칸 이동 가능. 탈출구까지 탈출하는 최소 턴 수를 구하자. 탈출 못하면 -1 출력
# 시간 이상 현상이 확산된 직후 타임머신이 이동한다.

풀이 : 좌표매칭, BFS
1. 시간 이상 현상
2. 타임머신 이동

좌표매칭의 경우, 이동 방향에 따라서 어느 면으로 이동했는지 체크하기 위한 배열 생성
- 각 면을 기준으로 체크해야함(면에 따라 조건이 존재한다. 이걸 switch-case로 맞추기)
맵은 전체를 하나로 생각하기 + 시작 맵에 내려온 경우, 3의 시작 좌표를 더하자
*/

#include <iostream>
#include <cstring>
#include <queue>
#include <vector>
using namespace std;

struct wierd {
	int r, c, d, v;
};

int N, M, F;
int end_r, end_c;
int time_r, time_c;
vector<vector<vector<int>>> grid(6);
int visited[21][21][21];
vector<wierd> wierd_point(11);
queue<pair<int, pair<int, int>>> q;

int dr[4] = { 0, 0, 1, -1 };
int dc[4] = { 1, -1, 0, 0 };
// 방향 별 단면 매핑
int mapping[6][4] = { {2, 1, 4, 3}, {4, 3, 0, 5}, {3, 4, 0, 5}, {1, 2, 0, 5}, {2, 1, 0, 5}, {1, 2, 3, 4} };
vector<int> grid_size;


bool isValid(int r, int c, int n) {
	return 0 <= r && r < n && 0 <= c && c < n;
}


void spread_wierd(int cur_time) {
	if (!cur_time)
		return;
	for (int idx = 0; idx < F; idx++) {
		if (!(cur_time % wierd_point[idx].v)) {
			int nr = wierd_point[idx].r + dr[wierd_point[idx].d];
			int nc = wierd_point[idx].c + dc[wierd_point[idx].d];
			if (isValid(nr, nc, N) && !grid[0][nr][nc]) {
				grid[0][nr][nc] = 1;
				wierd_point[idx].r = nr;
				wierd_point[idx].c = nc;
			}
		}
	}
}

// 새로운 단면 정보로 업데이트
pair<int, pair<int, int>> get_new_loc(int dim, int r, int c, int d) {
	int new_dim, nr, nc;
	
	new_dim = mapping[dim][d];

	if (dim == 1) {
		if (!new_dim) {
			nr = time_r + M - c - 1, nc = time_c + M;
		}
		else if (new_dim == 3 || new_dim == 4) {
			nr = r, nc = M - c - 1;
		}
		else if (new_dim == 5) {
			nr = M - c - 1, nc = M - r - 1;
		}
	}
	else if (dim == 2) {
		if (!new_dim) {
			nr = time_r + c, nc = time_c - 1;
		}
		else if (new_dim == 3 || new_dim == 4) {
			nr = r, nc = M - c - 1;
		}
		else if (new_dim == 5) {
			nr = c, nc = r;
		}
	}
	else if (dim == 3) {
		if (!new_dim) {
			nr = time_r + M, nc = time_c + c;
		}
		else if (new_dim == 1 || new_dim == 2) {
			nr = r, nc = M - c - 1;
		}
		else if (new_dim == 5) {
			nr = M - r - 1, nc = c;
		}
	}
	else if (dim == 4) {
		if (!new_dim) {
			nr = time_r - 1, nc = time_c + M - c - 1;
		}
		else if (new_dim == 1 || new_dim == 2) {
			nr = r, nc = M - c - 1;
		}
		else if (new_dim == 5) {
			nr = r, nc = M - c - 1;
		}
	}
	else if (dim == 5) {
		if (new_dim == 1) {
			nr = M - c - 1, nc = M - r - 1;
		}
		else if (new_dim == 2) {
			nr = c, nc = r;
		}
		else if (new_dim == 3) {
			nr = M - r - 1, nc = c;
		}
		else if (new_dim == 4) {
			nr = r, nc = M - c - 1;
		}
	}

	return { new_dim, {nr, nc} };
}


queue<pair<int, pair<int, int>>> move_timemachine(queue<pair<int, pair<int, int>>> origin_q) {
	queue<pair<int, pair<int, int>>> new_q;
	pair<int, pair<int, int>> new_point;

	while (!origin_q.empty()) {
		int r = origin_q.front().second.first, c = origin_q.front().second.second;
		int dim = origin_q.front().first;
		origin_q.pop();

		for (int d = 0; d < 4; d++) {
			int nr = r + dr[d], nc = c + dc[d];
			int ndim = dim;
			// 범위 벗어나는 경우 체크
			if (!isValid(nr, nc, grid_size[dim])) {
				// 미지의 공간 바닥인 경우는 그냥 나간거이므로 continue
				if (!dim)
					continue;
				new_point = get_new_loc(dim, r, c, d);
				ndim = new_point.first, nr = new_point.second.first, nc = new_point.second.second;
			}
			if (visited[ndim][nr][nc] == -1 && !grid[ndim][nr][nc]) {
				new_q.push({ ndim, {nr, nc} });
				visited[ndim][nr][nc] = visited[dim][r][c] + 1;
			}
		}
	}

	return new_q;
}


void init() {
	cin >> N >> M >> F;
	int tmp, t_flag = 0;
	memset(visited, -1, sizeof(visited));
	vector<int> ttmp;
	// 미지의 공간 바닥 입력
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			cin >> tmp;
			ttmp.push_back(tmp);
			if (tmp == 4)
				end_r = i, end_c = j;
			if (tmp == 3 && !t_flag) {
				t_flag = 1;
				time_r = i, time_c = j;
			}
		}
		grid[0].push_back(ttmp);
		ttmp.clear();
	}
	grid[0][end_r][end_c] = 0;
	// 타임머신 입력
	for (int idx = 1; idx < 6; idx++) {
		for (int i = 0; i < M; i++) {
			for (int j = 0; j < M; j++) {
				cin >> tmp;
				ttmp.push_back(tmp);
				if (tmp == 2) {
					q.push({ idx, {i, j} });
					visited[idx][i][j] = 0;
				}
			}
			grid[idx].push_back(ttmp);
			ttmp.clear();
		}
	}
	// 이상현상 입력
	for (int i = 0; i < F; i++) {
		cin >> wierd_point[i].r >> wierd_point[i].c >> wierd_point[i].d >> wierd_point[i].v;
		grid[0][wierd_point[i].r][wierd_point[i].c] = 1;
	}

	// 맵 사이즈 입력
	grid_size.push_back(N);
	for (int i=0;i<5;i++)
		grid_size.push_back(M);

}


int simulation() {
	int time = 1;
	while (1) {
		// 1. 이상현상 이동
		spread_wierd(time);
		// 2. 타임머신 이동
		q = move_timemachine(q);
		// 3-1. 만약 큐가 비었다면, 더이상 이동이 불가능한 경우이므로 게임 종료
		if (q.empty())
			return -1;
		// 3-2. 만약 도착지점에 도착했다면, 종료
		if (visited[0][end_r][end_c] != -1)
			break;
		time++;
	}
	return time;
}


int main() {
	init();

	cout << simulation() << '\n';

	return 0;
}