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
  	
      // 추상 메서드
      void save(Member member);
  
      // Member 클래스의 인스턴스를 반환하는 추상 메서드
      Member findById(Long memberId);
  }
  ```
  
  - db없이 데이터를 메모리상에 저장하기 위한 `MemoryMemberRepository.java` 생성(`MemberRepository`의 구현체)
  
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
  
  public enum Grade {
      BASIC,
      VIP
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

  - `FixDiscountPolicy.java` 생성(`DiscountPolicy`의 구현체)

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



- 여기까지 완료 되었을 때 고정적으로 1000원을 깎아주는 것이 아닌 일정 비율을 할인해 주도록 코드를 변경해야 한다면, 위 코드를 아래와 같이 수정해야 한다.

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
  - 클라이언트인 `OrderServiceImpl.java`는 추상(인터페이스)인 `DiscountPolicy`에 의존함과 동시에 구현인 `FixDiscountPolicy`, `RateDiscountPolicy`에도 의존한다. 따라서 DIP 위반이다.
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
  - 관심사의 분리 참조





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
          //생성자를 통한 의존관계 주입(MemberServiceImpl에 MemoryMemberRepository 객체의 참조값을 주입, 연결)
          //구현 객체를 생성
          return new MemberServiceImpl(new MemoryMemberRepository());
      }
  
      public OrderService orderService(){
          //생성자를 통한 의존관계 주입(OrderServiceImpl MemoryMemberRepository와 FixDiscountPolicy의 객체의 참조값을 주입, 연결)
          //구현 객체를 생성
          return new OrderServiceImpl(new MemoryMemberRepository(),new FixDiscountPolicy());
      }
  }
  ```

  - `MemberServiceImpl.java`

  ```java
  package start.first.member;
  
  public class MemberServiceImpl implements MemberService{
    // 기존에는 아래와 같이 MemberServiceImpl에서 MemberRepository도 의존하고 MemoryMemberRepository에도 의존했다.
    // 이는 배우가 기획과 캐스팅을 하는 것과 마찬가지인 것이다.
    // private final MemberRepository memberRepository = new MemoryMemberRepository();
    private final MemberRepository memberRepository;
  
    // 생성자를 만든다.
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



- 위 `AppConfig.java`의 코드는 관심사를 분리하기 위해 작성하긴 했으나 역할이 잘 드러나고 있다고 보기는 힘들다. 따라서 역할이 더 잘 드러날 수 있도록 코드를 수정해야 한다.

  -  `AppConfig.java`

  ```java
  package start.first;
  
  import start.first.discount.FixDiscountPolicy;
  import start.first.member.MemberService;
  import start.first.member.MemberServiceImpl;
  import start.first.member.MemoryMemberRepository;
  import start.first.order.OrderService;
  import start.first.order.OrderServiceImpl;
  
  
  /* 기존코드
  public class AppConfig {
  
      public MemberService memberService(){
      //intelliJ기준 'new MemoryMemberRepository()' 부분을 드래그 후 ctrl+alt+m을 누르고 memberRepository를 입력후 replace를 누르면
      아래 변경 코드처럼 리팩터링해준다.
          return new MemberServiceImpl(new MemoryMemberRepository());
      }
  
      public OrderService orderService(){
          //생성자 주입(OrderServiceImpl MemoryMemberRepository와 FixDiscountPolicy의 객체의 참조값을 주입, 연결)
          //구현 객체를 생성
          return new OrderServiceImpl(new MemoryMemberRepository(),new FixDiscountPolicy());
      }
  }
  */
  
  //역할이 더 잘 드러나도록 변경된 코드
  public class AppConfig {
  	
      //memberService의 역할
      public MemberService memberService(){
          return new MemberServiceImpl(memberRepository());
      }
  	
      //MemberRepository의 역할, 저장방식을 MemoryMemberRepository로 쓰겠다는 것이 더 잘드러난다.
      //나중에 저장소를 바꿔야 한다면 아래 return 부분만 바꾸면 된다.
      public MemoryMemberRepository memberRepository() {
          return new MemoryMemberRepository();
      }
  
      //orderService의 역할
      public OrderService orderService(){
          return new OrderServiceImpl(memberRepository(),discountPolicy());
      }
      
      //discountPolicy의 역할, 할인 정책을 FixDiscountPolicy를 쓰겠다는 것이 더 잘 드러난다.
      //나중에 할인 정책을 바꿔야 한다면 아래 return 부분만 바꾸면 된다.
      public DiscountPolicy discountPolicy(){
          return new FixDiscountPolicy();
      }
  }
  ```

  - 이제 할인 정책을 바꿔야 한다면 기존과 달리 client 코드는 건들 필요 없이 `AppConfig.java`만 수정하면 된다.

  ```java
  package start.first;
  
  import start.first.discount.FixDiscountPolicy;
  import start.first.discount.RateDiscountPolicy;
  import start.first.member.MemberService;
  import start.first.member.MemberServiceImpl;
  import start.first.member.MemoryMemberRepository;
  import start.first.order.OrderService;
  import start.first.order.OrderServiceImpl;
  
  public class AppConfig {
  	
      public MemberService memberService(){
          return new MemberServiceImpl(memberRepository());
      }
  	
      public MemoryMemberRepository memberRepository() {
          return new MemoryMemberRepository();
      }
  
      public OrderService orderService(){
          return new OrderServiceImpl(memberRepository(),discountPolicy());
      }
  
      public DiscountPolicy discountPolicy(){
          //고정 할인 정책에서
          //return new FixDiscountPolicy();
          //비율 할인 정책으로 변경
          return new FixDiscountPolicy();
      }
  }
  ```





# IoC와 DI와 컨테이너

- 제어의 역전(IoC,Inversion of Control)
  - 일반적으로 개발자가 객체를 생성하고 호출하고 제어하지만 개발자가 제어하지 않고 프레임워크 등이 제어를 하는 것을 제어의 역전이라고 부른다.
  - 기존 프로그램은 클라이언트 구현 객체가 스스로 필요한 서버 구현 객체를 생성하고, 연결하고, 실행했다. 즉, 구현 객체가 프로그램의 제어 흐름을 스스로 조종했다, 개발자 입장에서는 자연스러운 흐름이다.
  - 반면에 `AppConfig`가 등장한 이후에 구현 객체는 자신의 로직을 실행하는 역할만 담당한다. 이제 제어의 흐름은 `AppConfig`가 가져간다. 예를 들어 `OrderServiceImple`은 필요한 인터페이스들을 호출할 뿐 어떤 구현 객체들이 실행될지는 모른다.
  - 프로그램의 제어 흐름에 대한 권한은 모두 `AppConfig`가 가지고 있으며, 심지어 `OrderServiceImpl`조차도 `AppConfig`가 생성한다. 따라서 `AppConfig`는 `OrderServiceImpl`이 아닌 `OrderService` 인터페이스의 다른 구현 객체를 생성하고 실행할 수 도 있다.
  - 이렇듯 프로그램 제어 흐름을 직접 제어하는 것이 아니라 외부에서 관리하는 것을 제어의 역전이라 한다.
  - 프레임 워크와 라이브러리
    - 프레임워크가 내가 작성한 코드를 제어하고, 대신 실행하면 그것은 프레임 워크가 맞다.
    - 내가 작성한 코드가 직접 제어의 흐름을 담당한다면 그것은 프레임 워크가 아니라 라이브러리다.



- 의존관계 주입(Dependency Injection)
  -  `OrderServiceImpl`은 `MemberRepositoty`,  `DiscountPolicy` 인터페이스에 의존한다. 그러나 실제 어떤 구현 객체가 사용될지는 모른다.
  - 의존관계는 정적인 클래스 의존관계와, 실행 시점에서 결정되는 동적인 객체 의존관계를 분리해서 생각해야 한다.
  - 정적인 클래스 의존관계
    - 애플리케이션을 실행하지 않아도 분석할 수 있다.
    - 클래스가 사용하는 import 코드만 보고도 의존관계를 쉽게 파악할 수 있다.
  - 정적인 클래스 의존관계 만으로는 실제 어떤 객체가 `OrderServiceImpl`에 주입될 지 알 수 없다.
  - 동적인 객체 인스턴스  의존 관계
    - 애플리케이션 실행 시점에 실제 생성된 객체 인스턴스의 참조가 연결된 의존 관계
  - 애플리케이션 실행 시점(런타임)에 외부(`AppConfig`)에서 실제 구현 객체를 생성하고 클라이언트에 전달해서 클라이언트와 서버의 실제 의존 관계가 연결되는 것을 **의존관계 주입**이라 한다.
  - 외부(`AppConfig`)에서 객체 인스턴스를 생성하고, 그 참조값을 클라이언트에 전달해서 연결한다.
  - 의존관계 주입을 사용하면 클라이언트 코드를 변경하지 않고, 클라이언트가 호출하는 대상의 타입 인스턴스를 변경할 수 있다.
  - 의존관계 주입을 사용하면 정적인 클래스 의존관계를 변경하지 않고, 동적인 객체 인스턴스 의존관계를 쉽게 변경할 수 있다.



- IoC 컨테이너, DI 컨테이너
  - `AppConfig`와 같이 객체를 생성하고 관리하면서 의존관계를 연결해 주는 것을 IoC 컨테이너 혹은 DI 컨테이너 라고 한다.
  - 의존관계 주입에 초점을 맞춰 최근에는 주로 DI 컨테이너라 한다.
  - 또는 어샘블러, 오브젝토 팩도리 등으로 불리기도 한다.



# 스프링으로 개발하기

## 회원 관리 예제(Spring)

- 순수한 자바 코드로 DI를 적용한 코드를 스프링으로 변경해서 작성한다.



- 변경

  - `AppConfigSpring.java`

  ```java
  package start.first;
  
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  import start.first.discount.DiscountPolicy;
  import start.first.discount.FixDiscountPolicy;
  import start.first.discount.RateDiscountPolicy;
  import start.first.member.MemberService;
  import start.first.member.MemberServiceImpl;
  import start.first.member.MemoryMemberRepository;
  import start.first.order.OrderService;
  import start.first.order.OrderServiceImpl;
  
  //구성 정보, 설정 정보라는 것을 알리기 위해 @Configuration 어노테이션을 달아 준다.
  @Configuration
  public class AppConfigSpring {
  
      //@Bean 어노테이션을 사용하면 스프링 컨테이너에 등록이 된다.
      @Bean
      public MemberService memberService(){
          return new MemberServiceImpl(memberRepository());
      }
  
      @Bean
      public MemoryMemberRepository memberRepository() {
          return new MemoryMemberRepository();
      }
  
      @Bean
      public OrderService orderService(){
          return new OrderServiceImpl(memberRepository(),discountPolicy());
      }
  
      @Bean
      public DiscountPolicy discountPolicy(){
          return new FixDiscountPolicy();
      }
  }
  ```

  - `MemberAppSpring.java`

  ```java
  package start.first.member;
  
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import start.first.AppConfigSpring;
  
  public class MemberAppSpring {
  
      public static void main(String[] args) {
  		
          //컨테이너에 등록하기
          //ApplicationContext를 스프링 컨테이너라고 보면 된다.
          //AnnotationConfigApplicationContext는 @Configuration 어노테이션이 달린 클래스를 관리하기 위해 쓰는 것이고 인자로 구성 정보가 담긴 		   클래스를 받는다.
          //아래 코드가 실행되면 객체들이 생성되어 컨테이너에 등록되고 관리되게 된다.
          ApplicationContext applicationContext = new AnnotationConfigApplicationContext(AppConfigSpring.class);
          
          //등록된 객체(빈) 조회하기
          //getBean은 컨테이너에 등록된 Bean을 가져오는 것으로 첫 번째 인자로 메서드 이름, 두 번째 인자로 타입을 받는다.
          //@Bean 어노테이션의 속성 중 'name=' 이 있는데 이를 등록했다면 등록된 이름으로 하면 된다. 예를 들어 @Bean(name="ms")로 했다면 아래 코			드도 `applicationContext.getBean("ms",MemberService.class)`로 작성하면 된다. 그러나 관례상 바꾸지 않는다.
          MemberService memberService = applicationContext.getBean("memberService",MemberService.class);
          
          //기존의 객체 조회 방법, AppConfig를 사용해서 직접 조회
          /*
          AppConfig appConfig = new AppConfig();
          MemberService memberService = appConfig.memberService();
          OrderService orderService = appConfig.orderService();
          */
          
  
          Member member = new Member(1L,"memberA", Grade.VIP);
          memberService.join(member);
  
          //회원 조회
          Member findMember = memberService.findMember(1L);
          System.out.println("join member: " + member.getName());      //join member: memberA
          System.out.println("find member: " + findMember.getName());  //find member: memberA
      }
  }
  ```

  - 여기까지 변경 후 `MemberAppSpring.java`를 실행하면 아래와 같은 메세지가 터미널에 출력된다.

  ```
  --전략--
  //아래 부분이 스프링 컨테이너에 빈이 등록되는 것이다.
  15:26:22.506 [main] DEBUG org.springframework.beans.factory.support.DefaultListableBeanFactory - Creating shared instance of singleton bean 'appConfigSpring'
  15:26:22.511 [main] DEBUG org.springframework.beans.factory.support.DefaultListableBeanFactory - Creating shared instance of singleton bean 'memberService'
  15:26:22.530 [main] DEBUG org.springframework.beans.factory.support.DefaultListableBeanFactory - Creating shared instance of singleton bean 'memberRepository'
  15:26:22.532 [main] DEBUG org.springframework.beans.factory.support.DefaultListableBeanFactory - Creating shared instance of singleton bean 'orderService'
  15:26:22.533 [main] DEBUG org.springframework.beans.factory.support.DefaultListableBeanFactory - Creating shared instance of singleton bean 'discountPolicy'
  join member: memberA
  find member: memberA
  
  Process finished with exit code 0
  ```

  - `OrderAppSpring`

  ```java
  package start.first.order;
  
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import start.first.AppConfigSpring;
  import start.first.member.Grade;
  import start.first.member.Member;
  import start.first.member.MemberService;
  
  public class OrderAppSpring {
  
      public static void main(String[] args) {
          
          ApplicationContext applicationContext = new AnnotationConfigApplicationContext(AppConfigSpring.class);
          MemberService memberService = applicationContext.getBean("memberService",MemberService.class);
          OrderService orderService = applicationContext.getBean("orderService",OrderService.class);
  
          Long memberId = 1L;
          Member member = new Member(memberId, "memberA", Grade.VIP);
          memberService.join(member);
  
          Order order = orderService.createOrder(memberId,"itemA",10000);
  
          System.out.println("order: " + order);
          System.out.println("calculate price: " + order.calculatePrice());
  
      }
  }
  ```

  



- 코드 설명
  - `AppclicationContext`를 스프링 컨테이너라 한다.
    - 더 정확히는 `BeanFactory`, `ApplicationContext`로 구분하여 스프링 컨테이너를 지칭하지만 `BeanFactory`를 직접 사용하는 경우는 거의 없으므로 일반적으로 `ApplicationContext`를 스프링 컨테이너라 한다.
  - 기존에는 개발자가 `AppConfig`를 통해 직접 객체를 생성하고 DI를 했지만, 이제부터는 스프링 컨테이너를 통해서 사용한다.
  - 스프링 컨테이너는 `@Configuration`이 붙은 `AppConfig`를 설정(구성) 정보로 사용한다. 여기서 `@Bean`이라 적힌 메서드를 모두 호출해서 반환된 객체를 스프링 컨테이너에 등록한다. 그렇게 스프링 컨테이너에 등록된 객체를 스프링 빈이라 한다.
  - 스프링 빈은 `@Bean`이 붙은 메서드의 명을 스프링 빈의 이름으로 사용한다.
  - 이전에는 개발자가 필요한 객체를 `AppConfig`를 사용해서 직접 조회했지만 이제부터는 스프링 컨테이너를 통해서 필요한 스프링 빈(객체)을 찾아야 한다. 스프링 빈은 `applicationContext.getBean()` 메서드를 사용해서 찾을 수 있다.







# 스프링 컨테이너와 스프링 빈

## 스프링 컨테이너 생성

- 스프링 컨테이너의 생성
  - `AppclicationContext`를 통해 생성한다. `AppclicationContext`는 인터페이스로 `AnnotationConfigApplicationContext`는 그 구현체중 하나이다.
  - 스프링 컨테이너는 XML 기반으로 만들 수 있고, 어노테이션 기반의 자바 설정 클래스로 만들 수 있다.
  -  `AppConfigSpring`에서 사용했던 방식이 어노테이션 기반의 자바 설정 클래스로 스프링 컨테이너를 만든 것이다.



- 생성 과정

  - 구성 정보를 인자로 받아 스프링 컨테이너 생성, 컨테이너 내부에서는 스프링 빈 저장소에 `빈 이름:빈 객체` 형식으로 빈을 저장
  - 인자로 받은 구성 정보 중에서 `@Bean`이 붙은 메서드들의 리턴값으로 받은 객체를 스프링 빈 저장소에 등록(빈 이름은 메소드명으로 등록)
    - 주의할 점은 `@Bean` 어노테이션의 속성 중 `name=`을 사용할 경우 빈 이름은 중복되선 안된다.
    - 중복될 경우 다른 빈이 무시되거나, 기존 빈을 덮어버리거나, 설정에 따라 에러가 발생한다.
  - 의존관계 설정
    - 인자로 받은 구성 정보를 참고해서 의존관계를 주입한다.
    - `AppConfigSpring.java` 코드에서 `memberService`는 `memberRepository`에 의존하고, `orderService`는 `memberRepository`와 `discountPolicy`에 의존하는데 이러한 의존관계를 설정한다.

  - 개념적으로는 스프링 빈을 생성하는 단계와 의존관계를 설정하는 단계로 나뉘어져 있다. 
  - 그런데 이렇게 자바 코드로 스프링 빈을 등록하면 생성자를 호출하면서 의존관계 주입도 한번에 처리된다.



## 스프링 빈 조회

- 컨테이너에 등록된 모든 빈 조회

  - `src/test/java/start/first/beanfind`에 `ApplicationContextInfoTest.java` 생성

  ```java
  package start.first.beanfind;
  
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  import org.springframework.beans.factory.config.BeanDefinition;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import start.first.AppConfigSpring;
  
  public class ApplicationContextInfoTest {
  
      AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(AppConfigSpring.class);
  
      @Test
      @DisplayName("모든 빈 출력하기")
      void findAllBean(){
          String[] beanDefinitionNames = ac.getBeanDefinitionNames();
  
          for (String beanDefinitionName : beanDefinitionNames) {
              Object bean = ac.getBean(beanDefinitionName);
              //name은 key, object는 value에 해당
              System.out.println("name = " + beanDefinitionName + " object = " + bean);
          }
      }
      
      //spring 내부에서 등록하는 Bean은 제외하고 내가 등록했거나 외부 라이브러리에서 등록한 Bean만 검색
      @Test
      @DisplayName("애플리케이션 빈 출력하기")
      void findApplicationBean() {
          String[] beanDefinitionNames = ac.getBeanDefinitionNames();
          for (String beanDefinitionName : beanDefinitionNames) {
              BeanDefinition beanDefinition =
                      ac.getBeanDefinition(beanDefinitionName);
              //Role ROLE_APPLICATION: 직접 등록한 애플리케이션 빈
              //Role ROLE_INFRASTRUCTURE: 스프링이 내부에서 사용하는 빈
              //beanDefinition의 역할이 APPLICATION일 때만 출력
              if (beanDefinition.getRole() == BeanDefinition.ROLE_APPLICATION) {
                  Object bean = ac.getBean(beanDefinitionName);
                  System.out.println("name=" + beanDefinitionName + " object=" +
                          bean);
              }
          }
      }
  
  }
  ```



- 빈 타입 혹은 이름으로 조회

  - `.getBean(빈 이름, 빈 타입)`을 사용

  ```java
  package start.first.beanfind;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  import org.springframework.beans.factory.NoSuchBeanDefinitionException;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import start.first.AppConfigSpring;
  import start.first.member.MemberService;
  import start.first.member.MemberServiceImpl;
  
  public class ApplicationContextBasicFindtest {
  
      AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(AppConfigSpring.class);
  
      @Test
      @DisplayName("빈 이름으로 조회하기")
      void findBeanByName(){
          //getBean은 빈 타입만 넘겨도 되고 빈 이름과 타입을 함께 넘겨도 된다.
          MemberService memberService = ac.getBean("memberService",MemberService.class);
          //memberService가 MemberService의 인스턴스면 성공
          Assertions.assertThat(memberService).isInstanceOf(MemberService.class);
      }
  
      @Test
      @DisplayName("이름 없이 타입으로만 조회")
      void findBeanByType(){
          MemberService memberService = ac.getBean(MemberService.class);
          Assertions.assertThat(memberService).isInstanceOf(MemberServiceImpl.class);
      }
  
      @Test
      @DisplayName("구체 타입으로 조회")
      void findBeanByName2(){
          //findBeanByName과 달리 인터페이스인 MemberService가 아닌 구체인 MemberServiceImpl의 타입으로 조회한다.
          //인터페이스가 아닌 구체에 의존하기에 좋은 코드는 아니다. 그러나 필요한 때도 있으므로 구체 타입으로도 조회가 가능하다는 것만 알면 된다.
          MemberService memberService = ac.getBean("memberService",MemberServiceImpl.class);
          Assertions.assertThat(memberService).isInstanceOf(MemberServiceImpl.class);
      }
  
      //실패 테스트, 테스트는 항상 실패 테스트를 함께 만드는 것이 좋다.
      @Test
      @DisplayName("빈 이름으로 조회 실패")
      void findBeanByNameX(){
          //xxxxx라는 이름의 빈이 없으므로 NoSuchBeanDefinitionException예외가 발생
          //ac.getBean("xxxxx",MemberService.class)가 실행될 때 NoSuchBeanDefinitionException예외가 발생하면 성공
          org.junit.jupiter.api.Assertions.assertThrows(NoSuchBeanDefinitionException.class, () -> ac.getBean("xxxxx",MemberService.class));
      }
  }
  ```



- 동일한 타입이 둘 이상일 때 조회

  ```java
  package start.first.beanfind;
  
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  import org.springframework.beans.factory.NoUniqueBeanDefinitionException;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  import start.first.member.MemberRepository;
  import start.first.member.MemoryMemberRepository;
  
  import java.util.Map;
  
  import static org.junit.jupiter.api.Assertions.assertThrows;
  
  public class ApplicationContextSameBeanFindTest {
  
  
      //기존의 AppConfigSpring에는 동알한 타입이 없으므로 SameBeanConfig를 새로 만든다.
      AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(SameBeanConfig.class);
  
      //동일한 타입을 만들기 위한 Config 생성
      @Configuration
      static class SameBeanConfig {
  
          @Bean
          public MemberRepository memberRepository1() {
              return new MemoryMemberRepository();
          }
  
          @Bean
          public MemberRepository memberRepository2() {
              return new MemoryMemberRepository();
          }
  
      }
  
      @Test
      @DisplayName("타입으로 조회시 같은 타입이 둘 이상 있으면, 중복 오류가 발생한다.")
      void findBeanByTypeDuplicate(){
          //아래와 같이 실행할 경우 MemoryMemberRepository 타입에 해당하는 빈이 2개 있으므로 NoUniqueBeanDefinitionException error가 발생
          //MemberRepository memberRepository = ac.getBean(MemberRepository.class);
  
          //따라서 assertThrows를 사용한다.
          assertThrows(NoUniqueBeanDefinitionException.class,()->ac.getBean(MemberRepository.class));
      }
  
      @Test
      @DisplayName("타입으로 조회시 같은 타입이 둘 이상 있으면, 빈 이름을 지정하면 된다.")
      void findBeanByName(){
          MemberRepository memberRepository = ac.getBean("memberRepository1",MemberRepository.class);
          org.assertj.core.api.Assertions.assertThat(memberRepository).isInstanceOf(MemberRepository.class);
      }
  
      @Test
      @DisplayName("같은 타입이 둘 이상 있을 때 특정 타입을 모두 조회하기기")
      void findAllBeanByType(){
          //getBeansOfType을 사용
          Map<String, MemberRepository> beansOfType = ac.getBeansOfType(MemberRepository.class);
          for(String key : beansOfType.keySet()){
              System.out.println("key = " + key +" value = " + beansOfType.get(key));
          }
          System.out.println("beansOfType = " + beansOfType);
          //SameBeanConfig에서 생성한 빈이 2개이므로 beansOfType에 2개가 들어 있다면 성공한 것이다.
          org.assertj.core.api.Assertions.assertThat(beansOfType.size()).isEqualTo(2);
      }
  
  
  }
  ```



- 상속관계 일 때 빈 조회

  - 부모 타입을 조회하면 자식 빈들은 함께 조회 된다.
  - 모든 자바 객체의 부모인 Object 타입으로 조회하면 모든 스프링 빈을 조회한다.

  ```java
  package start.first.beanfind;
  
  import org.junit.jupiter.api.Assertions;
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  import org.springframework.beans.factory.NoUniqueBeanDefinitionException;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  import start.first.discount.DiscountPolicy;
  import start.first.discount.FixDiscountPolicy;
  import start.first.discount.RateDiscountPolicy;
  
  import java.util.Map;
  
  import static org.assertj.core.api.Assertions.assertThat;
  
  public class ApplicationContextExtendsFindTest {
  
      AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(TestConfig.class);
  
      //DiscountPolicy타입으로 조회했을 때 자식 타입인 RateDiscountPolicy와 FixDiscountPolicy가 조회되게 하기 위한 Config를 작성
      @Configuration
      static class TestConfig {
          @Bean
          public DiscountPolicy rateDiscountPolicy() {
              return new RateDiscountPolicy();
          }
  
          @Bean
          public DiscountPolicy fixDiscountPolicy() {
              return new FixDiscountPolicy();
          }
      }
  
      @Test
      @DisplayName("부모 타입으로 조회시 자식이 둘 이상 있으면 중복 에러가 발생")
      void findBeanByParentTypeDuplicate() {
          //아래 코드를 실행하면 NoUniqueBeanDefinitionException 에러가 발생한다.
          //DiscountPolicy bean = ac.getBean(DiscountPolicy.class);
  
          Assertions.assertThrows(NoUniqueBeanDefinitionException.class, () -> ac.getBean(DiscountPolicy.class));
      }
  
      @Test
      @DisplayName("부모 타입으로 자식이 둘 이상 있으면 빈 이름을 지정하면 된다.")
      void findBeanByParentTypeBeanName(){
          DiscountPolicy rateDiscountPolicy = ac.getBean("rateDiscountPolicy",DiscountPolicy.class);
          assertThat(rateDiscountPolicy).isInstanceOf(RateDiscountPolicy.class);
      }
  
      @Test
      @DisplayName("부모 타입으로 자식이 둘 이상 있으면 특정 자식 타입으로 조회해도 된다.")
      //현재 Config에는 부모 타입의 자식 타입 중 중복된 것이 없어 상관이 없으나 자식 타입 중 중복된 것이 있을 경우 에러가 발생할 수 있다.
      //따라서 좋은 방법은 아니다.
      void findBeanBySubType(){
          RateDiscountPolicy bean = ac.getBean(RateDiscountPolicy.class);
          assertThat(bean).isInstanceOf(RateDiscountPolicy.class);
      }
  
      @Test
      @DisplayName("부모 타입으로 모두 조회하기")
      void findAllBeanByParentType(){
          Map<String, DiscountPolicy> beansOfType = ac.getBeansOfType(DiscountPolicy.class);
          assertThat(beansOfType.size()).isEqualTo(2);
          for(String key : beansOfType.keySet()){
              System.out.println("key = " + key +" value = " + beansOfType.get(key));
          }
      }
      
      @Test
      @DisplayName("Object 타입으로 조회해보기")
      //Object는 자바의 모든 객체의 부모이므로 모든 빈이 다 조회된다.
      void findAllBeanByObjectType(){
          Map<String, Object> beansOfType = ac.getBeansOfType(Object.class);
          for(String key : beansOfType.keySet()){
              System.out.println("key = " + key +" value = " + beansOfType.get(key));
          }
      }
  
  }
  ```





## BeanFactory와 ApplicationContext

- BeanFactory나 ApplicationContext를 스프링 컨테이너라 한다.



- BeanFactory
  - 스프링 컨테이너의 최상위 인터페이스
  - 스프링 빈을 관리하고 조회하는 역할을 담당
  - `.getBean()`을 제공한다.
  - 위에서 사용했던 대부분의 기능은 BeanFactory가 제공하는 기능이다.



- ApplicationContext
  - BeanFactory를 상속 받은 인터페이스
  - BeanFactory의 기능을 모두 상속 받아서 제공한다.
  - BeanFactory 외에도 아래와 같은 인터페이스들을 상속받아 수 많은 부가 기능을 제공한다.
    - MessageSource: 메세지 소스를 활용한 국제화 기능, 한국에서 접속하면 한국어로, 외국에서 접속하면 외국어로 출력되는 것이 이를 통해 가능해진다.
    - EnvironmentCapable: 환경 변수 관리, 로컬, 개발, 운영 등을 구분해서 처리
    - ApplicationEventPublisher: 이벤트를 발행하고 구독하는 모델을 편리하게 지원
    - ResourceLoader: 파일, 클래스패스, 외부 등에서 리소스를 편리하게 조회





## 다양한 설정 형식

- 스프링 컨테이너는 자바 코드, XML, Groovy 등 다양한 형식의 설정 정보를 받아드릴 수 있게 유연하게 설계되어 있다.



- 자바 코드
  - 지금까지 했던 것이 애노테이션 기반 자바 코드 설정이다.
  - `AnnotationConfigApplicationContext`를 사용하여 자바 코드로 된 설정 정보를 넘기면 된다.
  - 최근에 많이 사용한다.



- XML

  - 최근에는 스프링 부트를 많이 사용하면서 XML 기반의 설정은 잘 사용하지 않는다.
  - `GenericXmlApplicationContext`를 사용하여 xml 설정 파일을 넘기면 된다.
  - 컴파일 없이 빈 설정 정보를 변경할 수 있는 장점이 있다.
  - `src/main/resources`에 `appConfig.xml` 파일을 생성

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
  
      <!--아래 3줄이 AppConfigSpring에서 memberService를 등록하는 부분에 해당한다.-->
      <bean id="memberService" class="start.first.member.MemberServiceImpl">
          <!--의존성을 작성-->
          <constructor-arg name="memberRepository" ref="memberRepository" />
      </bean>
  
      <!--아래 1줄이 AppConfigSpring에서 memberRepository를 등록하는 부분에 해당한다.-->
      <bean id="memberRepository" class="start.first.member.MemoryMemberRepository" />
  
      <!--아래 3줄이 AppConfigSpring에서 orderService를 등록하는 부분에 해당한다.-->
      <bean id="orderService" class="start.first.order.OrderServiceImpl">
          <!--의존성을 작성-->
          <constructor-arg name="memberRepository" ref="memberRepository" />
          <constructor-arg name="discountPolicy" ref="discountPolicy" />
      </bean>
  
      <bean id="discountPolicy" class="start.first.discount.RateDiscountPolicy" />
  </beans>
  ```

  - test할 파일 작성

  ```java
  package start.first.xml;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.Test;
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.support.GenericXmlApplicationContext;
  import start.first.member.MemberService;
  
  public class XmlAppContext {
  
      @Test
      void xmlAppContext(){
          ApplicationContext ac = new GenericXmlApplicationContext("appConfig.xml");
          MemberService memberService = ac.getBean("memberService", MemberService.class);
          Assertions.assertThat(memberService).isInstanceOf(MemberService.class);
      }
  }
  ```





