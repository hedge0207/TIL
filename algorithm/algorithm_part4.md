

- two pointer
  - 배열에서 원래 이중 for문으로 O(N<sup>2</sup>)에 처리되는 작업을 2개 포인터의 움직임으로 O(N)에 해결하는 알고리즘
    - 완전 탐색으로 풀면 시간 초과가 나는 문제에 적용하면 풀리는 경우가 많다.
  - 종류
    - 앞에서 시작하는 포인터와 끝에서 시작하는 포인터가 만나는 형식
    - 동일한 지점에서 시작하여 빠른 포인터가 느린 포인터 보다 앞서가는 방식
  - 유사한 알고리즘으로 슬라이딩 윈도우가 있다.



- List를 최대한 균등하게 N분할하기

  - code

  ```python
  def split(a, n):
      k, r = divmod(len(a), n)
      result = []
      st = 0
      print(k, r)
      for i in range(n):
          # 나머지가 다 소진될 때 까지 앞에서부터 1개씩 추가한다.
          # 뒤에 있는 것들은 1칸씩 밀리기에 또 다시 1씩 증가시키면서 더해줘야한다.
          # 나머지가 다 소진되면, 나머지 만큼만 더해준다.
          ed = (i + 1) * k + min(i + 1, r)
          arr = a[st:ed]
          st = ed
          result.append(arr)
  
      return result
  
  
  arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  for i in split(arr, 4):
      print(i)
  ```

  - 예시
    - `[1,2,3,4,5,6,7,8,9,10,11]`라는 list를 4(`N`)분할 하고자 한다.
    - Element의 개수가 11개이므로 `11 // 4`를 하면 2가 되고, 나머지(`11 % 4`)는 3이 된다.
    - 즉, 4개로 분할하면 분할 된 list 하나 당 2개가 들어가고 3개가 남게 된다.
    - `[1, 2]`, `[3, 4]`, `[5, 6]`, `[7, 8]`이 되고, `[9, 10, 11]`은 남게 된다.
    - 남은 3개의 element를 앞에서부터 하나씩 추가하여 `[1, 2, 9]`, `[3, 4, 10]`, `[5, 6, 11]`, `[7, 8]`이 되도록 해도 되지만, 이러면 list의 순서를 유지해야 하는 경우 문제가 된다.
    - 따라서, 처음에 분할 할 때 부터 앞에서부터 나머지에서 1개의 element씩을 빼서 분배해주는 방식을 사용해야한다.
    - 즉 나머지가 3이므로 처음 반복문을 순회할 때 나머지 중 1개를 더 추가하여 `[1,2,3]`으로 분할한다.
    - 다음 순회 때 나머지 중 1개를 더 추가하여 `[4,5,6]`으로 분할한다.
    - 다음 순회 때 나머지 중 1개를 더 추가하여 `[7,8,9]`로 분할한다.
    - 더 이상 나머지가 남아있지 않으므로 남은 것은 나머지 추가 없이 `[10, 11]`로 분할한다.
    - 즉 나머지를 r이라 할 때, 처음 분할 된 r개의 list에는 몫 + 1개의 element가 들어가게 되고, 더 이상 나머지가 남아있지 않은 r ~ N까지의 list에는 몫 만큼의 element가 들어가게 된다.
  - 구현
    - `+ min(i + 1, r)`는 순전히 나머지 처리를 위한 것으로, 나머지가 0이라면 이 코드는 필요 없다.
    - `min`을 제외하면 code는 `(i + 1) * k + i + 1`가 된다.
    - 여기서 `+1`은 나머지를 1개씩 추가해주기 위함이다.
    - 앞의 순회에서 `+1`을 하여 나머지 1개 만큼을 추가했으므로, 뒤에서는 index가 1씩 밀리게 되어 index를 뒤로 갈 수록 점점 증가시켜줘야한다.
    - 이를 위해서 순회시마다 1씩 증가하는 `i`를 사용하여, `i`를 더해준다. 
    - 따라서 더 이상 추가할 나머지가 남아있지 않으면, 즉 `i+r > r`이면, 더 이상 `+1` 씩 index를 더해주지 않고 앞에서 추가한 index의 개수 만큼만 index를 뒤로 미룬다.
  - 즉 위 code는 더 풀어쓰면 아래와 같다.

  ```python
  def split(a, n):
      k, r = divmod(len(a), n)
  
      result = []
      i = 0
      st = 0
      remaining_r = r
      while i < n:
          # 나머지가 0일 때의 끝 index
          ed = (i + 1) * k
      	# 만약 더 이상 분배할 나머지가 없다면,
          # 앞에서 밀린 index를 만큼을 ed에 추가해준다.
          if remaining_r == 0:
              ed += r
          # 아직 남아 있는 나머지가 있다면,
          else:
              # 나머지 중 1 개를 ed에 추가하고
              ed += 1
              # 나머지에서 1을 뺀다.
              remaining_r -= 1
              # 그 후 나머지로 인해 밀린 index를 반영하기 위해 i를 더한다.
              ed += i
          result.append(a[st:ed])
          st = ed
          i += 1
      return result
  
  
  arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  for i in split(arr, 5):
      print(i)
  ```






