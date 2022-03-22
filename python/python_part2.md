## 자료형_part2

### Tuple

- 튜플 생성

  - 소괄호로 묶어서 생성할 수도 있고
  - 소괄호를 생략하고 콤마로만 구분해서 생성할 수도 있다.
  - 튜플의 원소가 하나일 경우, 반드시 마지막에 콤마를 찍어야 한다.
  - `tuple()` 생성자를 사용할 수도 있다.

  ```python
  tup1 = (1,2,3)
  tup2 = 1,2,3
  tup3_1 = 1
  tup3_2 = 1,
  tup4 = tuple("abcde")
  
  print(type(tup1))	# <class 'tuple'>
  print(type(tup2))	# <class 'tuple'>
  print(type(tup3_1))	# <class 'int'>
  print(type(tup3_2)) # <class 'tuple'>
  print(tup4)			# ('a', 'b', 'c', 'd', 'e')
  ```

  - 리스트, 딕셔너리와 달리 표현식으로 생성이 불가능하다.
    - 소괄호로 표현식을 작성하면 튜플이 아닌 제네레이터(part7 참조)가 생성된다.



- 튜플의 특징

  - 튜플을 포함한 모든 자료형이 튜플에 포함될 수 있다.
  - 순서가 있다.
  - 한 번 생성되면 값을 변경할 수 없다.
    - 그러나 + 연산, * 연산은 가능하다.
  - 튜플을 활용하면 여러 값을 한 번에 각기 다른 변수에 할당하는 것이 가능하다.
    - 상기했듯 굳이` ()`로 묶지 않아도 콤마로 구분만 되어 있으면 튜플이 생성된다.
  - 튜플의 해제 할당 기능을 사용하면 두 변수의 값을 바꾸는 것도 가능하다.

  ```python
  # 순서가 있으므로 인덱스를 통해 접근이 가능하다.
  tup = ('one','two', 'three')
  print(tup[0:2])    # ('one', 'two')
  
  # 값을 변경할 수 없다.
  tup[0] = 'zero'   # 'tuple' object does not support item assignment
  
  # +, * 연산은 가능하다.
  tup1 = (1,2,3)
  tup2 = (4,5,6)
  print(tup1+tup2)  # (1, 2, 3, 4, 5, 6)
  print(tup1*2)     # (1, 2, 3, 1, 2, 3)
  
  # 여러 값을 변수에 한 번에 할당하는 것이 가능하다.
  email,phone = "email@email.com", "010-1234-5678"
  print(email,phone)   # email@email.com 010-1234-5678
  
  # 두 변수의 값을 바꾸는 것도 가능하다.
  email, phone = phone, email
  print(email,phone)   # 010-1234-5678 email@email.com
  ```




### List

- 리스트 생성

  - `list()` 생성자를 사용하여 생성이 가능하다.
  - `[]` 로 생성이 가능하다.
    - 성능은 이 방식이 더 좋으며, 보다 Python스러운 방식이다.

  ```python
  lst1 = list()
  lst2 = []
  print(type(lst1))  # <class 'list'>
  print(type(lst2))  # <class 'list'>
  ```

  - 리스트 표현식으로 생성하기

  ```python
  lst = [i for i in range(3)]
  print(lst)		# [0, 1, 2]
  ```

  - 리스트 표현식에 조건문 포함시키기

  ```python
  lst = [i for i in range(5) if i % 2 == 0]
  print(lst)		# [0, 2, 4]
  ```

  - 반복문과 조건문을 여러 개 사용하는 것도 가능하다.

  ```python
  # 아래 표현식과
  lst = [i*j for i in range(5) if i % 2 == 0 for j in range(5) if j % 2 != 0]
  print(lst)	# [0, 0, 2, 6, 4, 12]
  
  # 아래 이중 for문은 같다.
  lst = []
  for i in range(5):
      for j in range(5):
          if i%2==0 and j%2 != 0:
              tmp.append(i*j)
  
  print(lst)	# [0, 0, 2, 6, 4, 12]
  ```
  
  - 조건문에 따라 다른 값 주기
    - 조건문의 위치에 따라 동작 방식이 달라지는데 위 예시 처럼 조건문을 맨 뒤에 주면 조건문과 부합하는 값만 list에 들어간다.
    - 조건문을 반복문 앞에 주면 조건문에 따라 다른 값을 줄 수 있다.
  
  ```python
  # i값이 3보다 작으면 그냥 i값을 넣고, 크거나 같으면 *3을 해서 넣는다.
  lst = [i if i<3 else i*3 for i in range(5)]
  print(lst)	# [0, 1, 2, 9, 12]
  ```



