# 순수 자바로만 개발하기

## 회원 관리 예제

- 요구사항

  - 회원을 가입하고 조회할 수 있다.

  - 회원은 일반과 VIP 두 가지 등급이 있다.
  - 회원 데이터는 자체 DB를 구축할 수 있고, 외부 시스템과 연동할 수 있다(미확정).



- 개발

  - member 패키지 생성 후 `Member.java`를 생성

  ```java
  package start.first.member;
  
  public class Member {
      private Long id;
      private String name;
      private Grade grade;
      
      //IntelliJ기준 아래 코드들은 alt+insert 로 생성 가능하다.
      //생성자
      public Member(Long id, String name, Grade grade) {
          this.id = id;
          this.name = name;
          this.grade = grade;
      }
  
      //getter/setter
      public Long getId() {
          return id;
      }
  
      public String getName() {
          return name;
      }
  
      public Grade getGrade() {
          return grade;
      }
  
      public void setId(Long id) {
          this.id = id;
      }
  
      public void setName(String name) {
          this.name = name;
      }
  
      public void setGrade(Grade grade) {
          this.grade = grade;
      }
  }
  
  ```

  -  `Grade.java`를 enum으로 생성

  ```java
  package start.first.member;
  
  public enum Grade {
      BASIC,
      VIP
}
  ```

  - `MemberRepository.java` 를 인터페이스로 생성
  
  ```java
  package start.first.member;
  
  public interface MemberRepository {
  
      void save(Member member);
  
      Member findById(Long memberId);
  
  ```

}
  ```

  - db없이 데이터를 메모리상에 저장하기 위한 `MemoryMemberRepository.java` 생성
  
  ```java
  package start.first.member;
  
  import java.util.HashMap;
  import java.util.Map;
  
  public class MemoryMemberRepository implements MemberRepository{
  	
      //임시 db의 역할을 할 Map을 생성
      private static Map<Long,Member> store = new HashMap<>();
  
      @Override
      public void save(Member member) {
          store.put(member.getId(), member);
      }
  
      @Override
      public Member findById(Long memberId) {
          return store.get(memberId);
    }
  }
  ```

  - `MemberService.java`를 interface로 생성

  ```java
  package start.first.member;
  
  public interface MemberService {
      void join(Member member);
    Member findMember(Long memberId);
  }
  ```

  - `MemberService.java`의 구현체인 `MemberServiceImpl.java`를 생성

  ```java
  package start.first.member;
  
  public class MemberServiceImpl implements MemberService{
  
      private final MemberRepository memberRepository = new MemoryMemberRepository();
  
      @Override
      public void join(Member member) {
          memberRepository.save(member);
      }
  
      @Override
      public Member findMember(Long memberId) {
          return memberRepository.findById(memberId);
    }
  }
  ```




- 테스트

  - 방법1. `MemberApp.java` 클래스를 생성 후 실행

  ```java
  package start.first;
  
  import start.first.member.Grade;
  import start.first.member.Member;
  import start.first.member.MemberService;
  import start.first.member.MemberServiceImpl;
  
  public class MeberApp {
      //IntelliJ 기준 psvm을 치면 아래와 같은 main의 구조가 잡힌다.
      public static void main(String[] args) {
          //회원 가입
          MemberService memberService = new MemberServiceImpl();
          Member member = new Member(1L,"memberA", Grade.VIP);
          memberService.join(member);
          
          //회원 조회
          Member findMember = memberService.findMember(1L);
          System.out.println("join member: " + member.getName());      //join member: memberA
          System.out.println("find member: " + findMember.getName());  //find member: memberA
      }
  }
  ```

  - 방법2. `src.test.java.start.first.member`에 `MemberTest.java` 생성

  ```java
  package start.first.member;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.Test;
  
  public class MemberServiceTest {
  
      MemberService memberService = new MemberServiceImpl();
      
      //@Test 어노테이션을 달고
      //아래 메서드를 실행했을 때 에러가 나지 않으면 정상적으로 테스트가 완료된 것이다.
      @Test
      void join(){
          //given: 무엇이 주어졌을 때
          Member member = new Member(1L,"memberA",Grade.VIP);
  
          //when: 무엇을 하면
          memberService.join(member);
          Member findMember = memberService.findMember(1L);
  
          //then: 어떻게 되는가
          Assertions.assertThat(member).isEqualTo(findMember);
      }
  }
  ```

  

- 위 코드의 문제점

  - 의존관계가 인터페이스 뿐만 아니라 구현까지 모두 의존하는 문제점이 존재.
    - DIP를 위반하고 있다.
  - `MemberServiceImpl.java`

  ```java
  package start.first.member;
  
  public class MemberServiceImpl implements MemberService{
  	
      //아래 부분에서 private final MemberRepository memberRepository는 추상화(인터페이스)에 의존하고
      //new MemoryMemberRepository() 부분은 구현체에 의존하고 있다.
      private final MemberRepository memberRepository = new MemoryMemberRepository();
  
      @Override
      public void join(Member member) {
          memberRepository.save(member);
      }
  
      @Override
      public Member findMember(Long memberId) {
          return memberRepository.findById(memberId);
      }
  }
  ```





## 주문과 할인 예제

- 요구사항
  - 회원은 상품을 주문할 수 있다.
  - 회원 등급에 따라 할인 정책을 적용할 수 있다.
  - 할인 정책은 모든 VIP에게  1000원을 할인해주는 정책이다.
  - 할인 정책은 변경 가능성이 높으며 최악의 경우 할인을 적용하지 않을 수 도 있다.



- 개발

  - discount 패키지 생성
  - `DiscountPolicy.java` 생성

  ```java
  package start.first.discount;
  
  import start.first.member.Member;
  
  public interface DiscountPolicy {
  
      int discount(Member member, int price);
  }
  ```

  - `FixDiscountPolicy.java` 생성

  ```java
  package start.first.discount;
  
  import start.first.member.Grade;
  import start.first.member.Member;
  
  public class FixDiscountPolicy implements DiscountPolicy{
  
      private int discoutFixAmount = 1000;
  
      @Override
      public int discount(Member member, int price) {
          //enum은 ==을 사용하여 비교한다.
          if(member.getGrade()== Grade.VIP){
              return discoutFixAmount;
          }else{
              return 0;
          }
  
      }
  }
  ```

  - order 패키지 생성
  - `Order.java` 생성

  ```java
  package start.first.order;
  
  public class Order {
  
      private Long memberId;
      private String itemName;
      private int itemPrice;
      private int discountPrice;
      
      //생성자
      public Order(Long memberId, String itemName, int itemPrice, int discountPrice) {
          this.memberId = memberId;
          this.itemName = itemName;
          this.itemPrice = itemPrice;
          this.discountPrice = discountPrice;
      }
      
      //할인가 계산
      public int calculatePrice(){
          return itemPrice-discountPrice;
      }
  
      //출력용 메서드, alt+insert 버튼을 누르고 toString을 선택하면 자동생성 해준다.
      @Override
      public String toString() {
          return "Order{" +
                  "memberId=" + memberId +
                  ", itemName='" + itemName + '\'' +
                  ", itemPrice=" + itemPrice +
                  ", discountPrice=" + discountPrice +
                  '}';
      }
  
      //getter/setter
      public Long getMemberId() {
          return memberId;
      }
  
      public void setMemberId(Long memberId) {
          this.memberId = memberId;
      }
  
      public String getItemName() {
          return itemName;
      }
  
      public void setItemName(String itemName) {
          this.itemName = itemName;
      }
  
      public int getItemPrice() {
          return itemPrice;
      }
  
      public void setItemPrice(int itemPrice) {
          this.itemPrice = itemPrice;
      }
  
      public int getDiscountPrice() {
          return discountPrice;
      }
  
      public void setDiscountPrice(int discountPrice) {
          this.discountPrice = discountPrice;
      }
  }
  ```



- 테스트

  - 방법1: `OrderApp.java` 

  ```java
  package start.first.order;
  
  import start.first.member.Grade;
  import start.first.member.Member;
  import start.first.member.MemberService;
  import start.first.member.MemberServiceImpl;
  
  public class OrderApp {
      public static void main(String[] args) {
          MemberService memberService = new MemberServiceImpl();
          OrderService orderService = new OrderServiceImpl();
  
          Long memberId = 1L;
          Member member = new Member(memberId, "memberA", Grade.VIP);
          memberService.join(member);
  
          Order order = orderService.createOrder(memberId,"itemA",10000);
  
          System.out.println("order: " + order);
          //order: Order{memberId=1, itemName='itemA', itemPrice=10000, discountPrice=1000}
  		System.out.println("calculate price: " + order.calculatePrice());
          //calculate price: 9000
      }
  }
  ```

  - 방법2: `OrderServiceTest.java`

  ```java
  package start.first.order;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.Test;
  import start.first.member.Grade;
  import start.first.member.Member;
  import start.first.member.MemberService;
  import start.first.member.MemberServiceImpl;
  
  public class OrderServiceTest {
  
      MemberService memberService = new MemberServiceImpl();
      OrderService orderService = new OrderServiceImpl();
  
      @Test
      void createOrder(){
          Long memberId = 1L;
          Member member = new Member(memberId,"memberA", Grade.VIP);
          memberService.join(member);
  
          Order order = orderService.createOrder(memberId,"item1",10000);
          Assertions.assertThat(order.getDiscountPrice()).isEqualTo(1000);
  
      }
  }
  ```

  

- 여기까지 완료 되었을 때 고정적으로 1000원을 깎아주는 것이 아닌 일정 비율을 할인해 주도록 코드를 변경해야 한다면 위 코드를 아래와 같이 수정해야 한다.

  - `rateDiscountPolicy.java`

  ```java
  package start.first.discount;
  
  import start.first.member.Grade;
  import start.first.member.Member;
  
  public class RateDiscountPolicy implements DiscountPolicy{
  
      private int discountPercent = 10;
  
      @Override
      public int discount(Member member, int price) {
          if(member.getGrade()== Grade.VIP){
              return price*discountPercent/100;
          }else{
              return 0;
          }
      }
  }
  ```

  

- 테스트

  - `rateDiscountPolicyTest.java`

  ```java
  package start.first.discount;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  import start.first.member.Grade;
  import start.first.member.Member;
  
  class RateDiscountPolicyTest {
  
      RateDiscountPolicy discountPolicy = new RateDiscountPolicy();
      
      //성공 테스트
      @Test
      //JUnit5에서 제공하는 기능으로 터미널 창에 아래 작성한 내용으로 테스트명이 출력된다.
      @DisplayName("VIP는 10% 할인이 적용되어야 합니다.")
      void dis(){
          //given
          Member member = new Member(1L,"memberVIP", Grade.VIP);
  
          //when
          int discount = discountPolicy.discount(member,10000);
  
          //then
          Assertions.assertThat(discount).isEqualTo(1000);
      }
  
      //실패 테스트
      @Test
      @DisplayName("VIP가 아니면 할인이 적용되지 않아야 한다.")
      void dontDis(){
          //given
          //VIP가 아닌 BASIC으로 생성
          Member member = new Member(2L,"memberBASIC", Grade.BASIC);
  
          //when
          int discount = discountPolicy.discount(member,10000);
  
          //then
          //VIP가 아니므로 1000원이 아닌 0원이 되어야 한다.
          Assertions.assertThat(discount).isEqualTo(1000);
      }
      //위 실패 테스트를 진행하면 에러 메세지 아래에 아래와 같이 뜬다.
      //Expected :1000
  	//Actual   :0
  }
  ```

  

- 변경된 할인 정책 적용

  - `OrderServiceImpl.java`

  ```java
  package start.first.order;
  
  import start.first.discount.DiscountPolicy;
  import start.first.discount.FixDiscountPolicy;
  import start.first.discount.RateDiscountPolicy;
  import start.first.member.Member;
  import start.first.member.MemberRepository;
  import start.first.member.MemoryMemberRepository;
  
  public class OrderServiceImpl implements OrderService{
      private final MemberRepository memberRepository = new MemoryMemberRepository();
  	
      //고정 할인에서
      //private final DiscountPolicy discountPolicy = new FixDiscountPolicy();
      //비울 할인으로 수정
      private final DiscountPolicy discountPolicy = new RateDiscountPolicy();
  
      @Override
      public Order createOrder(Long memberId, String itemName, int itemPrice) {
          Member member = memberRepository.findById(memberId);
          int discountPrice = discountPolicy.discount(member, itemPrice);
          return new Order(memberId,itemName,itemPrice,discountPrice);
      }
  }
  
  ```



- 문제점
  - OCP, DIP와 같은 객체 지향 설계 원칙을 준수하지 못했다.
  - 클라이언트인 `OrderServiceImpl.java`는 추상(인터페이스)인 `DiscountPolicy`에 의존함과 동시에 구현인 `FixDiscountPolicy`, `RateDiscountPolicy`에도 의존한다. 따라서 DCP 위반이다.
  - 위에서 변경된 할인 정책을 적용하기 위해서는 추상인 `DiscountPolicy`를 확장하여 `RateDiscountPolicy`를 생성하는 것에서 그치는 것이 아니라 클라이언트에 해당하는 `OrderServiceImpl.java` 도 함께 수정해야 했다. 따라서 OCP위반이다.



- 해결과 그에 따른 또 다른 문제점

  - `OrderServiceImpl`이 `DiscountPolicy`에만 의존하도록 변경
  - `OrderServiceImpl.java`

  ```java
  package start.first.order;
  
  import start.first.discount.DiscountPolicy;
  import start.first.discount.FixDiscountPolicy;
  import start.first.discount.RateDiscountPolicy;
  import start.first.member.Member;
  import start.first.member.MemberRepository;
  import start.first.member.MemoryMemberRepository;
  
  public class OrderServiceImpl implements OrderService{
      private final MemberRepository memberRepository = new MemoryMemberRepository();
  //    private final DiscountPolicy discountPolicy = new FixDiscountPolicy();
  //    private final DiscountPolicy discountPolicy = new RateDiscountPolicy();
      //아래와 같이 추상에만 의존하도록 변경
      private DiscountPolicy discountPolicy;
      //그러나 이 코드를 실행하면 구현이 존재하지 않기에 `NullPointException` error가 발생한다.
  
      @Override
      public Order createOrder(Long memberId, String itemName, int itemPrice) {
          Member member = memberRepository.findById(memberId);
          int discountPrice = discountPolicy.discount(member, itemPrice);
          //구현이 존재하지 않기에 위 코드가 아래 코드와 같아진다.
          //int discountPrice = null.discount(member, itemPrice);
          //null에 discoumt라는 메소드는 존재하지 않으므로 error가 발생
          return new Order(memberId,itemName,itemPrice,discountPrice);
      }
  }
  ```



- 완전한 해결법
  - 누군가가 클라이언트인 `OrderServiceImpl`에 `DiscountPolicy`의 구현 객체를 대신 생성하고 주입해주어야 한다.
  - 아래 관심사의 분리 파트 참조





## 관심사의 분리

- 관심사 분리의 필요성

  - 애플리케이션을 하나의 공연으로 보고, 인터페이스를 배역, 구현을 배우라고 가정했을 때, 기존의 순수 자바로만 개발한 코드는 배우가 공연 기획도 하고, 캐스팅도 하고, 직접 연기도 하는 코드라고 할 수 있다. 
  - 배우는 본인의 역할인 배역만을 수행해야 하고 다른 배역에 어떤 배우가 캐스팅 되더라도 똑같이 공연을 수행할 수 있어야 한다. 그러기 위해서는 별도의 공연 기획자가 필요하다.

  - 실제로 `OrderServiceImpl.java`에서 `OrderServiceImpl`는 `OrderServiceImpl`의 역할만 수행하는 것이 아니라, 직접 `discountPolicy`의 객체를 생성하고,  할인 정책이 변경될 때마다 코드도 변경해줬어야 했다.

  - 애플리케이션의 공연 기획자에 해당하는 것이 `AppConfig`이다. 



- AppConfig

  - 애플리케이션의 전체 동작 방식을 구성(config)하기 위해, 구현 객체를 생성하고 연결하는 책임을 가지는 별도의 설정 클래스
  - `AppConfig.java`

  ```java
  package start.first;
  
  import start.first.discount.FixDiscountPolicy;
  import start.first.member.MemberService;
  import start.first.member.MemberServiceImpl;
  import start.first.member.MemoryMemberRepository;
  import start.first.order.OrderService;
  import start.first.order.OrderServiceImpl;
  
  public class AppConfig {
  
      public MemberService memberService(){
          //MemoryMemberRepository를 MemberServiceImpl이 넣어주는 것이 아니라 여기서 넣어준다.
          //생성자 주입(MemberServiceImpl에 MemoryMemberRepository 객체의 참조값을 주입, 연결)
          //구현 객체를 생성
          return new MemberServiceImpl(new MemoryMemberRepository());
      }
  
      public OrderService orderService(){
          //생성자 주입(OrderServiceImpl MemoryMemberRepository와 FixDiscountPolicy의 객체의 참조값을 주입, 연결)
          //구현 객체를 생성
          return new OrderServiceImpl(new MemoryMemberRepository(),new FixDiscountPolicy());
      }
  }
  ```

  - `MemberServiceImpl.java`

  ```java
  package start.first.member;
  
