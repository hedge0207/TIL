# docker로 실행하기

> https://www.elastic.co/guide/en/logstash/current/docker.html 참고

- config 파일 작성하기

  - `test.conf` 파일을 작성한다.

  ```yaml
  input {
      elasticsearch {
          hosts => "${ES_HOST}"
          index => "logstash-test"
          query => '{"query":{"match_all":{}}}'
      }
  }
  
  output {
      stdout {}
  }
  ```



- docker compose file 작성하기

  - 이 파일을 실행하면 logstash는 컨테이너 내부의 `/usr/share/logstash/pipeline` 디렉터리에서 `.conf` 파일들을 찾아 해당 config로 실행된다.
  - 따라서 위에서 생성한 `test.conf`파일을 `/usr/share/logstash/pipeline`에 volume을 잡아줘야한다.

  ```yaml
  version: '3.2'
  
  services:
    logstash:
      image: logstash:7.16.2
      container_name: theo_logstash
      ports:
        - 9600:9600
      volumes:
        - ./config:/usr/share/logstash/pipeline
      environment:
        ES_HOST: "<es_host>:<es_port>"
      restart: always
  ```





## logstash와 DB 연결하기

- hive의 데이터를 logstash를 통해 elasticsearch에 바로 색인할 수 있다.

  - hive를 예로 들었지만 hive의 jdbc driver가 아닌 다른 DB의 jdbc driver를 쓰면 다른 DB도 연결이 가능하다.
    - ES 공식 홈페이지에는 mysql을 연결하는 예시가 나와 있다.
  - 설정 파일
    - 대략적인 설정은 아래와 같다.
    - schedule을 주지 않을 경우 1번만 실행된다.
  
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
  



- 실행하기

  - `/bin/logstash` 파일에 logstash 실행 경로 관련 설정이 있어 반드시 아래와 같이 실행해야 한다.

  ```bash
  $ cd <logstash 설치 폴더>
  $ bin/logstash -f <conf 파일 경로>
  ```




- 로그 파일 전송하기

  - logstash가 지원하는 input plugin 중 `file`을 사용하여, 읽어들일 log 파일을 지정한다.
    - path 외에도 다양한 설정이 있으나, path만이 required 값이다.

  ```json
  input {
     file {
         path => "/home/es/theo/logstash/test.log"
     }
  }
  ```

  - filter를 사용하여 로그를 파싱한다.
    - 주로 `grok` plugin을 사용하지만 명확한 구분자가 있을 경우 `disscet`을 사용하는 것이 훨씬 편하다.
    - 둘 이상의 filter를 적용 가능하기에 grok과 disscet을 둘 다 사용할 수도 있다.

  ```json
  filter {
     dissect {
         mapping => {
             "message" => "[%{date}] [%{level}] [%{path}] [%{status_code}] %{req_body}"
         }
     }
  }
  ```

  - 원하는 output을 지정해준다.

  ```bash
  output {
     stdout {}
  }
  ```

  - 예시

  ```bash
  # 아래와 같은 데이터는
  [2022-02-16 17:11:23] [INFO] [/v1/search] [200] {"name":"theo", "age":78}
  
  # 다음과 같이 파싱된다.
  {
  	"date": 2022-02-16 17:11:23
  	"level": INFO
  	"path": /v1/search
  	"status_code": 200
  	"req_body": {"name":"theo", "age":78}
  }
  ```





