- List comprehension 사용시 주의사항

  - List comprehension은 generator가 아니라 실제 리스트를 반환한다.
    - 코드가 간결하여 간과하기 쉬운 점 중 하나로, 실제 리스트를 생성하고 메모리에 할당된다.
    - 즉, list의 생성이 끝나야 list comprehension 코드가 종료된다.

  - 예시
    - 아래의 두 코드는 10만번을 순회하는 동일한 코드임에도 range가 list comprehension에 비해 첫 반복이 실행되는 속도가 훨씬 빠르다.
    - 이는 list comprehension의 경우 list를 생성하는 시간이 있기 때문이다.

  ```python
  import time
  
  start = time.time()
  for i in range(10000000):
      print(time.time()-start)			# 3.337860107421875e-06
      break
  
  start = time.time()
  for i in [n for n in range(10000000)]:
      print(time.time()-start)			# 0.006056308746337891
      break
  ```

  - 따라서 list comprehension으로 생성한 list를 순회해야 할 경우 아래와 같이 generator를 생성해준다.
    - 대괄호가 아닌 소괄호로 묶으면 list가 아닌 generator가 생성된다.

  ```python
  for i in (n*2 for n in range(10000000)):
      continue
  ```



- 리스트 특징

  - 리스트를 포함한 모든 자료형이 리스트에 포함될 수 있다.
  - 순서가 있다.
  - 한 번 생성된 값을 변경 가능하다.

  ```python
  # 순서가 있으므로 인덱스를 통해 접근이 가능하다.
  lst = ['one', 'two', 'three']
  print(lst[0:2])   # ['one', 'two']
  
  # 변경이 가능하다.
  lst[0] = 'zero'
  print(lst)        # ['zero', 'two', 'three']
  ```




- 리스트의 할당과 복사

  - 리스트의 할당
    - 아래 코드에서 a를 b에 할당했으므로 a, b는 모두 같은 리스트를 가리키고 있다.
    - 따라서 b의 값을 변경시키면 a의 값도 변경된다.

  ```python
  a = [1, 2, 3]
  b = a
  b[2]=6
  print(a)	# [1, 2, 6]
  ```

  - 리스트의 복사
    - 값이 같은 다른 객체로 복사하고자 한다면 `copy()` 메서드를 사용하거나 반복문으로 새로 할당해야 한다.

  ```python
  # 반복문을 활용한 복사
  a = [1, 2, 3]
  b = []
  for i in a:
      b.append(i)
  
  print(b)		# [1, 2, 3]
  print(a is b)	# False
  
  # copy 메서드를 활용한 복사
  a = [1, 2, 3]
  b = a.copy()
  print(b)		# [1, 2, 3]
  print(a is b)	# False
  ```

  - 깊은 복사
    - 2차원 리스트의 경우  `copy()` 메서드를 사용하거나 반복문으로 새로 할당하더라도 내부의 값까지 복사되는 것은 아니다.
    - 따라서 `deepcopy()` 메서드를 사용(import가 필요하다)하거나 차원에 맞게 반복문을 사용해야 한다.

  ```bash
  a = [1, 2, 3]
  b = [a,[4,5,6]]
  c = []
  
  for i in b:
  	c.append(i)
  
  print(c)				# [[1, 2, 3], [4, 5, 6]]
  print(c[0])				# [1, 2, 3]
  # b와 c는 다른 객체를 가리키고 있지만
  print(b is c)			# False
  # 내부의 리스트는 같은 객체를 가리키고 있다.
  print(b[0] is c[0])		# True
  
  
  # 따라서 아래와 같이 차원수에 맞춰 반복문을 실행하거나
  a = [1, 2, 3]
  b = [a,[4,5,6]]
  c = []
  
  for i in b:
      tmp = []
      for j in i:
  	    tmp.append(j)
      c.append(tmp)
  
  print(c)				# [[1, 2, 3], [4, 5, 6]]
  print(c[0])				# [1, 2, 3]
  print(b is c)			# False
  print(b[0] is c[0])		# False
  
  
  # deepcopy 메서드를 활용한다.
  import copy
  
  
  a = [1, 2, 3]
  b = [a,[4,5,6]]
  c = []
  
  c = copy.deepcopy(b)
  
  print(c)				# [[1, 2, 3], [4, 5, 6]]
  print(c[0])				# [1, 2, 3]
  print(b is c)			# False
  print(b[0] is c[0])		# False
  ```



