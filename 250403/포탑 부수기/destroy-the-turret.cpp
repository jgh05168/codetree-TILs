/*
10:45 시작

N x M, 모든 위치에는 포탑이 존재함
각 포탑에는 공격력이 부여되고, 공격력 0 이하라면, 해당 포탑은 더이상 공격 x
최초에 공격력 0인 포탑 존재 가능

총 K턴 반복된다. / 부서지지 않은 포탑이 1개가 된다면 그 즉시 중지

1. 공격자 선정
부서지지 않은 포탑 중 가장 약한 포탑이 공격자가 됨
- 공격자는 N + M 만큼의 공격력이 증가한다
- 우선순위 : 공격력 낮은 순, 가장 최근에 공격한 포탑, 행과 열의 합이 가장 큰, 열 값이 가장 큰

2. 공격자의 공격
자신을 제외한 가장 강한 포탑 공격
- 공격력 높은 순, 공격한지 가장 오래된 포탑, 행과 열의 합이 가장 작은, 열 값이 가장 작은

	2-1. 레이저 공격
	- 상하좌우 4개의 방향으로 움직임 가능
		- 우 하 좌 상 우선순위
	- 부서진 포탑이 있는 위치는 지날 수 없다.
	- 가장자리에서 막힌 방향으로 지나가고자 한다면, 반대편으로 나옴
	- 공격자의 위치에서 공격 대상 포탑까지의 최단 경로로 공격함
		- 이런 경로가 존재하지 않는다면, 포탄 공격을 진행함
	- 경로에 있는 포탑도 공격을 받음 : 공격력 절반만큼

	2-2. 포탄 공격
	공격 대상에 포탄을 전진다. 
	- 공격 대상은 공격자 공격력 만큼 피해를 받음
	- 주위 8개 방향에 있는 포탑도 피해를 입음 = 공격자 공격력의 절반만큼
	- 공격자는 해당 공격에 영향을 받지 않는다 !!
	- 가장자리라면, 레이저 공격처럼 반대편에 영향이 간다.

3. 포탑 부서짐
공격력 0인 포탑은 부서진다.

4. 포탑 정비
공격과 무관했던 포탑은 공격력이 1씩 올라간다.

남아있는 포탑 중 가장 강한 포탑의 공격력을 출력하자

풀이 : 
포탑 구조체 정보 : r, c, 공격력, 공격한 시간, 죽었는지 여부
포탑의 개수 <= 100
그리드 정보 : 포탑, path, visited, 이번 턴에 공격에 관여했는지 여부
포탑은 cmp를 활용해 정렬하기. 맨 처음과 끝 녀석을 공격자, 공격받는자로 선정
매 턴이 끝날 때마다 죽었는지 여부 체크해서 업데이트하기
*/

#include <iostream>
#include <cstring>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

struct turret {
	int r, c, power, time;
};

int n, m, k;
int grid[11][11];
int visited[11][11];
pair<int, int> path[11][11];
int isWar[11][11];

vector<turret> turret_list;
vector<turret> new_turret_list;

int dr[8] = { 0, 1, 1, 1, 0, -1, -1, -1 };
int dc[8] = { 1, 1, 0, -1, -1, -1, 0, 1 };


bool cmp(turret a, turret b) {
	if (a.power == b.power) {
		if (a.time == b.time) {
			if (a.r + a.c == b.r + b.c) {
				return a.c > b.c;
			}
			return a.r + a.c > b.r + b.c;
		}
		return a.time < b.time;
	}
	return a.power < b.power;
}


void init() {
	cin >> n >> m >> k;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			cin >> grid[i][j];
			if (grid[i][j] > 0)
				turret_list.push_back({ i, j, grid[i][j], 0 });
		}
	}
	sort(turret_list.begin(), turret_list.end(), cmp);
}


int find_laser_route(int sr, int sc, int er, int ec) {
	memset(visited, 0, sizeof(visited));
	memset(path, 0, sizeof(path));
	queue<pair<int, int>> q;
	q.push({ sr, sc });
	visited[sr][sc] = 1;

	while (!q.empty()) {
		int r = q.front().first, c = q.front().second;
		q.pop();

		for (int d = 0; d < 8; d += 2) {
			int nr = (r + dr[d] + n) % n, nc = (c + dc[d] + m) % m;
			if (!visited[nr][nc] && grid[nr][nc]) {
				path[nr][nc] = { r, c };
				q.push({ nr, nc });
				visited[nr][nc] = 1;
				if (nr == er && nc == ec)
					return 1;
			}
		}
	}
	return 0;
}


void bomb_attack(int sr, int sc, int er, int ec) {
	grid[er][ec] -= grid[sr][sc];
	int half_power = grid[sr][sc] / 2;
	for (int d = 0; d < 8; d++) {
		int nr = (er + dr[d] + n) % n, nc = (ec + dc[d] + m) % m;
		if (!grid[nr][nc])
			continue;
		isWar[nr][nc] = 1;
		if (nr == sr && sc == sc)
			continue;
		grid[nr][nc] -= half_power;
	}
}


void start_attack(turret attacker, turret defender) {
	int laser_attack = 0;
	// 2-1. 레이저 공격 시작
	laser_attack = find_laser_route(attacker.r, attacker.c, defender.r, defender.c);

	// 공격에 성공했다면, path 따라서 공격하기
	if (laser_attack) {
		int r = defender.r, c = defender.c;
		int half_power = grid[attacker.r][attacker.c] / 2;
		isWar[r][c] = 1;
		grid[r][c] -= grid[attacker.r][attacker.c];
		
		int nr, nc;
		while (!(r == attacker.r && c == attacker.c)) {
			nr = path[r][c].first, nc = path[r][c].second;
			if (nr == attacker.r && nc == attacker.c)
				break;
			isWar[nr][nc] = 1;
			grid[nr][nc] -= half_power;
			r = nr; c = nc;
		}
	}
	else {
		// 2-2. 폭탄 공격
		bomb_attack(attacker.r, attacker.c, defender.r, defender.c);
	}
}


void update_new_turret() {
	new_turret_list.clear();
	for (int idx = 0; idx < turret_list.size(); idx++) {
		int r = turret_list[idx].r, c = turret_list[idx].c;
		if (grid[r][c] <= 0) {
			grid[r][c] = 0;
		}
		else {
			if (!isWar[r][c]) {
				turret_list[idx].power++;
				grid[r][c]++;
			}
			else
				turret_list[idx].power = grid[r][c];
			if (idx)
				turret_list[idx].time++;
			new_turret_list.push_back(turret_list[idx]);
		}
	}
	turret_list.swap(new_turret_list);
	sort(turret_list.begin(), turret_list.end(), cmp);
}



void simulation() {
	while (k--) {
		memset(isWar, 0, sizeof(isWar));

		// 1. 공격자 선정
		turret attacker = turret_list.front();
		grid[attacker.r][attacker.c] += n + m;
		turret defender = turret_list.back();
		isWar[attacker.r][attacker.c] = 1; isWar[defender.r][defender.c] = 1;
		// 아직 터렛 리스트에 정보 업데이트 안 한 상태
	
		// 2. 공격자 공격
		start_attack(attacker, defender);

		// 3. 포탑 재정비
		update_new_turret();

		// 4. 터렛 하나 남았는지 확인
		if (turret_list.size() == 1)
			break;
	}

}


int main() {

	init();

	simulation();

	cout << turret_list.back().power << '\n';

	return 0;
}