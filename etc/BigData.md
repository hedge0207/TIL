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
  - 생성

  ```python
  import pandas as pd
   
  # 방법1.
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
      
      
  #방법2. 인덱스를 직접 설정
  s2 = pd.Series([2,4,6,8],index=['a','b','c','d'])
  print(s2)
  
  #out
  a    2
  b    4
  c    6
  d    8
  dtype: int64
      
  
  #방법3. 딕셔너리를 사용
  obj = {'a':1,'b':2,'c':3,'d':4}
  s3 = pd.Series(obj)
  print(s3)
  
  #out
  a    1
  b    2
  c    3
  d    4
  dtype: int64
  ```

  - Series의 메소드

  ```python
  #Series의 값만 확인하기
  print(s.values)
  #Series의 인덱스만 확인
  print(s.index)
  #Series의 자료형 확인
  print(s.dtype)
  
  
  #out
  [1 3 5 7 9]
  RangeIndex(start=0, stop=5, step=1)
  int64
  ```

  - Series, index의 이름을 설정하는 것도 가능하다(value에 이름 넣는 것은 불가능).

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
  
  #방법1-1. python의 dictionary를 사용
  data = {
      'name':['Kim','Lee','Park'],
      'age':[23,25,27],
  }
   
  df = pd.DataFrame(data)
  print(df)
  
  #out
     name  age
  0   Kim   23
  1   Lee   25
  2  Park   27
  
  
  #방법1-2. 인덱스와 컬럼을 함께 설정
  data = {
      'name':['Kim','Lee','Park'],
      'age':[23,25,27],
  }
  df = pd.DataFrame(data,columns=['age','name'],index=['one','two','three'])
  print(df)
  
  #out
  #아래에서 확인 가능한 것 처럼 data의 순서와 DataFrame을 정의할 때의 columns의 순서가 달라도 key값을 알아서 찾아서 정의해준다. 단, data에 포함되어 있지 않았던 값(예시의 경우 weigth)은 NaN으로 나타나게 된다.
  #단, index의 경우 data의 개수와 맞지 않으면 에러가 발생하게 된다.
         age  name weight
  one     23   Kim    NaN
  two     25   Lee    NaN
  three   27  Park    NaN
  
  
  #방법2-1. python의 list를 사용
  data = [
      ['Kim',23],
      ['Lee',25],
      ['Park',27]
  ]
  col_name=['name','age']
  df=pd.DataFrame(data,columns=col_name)
  print(df)
  
  #out
     name  age
  0   Kim   23
  1   Lee   25
  2  Park   27
  
  
  #방법2-2. 위 방법을 한 번에 하는 방법
  data = [
      ['name',['Kim','Lee','Park']],
      ['age',[23,25,27]]
  ]
  df = pd.DataFrame.from_items(data)
  print(df)
  
  #out
     name  age
  0   Kim   23
  1   Lee   25
  2  Park   27
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
  Index(['name', 'age'], dtype='object')
  [['Kim' 23]
   ['Lee' 25]
   ['Park' 27]]
  
  
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
  75
  25.0
  23
  27
          age
  count   3.0
  mean   25.0
  std     2.0
  min    23.0
  25%    24.0
  50%    25.0
  75%    26.0
  max    27.0
  ```

  

  - 행, 열 인덱스의 이름 설정하기

  ```python
  print('before')
  print(df)
  df.index.name='index'
  df.columns.name='info'
  print()
  print('after')
  print(df)
  
  #out
  before
     name  age
  0   Kim   23
  1   Lee   25
  2  Park   27
  
  after
  info   name  age
  index
  0       Kim   23
  1       Lee   25
  2      Park   27
  ```

  

  - data에 접근

  ```python
  #행에 접근: 행 인덱싱을 통해 접근
  print(df[0:2]) #0번째 부터 2번째 앞까지 가져온다.
  
  
  #out
  info  name  age
  index
  0      Kim   23
  1      Lee   25
  
  
  
  # 열에 접근1. 인덱싱
  print(df['age'])   
  
  # 열에 접근2. 속성
  print(df.age)      
  
  # 열에 접근3-1.filter를 사용할 수도 있다. sql문과 동일하게 like, regex 등의 문법을 사용 가능하다.
  print(df.filter(items=['age']))
  
  
  #out
  index
  0    23
  1    25
  2    27
  Name: age, dtype: int64
          
  index
  0    23
  1    25
  2    27
  Name: age, dtype: int64
  
  #위 두 방식과 결과가 다르다.
  info   age
  index
  0       23
  1       25
  2       27
  
  #열에 접근 3-2. filter의 like,regex 활용
  #axis=1은 열을 필터링 하겠다는 뜻이다. 따라서 아래 코드는 열 중에서 m이 포함된 열을 찾는 것이다.
  print(df.filter(like='m',axis=1))
  #아래 코드는 열 중에서 e로 끝나는 열을 찾는 것이다.
  print(df.filter(regex='e$',axis=1))
  
  #out
  info   name
  index
  0       Kim
  1       Lee
  2      Park
  info   name  age
  index
  0       Kim   23
  1       Lee   25
  2      Park   27
  
  
  
  #boolean indexing과 함께 사용
  print(df.loc[df['gender']=='male',['year','height']])
  
  #out
           year  height
  two    2017.0    1.73
  three  2018.0    1.83
  ```

  

  - loc과 iloc의 차이
    - 공통점: 둘 다 첫 번째 인자로 행을 두 번째 인자로 열을 받는다.
    - 차이점: loc은 label(index명, column 명)을 통해서 값을 찾지만 iloc은 interger position을 통해서 값을 찾는다.

  ```python
  #인덱스, 컬럼이 숫자일 경우
  data = [
      ['Kim',23,71,178],
      ['Lee',25,68,175],
      ['Park',27,48,165],
      ['Choi',22,57,168],
      ['Jeong',29,77,188],
  ]
  col_name=[1,2,3,4]
  df=pd.DataFrame(data,columns=col_name)
  # print('loc output')
  # print(df.loc['one':'three','age':'weight'])
  # print()
  # print('iloc output')
  # print(df.iloc[0:3,1:3])
  
  print('loc output')
  print(df.loc[0:3,1:3])  #인덱스의 이름이 0인 것부터 3인 것 까지, 컬럼의 이름이 1인것 부터 3인것 까지
  print()
  print('iloc output')
  print(df.iloc[0:3,1:3]) #0 번째 인덱스 부터 2번째 인덱스 까지, 1번째 컬럼부터 2번째 컬럼 까지, 
  
  #out
  loc output
        1   2   3
  0   Kim  23  71
  1   Lee  25  68
  2  Park  27  48
  3  Choi  22  57
  
  iloc output
      2   3
  0  23  71
  1  25  68
  2  27  48
  
  
  
  #인덱스, 컬럼이 숫자가 아닐 경우
  data = [
      ['Kim',23,71,178],
      ['Lee',25,68,175],
      ['Park',27,48,165],
      ['Choi',22,57,168],
      ['Jeong',29,77,188],
  ]
  col_name=['name','age','weight','height']
  df=pd.DataFrame(data,columns=col_name, index = ['one','two','three','four','five'])
  
  print('loc output')
  print(df.loc['one':'three','age':'weight'])
  print()
  print('iloc output')
  print(df.iloc[0:3,1:3])
  
  #out
  loc output
         age  weight
  one     23      71
  two     25      68
  three   27      48
  
  iloc output
         age  weight
  one     23      71
  two     25      68
  three   27      48
  ```

  

  

  - boolean indexing:  특정 조건의 데이터만 필터링
    - 어떤 방식으로 접근했는 가에 따라 결과 값이 다르다.

  ```python
  #인덱스로 접근
  print(df[df['age']>=25])
  print(df[df.age>=25])
  #속성으로 접근
  print(df.age>=25)
  #sql문 사용
  print(df.query('age>=25'))
  
  #out
  #일치하는 행만 반환
  info   name  age
  index
  1       Lee   25
  2      Park   27
  info   name  age
  index
  1       Lee   25
  2      Park   27
  
  #각 행별 조건에 부합하는지 여부를 boolean 값으로 반환
  index
  0    False
  1     True
  2     True
  Name: age, dtype: bool
          
  #일치하는 행만 반환
  info   name  age
  index
  1       Lee   25
  2      Park   27
  
  
  #새로운 값도 대입 가능, 새로운 값을 추가하는 것은 불가능
  df.loc[df['age']>25,'name']='Jeong'
  print(df)
  
  info    name  age
  index
  0        Kim   23
  1        Lee   25
  2      Jeong   27
  ```

  

  - 열 추가

  ```python
  df['gender']='male'
  print(df)
  
  df['gender']=['male','female','male']
  print(df)
  
  
  #out
  info   name  age gender
  index
  0       Kim   23   male
  1       Lee   25   male
  2      Park   27   male
  info   name  age  gender
  index
  0       Kim   23    male
  1       Lee   25  female
  2      Park   27    male
  
  
  #Series를 추가할 수도 있다.
  s = pd.Series([170,180],index=[0,2])
  df['some']=s
  print(df)
  
  
  #out
  #위에서 index를 지정한 0, 2번 행은 각기 some열에 값이 들어갔으나 지정해주지 않은 1번 행은 값이 들어가지 않았다. 
  info   name  age  gender   some
  index
  0       Kim   23    male  170.0
  1       Lee   25  female    NaN  
  2      Park   27    male  180.0
  
  
  #계산후 열 추가
  df['lifetime']=df['age']+70
  print(df)
  
  #out
  info   name  age  gender   some  lifetime
  index
  0       Kim   23    male  170.0        93
  1       Lee   25  female    NaN        95
  2      Park   27    male  180.0        97
  
  
  
  #함수를 사용하여 열 추가
  def A_or_B(gender):
      if gender=="male":
          return "A"
      else:
          return "B"
  df['some2']=df['gender'].apply(A_or_B)
  #df.some2=df['gender'].apply(A_or_B) -> 이 코드로는 수정은 돼도 추가는 안 된다.
  print(df)
  
  #out
     name  age  gender   some  lifetime some2
  0   Kim   23    male  170.0        93     A
  1   Lee   25  female    NaN        95     B
  2  Park   27    male  180.0        97     A
  ```

  - 열 수정

  ```python
  #열 전체 수정, 열 추가와 같다.
  df['some']=111
  print(df)
  
  #out
     name  age  gender  some  lifetime
  0   Kim   23    male   111        93
  1   Lee   25  female   111        95
  2  Park   27    male   111        97
  
  
  # 함수를 사용하여 열 수정, apply 사용, 열을 추가 할 때도 사용 가능.
  def A_or_B(age):
      print(age)
      if age>24:
          return "A"
      else:
          return "B"
  df.some=df.age.apply(A_or_B)
  #위 함수에서 바꿀 열의 값은 some이고 함수에 인자로 넘어가게 되는 값은 age이다.
  print(df)
  
  #out
  23
  25
  27
     name  age  gender some  lifetime
  0   Kim   23    male    B        93
  1   Lee   25  female    A        95
  2  Park   27    male    A        97
  ```

  

  - 열 삭제

  ```python
  #방법1. del을 사용
  del df['some']
  print(df)
  
  #out
  info   name  age  gender  lifetime
  index
  0       Kim   23    male        93
  1       Lee   25  female        95
  2      Park   27    male        97
  
  
  #방법2-1. drop을 사용
  #drop은 기본적으로 행을 삭제할 때 사용하는 메소드이므로 열을 삭제하고자 한다면 axis=1을 입력하여 열을 삭제하려 한다는 것을 알려줘야 한다.
  df = df.drop('age',axis=1)
  print(df)
  
  #out
     name  gender  lifetime
  0   Kim    male        93
  1   Lee  female        95
  2  Park    male        97
  
  
  #방법2-2. 행 삭제와 마찬가지로 inplace 설정을 True로 하면 재할당 없이 바로 적용시킬 수 있다.
  df.drop('gender',axis=1, inplace=True)
  print(df)
  #out
     name  lifetime
  0   Kim        93
  1   Lee        95
  2  Park        97
  ```

  

  - 행 추가

  ```python
  #방법1. loc을 사용
  df.loc[3]=['Choi',21,'female',88]  #이 때 한 열의 값이라도 빠지면 에러가 발생
  print(df)
  
  #out
  info   name  age  gender  lifetime
  index
  0       Kim   23    male        93
  1       Lee   25  female        95
  2      Park   27    male        97
  3      Choi   21  female        88
  
  
  #방법2. append 를 사용
  df2 = pd.DataFrame([['Jeong',22,'male',89]],columns=['name','age','gender','lifetime'])
  
  #값이 실제로 바뀌진 않는다.
  print(df.append(df2))
  #ignore_index를 해주는 이유는 df2 역시 index가 0부터 시작될 것이므로 합치면 인덱스가 중복되게 되는데 ignore_index를 하면 합쳐지는 쪽의 인덱스가 합치는 쪽의 인덱스에 맞게 수정되어 들어가게 된다.
  print(df.append(df2,ignore_index=True))
  
  #out
  #인덱스 중복
      name  age  gender  lifetime
  0    Kim   23    male        93
  1    Lee   25  female        95
  2   Park   27    male        97
  3   Choi   21  female        88
  0  Jeong   22    male        89
  
  #gnore_index를 설정하여 인덱스가 중복이 일어나지 않았다.
      name  age  gender  lifetime
  0    Kim   23    male        93
  1    Lee   25  female        95
  2   Park   27    male        97
  3   Choi   21  female        88
  4  Jeong   22    male        89
  ```

  

  - 행 수정

  ```python
  # 행 추가와 마찬가지로 작성하면 되며 기존 행에 덮어씌워진다.
  print("before")
  print(df)
  print()
  
  df.loc[3]=['Cha',22,'male',60]
  print("after")
  print(df)
  
  
  #out
  before
     name  age  gender  lifetime
  0   Kim   23    male        93
  1   Lee   25  female        95
  2  Park   27    male        97
  3  Choi   21  female        88
  
  after
     name  age  gender  lifetime
  0   Kim   23    male        93
  1   Lee   25  female        95
  2  Park   27    male        97
  3   Cha   22    male        60
  ```

  

  

  - 행 삭제

  ```python
  #실제로 행이 삭제되지는 않는다.
  print(df.drop([2,3]))
  print()
  print(df)
  
  #out
  info  name  age  gender  lifetime
  index
  0      Kim   23    male        93
  1      Lee   25  female        95
  
  info   name  age  gender  lifetime
  index
  0       Kim   23    male        93
  1       Lee   25  female        95
  2      Park   27    male        97
  3      Choi   21  female        88
  
  
  # 삭제 1-1.drop한 DataFrame을 변수에 할당
  df = df.drop([1])
  print(df)
  
  #out
  info   name  age  gender  lifetime
  index
  0       Kim   23    male        93
  2      Park   27    male        97
  3      Choi   21  female        88
  
  
  # 삭제 1-2.drop할 때 inplace 설정을 True로
  df.drop(0,inplace=True)
  print(df)
  
  #out
  info   name  age  gender  lifetime
  index
  2      Park   27    male        97
  3      Choi   21  female        88
  
  
  #삭제 2. boolean indexing을 활용하여 조건에 맞지 않는 값을 삭제
  df = df[df.age>=25]
  print(df)
  
  #out
  info   name  age
  index
  1       Lee   25
  2      Park   27
  ```

  

- Panel
  
  - 3차원 자료 구조로 Axis 0(items), Axis 1(major_axis), Axis 2(minor_axis) 등 3개의 축을 가지고 있는데 Axis 0은 그 한 요소가 DataFrame에 해당되며, Axis 1은 DataFrame의 행에 해당되고, Axis 2는 DataFrame의 열에 해당된다.



## 데이터 읽고 쓰기

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
  
    
  
  

## 데이터 처리

- 그룹화(`groupby`)

```python
data = [
    ['Kim',23,71,178,'male','psy'],
    ['Lee',25,68,175,'female','psy'],
    ['Park',27,48,165,'female','phil'],
    ['Choi',22,57,168,'male','phil'],
    ['Jeong',29,77,188,'male','psy'],
    ['Han',34,47,158,'female','eco'],
    ['An',18,57,172,'male','phil'],
    ['Shin',37,71,178,'female','eco'],
    ['Song',29,48,168,'female','eco'],
]
col_name=['name','age','weight','height','gender','major']
df=pd.DataFrame(data,columns=col_name)

