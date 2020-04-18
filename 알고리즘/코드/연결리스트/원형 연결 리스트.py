class Node:
    def __init__(self, d=0, p=None, n=None):
        self.data = d  # 데이터 필드
        self.prev = p
        self.next = n  # 다음 노드


class LinkedList:
    def __init__(self):
        self.head = None  # 첫 번재 노드
        self.size = 0  # 연결 리스트에 있는 노드의 개수
        # tail은 쓰지 않는다.


def printList(lst):
    if lst.head is None:
        return
    cur = lst.head
    for _ in range(lst.size*2):   #next나 prev 값 중 None이 없으므로 while이 아닌 for문을 쓴다.  *2를 해주는 이유는 원형으로 잘 도는지 확인하기 위함이다. 실제로 쓸 때는 빼주면 된다.
        print(cur.data, end=" ")
        cur = cur.next
    print()
    # 역순 출력
    # cur = lst.head.prev   #tail이 없으므로 대신 head.prev를 쓴다.
    # for _ in range(lst.size*2):   #*2를 해주는 이유는 원형으로 잘 도는지 확인하기 위함이다. 실제로 쓸 때는 빼주면 된다.
    #     print(cur.data, end=" ")
    #     cur = cur.prev
    # print()


def addLast(lst, new):
    if lst.head is None:
        lst.head = new
        new.prev = new.next = new  # 원형일 때 노드가 1개면 prev,next 둘 다 같은 노드를 가리킨다.
    else:
        tail = lst.head.prev  # 꼬리를 정식으로 쓰지는 않지만 편의상 사용, head의 이전 노드를 꼬리로 본다.
        #이해가 가지 않으면 아래에 쓰인 tail을 모두 lst.head.prev로 바꿔서 보면 더 이해가 쉽다. 또, tail에는(즉, lst.head.prev에는) 반복문이 1번 돌았을 때부터 두번째 반복이 끝나기 전까지는 1이,
        #2번 돌았을 때부터 세번째 반복이 끝나기 전까지는 3이, 3번 돌았을 때부터 네번째 반복이 끝나기 전까지는 5가 들어가는 식으로 순차적으로 들어간다.
        #즉, 1을 데이터로 가지는 노드, 3을 데이터로 가지는 노드...이런 식으로 순차적으로 들어간다.
        new.prev = tail
        new.next = lst.head
        tail.next = new
        lst.head.prev = new  #이 줄에 따라 다음 반복때에는 tail에 이전 반복에 삽입된 노드가 들어가게 된다.
    lst.size += 1


def deleteLast(lst):
    if lst.head is None:
        return
    else:
        tail=lst.head.prev
        tail.prev.next=lst.head
        lst.head.prev=tail.prev
    lst.size-=1


# mylist = LinkedList()

# arr = [1, 3, 5, 7, 9]
# for var in arr:
#     addLast(mylist, Node(var))
# printList(mylist)
#
# for var in range(2):
#     deleteLast(mylist)
# printList(mylist)


def addFirst(lst,new):
    if lst.head is None:
        lst.head=new
        lst.head.prev=lst.head.next=new
    else:
        tail=lst.head.prev
        new.prev=tail
        new.next=lst.head
        tail.next=new
        lst.head.prev=new
        lst.head=new
    lst.size+=1



def deleteFirst(lst):
    if lst.head is None:
        return
    else:
        tail= lst.head.prev
        tail.next=lst.head.next
        lst.head = lst.head.next
        lst.head.prev=tail
    lst.size-=1


mylist = LinkedList()
arr = [1, 3, 5, 7, 9]
for var in arr:
    addFirst(mylist, Node(var))
printList(mylist)

# for var in range(2):
#     deleteFirst(mylist)
# printList(mylist)


def addAt(lst,idx,new):
    if lst.head is None or idx==0:
        addFirst(lst,new)
    elif idx>=lst.size:
        addLast(lst,new)
    else:
        if idx >= lst.size // 2:
            tmp=None
            cur=lst.head
            for _ in range(lst.size-idx+1):
                tmp = cur
                cur = cur.prev
            new.next = tmp
            new.prev = cur
            cur.next = new
            tmp.prev = new
        else:
            tmp = None
            cur = lst.head
            for _ in range(idx):
                tmp = cur
                cur = cur.next
            new.next = cur
            new.prev = tmp
            tmp.next = new
            cur.prev = new
        lst.size+=1


def deleteAt(lst,idx):
    if lst.head is None:
        return
    elif idx==0:
        deleteFirst(lst)
    elif idx>=lst.size:
        deleteLast(lst)
    else:
        if idx>=lst.size//2:
            tmp = None
            cur = lst.head
            for _ in range(lst.size-idx+1):
                tmp=cur
                cur=cur.prev
            cur.next=tmp.next
            tmp.next.prev=cur
        else:
            tmp = None
            cur = lst.head
            for _ in range(idx):
                tmp = cur
                cur = cur.next
            tmp.next=cur.next
            cur.next.prev=tmp
        lst.size-=1


addAt(mylist, 4, Node(4))
printList(mylist)
deleteAt(mylist,3)
printList(mylist)


