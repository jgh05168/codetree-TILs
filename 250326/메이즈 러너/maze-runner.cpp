/*
19:00 시작

[미로의 구성]
N x N,
좌상단은 (1, 1)
1. 빈 칸
2. 벽
	- 1이상 9이하 내구도를 가짐
	- 회전할 때, 내구도가 1씩 깎임
	- 내구도가 0이 되면 빈 칸으로 변경된다.
3. 출구
	- 참가자가 해당 칸에 도달하면 즉시 탈출

[참가자 이동]
1초마다 모든 참가자는 한 칸씩 이동
- 최단거리는 맨해튼거리로 정의됨
- 모든 참가자는 동시에 움직임
- 상하좌우 이동 & 벽으론 이동 불가능
- 움직인 칸은 머문 칸보다 출구까지의 최단거리가 가까워야됨 => 못움직이는 경우도 존재함
- 움직일 수 있는 칸이 2개 이상이라면 상하 움직임 우선
- 한 칸에 2명 이상 참가자 존재 가능

[미로 회전]
- 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 잡는다.
- 가장 작은 크기의 정사각형이 2개 이상이라면 r, c작은 순으로 정해짐
- 시계 방향으로 90도 회전된다. 회전되면서 벽은 내구도가 1씩깎임

[출력] 
게임이 끝났을 때 모든 참가자들의 이동 거리 합과 출구 좌표를 출력

풀이 : BFS, 시뮬
참가자 정보 : r, c, 총 이동 거리, 탈출 여부
맵 : maze, 참가자 map, visited, path
- 벽 회전이 일어나는 경우를 체크하여 path 업데이트해주기
*/

#include <iostream>
#include <cstring>
#include <queue>
#define MAX_SIZE 11

using namespace std;

struct runner {
	int r, c, canMove, isEscape;
};

int N, M, K;
int er, ec, total_move = 0;
int maze[MAX_SIZE][MAX_SIZE];
int runner_map[MAX_SIZE][MAX_SIZE][MAX_SIZE];	// r, c, runner 정보
runner runner_list[MAX_SIZE];
int visited[MAX_SIZE][MAX_SIZE];
pair<int, int> path[MAX_SIZE][MAX_SIZE][MAX_SIZE];

int dr[4] = { -1, 1, 0, 0 };
int dc[4] = { 0, 0, -1, 1 };

bool isValid(int r, int c) {
	return 0 <= r && r < N && 0 <= c && c < N;
}


void make_path(int idx) {
	pair<int, int> tmp_path[MAX_SIZE][MAX_SIZE];
	queue<pair<int, int>> q;
	memset(visited, -1, sizeof(visited));
	q.push({ runner_list[idx].r, runner_list[idx].c });
	visited[runner_list[idx].r][runner_list[idx].c] = 0;
	int r, c, flag = 0;
	int nr, nc;
	int dist = abs(runner_list[idx].r - er) + abs(runner_list[idx].c - ec);

	while (!q.empty()) {
		r = q.front().first, c = q.front().second;
		q.pop();

		if (flag)
			break;
		if (visited[r][c] >= dist)
			continue;

		for (int d = 0; d < 4; d++) {
			nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && visited[nr][nc] == -1 && maze[nr][nc] <= 0) {
				q.push({ nr, nc });
				visited[nr][nc] = visited[r][c] + 1;
				tmp_path[nr][nc] = { r, c };
				// 도착지에 도착했다면야 return
				if (maze[nr][nc] == -1) {
					flag = 1;
					break;
				}
			}
		}
	}

	if (!flag) {
		runner_list[idx].canMove = 0;
		return;
	}
	// 경로 생성
	runner_list[idx].canMove = 1;
	r = nr, c = nc;
	while (r != runner_list[idx].r || c != runner_list[idx].c) {
		nr = tmp_path[r][c].first, nc = tmp_path[r][c].second;
		path[idx][nr][nc] = { r, c };
		r = nr, c = nc;
	}
}



void init() {
	cin >> N >> M >> K;
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++)
			cin >> maze[i][j];
	}
	int r, c;
	for (int i = 0; i < M; i++) {
		cin >> r >> c;
		r--; c--;
		runner_list[i].r = r, runner_list[i].c = c;
		runner_map[r][c][i] = 1;
	}
	cin >> er >> ec;
	er--; ec--;
	maze[er][ec] = -1;		// 출구 정보 : -1

	// path 찾아두기
	for (int i = 0; i < M; i++) {
		make_path(i);
	}
}


