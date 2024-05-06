# 의존 관계 자동 주입

## 다양한 의존관계 주입 방법

- 의존관계 주입은 크게 4가지 방법이 있다.
  - 생성자 주입
  - 수정자 주입(setter 주입)
  - 필드 주입
  - 일반 메서드 주입



- 생성자 주입

  - 생성자를 통해서 의존관계를 주입 받는 방법
  - 특징
    - 생성자 호출시점에 딱 1번만 호출되는 것이 보장된다.
    - 불변, 필수 의존관계에 주로 사용한다.
  - 코드
    - 아래 코드에서 `OrderServiceImpl`이 스프링 빈으로 등록될 때 생성자가 호출되게 된다.
    - 생성자에 `@Autowired`가 있으므로 스프링 컨테이너에서 `MemberRepository`, `DiscountPolicy`를 꺼내서 `OrderServiceImpl`에 주입한다.
    - 생성자가 딱 1개만 있으면 `@Autowired`를  **생략**해도 자동 주입 된다. 물론 스프링 빈에만 해당한다(따라서 아래 코드에서는 사실 `@Autowired`를 굳이 적어줄 필요가 없다).
    - 지금까지 앞에서 사용했던 방법이 `@Autowired`가 생략된 생성자 주입이다.
  
  ```java
  // 전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      private final DiscountPolicy discountPolicy;
  
      @Autowired
      public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  }
  ```



- 수정자 주입(setter 주입)

  - setter라 불리는 필드의 값을 변경하는 수정자 메서드를 통해 의존관계를 주입하는 방법
  - 특징
    - 선택, 변경 가능성이 있는 의존관계에 사용
    - 자바빈 프로퍼티 규약(필드의 값을 직접 변경하지 않고 setX, getX라는 매서드를 통해 값을 조회하거나 수정하는 규칙을 만들었는데 이를 자바빈 프로퍼티 규약이라 한다)의 수정자 메서드 방식을 사용하는 방법이다.

  - 코드
    - `OrderServiceImpl`이 컨테이너에 등록된다.
    - `@Autowired`가  있는 것들을 찾아서 의존관계를 자동으로 주입한다.

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private MemberRepository memberRepository;
      private DiscountPolicy discountPolicy;
  	
      //아래와 같이 주입을 위한 setter를 만들고, @Autowired를 붙여준다.
      @Autowired
      public void setMemberRepository(MemberRepository memberRepository){
          this.memberRepository = memberRepository;
      }
  
      @Autowired
      public void setDiscountPolicy(DiscountPolicy discountPolicy){
          this.discountPolicy = discountPolicy;
      }
  }
  ```



- 필드주입

  - 이름 그대로 필드에 바로 주입하는 방법
  - 특징
    - 코드가 간결해 많은 개발자를 유혹하지만 외부에서 변경이 불가능해 테스트 하기 힘들다는 치명적인 단점이 존대
    - DI 프레임 워크가 없으면 아무것도 할 수 없다.
    - 사용하지 말자, 애플리케이션의 실제 코드와 상관이 없는 테스트 코드, 스프링 설정을 목적으로 하는 `@Configuration`등에만 선택적으로 사용하자.
  - 코드
    - 2군데를 수정해야 한다.

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      @Autowired private MemberRepository memberRepository;
      @Autowired private DiscountPolicy discountPolicy;
  }
  ```

  ```java
  //AppConfigSpring
  //전략
  
  @Configuration
  public class AppConfigSpring {
  
  	//중략
  
      @Bean
      public OrderService orderService(){
          //return을 null로 변경해준다.
          //return new OrderServiceImpl(memberRepository(),discountPolicy());
          return null;
      }
  	
      //후략
  }
  ```



