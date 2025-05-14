/*
20:05

n x n, 학생은 n^2명 존재한다.
초기에 신봉하는 음식은 F로 표현되고, T C M 중 하나이다.
다른 사람들에게 영향을 받음에 따라 조합이 생길 수도 있다.
각 학생들은 초기 신앙심을 가지고 있음 : B
T일동안 아 점 저 순서로 진행된다.

1. 아침 : 모든 학생은 신앙심을 1씩 얻는다.
	- B값에 1이 더해짐
2. 점심 : 인접한 학생들과 신봉 음식이 완전히 같은 경우에만 그룹을 형성한다.
	- 상하좌우
	- 그룹 안에서 대표자를 선정함. 
		- 신앙심 > 행, 열 작은 순
	- 대표자를 제외한 그룹원들은 각자 신앙심을 1씩 넘긴다. 
3. 저녁 : 모든 그룹의 대표자들이 신앙심을 전파한다.
	- 전파는 단일 -> 이중 -> 삼중 조합 순으로 진행된다.
	- 같은 그룹 내에서는 다음 기준으로 순서가 정해짐
		- 대표자 신앙심 > 행, 열 작은 순

	- 전파자는 신앙심 1만 남기고 나머지를 간절함 x=B - 1로 바꿔 전파에 사용한다.

	- 전파 방향은 B를 4로 나눈 나머지에 따라 결정된다.
		- 위 / 아래 / 왼 / 오
	- 전파자는 전파 방향으로 한 칸씩 이동하면서 전파 시도
	- 격자 밖 or 간절함 0이 되면 전파 종료
	
	- 전파 대상이 전파자와 신봉 음식이 같을 경우, 전파를 하지 않고 바로 다음으로 진행함
	- 전파 진행 시, 
		x > y라면 강한 전파 : 전파자는 간절함이 y + 1만큼 깎인다. 전파 대상의 신앙심은 1 증가한다.
			- 만약 전파자의 간절함이 0이 된다면 전파를 진행하지 않고 종료
		x <= y라면 약한 전파 : 전파자가 전파한 음식의 모든 기본 음식을 모두 합친 음식을 신앙하게 됨
			- 기존에 관심을 가지고 있던 기본 음식 + 전파자가 관심갖는 음식 모두 신봉함
			- 전파자는 간절함 0, 종료
	
	- 하루에 전파당한 학생이 있다면, 해당 학생은 즉시 방어상태가 되어 전파를 하지 않음.
		- 전파를 받는 것은 가능함

풀이 : 학생 node 생성해서 맵 만들기
node 정보 : 신앙심, 음식, 방어상태
bfs, 전파자 정보 저장을 위한 vector
*/


#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <queue>
#include <unordered_map>
#include <set>

using namespace std;

struct node {
	int faith, defender_mode;
	string food;
};

int N, T;
node classroom[51][51];
int visited[51][51];
vector<pair<int, pair<int, pair<int, int>>>> faith_sender;
unordered_map<string, int> output;

unordered_map<string, int> priority = { {"T", 0}, {"C", 0}, {"M", 0}, {"CM", 1}, {"TM", 1}, {"TC", 1}, {"TCM", 2} };
unordered_map<string, int> priority2 = { {"T", 6}, {"C", 5}, {"M", 4}, {"CM", 3}, {"TM", 2}, {"TC", 1}, {"TCM", 0} };
unordered_map<char, int> one_priority = { {'T', 0}, {'C', 1}, {'M', 2} };
int dr[4] = { -1, 1, 0, 0 };
int dc[4] = { 0, 0, -1, 1 };

bool isValid(int r, int c) {
	return 0 <= r && r < N && 0 <= c && c < N;
}


bool cmp(pair<int, pair<int, pair<int, int>>> a, pair<int, pair<int, pair<int, int>>> b) {
	if (a.first == b.first) {
		if (a.second.first == b.second.first) {
			if (a.second.second.first == b.second.second.first) {
				return a.second.second.second < b.second.second.second;
			}
			return a.second.second.first < b.second.second.first;
		}
		return a.second.first > b.second.first;
	}
	return a.first < b.first;
}

bool cmp2(char a, char b) {
	return one_priority[a] < one_priority[b];
}

bool cmp3(pair<string, int> a, pair<string, int> b) {
	return priority2[a.first] < priority2[b.first];
}

void init() {
	cin >> N >> T;
	string tmp;
	for (int i = 0; i < N; i++) {
		cin >> tmp;
		for (int j = 0; j < N; j++) {
			classroom[i][j].food += tmp[j];
		}
	}
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			cin >> classroom[i][j].faith;
		}
	}
}


