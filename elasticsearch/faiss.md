# 사전지식

- 단어 집합(vocabulary, 혹은 사전)
  - 서로 다른 단어들의 집합
  - 단어 집합에서는 기본적으로 book과 books와 같이 단어의 변형 형태도 서로 다른 단어로 간주한다.



- 말뭉치(corpus)
  - 자연어 연구를 위해 특정한 목적을 가지고 언어의 표본을 추출한 집합.



- 원-핫 인코딩(One-Hot Encoding)

  - 자연어 처리에서 문자를 숫자로 바꾸는 여러 기법 중 하나
    - 컴퓨터는 문자보다는 숫자를 더 잘 처리하기에 자연어 처리를 할 때에는 문자를 숫자로 변경해준다.
  - 단어 집합(vocabulary, 혹은 사전)
    - 서로 다른 단어들의 집합
    - 단어 집합에서는 기본적으로 book과 books와 같이 단어의 변형 형태도 서로 다른 단어로 간주한다.
    - 텍스트의 모든 단어를 중복을 허용하지 않고 모아놓으면 이를 단어 집합이라 할 수 있다.
  - 단어 집합의 크기를 벡터의 차원으로 표현하고, 표현하고 싶은 단어의 인덱스에 1의 값을 부여하고 다른 인덱스에는 0을 부여하는 단어의 벡터 표현 방식이다.
    - 이렇게 표현된 벡터를 원-핫 벡터라 부른다.
  - 크게 두 단계를 거친다.
    - 각 단어에 고유한 인덱스를 부여한다(정수 인코딩).
    - 표현하고 싶은 단어의 인덱스의 위치에 1을 부여하고, 다른 단어의 인덱스의 위치에는 0을 부여한다.

  - 예시

  ```python
  # 텍스트
  text = '나는 밥을 먹는다.'
  
  # 토큰화
  ['나', '는', '밥', '을', '먹는다']
  
  # 각 단어에 인덱스 부여
  {'나': 0, '는': 1, '밥': 2, '을': 3, '먹는다': 4}
  
  # 원-핫 인코딩을 활용하여 벡터화
  # 각 단어의 인덱스에 해당하는 값만 1이 되고 나머지는 모두 0이 된다.
  [[1,0,0,0,0],	# 나
  [0,1,0,0,0],	# 는
  [0,0,1,0,0],	# 밥
  [0,0,0,1,0],	# 을
  [0,0,0,0,1]]	# 먹는다
  ```

  - 한계
    - 단어의 개수가 늘어날 수록, 벡터를 저장하기 위해 필요한 공간(벡터의 차원)이 계속 늘어난다.
    - 단어 집합의 크기가 곧 벡터의 차원 수가 된다.
    - 만일 단어가 1000개인 코퍼스를 가지고 원 핫 벡터를 만들면, 모든 단어 각각은 모두 1,000 개의 차원을 가진 벡터가 된다.
    - 다시 말해 모든 단어 각각은 하나의 값만 1을 가지고, 999개의 값은 0의 값을 가지는 벡터가 되는데 이는 저장 공간 측면에서 매우 비효율적인 표현 방법이다.
    - 또한 단어의 유사도를 표현하지 못한다는 단점이 존재한다.



- 워드 임베딩
  - 희소 표현(Sparse representation)
    - 원-핫 인코딩을 통해 나온 원-핫 벡터들과 같이 벡터 또는 행렬의 값이 대부분 0으로 표현되는 방법을 희소표현이라 한다.
    - 희소 표현 방식으로 표현한 벡터를 희소 벡터라 한다.
  - 밀집 표현(Dense representation)
    - 희소 표현의 반대 개념으로 벡터의 차원을 단어 집합의 크기로 상정하지 않는다.
    - 사용자가 설정한 값으로 모든 단어의 벡터 표현의 차원을 맞춘다.
    - 이 과정에서 더 이상 0과 1만 가진 값이 아닌 실수값을 가지게 된다.
    - 예를 들어 단어가 1000 개인 코퍼스에서 강아지라는 단어를 희소표현으로는 [1,0,0,0, 996개의 0]과 같이 표현한다면,
    - 밀집 표현에서는 사용자가 차원을 4로 설정했다면 [0.2, 1.8, 1.1, -2.1]과 같이 표현된다.
  - 단어를 밀집 벡터의 형태로 표현하는 방법을 워드 임베딩이라 한다.
    - 밀집 벡터를 워드 임베딩 과정을 통해 나온 결과라고 하여 임베딩 벡터라고도 부른다.



# faiss 개요

- faiss
  - 효율적인 유사도 검색과 밀집 벡터(dense vectors)의 클러스터링(clustering)을 위한 라이브러리
    - 클러스터링: 데이터를 데이터 간의 유사도에 따라 k개의 그룹으로 나누는 것.

  - 유사도 검색
    - d 차원에 x_i라는 벡터들의 집합이 주어지면, faiss는 이들을 가지고 RAM에 index라는 이름의 데이터 구조를 구축한다.
    - 인덱스 구축이 완료된 후 d 차원의 새로운 벡터값 x가 주어지면, 인덱스에서 x와 가장 유사한 벡터값을 찾는다.
  - C++로 작성되었다.



