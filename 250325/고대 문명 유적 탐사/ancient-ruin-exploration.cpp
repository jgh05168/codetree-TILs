/*
09:03 시작

5 x 5 격자 형태, 각 칸에는 유물조각 배치되있음(1 ~ 7)

1. 탐사 진행
- 5 x 5 격자 내에서 3 x 3 격자를 선택해 회전시킬 수 있음
- 선택된 격자는 시계방향으로 4 각도 중 하나만큼 회전시킬 수 있다.
- 회전 목표 : 가능한 회전 방법 중 
	1) 유물 1차 획득 가치 최대화
	2) 회전한 각도가 가장 작은 방법을 선택
	3) 회전 중심 좌표의 열이 가장 작은 -> 행이 가장 작은 구간 선택

2. 유물 획득
- 유물 1차 획득 : 상하좌우 인접 유물 조각이 3개 이상 연결된 경우, 유물이 된다. -> 조각 개수 : 유물의 가치
- 조각이 사라진 위치에는 유적 벽면 순서대로 새로운 조각이 생겨남
	1) 열 번호가 작은 순으로 조각이 생겨남
	2) 행 번호가 큰 순으로 조각이 생겨남
- 새로운 조각은 재사용이 금지됨
- 유물 연쇄 획득

3. 탐사 반복
- K번의 턴에 걸쳐 진행된다.
- 각 턴마다 유물의 가치이 총합을 출력하자
- 유물 획득이 불가능하다면 그즉시 종료

풀이 : BFS, 시뮬
1. 회전 진행 시 열 작은 순 -> 행 작은 순 진행
2. 회전 진행 후 유물 1차 획득 해보기
3. 유물 획득 후 다시 연쇄작용
*/

#include <iostream>
#include <cstring>
#include <queue>
#include <vector>
#include <algorithm>

using namespace std;

int n = 5, m, k;
int grid[6][6];
int visited[6][6];
queue<int> treasure_piece;

int dr[4] = { 0, 1, 0, -1 };
int dc[4] = { 1, 0, -1, 0 };

bool isValid(int r, int c) {
	return 0 <= r && r < n && 0 <= c && c < n;
}


bool cmp(pair<int, int> a, pair<int, int> b) {
	if (a.second == b.second)
		return a.first > b.first;
	return a.second < b.second;
}


void init() {
	cin >> k >> m;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			cin >> grid[i][j];
		}
	}
	int tmp;
	for (int i = 0; i < m; i++) {
		cin >> tmp;
		treasure_piece.push(tmp);
	}
}


queue<int> rotate(int si, int sj) {
	int new_grid[4][4];
	int oi, oj, ni, nj;
	queue<int> new_queue;
	for (int i = si; i < si + 3; i++) {
		for (int j = sj; j < sj + 3; j++) {
			oi = i - si, oj = j - sj;
			ni = oj, nj = 3 - oi - 1;
			new_grid[ni][nj] = grid[i][j];
		}
	}
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			new_queue.push({ new_grid[i][j] });
	}

	return new_queue;
}


vector<pair<int, int>> get_treasure() {
	memset(visited, 0, sizeof(visited));
	vector<pair<int, int>> check_treasure;
	queue<pair<int, int>> q;

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (!visited[i][j]) {
				int piece = grid[i][j];
				queue<pair<int, int>> tmp_treasure;

				tmp_treasure.push({ i, j });
				q.push({ i, j });
				visited[i][j] = 1;

				while (!q.empty()) {
					int r = q.front().first, c = q.front().second;
					q.pop();

					for (int d = 0; d < 4; d++) {
						int nr = r + dr[d], nc = c + dc[d];
						if (isValid(nr, nc) && !visited[nr][nc] && grid[nr][nc] == piece) {
							tmp_treasure.push({ nr, nc });
							q.push({ nr, nc });
							visited[nr][nc] = 1;
						}
					}
				}
				// 갯수 체크
				if (tmp_treasure.size() > 2) {
					while (!tmp_treasure.empty()) {
						check_treasure.push_back(tmp_treasure.front());
						tmp_treasure.pop();
					}
				}
			}
		}
	}
	return check_treasure;
}


vector<pair<int, int>> find_coord() {
	queue<int> rotate_value;
	vector<pair<int, int>> max_coord;
	vector<pair<int, int>> tmp_coord;
	// 새로운 맵 초기화
	int new_grid[6][6];
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++)
			new_grid[i][j] = grid[i][j];
	}

	int rotate_degree = 4;
	for (int j = 0; j < n - 2; j++) {
		for (int i = 0; i < n - 2; i++) {
			// 5 x 5 중 가장자리 죄표 제외한 나머지 녀석들 기준으로 회전 필요함
			for (int d = 1; d < 5; d++) {
				// 회전 진행
				rotate_value = rotate(i, j);
				// 회전된 값 배열에 넣기
				for (int nr = i; nr < i + 3; nr++) {
					for (int nc = j; nc < j + 3; nc++) {
						grid[nr][nc] = rotate_value.front();
						rotate_value.pop();
					}
				}
				// 유물 1차 획득 시작
				tmp_coord = get_treasure();
				if (max_coord.size() < tmp_coord.size()) {
					rotate_degree = (d + 4) % 4;
					max_coord.swap(tmp_coord);
					for (int i = 0; i < n; i++) {
						for (int j = 0; j < n; j++)
							new_grid[i][j] = grid[i][j];
					}
				}
				else if (max_coord.size() == tmp_coord.size() && rotate_degree > (d + 4) % 4) {
					rotate_degree = (d + 4) % 4;
					max_coord.swap(tmp_coord);
					for (int i = 0; i < n; i++) {
						for (int j = 0; j < n; j++)
							new_grid[i][j] = grid[i][j];
					}
				}
			}
		}
	}

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++)
			grid[i][j] = new_grid[i][j];
	}
	return max_coord;
}


void simulation() {
	vector<pair<int, int>> treasure;
	int answer = 0;
	// K번 만큼 탐사 반복
	while (k--) {
		treasure.clear();
		answer = 0;

		// 1. rotate 찾기
		treasure = find_coord();
		// 1-2. 유물을 못찾으면 그대로 게임 종료
		if (treasure.empty())
			break;

		// 2-1. 유물 1차 탐사값 저장
		answer += treasure.size();
		// 2-2. 새로운 조각 저장
		sort(treasure.begin(), treasure.end(), cmp);
		for (auto coord : treasure) {
			grid[coord.first][coord.second] = treasure_piece.front();
			treasure_piece.pop();
		}
		// 2-3. 유물 연쇄 획득
		while (1) {
			treasure = get_treasure();
			if (treasure.empty())
				break;
			answer += treasure.size();
			// 2-2. 새로운 조각 저장
			sort(treasure.begin(), treasure.end(), cmp);
			for (auto coord : treasure) {
				grid[coord.first][coord.second] = treasure_piece.front();
				treasure_piece.pop();
			}
		}

		cout << answer << ' ';
	}

}

int main() {
	init();

	simulation();

	return 0;
}