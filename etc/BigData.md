# 기초

## Pandas

- Pandas

  - 파이썬의 데이터 분석 라이브러리로 행과 열로 이루어진 데이터 객체를 만들어 다룰 수 있게 해줘 보다 안정적으로 대용량 데이터를 처리할 수 있게 도와준다.
- Anaconda에 기본적으로 제공되지만, 아나콘다를 사용하지 않을 경우에는 설치해야 한다.
  - import해서 사용해야 한다.
    - import 할 때 파일명을 import할 module 이름과 다르게 설정해야 한다.
- numpy





## Pandas의 자료 구조

- Series

  - 1차원 자료구조로 리스트와 같은 시퀀스 데이터를 받아들이는데, 별도의 인덱스 레이블을 지정하지 않으면 자동으로 0부터 시작되는 디폴트 정수 인덱스를 사용한다.
  - 파이썬의 리스트를 기초로 만든 자료형이다.

  ```python
  import pandas as pd
   
  data = [1, 3, 5, 7, 9]
  s = pd.Series(data)
  print(s)
  
  #out
  0  1
  1  3
  2  5
  3  7
  4  9
  dtype:int64
  ```

  - Series의 메소드

  ```python
  #Series의 값만 확인하기
  print(s.values)
  #Series의 인덱스만 확인
  print(s.index)
  #Series의 자료형 확인
  print(s.dtype)
  
  #인덱스를 직접 설정하기
  s2 = pd.Series([2,4,6,8],index=['a','b','c','d'])
  print(s2)
  
  #out
  [1 3 5 7 9]
  RangeIndex(start=0, stop=5, step=1)
  int64
  a    2
  b    4
  c    6
  d    8
  dtype: int64
  ```

  - dictionary 자료형을 Series로 변경하면 dictionary의 key가 Series의 index가 된다.

  ```python
  dic = {'a':1,'b':2,'c':3}
  s2 = pd.Series(dic)
  
  print(s2)
  
  #out
  a    1
  b    2
  c    3
  dtype: int64
  ```

  - Series, index의 이름을 설정하는 것도 가능하다.

  ```python
  s2.name='이름'
  s2.index.name="인"
  print(s2)
  
  #out
  인
  a    1
  b    2
  c    3
  Name: 이름, dtype: int64
  ```

  

