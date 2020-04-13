# 재귀함수로 피보나치 수열 구하기
# def fib(n):
#     if n == 1 or n == 2:
#         return 1
#     return fib(n-1)+fib(n-2)
#
# for i in range(1, 11):
#     print(fib(i))


# 재귀함수로 1부터 n까지의 합 구하기
# def triangle_number(n):
#     if n == 1:
#         return 1
#     return n+triangle_number(n-1)
#
# # 테스트: triangle_number(1)부터 triangle_number(10)까지 출력
# for i in range(1, 11):
#     print(triangle_number(i))


# 재귀함수로 n의 각 자릿수의 합을 리턴
# def sum_digits(n):
#     if n < 10:
#         return n
#     return sum_digits(n//10)+n%10
#
#
# # 테스트
# print(sum_digits(22541))
# print(sum_digits(92130))
# print(sum_digits(12634))
# print(sum_digits(704))
# print(sum_digits(3755))


# 파라미터 some_list를 거꾸로 뒤집는 함수
# def flip(some_list):
#     if len(some_list) < 2:
#         return some_list
#     return some_list[-1:]+flip(some_list[:-1])
#
# # 테스트
# some_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# some_list = flip(some_list)
# print(some_list)


# 재귀함수로 이진탐색 구현
# def binary_search(element, some_list, start_index=0, end_index=None):
#     # end_index가 따로 주어지지 않은 경우에는 리스트의 마지막 인덱스
#     if end_index == None:
#         end_index = len(some_list) - 1
#
#     # 코드를 작성하세요.
#     # base case1(찾는 값이 리스트에 없는 경우)
#     if start_index > end_index:
#         return None
#
#     # base case2(찾는 값을 찾은 경우)
#     mid = (start_index + end_index) // 2
#     if some_list[mid] == element:
#         return mid
#
#     if some_list[mid] > element:
#         end_index = mid-1
#         return binary_search(element, some_list, start_index, end_index)
#     elif some_list[mid] < element:
#         start_index = mid+1
#         return binary_search(element, some_list, start_index, end_index)
#
#
# print(binary_search(2, [2, 3, 5, 7, 11]))
# print(binary_search(0, [2, 3, 5, 7, 11]))
# print(binary_search(5, [2, 3, 5, 7, 11]))
# print(binary_search(3, [2, 3, 5, 7, 11]))
# print(binary_search(11, [2, 3, 5, 7, 11]))


# # 재귀함수로 하노이의 탑 해를 구하기
# def move_disk(disk_num, start_peg, end_peg):
#     print("%d번 원판을 %d번 기둥에서 %d번 기둥으로 이동" % (disk_num, start_peg, end_peg))
#
# def hanoi(num_disks, start_peg, end_peg):
#     # 코드를 입력하세요.
#     if num_disks == 0:
#         return
#     other_peg = 6 - start_peg - end_peg
#     hanoi(num_disks-1, start_peg, other_peg)
#     move_disk(num_disks, start_peg, end_peg)
#     hanoi(num_disks - 1, other_peg, end_peg)
#
# # 테스트 코드 (포함하여 제출해주세요)
# hanoi(3, 1, 3)