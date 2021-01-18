# 클래스

- 파이썬은 객체 지향 언어다.
  - 모든 것이 객체로 이루어져 있다.



- 클래스는 왜 필요한가

  - 함수로 더하기를 처리하여 그 결과값을 여러 변수에 저장하는 프로그램을 구현하는 상황을 가정해보자
  - 아래와 같이 변수의 수가 늘어날 수록 동일한 작업을 수행하는 함수의 수도 그에 맟줘 증가해야 한다.
  - 이는 굉장히 비효율적으로 객체를 사용하면 이러한 비효율을 해결 가능하다.

  ```python
  result1 = 0
  result2 = 0
  
  def plus1(a,b):
      global result1
      result1 = a+b
  
  def plus2(a,b):
      global result2
      result2 = a+b
  ```

  

- 클래스와 객체
  - 클래스: 데이터와 일정한 작업을 함께 묶어 놓은 것.
  - 클래스와 객체는 과자틀과 과자틀에서 나온 과자의 관계와 같다.
  - 클래스가 과자틀이라면 객체는 그 과자틀로 만든 과지이다.
  - 객체와 인스턴스
    - 객체와 인스턴스는 동일한 말 처럼 보이지만 엄밀히 말하면 다르다.
    - 인스턴스란 특정 객체가 어떤 클래스의 객체인지를 관계 위주로 사용할 때 사용한다.
    - 즉, "a는 A 클래스의 인스턴스"라는 말이 "a는 A 클래스의 객체"라는 말보다 자연스럽고
    - "a는 객체"라는 말이 "a는 인스턴스"라는 말보다 자연스럽다.



- 클래스 사용하기

  - 클래스가 왜 필요한지 알아봤던 예시를 바탕으로 클래스를 사용하는 방법을 살펴본다.
  - 클래스와 인스턴스 생성

  ```python
  # 클래스 생성
  class Plus:
      pass
  
  # FourCal 클래스의 인스턴스 생성
  obj = Plus()
  print(type(obj))  # <class '__main__.FourCal'>
  ```

  - 클래스에 작업(함수) 추가하기
    - 클래스 내부에 생성된 함수는 일반 함수와 구분하기 위해 메서드라고 부른다.
    - 일반 함수와 달리 메서드는 첫 번째 매개변수로 `self`를 받는다(`self`말고 다른 이름으로 해도 무관하지만 self로 하는 것이 관례다).
    - `self`에는 메서드를 호출한 객체를 자동으로 받는다.

  ```python
  # 메서드 생성
  class Plus:
      def set_data(self,first,second):  # 첫 번째 매개변수로 `self`를 받는다. 즉 아래 실행문은 다음과 같이 객체 변수를 변경한다.
          self.first = first			  # obj.first = first
          self.second = second		  # obj.second = second
          
  # 메서드 호출 방법 1.
  # 첫 번째 매개변수인 self에는 fc가 자동으로 넘어간다.
  obj = Plus()
  obj.set_data(2,3)
  print(obj.first)  # 2
  
  
  # 메서드 호출 방법 2.아래와 같이 클래스를 통해 메서드를 호출할 때는 첫 번째 인자로 인스턴스를 반드시 넘겨줘야 한다.
  obj = Plus()
  Plus.set_data(a,2,3)
  ```

  - 객체들 간의 변수 공유
    - 객체에 생성되는 객체만의 변수를 객체변수라 한다.
    - 같은 클래스로 생성했어도 서로 다른 객체들은 객체 변수를 공유하지 않는다.

  ```python
  # 메서드 생성
  class Plus:
      def set_data(self,first,second):
          self.first = first
          self.second = second
          
  
  obj1 = Plus()
  obj1.set_data(2,3)
  obj2 = Plus()
  obj2.set_data(4,5)
  
  # 둘의 id 값이 다른 것을 확인 가능하다.
  print(id(obj1.first))	# 1647180802384
  print(id(obj2.first))	# 1647180802448
  ```

  - 원하는 작업 추가하기

  ```python
  class Plus:
      def set_data(self,first,second):
          self.first = first
          self.second = second
      def add(self):
          return self.first+self.second
  
  obj = Plus()
  obj.set_data(2,3)
  print(obj.add())  # 5
  ```

  

- 생성자

  - 위 예시에서는 `set_data`메서드를 활용하여 객체 변수를 설정하였다.
  - 객체에 초기값을 설정해야 할 필요가 있을 때는 메서드를 사용하는 방법 보다 생성자를 구현하는 것이 낫다.
  - **생성자(Constructor)**란 객체가 생성될 때 자동으로 호출되는 메서드를 말한다.

  ```python
  class Plus:
      def __init__(self,first,second):
          self.first = first
          self.second = second
  # 생성자는 first, second라는 두 개의 매개변수를 받으므로 생성할 때부터 인자를 넘겨줘야 한다.
  obj = Plus(2,3)
  print(obj.first, obj.second)	# 2 3
  ```

  

- 클래스의 상속

  - 어떤 클래스를 만들 때 다른 클래스의 기능을 물려 받는 것을 클래스의 상속이라 한다.
  - 위에서 만든 `Plus` 클래스를 상속한 후 뺄셈 기능을 추가하여 PlusMunis 클래스를 만들면 다음과 같이 만들 수 있다.
  - 기존 클래스가 라이브러리 형태로 제공되거나 수정이 허용되지 않는 상황에서 상속은 유용하게 쓸 수 있다.

  ```python
  # 피상속 클래스
  class Plus:
      def __init__(self,first,second):
          self.first = first
          self.second = second
      def add(self):
          return self.first+self.second
  
  # 아래와 같이 피상속 클래스를 괄호 안에 넣으면 된다.
  class PlusMinus(Plus):
      def mul(self):
          return self.first-self.second
  
  # 피상속 클래스의 생성자와
  pm = PlusMinus(5,4)
  # 메서드를 사용 가능하다.
  print(pm.add())		# 9
  print(pm.mul())		# 1
  ```

  

- 메서드 오버라이딩

  - 피상속 클래스의 메서드를 동일한 이름으로 다시 만드는 것을 메서드 오버라이딩이라 한다.
  - 이렇게 하면 상속을 받은 클래스의 메서드가 실행된다.

  ```python
  # 피상속 클래스
  class Plus:
      def __init__(self,first,second):
          self.first = first
          self.second = second
      def add(self):
          return self.first+self.second
  
  class PlusMinus(Plus):
      # 아래와 같이 피상속 클래스의 메서드와 동일한 이름으로 메서드를 생성하면 된다.
      def add(self):
          return self.first*self.second
      def mul(self):
          return self.first-self.second
  
  pm = PlusMinus(5,4)
  # 상속 받은 클래스의 메서드가 실행 된다.
  print(pm.add())		# 20
  print(pm.mul())		# 1
  ```

  

- 클래스 변수

  - 클래스로 만든 모든 인스턴스가 공유하는 변수이다.

  ```python
  class BlueClub:
      gender = "male"
  
  print(BlueClub.gender)	# male
  bc1 = BlueClub()
  bc2 = BlueClub()
  print(bc1.gender)	# male
  print(bc2.gender)	# male
  
  # 변경할 경우 모든 인스턴스의 클래스 변수도 함께 변경된다.
  BlueClub.gender = "female"
  print(bc1.gender)	# female
  print(bc2.gender)	# female
  ```

  



# 모듈