- DataFrame

  - Series의 결합체

  ```python
  s1 = pd.core.series.Series([1,2,3])
  s2 = pd.core.series.Series(['a','b','c'])
  
  df=pd.DataFrame(data=dict(num=s1,word=s2))
  print(df)
  
  
  #out
     num word
  0    1    a
  1    2    b
  2    3    c
  ```

  - 생성

  ```python
  #기본적인 생성 방법
  변수명 = pd.DataFrame(data=데이터로 넣을 값, index=인덱스(행)로 넣을 값, columns=열로 넣을 값)
  
  #방법1. python의 dictionary를 사용
  data = {
      'year': [2016, 2017, 2018],
      'name': ['김', '이', '박'],
      'height': ['1.637M', '1.73M', '1.83M']
  }
   
  df = pd.DataFrame(data)
  print(df)
  
  #out
     year name  height
  0  2016    김  1.637M
  1  2017    이   1.73M
  2  2018    박   1.83M
  
  #방법2-1. python의 list를 사용
  data = [
      [2016,'김','1.637M'],
      [2017,'이','1.73M'],
      [2018,'박','1.83M']
  ]
  column_name = ['year','name','height']
  df = pd.DataFrame(data,columns=column_name)
  print(df)
  
  
  #out
     year name  height
  0  2016    김  1.637M
  1  2017    이   1.73M
  2  2018    박   1.83M
  
  #방법2-2. 위 방법을 한 번에 하는 방법
  data = [
      ['year',[2016,2017,2018,]],
      ['name',['김','이','박']],
      ['height',['1.637M','1.73M','1.83M']]
  ]
  df = pd.DataFrame.from_items(data)
  print(df)
  
  
  #out
     year name  height
  0  2016    김  1.637M
  1  2017    이   1.73M
  2  2018    박   1.83M
  ```

  - DataFrame의 메소드

  ```python
  #행의 인덱스
  print(df.index)
  #열의 인덱스
  print(df.columns)
  #값 얻기
  print(df.values)
  
  #out
  RangeIndex(start=0, stop=3, step=1)
  Index(['year', 'name', 'height'], dtype='object')
  [[2016 '김' 1.637]
   [2017 '이' 1.73]
   [2018 '박' 1.83]]
  
  
  #연산 메소드
  
  #sum():합계
  print(df['height'].sum())
  #mean(): 평균
  print(df['height'].mean())
  #min(): 최소
  print(df['height'].min())
  #max(): 최대
  print(df['height'].max())
  #describe():기본적인 통계치 전부
  print(df.describe())
  #head(): 처음 5개의 행 표시, 괄호 안에 숫자를 넣을 경우 해당 숫자 만큼의 행 표시
  #tail(): 마지막 5개의 행 표시, 괄호 안에 숫자를 넣을 경우 해당 숫자 만큼의 열 표시
  
  #out
  5.197
  1.7323333333333333
  1.637
  1.83
           year    height
  count     3.0  3.000000
  mean   2017.0  1.732333
  std       1.0  0.096521
  min    2016.0  1.637000
  25%    2016.5  1.683500
  50%    2017.0  1.730000
  75%    2017.5  1.780000
  max    2018.0  1.830000
  ```

  - 행, 열 인덱스의 이름 설정하기

  ```python
  df.index.name = 'Num'
  df.columns.name = 'Info'
  print(df)
  
  #out
  Info  year name  height
  Num
  0     2016    김   1.637
  1     2017    이   1.730
  2     2018    박   1.830
  ```

  - DataFrame을 생성하면서 columns와 index를 설정 가능.

  ```python
  data = {
      'year': [2016, 2017, 2018],
      'name': ['김', '이', '박'],
      'height': ['1.637M', '1.73M', '1.83M']
  }
   
  df = pd.DataFrame(data,columns=['name','height','year','weight'],index=['one','two','three'])
  
  #out
  #아래에서 확인 가능한 것 처럼 data의 순서와 DataFrame을 정의할 때의 columns의 순서가 달라도 key값을 알아서 찾아서 정의해준다. 단, data에 포함되어 있지 않았던 값(예시의 경우 weigth)은 NaN으로 나타나게 된다. 
        name  height  year weight
  one      김   1.637  2016    NaN
  two      이   1.730  2017    NaN
  three    박   1.830  2018    NaN
  ```

  - 열 추가

  ```python
  df['gender']='male'
  print(df)
  
  
  df['gender']=['female','male','male']
  print(df)
  
  
  #out
        name  height  year weight gender
  one      김   1.637  2016    NaN   male
  two      이   1.730  2017    NaN   male
  three    박   1.830  2018    NaN   male
        name  height  year weight  gender
  one      김   1.637  2016    NaN  female
  two      이   1.730  2017    NaN    male
  three    박   1.830  2018    NaN    male
  
  
  #Series를 추가할 수도 있다.
  val = pd.Series([1,8],index=['one','three'])
  df['some']=val
  print(df)
  
  
  #out
        name  height  year weight  gender  some
  one      김   1.637  2016    NaN  female   1.0
  two      이   1.730  2017    NaN    male   NaN
  three    박   1.830  2018    NaN    male   8.0
  
  
  #계산후 열 추가
  df['some2']=df['heigth']+df['year']
  print(df)
  
  #out
        name  height  year weight  gender     some2
  one      김   1.637  2016    NaN  female  2017.637
  two      이   1.730  2017    NaN    male  2018.730
  three    박   1.830  2018    NaN    male  2019.830
  ```

  - 열 삭제

  ```python
  del df['some']
  print(df)
  
  #out
        name  height  year weight  gender
  one      김   1.637  2016    NaN  female
  two      이   1.730  2017    NaN    male
  three    박   1.830  2018    NaN    male
  ```

  - 행 추가

  ```python
  df.loc['four']=['최',2017,1,701,68,'male']
  print(df)
  
  #out
        name  height    year weight  gender    some2
  one      김   1.637  2016.0    NaN  female  2017.64
  two      이   1.730  2017.0    NaN    male  2018.73
  three    박   1.830  2018.0    NaN    male  2019.83
  four     최   1.000  2017.0  1,701      68     male
  ```

  

