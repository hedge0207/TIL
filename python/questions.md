

## Python은 왜 느린가?

> http://jakevdp.github.io/blog/2014/05/09/why-python-is-slow/

- Python은 동적 타이핑 언어다.

  - 동일한 결과를 얻기 위해서 더 많은 과정을 거쳐야 하기에 Python은 느릴 수 밖에 없다.
  - C와 같은 정적 타이핑 언어는 변수를 선언할 때 변수의 type을 함께 정의해주기에, 해당 변수의 type을 바로 알 수 있다.

  ```c
  int a = 1;
  int b = 2;
  int c = a + b;
  
  /*
  int 타입인 1을 a에 할당한다.
  int 타입인 2를 b에 할당한다.
  + 연산자를 통해 그 둘을 더한다.
  더한 값을 c에 할당한다.
  */
  ```

  - 반면에 Python의 경우 Python 프로그램이 실행될 때, interpreter는 코드에 정의된 변수의 type을 모르는 상태다.
    - Interpreter가 아는 것은 각 변수가 모두 Python Object라는 것이다.

  ```python
  a = 1
  b = 2
  c = a + b
  
  """
  1. 1을 a에 할당
    - a 변수의 PyObject_HEAD의 typecode를 int로 설정
    - a에 int type인 1을 할당
  2. 2를 b에 할당
    - b 변수의 PyObject_HEAD의 typecode를 int로 설정
    - b에 int type인 2를 할당
  3. 더하기
    - a의 PyObject_HEAD의 typecode 찾기
    - a는 interger이며, a의 val은 1이라는 것을 인지
    - b의 PyObject_HEAD의 typecode 찾기
    - b는 interger이며, b의 val은 2라는 것을 인지
    - a와 b를 더한다.
  4. 결과 값을 c에 할당
    - c 변수의 PyObject_HEAD의 typecode를 int로 설정
    - a에 int type인 1을 할당
  """
  ```



- Python은 컴파일 언어 보다는 인터프리터 언어에 가깝다.
  - 좋은 컴파일러는 반복되거나 불필요한 연산을 미리 찾아내어 속도를 높일 수 있다.
  - 그러나 인터프리터 언어에 가까운 Python은 위 방식이 불가능하다.



- Python의 object model은 비효율적인 메모리 접근을 유발할 수 있다.

  - 많은 언어들은 원시 자료형을 지원한다.
    - 원시 자료형은 어떤 데이터의 참조를 담고 있는 자료형이 아닌 값 그 자체를 담을 수 있는 자료형이다.
    - 그러나 python에는 원시 자료형 자체가 존재하지 않는다.
  - Python의 모든 것은 객체이다.
    - Python의 모든 변수들은 data 자체를 저장하고 있는 것이 아니라 data를 가리키는 pointer를 저장하고 있다.

  - 예시

    - 다른 언어들에서 일반적으로 원시 자료형이라 불리는 integer 등도 하나의 객체이다.

    - C에서 `int a = 1`의 a는 숫자 1 자체를 저장하고 있지만, Python에서  `a = 1`의 a는 숫자 1을 가리키는 pointer를 저장하고 있는 것이다.