- 리스트 관련 메서드

  > 아래 메서드들 중 일부는 튜플, 문자열 등에서도 사용 가능하다.

  - `len()`: 요소의 개수를 반환

  ```python
  lst = [1,2,3]
  print(len(lst))   # 3
  ```

  - `.append()`: 요소를 추가

  ```python
  lst = [1,2,3]
  lst.append(4)
  print(lst)   #[1, 2, 3, 4]
  ```

  - `.insert(인덱스, 추가할 값)`: 지정한 인덱스에 값을 삽입

  ```python
  lst = [1,2,3]
  lst.insert(1,4)
  print(lst)   # [1, 4, 2, 3]
  ```

  - `.remove()`: 요소를 삭제

  ```python
  lst = [1,2,3]
  lst.remove(1)
  print(lst)  # [2,3]
  ```

  - `del`: 요소를 삭제
    - `remove`와의 차이는 `remove`는 삭제할 값을 지정하지만 del은 삭제할 인덱스를 지정한다는 것이다.

  ```python
  lst = [1,2,3]
  del lst[1]
  print(lst)  # [1,3]
  ```

  - `.pop()`: 리스트의 마지막 요소를 삭제 후 반환

  ```python
  lst = [1,2,3]
  # 삭제 후 반환한다.
  print(lst.pop())  # 3
  print(lst)		  # [1,2]
  ```

  - `.clear()`: 모든 요소 삭제

  ```python
  lst = [1,2,3]
  lst.clear()
  print(lst)      # []
  ```

  - `.reverse()`: 순서를 뒤집는다.

  ```python
  lst = [1,2,3]
  lst.reverse()
  print(lst)    # [3, 2, 1]
  ```

  - `.sort()`: 정렬한다.

  ```python
  lst = [9,3,6]
  lst.sort()
  print(lst)    # [3,6,9]
  ```

  - `sorted()`: 정렬한다.
    - `.sort()`와의 차이는 원본 배열을 변경하지 않는다는 것이다.

  ```python
  lst = [9,3,6]
  print(sorted(lst))  # [3,6,9]
  print(lst)			# [9,3,6]
  ```

  - `.copy()`
    - 복사에는 얕은 복사와 깊은 복사가 있는데 `.copy()`를 사용하면 깊은 복사가 가능하다.
    - `[:]`를 활용해도 깊은 복사가 가능하다.

  ```python
  # 얕은 복사
  lst1 = [1,2,3]
  lst2 = lst1  
  lst2[0] = 9
  # 얕은 복사이기에 같은 객체를 가리키고 있어 하나를 변경하면 둘 다 변경된다.
  print(lst1,lst2)  # [9, 2, 3] [9, 2, 3]
  
  # 깊은 복사
  lst1 = [1,2,3]
  lst2 = lst1.copy()
  lst2[0] = 9
  # 깊은 복사이기에 서로 다른 객체를 가리키고 있어 하나를 변경해도 다른 하나는 변경되지 않는다.
  print(lst1,lst2)  # [1, 2, 3] [9, 2, 3]
  
  # [:]를 활용한 깊은 복사
  lst1 = [1,2,3]
  lst2 = lst1[:]
  lst2[0] = 9
  print(lst1,lst2)  # [1, 2, 3] [9, 2, 3]
  ```



### Dictionary

- 생성

  - `dict()`생성자를 사용해 생성 가능하다.
  - `{}`를 사용해 생성 가능하다.

  ```python
  dict1 = dict()
  dict2 = {}
  print(type(dict1))  # <class 'dict'>
  print(type(dict2))  # <class 'dict'>
  ```

  - 표현식으로 생성이 가능하다.

  ```python
  a = ['a', 'b', 'c']
  b = [1, 2, 3]
  
  my_dict = {k:v for k,v in zip(a,b)}
  print(my_dict)		# {'a': 1, 'b': 2, 'c': 3}
  ```