# 에라스토테네스의 체

- 에라스토테네스의 체

  - 소수(prime number)를 판별하는데 사용하는 알고리즘이다.
    - 고대 그리스의 수학자 에라스토테네스가 발견하였다.
    - 체 처럼 소수가 아닌 수 들을 걸러낸다.
  - 알고리즘
    - 2부터 소수를 구하고자 하는 구간의 모든 수를 나열한다.
    - 나열한 수를 앞에서부터 탐색해 나간다.
    - 첫 수인 2는 소수이므로 소수라는 표시를 한다.
    - 나열 된 숫자들에서 2의 배수인 것들은 모두 소수가 아니라는 표시를 한다.
    - 3은 표시가 되어 있지 않고, 소수이므로 소수라는 표시를 한다.
    - 나열 된 숫자들에서 3의 배수인 것들은 모두 소수가 아니라는 표시를 한다.
    - 4는 소수가 아니라는 표시가 되어 있으므로 넘어간다.
    - 5는 표시가 되어 있지 않고, 소수이므로 소수라는 표시를 한다.
    - 나열 된 숫자들에서 5의 배수인 것들은 모두 소수가 아니라는 표시를 한다.
    - 이를 모든 수에 대해 반복한다.
  - 구현

  ```python
  def prime_list(n):
      # 에라토스테네스의 체 초기화: n개 요소에 True 설정(소수로 간주)
      sieve = [True] * n
  
      # n의 최대 약수가 sqrt(n) 이하이므로 i=sqrt(n)까지 검사
      m = int(n ** 0.5)
      for i in range(2, m + 1):
          if sieve[i] == True:           # i가 소수인 경우
              for j in range(i+i, n, i): # i이후 i의 배수들을 False 판정
                  sieve[j] = False
  
      # 소수 목록 산출
      return [i for i in range(2, n) if sieve[i] == True]
  ```

  - 주의사항

    > [참고](https://nahwasa.com/entry/%EC%97%90%EB%9D%BC%ED%86%A0%EC%8A%A4%ED%85%8C%EB%84%A4%EC%8A%A4%EC%9D%98-%EC%B2%B4-%ED%98%B9%EC%9D%80-%EC%86%8C%EC%88%98%ED%8C%90%EC%A0%95-%EC%8B%9C-%EC%A0%9C%EA%B3%B1%EA%B7%BC-%EA%B9%8C%EC%A7%80%EB%A7%8C-%ED%99%95%EC%9D%B8%ED%95%98%EB%A9%B4-%EB%90%98%EB%8A%94-%EC%9D%B4%EC%9C%A0)

    - n까지의 소수 판별시에 n의 제곱근까지만 확인하면 된다(위 코드에서도 `n ** 0.5`까지만 확인했다).
    - n은 자연수 a, b에 대해 `n = a * b`라고 표현할 수 있다.
    - 또 n의 제곱근 m에 대해 `n = m * m`라고 표현할 수 있다.
    - 따라서, `a * b = m * m`이라 할 수 있다.
    - 이 때, a, b는 자연수여야하므로, a, b가 자연수임을 만족하는 경우는 아래의 세 가지 경우 뿐이다.
    - `a=m & b=m`, `a<m & b>m`, `a>m & b<m`
    - 즉, `min(a, b)<=m`이라고 할 수 있다.
    - N의 약수에 해당하는 a와 b 중 하나는 무조건 m 이하이므로, m까지만 조사하면 n이 소수인지 알 수 있게 된다.


