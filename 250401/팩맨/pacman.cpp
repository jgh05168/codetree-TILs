/*
09:05 시작

4 x 4 격자, 8방향, 턴 단위로 진행됨

1. 몬스터 복제 시도
- 현재 위치에서 자신과 같은 방향을 가진 몬스터를 복제함
- 아직 부화되지 않은 상태로 움직일 수 없음(알 상태임)
2. 몬스터 이동
- 현재 자신이 가진 방향으로 한 칸 이동
- 움직이려는 칸에 몬스터 시체가 있거나 팩맨이 있으면 반시계 방향으로 45도 회전
- 갈 수 있는 곳이 없다면 움직이지 않는다.
- 몬스터는 같은 위치에 존재할 수 있음
3. 팩맨 이동
- 총 3칸 이동하는데, 상하좌우 선택지를 갖는다.
- 몬스터를 가장 많이 먹을 수 있는 방향으로 움직임
- 최대 처치수가 동일하다면 상 좌 하 우 우선순위를 갖는다
- 알은 먹지 않음. 움직이기 전에 함께 있던 몬스터도 먹지 않음
4. 몬스터 시체 소멸
-시체는 2턴동안만 유지된다. 시체가 소멸되기까지 2턴이 필요함
5. 몬스터 복제 완성
- 알 형태였던 몬스터가 부화함

풀이 : 
고려 사항 : 
1. 복제되는 몬스터들 어떤 메모리에서 관리 ? 정적 ? or vector ? 
2. 팩맨이 죽인 몬스터들 어떻게 체크할것 ? -> 팩맨이 이동한 위치 정보를 기반으로 몬스터들 for문 돌면서 체크

몬스터 정보 : r, c, d, isDead
몬스터 마리 수 grid, 시체 grid
*/

#include <iostream>
#include <cstring>
#include <vector>
#include <set>
#define MON_SIZE 1000001
#define GRID_SIZE 4

using namespace std;

struct monster {
	int r, c, d;
};

int m, t;
int packman_r, packman_c;
int mon_cnt[GRID_SIZE][GRID_SIZE];
int mon_soul[GRID_SIZE][GRID_SIZE];
int mon_eggs[GRID_SIZE][GRID_SIZE];
int packman_path[GRID_SIZE][GRID_SIZE];
vector<monster> monster_list;
vector<monster> egg_list;

int dr[8] = { -1, -1, 0, 1, 1, 1, 0, -1 };
int dc[8] = { 0, -1, -1, -1, 0, 1, 1, 1 };

bool isValid(int r, int c) {
	return 0 <= r && r < GRID_SIZE && 0 <= c && c < GRID_SIZE;
}


void init() {
	memset(mon_cnt, 0, sizeof(mon_cnt));
	memset(mon_soul, 0, sizeof(mon_soul));
	memset(mon_eggs, 0, sizeof(mon_eggs));

	cin >> m >> t;
	cin >> packman_r >> packman_c;
	packman_r--, packman_c--;
	int r, c, d;
	for (int i = 0; i < m; i++) {
		cin >> r >> c >> d;
		monster_list.push_back({ r - 1, c - 1, d - 1 });
		mon_cnt[r - 1][c - 1]++;
	}
}

void get_eggs() {
	egg_list.clear();
	for (int idx = 0; idx < m; idx++) {
		egg_list.push_back(monster_list[idx]);
		mon_eggs[monster_list[idx].r][monster_list[idx].c] = 1;
	}
}

void move_monsters() {
	for (int idx = 0; idx < m; idx++) {
		int r = monster_list[idx].r, c = monster_list[idx].c;
		for (int d = 0; d < 8; d++) {
			int nr = r + dr[(monster_list[idx].d + d) % 8], nc = c + dc[(monster_list[idx].d + d) % 8];
			if (isValid(nr, nc) && !mon_soul[nr][nc] && !(nr == packman_r && nc == packman_c)) {
				monster_list[idx].d = (monster_list[idx].d + d) % 8;
				monster_list[idx].r = nr, monster_list[idx].c = nc;
				mon_cnt[nr][nc]++; mon_cnt[r][c]--;
				break;
			}
		}

	}
}


void move_packman() {
	// 3번 이동해야함
	int r = packman_r, c = packman_c;
	int max_eat = 0;
	pair<int, int> tmp_move[3];
	// 첫번째
	for (int d1 = 0; d1 < 8; d1 += 2) {
		int nr1 = r + dr[d1], nc1 = c + dc[d1];
		if (isValid(nr1, nc1)) {
			// 두번째
			for (int d2 = 0; d2 < 8; d2 += 2) {
				int nr2 = nr1 + dr[d2], nc2 = nc1 + dc[d2];
				if (isValid(nr2, nc2)) {
					// 세번째
					for (int d3 = 0; d3 < 8; d3 += 2) {
						int nr3 = nr2 + dr[d3], nc3 = nc2 + dc[d3];
						if (isValid(nr3, nc3)) {
							set<pair<int, int>> s;
							s.insert({ nr1, nc1 });
							s.insert({ nr2, nc2 });
							s.insert({ nr3, nc3 });
							int total_eat = 0;
							for (auto tmp : s)
								total_eat += mon_cnt[tmp.first][tmp.second];
							if (max_eat < total_eat) {
								max_eat = total_eat;
								tmp_move[0] = { nr1, nc1 };
								tmp_move[1] = { nr2, nc2 };
								tmp_move[2] = { nr3, nc3 };
							}
						}
					}
				}
			}
		}
	}

	// 최종 결산
	for (int idx = 0; idx < 3; idx++) {
		if (mon_cnt[tmp_move[idx].first][tmp_move[idx].second]) {
			mon_cnt[tmp_move[idx].first][tmp_move[idx].second] = 0;
			mon_soul[tmp_move[idx].first][tmp_move[idx].second] = 3;	// 현재 턴 제외 2턴 지나야 함
		}
		packman_path[tmp_move[idx].first][tmp_move[idx].second] = 1;
	}
	packman_r = tmp_move[2].first;
	packman_c = tmp_move[2].second;
}


void update_monster() {
	vector<monster> tmp;
	for (int idx = 0; idx < m; idx++) {
		if (packman_path[monster_list[idx].r][monster_list[idx].c])
			continue;
		tmp.push_back(monster_list[idx]);
	}
	for (int idx = 0; idx < egg_list.size(); idx++) {
		tmp.push_back(egg_list[idx]);
		mon_cnt[egg_list[idx].r][egg_list[idx].c]++;
	}

	monster_list.swap(tmp);
	m = monster_list.size();
}


int solution() {
	while (t--) {
		// 1. 몬스터 복제 시도
		get_eggs();

		// 2. 몬스터 이동
		move_monsters();

		// 3. 팩맨 이동 (알은 먹지 않음)
		memset(packman_path, 0, sizeof(packman_path));
		move_packman();

		// 4. 몬스터 시체 소멸
		for (int i = 0; i < GRID_SIZE; i++) {
			for (int j = 0; j < GRID_SIZE; j++) {
				if (mon_soul[i][j])
					mon_soul[i][j]--;
			}
		}

		// 5. 몬스터 업데이트
		update_monster();
	}

	// 6. 최종 몬스터 마리수 체크
	return monster_list.size();
}


int main() {
	init();

	cout << solution() << '\n';

	return 0;
}