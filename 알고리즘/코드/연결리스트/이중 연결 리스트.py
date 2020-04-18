class Node:
    def __init__(self, d=0, p=None, n=None):
        self.data = d  # 데이터 필드
        self.prev = p
        self.next = n  # 다음 노드


class LinkedList:
    def __init__(self):
        self.head = None  # 첫 번재 노드
        self.tail = None  # 마지막 노드, 마지막 노드에 추가하기 위해 설정
        self.size = 0  # 연결 리스트에 있는 노드의 개수


def printList(lst):
    if lst.head is None:
        return
    cur=lst.head
    while cur is not None:
        print(cur.data,end=" ")
        cur=cur.next
    print()
    #역순 출력
    # cur=lst.tail
    # while cur is not None:
    #     print(cur.data, end=" ")
    #     cur=cur.prev
    # print()


def addLast(lst,new):
    if lst.head is None:
        lst.head = lst.tail = new
    else:
        new.prev=lst.tail
        lst.tail.next=new
        lst.tail=new
    lst.size+=1

def deleteLast(lst):
    if lst.head is None:
        return
    else:
        if lst.tail.prev is None:  #연결 리스트가 1개 밖에 없을 때의 처리
            lst.tail=lst.head=None
        tmp = lst.tail.prev
        lst.tail.prev=None  
        tmp.next=None
        lst.tail=tmp
    lst.size-=1


mylist=LinkedList()

# arr = [1,3,5,7,9]
# for var in arr:
#     addLast(mylist, Node(var))
# printList(mylist)
#
# for var in [10,11,12]:
#     addLast(mylist, Node(var))
# printList(mylist)
#
# for _ in range(3):
#     deleteLast(mylist)
# printList(mylist)


def addFirst(lst,new):
    if lst.head is None:
        lst.head=lst.tail=new
    else:
        lst.head.prev=new
        new.next=lst.head
        lst.head=new
    lst.size+=1


def deleteFirst(lst):
    if lst.head is None:
        return
    else:
        if lst.tail.prev is None:
            lst.tail=lst.head=None
        tmp = lst.head.next
        tmp.prev=None
        lst.head=tmp
    lst.size-=1

# arr = [1,3,5,7,9]
# for var in arr:
#     addFirst(mylist, Node(var))
# printList(mylist)
#
# for var in [10,11,12]:
#     addFirst(mylist, Node(var))
# printList(mylist)
#
# for _ in range(3):
#     deleteFirst(mylist)
# printList(mylist)



def addAt(lst,idx,new):
    if lst.head is None or idx==0:
        addFirst(lst,new)
    elif idx>=lst.size:
        addLast(lst,new)
    else:
        if idx>=lst.size//2:
            tmp = None
            cur = lst.tail
            for _ in range(lst.size-idx):
                tmp=cur
                cur=cur.prev
            new.next=tmp
            new.prev=cur
            cur.next=new
            tmp.prev=new
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
        deleteLast()
    else:
        if idx>=lst.size//2:
            tmp = None
            cur = lst.tail
            for _ in range(lst.size-idx):
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


arr = [1,3,5,7,9,11,13,15,17,19,21]
for var in arr:
    addLast(mylist, Node(var))
printList(mylist)


addAt(mylist,7,Node(123))
printList(mylist)

deleteAt(mylist,8)
printList(mylist)