# tips

- 언제 topic을 분리하고, 언제 topic을 합쳐야 하는가
  - 기본적으로 RDBMS의 entitiy 개념을 kafka에도 적용하여 서로 다른 entity는 서로 다른 topic에 저장한다.
  - 만일 message를 순서대로 처리해야 한다면 다른 entitiy라 하더라도 같은 topic에서 처리한다.
    - kafka는 오직 같은 토픽의 같은 파티션 내에서만 순서를 모장하기 때문이다.
  - 다른 entity라 하더라도 한 entity가 다른 entity에 의존적이라면, 같은 topic에 저장한다.
    - 혹은 의존적이지는 않더라도 둘이 자주 함께 처리 된다면, 같은 topic에 저장한다.
    - 반면에 서로 관련이 없거나, 서로 다른 팀에서 관리한다면 다른 topic에 저장한다.
    - 만일 한 entity가 다른 entity에 비해 message 양이 압도적으로 많다면, topic을 분리하는 것이 좋다.
    - 그러나 적은 message 양을 갖는 여러 entity는 하나의 topic으로 묶는 것이 좋다.
  - 하나의 event가 여러 entity와 관련된 경우 하나의 topic으로 묶는 것이 좋다.
    - 예를 들어 purchase라는 entity는 product, customer라는 entity와 관련이 있을 수 있는데, 이들은 하나의 topic에 묶어서 저장하는 것이 좋다.
    - 추가적으로, 위와 같은 경우 message 자체를 분리하지 말고 한 message에 넣는 것이 좋다.
    - 여러 entity로 조합된 message를 분리하기는 쉬워도 분리된 여러 message를 하나의 message로 합치는 것은 어렵기 때문이다.
  - 여러 개의 consumer들이 특정한 topic 들의 group을 구독하고 있다면, 이는 topic을 합쳐야 한다는 것을 의미한다.
    - 잘개 쪼개진 topic을 합치게 되면 몇몇 consumer들은 원치 않는 message를 받게 될 수도 있다.
    - 그러나 Kafka에서 message를 받아오는 작업은 비용이 매우 적게 들기 때문에, consumer가 받아오는 message의 절반을 사용하지 않는다고 하더라도, 이는 크게 문제가 되지 않는다.
    - 그러나, 상기했듯 한 entity가 다른 entity에 비해 message 양이 압도적으로 많다면(99.9 대 0.01 정도라면) 그 때는 분리하는 것을 추천한다. 