## 스프링 빈 설정 메타 정보(BeanDefinition)

> 아래 내용은 실무에서도 잘 쓰지 않으므로 이해가 안되면 넘어가도 무방



- BeanDefinition
  - BeanDefinition을 빈 설정 메타정보라 한다.
    - 자바 코드의 `@Bean`, XML의 `<bean>` 하나 당 각각 하나씩 메타 정보가 생성된다.
    - 스프링 컨테이너는 이 메타 정보를 기반으로 스프링 빈을 생성한다.
  - 스프링이 다양한 설정 형식을 지원할 수 있는 것은 BeanDefinition이라는 추상화 덕분이다.
  - BeanDefinition이란 역할과 구현을 개념적으로 나눈 것이라고 할 수 있다.
  - 스프링 컨테이너는 구현이 자바 코드인지, XML 파일인지 몰라도 된다. 오직 BeanDefinition이라는 역할만 알면 된다.
    - XML을 읽어서 BeanDefinition을 만들고
    - 자바 코드를 읽어서 BeanDefinition을 만들면 그만이다.



- 다양한 설정 형식 지원 원리
  - 자바 코드에서 `AnnotationConfigApplicationContext`는 spring에 내장된 `AnnotatedBeanDefinitionReader`를 통해서 `AppConfig.class`를 읽고 BeanDefinition을 생성한다.
  - XML 파일을 사용할 때 `GenericXmlApplicationContext`는  spring에 내장된 `XmlBeanDefinitionReader`를 통해서 `appConfg.xml`을 읽고 BeanDefinition을 생성한다.
  - 따라서 새로운 형식의 설정 정보가 추가되면 `XXXBeanDefinitionReader`를 개발자가 직접 만들어서 BeanDefinition을 생성하면 된다.



