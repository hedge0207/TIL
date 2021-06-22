# Python에서 Oracle 사용하기

- Python과 Oracle 연동하기
  - mysql과는 다르게 Oracle은 단순히 패키지(mysql의 pymysql 처러)만 설치한다고 접근할 수는 없다.
  - 패키지 설치 외에 Oracle 클라이언트를 설치해야 한다.



- 패키지 설치하기

  - `cx_Oracle` 패키지 설치

  ```bash
  $ pip install cx_Oracle
  ```



- 리눅스에 Oracle client 설치하기

  - libaio 패키지를 설치한다.

  ```bash
  $ sudo apt install libaio1
  ```

  > \https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

  - 위 사이트에 접속해서 zip 또는 rpm 파일을 다운로드한다.
  - zip 파일을 받았을 경우 아래 명령어로 압축을 해제한다.

  ```bash
  $ unzip instantclient-basic-linux.x64-21.1.0.0.0.zip
  ```

  - 그 후 압축 해제된 폴더를 `/opt/oracle` 폴더에 옮긴다.

  ```bash
  # 디렉토리 생성
  $ mkdir /opt/oracle
  
  # 옮긴다.
  $ mv instantclient_21_1 /opt/oracle
  ```

  - 아래와 같이 설정해준다.
    - 혹은 그냥 export 해줘도 된다.

  ```bash
  # 이렇게 하거나
  $ sudo sh -c "echo /opt/oracle/instantclient_21_1 > /etc/ld.so.conf.d/oracle-instantclient.conf"
  $ sudo ldconfig
  
  # 이렇게 한다.
  export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_1:$LD_LIBRARY_PATH
  ```

  - rpm 파일을 받았을 경우 아래 명령어로 설치한다.

  ```bash
  $ sudo yum install oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm
  ```

  - 아래와 같이 설정해준다.
    - 혹은 그냥 export 해줘도 된다.

  ```bash
  # 이렇게 하거나
  sudo sh -c "echo /usr/lib/oracle/18.5/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf"
  sudo ldconfig
  
  # 이렇게 한다.
  export LD_LIBRARY_PATH=/usr/lib/oracle/18.5/client64/lib:$LD_LIBRARY_PATH
  ```







# 참고

https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#cx-oracle-8-installation

https://willbesoon.tistory.com/120