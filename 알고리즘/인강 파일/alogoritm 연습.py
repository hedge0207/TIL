# 투자 귀재 규식이
# 특정 기간 중 수익이 가장 큰 구간을 찾아내는 함수 sublist_max를 작성해 보려고 합니다.
# Brute Force 방법을 이용해서 이 문제를 한 번 풀어봅시다!
# sublist_max는 파라미터로 리스트 profits를 받는데요. profits에는 며칠 동안의 수익이 담겨 있습니다.
# 예를 들어서 profits가 [7, -3, 4, -8]이라면 첫 날에는 7달러를 벌었고, 둘째 날에는 3달러를 잃었고, 셋째 날에는 4달러를 벌었고, 마지막 날에는 8달러를 잃은 거죠.
# sublist_max 함수는 profits에서 최대 수익을 내는 구간의 수익을 리턴합니다.
# profits가 [7, -3, 4, -8]이라면 무엇을 리턴해야 할까요? profits에서 가장 많은 수익을 낸 구간은 [7, -3, 4]입니다. 이 구간에서 낸 수익은 8달러이니, 8을 리턴하면 되겠죠!
# 만약 profits가 [-2, -3, 4, -1, -2, 1, 5, -3]이라면? profits에서 수익이 가장 큰 구간은 [4, -1, -2, 1, 5]입니다. 이 구간에서 낸 수익은 7달러이니, 7을 리턴하겠죠?

# def sublist_max(profits):
#     # 코드를 작성하세요.
#     maxx = max(profits)
#     suml = []
#     for i in range(1, len(profits) + 1):
#         a = 0
#         for j in range(i):
#             a += profits[j]
#         if a > maxx:
#             maxx = a
#
#         a = 0
#         for j in range(i, len(profits)):
#             a += profits[j]
#             if a > maxx:
#                 maxx = a
#
#         a = 0
#         for j in range(i, len(profits) - i):
#             a += profits[j]
#             if a > maxx:
#                 maxx = a
#
#     return maxx
#
#
# # 테스트
# print(sublist_max([4, 3, 8, -2, -5, -3, -5, -3]))
# print(sublist_max([2, 3, 1, -1, -2, 5, -1, -1]))
# print(sublist_max([7, -3, 14, -8, -5, 6, 8, -5, -4, 10, -1, 8]))
# print(sublist_max([7, 18, 14, -39, -10, 21, 24, 15, -30, 10, -1, 8]))





# 거듭 제곱을 계산하는 함수 power를 작성하고 싶습니다. power는 파라미터로 자연수 x와 자연수 y를 받고, xy를 리턴합니다.
# 주의: return x ** y는 답이 아닙니다. 우리는 거듭 제곱을 구하는 원리를 파악하여 효율적인 ‘알고리즘’을 구현하고 싶은 것입니다.
# def power(x, y):
#     # 코드를 작성하세요.
#     if y == 1:
#         return x
#     return power(x,y-1)*x
#
# # 테스트
# print(power(3, 5))
# print(power(5, 6))
# print(power(7, 9))




# 신입 사원 장그래는 마부장님을 따라 등산을 가게 되었습니다.
# 탈수를 방지하기 위해서 1km당 1L의 물을 반드시 마셔야 하는데요. 다행히 등산길 곳곳에는 물통을 채울 수 있는 약수터가 마련되어 있습니다.
# 다만 매번 줄서 기다려야 한다는 번거로움이 있기 때문에, 시간을 아끼기 위해서는 최대한 적은 약수터를 들르고 싶습니다.
# 함수 select_stops는 파라미터로 약수터 위치 리스트 water_stops와 물통 용량 capacity를 받고, 장그래가 들를 약수터 위치 리스트를 리턴합니다. 앞서 설명한 대로 약수터는 최대한 적게 들러야겠죠.
# 참고로 모든 위치는 km 단위이고 용량은 L 단위입니다. 그리고 등산하기 전에는 이미 물통이 가득 채워져 있으며, 약수터에 들르면 늘 물통을 가득 채운다고 가정합시다.
# 처음에 4L의 물통이 채워져 있기 때문에, 장그래는 약수터에 들르지 않고 최대 4km 지점까지 올라갈 수 있습니다. 탈수 없이 계속 올라가기 위해서는 1km 지점이나 4km 지점에서 물통을 채워야겠죠?
# 최대한 적은 약수터를 들르면서 올라가야 하고, 마지막에 산 정상인 26km 지점의 약수터를 들르면 성공적인 등산입니다.

#26km 약수터에 가장 효율적으로 가는 방법은 이렇습니다.
# 24km 약수터까지 최대한 효율적으로 가는 방법 + 24km 약수터
# 22km 약수터까지 최대한 효율적으로 가는 방법 + 22km 약수터
# 이 두 방법 중 더 효율적인 방법을 선택하면 되겠네요.
# 부분 문제의 최적의 솔루션을 이용해서 기존 문제의 최적의 솔루션을 구할 수 있기 때문에, 이 문제에는 최적 부분 구조가 있습니다.
#항상 가능한 먼 약수터로 가는 것이 가장 좋은 선택이라고 확신할 수 있기 때문에, 이 문제에는 탐욕적 선택 속성이 있습니다. 따라서 이 문제는 Greedy Algorithm을 이용해서 효율적으로 해결할 수 있는 거죠!

# def select_stops(water_stops, capacity):
#     # 코드를 작성하세요.
#     a = capacity
#     v = []
#     for i in range(len(water_stops)-1):
#         if i == 0:
#             capacity-=water_stops[i]
#         else:
#             capacity -= water_stops[i]-water_stops[i-1]
#         if capacity < water_stops[i+1]-water_stops[i]:
#             capacity = a
#             v.append(water_stops[i])
#     v.append(water_stops[-1])
#     return v
#
#
# # 테스트
# list1 = [1, 4, 5, 7, 11, 12, 13, 16, 18, 20, 22, 24, 26]
# print(select_stops(list1, 4))
#
# list2 = [5, 8, 12, 17, 20, 22, 23, 24, 28, 32, 38, 42, 44, 47]
# print(select_stops(list2, 6))


#해답
# def select_stops(water_stops, capacity):
#     # 약수터 위치 리스트
#     stop_list = []
#     # 마지막 들른 약수터 위치
#     prev_stop = 0
#
#
#     for i in range(len(water_stops)):
#         # i 지점까지 갈 수 없으면, i - 1 지점 약수터를 들른다
#         if water_stops[i] - prev_stop > capacity:
#             stop_list.append(water_stops[i - 1])
#             prev_stop = water_stops[i - 1]
#
#     # 마지막 약수터는 무조건 간다
#     stop_list.append(water_stops[-1])
#
#     return stop_list
#
#
# list1 = [1, 4, 5, 7, 11, 12, 13, 16, 18, 20, 22, 24, 26]
# print(select_stops(list1, 4))
#
# list2 = [5, 8, 12, 17, 20, 22, 23, 24, 28, 32, 38, 42, 44, 47]
# print(select_stops(list2, 6))


#중복되는 수 찾기
# def find_same_number(some_list):
#     # 코드를 쓰세요
#     be = []
#     al = []
#     for i in some_list:
#         if i not in be:
#             be.append(i)
#         else:
#             al.append(i)
#     return al[0]
#
#
#
#
# # 중복되는 수 ‘하나’만 리턴합니다.
# print(find_same_number([1, 4, 3, 5, 3, 2]))
# print(find_same_number([4, 1, 5, 2, 3, 5]))
# print(find_same_number([5, 2, 3, 4, 1, 6, 7, 8, 9, 3]))