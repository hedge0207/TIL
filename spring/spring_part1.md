# 프로젝트 생성하기

- 스프링 부트 공식 문서

  > https://docs.spring.io/spring-boot/docs/current/reference/html/ 

- 준비물: Java, IDE(IntelliJ 혹은 Eclipse) 설치

  - 단, gradle과 IntelliJ를 함께 쓸 경우 build, run이 직접 실행되는 것이 아니라 gradle을 통해서 되어 느리게 실행되는 경우가 있으므로 `Setting`에서 `Build, Execution, Deployment` 하부의 `Bulid Tools`에서 `Gradle`을 찾아 `Build and run using` 옵션과 `Run tests using` 옵션을 모두 `IntelliJ IDEA`로 변경해준다.



- 스프링 부트 스타터 사이트로 이동해서 스프링 프로젝트 생성

  >https://start.spring.io/

  - 메이븐과 그레이들의 역할

    - 필요한 라이브러리 관리
    - 빌드시 라이프 사이클 관리

    - 과거에는 메이븐을 많이 썼으나 최근에는 그레이들을 많이 사용
    - 그레이들 추천

  - 스프링 부트의 버전 선택

    - SNAPSHOT, M1 등은 아직 개발 중인 버전

  - 프로젝트 메타 데이터 작성

    - 일반적으로 Group에는 기업 도메인명을 적는다.
    - Artifact는 빌드되어 나오는 결과물을 적는다.
    - Name, Descrition, Package name 등은 그대로 둬도 된다.

  - Dependencies에는 아래의 것들을 추가한다.

    -  `Spring Web `: Spring으로 웹 프로젝트를 생성하기 위해 설치
    - `Thymeleaf`: HTML을 만들어주는 템플릿 엔진, 다양한 종류가 있으나 `Thymeleaf`가 그나마 낫다.

  - 하단의 GENERATE 클릭

    - 압축파일이 다운 받아지는데 압축 해제 후 사용하면 된다.



- 라이브러리
  - 스프링 프로젝트를 생성하면 `External Libraries` 폴더에서 설치된 라이브러리들을 볼 수 있는데 프로젝트 생성시 자동으로 추가되는 라이브러리만 수십가지 이다.
  - 메이븐, 그레이들은 이렇게 다양한 라이브러리들의 의존관계를 관리해준다.
    - 예를 들어 A라는 라이브러리가 B에 의존하고 B는 C라는 라이브러리에 의존한다면 A를 추가할 때 B,C를 자동으로 모두 추가해준다.
    - `IntelliJ` 창의 최우측 상단에 보면 Gradle(Maven을 설치했을 경우 Maven) 버튼을 클릭 할 수 있는 데(없을 시 좌측 최하단에 네모 표시를 클릭하면 생긴다.) 거기서 라이브러리들의 Dependnecies를 확인 가능하다.
    - 폴더 구조로 되어 있는 데 하단에 있는 라이브러리는 상단에 있는 라이브러리를 사용하는 데 필요한 라이브러리들이다.
    - `spring-boot-starter`: 스프링 부트 프로젝트 생성 시 자동으로 추가되며 스프링 부트, 스프링 코어, 로깅에 필요한 라이브러리 들이 담겨 있다.
    - 로깅의 경우 실무에서는 `system.out.println()`을 사용하지 않고 위 라이브러리에 있는 `logback`, `slf4j`을 사용한다.







# 프로젝트 실행하기

- 프로젝트 열기

  - `IntelliJ` 실행 후 `Open or Import Project` 클릭
  - `build.gradle` 클릭하여 실행

  

- 구조
  - 지금은 src 하부 폴더인 main과 test만 알고 있으면 된다.
    - `main`: 하부 폴더로 `java`, `resources`가 있고 `java`에 패키지와 소스 파일이 존재. `resources` 폴더 내부에는 XML, HTML, properties 파일 등 자바 이외의 웹 브라우저를 구성하는데 필요한 파일들이 존재한다.
    - `test`: 역시 하부 폴더로 `java`가 있으며 테스트와 관련된 파일이 존재.
  - 이외의 폴더는 전부 환경 관련 폴더들이다.
  - `build.gradle`: 버전과 라이브러리에 대한 정보가 작성된 파일
    - 자바 버전, 스프링 부트 버전, dependencies, 그룹명 등을 볼 수 있다.
  - `External Libraries`: 외부에서 가져온 라이브러리들이 저장된 폴더



- 실행하기

  - `main/java/프로젝트명/프로젝트그룹명/프로젝트그룹명Application파일` 클릭
  - 코드 창 우클릭 후 `run` 클릭하여 실행
  - `Tomcat`
    - 아래 터미널 창을 확인해보면 맨 아래에서 두번째 줄에 아래와 같은 메세지를 확인할 수 있다.
    - `Tomcat started on port(s): 8080 (http) with context path ''`
    - `Tomcat`은 스프링에 내장된 웹 서버이다.
    - 과거에는 내장되어 있지 않아 `Tomcat` 서버를 별도로 실행해줘야 했다.

  ```java
  ![화면 캡처 2020-10-15 221017](../../../화면 캡처 2020-10-15 221017.jpg)package hello.hellospring;
  
  import org.springframework.boot.SpringApplication;
  import org.springframework.boot.autoconfigure.SpringBootApplication;
  
  @SpringBootApplication
  public class HelloSpringApplication {
  
  	public static void main(String[] args) {
  		SpringApplication.run(HelloSpringApplication.class, args);
  	}
  
  }
  ```

  - 이후 `http://localhost:8080/`으로 접속 시 아래와 같이 뜨면 정상적으로 작동한 것이다.

    <img src="spring_part1.assets/화면 캡처 2020-10-15 221017-1602768211229.jpg"/>



