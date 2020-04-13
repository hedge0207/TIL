#메모이제이션 예제
def fib_memo(n, cache):
    # 코드를 작성하세요.
    if n < 3:
        return 1
    elif cache[n] == -1:
        cache[n] = fib_memo(n-1, cache) + fib_memo(n-2, cache)
    return cache[n]
def fib(n):
    # n번째 피보나치 수를 담는 사전
    fib_cache = [-1]*(n+1)

    return fib_memo(n, fib_cache)


# 테스트
print(fib(10))
print(fib(50))
print(fib(100))



#타뷸레이션 예제
# def fib_tab(n):
#     # 코드를 작성하세요.
#     table = [1,1]
#     for i in range(n):
#         if i > 1:
#             table.append(table[i-1]+table[i-2]) #n 번째 피보나치 수를 구하는 데 처음부터 n 번째 이전의 n-2, n-1 값을 구하는 것이 아니라 테이블에 있는 n-2, n-1의 값을 인덱스로 접근하여 꺼내온다.
#     return table[n-1]
#
# # 테스트
# print(fib_tab(10))
# print(fib_tab(56))
# print(fib_tab(132))





#공간최적화 예제
# def fib_optimized(n):
#     # 코드를 작성하세요.
#     current = 1
#     previous = 0
#     for i in range(n-1): #이미 current가 1이기 때문에 한번 덜 반복해야 한다.
#         current = current+previous
#         previous = current-previous
#     return current
#
#
# # 테스트
# print(fib_optimized(16))
# print(fib_optimized(53))
# print(fib_optimized(213))





#새꼼달꼼 장사
# 가능한 최대 수익을 리턴시켜 주는 함수를 작성해 보세요
# price_list가 [100, 400, 800, 900, 1000]이라면,
# 새꼼달꼼 1개에 100원
# 새꼼달꼼 2개에 400원
# 새꼼달꼼 3개에 800원
# 새꼼달꼼 4개에 900원
# 새꼼달꼼 5개에 1000원
# 이렇게 가격이 책정된 건데요. 만약 오늘 솔희가 새꼼달꼼 5개를 판매한다면 최대로 얼마를 벌 수 있을까요?
# 한 친구에게 3개 팔고 다른 친구에게 2개를 팔면, 800+400을 해서 총 1200원의 수익을 낼 수 있겠죠.

#새꼼달꼼 장사(메모이제이션 활용)
#못풀었음

# #해답
# def max_memo(pl, cnt, dic):
#     # Base Case: 0개 혹은 1개면 부분 문제로 나눌 필요가 없기 때문에 가격을 바로 리턴한다
#     if cnt < 2:
#         dic[cnt] = pl[cnt]
#         return pl[cnt]
#
#     # 이미 계산한 값이면 cache에 저장된 값을 리턴한다
#     if cnt in dic:
#         return dic[cnt]
#
#     # maxx은 count개를 팔아서 가능한 최대 수익을 저장하는 변수
#     # 팔려고 하는 총개수에 대한 가격이 pl에 없으면 일단 0으로 설정
#     # 팔려고 하는 총개수에 대한 가격이 pl에 있으면 일단 그 가격으로 설정
#     if cnt < len(pl):
#         maxx = pl[cnt]
#     else:
#         maxx = 0
#
#     # cnt개를 팔 수 있는 조합들을 비교해서, 가능한 최대 수익을 maxx에 저장
#     for i in range(1, cnt // 2 + 1):                #([0, 100, 400, 800, 900, 1000], 5,{})의 경우
#         maxx = max(maxx, max_memo(pl, i, dic) + max_memo(pl, cnt - i, dic))  #각기 i, i-1값은 각각 (1,4),(2,3)가 된다. 즉, 모든 가능한 조합이 된다.
#
#     # 계산된 최대 수익을 dic에 저장
#     dic[cnt] = maxx
#
#     return maxx
#
#
# # 테스트
# print(max_memo([0, 100, 400, 800, 900, 1000], 5,{}))
# print(max_memo([0, 100, 400, 800, 900, 1000], 10,{}))
# print(max_memo([0, 100, 400, 800, 900, 1000, 1400, 1600, 2100, 2200], 9,{}))





#새꼼달꼼 장사(타뷸레이션 활용)
#못풀었음

#해답
# def max_profit(price_list, count):
#     # 개수별로 가능한 최대 수익을 저장하는 리스트
#     # 새꼼달꼼 0개면 0원
#     profit_table = [0]
#
#     # 개수 1부터 count까지 계산하기 위해 반복문
#     for i in range(1, count + 1):
#         # profit은 count개를 팔아서 가능한 최대 수익을 저장하는 변수
#         # 팔려고 하는 총개수에 대한 가격이 price_list에 있으면 일단 그 가격으로 설정
#         # 팔려고 하는 총개수에 대한 가격이 price_list에 없으면 일단 0으로 설정
#         if i < len(price_list):
#             profit = price_list[i]
#         else:
#             profit = 0
#
#         # count개를 팔 수 있는 조합들을 비교해서, 가능한 최대 수익을 찾는다
#         for j in range(1, i // 2 + 1):
#             profit = max(profit, profit_table[j] + profit_table[i - j])
#
#         profit_table.append(profit)
#
#     return profit_table[count]
#
#
# # 테스트
# print(max_profit([0, 200, 600, 900, 1200, 2000], 5))
# print(max_profit([0, 300, 600, 700, 1100, 1400], 8))
# print(max_profit([0, 100, 200, 400, 600, 900, 1200, 1300, 1500, 1800], 9))