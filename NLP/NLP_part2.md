## Vector의 유사도

- Vector의 유사도

  - 두 문서 사이의 유사도를 판단하기 위해 각 문서를 vector로 변환한 후 vector 값 들의 유사도를 사용하는 방법이다.
  - 사람들은 서로 다른 두 문서의 유사도를 주로 문서들 간에 동일한 단어 또는 비슷한 단어가 얼마나 공통적으로 많이 사용되었는지에 의존한다.
    - 기계도 크게 다르지 않다.

  - 기계의 유사도 계산 성능은 아래와 같은 요인들에 달렸다.
    - 각 문서의 단어들을 어떤 방법으로 수치화했는지(DTM. Word2Vec 등).
    - 문서 간의 단어들의 유사성을 어떤 방법으로 계산했는지(cosine similarity, Euclidean distance 등).



- Cosine Similarity

  - 두 vector들 사이의 cosine 각도를 이용하여 구할 수 있는 두 vector의 유사도를 의미한다.
    - 두 vector의 방향이 완전히 동일하면 1, 90도의 각을 이루면 0, 180로 반대 방향이면 -1의 값을 갖는다.
    - 즉 -1 이상 1 이하의 값을 가지며 1에 가까울수록 유사도가 높다고 볼 수 있다.
    - 두 벡터 A, B에 대해 cosine similarity는 아래와 같이 구한다.
    - DTM이나 TF-IDF 행렬을 통해 문서의 유사도를 구하는 경우에는 DTM이나 TF-IDF 행렬이 각각의 특징 vector A, B가 된다.

  $$
  similarity=cos(\Theta) = {A \cdot B\over||A||\ ||B||} = {\sum_{i=1}^nA_i \times B_i \over \sqrt{\sum_{i=1}^n(A_i)^2} \times \sqrt{\sum_{i=1}^n(B_i)^2}}
  $$

  - 아래 세 개의 문서를 가지고 cosine similarity를 구해볼 것이다.
    - 토마토 맛 토
    - 토 맛 토마토
    - 토마토 맛 토마토 사탕

  - 위 세 개의 문서를 띄어쓰기를 기준으로 tokenizing하고 세 문서에 대해서 DTM을 만든다.

  ```python
  import pandas as pd
  
  def tf(t, d):
    	return d.count(t)
  
  def build_dtm(vocabulary):
      result = []
      for i in range(N):
          result.append([])
          d = docs[i]
          for j in range(len(vocabulary)):
              t = vocabulary[j]
              # tf 함수를 사용하여 DTM에 값을 채워 넣는다.
              result[-1].append(tf(t, d))
      return pd.DataFrame(result, columns = vocabulary)
  
  
  docs = [
      "토마토 맛 토",
      "토 맛 토마토 토마토 맛 토",
      "토마토 맛 토마토 사탕"
  ]
  N = len(docs)
  # 공백을 기준으로 tokenizing
  vocabulary = list(set(word for doc in docs for word in doc.split()))
  
  # DTM을 구한다.
  dtm = build_dtm(vocabulary)
  print(dtm)
  """
     사탕  맛  토마토  토
  0   0  1    1  1
  1   0  2    2  2
  2   1  1    2  0
  """
  ```

  - Numpy를 사용하여 cosine similarity를 구할 수 있다.
    - 문서1과 문서3의 cosine similarity와 문서2와 문서3의 cosine similarity가 같으며, 문서1과 문서2의 cosine similarity가 1이 나왔다.
    - 문서 2는 문서1에서 모든 단어의 빈도수가 1 증가한 문서이다.
    - 즉 문서 내의 모든 단어의 빈도수가 동일하게 증가하는 경우에는 기존의 문서와 코사인 유사도의 값이 1이다.
    - 이를 통해 알 수 있는 것은 cosine similarity는 vector의 방향(패턴)에 초점을 두기에 문서의 길이가 다른 상황에서도 비교적 문서 길이의 영향을 덜 받는다는 점이다.


  ```python
  from numpy import dot
  from numpy.linalg import norm
  
  
  def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))
  
  print('문서 1과 문서2의 유사도 :',cos_sim(dtm.iloc[0].to_list(), dtm.iloc[1].to_list()))		# 1.0000000000000002
  print('문서 1과 문서3의 유사도 :',cos_sim(dtm.iloc[0].to_list(), dtm.iloc[2].to_list()))		# 0.7071067811865476
  print('문서 2와 문서3의 유사도 :',cos_sim(dtm.iloc[1].to_list(), dtm.iloc[2].to_list()))		# 0.7071067811865476
  ```