void find_faith_sender(int sr, int sc) {
	queue<pair<int, int>> q;
	q.push({ sr, sc });
	visited[sr][sc] = 1;
	int max_faith = 0;
	int fr = N, fc = N;
	string cur_food = classroom[sr][sc].food;
	vector<pair<int, int>> food_group;

	while (!q.empty()) {
		int r = q.front().first, c = q.front().second;
		q.pop();

		if (max_faith < classroom[r][c].faith) {
			max_faith = classroom[r][c].faith;
			fr = r; fc = c;
		}
		else if (max_faith == classroom[r][c].faith) {
			if (r < fr) {
				fr = r, fc = c;
			}
			else if (r == fr && c < fc) {
				fr = r, fc = c;
			}
		}
		food_group.push_back({ r, c });

		for (int d = 0; d < 4; d++) {
			int nr = r + dr[d], nc = c + dc[d];
			if (isValid(nr, nc) && !visited[nr][nc] && classroom[nr][nc].food == cur_food) {
				q.push({ nr, nc });
				visited[nr][nc] = 1;
			}
		}
	}

	// 	대표자를 제외한 그룹원들은 각자 신앙심을 1씩 넘긴다. 
	for (auto person : food_group) {
		int r = person.first, c = person.second;
		if (r == fr && c == fc)
			continue;
		classroom[r][c].faith--;
		classroom[fr][fc].faith++;
	}
	faith_sender.push_back({ priority[cur_food], {classroom[fr][fc].faith, {fr, fc}} });
}



void send_faith(int sr, int sc) {
	// 	전파자는 신앙심 1만 남기고 나머지를 간절함 x=B - 1로 바꿔 전파에 사용한다.
	int falling_power = classroom[sr][sc].faith - 1;
	classroom[sr][sc].faith = 1;
	int dir = (falling_power + 1) % 4;
	string cur_food = classroom[sr][sc].food;
	/*
	- 격자 밖 or 간절함 0이 되면 전파 종료
	
	- 전파 대상이 전파자와 신봉 음식이 같을 경우, 전파를 하지 않고 바로 다음으로 진행함
	- 전파 진행 시, 
		x > y라면 강한 전파 : 전파자는 간절함이 y + 1만큼 깎인다. 전파 대상의 신앙심은 1 증가한다.
			- 만약 전파자의 간절함이 0이 된다면 전파를 진행하지 않고 종료
		x <= y라면 약한 전파 : 전파자가 전파한 음식의 모든 기본 음식을 모두 합친 음식을 신앙하게 됨
			- 기존에 관심을 가지고 있던 기본 음식 + 전파자가 관심갖는 음식 모두 신봉함
			- 전파자는 간절함 0, 종료
	*/
	int r = sr, c = sc;
	while (1) {
		int nr = r + dr[dir], nc = c + dc[dir];
		// 탐사 종료 조건
		if (!isValid(nr, nc) || !falling_power)
			break;
		// 같을 경우는 그냥 지나감
		if (classroom[nr][nc].food == cur_food) {
			r = nr, c = nc;
			continue;
		}
		// 강한 전파
		if (falling_power > classroom[nr][nc].faith) {
			falling_power -= classroom[nr][nc].faith + 1;
			classroom[nr][nc].faith += 1;
			classroom[nr][nc].food = cur_food;
		}
		// 약한 전파
		else {
			set<char> food_set;
			for (int i = 0; i < classroom[nr][nc].food.length(); i++) {
				food_set.insert(classroom[nr][nc].food[i]);
			}
			for (int i = 0; i < cur_food.length(); i++) {
				food_set.insert(cur_food[i]);
			}

			// 음식 조합하기
			vector<char> make_new_food;
			for (auto now_food : food_set) {
				make_new_food.push_back(now_food);
			}
			sort(make_new_food.begin(), make_new_food.end(), cmp2);

			string new_food = "";
			for (auto f : make_new_food) {
				new_food += f;
			}

			classroom[nr][nc].food = new_food;
			classroom[nr][nc].faith += falling_power;
			falling_power = 0;
		}
		r = nr, c = nc;
		classroom[nr][nc].defender_mode = 1;
	}

}



void simulation() {
	while (T--) {
		// 0. 변수 초기화
		output.clear();
		for (auto f : priority) {
			output[f.first] = 0;
		}
		faith_sender.clear();


		/* 1. 아침 : 모든 학생은 신앙심을 1씩 얻는다. */
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				classroom[i][j].faith++;
			}
		}

		/* 2. 점심 : 인접한 학생들과 신봉 음식이 완전히 같은 경우에만 그룹을 형성한다. */
		memset(visited, 0, sizeof(visited));
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				if (!visited[i][j]) {
					find_faith_sender(i, j);
				}
			}
		}

		/* 3. 저녁 : 모든 그룹의 대표자들이 신앙심을 전파한다. */
		// 3-1. 대표자 우선순위를 위한 sort
		sort(faith_sender.begin(), faith_sender.end(), cmp);
		// 3-2. 전파 시작
		for (auto faith_man : faith_sender) {
			int r = faith_man.second.second.first, c = faith_man.second.second.second;
			if (classroom[r][c].defender_mode)
				continue;
			send_faith(r, c);
		}

		/* 4. 점수 산정 */
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				output[classroom[i][j].food] += classroom[i][j].faith;
				classroom[i][j].defender_mode = 0;
			}
		}
		vector<pair<string, int>> answer;
		for (auto o : output) {
			answer.push_back({ o.first, o.second });
		}
		sort(answer.begin(), answer.end(), cmp3);

		for (auto ans : answer) {
			cout << ans.second << ' ';
		}
		cout << '\n';
	}

}





int main() {
	init();

	simulation();
}