- 딕셔너리의 특징

  - 키(key)-값(value) 쌍을 요소로 갖는 자료형이다.
  - 키는 중복이 불가능하다.
    - 키를 중복으로 사용할 경우 하나의 키를 제외한 모든 중복된 키는 무시된다.
  - 키는 변경 불가능한 immutable 타입이어야 하며 값은 immutable과 mutable 모두 가능하다.
    - 변경 불가능한 문자열이나 튜플 등은 키가 될 수 있다(integer도 가능하다).
    - 변경 가능한 리스트는 키가 될 수 없다.
    - 값에는 딕셔너리를 포함한 모든 자료형이 올 수 있다.
  - 순서가 없는 자료형으로 key를 통해 값에 접근해야 한다.
  - 이미 입력된 값의 변경이 가능하다.
  - 요소의 추가와 삭제가 가능하다.

  ```python
  # key에는 변경 불가능한 자료형이, 값에는 모든 자료형이 올 수 있다.
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28,"가족":{"엄마":"김엄마","아빠":"홍아빠"}}
  
  # key를 통해 값에 접근할 수 있다.
  print(my_dict['이름'])  	  # 홍길동
  
  # 변경이 가능하다.
  my_dict['나이']=14
  print(my_dict['나이']) 	  # 14 
  
  # 요소(키-값) 추가
  my_dict["email"] = "email@email.com"
  print(my_dict["email"])    # email@email.com
  
  
  # 요소(키-값) 삭제
  del my_dict['email']
  print(my_dict)  # {'취미': ['축구', '야구'], '이름': '홍길동', '나이': 14, '가족': {'엄마': '김엄마', '아빠': '홍아빠'}}
  ```



- 딕셔너리 관련 함수

  - `.keys()`: key를 리스트로 반환한다.

  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  print(my_dict.keys())  # dict_keys(['취미', '이름', '나이'])
  ```

  - `.values()`: 값을 리스트로 반환한다.

  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  print(my_dict.values())  # dict_values([['축구', '야구'], '홍길동', 28])
  ```

  - `.items()`: 키-값 쌍을 리스트로 반환한다.

  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  print(my_dict.items()) # dict_items([('취미', ['축구', '야구']), ('이름', '홍길동'), ('나이', 28)])
  ```

  - `.clear()`: 모든 요소 삭제

  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  my_dict.clear()
  print(my_dict)  # {}
  ```

  - `.get()`: 키로 값 얻기, 키가 존재하는지 확인하기
    - 첫 번째 인자로 찾을 키를, 두 번째 인자(optional)로 해당 키가 존재하지 않을 때 반환할 값을 받는다.
    - 그냥 키로만 접근하는 것과의 차이는 존재하지 않는 키로 접근할 경우, 키로만 접근하면 error가 발생하지만,  `.get()`은 None을 반환한다는 것이다.
    - 키로 값을 얻는 것이 아닌 키가 존재하는지 확인만 하고자 한다면 `in` 연산자를 사용해도 된다.
  
  ```python
  my_dict = {"취미":['축구','야구'],"이름":'홍길동',"나이":28}
  
  print(my_dict['email'])		 # KeyError: 'email'
  print(my_dict.get('email'))  # None
  print('email' in my_dict)	 # False
  
  # 두 번째 인자로 해당 키가 없을 때 반환할 값을 받는다.
  print(my_dict.get('email', 'theo@email.com'))
  ```
  
  - `.update()`: 키-값 수정하기
    - 만일 수정하려는 키가 없으면 새로운 키-값 쌍을 추가한다.
  
  ```python
  # 키가 문자열일 경우 아래와 같이 변수를 할당하듯이 넣어준다.
  my_dict = {'a':1}
  my_dict.update(a=2)
  print(my_dict)	# {'a': 2}
  my_dict.update(b=3)
  print(my_dict)	# {'a': 2, 'b': 3}
  
  
  # 숫자일 경우 아래와 같이 딕셔너리나 리스트, 튜플에 넣어서 수정해야 한다.
  my_dict = {1:2}
  my_dict.update({1:3})
  print(my_dict)	# {1: 3}
  my_dict.update([[2,3]])
  print(my_dict)	# {1: 3, 2: 3}
  ```
  
  - `pop(키, [기본값])`: 키-값 쌍을 삭제한 뒤 삭제한 값을 반환한다.
    - 첫 번째 인자로 제거 할 key를, 두 번째 인자로 키가 없을 경우 반환 할 기본 값을 설정한다.
    - 기본값을 지정해주지 않은 상태에서 존재하지 않는 키를 첫 번째 인자로 주면 error가 발생한다.
  
  ```python
  my_dict = {'a':1,'b':2}
  print(my_dict.pop('a'))		# 1
  print(my_dict)				# {'b': 2}
  # 기본값을 줄 경우
  print(my_dict.pop("c", 3))	# 3
  ```
  
  - `popitem()`: 마지막 키-값 쌍을 삭제하고 튜플로 반환한다.
    - 3.6 이전 버전에서는 임의의 키-값 쌍을 삭제하고 튜플로 반환한다.
  
  ```python
  my_dict = {'a':1,'b':2}
  print(my_dict.popitem())	# ('a', 1)
  print(my_dict)			# {'b': 2}
  ```
  
  - `del`: 키-값 쌍을 삭제한다.
  
  ```bash
  my_dict = {'a':1,'b':2}
  del my_dict['a']
  print(my_dict)			# {'b': 2}
  ```
  
  - `dict.fromkeys()`: 리스트, 튜플을 딕셔너리로 만든다.
    - 두 번째 인자로 기본값을 넘길 수 있다.
  
  ```python
  keys = ['a', 'b', 'c']
  my_dict = dict.fromkeys(keys)
  print(my_dict)		# {'a': None, 'b': None, 'c': None}
  
  # 기본값을 지정하는 것이 가능하다.
  my_dict2 = dict.fromkeys(keys, 10)
  print(my_dict2)		# {'a': 10, 'b': 10, 'c': 10}
  ```



