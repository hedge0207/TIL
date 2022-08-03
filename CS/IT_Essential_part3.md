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

