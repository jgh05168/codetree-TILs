'''
수행할 수 있는 외주 작업이 하루에 한 개씩 존재
기한t, 수익p

외주 수익 최대값을 출력

기간 안에 조합하여 최댓값 찾기 = 백트래킹
n <= 15이기 때문에 조합으로 충분히 찾을 수 있을듯
수익이 큰 경우부터 넣어보는 방법으로 정렬한 뒤 진행
'''

import sys
input = sys.stdin.readline

n = int(input())
outgoing = []
for i in range(n):
    t, p = map(int, input().split())
    outgoing.append((t, p))

ans = 0
for i in range(n):
    tmp_ans = 0
    selected = [0] * n
    # 하나씩 놓아가면서 dp에 최댓값 채워넣기
    for j in range(i, n):
        t, p = outgoing[j]
        if not selected[j]:
            for k in range(t):
                selected[i + k] = 1
            tmp_ans += p

    ans = max(ans, tmp_ans)

print(ans)