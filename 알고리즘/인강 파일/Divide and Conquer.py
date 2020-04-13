# Divide and Conquer예제1
# 1부터 N까지의 합을 구하는 문제
# def consecutive_sum(start, end):
#     # 코드를 작성하세요
#     if start == end:
#         return start
#     return consecutive_sum(start,(start+end)//2)+consecutive_sum((start+end)//2+1, end)
#
# # 테스트
# print(consecutive_sum(1, 10))
# print(consecutive_sum(1, 100))
# print(consecutive_sum(1, 253))
# print(consecutive_sum(1, 388))


# #Divide and Conquer예제2
# #합병  정렬의 합병과정만 구현
# def merge(list1, list2):
#     # 코드를 작성하세요.
#     result = []
#     i = 0
#     j = 0
#     while i < len(list1) and j < len(list2):
#         if list1[i] > list2[j]:
#             result.append(list2[j])
#             j += 1
#         else:
#             result.append(list1[i])
#             i+=1
#     while i < len(list1):
#         result.append(list1[i])
#         i+=1
#     while j < len(list2):
#         result.append(list2[j])
#         j+=1
#     return result
# # 테스트
# print(merge([1],[]))
# print(merge([],[1]))
# print(merge([2],[1]))
# print(merge([1, 2, 3, 4],[5, 6, 7, 8]))
# print(merge([5, 6, 7, 8],[1, 2, 3, 4]))
# print(merge([4, 7, 8, 9],[1, 3, 6, 10]))


# Divide and Conquer예제2-해답
# def merge(list1, list2):
#     i = 0
#     j = 0
#
#     # 정렬된 항목들을 담을 리스트
#     merged_list = []
#
#     # list1과 list2를 돌면서 merged_list에 항목 정렬
#     while i < len(list1) and j < len(list2):
#         if list1[i] > list2[j]:
#             merged_list.append(list2[j])
#             j += 1
#         else:
#             merged_list.append(list1[i])
#             i += 1
#
#     # list2에 남은 항목이 있으면 정렬 리스트에 추가
#     if i == len(list1):
#         merged_list += list2[j:]
#
#     # list1에 남은 항목이 있으면 정렬 리스트에 추가
#     elif j == len(list2):
#         merged_list += list1[i:]
#
#     return merged_list
#
# # 테스트
# print(merge([1],[]))
# print(merge([],[1]))
# print(merge([2],[1]))
# print(merge([1, 2, 3, 4],[5, 6, 7, 8]))
# print(merge([5, 6, 7, 8],[1, 2, 3, 4]))
# print(merge([4, 7, 8, 9],[1, 3, 6, 10]))





# #합병정렬 전과정 구현 해답
# def merge(list1, list2):
#     i = 0
#     j = 0
#
#     # 정렬된 항목들을 담을 리스트
#     merged_list = []
#
#     # list1과 list2를 돌면서 merged_list에 항목 정렬
#     while i < len(list1) and j < len(list2):
#         if list1[i] > list2[j]:
#             merged_list.append(list2[j])
#             j += 1
#         else:
#             merged_list.append(list1[i])
#             i += 1
#
#     # list2에 남은 항목이 있으면 정렬 리스트에 추가
#     if i == len(list1):
#         merged_list += list2[j:]
#
#     # list1에 남은 항목이 있으면 정렬 리스트에 추가
#     elif j == len(list2):
#         merged_list += list1[i:]
#     return merged_list
#
#
# def merge_sort(my_list):
#     # base case
#     if len(my_list) < 2:
#         return my_list
#
#     # my_list를 반씩 나눈다(divide)
#     left_half = my_list[:len(my_list)//2]    # 왼쪽 반
#     right_half = my_list[len(my_list)//2:]   # 오른쪽 반
#
#     # merge_sort 함수를 재귀적으로 호출하여 부분 문제 해결(conquer)하고,
#     # merge 함수로 정렬된 두 리스트를 합쳐(combine)준다
#     return merge(merge_sort(left_half), merge_sort(right_half))
#
# # 테스트
#
# print(merge_sort([1, 3, 5, 7, 9, 11, 13, 11]))
# print(merge_sort([28, 13, 9, 30, 1, 48, 5, 7, 15]))
# print(merge_sort([2, 5, 6, 7, 1, 2, 4, 7, 10, 11, 4, 15, 13, 1, 6, 4]))