- 할당과 복사
  - List와 동일하다.



### Set

- 생성

  - 반드시 문자열 또는 괄호로 묶어줘야 한다(괄호의 종류는 상관 없다).
  - 비어있는 자료형도 생성 가능하다.
    - 단 `{}`로 생성하면 빈 딕셔너리가 되므로 주의해야 한다.

  ```python
  my_set1 = set({1,2,3})
  my_set2 = set("Hello!")
  my_set3 = {1, 2, 3}
  empty_set = set()
  empty_dict = {}
  
  print(type(my_set1))  # <class 'set'>
  print(type(my_set2))  # <class 'set'>
  print(my_set1)		  # {1, 2, 3}
  print(my_set2)		  # {'l', '!', 'o', 'e', 'H'}
  print(my_set3)        # {1, 2, 3}
  print(type(empty_set))	  # set
  print(type(empty_dict))	  # dict
  ```



- Set(집합) 자료형의 특징

  - 중복을 허용하지 않는다.
  - 순서가 없다.
  - 다른 자료형과 달리 set 안에 다른 set을 넣을 수 없다.
  
  ```python
  my_set = set("Hello!")
  
  print(my_set2)		  # {'l', '!', 'o', 'e', 'H'}
  # 중복을 허용하지 않기에 두 번 들어간 l은 하나만 들어가게 된다.
  # 순서가 없기에 순서대로 들어가지 않는다.
  ```



- frozenset

  - 이름 그대로 얼어있는 set으로 집합 연산과 요소를 추가, 삭제하는 연산을 수행할 수 없다.
  - frozneset은 다른 일반 set과 달리 frozenset 안에 frozenset을 넣을 수 있다.
    - 그러나 frozneset안에 일반 set을 넣거나 일반 set 안에 frozenset을 넣을 수는 없다.

  ```python
  a = frozenset(range(10))
  ```



- 집합연산자

  - 교집합, 합집합, 차집합, 대칭차집합 등을 구할 때 사용한다.
  - 대칭차집합
    - 두 집합 중 겹치지 않는 요소들의 집합을 대칭차집합이라 한다.
    - XOR 연산자와 유사하다.
  - 할당연산자를 사용 가능하다.
    - `&=`와 같이 사용하는 것이 가능하다.
  
  ```python
  my_set1 = set([1,2,3])
  my_set2 = set([3,4,5])
  
  # 교집합
  print(my_set1 & my_set2)				# {3}
  print(my_set1.intersection(my_set2))	# {3}
  
  # 합집합
  print(my_set1 | my_set2)				# {1, 2, 3, 4, 5}
  print(my_set1.union(my_set2))			# {1, 2, 3, 4, 5}
  
  # 차집합
  print(my_set1-my_set2)					# {1, 2}
  print(my_set1.difference(my_set2))		# {1, 2}
  print(my_set2-my_set1)					# {4, 5}
  print(my_set2.difference(my_set1))		# {4, 5}
  
  # 대칭차집합
  print(my_set1 ^ my_set2)				# {1, 2, 4, 5}
  ```



