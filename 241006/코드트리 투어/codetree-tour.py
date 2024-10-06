'''
양방향 그래프, 간선 여러개 존재(자신 포함)
- 출발지를 하나로 통일하여 관리한다. (첫 출발지는 0번)

[코드트리 랜드 건설]
연결리스트 생성하기

[여행 상품 생성]
(id, revenue, dest)에 해당하는 여행 상품을 생성하고, 관리 목록에 추가하기
- 고유한 식별자 id를 갖는다.

[여행 상품 취소]
고유 식별자 id에 해당하는 상품이 존재하는 경우, 관리 목록에서 삭제

[최적의 여행 상품 판매]
- 조건에 맞는 최적의 여행 상품을 선택하여 판매함
- 이득(매출 - 가격)이 최대인 상품을 우선적으로 고려함
- 같은 값을 가지는 상품이 여러개인 경우, id가 가장 작은 상품을 선택함
- cost는 현재 여행 상품의 출발지로부터 id상품의 도착지까지 도달하기 위한 최단거리를 의미함
- 출발지부터 목적지까지 도달이 불가능하거나, cost가 매출보다 커서 이득을 못본다면, 판매불가상품임
    - -1 출력

[출발지 변경]
출발지를 전부 s로 변경하기
- 각 상품의 cost를 변경해줘야 한다.

풀이:
출발지에서 각 목적지까지 다익스트라 진행
여행 상품을 저장할 우선순위큐에는 이득이 큰 순, id가 작은 순으로 정렬
각 여행상품은 클래스로 지정
    - __init__, __lt__, 이득을 계산하는 함수


'''

from collections import defaultdict
import heapq

# 전역 변수
cost = []
product_pq = []
product_available = defaultdict(int)
INF = float('inf')

class Product():
    def __init__(self, id, revenue, dest):
        self.id = id
        self.revenue = revenue
        self.dest = dest
        self.cost = cost[dest]
        profit = revenue - cost[dest]
        if cost[dest] == INF or profit < 0:
            self.profit = -1
        else:
            self.profit = profit

    def __lt__(self, other):
        if self.profit == other.profit:
            return self.id < other.id
        return self.profit > other.profit

    def update_profit(self):
        profit = self.revenue - cost[self.dest]
        if cost[self.dest] == INF or profit < 0:
            self.profit = -1
        else:
            self.profit = profit


def dijkstra(su):
    global cost
    pq = []
    cost = [INF] * n
    heapq.heappush(pq, (0, su))
    cost[su] = 0

    while pq:
        cur_w, u = heapq.heappop(pq)

        for v, w in land[u]:
            new_cost = cur_w + w
            if new_cost < cost[v]:
                heapq.heappush(pq, (new_cost, v))
                cost[v] = new_cost


Q = int(input())
# Query = 100은 무조건 주어짐
query = list(map(int, input().split()))
n, m, land_info = query[1], query[2], query[3:]
land = [[] * n for _ in range(n)]
for i in range(0, len(land_info), 3):
    u, v, w = land_info[i:i + 3]
    land[u].append((v, w))
    land[v].append((u, w))

# 출발지에서 다익스트라 진행
dijkstra(0)

# 명령 순차적으로 수행
for _ in range(Q - 1):
    query = list(map(int, input().split()))
    # 여행 상품 생성
    if query[0] == 200:
        id, revenue, dest = query[1:]
        heapq.heappush(product_pq, Product(id, revenue, dest))
        product_available[id] = 1
    # 여행 상품 취소
    elif query[0] == 300:
        id = query[1]
        product_available[id] = 0
    # 최적의 여행 상품 판매
    elif query[0] == 400:
        flag = 0
        while product_pq:
            if product_pq[0].profit < 0:
                break
            product = heapq.heappop(product_pq)
            if not product_available[product.id]:
                continue
            if product.profit >= 0:
                flag = 1
                print(product.id)
                product_available[product.id] = 0
                break
        if not flag:
            print(-1)
    elif query[0] == 500:
        startpoint = query[1]
        dijkstra(startpoint)
        for product in product_pq:
            product.update_profit()
        heapq.heapify(product_pq)