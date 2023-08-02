# 개요

- Fluentd
  - 오픈 소스 log collector이다.
    - 데이터를 수집하고, 파싱하고, 다른 곳으로 라우팅할 수 있다.
  - 특징
    - Data를 Json 형태로 구조화하여 사용한다.
    - 다양한 플러그인을 지원한다.
    - C와 Ruby(CRuby)로 개발되어 resource를 매우 적게 차지한다.
    - Memory base buffering과 file-base buffering이 모두 가능하여 HA(High Availablity)구성이 가능하다.
    - 보다 경령화된 버전인 Fluent-bit을 지원한다.
  - 역사
    - 2011년 Sadayuki Furuhashi에 의해 고안되었다.
    - Sadayuki Furuhashi는 Treasure Data라는 회사의 공동설립자이며, Treasure Data는 Fluentd의 주요 스폰서 중 하나이다.
    - 2016년 CNCF에서 승인을 받았고, 2019년에 Graduated Project가 됐다.



- Logstash와의 비교
  - 같은 log collector라는 점에서 logstash와 비교가 많이 되는 편이다.
    - ELK 스택에서 logstash를 빼고 fluentd를 넣어 EFK로 사용하는 경우도 많이 있다.
    - Github star 수 기준으로 logstash가 2천개 정도 앞서있다.
  - 자체 로그 수집 기능
    - Logstash는 자체적인 data 수집 기능은 없으며, 다양한 input plugin을 통해 들어오는 data들을 처리한다.
    - 반면에 Fluentd는 자체 데몬을 통해 다양한 소스의 로그를 수집할 수 있다.
  - 구현
    - Logstash는 JRuby로 구현되어 JVM 위에서 동작한다.
    - Fluentd는 C와 CRuby로 구현되어 JVM이 필요하지 않으며, 보다 가볍다.
  - Elasticsearch, Kibana와의 연동
    - Logstash와 Fluentd 모두 Elasticsearch, Kibana와 완벽한 연동을 지원한다.
    - 다만, 새로운 변경 사항에 대해서는 아무래도 Elastic 재단에서 관리하는 Logstash가 더 빠른 대응을 보여준다.
    - 또한 Elasticsearch, Kibana와 동일한 보안 기능을 지원하는 Logstash가 Elasticsearch, Kibana와 함께 사용하기 더 편리한 것은 사실이다.
    - 대신, Fluentd의 경우 CNCF에서 관리하는 다른 도구들과의 연동성이 좋다.
  - Plugin
    - Logstash의 경우 Elastic 재단이 관리하는 Logstash 공식 repo에서 약 200여개의 플러그인들을 관리중이다.
    - 반면에 Fluentd의 경우 Logstash 처럼 중앙 집중화된 관리소는 존재하지 않지만, 커뮤니티에서 만든 많은 플러그인들이 존재한다.
  - 성능
    - 성능에서 둘 사이의 차이는 거의 존재하지 않는다.
    - 다만 Fluentd가 메모리를 약간 덜 소비하는 것은 사실이다.
  - 안정성
    - Logstash의 경우 event를 memory에 저장하여 처리한다.
    - 따라서 처리 중 문제가 생길 경우 event가 유실될 수 있어, 일반적으로 Kafka나 Redis 등을 추가로 사용하여 안정성을 높이는 작업이 필요하다.
    - `반면에 Fluentd의 경우 memory와 disk중 어느 곳에 저장할지 선택할 수 있어 외부 queue 없이도 안정성을 보장할 수 있다.
    - 그러나 Logstash도 Persistence Queue를 지원한다.
  - UI
    - Logstash는 약간의 설정만 해주면 Kibana를 통해 UI를 사용 가능하다.
    - Fluentd는 Fluentd-ui 데몬을 따로 실행시켜야한다.
  - 분기 처리
    - Logstash의 경우 어떤 곳으로 데이터를 라우팅 시킬지를 결정하기 위해 `if else`문을 사용한다.
    - 익숙한 방법이긴 하지만, 라우팅 해야하는 곳이 늘어나면 금방 복잡해지게 된다.
    - Fluentd의 경우 입력으로 들어온 data이 포함된 tag를 보고 어느 곳으로 라우팅 시킬지를 결정한다.





## 동작 과정

- Fluentd는 크게 4개의 과정을 거쳐 동작한다.
  - Setup
    - Fluentd에 어떤 input 혹은 listener를 설정.
    - Event를 특정 output으로 routing하기 위한 일반적인 rule을 설정
  - Inputs
    - Event를 받아오는 단계
  - Filters
    - 받아온 event를 처리하는 단계
  - Matches and Labels
    - 처리된 event를 라우팅하는 단계



- Setup

  - `http`를 input으로 하고,  `stdout`을 output으로 하는 pipeline을 개발하려한다.
  - 먼저 configuration file에 아래와 같이 input 설정을 해준다.
    - HTTP server가 TCP port 8888번을 listening할 것이라는 의미이다.

  ```xml
  <source>
    @type http
    port 8888
    bind 0.0.0.0
  </source>
  ```

  - Matching rule 설정
    - `test.cycle`라는 tag를 달고 오는 event들을 `stdout`이라는 type의 output으로 라우팅하겠다는 의미이다.

  ```xml
  <match test.cycle>
    @type stdout
  </match>
  ```



- Input
  - Data source로부터 Fludentd event를 생성하는 것은 Input plugin이 맡는다.
  - Fluend의 event는 세 부분으로 구성된다.
    - `tag`: Event가 어디서 왔는지를 특정하며, message routing에 사용된다.
    - `time`: Event가 발생한 시간을 nonosecond 단위로 특정한다.
    - `record`: 실제 log를 JSON object로 특정한다.



- Filters

  - Setup이 설정되면, Router Engine에는 다양한 input data에 적용할 rule들이 포함되게 된다.
    - 내부적으로, Event는 event의 lifecycle을 변경시킬 수 있는 여러 절차를 거치게 된다.
  - Filter 설정하기
    - 아래에서 보이는 것과 같이 Filter는 Match section 전에 반드시 거쳐야 하는 단계가 되어, Event의 type 혹은 rule에 따라 어떤 event를 통과시킬지,  통과시키지 않을 지를 결정한다.
    - 아래 예시에서는 logout과 관련된 action을 모두 통과시키지 않도록 설정했다.

  ```xml
  <source>
    @type http
    port 8888
    bind 0.0.0.0
  </source>
  
  <filter test.cycle>
    @type grep
    <exclude>
      key action
      pattern ^logout$
    </exclude>
  </filter>
  
  <match test.cycle>
    @type stdout
  </match>
  ```



- Label

  - Label의 역할
    - Filter의 개수가 많아질수록, 설정 파일을 읽기 힘들어진다는 문제가 있는데, Label은 이러한 문제를 해결해준다.
    - 뿐만 아니라 Lable은 top-to-bottom 순서를 따르지 않는 새로운 routing section을 정의할 수 있게 해준다.
  - 예를 들어 Filter에서 설정한 configuration은 아래와 같이 바꿀 수 있다.
    - `source` 아래의 `@label` parameter는 이후의 단계들은 `@STAGING` label section에서 처리될 것임을 의미한다.
    - 모든 event들은 Source에 보고되고, Routing Engine은 `@STAGING`에서 작업을 수행할 것이다.
    - 즉, 기존의 filter는 skip된다.

  ```xml
  <source>
    @type http
    bind 0.0.0.0
    port 8888
    @label @STAGING	<!-- @label 추가 -->
  </source>
  
  <!--아래 filter는 skip되고-->
  <filter test.cycle>
    @type grep
    <exclude>
      key action
      pattern ^login$
    </exclude>
  </filter>
  
  <!--이 부분이 실행된다.-->
  <label @STAGING>
    <filter test.cycle>
      @type grep
      <exclude>
        key action
        pattern ^logout$
      </exclude>
    </filter>
  
    <match test.cycle>
      @type stdout
    </match>
  </label>
  ```



## 설치

- td-agent와 calyptia-fluentd
  - td-agent
    - Fluentd의 stable한 배포판이다.
    - Fluentd는 Ruby와 C로 개발되었다.
    - 사용자들이 Ruby daemon을 설치하고 실행하는데 겪는 불편을 최소화하기 위해서 td-agent를 제공한다.
  - calyptia-fluentd
    - Fluentd는 Ruby 2.7을 사용하고 있는데 호환성 문제로 Ruby 3을 사용해야 하는 사람들을 위해 Ruby3로 개발한 Fluentd라고 볼 수 있다.
    - Calyptia라는 회사가 관리하고 있다.



- Docker로 설치하기

  - Fluentd 이미지 받기

  ```bash
  $ docker pull fluent/fluentd
  ```

  - 간단하게 configuration 구성하기
    - 아무 경로에나 `fluent.conf` 파일을 아래와 같이 작성한다.

  ```xml
  <source>
    @type http
    port 9880
    bind 0.0.0.0
  </source>
  
  <match **>
    @type stdout
  </match>
  ```

  - 실행하기

  ```bash
  $ docker run -p 9880:9880 -v <fluent.conf 파일의 경로>:/fluentd/etc/fluent.conf --name <container name> fluent/fluentd:latest
  ```

  - 요청 보내보기

  ```bash
  curl -X POST -d 'json={"json":"message"}' http://127.0.0.1:9880/sample.test
  ```

  - 확인하기

  ```bash
  $ docker logs <container_name> | tail -n 1
  # 2023-04-18 06:54:14.760818700 +0000 sample.test: {"json":"message"}
  ```



- Elasticsearch output plugin 설치

  - `td-agent` V3.0.1 이상부터는 내장되어 있지만, docker image의 경우 elasticsearch output plugin이 내장되어 있지 않다.
    - 따라서 별도로 설치를 해줘야한다.
  - Fluentd image 생성을 위한 dockerfile 작성
    - `debian` 이미지를 사용해야 한다.

  ```dockerfile
  FROM fluent/fluentd:v1.16-debian-1
  
  USER root
  
  RUN apt update -y
  RUN apt install -y ubuntu-dev-tools
  
  RUN gem install elasticsearch -v 7.17.1 --no-document
  RUN gem install fluent-plugin-elasticsearch -v 5.0.3 --no-document
  
  USER fluent
  ```

  - Docker image 빌드

  ```bash
  $ docker build -t fluentd:latest .
  ```





## Docker log 수집하기

- Fluentd의 강점 중 하나는 Docker 컨테이너의 로그를 간단하게 수집할 수 있다는 점이다.
  - Application은 다양한 event 혹은 문제들을 로그로 남길 필요가 있지만, 이를 직접 관리하는 것은 매우 까다로운 일이다.
    - 특히 log를 분석해야 하거나, 여러 instance가 log를 남겨야 하는 상황인 경우에는 더 까다로워진다.
  
  - 그러나 Fluentd를 사용하면 보다 간단하게 docker container의 log를 수집할 수 있다.
    - Docker가 Fluentd logging driver를 제공하기 때문이다.
    - Docker v1.8부터 사용 가능하다.
  



- 우선 Docker log를 남기기 위해 log 생성기를 준비한다.

  - 아래와 같은 Python 스크립트를 통해 log를 남긴다.

  ```python
  import time
  import logging
  
  
  logger = logging.getLogger("simple_example")
  logger.setLevel(logging.DEBUG)
  
  sh = logging.StreamHandler()
  sh.setLevel(logging.DEBUG)
  
  formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] - %(message)s")
  sh.setFormatter(formatter)
  
  logger.addHandler(sh)
  
  
  try:
      while True:
          logger.info("Hello World!")
          time.sleep(1)
  except (KeyboardInterrupt, SystemExit):
      logger.info("Bye!")
  ```

  - Docker image 생성을 위한 dockerfile을 작성한다.

  ```dockerfile
  FROM python:3.8.0
  COPY ./main.py /main.py
  ENTRYPOINT ["python", "main.py"]
  ```

  - Docker image를 생성한다.

  ```bash
  $ docker build -t log-generator:1.0.0 <dockerfile 경로>
  ```



- Fluentd를 실행한다.

  - Configuration file 작성
    - `forward`는 다른 Fluentd로부터 log를 받아오는 plugin이다.

  ```xml
  <source>
    @type forward
    port 24224
    bind 0.0.0.0
  </source>
  
  <match *.*>
    @type stdout
  </match>
  ```

  - Fluentd를 실행한다.
    - 아래는 Docker로 실행시키는 명령어이다.

  ```bash
  $ docker run -p 24224:24224 -v <위에서 작성한 .conf파일 경로>:/fluentd/etc/fluent.conf --name log-fluent fluent/fluentd:latest
  ```



- 위에서 만든 로그 생성기를 실행한다.

  - `--log-driver` flag에 `fluentd`를 값을 준다.
    - `--log-opt`flag의 옵션으로 `fluentd-address=192.168.0.4:24225`와 같이 fluentd의 host와 port를 설정하는 것도 가능하다.

  ```bash
  $ docker run --log-driver=fluentd --name theo-log-gen theo-log-gen:lastest
  ```

  - 아래 명령어로 Fluentd container의 log를 확인해보면 log 생성기에서 생성된 로그가 출려되는 것을 확인할 수 있다.

  ```bash
  $ docker logs log-fluent
  ```






# Python과 연동하기

- Fluentd configuration file 작성하기

  - `./conf/fluent.conf`에 아래와 같이 configuration 파일을 생성한다.

  ```xml
  <source>
    @type forward
    port 24224
  </source>
  <match fluentd.test.**>
    @type stdout
  </match>
  ```



- Fluentd docker container 생성

  ```yaml
  version: "3"
  services:
    fluentd:
      image: fluent/fluentd:latest
      volumes:
        - ./conf/fluent.conf:/fluentd/etc/fluent.conf
      ports:
        - "24224:24224"
  ```



- Python script 작성하기

  - Fluentd package 설치

  ```bash
  $ pip install fluent-logger
  ```

  - Script 작성

  ```python
  from fluent import sender
  from fluent import event
  
  
  sender.setup('fluentd.test', host='localhost', port=24224)
  event.Event('follow', {
    'from': 'userA',
    'to':   'userB'
  })
  ```

  - 위 파일을 실행하면 아래와 같이 log가 찍히게 된다.

  ```
  fluentd-fluentd-1  | 2023-04-25 05:00:52.000000000 +0000 fluentd.test.follow: {"from":"userA","to":"userB"}
  ```

  