- 일반 메서드 주입

  - 일반 메서드를 통해서 주입 받을 수 있다.
  - 특징
    - 한번에 여러 필드를 주입 받을 수 있다.
    - 일반적으로 잘 사용하지 않는다.
  - 코드

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private MemberRepository memberRepository;
      private DiscountPolicy discountPolicy;
  
      @Autowired
      public void init(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  }
  ```







## 옵션 처리

- 주입할 스프링 빈이 없어도 동작해야 할 때가 있다. 그런데 `@Autowired`만 사용하면 `required` 옵션의 기본값이 `true`로 되어 있어 자동 주입 대상이 없으면 오류가 발생한다.



- 자동 주입 대상을 옵션으로 처리하는 방법은 다음과 같다.
  - `@Autowired(required=false)`를 사용하여 자동 주입할 대상이 없으면 수정자 메서드 자체가 호출이 안되게 한다.
  - `org.springframeword.lang.@Nullable`: 자동 주입할 대상이 없으면 null이 입력된다.
  - `Optional<>`: 자동 주입할 대상이 없으면 `Optional.empty`가 입력된다.



- 코드

  ```java
  //전략
  
  public class AutowiredTest {
  
      @Test
      void AutowiredOption(){
          ApplicationContext ac = new AnnotationConfigApplicationContext(TestBean.class);
      }
  
      static class TestBean{
  
          //Member는 spring bean으로 등록하지 않았으므로 테스트에 적합
          
          //방법1.@Autowired(required=false)
          @Autowired(required = false)
          public void setNoBean1(Member noBean1){
              System.out.println("noBean1 = " + noBean1);
          }
  
          //방법2.org.springframeword.lang.@Nullable
          @Autowired
          public void setNoBean2(@Nullable Member noBean2){
              System.out.println("noBean2 = " + noBean2);
          }
  
          //방법3.Optional<>
          @Autowired
          public void setNoBean3(Optional<Member> noBean3){
              System.out.println("noBean3 = " + noBean3);
          }
      }
  }
  
  //out
  //noBean1은 setNoBean1 메서드 자체가 호출이 안된다.
  noBean2 = null  //호출은 되지만 null이 입력
  noBean3 = Optional.empty //Optional.empty가 입력
  ```







## 생성자 주입을 선택해야만 하는 이유

- 과거에는 수정자 주입과 필드 주입을 많이 사용했지만, 최근에는 스프링을 포함한 DI 프레임워크 대부분이 생성자 주입을 권장한다.
  - 항상 생성자 주입을 선택하라
  - 가끔 옵션이 필요하다면 수정자 주입을 선택하라
  - 필드 주입은 사용하지 않는 것이 좋다.



- 권장하는 이유

  - 불변
    - 대부분의 의존관계 주입은 한번 일어나면 애플리케이션 종료시점까지 의존관계를 변경할 일이 없다. 오히려 대부분의 의존관계는 애플리케이션 종료 전까지 변하면 안된다.
    - 수정자 주입을 사용하면 setXxx 메서드를 public으로 열어둬야 한다.
    - 누군가 실수로 변경할 수 도 있고, 변경하면 안되는 메서드를 열어두는 것은 좋은 설계 방법이 아니다.
    - 생성자 주입은 객체를 생성할 때 딱 1번만 호출되므로 이후에 호출되는 일이 없다. 따라서 불변하게 설계할 수 있다.

  - 누락
    - 프레임워크 없이 순수한 자바 코드를 단위 테스트 하는 경우 문제가 될 수 있다.
    - 아래와 같이 수정자 주입을 사용한 코드를 단위 테스트하고자 했을 때 에러가 발생할 수 있다. 이는 의존관계를 일일이 setter로 넣어주는 과정에서 빠지는 것이 생길 수 있기 때문이다. 
    - 반면에 생성자로 할 경우 의존관계를 처음부터 넣어줘야 하기 때문에 위와 같은 에러가 발생할 일이 없다.

  ```java
  //setter로 의존성 주입
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private MemberRepository memberRepository;
      private DiscountPolicy discountPolicy;
  
      @Autowired
      public void setMemberRepository(MemberRepository memberRepository){
          this.memberRepository = memberRepository;
      }
  
      @Autowired
      public void setDiscountPolicy(DiscountPolicy discountPolicy){
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

  ```java
  package start.first.order;
  
  import org.junit.jupiter.api.Test;
  
  public class OrderServiceImplTest {
  
      @Test
      void createOrder(){
          OrderServiceImpl orderService = new OrderServiceImpl();
          orderService.createOrder(1L,"itemA",10000);
      }
  }
  
  //NullPointerException에러가 발생하는데 OrderServiceImpl에서 memberRepository, discountPolicy의 값을 setter로 세팅해 준 적이 없기 때문이다. 이 경우 컴파일 에러가 발생하지 않기에 실행할 때까지 잘못 되었다는 것을 알 수 없다.
  ```

  ```java
  //생성자 주입
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      private final DiscountPolicy discountPolicy;
  
      @Autowired
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

  ```java
  //전략
  
  public class OrderServiceImplTest {
  
      @Test
      void createOrder(){
          //아래 두 줄은 회원을 생성하는 코드로, member가 없을 경우 에러가 발생해서 만든 것으로, 없어도 의존관계로 인한 에러는 발생하지 않는다.
          MemoryMemberRepository memoryMemberRepository = new MemoryMemberRepository();
          memoryMemberRepository.save(new Member(1L,"userA", Grade.VIP));
          
          //생성할 때 의존관계를 주입한다.
          //만일 아래와 같은 코드를 작성할 경우 IntelliJ에서부터 빨간줄이 쳐져 바로 알 수 있다.
          //OrderServiceImpl orderService = new OrderServiceImpl();
          OrderServiceImpl orderService = new OrderServiceImpl(new MemoryMemberRepository(), new FixDiscountPolicy());
          Order order = orderService.createOrder(1L,"itemA",10000);
          Assertions.assertThat(order.getDiscountPrice()).isEqualTo(1000);
      }
  }
  ```

  - final 키워드를 사용할 수 있다.
    - 생성자 주입을 사용하면 필드에 final 키워드를 사용할 수 있는데, 이는 생성자에서 혹시라도 값이 설정되지 않는 오류를 커파일 시점에서 막아준다.
    - 생성자 주입을 제외한 모든 주입 방식은 모두 생성자 이후에 호출되므로, 필드에 `final`키워드를 사용할 수 없다.

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      private final DiscountPolicy discountPolicy;
  
      //아래와 같이 한 가지를 누락하면 컴파일 에러가 발생한다(IntelliJ에서 빨간줄이 쳐지는 것을 확인 가능하다).
      @Autowired
      public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
  		this.memberRepository = memberRepository;
          //this.discountPolicy = discountPolicy가 누락되어 있다.
      }
  }
  ```







## 롬복과 최신 트랜드

- 생성자 주입으로 해야 하는 이유를 위에서 살펴보았는데, 다른 주입 방식에 비해 코드가 길다는 단점이 존재한다. 
  - 따라서 코드를 최적화 해야한다.



- 최적화

  - 기본 코드

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      private final DiscountPolicy discountPolicy;
  
      @Autowired
      public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
  		this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy
      }
  }
  ```

  - 생성자가 단 하나만 있으면 `@Autowired`를 생략 가능하다.
  - lombok을 사용
    - build.gradle에 아래 코드를 추가한다.
    - Plugins에서 lombok을 설치한다. 
    - Settings- Build,Execution,Deployment-Compiler-Annotation Processors에서 Enable annotation processing을 체크한다.

  ```java
  plugins {
  	id 'org.springframework.boot' version '2.3.2.RELEASE'
  	id 'io.spring.dependency-management' version '1.0.9.RELEASE'
  	id 'java'
  }
  
  group = 'hello'
  version = '0.0.1-SNAPSHOT'
  sourceCompatibility = '11'
  
  //lombok 설정 추가 시작
  configurations {
  	compileOnly {
  		extendsFrom annotationProcessor
  	}
  }
  //lombok 설정 추가 끝
  
  repositories {
  	mavenCentral()
  }
  
  dependencies {
  	implementation 'org.springframework.boot:spring-boot-starter'
  	//lombok 라이브러리 추가 시작
  	compileOnly 'org.projectlombok:lombok'
  	annotationProcessor 'org.projectlombok:lombok'
  	testCompileOnly 'org.projectlombok:lombok'
  	testAnnotationProcessor 'org.projectlombok:lombok'
  	//lombok 라이브러리 추가 끝
  	testImplementation('org.springframework.boot:spring-boot-starter-test') {
  		exclude group: 'org.junit.vintage', module: 'junit-vintage-engine'
  	}
  }
  
  test {
  	useJUnitPlatform()
  }
  ```

  ```java
  //lombok 예시
  //아래와 같이 getter, setter를 비롯한 많은 코드를 코드 작성 없이 사용할 수 있게 해준다.
  package start.first;
  
  
  import lombok.Getter;
  import lombok.Setter;
  
  @Getter
  @Setter
  public class HelloLombok {
  
      private String name;
      private int age;
  
      public static void main(String[] args) {
          HelloLombok helloLombok = new HelloLombok();
          helloLombok.setName("asd");
          
          String name = helloLombok.getName();
          System.out.println("name = " + name);
      }
  }
  ```

  - lombok을 사용하여 최적화된 코드

  ```java
  //전략
  
  @Component
  @RequiredArgsConstructor //이 어노테이션을 사용하면 final이 붙은 필드들을 모아서 생성자를 자동으로 만들어준다.
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      private final DiscountPolicy discountPolicy;
  
  }
  ```







## 조회 되는 빈이 2개 이상일 경우

- `@Autowired`는 타입으로 조회하는데, 앞서 학습했듯 타입으로 조회하면 선택된 빈이 2개 이상일 경우 문제가 발생한다.



- 문제
  - `DiscountPolicy`의 하위 타입인 `FixDiscountPolicy`, `RateDiscountPolicy` 둘 다 스프링 빈으로 선언한 후 의존관계 자동 주입을 실행하면 `NoUniqueBeanDefinitionException` 에러가 발생한다. 자세히 보면 다음과 같은 문구를 확인 가능하다. `expected single matching bean but found 2: fixDiscountPolicy,rateDiscountPolicy`.
  - 이 때 하위 타입으로 지정할 수도 있지만 이는 DIP를 위배하고 유연성이 떨어진다. 그리고 이름만 다르고, 완전히 똑같은 타입의 스프링 빈이 2개 있을 때 해결이 안된다.



- 해결

  - @Autowired 필드 명(혹은 파라미터 명) 매칭
    - @Autowired는 타입 매칭을 시도하고, 이 때 여러 빈이 있으면 필드 이름 또는 파라미터 이름으로 빈 이름을 추가 매칭한다.

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      //DiscountPolicy는 2개가 있어 에러가 발생해야하지만 이 방법을 적용하면 발생하지 않는다.
      private final DiscountPolicy discountPolicy;
  
      @Autowired
      //아래와 같이 파라미터명을 rateDiscountPolicy로 명시해준다. 필드 주입도 마찬가지로 필드에 이름을 명시해주면 된다.
      public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy rateDiscountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = rateDiscountPolicy;
      }
  }
  ```

  - @Quilifier -> @Quilifier끼리 매칭 -> 빈 이름 매칭
    - 추가 구분자를 붙여주는 방법.
    - 주입시 추가적인 방법을 제공하는 것이지 빈 이름을 변경하는 것은 아니다.
    - 만일 지정해준 이름을 못 찾을 경우(아래 예시에서 mainDiscountPolicy를 못 찾을 경우) 이름에 해당하는 스프링 빈을 추가로 찾는다. 그러나 @Quilifier는 @Quilifier를 찾는 용도로만 사용하는 것이 좋다.

  ```java
  //RateDiscountPolicy.java
  @Component
  @Qualifier("mainDiscountPolicy")
  public class RateDiscountPolicy implements DiscountPolicy{
      //중략
  }
  
      
      
  //FixDiscountPolicy.java
  @Component
  @Qualifier("fixDiscountPolicy")
  public class FixDiscountPolicy implements DiscountPolicy{
      //중략
  }
  ```

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      //DiscountPolicy는 2개가 있어 에러가 발생해야하지만 이 방법을 적용하면 발생하지 않는다.
      private final DiscountPolicy discountPolicy;
  
      @Autowired
      //아래와 같이 @Qualifier를 사용하여 어떤 빈인지 명시해준다. 마찬가지로 필드 주입, 수정자 주입에도 사용할 수 있다.
      public OrderServiceImpl(MemberRepository memberRepository, @Qualifier("mainDiscountPolicy") DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  }
  ```

  - @Primary 사용
    - 우선 순위를 정하는 방법이다. @Autowired시에 여러 빈이 매칭되면 @Primary가 우선권을 가진다.

  ```java
  //RateDiscountPolicy.java
  @Component
  @Primary  //@Primary를 추가한다.
  public class RateDiscountPolicy implements DiscountPolicy{
      //중략
  }
  
      
  //FixDiscountPolicy.java
  @Component
  public class FixDiscountPolicy implements DiscountPolicy{
      //중략
  }
  ```

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      //DiscountPolicy는 2개가 있어 에러가 발생해야하지만 이 방법을 적용하면 발생하지 않는다.
      private final DiscountPolicy discountPolicy;
  
      @Autowired
      //이번에는 아무 처리도 하지 않아도 에러가 발생하지 않는다.
      public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  }
  ```



- @Quilifier와 @Primary의 우선권
  - 스프링은 일반적으로 자동보다는 수동이, 넓은 범위의 선택권 보다는 좁은 범위의 선택권이 우선 순위가 높다.
  - 따라서 @Quilifier가 우선 순위가 높다.







## 애노테이션 직접 만들기

- `@Qualifier("mainDiscountPolicy")`와 같이 사용할 때 문제는 인자로 넘기는 값이 문자열이기 때문에 컴파일시에 체크가 안된다는 점이다. 따라서 오타를 낼 경우 체크가 되지 않는다. 따라서 에러가 발생하도록 하려면 아래와 같이 사용해야 한다.



