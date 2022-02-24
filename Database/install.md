# Tibero 설치 및 Python 연동

> Tibero 서버는 설치되어 있다고 가정

- Linux에서 Tibero와 Python의 연동을 위해서는 아래와 같은 것들이 필요하다.
  - Tibero client
  - unixODBC-devel 리눅스 패키지
  - pyodbc 패키지(python)



- Tibero client 설치

  - tibero 사이트에서 client 바이너리 파일을 다운 받는다.
  - 바이너리 파일의 압축을 푼다.

  ```bash
  $ tar -xvf <압축 파일 명>
  ```

  - profile을 설정한다.

  ```bash
  $ vi ~/.bash_profile
  export TB_HOME=<tibero 압축을 푼 경로>/tibero6
  export TB_SID=tb6
  export PATH=$TB_HOME/bin:$TB_HOME/client/bin:$PATH:
  export LD_LIBRARY_PATH=$TB_HOME/client/lib:$LD_LIBRARY_PATH
  
  $ soruce ~/.bash_profile
  ```

  - `get_tip.sh`를 실행한다.

  ```bash
  $ cd $TB_HOME/config
  $ sh gen_tip.sh
  ```

  - 네트워크 파일을 설정한다.

  ```bash
  $ cd $TB_HOME/client/config
  $ vi tbdsn.tbr
  <위에서 설정해준 SID>=(
  	(INSTANCE=(HOST=<tibero host>)
  			  (PORT=<tibero port>)
  			  (DB_NAME=<연결할 DB 명>)
  	)
  )
  ```



- unixODBC-devel 패키지 설치(centos 기준)

  - gcc 패키지를 필요로 한다.

  ```bash
  # 설치 여부 확인
  $ gcc -v
  
  # 없을 경우 설치
  $ yum install gcc
  ```

  - unixODBC-devel  설치

  ```bash
  $ yum install unixODBC-devel
  ```

  - odbc.ini 파일 작성
    - /tibero6/client/lib에 있는 libtbodbc.so 파일이 Tibero ODBC 드라이버이다.
  
  
  ```bash
  $ vi /etc/odbc.ini
  [ODBC Data Sources]
  <위에서 설정해준 SID> = Tibero6 ODBC driver
  
  [ODBC]
  Trace = No
  TraceFile = /tmp/odbc.trace
  
  [tibero6]
  Driver = <tibero client 설치 경로>/client/lib/libtbodbc.so
  Description = Tibero6 ODBC Datasource
  SID = tb6
  User = tibero
  Password = tmax
  ```
  
  - 접근 가능 여부 확인
  
  ```bash
  $ isql -v tb6
  ```




- pyodbc 패키지 설치

  - pip로 설치

  ```bash
  $ pip install pyodbc
  ```




- 실행하기

  ```python
  import pyodbc
  
  
  DSN = "tb6"
  USER="tibero"
  PWd="tmax"
  
  connection_info = 'DSN='+DSN+';UID='+USER+';PWD='+PWD
  conn = pyodbc.connect(connection_info)
  conn.setencoding(encoding='utf-8')
  cursor = conn.cursor()
  sql = "select * from some_table"
  cursor.execute(sql)
  for col in cursor.fetchall():
      print(col)
  
  cursor.close()
  conn.close()
  ```

  