- Panel
  
  - 3차원 자료 구조로 Axis 0(items), Axis 1(major_axis), Axis 2(minor_axis) 등 3개의 축을 가지고 있는데 Axis 0은 그 한 요소가 DataFrame에 해당되며, Axis 1은 DataFrame의 행에 해당되고, Axis 2는 DataFrame의 열에 해당된다.



- Data 접근

  - 인덱싱 혹은 속성을 사용하여 데이터에 접근한다.

  ```python
  data = {
      'year': [2016, 2017, 2018],
      'name': ['김', '이', '박'],
      'height': ['1.637M', '1.73M', '1.83M']
  }
   
  df = pd.DataFrame(data)
  
  print(df['year'])   #인덱싱
  #혹은 아래와 같이 filter를 사용할 수도 있다. sql문과 동일하게 like, regex 등의 문법을 사용 가능하다.
  #df.filter(itmes=['year'])
  
  print(df.year)      #속성
  
  #out
  # 결과는 같다.
  0    2016
  1    2017
  2    2018
  Name: year, dtype: int64
  0    2016
  1    2017
  2    2018
  Name: year, dtype: int64
  ```

  - boolean indexing:  특정 조건의 데이터만 필터링

  ```python
  #df는 위에서 선언한 것과 같다.
  print(df['gender']=='male')
  #혹은 query를 통해서도 가능하다.
  # ex.df.query('gender==male')
  print(df[df['year']>2016])
  
  
  #out
  one      False
  two       True
  three     True
  four     False
  Name: gender, dtype: bool
     year name height
  1  2017    이  1.73
  2  2018    박  1.83
  
  
  #새로운 값도 대입 가능
  df.loc[df['year']>2017,'weight']=71
  print(df)
  
  #out
        name  height    year weight  gender    some2
  one      김   1.637  2016.0    NaN  female  2017.64
  two      이   1.730  2017.0    NaN    male  2018.73
  three    박   1.830  2018.0     71    male  2019.83
  four     최   1.000  2017.0  1,701      68     male
  ```
  - 행 인덱싱

  ```python
  print(df[0:2]) #0번째 부터 2번째 앞까지 가져온다.
  
  #out
      name  height  year weight  gender     some2
  one    김   1.637  2016    NaN  female  2017.637
  two    이   1.730  2017    NaN    male  2018.730
  
  print(df['one':'three']) #앞에 쓴 인덱스부터 뒤에 쓴 인덱스까지 가져온다.
  
  #out
        name  height  year weight  gender     some2
  one      김   1.637  2016    NaN  female  2017.637
  two      이   1.730  2017    NaN    male  2018.730
  three    박   1.830  2018    NaN    male  2019.830
  
  
  
  #loc를 사용하면 특정 행의 정보만 가져올 수 있다. Series 형태로 반환한다.
  print(df.loc['two']) 
  #,로 구분하여 복수의 행 정보를 가져올 수 있다.
  #ex.df.loc['one','three'] 
  
  #out
  name            이
  height       1.73
  year         2017
  weight        NaN
  gender       male
  some2     2018.73
  Name: two, dtype: object
          
  print(df.loc['one':'two'])
  
  #out
      name  height  year weight  gender     some2
  one    김   1.637  2016    NaN  female  2017.637
  two    이   1.730  2017    NaN    male  2018.730
  
  
  
  #특정 행의 특정 열을 가져오는 것도 가능하다.
  print(df.loc[:,['year','gender']])
  print(df.loc['one':'two','year':'gender'])
  
  #out
         year  gender
  one    2016  female
  two    2017    male
  three  2018    male
       year weight  gender
  one  2016    NaN  female
  two  2017    NaN    male
  
  
  #iloc을 사용하는 방법, 인덱스 번호를 사용한다는 것만 제외하면 loc과 동일하다.
  #.iloc[행,열]
  print(df.iloc[0:2,2:5])
  print(df.iloc[[0,1],[2,3,4]])  # 결과는 같다.
  
  #out
         year weight  gender
  one  2016.0    NaN  female
  two  2017.0    NaN    male
         year weight  gender
  one  2016.0    NaN  female
  two  2017.0    NaN    male
  
  
  
  #boolean indexing과 함께 사용
  print(df.loc[df['gender']=='male',['year','height']])
  
  #out
           year  height
  two    2017.0    1.73
  three  2018.0    1.83
  ```

  

  

  

