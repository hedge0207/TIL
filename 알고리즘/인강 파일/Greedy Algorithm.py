#동전을 최소한으로 사용해서 동전 거슬러 주기
# def min_coin_count(value, coin_list):
#     # 코드를 작성하세요.
#     cnt = 0
#     while value != 0:
#         if value >= coin_list[1]:
#             cnt+=1
#             value-=coin_list[1]
#         elif value >= coin_list[0]:
#             cnt += 1
#             value-=coin_list[0]
#         elif value >= coin_list[3]:
#             cnt += 1
#             value -= coin_list[3]
#         elif value >= coin_list[2]:
#             cnt += 1
#             value -= coin_list[2]
#         # print(value)
#     return cnt
#
# # 테스트
# default_coin_list = [100, 500, 10, 50]
# print(min_coin_count(1440, default_coin_list))
# print(min_coin_count(1700, default_coin_list))
# print(min_coin_count(23520, default_coin_list))
# print(min_coin_count(32590, default_coin_list))


#해답
# def min_coin_count(value, coin_list):
#     # 누적 동전 개수
#     count = 0
#
#     # coin_list의 값들을 큰 순서대로 본다
#     for coin in sorted(coin_list, reverse=True):
#         # 현재 동전으로 몇 개 거슬러 줄 수 있는지 확인한다
#         count += (value // coin)
#
#         # 잔액을 계산한다
#         value %= coin
#
#     return count





#리스트 속 리스트에서 숫자를 하나씩 뽑아서 숫자들을 곱했을 때 때 최대곱이 되면 리턴
#이 문제의 최적 부분 구조 tc2를 예로 들면 [[9, 7, 8], [9, 2, 3], [9, 8, 1], [2, 8, 3], [1, 3, 6], [7, 7, 4]]를 구하기 위해서는
# [[9, 7, 8], [9, 2, 3], [9, 8, 1], [2, 8, 3], [1, 3, 6]]의 최대곱을 a라 했을 때 a와 7,7,4를 곱해야 최대곱이 출력된다. 마찬가지로 a는
# [[9, 7, 8], [9, 2, 3], [9, 8, 1], [2, 8, 3]]의 최대곱을 b라 했을 때 b*1,b*3,b*6 중 최대곱이 a가 된다. 따라서 최적 부분 구조가 존재한다.
#이 문제의 탐욕적 선택 속성은 각 리스트에서 최댓값만 뽑아서 곱하면 최대곱이 보장되므로 탐욕적 선택 속성 역시 존재한다.
# def max_product(card_lists):
#     # 코드를 작성하세요.
#     maxl = []
#     for i in range(len(card_lists)):
#         maxx = 0
#         for j in range(3):
#             maxx = max(maxx,card_lists[i][j])
#         maxl.append(maxx)
#     sol = 1
#     for i in maxl:
#         sol *= i
#
#     return sol
#
# # 테스트
# test_cards1 = [[1, 6, 5], [4, 2, 3]]
# print(max_product(test_cards1))
#
# test_cards2 = [[9, 7, 8], [9, 2, 3], [9, 8, 1], [2, 8, 3], [1, 3, 6], [7, 7, 4]]
# print(max_product(test_cards2))
#
# test_cards3 = [[1, 2, 3], [4, 6, 1], [8, 2, 4], [3, 2, 5], [5, 2, 3], [3, 2, 1]]
# print(max_product(test_cards3))
#
# test_cards4 = [[5, 5, 5], [4, 3, 5], [1, 1, 1], [9, 8, 3], [2, 8, 4], [5, 7, 4]]
# print(max_product(test_cards4))


#해답
# def max_product(card_lists):
#     # 누적된 곱을 저장하는 변수
#     product = 1
#
#     # 반복문을 돌면서 카드 뭉치를 하나씩 본다
#     for card_list in card_lists:
#         # product에 각 뭉치의 최댓값을 곱해 준다
#         product *= max(card_list)
#
#     return product






