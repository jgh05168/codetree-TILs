/*
r x c
가장 위를 1행, 가장 아래를 r행

숲의 북쪽으로만 들어올 수 있음
k명의 정령, 골렘은 십자모양 구조를 갖고 있음
정령은 어떤 방향에서든 골렘에 탈 수 있지만, 내릴 땐 정해진 출구로만 내릴 수 있음

중앙이 c열이 되도록 하는 위치에서 내려오기 시작, 초기 골렘의 출구는 d방향에 위치함
1. 남쪽으로 한 칸 내려옴(초록색 칸들이 비어있을 때만 내려오기 ㄱㄴ)
2. 1번 방법이 불가능하면 서쪽방향으로 회전하면서 이동 - 반시계 회전
3. 동짝방향으로 회전하면서 내려오기 - 시계 회전

위 3가지 방법이 모두 불가능할 땐 멈춘다.

현재 위치하는 골렘의 출구가 다른 골렘과 인접하다면, 해당 출구를 통해 이동 가능
정령이 갈 수 있는 가장 남쪽 칸이 정령의 점수가 된다.

# 골렘의 몸 일부가 숲을 벗어난 상태라면, 정령의 최종 위치를 답에 포함시키지 않는다.
	-> 맵을 비우기


풀이 : BFS, 구현
하드코딩으로 내려갈 수 있는 위치 예측하기
회전의 경우에는 두 함수 모두 구현해두기
골렘 struct 생성, 골렘 정보 : 골렘 중앙점(r, c) & 출구
골렘의 회전은 각 이동이 끝난 직후 바로 판단해서 출구 업데이트해주기
모든 이동이 끝난 뒤, 맵에 골렘의 정보를 업데이트하기 -> 이후 bfs 시작
*/

#include <iostream>
#include <cstring>
#include <queue>
#include <vector>
#include <algorithm>

using namespace std;

int R, C, K;
int grid[74][71] = { 0, };
int visited[74][71] = { 0, };
pair<int, int> exit_list[1001];

int dr[4] = { -1, 0, 1, 0 };
int dc[4] = { 0, 1, 0, -1 };
int move_dir[3][2] = { {1, 0}, {1, -1,}, {1, 1} };
vector<vector<pair<int, int>>> check_move(3);


struct gollum {
	int r, c, exit;
};

bool isValid(int r, int c) {
	return 0 <= r && r < R + 3 && 0 <= c && c < C;
}


int get_score(int sr, int sc) {
	queue<pair<int, int>> q;
	q.push({ sr, sc });
	memset(visited, 0, sizeof(visited));
	visited[sr][sc] = 1;
	int max_v = sr;

	while (!q.empty()) {
		int r = q.front().first, c = q.front().second;
		q.pop();

		for (int d = 0; d < 4; d++) {
			int nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && !visited[nr][nc] && grid[nr][nc]) {
				// 같은 부분이 아니라면, 이전 위치가 출구인지 확인
				if (grid[r][c] != grid[nr][nc])
					if (!(r == exit_list[grid[r][c]].first && c == exit_list[grid[r][c]].second))
						continue;
				q.push({ nr, nc });
				visited[nr][nc] = 1;
				max_v = max(max_v, nr);
			}
		}
	}

	return max_v - 2;
}


void solution() {
	int sc, sd;
	gollum g;
	int answer = 0;
	int gollum_idx = 1;
	for (int num = 1; num < K + 1; num++) {
		// 골렘 정보
		cin >> g.c >> g.exit;
		g.r = 1;
		g.c--;

		// 내려가기
		int goDown = 1;
		int nr, nc;
		while (goDown) {
			goDown = 0;
			for (int i = 0; i < 3; i++) {
				int flag = 1;
				for (int j = 0; j < check_move[i].size(); j++) {
					nr = g.r + check_move[i][j].first, nc = g.c + check_move[i][j].second;
					if (!isValid(nr, nc) || grid[nr][nc]) {
						flag = 0;
						break;
					}
				}
				// 만약 내려가는데 성공했다면야
				if (flag) {
					g.r += move_dir[i][0];
					g.c += move_dir[i][1];
					if (i == 1) 
						g.exit = (g.exit + 4 - 1) % 4;
					else if (i == 2)
						g.exit = (g.exit + 1) % 4;
					goDown = 1;
					break;
				}
			}
		}

		// 이동할 수 있는 위치까지 다 내려왔다면, 맵 업데이트
		// 만약 상단부가 맵 밖이라면 맵 클리어 후 continue;
		if (g.r - 1 < 3) {
			memset(grid, 0, sizeof(grid));
			gollum_idx = 1;
			continue;
		}
		// 아니라면 업데이트하기
		grid[g.r][g.c] = num;
		for (int d = 0; d < 4; d++) {
			int nr = g.r + dr[d], nc = g.c + dc[d];
			if (d == g.exit)
				exit_list[num] = { nr, nc };
			grid[nr][nc] = num;
		}

		// 현재 위치에서부터 bfs로 최하단으로 내려가기

		answer += get_score(g.r, g.c);
	}

	cout << answer << '\n';
}


void init() {
	cin >> R >> C >> K;
	// 아래
	check_move[0].push_back({ 1, -1 });
	check_move[0].push_back({ 2, 0 });
	check_move[0].push_back({ 1, 1 });

	// 왼
	check_move[1].push_back({ -1, -1 });
	check_move[1].push_back({ 0, -2 });
	check_move[1].push_back({ 1, -1 });
	check_move[1].push_back({ 1, -2 });
	check_move[1].push_back({ 2, -1 });

	// 오
	check_move[2].push_back({ -1, 1 });
	check_move[2].push_back({ 0, 2 });
	check_move[2].push_back({ 1, 1 });
	check_move[2].push_back({ 1, 2 });
	check_move[2].push_back({ 2, 1 });
}


int main() {
	init();

	solution();

	return 0;
}