- 외부 데이터 읽고 쓰기

  - pandas는 CSV, txt, Excel, SQL, HDF5 포맷 등 다양한 외부 리소스 데이터를 일고 쓸 수 있는 기능을 제공한다.
  
  - 읽을 때는 `read_파일유형`, 쓸 때는 `to_파일유형`을 통해 가능하다.
    
    - excel의 경우 read_excel, to_excel로 사용하면 된다.
    - txt는 `read_csv`로 가져온다.
    
  - 각 열이 `,`로 구분되어 있으면 추가적인 코드 없이 `,`를 기준으로 분절되어 들어오지만 다른 것으로 구분되어 있을 경우 아래와 같이 `delimiter`라는 인자를 넘겨줘야 한다.
  
    ```python
    # 탭으로 구분된 경우
    df = pd.read_csv('data/list.txt',delimiter='\t')
    ```
  
  - 또한 읽어올 때 별도의 코드가 없으면 가장 첫 행이 열의 이름이 된다. 따라서 아래와 같이 `header=None`을 입력하면 열의 이름은 자동으로 0부터 시작하는 숫자가 들어가게 된다.
  
    ```python
    df=pd.read_csv('data/list.txt',header=None)
    
    #만일 header를 넣고 싶으면 아래와 같이 해주면 된다.
    df.columns = ['a','b','c']
    
    #두 과정을 동시에 하려면 아래와 같이 하면 된다.
    df=pd.read_csv('data/list.txt',header=None, names=['a','b','c'])
    ```
  
  - Dataframe을 파일로 저장
  
    ```python
    data = {
        'year': [2016, 2017, 2018],
        'name': ['김', '이', '박'],
        'height': ['1.637M', '1.73M', '1.83M']
    }
     
    df = pd.DataFrame(data)
    
    df.to_csv('파일명.csv')
    
    #코드를 작성한 파일이 있는 폴더에 파일명.csv 파일이 생성된다.
    
    #기본적으로 인덱스와 헤더가 함께 저장이 되는데 이를 막고 싶으면 아래와 같이 작성하면 된다.
    df.to_csv('파일명.csv',index=False,header=False)
    
    #또한 데이터가 비어있을 경우 기본적으로 빈칸이 되는데 이를 빈 칸이 아닌 다른 값으로 하고 싶다면 아래와 같이 하면된다.
    df.to_csv('파일명.csv',na_rap='대신할 값')
    ```
  
    
  
  









## Matplotlib

- Matplotlib:  파이썬에서 데이타를 차트나 플롯(Plot)으로 그려주는 라이브러리 패키지로서 가장 많이 사용되는 데이타 시각화(Data Visualization) 패키지