#익중이네 밴드부는 매주 수요일 오후 6시에 합주를 하는데요. 멤버들이 너무 상습적으로 늦어서, 1분에 1달러씩 내야 하는 벌금 제도를 도입했습니다.
# 그런데 마침 익중이와 친구 넷이 놀다가 또 지각할 위기입니다. 아직 악보도 출력해 놓지 않은 상황이죠.
# 어차피 같이 놀다 늦은 것이니 벌금을 다섯 명이서 똑같이 나눠 내기로 하고, 벌금을 가능한 적게 내는 방법을 고민해 보기로 합니다.
# 다섯 사람이 각각 출력해야 하는 페이지 수는 3장, 1장, 4장, 3장, 2장입니다. 프린터는 한 대밖에 없고, 1장을 출력하기 위해서는 1분이 걸립니다.
# 현재 순서대로 출력한다면,
# 첫 번째 사람: 3분 지각
# 두 번째 사람: 3+1분 지각
# 세 번째 사람: 3+1+4분 지각
# 네 번째 사람: 3+1+4+3분 지각
# 다섯 번째 사람: 3+1+4+3+2분 지각
# 총 39달러의 벌금을 내야 합니다.
# 흠… 더 적게 내는 방법이 있지 않을까요?
# 출력할 페이지 수가 담긴 리스트 pages_to_print를 파라미터로 받고 최소 벌금을 리턴해 주는 함수 min_fee를 Greedy Algorithm으로 구현하세요.
# 위에서 보다 싶이 처음에 어떤 사람이 뽑느냐에 따라 부분문제가 갈리게 된다. 이 부분문제들의 해답을 찾아서 이를 비교함으로써 기존 문제의 해답을 구할 수 있다. 따라서 최적 부분 구조가 존재한다.
# 또한 가장 시간이 적게 걸리는 사람 부터 출력을 하면 최적의 답이 보장되므로 탐욕적 선택 속성도 존재한다.

# def min_fee(pages_to_print):
#     # 코드를 작성하세요.
#     a = sorted(pages_to_print)
#     slate = 0
#     for i in range(1,len(a)+1):
#         b = 0
#         for j in range(i):
#             slate += a[j]
#     return slate
#
#
# # 테스트
# print(min_fee([6, 11, 4, 1]))
# print(min_fee([3, 2, 1]))
# print(min_fee([3, 1, 4, 3, 2]))
# print(min_fee([8, 4, 2, 3, 9, 23, 6, 8]))

#해답
# def min_fee(pages_to_print):
#     # 인풋으로 받은 리스트를 정렬시켜 준다
#     sorted_list = sorted(pages_to_print)
#
#     # 총 벌금을 담을 변수
#     total_fee = 0
#
#     # 정렬된 리스트에서 총 벌금 계산
#     for i in range(len(sorted_list)):
#         total_fee += sorted_list[i] * (len(sorted_list) - i) #뒷 사람들은 모두 sorted_list[i] 만큼 지각을 하므로* (len(sorted_list) - i)를 해준다.
#
#     return total_fee






# 리스트에 담겨있는 튜플들은 각각 하나의 수업을 나타냅니다. 각 튜플의 0번째 항목은 해당 수업의 시작 시간, 그리고 1 번 항목은 해당 수업이 끝나는 시간입니다.
# 예를 들어서 0번 인덱스에 있는 튜플값은 (4, 7)이니까, 해당 수업은 4교시에 시작해서 7교시에 끝나는 거죠.
# (2, 5)를 듣는다고 가정합시다. (4, 7) 수업은 (2, 5)가 끝나기 전에 시작하기 때문에, 두 수업은 같이 들을 수 없습니다. 반면, 수업 (1, 3)과 (4, 7)은 시간이 겹치지 않기 때문에 동시에 들을 수 있습니다.
# 열정이 불타오르는 신입생 지웅이는 최대한 많은 수업을 들을 수 있는 수업 조합을 찾아주는 함수 course_selection 함수를 작성하려고 합니다.
# course_selection은 파라미터로 전체 수업 리스트를 받고 가능한 많은 수업을 담은 리스트를 리턴합니다.
# (단, (2, 5), (5, 7)과 같이 5교시에 끝나는 수업과 5교시에 시작하는 수업은 서로 같이 듣지 못한다고 가정합니다)

