# CORS

> https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
>
> https://evan-moon.github.io/2020/05/21/about-cors/
>
> https://ko.javascript.info/fetch-crossorigin

- CORS(Cross-Origin Resource Sharing, 교차 출처 리소스 공유)

  - Origin
    - scheme(protocol), domain(hostname), port을 묶어서 origin이라 부른다.
    - 예를 들어 `http://example.com:80/foo`라는 URL이 있다고 할 때 `http://example.com:80`까지가 origin이다.

  - 의미
    - 서로 다른 origin들 사이의 자원을 공유하는 것을 의미한다.
    - 예를 들어 `http://domain-a.com`이라는 front-end origin에서 `http://domain-b.com`이라는 back-end origin에 정보를 요청하는 것이 CORS다.
  - SOP(Same Origin Policy)
    - 같은 origin에서만 리소스를 공유할 수 있게 하는 정책.
    - 현실적으로 웹에서 같은 origin에 있는 리소스만을 가져오는 것은 불가능했다.
    - 따라서 예외 조항을 두었는데, 그 중 하나가 CORS 정책을 지킨 리소스 요청이다.
    - 이와 같은 제약을 둔 것은 XSS(Cross Site Script)나 CSRF(Cross Site Request Forgery) 같은 공격을 막기 위해서이다.
  - CORS는 브라우저의 정책이다.
    - 즉, 브라우저가 자신이 보낸 요청 및 서버로부터 받은 응답이 CORS 정책을 지키는지 검사한다.
    - 따라서 이를 지키지 않은 요청은 보내지 않고, 이를 지키지 않은 응답은 받아서 버린다.



- 안전한 요청

  - 크로스 오리진 요청은 크게 안전한 요청과 그 외의 요청의 두 가지 종류로 구분된다.
  - 안전한 요청은 아래의 두 가지 조건을 모두 충족하는 요청을 말한다.
    - 안전한 메서드 사용(GET, POST, HEAD).
    - 안전한 헤더를 사용(`Accept`, `Accept-Language`, `Content-Language`, 값이 `multipart/form-data`, `test/plain`, `application/x-www-from-urlencoded` 중 하나인 `Content-type`)

  - 그 외의 요청은 당연히 둘 중 하나라도 충족하지 못한 요청을 말한다.



- CORS와 안전한 요청(MDN 문서에서는 Simple Request라고 표현)

  - 크로스 오리진 요청을 보낼 경우 브라우저는 항상 `Origin`이라는 헤더를 요청에 추가한다.
  - 예시
    - `http://A.com/product`에서 `httpL//B.com/request`로 요청을 보낸다고 가정했을 때 헤더는 다음과 같다.
    - `Origin`에는 요청이 이루어지는 페이지 경로(`/product`)가 아닌 origin 정보가 담기게 된다.

  ```text
  GET /request
  Host: B.com
  Origin: http://B.com
  ```

  - 서버는 요청 헤더에 있는 `Origin`을 검사하고, 이 origin에서 요청을 받기로 설정이 되어 있다면, 헤더에 `Access-Control-Allow-Origin`을 추가해 응답을 보낸다.
    - 이 헤더에는 허가된 origin(예시의 경우 `http://A.com`)에 대한 정보나 `*`가 명시된다.



- 응답 헤더
  - 크로스 오리진 요청이 이루어진 경우, JavaScript는 기본적으로 안전한 응답 헤더로 분류되는 헤더에만 접근할 수 있다.
    - 그 외의 헤더에 접근하면 에러가 발생한다.
  - 안전한 응답 헤더는 다음과 같다.
    - `Cache-Control`
    - `Content-Language`
    - `Content-Type`
    - `Expires`
    - `Last-Modified`
    - `Pragma`
  - 만일 안전하지 않은 헤더에 에러 없이 접근하려면 서버에서 `Access-Control-Expose-Headers`라는 헤더를 보내줘야 한다.
    - 이 헤더에는 JavaScript에 접근을 허용하지만 안전하지는 않은 header들의 콤마로 구분된 목록이 담겨 있다.



- CORS와 안전하지 않은 요청
  - 안전하지 않은 요청이 이루어지는 경우, 서버에 바로 요청을 보내지 않고 preflight 요청이라는 사전 요청을 서버에 보내 권한이 있는지를 확인한다.
    - 클라이언트에서 preflight 요청을 보내는 로직을 추가해야 되는 것은 아니고, 브라우저가 알아서 보낸다.
  - preflight 요청은 `OPTIONS` 메서드를 사용하고 아래의 두 헤더가 함께 들어가며, body는 비어 있다.
    - `Access-Control-Request-Method`: 안전하지 않은 요청에서 사용하는 메서드 정보가 담겨 있다.
    - `Access-Control-Request-Headers`: 안전하지 않은 요청에서 사용하는 헤더 목록이 담겨있다.
  - 서버가 안전하지 않은 요청을 받는 것을 허용했다면 빈 body와 아래 헤더들을 status code 200으로 브라우저로 보낸다.
    - `Access-Control-Allow-Origin`
    - `Access-Control-Allow-Methods`: 허용된 메서드 정보가 담겨 있다.
    - `Access-Control-Allow-Headers`: 허용된 헤더 정보가 담겨 있다.
    - `Access-Control-Max-Age`: 퍼미션 체크 여부를 몇 초간 캐싱해 놓을지가 담겨 있다. 이 기간 동안은 브라우저가 preflight를 보내지 않고 바로 본 요청을 보낸다.