# 프로젝트 작성하기

- 스프링은 코드를 변경 할 경우 반드시 서버를 껐다 켜야 한다.

  - `spring-boot-devtools` 라이브러리를 사용할 경우 html 파일만 컴파일 해주면 서버 재시작 없이도 변경 사항이 반영된다.

    > https://velog.io/@bread_dd/Spring-Boot-Devtools 참고



- Welcome page 만들기

  - 스프링 부트에서는 `src/main/resources/static`폴더 내부에 `index.html` 파일을 만들면 사이트에 처음 들어갔을 때 해당 페이지를 띄워 준다.

    - 파일명이 반드시 `index.html`이어야 한다.

  - `src/main/resources/static/index.html`

    - 아래와 같이 작성 후 서버가 켜져 있었을 경우 서버를 재실행 하고 `localhost:8080`으로 접속해보면 hello!가 떠 있는 것을 확인할 수 있다.

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        hello!
    </body>
    </html>
    ```



- `controller`
  - `main/java/프로젝트명/프로젝트그룹명`의 하부 파일로 `controller`라는 이름의 패키지를 생성

  - 위 패키지의 내부에 `이름Controller(e.g. HelloController)` 라는 이름의 자바 클래스 생성, 최초 생성 시 아래의 코드만 작성되어 있다.

    ```java
    package hello.hellospring.controller;
    
    public class HelloController {
    }
    ```

  - `HelloController` 상단에 `@Controller`를 입력하면 아래와 같이 추가된다.

    ```java
    package hello.hellospring.controller;
    
    import org.springframework.stereotype.Controller;
    
    @Controller
    public class HelloController {
    }
    ```

  - 이제 작성하고자 하는 내용을 추가한다.

    ```java
    package hello.hellospring.controller;
    
    import org.springframework.stereotype.Controller;
    import org.springframework.ui.Model;
    import org.springframework.web.bind.annotation.GetMapping;
    
    @Controller
    public class HelloController {
        
        // /hello-world로 요청이 들어올 경우 아래 메서드를 호출한다.
        @GetMapping("hello-world")
        public String hello(Model model){
            //아래 코드에는 나오지 않지만 실제 코드창에는 다음과 같이 자동으로 뜬다.
            //model.addAttribute(attributeName: "data", attributeValue: "ㅎㅇㅎㅇ");
            //키는 data, 값은 "ㅎㅇㅎㅇ"라는 뜻이다.
            model.addAttribute("data","ㅎㅇㅎㅇ");
            return "hello";
        }
    }
    ```

  - 그 후 `templates` 폴더 내부에 `hello.html` 파일 생성 후 아래와 같이 작성

    - html 파일의 이름은 `return` 값으로 입력한 문자열과 동일해야 한다.

    ```html
    <!DOCTYPE html>
    <!--이 프로젝트에서는 thymeleaf을 쓰므로 아래와 같이 입력하고-->
    <html xmlns:th="http://www.thymeleaf.org">
    <head>
        <meta charset="UTF-8">
        <title>Hello</title>
    </head>
    <body>
        <!--태그에 속성으로 th를 준 뒤 위에서 입력한 key값은 data를 출력하면-->
        <div th:text="'안녕하세요. '+${data}">안녕하세요. 손님</div>
    </body>
    </html>
    
    <!--
    out
    localhost:8080/hello-world 로 접속하면
    "안녕하세요. 손님" 이 출력되지 않고
    data에 해당하는 value인 ㅎㅇㅎㅇ가 들어가게 되어
    "안녕하세요. ㅎㅇㅎㅇ" 가 출력된다.
    ```



- 전체적인 흐름
  - 웹 브라우저에서 내장 톰켓 서버로 요청을 보낸다.
  - 톰켓 서버는 스프링에 해당 요청을 처리하는 메서드가 있는 Controller로 해당 요청을 전달한다.
  - 모델에 {key:value}로 이루어진 데이터를 추가한 뒤 문자를 리턴값으로 반환한다.
  - 뷰 리졸버가 `resources/templates`내부에서 반환된 문자열과 파일명이 동일한 html파일을 찾아서 화면을 찾는다.
  - html파일을 렌더링한다(`Thymeleaf` 등의 템플릿 엔진이 이 역할을 수행).





- 코드 내부의 `getX()`와 같은 코드는 사용자가 직접 작성한 메소드일 수도 있으나 `lombok`이라는 확장프로그램을 설치하면 관련 메소드들을 사용 가능하다.