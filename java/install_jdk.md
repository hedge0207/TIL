# 설치

- Ubuntu에 설치하기

  - 아래 사이트에서 원하는 jdk 버전을 다운로드한다.

    > https://www.oracle.com/java/technologies/downloads/

  - 원하는 경로에 압축을 푼다.

  ```bash
  $ gzip -d <위에서 다운 받은 파일 경로>
  
  # tar 파일을 풀어야하는 경우 아래 명령어를 실행한다.
  $ tar -xvf <압축을 푼 결과로 나온 파일 경로>
  ```

  - 환경변수를 export한다.
    - `.bashrc` 파일에 아래와 같이 추가한다.

  ```bash
  $ vi ~/.bashrc
  
  
  export JAVA_HOME=<위에서 java를 설치한 경로>
  export PATH=$PATH:$JAVA_HOME/bin
  ```

  - 수정 사항을 적용한다.
  
  ```bash
  $ source ~/.bashrc
  ```
  
  