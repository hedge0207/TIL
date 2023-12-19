# CDC

- CDC(Change Data Capture)
  - 변경된 데이터를 판별 하는 데 사용되는 소프트웨어 설계 패턴이다.
    - 대부분의 application에서 data가 추가되고, 삭제되고, 수정되는 일이 빈번하게 발생한다.
    - 따라서 application 내에서 같은 data를 사용하는 component들 끼리 sync를 맞추는 것이 매우 중요하다.
    - 그러나 변경 사항이 있을 때 마다 모든 data를 복제하여 사용하는 것은 비효율적이다.
    - 변경 사항이 있는 데이터만 판별하여 data들 사이에 sync를 맞추기 위해 사용하는 것이 CDC이다.
  - 크게 pull 방식과 push 방식이 있다.
    - Push 방식은 source system이 변경 사항을 기록하고 이를 application 등의 downstream으로 전송하는 방식이다.
    - Source database가 변경 사항이 있을 때 마다 downstream으로 변경 사항을 전파하므로 준 실시간으로 data의 변경 사항을 반영할 수 있다는 장점이 있지만, target system이 이를 받는 데 실패할 경우 sync가 맞지 않게 될 수 있으므로 이에 대한 대비책을 마련해야 한다는 단점이 있다.
    - Pull 방식은 source system은 변경 사항만 기록하고 downstream에서 주기적으로 이 변경 사항을 읽어오는 방식이다.
    - Target system이 변경 사항을 pull 하기 전까지는 변경 사항을 알 수 없다는 단점이 있다.
    - 일반적으로 push 방식과 pull 방식 모두 source database와 target system 사이에 source에서 target으로 보내는 변경 사항을 저장할 수 있는 messaging system을 둔다.



- CDC pattern

  - Timestamp-based

    - DB의 table에 마지막으로 변경된 시점을 기록할 수 있는 column을 추가하여 row가 변경될 때 마다 해당 값도 함께 변경하는 방식으로 변경사항을 추적한다.
    - 이 column은 일반적으로 last_modified, last_updated 등의 이름을 갖는다.
    - Downstream에서는 이 값을 가지고 data들을 조회한다.
    - 사용과 구현이 간편하다는 장점이 있다.
    - 삭제된 row를 찾을 수 없고, target system에서 source system의 모든 last_updated column의 값을 확인해야 하므로 source system에 부하가 가해진다.

  - Trigger-based

    - 대부분의 database는 trigger 기능을 제공한다.
    - Table에 IUD 등이 발생할 경우 자동으로 실행되는 프로시저이다.
    - Data의 변경 사항은 shadow table 혹은 event table이라 불리는 별도의 table에 저장된다.
    - 삭제를 포함한 모든 종류의 변경 사항을 탐지할 수 있으며, 많은 수의 database가 trigger를 지원한다는 장점이 있다.
    - 그러나 변경 사항이 생길 때 마다 source database가 변경 사항을 기록해야 하므로 source database의 성능에 악영향을 미친다는 단점이 있다.

  - Log-based

    - Transaction log라 불리는 file에 변경 사항을 모두 기록하여 이를 활용하는 방식이다.
    - 일반적으로 transaction log는 backup이나 재해 복구를 목적으로 사용하지만, CDC에도 사용될 수 있다.
    - Data의 변경 사항은 실시간으로 탐지되어 file로 작성되고, target system은 이 file을 읽어 변경 사항을 반영한다.

    - Source database에 overhead가 가해지지 않고, 모든 종류의 변경 사항을 탐지할 수 있으며, source database의 schema를 변경하지 않아도 된다는 장점이 있다.
    - Transaction log에 대한 표준화된 format이 없어 표준화가 어려울 수 있다.



- BASE
  - 기존 RDBMS에서 트랜잭션의 성질을 나타내기 위해 ACID(Atomicity, Consistency, Isolation, Durability)라는 약어를 사용했다. 
  - NoSQL 계열에서는 주로 ACID가 아닌 BASE(Basically Available, Soft state, Eventually consistent)라는 용어를 사용한다.
    - ACID는 transaction의 안정성을 강조하는 반면, BASE는 시스템 전체의 고가용성과 성능을 강조한다.
  - Basically Available
    - 읽기와 쓰기 작업이 가능하도록 최대한의 노력을 하지만 일관성이 없을 수 있다는 의미이다.
    - 특정 서버에서 error가 발생하더라도 다른 서버에서 읽기와 쓰기가 가능하도록 한다.
    - 고가용성과 관련이 있는 개념이다.
    - 그러나 쓰기 작업은 충돌이 발생할 경우 영구적으로 반영되지 않을 수도 있으며, 읽기 작업을 통해 읽어 온 data는 최신 데이터가 아닐 수도 있다.
  - Soft state
    - 저장소는 쓰기 일관성이 있을 필요가 없으며, 복제본들이 항상 같은 상태를 유지할 필요가 없다는 의미이다.
    - Data의 변경사항이 모든 복제본에 즉각적으로 반영되지 않을 수 있다.
    - 그러나 eventual consistency에 의해 결과적으로는 복제본들이 같은 data를 가지게 된다.
    - 이는 다르게 말하면 외부의 입력 없이도 data가 변경될 수 있다는 것을 의미한다.
    - 예를 들어 A와 A의 복제본인 A'가 있다고 가정해보자.
    - A에 새로운 입력이 들어왔고 A에는 이 사항이 반영됐다.
    - 그 후 A'에 읽기 요청이 들어오고, A'는 아직 A와 동기화 되지 않은 data를 반환한다.
    - 그 후 A'에 A의 data가 동기화 된다.
    - 이후에 사용자가 다시 A'에 읽기 요청을 하면 변경된 data를 받게 된다.
    - 사용자 입장에서는 아무 입력도 하지 않았는데 A'의 값이 변경된 것과 마찬가지이다.
    - 즉 사용자는 쓰기-읽기-읽기를 실행했고, 읽기와 읽기 사이에는 data를 변경하려는 조작을 하지 않았음에도 A'의 data에는 변경이 발생했다.
  - Eventual consistency(결과적 일관성)
    - 여기서의 consistency가 표현하고자 하는 것은 ACID의 consistency가 표현하고자 하는 것과 다르다.
    - Soft state에서 설명했 듯이 복제본들이 항상 같은 상태를 유지할 필요가 없으므로, 단기적으로는 일관성을 잃을 수 있으나 결국에는 일관성을 유지해야한다는 의미이다.
    - 반대되는 개념으로 strong consistency가 있다.