# 이 문제의 최적 부분 구조
#[(4, 7), (2, 5), (1, 3), (8, 10)]라고 가정했을 때 (4, 7)을 먼저 선택했다고 가정하면 우선 (4, 7)과 겹치는 수업들을 제외해야 한다.
# (2, 5)만 겹치기 때문에 이제 [(1, 3), (8, 10)] 중에서 또 수업을 고르면 된다.
# 이번에는 (2, 5)를 먼저 선택했다고 가정했을 때, (2, 5)와 겹치는 수업은 (4, 7)과 (1, 3)이다. 따라서 이제 [(8, 10)] 밖에 고를 것이 없다.
# 즉 첫 수업으로 몇 번째 수업을 골랐는가에 따라 총 5가지의 부분문제가 나올 수 있고 이 부분문제들의 답을 구하고 이를 비교하여 기존문제의 답을 구할 수 있으므로 최적 부분구조가 존재한다.

# 탐욕적 선택 속성
# 남은 수업 중 가장 먼저 끝나는 수업을 선택하면, 늘 최선의 결과를 이뤄낼 수 있다. 따라서 탐욕적 선택 속성이 존재한다.

#위와 같은 탐욕적 선택 속성을 찾는 과정
#이 문제에서 매 단계마다 가장 좋아 보이는 선택은 무엇일까요?

# 가장 먼저 시작하는 수업을 고른다.
# 겹치는 수업이 가장 적은 수업을 고른다.
# 가장 짧은 수업을 고른다.
# 가장 먼저 끝나는 수업을 고른다.
# 이 네 가지 정도가 있는데요. 어떤 방법을 선택하는 게 가장 좋을까요?

# 각 경우에 대해서 반례(틀리다고 증명하는 예시)를 찾아봅시다.
# [(2, 5), (8, 10), (5, 9), (1, 16), (2, 6), (13, 16), (9, 11)]
# 가장 먼저 시작하는 수업을 고른다. 가장 일찍 시작하는 수업인 (1, 16)을 선택하면, 나머지 모든 수업들을 못 듣게 됩니다.
# 겹치는 수업이 가장 적은 수업을 고른다. 가장 적게 겹치는 수업부터 고르면 [(6, 9), (2, 5), (10, 13)]을 듣게 됩니다. 하지만 실제로는 [(1, 3), (4, 7), (8, 11), (12, 14)]와 같이 4개의 수업을 들을 수 있죠.
# 가장 짧은 수업을 고른다. 가장 짧은 수업인 (5, 8)을 선택하면, 나머지 모든 수업들을 못 듣게 됩니다.
# 가장 먼저 끝나는 수업을 고른다. 딱히 반례가 없다.

# def course_selection(course_list):
#     # 코드를 작성하세요.
#     minn = 987654321
#     for i in range(len(course_list)-1):
#         for j in range(len(course_list)-i-1):
#             if course_list[j][1] > course_list[j+1][1]:
#                 course_list[j], course_list[j+1] = course_list[j+1],course_list[j]
#
#     sol = [course_list[0]]
#     for i in range(1,len(course_list)):
#         if course_list[i][0] > sol[-1][1]:
#             sol.append(course_list[i])
#     return sol
#
#
# # 테스트
# print(course_selection([(6, 10), (2, 3), (4, 5), (1, 7), (6, 8), (9, 10)]))
# print(course_selection([(1, 2), (3, 4), (0, 6), (5, 7), (8, 9), (5, 9)]))
# print(course_selection([(4, 7), (2, 5), (1, 3), (8, 10), (5, 9), (2, 5), (13, 16), (9, 11), (1, 8)]))