groupby_major = df.groupby('major')
print(groupby_major)
print()
print(groupby_major.groups)

#out
<pandas.core.groupby.generic.DataFrameGroupBy object at 0x00000297D560F780>

{'eco': Int64Index([5, 7, 8], dtype='int64'), 'phil': Int64Index([2, 3, 6], dtype='int64'), 'psy': Int64Index([0, 1, 4], dtype='int64')}


#활용
for n, g in groupby_major:
    print(n+":"+str(len(g))+'명')
    print(g)
    print()

#out
eco:3명
   name  age  weight  height  gender major
5   Han   34      47     158  female   eco
7  Shin   37      71     178  female   eco
8  Song   29      48     168  female   eco

phil:3명
   name  age  weight  height  gender major
2  Park   27      48     165  female  phil
3  Choi   22      57     168    male  phil
6    An   18      57     172    male  phil

psy:3명
    name  age  weight  height  gender major
0    Kim   23      71     178    male   psy
1    Lee   25      68     175  female   psy
4  Jeong   29      77     188    male   psy


#각 전공별 인원수를 DataFrame으로 만들기
dic = {
    'count':groupby_major.size()
    }
df_major_cnt = pd.DataFrame(dic)
print(df_major_cnt)

#out
       count
major
eco        3
phil       3
psy        3

