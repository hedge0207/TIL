# #Brute Force예제
# def max_product(left_cards, right_cards):
#     # 코드를 작성하세요.
#     lista = []
#     for i in left_cards:
#         for j in right_cards:
#             lista.append(i*j)
#     return max(lista)
#
#
# # 테스트
# print(max_product([1, 6, 5], [4, 2, 3]))
# print(max_product([1, -9, 3, 4], [2, 8, 3, 1]))
# print(max_product([-1, -7, 3], [-4, 3, 6]))


# #Brute Force예제2
# # 두 매장 사이의 거리가 가장 가까운 두 매장을 찾아서 보고하라
# # 제곱근 사용을 위한 sqrt 함수
# from math import sqrt
# # 두 매장의 직선 거리를 계산해 주는 함수
# def distance(store1, store2):
#     return sqrt((store1[0] - store2[0]) ** 2 + (store1[1] - store2[1]) ** 2)
#
# # 가장 가까운 두 매장을 찾아주는 함수
# def closest_pair(coordinates):
#     # 여기 코드를 쓰세요
#     Min = 987654321
#     for i in coordinates:
#         for j in coordinates:
#             if i == j:
#                 continue
#             if Min > distance(i,j):
#                 Min = distance(i,j)
#                 Mins = [i,j]
#     return Mins
#
#
# # 테스트
# test_coordinates = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
# print(closest_pair(test_coordinates))


# Brute Force예제3
# 강남역에 엄청난 폭우가 쏟아진다고 가정합시다. 정말 재난 영화에서나 나올 법한 양의 비가 내려서, 고층 건물이 비에 잠길 정도입니다.
# 그렇게 되었을 때, 건물과 건물 사이에 얼마큼의 빗물이 담길 수 있는지 알고 싶은데요. 그것을 계산해 주는 함수 trapping_rain을 작성해 보려고 합니다.
# 함수 trapping_rain은 건물 높이 정보를 보관하는 리스트 buildings를 파라미터로 받고, 담기는 빗물의 총량을 리턴해 줍니다.
# 예를 들어서 파라미터 buildings로 [3, 0, 0, 2, 0, 4]가 들어왔다고 합시다. 그러면 0번 인덱스에 높이 3의 건물이, 3번 인덱스에 높이 2의 건물이, 5번 인덱스에 높이 4의 건물이 있다는 뜻입니다. 1번, 2번, 4번 인덱스에는 건물이 없습니다.
# 그러면 아래의 사진에 따라 총 10 만큼의 빗물이 담길 수 있습니다. 따라서 trapping_rain 함수는 10을 리턴하는 거죠.
# def trapping_rain(buildings):
#     # 코드를 작성하세요
#     rain = 0
#     for i in range(len(buildings)):
#         Maxl = buildings[i]
#         for j in range(0,i+1):
#             if Maxl < buildings[j]:
#                 Maxl = buildings[j]
#
#         Maxr =  buildings[i]
#         for j in range(i+1,len(buildings)):
#             if Maxr < buildings[j]:
#                 Maxr = buildings[j]
#
#         aa = min(Maxl,Maxr)
#         rain += aa - buildings[i]
#     return rain
#
# # 테스트
# print(trapping_rain([3, 0, 0, 2, 0, 4]))
# print(trapping_rain([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
