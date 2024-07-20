'''
수행할 수 있는 외주 작업이 하루에 한 개씩 존재
기한t, 수익p

외주 수익 최대값을 출력

dp, 최댓값 업데이트 해주는 방식으로 진행
'''

import sys
input = sys.stdin.readline

n = int(input())
outgoing = []
for i in range(n):
    t, p = map(int, input().split())
    outgoing.append((t, p))

dp = [0] * (n + 1)
for i in range(n - 1, -1, -1):
    # 일을 할 수 있다면
    if i + outgoing[i][0] <= n:
        dp[i] = max(dp[i + outgoing[i][0]] + outgoing[i][1], dp[i + 1])
    else:
        dp[i] = dp[i + 1]

print(dp[0])