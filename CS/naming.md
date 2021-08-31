# boolean

- is

  - is+N
    - "~인가?"라는 뜻으로 사용한다.
    - check도 위와 같은 뜻으로 많이 사용되지만 둘을 구분해서 사용하는 것이 좋다.
    - check는 참/거짓을 판단하기 위한 것이고, is는 참만 판단하기 위한 것이다.

  ```python
  def is_int(foo):
      if isinstance(foo, int):
          return True
      else:
          return False
  
  def check_int(foo):
      if isinstance(foo, int):
          return True
      else:
          return False
  
      
  # 위와 같이 check와 is의 함수는 같아도    
  # is는 이렇게 사용하는 것이 자연스럽고
  if is_int(1):
      print("int")
  
  # check는 이렇게 사용하는 것이 자연스럽다.
  if check_int(1)==True:
      print(int)
  ```

  - is+~ing
    - "~하는 중인가?"라는 뜻으로 사용한다.

  - is+p.p
    - "~된"이라는 뜻으로 사용한다.
  - 동사와 함께 쓰지 말아야 한다.
    - is가 이미 동사이므로 동사와 함께 쓰지 않도록 주의한다.



- has

  - has+N
    - "~을 가지고 있는가?"라는 뜻으로 사용된다.

  ```python
  def has_elements(some_list):
      if len(some_list)==0:
          return False
      return True
  
  my_list = []
  if has_elements(my_list):
      print(my_list)
  ```

  - has + p.p
    - "과거에 ~한 것이 현재까지 유지되는 중인가?" 라는 뜻으로 쓰인다.



- 동사 원형

  - 동사원형을 변수명으로 사용할 때는 3인칭 단수로 써야 한다.
    - 위에서 have가 아닌 has를 쓴 것도 이와 같은 이유 때문이다.

  ```python
  def receive_file(path):
      try:
      	'''
     		파일 받아오는 로직
      	'''
          return True
      except:
          return False
  
  file_exists = receive_file('/some/path')
  if file_exists:
      print("File exists!")
  ```

  