- CAP theorem(Brewer's theorem)

  > http://eincs.com/2013/07/misleading-and-truth-of-cap-theorem/
  >
  > https://www.julianbrowne.com/article/brewers-cap-theorem/

  - CAP theorem은 Consistency, Availability, Partition tolerance 모두를 만족하는 분산 시스템은 있을 수 없다는 정리이다.
    - 컴퓨터 과학자 Eric Brewer가 주장하여 Brewer's theorem이라고도 불린다.
    - 2000년에 Eric Brewer가 CAP 가설을 발표하고 이에 대한 증명이 2002년에 Gilbert와 Lynch에 의해 이루어졌다.
    - 주의할 점은 CAP theorem은 분산 시스템을 설명하기 위한 정리이므로 분산 시스템이 아닌 시스템을 설명하는 데 사용해선 안 된다는 점이다.
  - Consistency
    - 읽기 작업은 항상 최신 상태의 data를 읽어와야 하며, 그렇지 못 할 경우 읽어와서는 안 된다.
    - Brewer는 consistency라는 단어를 사용했으나 Gilbert와 Lynch가 이를 증명할 때는 atomic이라는 용어를 사용했다.
    - 기술적으로 엄밀히 말해서 atomic이라는 단어가 더 적절하다고도 볼 수 있으며 CAP의 consistency는 ACID의 consistency 보다 atomic에 더 가까운 개념이기도 하다.
    - 항상 최신 상태의 data를 읽어와야 하므로 분산 시스템 내의 모든 node들은 동일한 데이터를 가지고 있어야한다.
  - Availability
    - System은 항상 사용 가능한 상태여야 함을 의미한다.
    - 전체 노드가 중지되지 않는 한 system은 항상 사용 가능한 상태여야한다.
  - Partition Tolerance(분할 허용성)
    - Service를 구성하는 모든 node들은 다른 node들과 독립적으로 동작할 수 있어야 한다.
    - 한 node에서 다른 node로 전송되는 message들은 손실될 수 있음 허용한다는 것을 의미한다.
  - Partition Tolerance는 사실상 필수이다.
    - P를 허용하지 않으려면 절대 장애가 발생하지 않는 network를 구축해야한다.
    - 그러나 이는 실제로 존재할 수 없으므로 사실상 P는 선택의 문제가 아니다.
    - 따라서 CAP은 분산 시스템에서 네트워크 장애 상황일 때 일관성과 가용성 중 하나만 선택할 수 있다는 것을 내포하고 있다.
    - 결국 CAP theorem이 궁극적으로 말하고자 하는 바는 네트워크에 장애가 생겼을 때 일관성과 가용성 중 하나만 선택할 수 있다는 것이다.
  - CAP 가설의 증명
    - CAP를 모두 만족하는 분산 시스템 DS가 있다고 가정해보자.
    - DS는 A, B라는 두 개의 노드로 구성되어 있다.
    - 일관성을 충족하므로 A와 B는 동일한 data를 가지고 있으며, 한 node의 변경 사항은 즉시 다른 node에도 반영된다.
    - 이 때 network에 장애가 생겨 A와 B 사이의 통신이 불가능한 상태가 되어 A에서 B로 가는 모든 message는 유실된다(P).
    - 따라서 A는 이후에 B에 쓰기 요청이 있었는지 없었는지 알 수 있는 방법이 없다.
    - 따라서 A로 읽기 요청이 들어왔을 경우 A는 일관성 없는 응답(B와 다를 수 있는 응답)을 반환할 것인지, 아니면 응답을 보내지 않고 가용성을 포기할 것인지를 선택해야만 한다.
  - C와 A를 이분법 적으로 선택해야하는 것은 아니다.
    - 둘 다 조금씩 충족시키거나 하나를 완전히 충족시키고 다른 하나를 조금만 충족시키는 구현 방식도 있을 수 있다.
    - 즉 둘 다 완전히 충족시키는 것은 불가능하나 이를 보완할 수 있는 방법이 없는 것은 아니다.



- PACELC theorem
  - CAP은 사실상 network 장애 상황일 때 분산 시스템 설계자가 일관성과 가용성 중 하나만 선택해야함을 보이는 정리였다.
    - 따라서 정상 상황일 때의 선택에 대해서 잘 설명하지는 못한다.
  - PACELC(Partition)은 분산 시스템을 정상 상황일 때와 장애 상황일 때를 나누어 설명한다.
    - Partition 장애 상황(P)에서는 A와 C 중 하나를 선택해야 한다.
    - 반면에 정상 상황일 경우 L(Latency)과 C(Consistency)중 하나를 선택해야 한다.
    - 모든 node들에 새로운 data를 반영하여 응답을 보내려면 응답 시간(L)이 길어지기 때문이다.