- faiss 설치하기

  - anaconda를 통해 설치해야 한다.

  ```bash
  # CPU 버전
  $ conda install -c pytorch faiss-cpu
  
  # GPU(+CPU) 버전
  $ conda install -c pytorch faiss-gpu
  
  # 특정 CUDA 버전을 설치
  $ conda install -c pytorch faiss-gpu cudatoolkit=10.2 # for CUDA 10.2
  ```



- 시작하기

  - faiss는 일반적으로 수십개에서 수백개의 고정된 차원(d)의 벡터 집합을 다룬다.
    - 이 벡터 집합은 메트릭스 형태(행과 열이 있는 형태)로 저장된다.
    - 이 메트릭스에는 오직 32-bit 부동소수점 형태만을 입력이 가능하다.
  - 인덱스에 저장할 벡터 생성하기
    - numpy의 random 함수를 이용하여 실제 벡터 값과 유사한 5개의 벡터 샘플을 32차원으로 생성한다.
    - numpy의 random 함수는 첫 번째 인자로 행의 개수, 두 번째 인자로 열의 개수를 받는다.

  ```python
  import numpy as np
  
  d = 32  # dimension
  nb = 5  # 벡터 샘플의 개수
  
  # faiss 인덱스에서 허용하는 유일한 타입인 float32 타입을 갖는 5개의 난수를 생성한다.
  vd = np.random.random((nb, d)).astype('float32')
  
  print(vd)
  
  '''
  [[0.4659283  0.42918417 0.01298451 0.9269639  0.05621753 0.7351387
    0.63571554 0.86692244 0.5866233  0.29657757 0.11990956 0.85105425
    0.6538739  0.33062434 0.6977781  0.7647909  0.7351392  0.95469826
    0.05220455 0.8614601  0.3923799  0.17863388 0.22511123 0.70524293
    0.27818888 0.03589209 0.6745775  0.7411113  0.3825581  0.76772106
    0.7750249  0.78105927]
   [0.28354147 0.14845583 0.5041909  0.43917158 0.6028518  0.27814764
    0.93687785 0.925087   0.9161655  0.6958438  0.78605276 0.64411163
    0.8175183  0.9495612  0.3956658  0.2993481  0.8905652  0.52639216
    0.89879274 0.66501343 0.48250428 0.89758825 0.9712463  0.4691813
    0.03092448 0.16588193 0.38339794 0.02846475 0.546486   0.30336487
    0.19934377 0.7564637 ]
   [0.3471091  0.7783196  0.6439691  0.16961639 0.20240185 0.70789915
    0.01438617 0.5426006  0.2617067  0.36044455 0.514728   0.02281249
    0.20670229 0.3750471  0.985061   0.4162246  0.55465186 0.8800842
    0.9513658  0.2916382  0.01115082 0.6450339  0.5791974  0.12054065
    0.48100883 0.8372618  0.6625179  0.30839232 0.671437   0.6918782
    0.63359994 0.02588365]
   [0.16880319 0.14798965 0.78834933 0.6159184  0.27801704 0.854614
    0.32414752 0.03574207 0.43986765 0.95678073 0.14045487 0.09732798
    0.15858607 0.5140166  0.36330354 0.36213607 0.31542563 0.7941953
    0.17334807 0.46838593 0.00850026 0.50660694 0.07101087 0.5871371
    0.70244664 0.99327904 0.6349156  0.35885695 0.13274446 0.37857753
    0.8203621  0.15009409]
   [0.83770096 0.9035732  0.77767766 0.34106514 0.8665412  0.9165315
    0.37519315 0.38307557 0.13840424 0.21772291 0.46787208 0.99518454
    0.53366786 0.5318203  0.2097983  0.52776855 0.9512746  0.06041929
    0.9948824  0.04607703 0.15952021 0.08325534 0.00547846 0.9933608
    0.3836217  0.7754981  0.65809315 0.60108423 0.919548   0.25876355
    0.45998612 0.23619007]]
  '''
  ```

  - 벡터 값들을 넣을 인덱스 생성하기

  ```python
  import numpy as np
  import faiss
  
  d = 32  # dimension
  nb = 5
  
  vd = np.random.random((nb, d)).astype('float32')
  
  # 인덱스와 벡터의 차원이 일치해야 한다.
  index = faiss.IndexFlatL2(d)
  # train된 인덱스인지 확인
  print(index.is_trained)	# True
  # 인덱스에 벡터값 추가
  index.add(vd)
  # 인덱스에 저장된 모든 벡터값들의 개수 확인
  print(index.ntotal)		# 5
  ```

  