# .reset_index()
#위에서 major가 각각의 행을 형성하고 있는데 이를 column으로 옮기려면 아래와 같이 reset_index()를 해주면 된다.
df_major_cnt = pd.DataFrame(dic).reset_index()
print(df_major_cnt)

#out
  major  count
0   eco      3
1  phil      3
2   psy      3
```





- 중복 데이터 삭제
  - `.duplicated()`: 중복 데이터가 있는지 확인
  - `.drop_duplicates()`

```python
data = [
    ['Kim',23,71,178,'male','psy'],
    ['Lee',23,71,178,'male','psy'],  #하나만 다르다.
    ['Kim',23,71,178,'male','psy'],  #완전히 중복.
]
col_name=['name','age','weight','height','gender','major']
df=pd.DataFrame(data,columns=col_name)

#중복 데이터가 있는지 확인
print(df.duplicated())

#out
0    False
1    False
2     True  #완전히 중복이어야 True를 반환
dtype: bool
    

#중복 데이터 삭제
print(df.drop_duplicates())  #실제로 삭제되지는 않는다. 실제로 삭제하려면 재할당 필요

#out
  name  age  weight  height gender major
0  Kim   23      71     178   male   psy
1  Kim   23      71     178   male   eco


#특정 열의 값이 중복되는 행을 확인
print(df.duplicated(['name']))