- Euclidean distance

  - 다차원 공간에서 두 개의 점 사이의 거리를 통해 유사도를 판단하는 방법이다.
    - 거리가 가까울 수록 유사도가 높다고 본다.
  - 다차원 공간에서 두 개의 점 p와 q가 각각 $p=(p_1,...,p_n)$과 $q=(q_1,...,q_n)$의 좌표를 가질 때 두 점 사이의 거리를 계산하는 Euclidean distance를 구하는 공식은 아래와 같다.

  $$
  \sqrt{(q_1-p_1)^2 + (q_2-p_2)^2 + \dots + (q_n - p_n)^2} = \sqrt{\sum_{i=1}^n(q_i-p_i)^2}
  $$

  - Numpy를 사용하여 간단하게 구할 수 있다.
    - 위에서 cosine similarity를 구할 때 사용한 것과 동일한 문서로 동일한 DTM을 생성했다고 가정한다.
    - 문서1과 문서2가 문서1과 문서3보다 가까우므로 문서1은 문서3보다 문서2와 더 유사하다고 할 수 있다.

  ```python
  def dist(x,y):
      x = np.array(x) 
      y = np.array(y) 
      return np.sqrt(np.sum((x-y)**2))
  
  
  print('문서1과 문서2의 거리 :',dist(dtm.iloc[0].to_list(), dtm.iloc[1].to_list()))		# 1.7320508075688772
  print('문서1과 문서3의 거리 :',dist(dtm.iloc[0].to_list(), dtm.iloc[2].to_list()))		# 1.7320508075688772
  print('문서2와 문서3의 거리 :',dist(dtm.iloc[1].to_list(), dtm.iloc[2].to_list()))		# 2.449489742783178
  ```



- Jaccard similarity

  - 두 집합의 합집합에서 두 집합 교집합의 비율을 구하여 두 집합의 유사도를 구하는 방식이다.
    - 0에서 1사이의 값을 가지며, 두 집합이 유사할 수록 1에 가까와진다.
    - 자카드 유사도를 구하는 함수를 $J$라 할 때, $J$는 아래와 같다.

  $$
  J(A,B) = {|A \cap B|\over |A \cup B|} = {|A \cap B|\over |A|+|B|-|A \cap B|}
  $$

  - Python의 `set`을 사용하여 구현이 가능하다.

  ```python
  docs = [
      "토마토 맛 토",
      "토 맛 토마토 토마토 맛 토",
      "토마토 맛 토마토 사탕"
  ]
  
  tokenized_docs = list(map(set, [doc.split() for doc in docs]))
  union = tokenized_docs[0].union(tokenized_docs[1])
  intersection = tokenized_docs[0].intersection(tokenized_docs[1])
  
  for i in range(len(docs)):
      for j in range(i, len(docs)):
          if i == j:
              continue
          union = tokenized_docs[i].union(tokenized_docs[j])
          intersection = tokenized_docs[i].intersection(tokenized_docs[j])
          print("문서{} & 문서{}의 유사도:".format(i+1, j+1), len(intersection)/len(union))
          
  """
  문서1 & 문서2의 유사도: 1.0
  문서1 & 문서3의 유사도: 0.5
  문서2 & 문서3의 유사도: 0.5
  """
  ```

