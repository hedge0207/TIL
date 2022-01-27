## logstash와 DB 연결하기

- hive의 데이터를 logstash를 통해 elasticsearch에 바로 색인할 수 있다.

  - hive를 예로 들었지만 hive의 jdbc driver가 아닌 다른 DB의 jdbc driver를 쓰면 다른 DB도 연결이 가능하다.
    - ES 공식 홈페이지에는 mysql을 연결하는 예시가 나와 있다.
  - 설정 파일
    - 대략적인 설정은 아래와 같다.

  ```yml
  input {
     jdbc {
         jdbc_driver_library => "./hive-jdbc-2.3.9.jar,./libthrift-0.9.3.jar,./hive-service-rpc-2.3.9.jar,./hive-service-2.3.9.jar,./hive-common-2.3.9.jar,./commons-lang-2.6.jar,./hive-serde-2.3.9.jar"
         jdbc_driver_class => "org.apache.hive.jdbc.HiveDriver"
         jdbc_connection_string => "jdbc:hive2://<Host>:<Port>/<DB명>"
         jdbc_user => "some_user_name"
         jdbc_password => "my_password"
         statement => "select * from product"
         schedule => "* * * * *"
     }
  }
  output 
     elasticsearch {
         hosts => ["10.12.109.101:8379"]
         index => "logstash_test"
     }
  }
  ```

  - input
    - `jdbc_driver_library`: 연결에 필요한 라이브러리들을 입력한다.
    - `jdbc_driver_class`: 드라이버 클래스를 설정한다(DB마다 다르므로 다른 DB를 사용하고자 하면 드라이버 클래스를 찾아봐야 한다).
    - `jdbc_connection_string`: DB와 연결 정보를 입력한다.
    - `jdbc_user`, `jdbc_password`: DB에 등록된 사용자명과 비밀번호를 입력한다.
    - `statement`: DB에서 실행할 쿼리를 입력한다.
    - `schedule`: 데이터 수집을 실행할 주기를 입력한다(crontab과 동일하다).
  - output
    - elasticsearch의 host와 index명을 입력한다.



- jdbc_driver_library

  > https://www.apache.org/dyn/closer.cgi/hive/

  - 다른 설정은 크게 문제될 것이 없으나 주로 jdbc_driver_library에서 문제가 발생한다.
  - DB 연결을 위한 라이브러리들을 설치해줘야 하는데 워낙 많다보니 일일이 찾아서 입력해줘야 하는 번거로움이 있다.
  - 필요한 라이브러리 확인
    - 필요한 라이브러리를 설치하지 않은 상태에서 logstash를 실행하면 아래와 같이 `NoClassDefFoundError`가 발생하면서 어떤 class가 없는지를 알려준다.
    - 추후 필요한 라이브러리를 한 번에 확인하는 방법을 찾으면 추가 예정

  - 라이브러리 설치
    - 위 링크로 가서 필요한 버전의 apach-hive를 다운 받는다.
    - 압축을 풀면 다양한 jar 파일이 있을텐데 원래는 `jdbc/hive-jdbc-2.3.9-standalone.jar`  하나만 있으면 실행이 가능하다.
    - 즉 `hive-jdbc-2.3.9-standalone.jar`파일만 logstash 폴더의 적당한 위치에 놓고 `jdbc_driver_library`에 그 경로를 지정해주면 실행이 된다.
    - 그러나 log4j 문제로 이전 버전인 `hive-jdbc-2.3.9-standalone.jar` 파일이 실행되지 않는 문제가 있어 일일이 필요한 라이브러리를 찾아서 옮겨줘야 한다.
    - 위 예시의 경우 `StringUtil`이라는 클래스가 없다고 하므로 `lib/` 폴더 내부의 `commons-lang-2.6.jar` 파일을 logstash 폴더 내부에 옮긴 후, 아래와 같이 추가해준다.
    - 위 예외가 발생하지 않을 때 까지 이 과정을 반복한다.
  
  ```yaml
  input {
     jdbc {
         jdbc_driver_library => "./commons-lang-2.6.jar"
     }
  }
  ```
  
  



