- Credentialed Request
  - 쿠키 정보나 인증과 관련된 정보를 담을 수 있게 해주는 옵션이다.
  - 요청시에 아래와 같은 3가지 옵션이 있다.
    - `omit`: cookie(혹은 cookie를 비롯한 사용자 credentials)를 보내거나 받지 않는다.
    - `same-origin`(기본값): origin이 같을 경우에만 cookie를 받는다.
    - `include`: origin이 다르더라도 cookie를 보낸다.
  - Credentialed Request를 사용할 때는 서버의 응답 헤더에 두 가지 헤더가 추가되어야 한다.
    - `Access-Control-Allow-Credentials`의 값이 true여야 한다.
    - `Access-Control-Allow-Origin`의 값이 `*`여선 안 된다.





# 왜 숫자는 0부터 세는가?

> https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html

- 자연수의 부분수열 표기
  - 자연수의 부분수열(`[2, 3, ..., 12]`)을 표기할 때 중략을 표현하는 점 3개(`...`) 없이 표현하는 방법에는 다음과 같은 것들이 있다.
    - a: `2 <= i < 13`
    - b: `1 < i <= 12`
    - c: `2 <= i <= 12`
    - d: `1 < i < 13`
  - 위의 4가지 방법들 중 더 효율적인 표기법은 분명히 존재한다.
  - 한 쪽에만 equal or bigger than 표기(<=)가 있으면 아래와 같은 점에서 효율적이다.
    - a, b 방식의 경우 양 경계값의 차이가 부분수열의 길이와 같다. 따라서 부분수열의 길이를 보다 직관적으로 알 수 있다.
    - 또한 두 부분 수열이 맞닿아 있을 때 한 쪽의 상한 수가 다른 쪽의 하한수와 같아진다.
    - 예를 들어 a 표기법의 경우 `2 <= i < 13`과 같이 표기할 경우 이전 수열은 `1 <= 1 < 2`과 같이 상한수와 하한수(이 경우 `2`)의 변경 없이 표기가 가능하고, 다음 수열인 `13 <= i < 15` 역시 상한수(이 경우 `13`)와 하한수의 변경 없이 표기가 가능하며, b 표기법 역시 마찬가지다.
  - b와 d 처럼 하한수(예시의 경우 `2`)를 제외하면 가장 작은 자연수 0(0을 자연수라고 할 때 0이 가장 작은 자연수이다)으로 시작하는 부분 수열을 표기할 때 하한수를 비자연수에 있는 숫자에서 선택하도록 강제된다.
    - 만일 `[0, 1, 2, 3]`과 같은 부분수열을 표기하려면 `-1 < i <= 3`(b 방식), `-1 < i < 4`(d 방식)와 같이 표기해야한다.
    - 이는 직관적이지도 않고 부자연스럽다.
  - 따라서 a 방식이 가장 효율적인 표현 방법이다.



- 만약 인덱스가 1부터 시작할 경우
  - 위에서 a 방식이 부분 수열을 표기하는 가장 효율적인 방식이라는 것을 확인했다.
    - 따라서 a 방식으로 인덱스의 범위를 표기할 때, 인덱스를 1부터 시작하는 것과, 0부터 시작하는 것의 차이는 아래와 같다.
  - 길이가 N인 수열의 인덱스가 1부터 시작할 경우(a 표기법에 따른) 인덱스의 범위는 `1 <= i < N+1`이 된다.
  - 반면 0부터 시작할 경우(a 표기법에 따른) 인덱스의 범위는 보다 깔끔한 `0 <= N < N`이 된다.





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





# 보안

- Software 보안의 3대 요소
  - 기밀성(confidentiality): 인가되지 않은 접근 차단.
  - 무결성(integrity): 인가 받지 않은 사용자는 데이터의 변경이 불가능.
  - 가용성(availability): 권한을 가진 사용자는 서비스를 지속해서 사용할 수 있음.



- 용어
  - 자산(assets)
    - 조직이 가치를 부여한 대상
    - 데이터, 하드웨어 등
  - 위협(threat)
    - 자산에 악영향을 끼칠 수 있는 사건이나 행위
    - 해킹, 데이터 변조 등
  - 취약점(vulnerability)
    - 위협이 발생하기 위한 사전 조건.
    - 비밀번호 공유, 입력값 미 검증 등
  - 위험(risk)
    - 위협이 취약점을 이용하여 조직에 피해를 끼칠 가능성.



- 접근 통제 기법

  - 접근 통제 용어
    - 주체(subject): 시스템에 접근을 요청하는 능동적인 개채
    - 객체(object): 접근 대상이 되는 개채
    - 접근(access): 주체의 활동
  - 식별(identification)
    - 자신의 정보를 시스템에 밝히는 행위
    - 주체가 객체에게 자신의 정보를 제공.
  - 인증(authentication)
    - 주체의 신원을 검증하는 활동
    - 주체의 신원을 객체가 인증.
  - 인가(authorization)
    - 인증된 주체에게 접근을 허용하는 활동
  - 책임추적(accountability)
    - 주체의 접근을 추적하고 행동을 기록하는 활동

  - 3A
    - authentication
    - authorization
    - accounting



