# Rally

> https://github.com/elastic/rally
>
> https://esrally.readthedocs.io/en/latest/index.html

- Rally

  - Elasticsearch cluster의 성능을 측정할 수 있는 framework이다.

    - Elasticsearch를 개발한 elastic에서 개발했다.
    - Python으로 개발되었다.

    - Windows에서 동작하는 Cluster를 benchmark하는 것은 가능하지만, Rally 자체는 Unix 운영체제에서 실행되어야한다.
    - [Docker](https://hub.docker.com/r/elastic/rally)로도 사용이 가능하다.

  - Elasticsearch의 새로운 version이 release 될 때 마다 rally를 활용하여 benchmark를 수행한다.

  - Cluster를 benchmark한 결과를 Kibana를 통해 시각화해서 볼 수 있다.



- Rally 설치

  - 설치전 필요한 것들
    - Python과 pip3가 설치되어 있어야한다.
    - Rally는 부하 테스트를 실행하기 전에 내부적으로 Elasticsearch를 직접 다운로드해서 실행하기 때문에 git과 JDK가 설치되어 있어야한다.

  - 아래와 같이 Rally를 설치한다.

  ```bash
  $ pip install esrally
  ```



- Track과 Car

  - Track
    - 부하 테스트를 진핼할 때 사용할 data로, 경주를 시작할 때 track을 정하는 것 처럼 부하 테스트에 사용할 data를 선택해야한다.
    - Elasticsearch benchmark 사이트에서 제공하는 분석 data를 그대로 사용할 수 있다.
    - 아래 명령어로 rally에 존재하는 track들을 조회할 수 있다.

  ```bash
  $ esrally list tracks
  ```

  - Car
    - 부하 테스트를 진행할 때 사용할 Elasticsearch node이다.
    - 원하는 car를 선택하면 부하 테스트를 실행할 때 선택한 구성의 Elasticsearch를 내려 받아 자동으로 설정한 후 benchmark를 실행한다.
    - 아래 명령어로 Rally가 제공하는 car의 종류를 확인할 수 있다.
    - 결과로 car와 mixin들이 출력되는데 car는 Elasticsearch server를 의미하고, mixin은 car에 추가할 설정을 의미한다.

  ```bash
  $ esrally list cars
  ```



- Pipeline

  - Benchmark를 실행하고 결과를 얻기 위한 일련의 과정을 설정하는 flag이다.
    - Benchmark 자체를 customize하는 flag가 아니라 benchmark 이전과 이후에 어떤 동작을 취할지를 설정하는 flag이다.
    - 현재는 3 가지 설정만 지원한다.

  ```bash
  $ esrally list pipelines
  ```

  - `from-sources`
    - Source code로부터 Elasticsearch를 build하고 build된 Elasticsearch에 benchmark를 실행한다.
    - Source code로부터 설치하더라도 git은 설치되어 있어야한다.
    - `--revision` flag를 함께 설정해야며, `--revision` flag를 설정하면 따로 명시하지 않아도 이 pipeline이 선택된다.
    - Elasticsearch를 개발하는 사람들을 위한 pipeline이라고도 볼 수 있다.

  ```bash
  $ esrally race --track=<track> --pipeline=from-sources --revision=<revision>
  ```

  - `from-distribution`
    - 공식 Elasticsearch distribution을 다운 받아, 이것으로 benchmark를 실행한다.
    - Snapshot repository를 명시하여 Elasticsearch snapshot versions도 benchmark 할 수 있으나, official distribution을 사용하는 것을 권장한다.
    - `--distribution-version`를 줄 경우 따로 명시하지 않아도 이 pipeline이 선택된다.

  ```bash
  # 아래 두 명령어는 사실상 같다.
  $ esrally race --track=<track> --pipeline=from-distribution --distribution-version=7.0.0
  
  $ esrally race --track=<track> --distribution-version=7.0.0
  ```

  - `benchmark-only`
    - 이미 존재하는 cluster를 대상으로 benchmark를 수행할 경우 이 pipeline을 사용하면 된다.
    - 이름에서 알 수 있듯 benchmark만 수행하는 flag이다.
    - Rally가 cluster를 provisioning 할 수 없기 때문에 CPU 사용량 같은 지표들을 수집할 수 없다는 한계가 있다.

  ```bash
  $ esrally race --track=geonames --pipeline=benchmark-only --target-hosts=127.0.0.1:9200
  ```



- Race 시작하기

  - `race`명령어를 통해 실행하면 된다.

  ```bash
  $ esrally race [option1] [option2] [...]
  ```

  - distribution-version
    - Test를 실행할 Elasticsearch version을 입력한다.
  - `track`
    - Race를 실행할 track을 입력한다.
  - `car`
    - Race를 실행할 car를 입력한다.
    - `,`로 구분하여 car와 mixin을 조합할 수 있다.

  ```bash
  $ esrally race --track=geonames --car="4gheap,ea"
  ```

  - `report-format`과 `report-file`
    - 기본적으로 benchmark 결과 보고서는 stdout 출력된다.
    - `report-file`을 입력할 경우 설정된 경로에 file을 생성한다.
    - `report-format`으로 file format을 설정할 수 있다(markdown과 csv를 지원하며 기본 값은 markdown이다).

  ```bash
  $ esrally race --track=<track> --report-format=csv --report-file=~/benchmarks/result.csv
  ```



- Race 결과

  - Race를 실행하면 아래와 같은 보고서가 출력된다.
    - Markdown 형식으로 출력된되기에 markdown을 지원하는 곳에 그대로 붙여넣을 수 있다.

  ```
  ------------------------------------------------------
      _______             __   _____
     / ____(_)___  ____ _/ /  / ___/_________  ________
    / /_  / / __ \/ __ `/ /   \__ \/ ___/ __ \/ ___/ _ \
   / __/ / / / / / /_/ / /   ___/ / /__/ /_/ / /  /  __/
  /_/   /_/_/ /_/\__,_/_/   /____/\___/\____/_/   \___/
  ------------------------------------------------------
              
  |                                                         Metric |   Task |          Value |   Unit |
  |---------------------------------------------------------------:|-------:|---------------:|-------:|
  |                     Cumulative indexing time of primary shards |        |   15.1736      |    min |
  |             Min cumulative indexing time across primary shards |        |    1.66667e-05 |    min |
  |          Median cumulative indexing time across primary shards |        |    0.106033    |    min |
  |             Max cumulative indexing time across primary shards |        |    2.28273     |    min |
  |            Cumulative indexing throttle time of primary shards |        |    0           |    min |
  |    Min cumulative indexing throttle time across primary shards |        |    0           |    min |
  | Median cumulative indexing throttle time across primary shards |        |    0           |    min |
  |    Max cumulative indexing throttle time across primary shards |        |    0           |    min |
  |                        Cumulative merge time of primary shards |        |    1.43273     |    min |
  |                       Cumulative merge count of primary shards |        |  158           |        |
  |                Min cumulative merge time across primary shards |        |    0           |    min |
  |             Median cumulative merge time across primary shards |        |    0           |    min |
  |                Max cumulative merge time across primary shards |        |    0.254667    |    min |
  |               Cumulative merge throttle time of primary shards |        |    0           |    min |
  |       Min cumulative merge throttle time across primary shards |        |    0           |    min |
  |    Median cumulative merge throttle time across primary shards |        |    0           |    min |
  |       Max cumulative merge throttle time across primary shards |        |    0           |    min |
  |                      Cumulative refresh time of primary shards |        |    1.05298     |    min |
  |                     Cumulative refresh count of primary shards |        | 1664           |        |
  |              Min cumulative refresh time across primary shards |        |    0.0002      |    min |
  |           Median cumulative refresh time across primary shards |        |    0.00301667  |    min |
  |              Max cumulative refresh time across primary shards |        |    0.3159      |    min |
  |                        Cumulative flush time of primary shards |        |    0.110067    |    min |
  |                       Cumulative flush count of primary shards |        |   26           |        |
  |                Min cumulative flush time across primary shards |        |    0           |    min |
  |             Median cumulative flush time across primary shards |        |    0.00235     |    min |
  |                Max cumulative flush time across primary shards |        |    0.0186667   |    min |
  |                                        Total Young Gen GC time |        |    0.017       |      s |
  |                                       Total Young Gen GC count |        |    3           |        |
  |                                          Total Old Gen GC time |        |    0           |      s |
  |                                         Total Old Gen GC count |        |    0           |        |
  |                                                     Store size |        |    1.57477     |     GB |
  |                                                  Translog size |        |    0.556367    |     GB |
  |                                         Heap used for segments |        |    0           |     MB |
  |                                       Heap used for doc values |        |    0           |     MB |
  |                                            Heap used for terms |        |    0           |     MB |
  |                                            Heap used for norms |        |    0           |     MB |
  |                                           Heap used for points |        |    0           |     MB |
  |                                    Heap used for stored fields |        |    0           |     MB |
  |                                                  Segment count |        |   93           |        |
  |                                    Total Ingest Pipeline count |        |    0           |        |
  |                                     Total Ingest Pipeline time |        |    0           |      s |
  |                                   Total Ingest Pipeline failed |        |    0           |        |
  |                                                 Min Throughput |   bulk |  984.72        | docs/s |
  |                                                Mean Throughput |   bulk |  984.72        | docs/s |
  |                                              Median Throughput |   bulk |  984.72        | docs/s |
  |                                                 Max Throughput |   bulk |  984.72        | docs/s |
  |                                        50th percentile latency |   bulk |   28.8898      |     ms |
  |                                       100th percentile latency |   bulk |   47.3623      |     ms |
  |                                   50th percentile service time |   bulk |   28.8898      |     ms |
  |                                  100th percentile service time |   bulk |   47.3623      |     ms |
  |                                                     error rate |   bulk |    0           |      % |
  
  
  --------------------------------
  [INFO] SUCCESS (took 49 seconds)
  --------------------------------
  ```



- 이미 존재하는 cluster에서 benchmark 실행하기

  > :warning: 만약 Rally에 익숙하지 않고, Rally가 어떻게 동작하는지 모른다면, production cluster에서 Rally를 실행해선 안 된다.
  >
  > 또한 익숙하다고 하더라도 benchmark는 가급적 다른 traffic이 benchmark 결과에 영향을 미치지 않는 benchmark 전용 cluster에서 실행하는 것을 권장한다.

  - 아래와 같이 `race`를 실행할 때 `--target-hosts`를 입력하면 된다.

  ```bash
  $ esrally race --track=<track> --target-hosts=127.0.0.1:9200 --pipeline=benchmark-only
  ```

  - 만약 보안 기능이 활성화 되어 있다면 `--client-options` flag를 함께 줘야한다.
    - 아래는 예시로, 보안 설정에 맞는 값을 입력해야한다.

  ```bash
  esrally race --track=<tack> --target-hosts=10.5.5.10:9243,10.5.5.11:9243,10.5.5.12:9243 --pipeline=benchmark-only --client-options="use_ssl:true,verify_certs:true,basic_auth_user:'elastic',basic_auth_password:'changeme'"
  ```





## Custom Track 생성하기

> https://esrally.readthedocs.io/en/latest/adding_tracks.html
>
> https://esrally.readthedocs.io/en/latest/track.html

- 이미 존재하는 cluster에서 data를 추출하여 track을 생성할 수 있다.

  - `create-command` 명령어를 사용하여 track을 생성할 수 있다.
    - `--track`에 생성할 track의 이름을 작성한다.
    - `--target-hosts`에 Elasticsearch url을 입력한다.
    - `--indices`에 test를 실행할 index들을 입력한다.
    - `--output-path`에 생성한 track을 저장할 path를 입력한다.

  ```bash
  $ esrally create-track --track=my_track --target-hosts=127.0.0.1:9200 --indices="foo" --output-path=./tracks
  ```

  - 위 명령어를 실행하면 지정한 위치에 track 이름으로 된 directory가 생성된다.
    - `track.json`: 실제 Rally track에 대한 정보를 담고 있다.
    - `foo.json`: 대상 index의 mapping, setting 정보를 담고 있다.
    - `*-documents.json(.bz2)`: 대상 index의 모든 documents를 담고 있으며, `-1k` suffix가 붙은 file은 더 적은 양의 document를 담고 있는 file로 test mode에 사용된다.

  ```bash
  $ find tracks/my_track
  
  # 결과
  tracks/my_track
  tracks/my_track/foo.json
  tracks/my_track/track.json
  tracks/my_track/foo-documents-1k.json.bz2
  tracks/my_track/foo-documents-1k.json
  tracks/my_track/foo-documents.json
  tracks/my_track/foo-documents.json.bz2
  ```

  - 추출한 track을 race에 사용하려면 `--track-path`로 생성된 `track.json` file이 있는 directory의 위치를 입력하면 된다.

  ```bash
  $ esrally race --esrally race --track-path=./tracks/my_track --target-hosts=127.0.0.1:9200 --pipeline=benchmark-only
  ```