- 기초

  - 그래프 선언과 출력

    - 그래프 선언 후 show()를 사용하여 그래프 출력

    ```python
    from matplotlib import pyplot as plt
     
    # 처음에 넣는 리스트가 x축이 되고, 두 번째로 넣는 리스트가 y축이 된다.
    plt.plot(["a","b","c"], [100,120,90])
    # show()를 사용하여 출력
    plt.show()
    
    plt.plot([1,2,3], ["A","B","C"])
    plt.show()
    ```

    

  - x,y축 레이블과 그래프의 제목 붙이기.

    ```python
  plt.plot(["a","b","c"], [48,67,58])
    plt.xlabel('Participant')
    plt.ylabel('Weight')
    plt.title('Participant Weigth')
    plt.show()
    ```
  
    

  - 범례 추가

    ```python
  plt.plot(["a","b","c"], [48,67,58])
    plt.plot(["a","b","c"], [52,68,68])
    plt.xlabel('Participant')
    plt.ylabel('Weight')
    plt.title('Participant Weigth')
    plt.legend(['Before', 'After'])
    plt.show()
    ```
  
    

  - DataFrame 사용

    - 아래와 같이 pandas의 dataframe 자료형을 사용하여 표현할 수 있다.

    ```python
  from matplotlib import pyplot as plt
    import pandas as pd
    
    df = pd.DataFrame({'Before': [48,67,58],'After': [52,67,68]},
                        index=["a","b","c"]
                        )
    plt.plot(df)
    plt.show()
    ```
  
    

  - 다른 형태의 그래프

    - 위에서 살펴본 직선 이외에도 아래와 같이 막대 그래프로 표현할 수 있다.

    ```python
  plt.bar(["a","b","c"], [48,67,58],width=0.5,color="blue")
    plt.xlabel('Participant')
    plt.ylabel('Weight')
    plt.title('Participant Weigth')
    plt.show()
    
    #DataFrame 자료형을 통해 여러개의 막대를 표현할 수 있다.
    ```
  
    







# 추천 시스템

> https://www.youtube.com/watch?v=_YndKkun2Sw 참고

## Collaborative filtering

- 대표적인 추천 알고리즘



### User based Collaborative filtering

- 과정

  - 어떤 유저들이 유사한지를 판단한다.
  - 어떤 유저가 어떤 영화를 고평가 했다면 1, 고평가하지 않았다면 0을 줘서 아래 표와 같이 vector로 표현한다.

  |      | 어벤져스 | 존윅 | 인터스텔라 | 어바웃 타임 | 러브레터 |
  | ---- | -------- | ---- | ---------- | ----------- | -------- |
  | A    | 1        | 1    | 1          | 0           | 0        |
  | B    | 0        | 0    | 0          | 1           | 1        |
  | C    | 1        | 1    | 0          | 0           | 0        |
  | D    | 0        | 0    | 0          | 0           | 1        |

  - 유저들 사이의 유사성을 계산한다.
    - 계산 방법 중 하나인 `Cosine similarity`로 A,C의 유사도를 계산하면 다음과 같다.
    - A,C 둘 다 고평가한 영화는 2개이므로 분자에는 2가 간다.
    - Cosine similarity = 2/sqrt(3)*sqrt(2)=0.81
    - 마찬가지 방식으로 B와 C, D와 C의 유사도를 계산하면 둘 다 0이 나온다.
    - 따라서 A가 C와 가장 유사도가 높은 유저라고 할 수 있다.
  - 유사도에 기반해서 다른 유저에게 영화를 추천해준다.
    - C 유저는 A 유저와 유사도가 가장 높으므로 A 유저가 고평가했지만 C 유저는 보지 않은 인터스텔라를 C에게 추천해준다.



### Item based Collaborative filtering