#out
0    False
1    False
2     True
dtype: bool
    
    
    
#특정 열의 값이 중복되는 행을 삭제
#첫 번째 인자로 중복을 확인해 삭제할 열을, 두 번째 인자로 중복된 행 중 어떤 행을 살릴 것인지를 keep을 통해 설정해준다. keep값을 주지 않을 경우  default는 first다.
print("keep='first'")
print(df.drop_duplicates(['name'],keep='first'))
print("keep='last'")
print(df.drop_duplicates(['name'],keep='last'))

#out
keep='first'
  name  age  weight  height gender major
0  Kim   23      71     178   male   psy
1  Lee   23      71     178   male   psy
keep='last'
  name  age  weight  height gender major
1  Lee   23      71     178   male   psy
2  Kim   23      71     178   male   psy
```





- NaN을 찾아서 원하는 값으로 변경하기

  - Pandas에서는 숫자가 올 열에 `None`을 넣으면 `NaN`이 들어가고 문자가 올 열에 넣으면 그대로 `None`이 들어간다.
  - `.shape`: DataFrame의 크기를 확인하는 메소드, `(행의 개수, 열의 개수)` 형태로 결과가 출력된다.
  - `.info()`: DataFrame의 정보를 확인하는 메소드
  - `.isna()`, `.isnull()`: `None` 값을 확인하는 메소드, 둘의 기능은 같다.
    - pandas의 소스 코드를 보면 `isnull=isna` 부분을 확인할 수 있다. 즉, `isnull`은 `isna`의 별칭이다.

  ```python
  data = [
      ['Kim',23,71,178,'male','psy'],
      ['Park',27,48,165,'female','phil'],
      ['Song',29,48,168,'female','eco'],
      ['Lee',23,71,None,'male',None],
      ['Lee',23,52,None,'female',None],
  ]
  col_name=['name','age','weight','height','gender','major']
  df=pd.DataFrame(data,columns=col_name)
  print(df)
  print()
  print(".shape")
  print(df.shape)
  print()
  print(".info()")
  print(df.info())
  print()
  print(".isna()")
  print(df.isna())
  print()
  print(".isnull()")
  print(df.isnull())
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71     NaN    male  None
  4   Lee   23      52     NaN  female  None
  
  .shape
  (5, 6)
  
  .info()
  <class 'pandas.core.frame.DataFrame'>
  RangeIndex: 5 entries, 0 to 4
  Data columns (total 6 columns):
  name      5 non-null object
  age       5 non-null int64
  weight    5 non-null int64    #5개의 행 중 5개가 null 값이 아님
  height    3 non-null float64  #5개의 행 중 3개가 null 값이 아님
  gender    5 non-null object
  major     3 non-null object
  dtypes: float64(1), int64(2), object(3)
  memory usage: 368.0+ bytes
  None
  
  .isna()
      name    age  weight  height  gender  major
  0  False  False   False   False   False  False
  1  False  False   False   False   False  False
  2  False  False   False   False   False  False
  3  False  False   False    True   False   True
  4  False  False   False    True   False   True
  
  .isnull()
      name    age  weight  height  gender  major
  0  False  False   False   False   False  False
  1  False  False   False   False   False  False
  2  False  False   False   False   False  False
  3  False  False   False    True   False   True
  4  False  False   False    True   False   True
  ```

  

  - `.fillna()`: `Nan`을 괄호 안에 있는 값으로 변경

  ```python
  #방법1. 재할당
  df.height = df.height.fillna(0)
  df.major = df.major.fillna(0)   #다른 열에 들어 있는 자료형과 달라도 변경이 가능하다.
  print(df)
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71     0.0    male     0
  4   Lee   23      52     0.0  female     0
  
  
  
  #방법2. inplace 사용으로 재할당 없이
  df['height'].fillna(0,inplace=True)
  df['major'].fillna(0,inplace=True)
  print(df)
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71     0.0    male     0
  4   Lee   23      52     0.0  female     0
  
  
  
  #다른 열의 데이터에 따라 다른 값을 넣고자 할 때
  #null 값이 있어야 fillna를 쓸 수 있으므로 재선언 한 후
  #남자면 height를 남자의 평균으로, 여자면 height를 여자의 평균으로 넣으려 한다면
  # 아래 코드에서 df.groupby('gender')['height'].transform('median')까지가 넣을 값을 결정하는 코드다.
  df['height'].fillna(df.groupby('gender')['height'].transform('median'),inplace=True)
  print(df)
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71   178.0    male  None
  4   Lee   23      52   166.5  female  None
  
  
  
  #몸무게가 60 이상이면 경제학, 미만이면 심리학을 전공으로 넣으려 한다면
  def decide_major(weight):
      if weight>=60:
          return "eco"
      else:
          return "psy"
  df.major.fillna(df.weight.apply(decide_major),inplace=True)
  print(df)
  
  #out
     name  age  weight  height  gender major
  0   Kim   23      71   178.0    male   psy
  1  Park   27      48   165.0  female  phil
  2  Song   29      48   168.0  female   eco
  3   Lee   23      71   178.0    male   eco
  4   Lee   23      52   166.5  female   psy
  ```





- `apply` 심화

  ```python
  #추가 인자 전달(같은 방법으로 복수의 추가 인자를 넘기는 것이 가능)
  def get_birth(age,current_year):
      return current_year-age+1
  
  df['birth']=df['age'].apply(get_birth,current_year=2020)
  print(df)
  
  #out
     name  age  weight  height  gender major  birth
  0   Kim   23      71     178    male   psy   1998
  1  Park   27      48     165  female  phil   1994
  2  Song   29      48     168  female   eco   1992
  3   Lee   23      71     180    male   psy   1998
  4   Lee   23      52     170  female   eco   1998
  
  
  
  #복수의 열을 인자로 넘기는 방법
  def cal_bmi(row):
      return round(row.weight/(row.height**2)*10000,2)
  
  #df를 통째로 인자로 넘기는 코드로 axis=1을 줘서 행을 넘기는 것이다.
  df['BMI']=df.apply(cal_bmi,axis=1)
  print(df)
  
  #out
     name  age  weight  height  gender major  birth    BMI
  0   Kim   23      71     178    male   psy   1998  22.41
  1  Park   27      48     165  female  phil   1994  17.63
  2  Song   29      48     168  female   eco   1992  17.01
  3   Lee   23      71     180    male   psy   1998  21.91
  4   Lee   23      52     170  female   eco   1998  17.99
  
  
  
  #lambda 식을 사용하는 것도 가능하다.
  ```

  



- `map`, `applymap`

  - `.map()`: apply와 사용법이 동일하다. 다만 `map`은 `apply` 와 달리 함수를 사용하지 않고 dictionary로 직접 값을 변경 가능하다.

  ```python
  #apply와 동일한 사용법
  data = [
      ['1997-02-04'],
      ['1992-07-18'],
  ]
  col_name=['date']
  df=pd.DataFrame(data,columns=col_name)
  
  def year(date):
      return date.split('-')[0]
  
  df['year']=df['date'].map(year)
  print(df)
  
  #out
           date  year
  0  1997-02-04  1997
  1  1992-07-18  1992
  
  
  
  #apply와 다른 사용법
  df.year = df.year.map({'1997':197, '1992':192})
  print(df)
  
  #out
           date  year
  0  1997-02-04   197
  1  1992-07-18   192
  ```

  

  - `.applymap()`: DataFrame 내의 모든 값을 일괄적으로 변경시키기 위해 사용

  ```python
  def change_all(df):
      return 0
  
  df = df.applymap(change_all)
  print(df)
  
  #out
     date  year
  0     0     0
  1     0     0
  ```

  



- `unique`, `value_counts`

  - `.unique()`: 컬럼 내의 데이터를 중복되지 않게 뽑을 때 사용

  ```python
  data = [
      ['Kim',23,'male','psy'],
      ['Park',27,'female','phil'],
      ['Song',29,'female','eco'],
      ['Lee',23,'male','psy'],
      ['Lee',23,'female','eco'],
      ['Jeong',23,'female','geo'],
  ]
  col_name=['name','age','gender','major']
  df=pd.DataFrame(data,columns=col_name)
  
  print(df.major.unique())
  print(type(df.major.unique()))
  
  #out
  ['psy' 'phil' 'eco' 'geo']
  <class 'numpy.ndarray'>
  ```

  

  - `.value_counts()`: 각 데이터 별 개수 확인
    - `.value_counts` 처럼 `()`를 붙이지 않고 쓸 경우 완전히 다른 결과를 반환하므로 주의

  ```python
  print(df.major.value_counts())
  
  eco     2
  psy     2
  geo     1
  phil    1
  Name: major, dtype: int64
  ```

  



- 두 개의 DataFrame 합치기

  - `.concat()`: Pandas의 함수로 인자로 합칠 데이터 프레임 2개를 넘긴다.
  - `.append()`: DataFrame의 메소드로 합쳐질 데이터 프레임을 인자로 넘긴다.

  ```python
  # 행으로 합치기
  # 방법1. .concat()사용
  data1 = {
      'name':['Kim','Lee','Park'],
      'age':[23,25,27],
  }
  df1 = pd.DataFrame(data1)
  
  data2 = {
      'name':['Choi','Jeong','An'],
      'age':[31,35,33],
  }
  df2 = pd.DataFrame(data2)
  
  result = pd.concat([df1,df2])
  print(result)
  
  #인덱스를 겹치지 않게 하려면 아래와 같이
  result = pd.concat([df1,df2],ignore_index=True)
  print(result)
  
  #out
      name  age
  0    Kim   23
  1    Lee   25
  2   Park   27
  0   Choi   31
  1  Jeong   35
  2     An   33
  
      name  age
  0    Kim   23
  1    Lee   25
  2   Park   27
  3   Choi   31
  4  Jeong   35
  5     An   33
  
  
  
  #방법2. .append()사용
  result = df1.append(df2, ignore_index=True)
  
  #out
      name  age
  0    Kim   23
  1    Lee   25
  2   Park   27
  3   Choi   31
  4  Jeong   35
  5     An   33
  
  
  
  
  #열로 합치기
  #열로 합칠 때 ingnore_index=True를 주면 열의 이름이 0부터 시작하는 숫자로 변하게 된다.
  data3 = {
      'major':['psy','eco','phil'],
      'gender':['male','male','female'],
  }
  df3 = pd.DataFrame(data3)
  
  #.concat()사용, .append()는 사용 불가
  result = pd.concat([df1,df3],axis=1)
  print(result)
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