- 부분 집합과 상위 집합 확인하기

  - 부분집합, 진부분집합, 상위집합, 진상위집합과 같이 속하는 관계를 표현할 수 있다.
    - 진부분집합은 한 집합이 다른 집합의 부분집합이지만 두 집합이 같지는 않은 집합이다.
    - 진상위집합은 한 집합이 다른 집합의 상위집합이지만 두 집합이 같지는 않은 집합이다.

  ```python
  my_set = {1, 2, 3, 4}
  # {1,2,3}은 my_set의 부분집합이다.
  print(my_set <= {1, 2, 3, 4, 5})	# True
  # {1,2,3,4}는 my_set의 진부분집합이 아니다.
  print(my_set < {1, 2, 3, 4})		# False
  # my_set은 {1, 2, 3}의 상위집합이다.
  print(my_set >= {1, 2})				# True
  # {1,2,3,4}는 my_set의 진상위집합이 아니다.
  print(my_set >= {1, 2, 3, 4})		# False
  ```



- 집합 관련 함수들

  - `.add()`: 요소를 1개 추가한다.

  ```python
  my_set = set([1,2,3])
  my_set.add(4)
  print(my_set)   # {1, 2, 3, 4}
  ```

  - `.update()`: 요소 여러 개 추가하기

  ```python
  my_set = set([1,2,3])
  my_set.update([4,5,6])
  print(my_set)   # {1, 2, 3, 4, 5, 6}
  ```

  - `.remove()`: 특정 요소 제거하기

  ```python
  my_set = set([1,2,3])
  my_set.remove(2)
  print(my_set)   # {1, 3}
  ```

  - `isdisjoint`: 현재 세트가 다른 세트와 겹치는 요소가 있는지 확인
    - 겹치는 요소가 없으면 True, 있으면 False를 반환한다.

  ```python
  my_set = {1, 2, 3, 4}
  print(my_set.isdisjoint({5,6,7,8}))	# True
  print(my_set.isdisjoint({4,5,6,7}))	# False
  ```



### iterator

- 객체의 한 종류

  - iterable한 객체를 `iter()` 함수를 통하여 생성할 수 있다.
  - `데이터 타입_itetrator` 형태로 생성된다.

  ```python
  name = "Chandelier"
  fruits = ["apple","banana","mango"]
  
  iter_string = iter(name)
  iter_list = iter(fruits)
  
  print(iter_string)			# <str_iterator object at 0x0000018073B3FFA0>
  print(type(iter_string))	# <class 'str_iterator'>
  
  print(iter_list)			# <list_iterator object at 0x0000018073B3FB20>
  print(type(iter_list))		# <class 'list_iterator'>
  ```



- itetator 객체는 객체의 element에 순서대로 접근할 수 있다.

  - `next()`메서드를 사용한다. 
  - iterator 객체의 길이 이상으로 접근하려 할 경우 `StopIteration` 예외가 발생한다.

  ```python
  name = "Chandelier"
  fruits = ["apple","banana","mango"]
  
  iter_string = iter(name)
  iter_list = iter(fruits)
  
  print(next(iter_list))	# apple
  print(next(iter_list))	# banana
  print(next(iter_list))	# mango
  print(next(iter_list))	# StopIteration
  ```



- iterable한 값을 통해서 iterator를 만들 수 있지만 iterable하다고 iterator인 것은 아니다.

  - iterator는 iterable한 값을 iterable하게 해준다.
  - 즉 우리가 for문 등을 통해 iterable 한 값을 순회할 수 있는 것은 python 내부적으로 iterable한 값을 iterator로 변환시켜주기 때문이다.

  ```python
  # iterable한 값이라도 iteraotr는 아니다.
  fruits = ["apple","banana","mango"]
  
  print(next(fruits))	# TypeError: 'list' object is not an iterator
  ```



- iterator 객체는 한 번 접근 하면 더 이상 사용할 수 없게 되어 해당 데이터는 폐기된다.

  - 아래 코드에서 위에 있는 반복문은 실행되지만 아래에 있는 반복문은 실행되지 않는다.

  ```python
  a = ['3.', '1.', 'a.', 'd.', 'b.', '2.']
  b = enumerate(a)
  
  # 실행 된다.
  for i in b:
      print(i)
  
  print("-"*100)
  
  # 실행 안된다.
  for i in b:
      print(i)
  ```