# #Divide and Conquer예제4, 퀵 정렬(partion만 구현하기)
# # 두 요소의 위치를 바꿔주는 helper function
# def swap_elements(my_list, index1, index2):
#     # 코드를 작성하세요.
#     my_list[index1],my_list[index2] = my_list[index2],my_list[index1]
#
# # 퀵 정렬에서 사용되는 partition 함수
# def partition(my_list, start, end):
#     # 코드를 작성하세요.
#     b = start
#     p = end
#     for i in range(len(my_list)):
#         if my_list[i] > my_list[p]:
#             continue
#         else:
#             swap_elements(my_list,b,i)
#             b+=1
#     swap_elements(my_list, b, p)
#     p = b-1
#     return p
#
#
#
# # 테스트 1
# list1 = [4, 3, 6, 2, 7, 1, 5]
# pivot_index1 = partition(list1, 0, len(list1) - 1)
# print(list1)
# print(pivot_index1)
#
# # 테스트 2
# list2 = [6, 1, 2, 6, 3, 5, 4]
# pivot_index2 = partition(list2, 0, len(list2) - 1)
# print(list2)
# print(pivot_index2)


# Divide and Conquer예제4, 퀵 정렬(전 과정 구현하기)
# 두 요소의 위치를 바꿔주는 helper function
def swap_elements(my_list, index1, index2):
    # 이전 과제에서 작성한 코드를 붙여 넣으세요!
    my_list[index1], my_list[index2] = my_list[index2], my_list[index1]
#
#
# # 퀵 정렬에서 사용되는 partition 함수
def partition(my_list, start, end):
    # 이전 과제에서 작성한 코드를 붙여 넣으세요!
    i = start
    b = start
    p = end

    while i < p:
        if my_list[i] <= my_list[p]:
            swap_elements(my_list, i, b)
            b += 1
        i += 1

    swap_elements(my_list, b, p)
    p = b

    return p


# # 퀵 정렬
# def quicksort(my_list, start, end):
#     # 코드를 작성하세요.
#     if end-start < 1:
#         return
#     p = partition(my_list, start, end)
#     return [quicksort(my_list, start, p-1)] + [quicksort(my_list, p, end)]



# 퀵 정렬부분 해답
def quicksort(my_list, start, end):
    # base case
    if end - start < 1:
        return

    # my_list를 두 부분으로 나누어주고,
    # partition 이후 pivot의 인덱스를 리턴받는다
    pivot = partition(my_list, start, end)

    # pivot의 왼쪽 부분 정렬
    quicksort(my_list, start, pivot - 1)

    # pivot의 오른쪽 부분 정렬
    quicksort(my_list, pivot + 1, end)


# 테스트 1
list1 = [1, 3, 5, 7, 9, 11, 13, 11]
quicksort(list1, 0, len(list1) - 1)
print(list1)

# 테스트 2
list2 = [28, 13, 9, 30, 1, 48, 5, 7, 15]
quicksort(list2, 0, len(list2) - 1)
print(list2)

# 테스트 3
list3 = [2, 5, 6, 7, 1, 2, 4, 7, 10, 11, 4, 15, 13, 1, 6, 4]
quicksort(list3, 0, len(list3) - 1)
print(list3)





# Divide and Conquer예제4, 퀵 정렬(quicksort함수에서 start와 end빼고 구현하기)
# 두 요소의 위치를 바꿔주는 helper function
# def swap_elements(my_list, index1, index2):
#     # 이전 과제에서 작성한 코드를 붙여 넣으세요!
#     my_list[index1], my_list[index2] = my_list[index2], my_list[index1]
#
# # 퀵 정렬에서 사용되는 partition 함수
# def partition(my_list, start, end):
#     # 이전 과제에서 작성한 코드를 붙여 넣으세요!
#     i = start
#     b = start
#     p = end
#
#     while i < p:
#         if my_list[i] <= my_list[p]:
#             swap_elements(my_list, i, b)
#             b += 1
#         i += 1
#
#     swap_elements(my_list, b, p)
#     p = b
#     return p
#
# # 퀵 정렬 (start, end 파라미터 없이도 호출이 가능하도록 수정해보세요!)
# def quicksort(my_list, start = 0, end=None):
#     if end == None:
#         end = len(my_list)-1
#     # base case
#     if end - start < 1:
#         return
#     # my_list를 두 부분으로 나누어주고,
#     # partition 이후 pivot의 인덱스를 리턴받는다
#     pivot = partition(my_list, start, end)
#
#     # pivot의 왼쪽 부분 정렬
#     quicksort(my_list, start, pivot - 1)
#
#     # pivot의 오른쪽 부분 정렬
#     quicksort(my_list, pivot + 1, end)
#
#
# # 테스트 1
# list1 = [1, 3, 5, 7, 9, 11, 13, 11]
# quicksort(list1) # start, end 파라미터 없이 호출
# print(list1)
#
# # 테스트 2
# list2 = [28, 13, 9, 30, 1, 48, 5, 7, 15]
# quicksort(list2) # start, end 파라미터 없이 호출
# print(list2)
#
# # 테스트 3
# list3 = [2, 5, 6, 7, 1, 2, 4, 7, 10, 11, 4, 15, 13, 1, 6, 4]
# quicksort(list3) # start, end 파라미터 없이 호출
# print(list3)