- 과정
  - User based Collaborative filtering과 마찬가지로 유저 정보와 영화 정보를 vector화 해서 표현한다.

    |            | A    | B    | C    | D    |
    | ---------- | ---- | ---- | ---- | ---- |
    | 어벤져스   | 1    | 0    | 1    | 0    |
    | 존윅       | 1    | 0    | 1    | 0    |
    | 인터스텔라 | 1    | 0    | 0    | 0    |
    | 어바웃타임 | 0    | 1    | 0    | 0    |
    | 러브레터   | 0    | 1    | 0    | 1    |
  
  - 영화의 유사성을 계산한다.
    - 역시  `Cosine similarity`로 어바웃 타임과 러브레터의 유사도를 계산하면 다음과 같다.
    - 러브레터는 B와 C에게 높은 평가를 받았다.
    - 어바웃 타임은 B에게만 높은 평가를 받았다.
    - 이 때  `Cosine similarity`로 어바웃 타임과 러브레터의 유사도를 비교해보면 0.71이 나온다.
    - B는 어벤져스, 존윅, 인터스텔라에는 높은 평가를 하지 않았다.
    - 마찬가지 방식으로 러브레터와 어번제스, 존윅 , 인터스텔라의 유사도를 계산하면 모두 0이 나온다.
    - 따라서 어바웃 타임이 러브레터와 가장 유사도가 높은 영화라고 할 수 있다.
  - 영화의 유사도에 기반해서 D에게 어바웃 타임을 추천해준다.
    
    - D가 높게 평가한 러브레터와 유사도가 가장 높지만 아직 D가 보지 않은 어바웃 타임을 추천해준다.





## Content based filtering

- Collaborative filtering의 경우 `cold start problem`이 존재
  - cold start problem: Collaborative filtering은 모두 유저의 평가를 기반으로 추천이 이루어지는데 새로운 영화가 나온 경우 해당 영화에 대한 유저의 평가가 존재하지 않으므로 해당 영화는 추천 할 수 없다. 이와 같이 새롭게 출시된 제품의 평가가 존재하지 않아 새로운 제품의 추천이 이루어지지 않는 문제를 cold start problem라고 부른다. 
  - Content based filtering는 cold start problem가 발생하지 않는다.



- 각 영화별로 특성을 정의한다.

  - 각 영화가 특정 특성을 지니고 있으면 1, 없으면 0으로 표시하여 vector화 한다.

  |            | SF   | 로맨스 | 영국인 배우 | 액션 | 크리스토퍼 놀란 감독 |
  | ---------- | ---- | ------ | ----------- | ---- | -------------------- |
  | 어벤져스   | 1    | 0      | 1           | 1    | 0                    |
  | 존윅       | 0    | 0      | 1           | 1    | 0                    |
  | 인터스텔라 | 1    | 0      | 0           | 0    | 1                    |
  | 어바웃타임 | 0    | 1      | 1           | 0    | 0                    |
  | 러브레터   | 0    | 1      | 0           | 0    | 0                    |

  - 이후 기존 영화는 Collaborative filtering과 같이 특성을 기반으로 유사성을 판단하여 유저에게 추천을 해준다.
    - 예를 들어 A는 어벤져스에 고평가를 했다고 했을 때
    - 어벤져스와 영국인 배우, 액션이라는 공통점을 가진 존윅을 추천해준다.
  - 새로 개봉한 영화의 경우도 마찬가지로 새로 개봉한 영화의 특성을 정의하고 이를 백터화 하여 기존 영화들과의 유사성을 판단하여 추천해준다.
    - 예를 들어 A는 어벤져스에 고평가를 했다고 했을 때
    - SF 장르에, 영국인 배우가 출연하는 마션이라는 영화가 개봉을 했다면, 마션은 A가 고평가한 어벤져스와 특성을 기반으로 계산한 유사도가 높을 것이므로 A에게 마션을 추천해준다.



# 통계

- Linear Regression(선형 회귀): 종속변수 y와 한 개 이상의 독립변수 x와의 선형 상관 관계를 모델링 하는 회귀 분석 기법이다.
- Gradient descent
- 예측 과정
  - 임의 값 weight, bias 생성
  - error 값들을 구한다
  - MSE(mean square error)의 미분 결과*learning_rate를 구한다.
  - 3번 결과 값을 weight, bias에 반영한다.
  - MSE(Cost,Loss)가 최소값에 가까워 질 때까지 2~4번을 반복한다.
  - 최적의 weight, bias를 가지고 predict 한다. 