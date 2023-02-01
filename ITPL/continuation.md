- 변경의 핵심
  - Store-passing style을 명시적으로 표현할 때와 마찬가지로, global하고, Store-passing이 적용되지 않은 코드를 없애야한다.
  - 각 function 호출시마다 암시적으로 넘기던 것을 명시적으로 넘겨야 한다.

```scala
// CPS를 적용하지 않은 factorial code
def factorial(n: Int): Int =
    if (n <= 1)
    	1
    else
    	n * factorial(n - 1)


// CPS를 적용하지 않은 factorial function에 종속적이다.
def factorialCps(n: Int, k: Cont): Int =
	k(factorial(n))


// 마찬가지로 아직 종속적
def factorialCps(n: Int, k: Cont): Int =
    if (n <= 1)
   		k(1)
    else
    	k(n * factorial(n - 1))
```



- continuation의 반환 type
  - continuation의 반환 type은 어느 type이든 될 수 있다.
  - 단, continuation은 이전 처리의 결과를 input으로 받고, 그 input을 처리한 결과를 다시 output으로 넘긴다.
    - 따라서 continuation의 반환 type은 전체 표현식의 반환 type과 같아야한다.



- `factorialCps(n, k)`의 continuation은 `(n-1)!`에 `n`을 곱한 값을 계산하는 것이다.