- 해결

  - 어노테이션 파일을 하나 만든다.

  ```java
  package start.first.annotation;
  
  import org.springframework.beans.factory.annotation.Qualifier;
  
  import java.lang.annotation.*;
  
  //@Qualifier 내부에 있는 어노테이션들이다.
  @Target({ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER, ElementType.TYPE, ElementType.ANNOTATION_TYPE})
  @Retention(RetentionPolicy.RUNTIME)
  @Inherited
  @Documented
  @Qualifier("mainDiscountPolicy")
  public @interface MainDiscountPolicy {
      
  }
  ```

  - 위에서 만든 어노테이션을 적용한다.

  ```java
  //RateDiscountPolicy.java
  @Component
  @MainDiscountPolicy
  public class RateDiscountPolicy implements DiscountPolicy{
      //중략
  }
  ```

  - 사용할 곳에도 추가해준다.

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      //DiscountPolicy는 2개가 있어 에러가 발생해야하지만 이 방법을 적용하면 발생하지 않는다.
      private final DiscountPolicy discountPolicy;
  
      @Autowired
      //아래와 같이 @MainDiscountPolicy를 추가해준다.
      public OrderServiceImpl(MemberRepository memberRepository, @MainDiscountPolicy DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  }
  ```



- 본래 어노테이션은 상속이라는 개념이 없다. 여러 어노테이션을 모아서 사용하는 기능은 스프링이 지원해주는 기능이다.
  - @Qualifier 뿐만 아니라 다른 어노테이션들도 함께 조합해서 사용할 수 있다.
  - 물론 스프링이 제공하는 기능을 뚜렷한 목적 없이 무분별하게 재정의 하는 것은 유지보수에 혼란을 가중시키므로 주의해야 한다.





## 조회한 빈이 모두 필요할 때 List와 Map

- 의도적으로 특정 타입의 스프링 빈이 다 필요한 경우가 있다. 예를 들어 할인 서비스를 제공할 때 클라이언트가 할인의 종류를 선택할 수 있다고 하면 이를 간단하게 구현할 수 있다.

  ```java
  //전략
  
  public class AllBeanTest {
  
      @Test
      void findAllBean(){
          ApplicationContext ac = new AnnotationConfigApplicationContext(AutoAppConfig.class, DiscountService.class);
  
          DiscountService discountService = ac.getBean(DiscountService.class);
          Member member = new Member(1L,"userA", Grade.VIP);
          int discountPrice = discountService.discount(member, 10000, "fixDiscountPolicy");
  
          Assertions.assertThat(discountService).isInstanceOf(DiscountService.class);
          Assertions.assertThat(discountPrice).isEqualTo(1000);
  
          int ratediscountPrice = discountService.discount(member, 20000, "rateDiscountPolicy");
          Assertions.assertThat(ratediscountPrice).isEqualTo(2000);
      }
  
      static class DiscountService{
          private final Map<String, DiscountPolicy> policyMap;
          private final List<DiscountPolicy> policyList;
  
          @Autowired
          public DiscountService(Map<String, DiscountPolicy> policyMap, List<DiscountPolicy> policyList) {
              this.policyMap = policyMap;
              this.policyList = policyList;
              System.out.println("policyMap = " + policyMap);
              System.out.println("policyList = " + policyList);
          }
  		
          //policyMap에는 fixDiscountPolicy, rateDiscountPolicy의 2개의 빈이 담겨 있다.
          public int discount(Member member, int price, String discountCode) {
              //인자로 넘어온 discountCode로 policyMap라는 맵의 key에 해당하는 빈을 찾는다.
              DiscountPolicy discountPolicy = policyMap.get(discountCode);
              //위에서 찾은 빈이 discountPolicy가 되고 이에 따라 할인율이 다르게 적용되게 된다.
              return discountPolicy.discount(member,price);
          }
      }
  }
  
  
  //out
  policyMap = {fixDiscountPolicy=start.first.discount.FixDiscountPolicy@1b2c4efb, rateDiscountPolicy=start.first.discount.RateDiscountPolicy@c35172e}
  policyList = [start.first.discount.FixDiscountPolicy@1b2c4efb, start.first.discount.RateDiscountPolicy@c35172e]
  ```







## 자동과 수동의 올바른 실무 운영 기준

- 편리한 자동 기능을 기본으로 사용한다.
  - 스프링이 나오고 시간이 갈 수록 점점 더 자동을 선호하는 추세다.
  - 최근 스프링 부트는 컴포넌트 스캔을 기본으로 사용하고, 스프링 부트의 다양한 스프링 빈들도 조건이 맞으면 자동으로 등록하도록 설계했다.
  - 결정적으로 자동 빈 등록을 사용해도 OCP, DIP를 지킬 수 있다,



- 수동 빈 등록은 언제 사용하면 좋은가

  - 애플리케이션은 크게 업무 로직과 기술 지원 로직으로 나눌 수 있다.
  - 업무 로직 빈: 웹을 지원하는 컨트롤러, 핵심 비즈니스 로직이 있는 서비스, 데이터 계층의 로직을 처리하는 리포지토리등이 모두 업무 로직이다. 보통 비즈니스 요구사항을 개발할 대 추가되거나 변경된다.
    - 숫자도 매우 많고, 한번 개발할 때 컨트롤러, 서비스, 리포지토리처럼 어느정도 유사한 패턴이 있다.
    - 보통 문제가 발생했을 때 어떤 곳에서 문제가 발생했는지 명확하게 파악하기 쉽다.
    - 이 경우 자동 기능를 적극 활용하는 것이 좋다.

  - 기술 지원 빈: 기술적인 문제나 공통 관심사(AOP)를 처리할 때 주로 사용된다. 데이터베이스 연결이나 공통 로그 처리처럼 업무 로직을 지원하기 위한 하부 기술이나 공통 기술들이다.
    - 업무 로직에 비해 숫자가 매우 적고, 보통 애플리케이션 전반에 걸쳐 광범위하게 영향을 미친다.
    - 업무 로직에 비해 문제가 발생했을 때 어디가 문제인지 잘 드러나지 않고, 잘 적용이 되고 있는지도 파악이 어렵다.
    - 따라서 기술 지원 로직들은 가급적 수동 빈 등록을 사용해서 명확하게 하는 것이 좋다.
  - 비즈니스 로직 중에서 다형성을 적극 활용할 때
    - 이 경우 수동으로 등록하는 것이 낫다
    - 자동으로 등록하더라도 특정 패키지에 같이 묶어 두는 것이 좋다.
    - 예시로 fixDiscountPolicy와 rateDiscountPolicy가 있는데 코드를 짠 자신은 이 빈들이 어떻게 주입되는지 알 수 있지만 코드를 짜지 않은 다른 사람이 볼 때 완전히 이해하기 위해서는 관련된 모든 코드를 다 봐야 한다. 따라서 아래와 같이 설정 정보를 만들어서 수동으로 등록하거나 최소한 한 패키지에 묶어 놔야 한다.

  ```java
  @Configuration
  public class DiscountPolicyConfig {
  
       @Bean
       public DiscountPolicy rateDiscountPolicy() {
       	return new RateDiscountPolicy();
       }
      
       @Bean
       public DiscountPolicy fixDiscountPolicy() {
       	return new FixDiscountPolicy();
       }
  }
  ```



- 스프링과 스프링 부트가 자동으로 등록하는 수 많은 빈들은 가급적 스프링의 의도대로 자동으로 사용하는 것이 좋다.
  - 스프링이 자동으로 등록할 메뉴얼을 참고해서 경우 자동으로 등록되도록 두는 것이 좋다.
  - 스프링이 아니라 내가 직접 기술 지원 객체를 스프링 빈으로 등록할 때는 수동으로 등록해서 보다 명확하게 드러내는 것이 좋다.







# 빈 생명주기 콜백

## 빈 생명주기 콜백 시작

- 데이터베이스 커넥션 풀이나, 네트워크 소켓처럼 애플리케이션 시작 시점에 필요한 연결을 미리 해두고, 애플리케이션 종료 시점에 연결을 모두 종료하는 작업을 진행하려면, 객체의 초기화와 종료 작업이 필요하다.



- 스프링 빈의 이벤트 라이프 사이클
  - 스프링 컨테이너 생성
  - 스프링 빈 생성
  - 의존관계 주입(수정자 주입, 필드 주입의 경우에 해당, 생성자 주입은 빈이 생성될 때 주입이 함께 일어남)
  - 초기화 콜백(사용할 수 있는 준비가 모두 끝난 상태)
  - 사용
  - 소멸전 콜백(빈이 소멸되기 직전에 호출)
  - 스프링 종료



- 객체의 생성과 초기화를 분리해야 한다.
  - 생성자는 필수 정보(파라미터)를 받고, 메모리를 할당해서 객체를 생성하는 책임을 가진다.
  - 반면에 초기화는 이렇게 생성된 값들을 활용하여 외부 커넥션을 연결하는등 무거운 동작을 수행한다.
  - 따라서 생성자 안에서 무거운 초기화 작업을 함께 하는 것 보다는 객체를 생성하는 부분과 초기화 하는 부분을 명확하게 나누는 것이 유지보수 관점에서 좋다. 물론 초기화 작업이 내부 값들만 약간 변경하는 정도로 단순한 경우에는 생성자에서 한번에 다 처리하는 것이 더 나을 수 도 있다.



- 네트워크에 미리 연결하는 객체를 하나 생성한다고 가정한 예시(실제 네트워크에 연결하는 것은 아니다)

  - 서버가 뜰 때 미리 외부 네트워크와 연결되어야 한다.
  - 서버가 종료될 때 미리 외부 네트워크와 연결이 끊어져야 한다.
  - 코드

  ```java
  package start.first.lifecycle;
  
  public class NetworkClient {
  
      private String url;
  
      public NetworkClient(){
          System.out.println("생성자 호출, url = " + url);
          connect();
          call("초기화 연결 메세지");
      }
  
      public void setUrl(String url){
          this.url = url;
      }
  
      //서비스 시작시 호출
      public void connect(){
          System.out.println("connect " + url);
      }
      
      //연결이 된 상태
      public void call(String message){
          System.out.println("call: " + url + " message = " + message);
      }
  
      //서비스 종료시 호출
      public void disconnect(){
          System.out.println("close " + url);
      }
      
  }
  ```

  - 테스트

  ```java
  //전략
  
  public class BeanLifeCycleTest {
  
      @Test
      public void lifeCycleTest(){
          //close를 사용하기 위해서는 ConfigurableApplicationContext 타입이어야 한다.
          //ConfigurableApplicationContext는 ApplicationContext를 상속 받는다.
          //AnnotationConfigApplicationContext는 ConfigurableApplicationContext를 상속 받는다.
          ConfigurableApplicationContext ac = new AnnotationConfigApplicationContext(LifeCycleConfig.class);
          NetworkClient client = ac.getBean(NetworkClient.class);
          ac.close();
      }
  
      @Configuration
      static class LifeCycleConfig{
          @Bean
          public NetworkClient networkClient(){
              NetworkClient networkClient = new NetworkClient();  //객체 생성
              networkClient.setUrl("http://hello-word.dev");		//수정자를 통한 의존관계 주입
              return networkClient;
          }
      }
  }
  
  //out
  생성자 호출, url = null  //url이 null이 뜬다. 만일 실제 연결하려 했다면, url이 잘못 되었으므로 연결 되지 않았을 것이다.
  connect null
  call: null message = 초기화 연결 메세지
  ```

  - 실행 결과를 보면 null이 라고 출력 되는데, 그 이유는 객체를 생성하고 의존관계가 주입되기 때문이다.

    - 스프링 빈은 기본적으로 객체 생성 후 의존관계가 주입된다(생성자 주입은 예외).
    - 스프링 빈은 객체를 생성하고, 의존관계 주입이 다 끝난 다음에야 필요한 데이터를 사용할 수 있는 준비가 완료된다.
    - 따라서 초기화 작업(외부 네트워크와 연결하는 작업)은 의존관계 주입이 모두 완료되고 난 다음에 호출해야 한다.
    - 그렇다면 개발자가 의존관계 주입이 모두 완료된 시점을 어떻게 알 수 있는가?



- 스프링의 빈 생명주기 콜백 지원
  - 인터페이스
  - 설정 정보에 초기화 메서드, 종료 메서드 지정
  - @PostConstruct, @PreDestroy 애노티에션 지원





## 인터페이스(InitializingBean DisposableBean)

- 초기화, 소멸 인터페이스를 상속 받아서 사용한다.



- 코드(기존의 NetworkClient 코드에 추가)

  ```java
  package start.first.lifecycle;
  
  import org.springframework.beans.factory.DisposableBean;
  import org.springframework.beans.factory.InitializingBean;
  
  //InitializingBean(연결이 시작될 때 사용), DisposableBean(연결이 끊어질 때 사용)을 상속 받는다.
  public class NetworkClient implements InitializingBean, DisposableBean {
  
      private String url;
  
      public NetworkClient(){
          System.out.println("생성자 호출, url = " + url);
          connect();
          call("초기화 연결 메세지");
      }
  
      public void setUrl(String url){
          this.url = url;
      }
  
      //서비스 시작시 호출
      public void connect(){
          System.out.println("connect " + url);
      }
      
      //연결이 된 상태
      public void call(String message){
          System.out.println("call: " + url + " message = " + message);
      }
  
      //서비스 종료시 호출
      public void disconnect(){
          System.out.println("close " + url);
      }
  
      @Override
      //InitializingBean에 있는 메서드를 상속받아 사용하는 것이다.
      //의존관계 주입이 끝나면 호출할 메서드
      public void afterPropertiesSet() throws Exception {
          System.out.println("NetworkClient.afterPropertiesSet 호출");
          connect();
          call("초기화 연결 메세지");
      }
  
      @Override
      //DisposableBean에 있는 메서드를 상속받아 사용하는 것이다.
      //연결이 끝어지면 호출할 메서드
      public void destroy() throws Exception {
          System.out.println("NetworkClient.destroy 호출");
          disconnect();
      }
  }
  ```



- 테스트(기존의 BeanLifeCycleTest를 그대로 사용)

  - 테스트 결과 null값이던 주소가 제대로 들어가는 것을 확인할 수 있다.

  ```java
  //out
  생성자 호출, url = null
  connect null
  call: null message = 초기화 연결 메세지
  NetworkClient.afterPropertiesSet 호출
  connect http://hello-word.dev  //주소가 제대로 들어가있다.
  call: http://hello-word.dev message = 초기화 연결 메세지
  16:18:33.361 [main] DEBUG org.springframework.context.annotation.AnnotationConfigApplicationContext - Closing org.springframework.context.annotation.AnnotationConfigApplicationContext@4a7f959b, started on Sat Dec 05 16:18:33 KST 2020
  NetworkClient.destroy 호출
  close http://hello-word.dev
  ```



- 위와 같은 초기화, 소멸 인터페이스의 단점
  - 스프링 전용 인터페이스로, 해당 코드가 스프링 전용 인터페이스에 의존하게 된다.
  - 초기화, 소멸 메서드의 이름(`afterPropertiesSet`, `destroy`)을 변경할 수 없다.
  - 내가 코드를 고칠 수 없는 외부 라이브러리에 적용할 수 없다.
  - 이 방법은 스프링 초창기에 나온 방법들이고, 지금은 더 나은 방법들이 있어서 거의 사용하지 않는다.





## 빈 등록 초기화, 소멸 메서드

- 설정 정보에 `@Bean(initMethod = "init", destroyMethod = "close")`처럼 초기화, 소멸 메서드를 지정할 수 있다.



- 코드

  ```java
  //전략
  
  public class NetworkClient{
      private String url;
  
      public NetworkClient(){
          System.out.println("생성자 호출, url = " + url);
          connect();
          call("초기화 연결 메세지");
      }
  
      public void setUrl(String url){
          this.url = url;
      }
  
      //서비스 시작시 호출
      public void connect(){
          System.out.println("connect " + url);
      }
      
      //연결이 된 상태
      public void call(String message){
          System.out.println("call: " + url + " message = " + message);
      }
  
      //서비스 종료시 호출
      public void disconnect(){
          System.out.println("close " + url);
      }
  
      public void init() throws Exception {
          System.out.println("NetworkClient.init 호출");
          connect();
          call("초기화 연결 메세지");
      }
  
      public void close() throws Exception {
          System.out.println("NetworkClient.close 호출");
          disconnect();
      }
  }
  ```



- 테스트

  ```java
  package start.first.lifecycle;
  
  import org.junit.jupiter.api.Test;
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.ConfigurableApplicationContext;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  
  public class BeanLifeCycleTest {
  
      @Test
      public void lifeCycleTest(){
          ConfigurableApplicationContext ac = new AnnotationConfigApplicationContext(LifeCycleConfig.class);
          NetworkClient client = ac.getBean(NetworkClient.class);
          ac.close();
      }
  
      @Configuration
      static class LifeCycleConfig{
  
          //아래와 같이 Bean의 속성값으로 시작 메서드와 종료 메서드를 문자열로 지정해준다.
          @Bean(initMethod = "init", destroyMethod = "close")
          public NetworkClient networkClient(){
              NetworkClient networkClient = new NetworkClient();
              networkClient.setUrl("http://hello-word.dev");
              return networkClient;
          }
      }
  }
  ```



- 설정 정보 사용 장점
  - 메서드 이름을 자유롭게 줄 수 있다.
  - 스프링 빈이 스프링 코드에 의존하지 않는다.
  - 코드가 아니라 설정 정보를 사용하기에 코드를 고칠 수 없는 외부 라이브러리에도 초기화, 종료 메서드를 적용할 수 있다(라이브러리에서 사용한 초기화, 종료 메서드명을 입력해주기만 하면 된다).



- 종료 메서드 추론
  - `@Bean`의 `destroyMethod` 속성에는 특별한 기능이 있다.
  - 내부 코드를 보면 기본 값이 `"(inferred)"`(추론)라고 되어 있는 것이 확인 가능한데, 라이브러리는 대부분 `close`, `shutdown`이라는 이름의 종료 메서드를 사용한다.
  - 기본 값인 `"(inferred)"`는 `close`, `shutdown`라는 이름의 메서드를 자동으로 호출해준다. 이름 그대로 종료 메서드를 추론해서 호출해준다.
  - 따라서 직접 스프링 빈으로 등록하면 종료 메서드는 따로 적어주지 않아도 잘 동작한다.
  - 추론 기능을 사용하기 싫으면 `destroyMethod=""`처럼 빈 공백을 지정하면 된다.





## 에노테이션 PostConstruct과 PreDestroy

- 위에서 살펴본 2가지 방법 대신 이 방법을 사용하면 된다. 스프링에서도 이 방법을 사용하는 것을 권장한다.



- 코드

  ```java
  //전략
  
  public class NetworkClient{
      private String url;
  
      public NetworkClient(){
          System.out.println("생성자 호출, url = " + url);
          connect();
          call("초기화 연결 메세지");
      }
  
      public void setUrl(String url){
          this.url = url;
      }
  
      //서비스 시작시 호출
      public void connect(){
          System.out.println("connect " + url);
      }
      
      //연결이 된 상태
      public void call(String message){
          System.out.println("call: " + url + " message = " + message);
      }
  
      //서비스 종료시 호출
      public void disconnect(){
          System.out.println("close " + url);
      }
  	
      //초기화 메서드를 단다.
      @PostConstruct
      public void init() throws Exception {
          System.out.println("NetworkClient.init 호출");
          connect();
          call("초기화 연결 메세지");
      }
  	
      //종료 메서드를 단다.
      @PreDestroy
      public void close() throws Exception {
          System.out.println("NetworkClient.close 호출");
          disconnect();
      }
  }
  ```



- 테스트

  - 위에서 사용한 테스트에서 `@Bean(initMethod = "init", destroyMethod = "close")` 만 `@Bean`으로 변경하면 된다.
  - 제대로 적용 되는 것을 확인 가능하다.



- @PostConstruct, @PreDestroy의 특징
  - 최신 스프링에서 가장 권장하는 방법.
  - 어노테이션 하나만 붙이면 되므로 매우 편리하다.
  - import할 때 패키지를 잘 보면 `import javax.annotation.xxx`이다. 스프링에 종속적인 기술이 아니라 JSR-250이라는 자바 표준이다. 따라서 스프링이 아닌 다른 컨테이너에서도 동작한다.
  - 컴포넌트 스캔과 잘 어울린다.
  - 유일한 단점은 외부 라이브러리에는 적용하지 못한다는 것이다. 외부 라이브러리를 초기화, 종료 해야하면 @Bean의 기능(빈 등록 초기화, 소멸 메서드)을 사용하자.





# 빈 스코프

## 빈 스코프

- 빈 스코프란
  - 지금까지 우리는 스프링 빈이 스프링 컨테이너의 시작과 함께 생성되어 스프링 컨테이너가 종료될 때 까지 유지된다고 학습했다.
  - 이는 스프링 빈이 기본적으로 싱글톤 스코르로 생성되기 때문이다.
  - 스코프는 번역 그대로 빈이 존재할 수 있는 범위를 뜻한다.



- 스프링은 다음과 같은 다양한 스코프를 지원한다.
  - 싱글톤: 기본 스코프, 스프링 컨테이너의 시작과 종료까지 유지되는 가장 넓은 범위의 스코프였다.
  - 프로토타입: 스프링 컨테이너는 프로토타입 빈의 생성과 의존관계 주입까지만 관여하고 더는 관리하지 않는 매우 짧은 범위의 스코프이다.
  - 웹 관련 스코프
    - `request`: 웹 요청이 들어오가 나갈때 까지 유지되는 스코프.
    - `sessiong`: 웹 세션이 생성되고 종료될 때 까지 유지되는 스코프
    - `application`: 웹의 서블릿 컨텍스와 같은 범위로 유지되는 스코프이다.



- 빈 스코프는 지정 방법

  - 컴포넌트 스캔의 경우

  ```java
  @Scope("prototype")
  @Component
  public class SomeBean(){}
  ```

  - 수동 등록의 경우

  ```java
  @Scope("prototype")
  @Bean
  PrototypeBean SomeBean(){
      return new SomeBean();
  }
  ```





## 프로토 타입 스코프

- 싱글톤 스코프(기본 스코프)의 빈을 조회하면 스프링 컨테이너는 항상 같은 인스턴스의 스프링 빈을 반환한다. 반면에 프로토타입 스코프를 스프링 컨테이너에 조회하면 스프링 컨테이너는 항상 새로운 인스턴스를 생성해서 반환한다.

  - 클라이언트가 싱글톤 스코프의 빈을 스프링 컨테이너에 요청하면, 스프링 컨테이너는 본인이 관리하는 스프링 빈을 반환한다.
  - 이후에 스프링 컨테이너에 다른 클라이언트로부터 같은 요청이 와도 같은 객체 인스턴스의 스프링 빈을 반환한다. 
  - 즉 3명의 클라이언트가 동일한 요청을 보내면, 동일한 빈을 반환 받는다.

  ```java
  //전략
  
  public class SingletoneTest {
  
      @Test
      void singletonBeanFind(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(SingletonBean.class);
  
          SingletonBean singletonBean1 = ac.getBean(SingletonBean.class);
          SingletonBean singletonBean2 = ac.getBean(SingletonBean.class);
          System.out.println("singletonBean1 = " + singletonBean1);
          System.out.println("singletonBean2 = " + singletonBean2);
          Assertions.assertThat(singletonBean1).isSameAs(singletonBean2);
  
          ac.close();
      }
  
      //디폴트값이므로 굳이 @Scope를 적어주지 않아도 된다.
      @Scope("singleton")
      static class SingletonBean {
  
          @PostConstruct
          public void init() {
              System.out.println("SingletoBean.init 호출");
          }
  
          @PreDestroy
          public void destroy() {
              System.out.println("SingletonBean.destroy 호출");
          }
  
      }
  }
  
  //out
  SingletoBean.init 호출  //init이 먼저 호출되어 빈을 생성한다.
  singletonBean1 = start.first.scope.SingletoneTest$SingletonBean@609db546
  singletonBean2 = start.first.scope.SingletoneTest$SingletonBean@609db546
  21:14:05.474 [main] DEBUG org.springframework.context.annotation.AnnotationConfigApplicationContext - Closing org.springframework.context.annotation.AnnotationConfigApplicationContext@3e84448c, started on Sat Dec 05 21:14:05 KST 2020
  SingletonBean.destroy 호출
  ```





- 프로토 타입 빈의 경우

  - 각기 다른 3명의 클라이언트가 프로토타입 스코프의 빈을 스프링 컨테이너에 요청하면 스프링 컨테이너는 이 시점에 프로토타입 빈을 생성하고, 필요한 의존관계를 주입한다.
  - 즉 요청이 올 때마다 새로운 빈을 생성하고 의존관계를 주입하며, 반환 후에는 더 이상 관리하지 않는다.
  - 결국 3명의 클라이언트 모두 같은 요청을 보내도 각기 다른 빈을 반환받게 된다.'
  - 핵심은 스프링 컨테이너는 프로토타입 빈을 생성하고, 의존관계 주입, 초기화까지만 처리한다는 것이다.  클라이언트에 빈을 반환하고, 이후 스프링 컨테이너는 생성된 프로토타입 빈을 관리하지 않는다. 프로토타입빈을 관리할 책임은 프로토타입 빈을 받은 클라이언트에 있다. 그래서 `@Predestroy` 같은 종료 메서드가 호출되지 않는다.

  ```java
  //전략
  
  public class PrototypeScope {
  
      @Test
      void prototypeBeanFind(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(PrototypeBean.class);
  
          System.out.println("find prototypeBean1");
          PrototypeBean prototypeBean1 = ac.getBean(PrototypeBean.class);
          System.out.println("find prototypeBean2");
          PrototypeBean prototypeBean2 = ac.getBean(PrototypeBean.class);
          System.out.println("prototypeBean1 = " + prototypeBean1);
          System.out.println("prototypeBean2 = " + prototypeBean2);
  
          Assertions.assertThat(prototypeBean1).isNotSameAs(prototypeBean2);
      }
  
      @Scope("prototype")
      static class PrototypeBean {
  
          @PostConstruct
          public void init() {
              System.out.println("PrototypeBean.init 호출");
          }
  
          @PreDestroy
          public void destroy() {
              System.out.println("PrototypeBean.destroy 호출");
          }
      }
  }
  
  //out
  find prototypeBean1  //이게 먼저 출력 되고
  PrototypeBean.init 호출  //init이 호출된다. 즉, 호출 될 때마다 빈을 생성하는 것이다.
  find prototypeBean2  //마찬가지로 이게 먼저 호출 되고
  PrototypeBean.init 호출 //init이 호출된다.
  prototypeBean1 = start.first.scope.PrototypeScope$PrototypeBean@609db546
  prototypeBean2 = start.first.scope.PrototypeScope$PrototypeBean@20f5281c  //서로 다른 주소가 나온다.
  //destroy는 호출되지 않는다.
  ```



- 정리

  - 싱글톤 빈은 스프링 컨테이너 생성 시점에 초기화 메서드(init)가 실행되지만, 프로토타입 스코프의 빈은 스프링 컨테이너에서 빈을 조회할 때 생성되고, 초기화 메서드도 실행된다.
  - 프로토타입 빈을 2번 조회했으므로 완전히 다른 스프링 빈이 생성되고, 초기화도 2번 실행된 것을 확인할 수 있다.
  - 싱글톤 빈은 스프링 컨테이너가 관리하기에, 스프링 컨테이너가 종료될 때 빈의 종료 메서드(destroy)가 실행되지만, 프로토타입 빈은 스프링 컨테이너가 생성과 의존관계 주입, 그리고 초기화 까지만 관여하고, 더는 관리하지 않는다. 따라서 프로토타입 빈은 스프링 컨테이너가 종료될 때 `@PreDestroy` 같은 종료 메서드가 전혀 실행되지 않는다.
  - 만일 종료 메서드를 호출하고 싶으면 아래와 같이 직접 호출해야 한다.

  ```java
  //전략
  
  public class PrototypeScope {
  
      @Test
      void prototypeBeanFind(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(PrototypeBean.class);
          
          PrototypeBean prototypeBean1 = ac.getBean(PrototypeBean.class);
          PrototypeBean prototypeBean2 = ac.getBean(PrototypeBean.class);
  
          Assertions.assertThat(prototypeBean1).isNotSameAs(prototypeBean2);
          //아래와 같이 직접 호출해야 한다.
          prototypeBean1.destroy();
          prototypeBean2.destroy();
      }
  
  //후략
  ```





## 싱글톤 빈과 프로토 타입 빈을 함께 사용시 발생하는 문제

- 스프링 컨테이너에 프로토타입 스코프의 빈을 요청하면 항상 새로운 객체 인스턴스를 생성해서 반환한다. 하지만 싱글톤 빈과 함께 사용할 때는 의도한 대로 잘 동작하지 않으므로 주의해야 한다.

  - 클라이언트 A가 count라는 필드를 가지고 있는 프로토타입 빈을 요청한다.
  - 해당 빈은 호출될 때마다 count필드가 0에서부터 1씩 증가한다.
  - A가 해당 빈을 호출하였으므로 count가 1 증가한다.
  - B가 동일한 빈에 요청한다. 프로토타입 빈은 요청 시마다 빈을 새롭게 생성하므로 새로운 빈의 count역시 1이 된다.

  ```java
  //전략
  
  public class SingletonWithPrototypeTest1 {
  
      @Test
      void prototypeFind(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(PrototypeBean.class);
          PrototypeBean prototypeBean1 = ac.getBean(PrototypeBean.class);
          prototypeBean1.addCount();
          Assertions.assertThat(prototypeBean1.getCount()).isEqualTo(1);
  
          PrototypeBean prototypeBean2 = ac.getBean(PrototypeBean.class);
          prototypeBean2.addCount();
          Assertions.assertThat(prototypeBean2.getCount()).isEqualTo(1);
      }
  
      @Scope("prototype")
      static class PrototypeBean {
          private int count = 0;
  
          public void addCount(){
              count++;
          }
  
          public int getCount(){
              return count;
          }
  
          @PostConstruct
          public void init(){
              System.out.println("PrototypeBean.init " + this);
          }
  
          @PreDestroy
          public void destroy(){
              System.out.println("PrototypeBean.destroy 호출");
          }
      }
  }
  ```



- 싱글톤 빈에서 프로토타입 빈 사용(clientBean이라는 싱글톤 빈이 의존관계 주입을 통해서 프로토타입 빈을 주입받아서 사용하는 예시)

  - 싱글톤 빈은 스프링 컨테이너 생성 시점에 함께 형성되고, 의존관계 주입도 발생한다.
  - clientBean은 의존관계 자동 주입을 사용하며, 주입 시점에 스프링 컨테이너에 프로토타입 빈을 요청한다.
  - 스프링 컨테이너는 프로토타입 빈을 생성해서 clientBean에 반환한다. 프로토타입 빈의 count필드 값은 0이다.
  - clinetBean은 프로토타입 빈을 내부 필드에 보관한다(정확히는 참고값을 보관한다).
  - 클라이언트A는 clientBean을 스프링 컨테이너에 요청해서 반환받는다. 싱글톤이므로 항상 같은 clientBean이 반환된다.
  - 클라이언트A는 `clientBean.logic()`을 호출한다.
  - clientBean은 prototypeBean의 `addCount()`를 호출해서 프로토타입 빈의 count가 증가하여 1이 된다.
  - 클라이언트B는 clientBean을 스프링 컨테이너에 요청해서 반환받는다. 싱글톤이므로 항상 같은 clientBean이 반환된다.
  - 여기서 중요한 점은 clientBean이 내부에 가지고 있는 프로토타입 빈은 이미 과거에 주입이 끝난 빈이다. 주입 시점에 스프링 컨테이너에 요청해서 프로토 타입 빈이 새로 생성이 된 것이지, 사용할 때마다 새로 생성되는 것이 아니다.
  - 클라이언트B는 `clientBean.logic()`을 호출한다.
  - `clientBean`은 prototypeBean의 `addCount()`를 호출해서 프로토타입 빈의 count를 증가하여 2가 된다(A에 의해 1이 증가해서 1인 상태였으므로).

  ```java
  //전략
  
  public class SingletonWithPrototypeTest1 {
  
      @Test
      void singleToneClienntUserPrototype(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(ClientBean.class, PrototypeBean.class);
          ClientBean clientBean1 = ac.getBean(ClientBean.class);
          int count1 = clientBean1.logic();
          Assertions.assertThat(count1).isEqualTo(1);
  
          ClientBean clientBean2 = ac.getBean(ClientBean.class);
          int count2 = clientBean2.logic();
          Assertions.assertThat(count2).isEqualTo(2); //1이 아닌 2가 된다.
  
  
      }
  
      //싱글톤 빈
      @Scope("singleton")
      static class ClientBean{
          private final PrototypeBean prototypeBean;
  
          //프로토타입 빈 주입, 생성시에 주입된 프로토타입 빈이 계속 사용된다.
          @Autowired
          public ClientBean(PrototypeBean prototypeBean){
              this.prototypeBean = prototypeBean;
          }
  
          public int logic(){
              prototypeBean.addCount();
              int count = prototypeBean.getCount();
              return count;
          }
      }
  
      //프로토타입 빈
      @Scope("prototype")
      static class PrototypeBean {
          private int count = 0;
  
          public void addCount(){
              count++;
          }
  
          public int getCount(){
              return count;
          }
  
          @PostConstruct
          public void init(){
              System.out.println("PrototypeBean.init " + this);
          }
  
          @PreDestroy
          public void destroy(){
              System.out.println("PrototypeBean.destroy 호출");
          }
      }
  }
  ```



- 프로토타입 빈은 호출될 때마다 빈을 생성한다는 것에 의의가 있음에도 위와 같이 주입 받아 쓰게 되면 싱글톤 빈이 생성될 때 주입 받은 프로토타입 빈을 계속 사용하므로 프로토타입 빈을 쓰는 의미가 없어지게 된다. 이를 해결하는 몇 가지 방법이 있다.







## 프로토타입 스코프와 싱글톤 스코프를 함께 사용시 발생하는 문제 해결

- 싱글톤 빈과 프로토타입 빈을 함께 사용할 때, 사용할 때 마다 항상 새로운 프로토타입 빈을 생성하는 방법



- 방법

  - 싱글톤 빈이 프로토타임을 사용할 때마다 스프링 컨테이너에 새로 요청하는 방법, 별로 좋은 방법은 아니다.
    - 실행해보면 항상 새로운 프로토타입 빈이 생성되는 것을 확인할 수 있다.
    - 의존관계를 외부에서 주입 받는게 아니라 이렇게 직접 필요한 의존관계를 찾는 것을 Dependency Lookup(DL, 의존관계 조회(혹은 탐색))이라고 한다.
    - 이렇게 스프링의 애플리케이션 컨텍스트 전체를 주입받게 되면, 스프링 컨테이너에 종속적인 코드가 되고, 단위 테스트도 어려워진다.
    - 지금 필요한 기능은 지정한 프로토타입 빈을 컨테이너에서 대신 찾아주는 DL 정도의 기능만 제공하는 무언가가 있으면 된다.
    - 스프링에는 이 모든 것이 준비되어 있다.

  ```java
  public class PrototypeProviderTest {
      @Test
      void providerTest() {
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(ClientBean.class, PrototypeBean.class);
          ClientBean clientBean1 = ac.getBean(ClientBean.class);
          int count1 = clientBean1.logic();
          assertThat(count1).isEqualTo(1);
          
          ClientBean clientBean2 = ac.getBean(ClientBean.class);
          int count2 = clientBean2.logic();
          assertThat(count2).isEqualTo(1);
      }
      
      @Scope("singleton")
      static class ClientBean {
          
          @Autowired
          private ApplicationContext ac;
          
          public int logic() {
              //logic이 실행될 때마다 컨테이너에서 빈을 가져온다.
              PrototypeBean prototypeBean = ac.getBean(PrototypeBean.class);
              prototypeBean.addCount();
              int count = prototypeBean.getCount();
              return count;
          }
      }
      
      @Scope("prototype")
      static class PrototypeBean {
          private int count = 0;
          public void addCount() {
              count++;
          }
          public int getCount() {
              return count;
          }
          @PostConstruct
          public void init() {
              System.out.println("PrototypeBean.init " + this);
          }
          @PreDestroy
          public void destroy() {
              System.out.println("PrototypeBean.destroy 호출");
          }
      }
  }
  ```

  - ObjectFatory, ObjectProvider
    - ObjectFatory: 기능이 단순(`.getObject()`하나 뿐이다), 별도의 라이브러리 필요 없음, 스프링에 의존
    - ObjectProvider: ObjectFatory 상속, 옵션, 스트림 처리등 편의 기능이 많고, 별도의 라이브러리 필요 없음, 스프링에 의존
    - 지정한 빈을 컨테이너에서 대신 찾아주는 DL 서비스를 제공하는 것이 바로 ObjectProvider이다.
    - 과거에는 ObjectFatory가 있었는데, 여기에 편의 기능을 추가해서 ObjectProvider가 만들어졌다.
    - 아래 코드를 실행하면 항상 새로운 프로토타입 빈이 생성되는 것을 확인할 수 있다.
    - 스프링이 제공하는 기능을 사용하지만, 기능이 단순하므로 단위테스트를 만들거나 mock 코드를 만들기는 훨씬 쉬워진다.

  ```java
  //전략
  
  public class SingletonWithPrototypeTest1 {
  
      @Test
      void singleToneClienntUserPrototype(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(ClientBean.class, PrototypeBean.class);
          ClientBean clientBean1 = ac.getBean(ClientBean.class);
          int count1 = clientBean1.logic();
          Assertions.assertThat(count1).isEqualTo(1);
  
          ClientBean clientBean2 = ac.getBean(ClientBean.class);
          int count2 = clientBean2.logic();
          Assertions.assertThat(count2).isEqualTo(1);
  
  
      }
  
      //싱글톤 빈
      @Scope("singleton")
      static class ClientBean{
          
          //필드 주입으로 의존성 주입(생성자 주입으로 하는 것이 권장되지만 예시이므로 필드 주입 사용)
          @Autowired
          private ObjectProvider<PrototypeBean> prototypeBeanProvider;
  
  
          public int logic(){
              //getObject를 호출하면 스프링 컨테이너에서 PrototypeBean을 찾아서 반환(DL)한다.
              PrototypeBean prototypeBean = prototypeBeanProvider.getObject();
              prototypeBean.addCount();
              int count = prototypeBean.getCount();
              return count;
          }
      }
  
      //프로토타입 빈은 위의 코드와 동일하므로 생략
  }
  ```

  - JSR-330 Provider
    - `javax.inject.Provider`라는 JSR-330 자바 표준을 사용하는 방법이다.
    - 이 방법을 사용하려면 `javax.inject:javax.inject:1`라이브러리를 gradle에 추가해야 한다.
    - 실행해보면 `.get()`을 통해 항상 새로운 프로토타입 빈이 생성되는 것을 확인할 수 있다.
    - `.get()`을 호출하면 내부에서는 스프링 컨테이너를 통해 해당 빈을 찾아서 반환한다(DL).
    - 기능이 `.get()` 메서드 하나로 매우 단순하고, 별도의 라이브러리가 필요하며, 자바 표준이므로 스프링 이외의 컨테이너에서도 사용 가능하다.

  ```java
  //전략
  //javax에서 import해야 한다. 다른 이름의 Provider도 있으므로 import시 주의해야 한다.
  import javax.inject.Provider;
  
  public class SingletonWithPrototypeTest1 {
  
      @Test
      void prototypeFind(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(PrototypeBean.class);
          PrototypeBean prototypeBean1 = ac.getBean(PrototypeBean.class);
          prototypeBean1.addCount();
          Assertions.assertThat(prototypeBean1.getCount()).isEqualTo(1);
  
          PrototypeBean prototypeBean2 = ac.getBean(PrototypeBean.class);
          prototypeBean2.addCount();
          Assertions.assertThat(prototypeBean2.getCount()).isEqualTo(1);
      }
  
      @Test
      void singleToneClienntUserPrototype(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(ClientBean.class, PrototypeBean.class);
          ClientBean clientBean1 = ac.getBean(ClientBean.class);
          int count1 = clientBean1.logic();
          Assertions.assertThat(count1).isEqualTo(1);
  
          ClientBean clientBean2 = ac.getBean(ClientBean.class);
          int count2 = clientBean2.logic();
          Assertions.assertThat(count2).isEqualTo(1);
  
  
      }
  
      //싱글톤 빈
      @Scope("singleton")
      static class ClientBean{
          
          //필드 주입으로 의존성 주입(생성자 주입으로 하는 것이 권장되지만 예시이므로 필드 주입 사용)
          @Autowired
          //이 부분과
          private Provider<PrototypeBean> prototypeBeanProvider;
  
  
          public int logic(){
              //이 부분만 바꿔주면 된다.
              PrototypeBean prototypeBean = prototypeBeanProvider.get();
              prototypeBean.addCount();
              int count = prototypeBean.getCount();
              return count;
          }
      }
  
      //프로토타입 빈은 위의 코드와 동일하므로 생략
  }
  ```



- 프로토타입 빈을 언제 사용하는가
  - 매번 사용할 때마다 의존관계 주입이 완료된 새로운 객체가 필요할 때 사용하면 된다.
  - 그런데 실무에서 웹 어플리케이션을 개발하다보면, 싱글톤 빈으로 대부분의 문제를 해결할 수 있기에 프로토타입 빈을 직접 사용하는 일은 드물다.
  - ObjectProvider , JSR-330 Provider 등은 프로토타입 뿐만 아니라 DL이 필요한 경우는 언제든지 사용할 수 있다.



- 참고사항들
  - 위에서 소개하지 않은 방법 중 스프링이 제공하는 메서드에 `@Lookup` 어노테이션을 사용하는 방법도 있지만, 이전 방법들로 충분하고, 고려해야 할 사항도 많아서 잘 사용하지 않는다.
  - 실무에서 자바 표준인 JSR-330 Provider를 사용할 것인지, 아니면 스프링이 제공하는 ObjectProvider를 사용할 것인지 고민이 될 것이다.
    - ObjectProvider는 DL을 위한 편의 기능을 많이 제공해주고, 스프링 외에 별도의 의존관계 추가가 필요 없기에 편리하다.
    - 코드를 스프링이 아닌 다른 컨테이너에서도 사용할 수 있어야 한다면  JSR-330 Provider를 사용해야 한다.
    - 스프링을 사용하다 보면 이 기능과 같이 자바 표준과 스프링이 제공하는 기능이 겹칠때가 있다. 대부분의 경우 스프링이 더 다양하고 편리한 기능을 제공하기에 특별히 다른 컨테이너를 사용할 일이 없다면(그리고 거의 그럴 일은 없다), 스프링이 제공하는 기능을 사용하면 된다.





## 웹 스코프

- 웹 스코프의 특징
  - 웹 스코프는 웹 환경에서만 동작한다.
  - 웹 스코프는 프로토타입과 다르게 스프링이 해당 스코프의 종료 시점까지 관리한다. 따라서 종료 메서드가 호출된다.



- 웹 스코프 종류
  - request: HTTP 요청 하나가 들어오고 나갈 때 까지 유지되는 스코프, 각각의 HTTP 요청마다 별도의 빈 인스턴스가 생성되고, 관리된다.
  - session: HTTP session과 동일한 생명주기를 가지는 스코프
  - application: 서블릿 컨텍스트(ServletContext)와 동일한 생명주기를 가지는 스코프
  - websocket: 웹 소켓과 동일한 생명주기를 가진느 스코프





### request 스코프 예제 개발

- 동시에 여러 HTTP 요청이 오면 정확히 어떤 요청이 남긴 로그인지 구분하기 어렵다. 이럴 때 사용하는 것이 바로 request 스코프이다.



- 웹 환경 추가하기: 웹 스코프는 웹 환경에서만 동작하므로 web이 동작하도록 라이브러리를 추가.

  - 아래 라이브러리를 추가하면 스프링 부트는 내장 톰캣 서버를 활용하여 웹 서버와 스프링을 함께 실행시킨다.
  - 스프링 부트는 웹 라이브러리가 없으면 우리가 지금까지 학습한 `AnnotationConfigApplicationContext`를 기반으로 애플리케이션을 구동한다.
  - 웹 라이브러리가 추가되면 웹과 관련된 추가 설정과 환경들이 필요하므로 `AnnotationConfigServletWebServerApplicationContext`를 기반으로 애플리케이션을 구동한다.

  ```java
  implementation 'org.springframework.boot:spring-boot-starter-web'
  ```



- 이제 메인 메서드를 실행시키면 웹 어플리케이션이 실행되면서 터미널 창에 다음 메세지가 찍히게 된다.

  ```java
  //2020-12-06 20:02:57.786  INFO 15672 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
  //2020-12-06 20:02:57.799  INFO 15672 --- [           main] start.first.FirstApplication             : Started FirstApplication in 2.299 seconds (JVM running for 2.707)
  
  //만약 기본 포트인 8080포트를 9090으로 변경하고자 한다면`application.properties`에 다음 설정과 같은 코드를 추가한다.
  server.port=9090
  ```



- 로그가 남도록 request 스코프를 활용해서 추가 기능을 개발해보자.

  - 로그를 출력하기 위한 `MyLogger` 클래스 생성

  ```java
  //전략
  
  @Component
  //request 스코프로 지정, 이제 이 빈은 HTTP 요청 당 하나씩 생성되고, HTTP 요청이 끝나는 시점에 소멸된다.
  @Scope(value = "request")
  public class MyLogger {
  
      private String uuid;
      private String requestURL;
  
      //requestURL은 빈이 생성되는 시점에는 알 수 없으므로 setter를 통해서 외부에서 입력 받는다.
      public void setRequestURL(String requestURL){
          this.requestURL = requestURL;
      }
  
      public void log(String message){
          System.out.println("[" + uuid + "]" + "[" + requestURL + "] " + message);
      }
  
      @PostConstruct
      public void init(){
          //java에서 제공하는 UUID가 있다. 유니크한 아이디를 만들기 위해 사용하며, 아이디가 겹칠 확률은 로또에 연속 당첨될 확률보다 낮다.
          //다른 HTTP들을 구분하기 위해 빈이 생성되는 시점에 uuid를 생성해서 저장해둔다.
          uuid = UUID.randomUUID().toString();
          System.out.println("[" + uuid + "]" + " request scope bean create: " + this);
      }
  
      @PreDestroy
      public void close(){
          System.out.println("[" + uuid + "]" + " request scope bean close: " + this);
      }
  }
  ```

  - Controller 작성

  ```java
  //전략
  
  @Controller
  @RequiredArgsConstructor
  public class LogDemoController {
  
      private final LogDemoService logDemoService;
      //아래와 같이 MyLogger를 주입 받는데, 문제는 MyLogger는 reqeust scope이므로 아직 생성도 되지 않은 상태다.
      private final MyLogger myLogger;
  
      @RequestMapping("log-demo")
      //화면에 출력할 것이 아니므로 Response를 통해 제대로 동작하는지 확인
      @ResponseBody
      //HttpServletRequest를 통해 요청 URL을 받는다.
      public String logDemo(HttpServletRequest request){
          //getRequestURL()은 요청 받은 URL을 알려주는 메서드다.
          String requestURL = request.getRequestURL().toString();
          //이렇게 받은 reuqestURL 값을 myLogger에 저장해둔다.myLogger는 HTTP scope이기에 요청 당 각각 구분되므로 값이 섞이지 않는다.
          //사실 이렇게 requestURL을 MyLogger에 저장하는 부분은 컨트롤러보다 공통 처리가 가능한 스프링 인터셉터나 서블릿 필터 같은 곳을 활용하는 것이 좋다. 그러나 코드를 단순화 하기 위해 컨트롤러에 작성한다.
          myLogger.setRequestURL(requestURL);
  
          myLogger.log("controller test");
          logDemoService.logic("testId");
  
          return "OK";
      }
  
  }
  ```

  - Service 작성
    - request scope를 사용하지 않고 파라미터로 이 모든 정보를 서비스 계층에 넘긴다면, 파라미터가 많아서 지저분해진다.
    - 더 문제는 requestURL과 같은 웹과 관련된 정보가 웹과 관련없는 서비스 계층까지 넘어가게 된다.
    - 웹과 관련된 부분은 컨트롤러까지만 사용해야 한다. 서비스 계층은 웹 기술에 종속되지 않고, 가급적 순수하게 유지하는 것이 유지보수에 좋다.
    - request scope의 MyLogger 덕문에 이런 부분을 파라미터로 넘기지 않고 MyLogger의 멤버 변수에 저장해서 코드와 계층을 깔끔하게 유지할 수 있다.

  ```java
  //전략
  
  @Service
  @RequiredArgsConstructor
  public class LogDemoService {
  
      private final MyLogger myLogger;
  
      public void logic(String id){
          myLogger.log("service id = " + id);
      }
  }
  ```

  - 위 코드를 실행했을 때 문제점
    - 코드가 실행되면 스프링 컨테이너는 빈을 등록하기 시작한다.
    - 그런데 Controller와 Service 모두 MyLogger를 주입 받아서 사용한다.
    - 그러나 MyLogger의 scope는 request이므로 아직 생성도 되지 않은 상태이다.
    - 따라서 빈을 등록할 수 없고 다음과 같은 에러가 발생한다. `Error creating bean with name 'myLogger': Scope 'request' is not active for the current thread`
  - 해결법
    - ObjectProvider를 사용한다.
    - ObjectProvider로 `myLoggerProvider.getObject()`를 호출하는 시점까지 request scope 빈의 생성을 지연한다.
    - `myLoggerProvider.getObject()`를 호출하는 시점에는 HTTP 요청이 진행중이므로 request scope 빈의 생성이 정상 처리된다.
    - `myLoggerProvider.getObject()`를 `LogDemoController`, `LogDemoService`에서 각각 학번씩 따로 호출해도 같은 HTTP 요청이면 같은 스프링 빈이 반환된다.

  ```java
  //전략
  
  @RequiredArgsConstructor
  public class LogDemoController {
  
      private final LogDemoService logDemoService;
      //ObjectProvider 추가
      private final ObjectProvider<MyLogger> myLoggerProvider;
  
      @RequestMapping("log-demo")
      @ResponseBody
      public String logDemo(HttpServletRequest request){
          //ObjectProvider로 가져오기
          MyLogger myLogger = myLoggerProvider.getObject();
          String requestURL = request.getRequestURL().toString();
          myLogger.setRequestURL(requestURL);
  
          myLogger.log("controller test");
          logDemoService.logic("testId");
  
          return "OK";
      }
  
  }
  ```

  ```java
  //전략
  
  @Service
  @RequiredArgsConstructor
  public class LogDemoService {
  	
      //ObjectProvider 추가
      private final ObjectProvider<MyLogger> myLoggerProvider;
  
      public void logic(String id){
          //ObjectProvider로 가져오기
          MyLogger myLogger = myLoggerProvider.getObject();
          myLogger.log("service id = " + id);
      }
  }
  ```

  - 이제 `http://localhost:8080/log-demo`로 접속해보면 터미널 창에 아래와 같은 메세지가 출력되는 것을 확인 가능하다.
    - 아래 uuid는 요청을 보낼 때 마다 다르게 찍히는 것을 확인 가능하다.

  ```java
  //[f1dc1dd6-59d7-4294-b49d-a408dca85fa4] request scope bean create: start.first.common.MyLogger@716ffdfd  //빈 생성
  //[f1dc1dd6-59d7-4294-b49d-a408dca85fa4][http://localhost:8080/log-demo] controller test
  //[f1dc1dd6-59d7-4294-b49d-a408dca85fa4][http://localhost:8080/log-demo] service id = testId
  //[f1dc1dd6-59d7-4294-b49d-a408dca85fa4] request scope bean close: start.first.common.MyLogger@716ffdfd   //빈 소멸
  ```



### 스코프와 프록시

- 위 예시를 프록시 방식을 사용하여 작성하면 다음과 같다.

  - MyLogger.java

  ```java
  //전략
  
  @Component
  //proxyMode를 추가, 적용 대상이 클래스면 TARGET_CLASS를, 적용 대상이 인터페이스면 INTERFACES를 입력한다.
  @Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
  public class MyLogger {
  	//아래는 동일하므로 생략
  }
  ```

  - LogDemoController와 LogDemoService를 ObjectProvider를 사용하기 전 코드로 돌려 놓는다.
  - 정상적으로 동작 하는 것을 확인 할 수 있다.



- 위 방식은 MyLogger의 가짜 프록시 클래스를 만들어두고 HTTP request와 상관 없이 가짜 프록시 클래스를 다른 빈에 미리 주입해 두는 방식이다.

  - CGLIB 라이브러리로 내 클래스를 상속 받은 가짜 프록시 객체를 만들어서 주입한다.
  - `@Scope`의 `proxyMode = ScopedProxyMode.TARGET_CLASS`를 설정하면 스프링 컨테이너는 CGLIB라는 바이트 코드를 조작하는 라이브러리를 사용하여 MyLogger를 상속받은 가짜 프록시 객체를 생성한다.
  - 결과를 확인해보면 우리가 등록한 순수한 MyLogger 클래스가 아닌 `MyLogger$$EnhancerBySpringCGLIB`라는 클래스로 만들어진 객체가 대신 등록된 것을 확인할 수 있다.
  - 그리고 스프링 컨테이너에 "myLogger"라는 이름으로 진짜 대신에 이 가짜 프록시 객체를 등록한다.
  - `ac.getBean("myLogger", Mylogger.class)`로 조회해도 프록시 객체가 조회되는 것을 확인할 수 있다.
  - 따라서 의존관계 주입도 이 가짜 프록시 객체가 주입된다.

  ```java
  //전략
  
  @Controller
  @RequiredArgsConstructor
  public class LogDemoController {
  
      private final LogDemoService logDemoService;
      private final MyLogger myLogger;
  
      @RequestMapping("log-demo")
      @ResponseBody
      public String logDemo(HttpServletRequest request){
          String requestURL = request.getRequestURL().toString();
          //아래 코드를 통해 myLogger를 확인
          System.out.println("myLogger = " + myLogger.getClass());
          myLogger.setRequestURL(requestURL);
  
          myLogger.log("controller test");
          logDemoService.logic("testId");
  
          return "OK";
      }
  
  }
  
  //out
  myLogger = class start.first.common.MyLogger$$EnhancerBySpringCGLIB$$9fab1ba0 //CGLIB를 확인 가능하다.
  ```



- 가짜 프록시 객체는 요청이 오면 그때 내부에서 진짜 빈을 요청하는 위임 로직이 들어있다. 
  - 가짜 프록시 객체는 내부에 진짜 myLogger를 찾는 방법을 알고 있다. 
  - 클라이언트가 myLogger.logic() 을 호출하면 사실은 가짜 프록시 객체의 메서드를 호출한 것이다. 
  - 가짜 프록시 객체는 request 스코프의 진짜 myLogger.logic() 를 호출한다. 
  - 가짜 프록시 객체는 원본 클래스를 상속 받아서 만들어졌기 때문에 이 객체를 사용하는 클라이언트 입장에 서는 사실 원본인지 아닌지도 모르게, 동일하게 사용할 수 있다(다형성)



- 정리
  - CGLIB라는 라이브러리로 내 클래스를 상속 받은 가짜 프록시 객체를 만들어서 주입한다. 
  - 이 가짜 프록시 객체는 실제 요청이 오면 그때 내부에서 실제 빈을 요청하는 위임 로직이 들어있다. 
  - 가짜 프록시 객체는 실제 request scope와는 관계가 없다. 그냥 가짜이고, 내부에 단순한 위임 로직만 있 고, 싱글톤 처럼 동작한다.



- 이 방식의 특징
  - 프록시 객체 덕분에 클라이언트는 마치 싱글톤 빈을 사용하듯이 편리하게 request scope를 사용할 수 있 다. 
  - 사실 Provider를 사용하든, 프록시를 사용하든 핵심 아이디어는 진짜 객체 조회를 꼭 필요한 시점까지 지연 처리 한다는 점이다. 
  - 단지 애노테이션 설정 변경만으로 원본 객체를 프록시 객체로 대체할 수 있다. 
  - 이것이 바로 다형성과 DI 컨 테이너가 가진 큰 강점이다. 
  - 꼭 웹 스코프가 아니어도 프록시는 사용할 수 있다.



- 주의점
  - 마치 싱글톤을 사용하는 것 같지만 다르게 동작하기 때문에 결국 주의해서 사용해야 한다. 
  - 이런 특별한 scope는 꼭 필요한 곳에만 최소화해서 사용하자, 무분별하게 사용하면 유지보수하기 어려워 진다.











