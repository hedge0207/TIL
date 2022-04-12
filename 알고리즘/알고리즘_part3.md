# 편집 거리 알고리즘

- 편집 거리 알고리즘(Edit Distance)이란
  - 두 문장의 유사도를 판별하는 알고리즘이다.
    - 표절 여부, 철자 오류 검사 등에 사용된다.
    - 뿐만 아니라 유전 및 의료 공학에서 유전자 유사도 판별에도 사용된다.
  - Hamming Distance,  Levenshtein Distance등의 알고리즘이 있다.



## Levenshtein Distance

> https://madplay.github.io/post/levenshtein-distance-edit-distance 참고

- 편집 거리를 구하기 위해 가장 흔히 사용되는 알고리즘이다.

  - 한 문장이 다른 문장이 되기 위하여 몇 번의 삽입, 수정, 삭제를 거쳐야 하는지 계산하고, 그 최소값을 구한다.
    - 연산 횟수가 적을 수록 두 문장 사이에 유사도가 높다고 판단한다.

  - 간단한 예시
    - word가 world가 되기 위해서는 한 번의 삽입(l을 삽입) 연산이 필요하다.
    - sun이 son이 되기 위해서는 u를 o로 바꾸는 한 번의 수정 연산이 필요하다.
    - world가 word가 되기 위해서는 한 번의 삭제(l을 삭제) 연산이 필요하다.



