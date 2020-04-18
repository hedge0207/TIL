# is는 레퍼런스를 비교하고 ==는 값을 비교하기 때문에 ==, !=보다 is, is not을 사용한는 것을 권장한다.
# 연결 리스트를 만들 때 주의할 사항 중 하나는 항상 연결리스트가 빈 경우(if list.head is None)에 대한 예외 처리를 해줘야 한다는 것이다.
# 일반적인 순서는 추가, 삭제할 노드의 next, prev(이중 연결 리스트의 경우) 값을 수정해준 후 추가, 삭제 된 노드의 앞뒤 노드의 next, prev 값을 수정해 주는 것이다. 만일
# 추가, 삭제한 위치가 연결 리스트의 처음이나 끝이었다면 head와 tail을 수정하는 과정도 거쳐야 한다.
# 덧붙여, 삭제를 하는 경우 노드의 개수가 1일때 삭제를 하면 연결 리스트가 사라지는 것이므로 이에 대한 처리도 해야 한다.
class Node:
    def __init__(self, d=0, n=None):
        self.data = d  # 데이터 필드
        self.next = n  # 다음 노드

class LinkedList:
    def __init__(self):
        self.head = None  # 첫 번재 노드
        self.tail = None  # 마지막 노드, 마지막 노드에 추가하기 위해 설정
        self.size = 0  # 연결 리스트에 있는 노드의 개수


mylist = LinkedList()


def printList(lst):  # lst는 LinkedList의 객체다.  cf.일반적으로 printList 함수는 LinkedList 클래스 내부에 정의한다.
    if lst.head is None:  # 빈 리스트일 경우, 위에서 head의 기본값으로 None을 줬으므로 빈 리스트라면 head가 None일 것이다.
        return
    cur = lst.head  # 시작 노드
    print(lst.size, '[',end=" ")
    while cur is not None:  #cur이 None이라는 것은 이전 반복에서 cur.next가 None이었다는 것이고 이는 다음 노드가 없다는 것을 의미한다.
        print(cur.data,end=" ")
        cur = cur.next
    print("]")


# 마지막 노드를 추가
def insertLast(lst, new):  # new는 새로 추가할 노드 객체
    if lst.head is None:  # 빈 리스트일 경우
        lst.head = lst.tail = new
    else:  # 빈 리스트가 아닐 경우
        # 삽입과 삭제에서는 앞의 노드를 아는 것이 중요한데, 마지막에 노드를 추가하는 경우, 기존에 마지막이었던 노드가 앞의 노드가 된다.
        lst.tail.next = new  #기존에 꼬리였던 노드는 다음 노드로 새로운 노드를 가리키게 되고
        lst.tail = new       #새로운 노드가 꼬리가 된다.
    lst.size += 1



# # 마지막 노드를 삭제
def deleteLast(lst):
    if lst.head is None:
        return
    else:
        pre = None  # 이전 노드를 저장하는 변수
        cur = lst.head #현재 노드를 저장하는 변수
        while cur.next is not None:    #cur.next가 None이라는 것은 cur이 가리키는 다음 노드가 없다는 것, 즉 마지막 노드라는 것이므로 반복문이 종료 될 때 cur에는 마지막 노드가 담기게 된다.
            pre = cur
            cur = cur.next
        if pre is None: #노드의 개수가 1개 뿐일 때, whild문이 돌지 않아 pre는 초기 값인 None이 담긴다.
            lst.head=lst.tail=None  #그냥 없애준다.
        else:
            pre.next = None  #pre.next을 None으로 설정했므로 while문을 거쳐 마지막 노드가 된 cur과 연결이 끊기게 되고 삭제된 것과 마찬가지가 된다.
            lst.tail = pre   #꼬리를 pre로 바꿔준다.
        lst.size -= 1


# # 예시 출력
# for i in range(5):
#     insertLast(mylist, Node(i))
#     printList(mylist)
# 
# 
# while mylist.size:
#     deleteLast(mylist)
#     printList(mylist)



# 첫 노드를 추가
def insertFirst(lst,new):
    if lst.head is None:
        lst.head = lst.tail = new
    else:
        new.next=lst.head  #new의 next를 원래 첫 번째 자리에 있던 노드로 설정
        lst.head=new       #head를 new가 되게 설정
    lst.size+=1


#첫 노드를 삭제
def deleteFirst(lst):
    if lst.head is None:
        return
    else:
        lst.head = lst.head.next
        # 노드의 개수가 1개뿐이라면 lst.head.next는 None이다.
        if lst.head is None:
            lst.tail = None #없애준다.

        lst.size-=1
#마지막 노드를 삭제하는 것과 첫 노드를 삭제하는 것이 다른 이유는 단일 연결 리스트이기 때문이다. 단일연결 리스트의 특성 상 헤드쪽에서 테일 쪽으로 갈 수는 있어도 그 역방향으로는 갈 수 없는데
#첫 노드를 삭제하는 경우 첫 노드는 다음 노드에 대한 정보(next)를 가지고 있으나 마지막 노드를 삭제하는 경우에는 그렇지 않다. 마지막 노드는 마지막 전 노드에 대한 정보를 가지고 있지 않기에 마지막 전 노드가
#무엇인지 head부터 탐색하면서 찾아야 한다. 그래야 마지막 전 노드의 next를 None으로 바꿔 마지막 노드와 연결을 끊을 수 있다.

# 예시출력
# for i in range(5):
#     insertFirst(mylist, Node(i))
#     printList(mylist)
#
# while mylist.size:
#     deleteFirst(mylist)
#     printList(mylist)


# 임의의 위치에 삽입
def insertAt(lst, idx, new):
    # 빈 리스트일 경우 또는 추가해야 할 인덱스가 0인 경우(idx==0)
    if lst.head is None or idx ==0:
        insertFirst(lst,new)
    # 마지막에 추가하는 경우 idx>=lst.size
    elif idx>=lst.size:
        insertLast(lst.new)
    # 중간에 추가하는 경우
    else:
        pre=None
        cur=lst.head
        for _ in range(idx):  #cur은 0번 자리에 있으므로 idx 자리에 추가하려면 cur을 idx번 움직이면 된다.
            pre = cur
            cur = cur.next
        new.next = cur
        pre.next = new
        lst.size+=1


#임의의 위치에 삭제
def deleteAt(lst,idx):
    if lst.head is None:
        return
    elif idx==0:
        deleteFirst(lst)
    elif idx>=lst.size:
        deleteLast(lst)
    else:
        pre = None      #이 경우에는 연결 리스트가 완전히 사라지는 경우에 대한 예외처리를 할 필요가 없다. 처음과 끝이 아닌 인덱스를 제거한다는 것은 리스트의 길이가 2 이상이라는 것이기 때문이다.
        cur = lst.head
        for _ in range(idx):
            pre=cur
            cur=cur.next
        pre.next=cur.next
        lst.size-=1





for i in range(5):
    insertFirst(mylist,Node(i))
    printList(mylist)

for i in range(3):
    insertAt(mylist,2,Node(i+10))
    printList(mylist)

for i in range(3):
    deleteAt(mylist,2)
    printList(mylist)