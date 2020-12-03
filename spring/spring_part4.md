# 의존 관계자동 주입

## 다양한 의존관계 주입 방법

- 의존관계 주입은 크게 4가지 방법이 있다.
  - 생성자 주입
  - 수정자 주입(setter 주입)
  - 필드 주입
  - 일반 메서드 주입



- 생성자 주입

  - 생성자를 통해서 의존관계를 주입 받는 방법
  - 지금까지 앞에서 사용했던 방법이 생성자 주입이다.

  - 특징
    - 생성자 호출시점에 딱 1번만 호출되는 것이 보장된다.
    - 불변, 필수 의존관계에 주로 사용한다.
  - 코드
    - 아래 코드에서 `OrderServiceImpl`이 스프링 빈으로 등록될 때 생성자가 호출되게 된다.
    - 생성자에 `@Autowired`가 있으므로 스프링 컨테이너에서 `MemberRepository`, `DiscountPolicy`를 꺼내서 `OrderServiceImpl`에 주입한다.
    - 생성자가 딱 1개만 있으면 `@Autowired`를  **생략**해도 자동 주입 된다. 물론 스프링 빈에만 해당한다(따라서 아래 코드에서는 사실 `@Autowired`를 굳이 적어줄 필요가 없다).

  ```java
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

- 생성자 주입으로 해야 하는 이유를 위에서 살펴보았는데 다른 주입 방식에 비해 코드가 길다는 단점이 존재한다. 따라서 코드를 최적화 해야한다.



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





## 조회한 빈이 모두 필요할 때 List, Map

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







## 자동, 수동의 올바른 실무 운영 기준

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

- 빈 생명주기 콜백 시작
  - 