## enum

- enum
  - Python 3.4부터 지원시작
  - 일반적으로 서로 관련 있는 여러 상수의 집합을 정의하기 위해 사용한다.
  - 인스턴스의 종류를 제한할 수 있기에 견고한 프로그램 작성에 도움이 된다.



- 사용법

  - import해서 사용해야 한다.
  - Enum 내장 모듈을 상속 받는 클래스를 정의하여 사용한다.

  ```python
  from enum import Enum
  
  class Supply(Enum):
      NOTEBOOK = 1
      PENCIL = 2
      MOUSE = 3
  ```

  - enum 타입의 상수 인스턴스는 이름(name)과 값(value)을 지닌다.

  ```python
  print(Supply.NOTEBOOK)			# Supply.NOTEBOOK
  print(Supply.NOTEBOOK.name)		# NOTEBOOK
  print(Supply.NOTEBOOK.value)	# 1
  ```

  - iterable한 값이다.

  ```python
  for supply in Supply:
      print(supply)
  
  # Supply.NOTEBOOK
  # Supply.PENCIL  
  # Supply.MOUSE
  ```

  -  Class로 사용하는 대신에 일반 함수처럼 호출해서 enum 타입을 정의할 수도 있다.

  ```python
  Skill = Enum("Supply", "NOTEBOOK PENCIL MOUSE")
  ```

  - 값 자동 할당
    - 대부분의 경우 value가 무엇인지 중요하지 않다.
    - `auto()` 함수를 사용하면, 숫자를 1씩 증가시키면서 enum 내의 모든 value가 고유하도록 숫자를 할당해준다.
    - `_generate_next_value_()` 메서드를 오버라이드하면 숫자가 아닌 다른 값을 자동 할당할 수 있다.

  ```python
  from enum import Enum, auto
  
  class Supply(Enum):
      NOTEBOOK = auto()
      PENCIL = auto()
      MOUSE = auto()
      
  
  # overide
  class Supply(Enum):
      def _generate_next_value_(name, start, count, last_values):
          return name
      
      NOTEBOOK = auto()
      PENCIL = auto()
      MOUSE = auto()
  ```



- enum mixin

  - enum 타입을 사용할 때 불편한 점 중 하나는 상수의 이름이나 값에 접근할 때 name이나 value 속성을 사용해야 한다는 것이다.
  - enum mixin을 사용하면 이러한 불편을 해소할 수 있다.
    - 완전히 문자열로 취급된다.

  ```python
  class StrEnum(str, Enum):
      def _generate_next_value_(name, start, count, last_values):
          return name
  
      def __repr__(self):
          return self.name
  
      def __str__(self):
          return self.name
      
  class Supply(StrEnum):
      NOTEBOOK = auto()
      PENCIL = auto()
      MOUSE = auto()
  
  print(Supply.NOTEBOOK == 'NOTEBOOK')	# True
  ```

  














## 자료형의 변경

- `str()`, `int()`, `float()`, `bool()` 등의 함수를 사용해서 변경하면 된다.



- 주의점

  - `int()`의 경우 숫자가 아닌 것을 숫자로 변환할 수 없으며, 소수점이 있는 숫자 형식의 문자열을 정수형으로 변환할 수 없다.
  - 소수점이 없는 숫자 형식의 문자열은 정수형으로 변환이 가능하다.
  - 소수점이 있든 없든 숫자 형식이기만 하면 실수형으로 변환이 가능하다.
  - 변환 함수는 변환된 값을 반환할 뿐 실제로 자료형을 변경시키는 것은 아니다.

  ```python
  # 숫자 형식인 문자열의 정수와 실수 변환
  chr = "1"
  print(type(int(chr)))		# <class 'int'>
  print(type(float(chr)))		# <class 'float'>
  
  # 변환 함수는 변환된 값을 반환만 할 뿐이다.
  var = True
  print(type(str(var)))	# <class 'str'>
  print(type(var))		# <class 'bool'>
  
  # 아래와 같이 재할당 해주거나 다른 변수에 담아서 사용해야 한다.
  var = True
  var = str(var)
  print(type(var))		# <class 'str'>
  ```





