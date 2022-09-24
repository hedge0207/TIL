# Data processing

- Data processing이란

  - Data를 수집하고, 조작하고, 수집된 데이터를 의도한 목적대로 사용하는 것을 의미한다.

  - 일반적으로 수집-집계-분석의 과정으로 이루어진다.

  - 아래와 같이 다양한 방식이 존재한다.
    - Batch processing
    - Real-time/Stream processing
    - Online Processing
    - MultiProcessing
    - Time-Sharing



- Batch processing

  - 대량의 데이터를 모아서 정해진 기간 동안 한 번에 처리하는 data processing 기법이다.
    - 여러 개의 데이터를 처리하는 것 뿐 아니라, 대용량의 데이터를 한 번에 처리한다면 batch processing이라 할 수 있다.
    - 즉 핵심은 몇 개의 데이터를 한 번에 처리한다는 것이 아니라 큰 데이터를 한 번에 처리한다는 것이다.

  - 아래와 같은 경우에 주로 사용한다.
    - Data size가 정해져 있거나, 예측할 수 있는 경우.
    - Data가 일정 기간동안 축적되고, 비슷한 data들을 그룹화 할 수 있는 경우.
    - 데이터의 생성과 사용 사이에 시간적 여유가 있는 경우.
  - 사용 예시
    - 월 단위 결제



- Stream processing

  - 데이터가 모일 때 까지 기다리지 않고 data가 생성된 즉시 바로 처리하는 data processing 기법이다.
    - data를 real-time 혹은 near real-time으로 처리한다.
    - 이전에는 real-time processing이라는 명칭을 더 많이 사용했으나 요즘은 stream processing이 더 널리 사용된다.

  - 아래와 같은 경우에 주로 사용한다.
    - Data size가 무한하거나, 예측할 수 없는 경우.
    - input이 들어오는 속도만큼 output을 산출하는 속도를 낼 수 있는 경우.
    - 데이터가 연속적으로 들어오면서, 데이터를 즉각적으로 사용해야 할 경우.
  - 사용 예시
    - 실시간 로그 분석



- Batch processing과 Stream processing의 차이

| Batch Processing                                             | Stream Processing                                            |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 많은 양의 data를 한 번에 처리                                | streaming data를 실시간으로 처리                             |
| 여러 단계를 거쳐 data를 처리                                 | 적은 단계를 거쳐 data를 처리                                 |
| Data를 처리하는데 분~일 단위의 시간이 소요                   | 초 또는 밀리초 단위로data를 처리                             |
| input이 안정적                                               | input이 유동적                                               |
| Data 처리가 모두 끝난 후 응답이 제공된다.                    | 응답이 바로 제공된다.                                        |
| 대량의 batch data 처리를 위해 storage와 processing resource가 필요하다 | Batch에 비해 storage는 덜 필요하지만 processing resources는 필요하다. |





# Monorepo Vs Polyrepo

> https://medium.com/hcleedev/dev-monorepo-%EA%B0%9C%EB%85%90-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0-33fd3ce2b767

- Monorepo
  - 하나의 project를 하나의 repository에서 관리하는 것을 의미한다.
    - 예로 Front-end 코드와 Back-end 코드를 한 repo에서 관리하는 것을 들 수 있다.
  - one-repo, uni-repo라고도 부른다.



- Polyrepo
  - 하나의 project를 하나의 repository에서 관리하는 것을 말한다.
    - 예로 Front-end 코드와 Back-end 코드를 각기 다른 repo에서 관리하는 것을 들 수 있다.
  - many-repo, multi-repo라고도 부른다.



- Monorepo의 장점
  - Project의 version을 일괄적으로 관리하기가 쉽다.
    - 여러 모듈의 버전을 일일이 맞춰주지 않아도 된다.
  - 코드의 재사용성이 증가한다.
    - 만일 하나의 project를 구성하는 2개의 각기 다른 repo에서 공통된 code를 사용해야 할 경우, 공유가 불가능하므로 중복된 code가 들어갈 수 밖에 없다.
    - 그러나 Monorepo의 경우 여러 모듈을 하나의 repo에서 관리하므로 코드의 재사용이 가능하다.
  - 의존성 관리가 쉬워진다.
    - 의존성을 하나의 repo에서만 관리하면 되므로 의존성 관리가 간편해진다.
  - 변경 사항을 보다 원자적으로 관리할 수 있다.
    - 만일 여러 repo에서 공통적으로 쓰이는 코드가 변경되었을 경우, 모든 repo를 돌면서 변경 사항을 적용해줘야한다.
    - 그러나 monorepo의 경우 한번의 변경으로 적용이 가능하다.
  - Team 간의 경계와 code ownership이 유연해진다.
    - 이를 통해 보다 원활한 협업이 가능해진다.



- Monorepo의 단점

  - Project가 거대해질 수록 monorepo를 관리하는데 소요되는 비용이 증가한다.
  - 의존성을 추가하는 데 부담이 없어, 불필요한 의존성이 증가한다.

  - Code Ownership에 위배된다.
    - Code의 소유권은 단일 팀에 속해야 한다고 생각하는 개발자들도 있다.
    - Code에 대한 책임이 모호해져 코드 관리가 더 힘들어질 수 있다.



