- iterator

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