- BeanDefinition 정보
  - BeanClassName: 생성할 빈의 클래스명(자바 설정 처럼 팩토리 역할의 빈을 사용하면 없음)
  - factoryBeanName: 팩토리 역할의 빈을 사용할 경우 이름(e.g. appConfig) 
  - factoryMethodName: 빈을 생성할 팩토리 메서드 지정(e.g. memberService) 
  - Scope: 싱글톤(기본값) 
  - lazyInit: 스프링 컨테이너를 생성할 때 빈을 생성하는 것이 아니라, 실제 빈을 사용할 때 까지 최대한 생성을 지연처리 하는지 여부 
  - InitMethodName: 빈을 생성하고, 의존관계를 적용한 뒤에 호출되는 초기화 메서드 명 
  - DestroyMethodName: 빈의 생명주기가 끝나서 제거하기 직전에 호출되는 메서드 명 
  - Constructor arguments, Properties: 의존관계 주입에서 사용한다. (자바 설정 처럼 팩토리 역할 의 빈을 사용하면 없음)



- BeanDefinition 정보 직접 확인해보기

  ```java
  package start.first.beandefinition;
  
  import start.first.AppConfigSpring;
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  import org.springframework.beans.factory.config.BeanDefinition;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  
  
  public class BeanDefinitionTest {
  	
      //자바 코드일 때 메타 정보 확인
      AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(AppConfigSpring.class);
      //XML일 때 메타 정보 확인
      // GenericXmlApplicationContext ac = new GenericXmlApplicationContext("appConfig.xml");
  
      @Test
      @DisplayName("빈 설정 메타정보 확인")
      void findApplicationBean() {
          String[] beanDefinitionNames = ac.getBeanDefinitionNames();
          for (String beanDefinitionName : beanDefinitionNames) {
              BeanDefinition beanDefinition =
                      ac.getBeanDefinition(beanDefinitionName);
              if (beanDefinition.getRole() == BeanDefinition.ROLE_APPLICATION) {
                  System.out.println("beanDefinitionName" + beanDefinitionName +
                          " beanDefinition = " + beanDefinition);
              }
          }
      }
  }
  
  //out
  //전략
  beanDefinitionNameappConfigSpring beanDefinition = Generic bean: class [start.first.AppConfigSpring$$EnhancerBySpringCGLIB$$b0b643e9]; scope=singleton; abstract=false; lazyInit=null; autowireMode=0; dependencyCheck=0; autowireCandidate=true; primary=false; factoryBeanName=null; factoryMethodName=null; initMethodName=null; destroyMethodName=null
  //후략
  ```

  