- 실제 예시

  - delegate가 delete가 되려면 몇 번의 연산을 거쳐야 하는가?
  - 아래와 같이 표를 작성한다.
    - 첫 번째 문자는 null로 채워넣는다.

  |      |      | d    | e    | l    | e    | t    | e    |
  | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
  |      |      |      |      |      |      |      |      |
  | d    |      |      |      |      |      |      |      |
  | e    |      |      |      |      |      |      |      |
  | l    |      |      |      |      |      |      |      |
  | e    |      |      |      |      |      |      |      |
  | g    |      |      |      |      |      |      |      |
  | a    |      |      |      |      |      |      |      |
  | t    |      |      |      |      |      |      |      |
  | e    |      |      |      |      |      |      |      |

  - null 문자에서 delete가 되는 과정
    - null문자에서 null문자가 되기 위해서는 아무 연산도 필요하지 않다(총 0번의 연산)
    - null 문자에서 d가 되기 위해서는 d를 삽입하는 연산이 1번 필요하다(총 1번의 연산).
    - null 문자에서 de가 되기 위해서는 d를 삽입하는 연산 1번과 e를 삽입하는 연산이 1번씩 필요하다(총 2번의 연산).
    - null 문자에서 de가 되기 위해서는 d를 삽입하는 연산 1번과 e를 삽입하는 연산이 1번, l을 삽입하는 연산이 1번씩 필요하다(총 3번의 연산).
    - (...중략...)
    - null문자에서 delete가 되기 위해서는 d,e,l,e,t,e를 한번씩 삽입하는 연산이 필요하다(총 6번의 연산)
    - null이 delegate가 되는 과정도 마찬가지다.

  |      |      | d    | e    | l    | e    | t    | e    |
  | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
  |      | 0    | 1    | 2    | 3    | 4    | 5    | 6    |
  | d    | 1    |      |      |      |      |      |      |
  | e    | 2    |      |      |      |      |      |      |
  | l    | 3    |      |      |      |      |      |      |
  | e    | 4    |      |      |      |      |      |      |
  | g    | 5    |      |      |      |      |      |      |
  | a    | 6    |      |      |      |      |      |      |
  | t    | 7    |      |      |      |      |      |      |
  | e    | 8    |      |      |      |      |      |      |

  - delegate의 d가 delete가 되는 과정
    - d가 d가 되기 위해서는 아무 연산도 필요하지 않다(총 0번의 연산).
    - d가 de가 되기 위해서는 e를 삽입하는 연산이 1번 필요하다(총 1번의 연산).
    - d가 del가 되기 위해서는 e, l을 삽입하는 연산이 1번씩 필요하다(총 2번의 연산).
    - (...중략...)
    - d가 delete가 되기 위해서는 e,l,e,t,e를 삽입하는 연산이 1번씩 필요하다(총 5번의 연산)
  - delegate의 de가 delete가 되는 과정
    - de가 d가 되기 위해서는 삭제 연산이 1번 필요하다(총 1번의 연산).
    - de가 de가 되기 위해서는 아무 연산도 필요하지 않다(총 0번의 연산).
    - (...후략...)
  - (...중략...)
  - delega가 delete가 되는 과정
    - (...전략...)
    - delega가 delete가 되기 위해서는 2번의 수정 연산(g->t, a->e)가 필요하다.
  - 위 과정을 전부 거치면 아래와 같은 표가 완성된다.
    - 표의 가장 우측 최하단에 있는 숫자(2)가 delegate를 delete로 변경하기 위한 최소 연산의 수가 된다.

  |      |      | d    | e    | l    | e    | t    | e    |
  | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
  |      | 0    | 1    | 2    | 3    | 4    | 5    | 6    |
  | d    | 1    | 0    | 1    | 2    | 3    | 4    | 5    |
  | e    | 2    | 1    | 0    | 1    | 2    | 3    | 4    |
  | l    | 3    | 2    | 1    | 0    | 1    | 2    | 3    |
  | e    | 4    | 3    | 2    | 1    | 0    | 1    | 2    |
  | g    | 5    | 4    | 3    | 2    | 1    | 1    | 2    |
  | a    | 6    | 5    | 4    | 3    | 2    | 2    | 2    |
  | t    | 7    | 6    | 5    | 4    | 3    | 2    | 3    |
  | e    | 8    | 7    | 6    | 5    | 4    | 3    | 2    |

  - 위와 같이 일일이 비교하지 않고도 구하는 방법이 존재한다.
    - 비교하는 문자가 같은 경우 11시 방향 대각선의 값을 그대로 가져온다.
    - 변경하려고 할 경우 11시 방향 대각선에서 +1한 값을 가져온다.
    - 삭제하려고 할 경우 위의 값에서 +1한 값을 가져온다.
    - 삽입하려고 할 경우 왼쪽 값에서 +1한 값을 가져온다.
  - Levenshtein Distance 알고리즘은 최소 거리를 구하는 알고리즘이므로 아래와 같이 요약이 가능하다.
    - 비교하는 문자가 같은 경우 11시 방향 대각선의 값을 그대로 가져온다.
    - 비교하는 문자가 다를 경우 11시, 위, 왼쪽 값 중 가장 작은 값에서 +1한 값을 가져온다.
    - 예를 들어 delegate의 마지막 e와 delete의 마지막 e는 같은 문자이므로 11시 방향 대각선 값인 2를 그대로 가져온다.
    - 반면에 delegate의 g와 delete의 l은 서로 다른 문자이므로 11시, 위, 왼쪽 중 가장 작은 값인 위의 값(1)에서 +1한 값을 가져온다.



- 코드로 구현

  > https://towardsdatascience.com/text-similarity-w-levenshtein-distance-in-python-2f7478986e75 참고

  - DP와 memorization 개념이 들어간다.

  ```python
  from functools import lru_cache
  
  def lev_dist(a, b):
      '''
      This function will calculate the levenshtein distance between two input
      strings a and b
      
      params:
          a (String) : The first string you want to compare
          b (String) : The second string you want to compare
          
      returns:
          This function will return the distnace between string a and b.
          
      example:
          a = 'stamp'
          b = 'stomp'
          lev_dist(a,b)
          >> 1.0
      '''
      
      @lru_cache(None)  # for memorization
      def min_dist(s1, s2):
  
          if s1 == len(a) or s2 == len(b):
              return len(a) - s1 + len(b) - s2
  
          # no change required
          if a[s1] == b[s2]:
              return min_dist(s1 + 1, s2 + 1)
  
          return 1 + min(
              min_dist(s1, s2 + 1),      # insert character
              min_dist(s1 + 1, s2),      # delete character
              min_dist(s1 + 1, s2 + 1),  # replace character
          )
  
      return min_dist(0, 0)
  ```



- 원리는 점화식을 이해한 뒤 추후 추가