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
# def A_or_B(gender):
#     if gender=="male":
#         return "A"
#     else:
#         return "B"
# df['some2']=df['gender'].apply(A_or_B)
# print(df)


#열 전체 수정
df['some']=111
# print(df)

#함수를 통해 열 수정
def A_or_B(age):
    if age>24:
        return "A"
    else:
        return "B"
df.some=df.age.apply(A_or_B)
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


#행 수정
# print(df)
# df.loc[3]=['Cha',22,'male',60]
# print(df)



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
    ['Kim',23,71,178,'male','psy'],
]
col_name=['name','age','weight','height','gender','major']
df=pd.DataFrame(data,columns=col_name)

groupby_major = df.groupby('major')
# print(groupby_major)
# print(groupby_major.groups)

#활용
# for n, g in groupby_major:
#     print(n+":"+str(len(g))+'명')
#     print(g)
#     print()

#각 전공별 인원수를 DataFrame으로 만들기
dic = {
    'count':groupby_major.size()
    }
df_major_cnt = pd.DataFrame(dic)
# print(df_major_cnt)

#위에서 major가 각각의 행을 형성하고 있는데 이를 column으로 옮기려면 아래와 같이 reset_index()를 해주면 된다.
df_major_cnt = pd.DataFrame(dic).reset_index()
# print(df_major_cnt)


#중복 처리
data = [
    ['Kim',23,71,178,'male','psy'],
    ['Lee',23,71,178,'male','psy'],  #하나만 다르다.
    ['Kim',23,71,178,'male','psy'],  #완전히 중복.
]
col_name=['name','age','weight','height','gender','major']
df=pd.DataFrame(data,columns=col_name)

# print(df.duplicated())

# print(df.drop_duplicates())

# print(df.duplicated(['name']))

# print("keep='first'")
# print(df.drop_duplicates(['name'],keep='first'))
# print("keep='last'")
# print(df.drop_duplicates(['name'],keep='last'))




#NaN 값을 찾아서 다른 값으로 변경하기
data = [
    ['Kim',23,71,178,'male','psy'],
    ['Park',27,48,165,'female','phil'],
    ['Song',29,48,168,'female','eco'],
    ['Lee',23,71,None,'male',None],
    ['Lee',23,52,None,'female',None],
]
col_name=['name','age','weight','height','gender','major']
df=pd.DataFrame(data,columns=col_name)
# print(df)
# print()
# print(".shape")
# print(df.shape)
# print()
# print(".info()")
# print(df.info())
# print()
# print(".isna()")
# print(df.isna())
# print()
# print(".isnull()")
# print(df.isnull())


#변경하기
# df.height = df.height.fillna(0)
# df.major.fillna(0)
# print(df)

# df['height'].fillna(0,inplace=True)
# df['major'].fillna(0,inplace=True)
# print(df)

# df['height'].fillna(df.groupby('gender')['height'].transform('median'),inplace=True)
# print(df)

def decide_major(weight):
    if weight>=60:
        return "eco"
    else:
        return "psy"
df.major.fillna(df.weight.apply(decide_major),inplace=True)
# print(df)

data = [
    ['Kim',23,71,178,'male','psy'],
    ['Park',27,48,165,'female','phil'],
    ['Song',29,48,168,'female','eco'],
    ['Lee',23,71,180,'male','psy'],
    ['Lee',23,52,170,'female','eco'],
]
col_name=['name','age','weight','height','gender','major']
df=pd.DataFrame(data,columns=col_name)

def get_birth(age,current_year):
    return current_year-age+1
df['birth']=df['age'].apply(get_birth,current_year=2020)
# print(df)

def cal_bmi(row):
    return round(row.weight/(row.height**2)*10000,2)

df['BMI']=df.apply(cal_bmi,axis=1)
# print(df)

data = [
    ['1997-02-04'],
    ['1992-07-18'],
]
col_name=['date']
df=pd.DataFrame(data,columns=col_name)


def year(date):
    return date.split('-')[0]

df['year']=df['date'].map(year)
# print(df)

df.year = df.year.map({'1997':197, '1992':192})
# print(df)

def change_all(df):
    return 0

df = df.applymap(change_all)
# print(df)


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

# print(df.major.unique())
# print(type(df.major.unique()))

# print(df.major.value_counts)


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

# result = pd.concat([df1,df2])
# print(result)
# print()
# result = pd.concat([df1,df2],ignore_index=True)
# print(result)

result = df1.append(df2, ignore_index=True)
# print(result)


data3 = {
    'major':['psy','eco','phil'],
    'gender':['male','male','female'],
}
df3 = pd.DataFrame(data3)


result = pd.concat([df1,df3],axis=1)
# print(result)

result = df1.append(df3,axis=1)
print(result)