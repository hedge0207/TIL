import pandas as pd
 
# Series 생성
# 기본 생성
data = [1,3,5,7,9]
s = pd.Series(data)
# print(s)

# 인덱스를 직접 설정
s2 = pd.Series([2,4,6,8],index=['a','b','c','d'])
# print(s2)

# 딕셔너리를 활용
obj = {'a':1,'b':2,'c':3,'d':4}
s3 = pd.Series(obj)
# print(s3)


#Series의 메소드
# print(s.index)
# print(s.values)
# print(s.dtype)


#Series와 Series의 인덱스, 밸류에 이름 넣기
s.name='이름'
s.index.name="인덱스"
# print(s)




#DataFrame
#생성
#방법1. 딕셔너리 사용
data = {
    'name':['Kim','Lee','Park'],
    'age':[23,25,27],
}
df = pd.DataFrame(data)
# print(df)

#방법1-2. 인덱스와 컬럼을 함께 설정
data = {
    'name':['Kim','Lee','Park'],
    'age':[23,25,27],
}
df = pd.DataFrame(data,columns=['age','name','weight'],index=['one','two','three'])
# print(df)

#방법2-1. 리스트 사용
data = [
    ['Kim',23],
    ['Lee',25],
    ['Park',27]
]
col_name=['name','age']
df=pd.DataFrame(data,columns=col_name)
# print(df)

data = [
    ['name',['Kim','Lee','Park']],
    ['age',[23,25,27]]
]
df = pd.DataFrame.from_items(data)
# print(df)


#DataFrame의 메소드
#행의 인덱스
# print(df.index)
#열의 인덱스
# print(df.columns)
#값 얻기
# print(df.values)
#sum(): 합계
# print(df['age'].sum())
#mean(): 평균
# print(df['age'].mean())
#min(): 최소
# print(df['age'].min())
#max(): 최대
# print(df['age'].max())
#describe():기본적인 통계치 전부
# print(df.describe())

#행, 열 인덱스의 이름 설정하기
# print('before')
# print(df)
df.index.name='index'
df.columns.name='info'
# print()
# print('after')
# print(df)



#data에 접근
# print(df[0:2])
# print(df.loc[[0,2]])
# print(df.iloc[0:2,1:2])
# print(df.iloc[1,1])
# print(df.filter(like='m',axis=1))
# print(df.filter(regex='e$',axis=1))
# print(df.iloc[:,['age']])
# print(df['age'])
# print(df.age)
# print(df.filter(items=['age']))
# print(df)


#loc과 iloc의 차이

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

# print('loc output')
# print(df.loc[0:3,1:3])
# print()
# print('iloc output')
# print(df.iloc[0:3,1:3])

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
# print('loc output')
# print(df.loc['one':'three','age':'weight'])
# print()
# print('iloc output')
# print(df.iloc[0:3,1:3])

#boolean indexing
# print(df[df.age>=25])
# print(df[df['age']>=25])
# print(df.age>=25)
# print(df.name=='Kim')
# print(df.query('age>=25'))

#새로운 값도 대입 가능
# df.loc[df['age']>25,'name']='Jeong'

#boolean indexing을 활용하여 조건에 맞지 않는 값을 삭제
# print(df)
# df = df[df['age']>=25]
# print(df)



#재선언
data = [
    ['Kim',23],
    ['Lee',25],
    ['Park',27]
]
col_name=['name','age']
df=pd.DataFrame(data,columns=col_name)


# #열 추가
df['gender']='male'
# # print(df)
df['gender']=['male','female','male']
# # print(df)

# #Series를 추가
s = pd.Series([170,180],index=[0,2])
df['some']=s
# # print(df)

# #계산 후 열 추가
df['lifetime']=df['age']+70
# # print(df)

#함수를 통해 열 추가
def A_or_B(age):
    print(age)
    if age>24:
        return "A"
    else:
        return "B"
# df.some=df.age.apply(A_or_B)
# print(df)


#열 삭제
del df['some']
# print(df)
# print(df)

# df = df.drop('age',axis=1)
# print(df)

# df.drop('gender',axis=1, inplace=True)
# print(df)

# #행 추가
df.loc[3]=['Choi',21,'female',88]
df2 = pd.DataFrame([['Jeong',22,'male',89]],columns=['name','age','gender','lifetime'])

# print(df.append(df2))




# #행 삭제
# # print(df.drop([2,3]))
# # print(df)

# df = df.drop([1])
# # print(df)

# df.drop(0,inplace=True)
# # print(df)





# 그룹화
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
print(groupby_major.groups)