int runner_move() {
	int nr, nc;
	int escape = 0;
	for (int idx = 0; idx < M; idx++) {
		// 탈출한 경우나 이동할 수 없는 경우면, 컨티뉴
		if (runner_list[idx].isEscape || !runner_list[idx].canMove)
			continue;
		// 미리 생성한 path 따라서 한 칸씩 이동 및 업데이트
		int r = runner_list[idx].r, c = runner_list[idx].c;
		nr = path[idx][r][c].first, nc = path[idx][r][c].second;
		runner_map[r][c][idx] = 0;
		runner_map[nr][nc][idx] = 1;
		runner_list[idx].r = nr, runner_list[idx].c = nc;
		// runner가 탈출했는지 체크해보자
		if (maze[nr][nc] == -1) {
			escape++;
			runner_list[idx].isEscape = 1;
			runner_map[nr][nc][idx] = 0;
		}
		total_move++;
	}

	return escape;
}


void rotate(int si, int sj, int n) {
	int tmp_maze[MAX_SIZE][MAX_SIZE];
	int tmp_runner_map[MAX_SIZE][MAX_SIZE][MAX_SIZE];
	// 초기화
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			tmp_maze[i][j] = maze[i][j];
			for (int k = 0; k < M; k++) {
				tmp_runner_map[i][j][k] = runner_map[i][j][k];
			}
		}
	}
	
	// 회전 시작
	for (int i = si; i < si + n; i++) {
		for (int j = sj; j < sj + n; j++) {
			int oi = i - si, oj = j - sj;
			int ni = oj, nj = n - oi - 1;
			if (maze[i][j] == -1) {
				er = ni + si, ec = nj + sj;
			}
			if (maze[i][j] > 0) {
				tmp_maze[ni + si][nj + sj] = maze[i][j] - 1;
			}
			else {
				tmp_maze[ni + si][nj + sj] = maze[i][j];
			}
			for (int k = 0; k < M; k++) {
				tmp_runner_map[ni + si][nj + sj][k] = runner_map[i][j][k];
				if (runner_map[i][j][k])
					runner_list[k].r = ni + si, runner_list[k].c = nj + sj;
			}
		}
	}

	// 맵 원래꺼에 다시 씌우기
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			maze[i][j] = tmp_maze[i][j];
			for (int k = 0; k < M; k++) {
				runner_map[i][j][k] = tmp_runner_map[i][j][k];
			}
		}
	}
}


void find_maze() {
	// (0, 0)부터 시작, 사이즈는 2부터 N까지(10)
	for (int _size = 2; _size < N; _size++) {
		// 순회(10 x 10)
		for (int i = 0; i < N - _size + 1; i++) {
			for (int j = 0; j < N - _size + 1; j++) { 
				int find_runner = 0, find_exit = 0;
				// 회전이 필요한 만큼 순회하면서 찾기 (10 x 10)
				for (int r = i; r < i + _size; r++) {
					for (int c = j; c < j + _size; c++) {
						// 사람 있는지 체크 (10)
						for (int ridx = 0; ridx < M; ridx++) {
							if (runner_map[r][c][ridx]) {
								find_runner = 1;
								break;
							}
						}
						// 출구 있는지 체크
						if (maze[r][c] == -1)
							find_exit = 1;
					}
				}
				// 출구랑 입구 모두 찾았으면 90도 회전 후 종료
				if (find_runner && find_exit) {
					rotate(i, j, _size);
					return;
				}
			}
		}
	}
}


void simulation() {
	int gameover = 0;
	while (K--) {
		// 1. 참가자 이동
		gameover += runner_move();
		// 게임 종료 확인
		if (gameover == M)
			break;

		// 2. 미로 회전
		find_maze();

		// 3. 회전했으니 경로 업데이트
		for (int i = 0; i < M; i++) {
			if (!runner_list[i].isEscape)
				make_path(i);
		}
	}

	// 출력
	cout << total_move << '\n';
	cout << er + 1 << ' ' << ec + 1 << '\n';
}


int main() {
	init();

	simulation();

	return 0;
}