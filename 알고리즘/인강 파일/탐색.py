# 선형탐색
# def linear_search(element, some_list):
#     for i in range(len(some_list)):
#         if some_list[i] == element:
#             return i
#
#
# print(linear_search(2, [2, 3, 5, 7, 11]))
# print(linear_search(0, [2, 3, 5, 7, 11]))
# print(linear_search(5, [2, 3, 5, 7, 11]))
# print(linear_search(3, [2, 3, 5, 7, 11]))
# print(linear_search(11, [2, 3, 5, 7, 11]))


# 이진탐색
# def binary_search(element, some_list):
#     st = 0
#     ed = len(some_list)-1
#     while True:
#         mid = (st+ed)//2
#         if some_list[mid] == element:
#             return mid
#         elif some_list[mid] > element:
#             ed = mid-1
#         else:
#             st = mid+1
#         if st > ed:
#             return None
#
#
# print(binary_search(2, [2, 3, 5, 7, 11]))
# print(binary_search(0, [2, 3, 5, 7, 11]))
# print(binary_search(5, [2, 3, 5, 7, 11]))
# print(binary_search(3, [2, 3, 5, 7, 11]))
# print(binary_search(11, [2, 3, 5, 7, 11]))
# print(binary_search(13, [2, 3, 5, 7, 11]))