public class MemberServiceImpl implements MemberService{
  
    //기존에는 아래와 같이 MemberServiceImpl에서 MemberRepository도 의존하고 MemoryMemberRepository에도 의존했다.
      //이는 배우가 기획과 캐스팅을 하는 것과 마찬가지인 것이다.
      //private final MemberRepository memberRepository = new MemoryMemberRepository();
      private final MemberRepository memberRepository;

      //생성자를 만든다.
      public MemberServiceImpl(MemberRepository memberRepository) {
          this.memberRepository = memberRepository;
      }
  
      @Override
      public void join(Member member) {
          memberRepository.save(member);
      }
  
      @Override
      public Member findMember(Long memberId) {
          return memberRepository.findById(memberId);
      }
  }
  ```
  
  - `OrderServiceImpl.java`
  
  ```java
  package start.first.order;
  
  import start.first.discount.DiscountPolicy;
  import start.first.discount.FixDiscountPolicy;
  import start.first.discount.RateDiscountPolicy;
  import start.first.member.Member;
  import start.first.member.MemberRepository;
  import start.first.member.MemoryMemberRepository;
  
  public class OrderServiceImpl implements OrderService{
      //기존 코드
      //private final MemberRepository memberRepository = new MemoryMemberRepository();
      //private final DiscountPolicy discountPolicy = new FixDiscountPolicy();
      //private final DiscountPolicy discountPolicy = new RateDiscountPolicy();
  
      //변경한 코드
      private final MemberRepository memberRepository;
      private final DiscountPolicy discountPolicy;
  
      //생성자
      public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  
      @Override
      public Order createOrder(Long memberId, String itemName, int itemPrice) {
          Member member = memberRepository.findById(memberId);
          int discountPrice = discountPolicy.discount(member, itemPrice);
          return new Order(memberId,itemName,itemPrice,discountPrice);
      }
  }
  ```
  
  - 이제 `MemberServiceImpl`,  `OrderServiceImpl`는 더 이상 객체에 의존하지 않는다. 이들의 입장에서 생성자를 통해 어떤 구현 객체가 주입될지는 알 수 없다. 이는 오직 `AppConfig`에서 결정되며, 이들은 의존 관계에 대한 고민은 `AppConfig`에 맡기고 실행에만 집중하면 된다(관심사의 분리).
  - 의존성 주입(Dependency Injection)
    - `MemberServiceImpl`,  `OrderServiceImpl`의 입장에서 보면 의존관계를 마치 외부에서 주입해주는 것과 같다고 해서 의존관계 주입, 혹은 의존성 주입이라 한다.

