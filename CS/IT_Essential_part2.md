# RPC

> https://velog.io/@jakeseo_me/RPC%EB%9E%80
>
> https://www.getoutsidedoor.com/2019/07/11/what-is-grpc/

- RPC(Remote Procedure Call, 원격 프로시저 호출)
  - 별도의 원격 제어를 위한 코딩 없이 다른 주소 공간에서 함수나 프로시저를 실행할 수 있게 하는 프로세스 간 통신 기술
    - 프로세스간 통신을 위해 사용하는 IPC(Inter Process Communication) 방법의 한 종류.
    - 분산 컴퓨팅 환경에서 프로세스 간 상호 통신 및 컴퓨팅 자원의 효율적인 사용을 위해서 발전된 기술이다.
    - 원격지의 프로세스에 접근하여 프로시저 또는 함수를 호출하여 사용한다.
    - RPC를 이용하면 프로그래머는 함수가 실행 프로그램에 로컬 위치에 있든 원격 위치에 있든 동일한 코드를 이용할 수 있다.
  - 함수와 프로시저의 차이
    - 함수(function): input에 따른 output의 발생을 목적으로 하는 것으로, Return값을 필수로 가져야한다.
    - 프로시저(Procedure): output 값 자체에 집중하기보단, 명령 단위가 수행하는 절차에 집중한 개념으로, Return 값이 없을 수도 있다.
  - RPC의 기능
    - 언어나 환경에 구애받지 않고 Client-Server 간의 커뮤니케이션을 가능하게 한다.
    - 일반적으로 프로세스는 자신의 주소공간 안에 존재하는 함수만 호출하여 실행 가능하다.
    - 그러나, PRC는 네트워크를 통한 메시징을 통해 다른 주소 공간의 함수나 프로시저를 호출할 수 있게 해 준다.
    - 이를 통해 MSA(Micro Service Architecture) 서비스를 만들 때, 언어나 환경에 구애받지 않고, 비즈니스 로직을 개발하는 데 집중할 수 있다.



- IDL(Interface Definition Language)

  - 소프트웨어 컴포넌트의 인터페이스를 묘사하기 위한 명세 언어
    - 어느 한 언어에 국한되지 않는 언어 중립적인 방법으로 인터페이스를 표현함으로써, 같은 언어를 사용하지 않는 소프트웨어 컴포넌트 사이의 통신을 가능하게 한다.
    - 즉, 두 개의 시스템을 연결하는 다리 역할을 한다.

  - RPC는 IDL을 사용하여 인터페이스를 명시한다.
    - 서버와 클라이언트가 서로 다른 언어를 사용하는 경우도 있다.
    - 서로 다른 언어가 요청과 응답을 주고 받기 위해 인터페이스를 통해 규칙을 명세하고, 각자의 시스템이 이해할 수 있는 형태로 변형하는 작업이 필요한데, IDL이 이러한 역할을 담당한다.
  - 정의된 IDL을 기반으로 rpcgen이라는 rpc 프로토콜 컴파일러를 통해 코드(stub)가 생성된다.
    - Stub은 클라이언트에게는 서버의 프로시저 호출을 위한 참조자가 된다.
    - 서버에게는 프로시저 이해를 위한 참조가 된다(서버 측의 stub을 skeleton이라 부른다.).
    - stub은 원시소스코드 형태로 만들어지므로 클라이언트, 서버 프로그램에 포함하여 빌드한다.





- RPC의 구조 및 동작 과정

  ![img](IT_Essential_part2.assets/operating-system-remote-procedure-call-1-16532903490084-16533502803281.png)

  ![img](IT_Essential_part2.assets/operating-system-remote-call-procedure-working-16532903624116-16533502803292.png)

  - 클라이언트가 클라이언트 스텁 프로시저를 작동시키고, 파라미터를 전달한다.
  - 클라이언트 스텁이 메시지에 파리미터를 Marshall(Pack, 직렬화)한다.
    - Marshall: 파라미터 값을 표준화된 형식으로 변환시키고, 각 파라미터를 메시지에 복사하는 과정
    - 데이터 형태를 XDR(eXternal Data Representation) 형식으로 변환한다.
    - XDR로 변환하는 이유는 integer, float과 같은 기본 데이터 타입에 대해서 머신마다 메모리 저장 방식(i.e. little endian, big endian)이 CPU 아키텍처 별로 다르며, 네트워크 전송 과정에서 바이트 전송 순서를 보장하기 위해서이다.
  - 클라언트 스텁이 메시지를 전송 계층(transport layer)에 넘겨준다.
    - 전송 계층은 해당 메시지를 원격 서버로 보낸다.
  - 서버 측에서 전송 계층이 받아온 메시지를 서버 스텁에 넘겨준다.
    - 서버 스텁은 메시지를 Demarshall(Unmarshall, Unpack)한다.
  - 서버 스텁은 프로시저를 호출한다.
  - 서버 프로시저가 종료되면, 서버 스텁을 반환하고, 서버 스텁은 반환 값을 Marshall하여 메시지에 담는다.
    - 이 메시지를 전송 계층에 전달한다.
  - 전송 계층은 반환 값을 다시 클라이언트의 전송 계층에 전달한다.
  - 클라이언트의 전송 계층은 받은 메시지를 클라이언트 스텁에 전달한다.
  - 클라이언트 스텁은 받아온 반환 파라미터값을 Demarshall하고, 실행한다.



## gRPC

> https://chacha95.github.io/2020-06-15-gRPC1/
>
> https://grpc.io/docs/what-is-grpc/introduction/

- gRPC
  - Google에서 개발한 RPC 시스템
  - TCP/IP 프로토콜과 HTTP 2.0 프로토콜을 사용한다.
    - HTTP 2.0은 HTTP 1.1의 프로토콜을 계승해 성능을 더욱 발전시켰다.
  - HTTP 2.0의 특징
    - Multiplexed Streams: 한 connection으로 동시에 여러 개의 메시지를 주고 받을 수 있으며, Response는 순서와 상관 없이 stream으로 주고 받는다.
    - Stream Prioritization: 리소스간 우선 순위를 설정해 클라이언트가 먼저 필요로하는 리소스부터 보내준다.
    - Server Push: 서버는 클라이언트의 요청에 대해 요청하지 않은 리소스를 마음대로 보내줄 수 있다.
    - Header Compression: Header table과 Huffman Encoding 기법을 사용해 header를 압축한다.
  - IDL로 protocol buffers를 사용한다.
    - google에서 자체 개발한 IDL이다.
    - 구조화된 데이터를 직렬화 할 수 있게 해준다.
    - 다른 방식(XML, Json 등)에 비해 간단하고, 파일 크기도 3~10배 작으며 속도도 20~100배 빠르다는 장점이 있다.
    - Json 같은 IDL도 사용이 불가능 한 것은 아니다.
  - Python, Java, C++, C#, JavaScript, Ruby 등에서 사용 가능하다.



- gRPC의 구조

  ![Concept Diagram](IT_Essential_part2.assets/landing-2-16534518558762.svg)

  - 다른 RPC들과 마찬가지로 service를 정의하고, 원격으로 호출할 수 있는 메서드들을 정의하고, type을 반환한다.
  - 서버에서는 위와 같은 명세를 구현하고 gRPC 서버를 실행시킨다.
  - 클라이언트는 stub을 통해 gRPC 서버와 통신한다.



### Protocol Buffers

- Protocol Buffers
  - Google에서 개발한 IDL이다.
    - Open source로 개발되었다.
  - 구조화된 데이터를 직렬화하는 데 사용한다.
  - 일반적인 text 파일과 동일하지만, `.proto`라는 확장자를 지닌다.



- 개요

  - 구조 정의하기
    - 직렬화 하려는 데이터의 구조를 정의한다.
    - `message`라는 키워드를 사용하며, field라 불리는 name-value 쌍으로 정의한다.

  ```protobuf
  message HelloRequest {
    string name = 1;
  }
  
  message HelloReply {
    string message = 1;
  }
  ```

  - 서비스 정의하기
    - `message` 키워드를 통해 정의해둔 데이터들로 RPC method parameter들과 return type을 정의한다.

  ```protobuf
  service Greeter {
    rpc SayHello (HelloRequest) returns (HelloReply) {}
  }
  ```

  - 컴파일하기
    - protocol buffer compiler(`protoc`)을 통해 proto 파일을 컴파일한다.
    - 자신이 원하는 언어로 컴파일이 가능하며 컴파일 과정을 통해 message를 통해 정의한 데이터에 접근할 수 있는 방법과, raw bytes로 직렬화하거나 parsing하는 메서드가 각 언어에 맞게 생성된다.







# Session과 JWT

> https://jwt.io/introduction

- 사용자 인증에 사용되는 두 가지 방식이다.
  - [쿠키, 세션, 웹 스토리지, IndexedDB]에서 본 것과 같이 HTTP는 기본적으로 stateless하다.
  - 그러나 사용자 정보와 같이 지속적으로 유지되야 하는 정보가 존재한다.
    - 클라이언트가 서버에 요청을 보낼 때마다 로그인을 할 수는 없다.



- 기존에는 session 방식을 사용했으나 최근에는 JWT 방식을 많이 사용한다.
  - 각각의 장단점이 있으므로 서비스에 더 적합한 방식을 택하면 된다.



## Session 방식

- Session 방식의 인증 과정은 다음과 같다.
  - Client(browser)가 server로 login 요청을 보낸다.
  - Server는 username과 password 등을 확인하고 일치하면 Session(DB 혹은 Redis 등 데이터를 저장하고 key값 기반으로 데이터를 조회할 수 있는 저장소)에 key, value, expire_date 등을 저장한다.
  - Server는 session_id(key)를 client에 반환하고, client는 해당 정보를 cookie에 저장한다.
  - 이후, 인증이 필요한 요청을 서버로 보낼 때마다,  session_id를 함께 보낸다.
  - 서버는 session_id가 유효한지 확인하고, session_id로 session에 저장된 data를 조회하여 처리 후 client에 응답을 보낸다.



- 장점
  - Client가 가지고 있는 정보는 session_id뿐이므로 중간에 탈취 당해도 정보 유출의 위험이 없다.
  - 서버단에서 session에 대한 통제가 가능하다(예를 들어 모바일과 데스크탑의 동시 접속을 막으려고 할 경우 이미 한 기기에서 로그인한 사용자라면 해당 기기로 발급된 session을 삭제하고 새로운 기기에 대한 session을 생성하면 된다).



- 단점
  - 사용자 수가 증가하면 session도 늘려줘야한다.
  - 매 요청마다 session을 조회해야 한다.



## JWT 방식

> https://jwt.io/introduction
>
> https://velopert.com/2389

- JWT

  - 안전한 정보 교환을 위한 개방형 규약([RFC 7519](https://tools.ietf.org/html/rfc7519))이다.
    - 정보를 주고 받을 때, JSON object를 활용한다.
    - 자가수용적(Self-contained)인 특징을 가지고 있어, JWT 토큰 자체에 전달하고자 하는 데이터, 검증할 수 있는 서명 데이터 등이 모두 포함되어 있다.
    - 정보가 전자 서명되어 있어 검증이 가능하고 신뢰할 수 있다.
    - HMAC 알고리즘을 사용하는 비밀키나  RDS 또는 ECDSA와 같은 공개키, 개인키 쌍으로 서명될 수 있다.
  - 형식
    - JWT는 Header, Payload, Signature의 세 부분으로 구성된다.
    - 각 부분은 `.`으로 나뉜다.
    - 


  ```bash
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
  ```

  - JWT의 목적은 데이터 자체를 보호하는 것이 아니다.
    - JWT의 목적은 데이터가 인증된 소스에서 생성되었음을 sign을 통해 증명하는 것이다.
    - Token에 서명을 하면 변조로부터 보호되지만 누구나 읽을 수 있다. 
    - 실제로 header, payload는 어떠한 암호화도 거치지 않고 단지 encoding만 된 상태이기에, decoding만 하면 누구나 정보를 볼 수 있다.
    - 따라서, JWT의 header 또는 payload에 담은 정보가 암호화되지 않은 경우 header 또는 payload에 비밀 정보를 넣어선 안 된다.



- Header

  - JWT를 어떻게 계산할 것인지에 대한 정보가 담겨 있다.
  - 일반적으로 token의 type과 sign 알고리즘(e.g. HMAC SHA256 or RSA.)에 대한 정보가 담겨 있다.

  ```json
  {
    "alg": "HS256",
    "typ": "JWT"
  }
  ```

  - 위 정보를 base64Url로 encoding한다.

  ```bash
  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
  ```



- Payload

  - 실제로 전달하고자 하는 정보가 담겨있는 부분이다.
  - Claim이 담겨 있는데, claim이란 entitiy와 그에 대한 추가적인 정보를 담고 있는 조각을 의미한다.
    - 즉 name, value의 한 쌍을 claim이라 부르고, name을 entity라 부른다.
  - Claim에는 3가지 종류가 있다.
    - Registered claims: 꼭 토큰에 포함시켜야 하는 것은 아니지만, 토큰에 포함시키는 것을 추천하는 claim들로, JWT 스펙에 정의되어 있는 claim들이다. iss(issuer), exp(expiration time), sub(subject), aud(audience) 등이 이에 속한다.
    - Public claims: JWT를 사용하는 사람들이 정의하는 claim들이다. 충돌을 피하기 위해서  [IANA JSON Web Token Registry](https://www.iana.org/assignments/jwt/jwt.xhtml)나 URI로 정의한다.
    - Private claims: JWT를 사용하여 통신을 주고 받는 당사자들이 협의한 claim들이다.

  ```json
  {
    "sub": "1234567890",
    "name": "John Doe",
    "iat": 1516239022
  }
  ```

  - 위 정보를 base64Url로 encoding한다.

  ```bash
  eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ
  ```



- Signature

  - 생성 과정
    - Header를 base64Url로 encoding한 값과, payload를 base64Url로 encoding한 값을 `.`을 사이에 두고 합한다.
    - 비밀키와 header에서 `alg`에 지정한 암호화 알고리즘을 사용하여 생성한다.

  ```json
  // Signature를 생성하는 슈도코드
  HMACSHA256(
    base64UrlEncode(header) + "." +
    base64UrlEncode(payload),
    your-256-bit-secret
  )
  ```

  - 위 정보를 base64Url로 인코딩한다.

  ```bash
  SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
  ```



- 인증 과정
  - Client에서 Server로 사용자의 인증 정보를 전송한다.
  - Server는 인증 정보가 정확한지 확인 후 JWT를 생성하여 client에 전달한다.
  - Client는 이를 어딘가(client의 플랫폼에 따라 다르다)에 저장한다.
  - 이후부터 발생하는 모든 인증이 필요한 요청에 JWT를 담아서 Server로 보낸다.
  - 서버는 JWT를 비밀키를 통해 JWT의 signature를 검증하여 변조 여부를 확인하고, 이상이 없으면  JWT로부터 사용자 정보를 추출한다.



- 장점
  - 서버에서 관리하지 않으므로, 사용자가 늘어 JWT를 많이 발급해도 서버의 자원 사용이 증가하지 않는다.
  - 쿠키가 아닌 다른 곳에 저장(일반적으로 local storage)이 가능하므로 쿠크릴 사용할 수 없는 모바일 애플리케이션 등에서도 사용이 가능하다.



- 단점
  - Payload, Header등이 암호화되지 않은 상태로 그대로 노출되므로, 개인정보가 담길 경우 위험할 수 있다.
  - 서버에서 JWT를 저장하는 것이 아니므로, 서버에서 발급된 순간 서버가 통제할 수 있는 방법이 없다.
    - 예를 들어, 특정 사용자를 강제로 로그아웃 시킬 경우, 세션 기반 인증에서는 해당 시용자의 세션을 삭제하면 그만이지만, JWT 방식에서는 불가능하다.



- JWT의 보안 전략
  - 만료 기한을 최대한 짦게 설정한다.
    - 토큰이 탈취되더라도 빠르게 만료되기에 피해를 최소화 할 수 있다.
    - 사용자가 자주 로그인해야 한다는 문제가 있다.
  - Sliding Session
    - Client가 JWT를 server로 보낼 때 마다 JWT의 갱신을 요청하는 방법이다.
    - 매 요청마다 갱신이 이루어지도록 할 수도 있고, 글 쓰기, 결제 등 중간에 인증이 만료되선 안 되는 작업에만 한정적으로 적용할 수도 있다.
  - Refresh Token
    - 최초 토큰을 생성할 때, Access Token과 Refresh Token을 발급하는 방법이다.
    - Client가 만료된 Access Token으로 Server와 통신을 진행하다 Access Token이 만료된다.
    - Server는 client에 access token이 만료되었다는 응답을 보내고, client는 access token보다 유효기간이 긴 refresh token을 server로 보내 access token의 발급을 요청한다.
    - Server는 client가 보낸 refresh token이 server에 저장된 refresh token과 비교하여, 유효한 경우 새로운 access token을 발급하고, 유효하지 않은 경우 다시 로그인을 요구한다.
    - 서버가 refresh token을 관리하므로 refresh token을 만료시켜 access token의 재발급을 막을 수 있다는 장점이 있다.
    - 그러나 refresh token을 어딘가에 저장하고 조회해야 하기에 I/O가 발생하고, 이는 JWT의 장점을 충분히 활용하지 못하는 것이다.
    - 또한 client는 refresh token이 탈취되지 않도록 추가적인 처리가 필요하다.





# text encoding

- encoding
  - 컴퓨터는 전기 신호로 정보를 표현한다.
    - 전기 신호가 있으면 1, 없으면 0이 되며 이 신호의 유무가 데이터의 최소 단위가 되고 이를 비트(bit)라 한다.
    - 하나의 비트는 0 또는 1만 표현할 수 있기 때문에 다양한 데이터를 표현하는 것은 불가능하다.
    - 따라서 다양한 데이터를 표현하기 위해서 여러 비트를 하나로 묶은 byte라는 단위를 사용한다.
    - 바이트란 일정한 개수의 비트로 이루어진 연속된 비트열로, 바이트를 구성하는 비트의 개수가 정해진 것은 아니지만 일반적으로 8비트를 1바이트로 사용한다.
    - 한 개의 비트는 0 또는 1이라는 2개의 정보를 표현할 수 있는데 이를 8개로 묶으면 256(2의 8승)가지의 정보를 표현할 수 있다.
  - 문자열 역시 byte로 표현되는데, 문자를 byte로 변환하는 것을 encoding이라 부른다.



- ASCII(American Standard Code for Information Interchange)

  - 이름에서 알 수 있듯이 미국에서 정의한 부호 체계이다.

  - 7비트로 문자를 표현한다.

    - 즉 128개의 문자를 표현할 수 있으며, 33개의 출력 불가능한 제어 문자들과 95개의 출력 가능한 문자들로 이루어져 있다.
    - 제어문자들의 대부분은 더 이상 사용되지 않는다.
    - 95개의 문자는 52개의 영문 알파벳 대소문자와 10개의 숫자, 32개의 특수문자, 하나의 공백 문자로 구성된다.

    - 8비트가 아닌 7비트를 사용하는 이유는 1비트는 통신 에러 검출을 위해 사용하기 때문이며, 이를 위해 사용되는 비트를 Parity bit라 부른다.



- ANSI(American National Standards Institute) 코드
  - American National Standards Institute에서 만든 문자 코드이다.
  - ASCII 코드만으로는 영어가 아닌 언어를 표현하기에는 부족하다.
    - 따라서 1bit를 추가하여 0~127까지는 기존의 ASCII코드와 동일한 문자를 할당하고 나머지 128개로 각 나라의 문자를 표현하는 방식으로 만들었다.
  - 특정 인코딩 방식을 말하는 것이 아니라 code page를 의미한다.
    - 각 언어별로 code page가 존재하며, 어떤 코드 페이지를 사용하는 가에 따라 정의된 문자가 달라진다.
    - 예를 들어 cp949는 한글을 위한 code page이다.
  - EUC-KR
    - 한글을 위한 code page로 완성형 코드 조합이다.
    - 완성형 코드란 완성된 문자 하나하나 코드 번호를 부여한 것이다. 반대 개념으로 조합형 코드가 있다. 예를 들어 "감"이라는 문자가 있을 때  "ㄱ", "ㅏ", "ㅁ"에 각기 코드를 부여하고 이를 조합하여 만드는 것이 조합형, "감"이라는 문자 자체에 코드를 부여한 것이 완성형 코드이다.
    - ASCII에 속한 문자들은 1byte, 한글은 2bytes로 표현하는 가변 길이 인코딩 방식이다.
  - cp949
    - MS에서 EUC-KR을 확장하여 만든 완성형 코드 조합이다.



- Unicode
  - 등장 배경
    - 1byte로 표현 불가능한 언어들(자음과 모음의 조합으로 한 글자가 완성되는 한글, 1만자가 넘어가는 한자가 존재하는 중국어 등)이 존재.
    - ANSI 방식의 경우도 각 언어마다 각기 다른 code page를 지니고 있어 사용에 여러 언어를 동시에 사용하는 데 불편함이 있었다.
    - 이와 같은 문제를 해결하기 위해 세상의 모든 언어를 하나의 코드 표에 담은 unicode가 등장했다.
  - 총 1,114,112개의 문자를 표현 가능하다.
    - 따라서 기본다중언어판(BMP, Basic Multilingual Plane)이라 불리는 16비트(2bytes) 영역에 모든 문자를 집어넣을 수 있으리라 생각했다.
    - 그러나 고어, 사어, 각종 특수 문자등으로 인해 65,536개로도 부족하게 되었다.
    - 이에 따라 BMP의 2048자를 대행 코드 영역(Surrogates)으로 할당하고, 이 중 1024자를 상위 대행(high surrogates), 1024자를 하위 대행(low surrogates)로 정의하여 이 둘의 조합으로 다시 1,048,576자를 추가로 정의할 수 있도록 했다.
    - 따라서 기존의 65,536+추가된 1,048,576으로 총 1,114,112개의 문자를 표현 가능해졌다.
  - 유니코드는 전체 공간이 17개의 판(plane)으로 나뉘어 있다.
    - unicode가 표현할 수 있는 전체 문자의 수 인 1,114,112를 2bytes로 표현할 수 있는 문자의 수인 65,536로 나누면 17이 된다.
    - 1개의 BMP와 16개의 보충언어판(SMP, Supplementary Multilingual Plane)로 구성된다.



- UTF(Unicord Transformation Format)
  - 이름에서도 알 수 있듯 unicode로 인코딩하는 방식이다.
  - 뒤에 숫자가 붙는데 이 숫자는 몇 bit를 1byte로보고 인코딩 할 것인지를 의미한다.
    - 예를 들어 UTF-8은 8bit를 1byte로 보고 인코딩한다.
  - UTF-8 
    - 일반적으로 가장 많이 쓰이는 인코딩 방식이다.
    - 문자를 1byte~6bytes까지 가변적으로 인코딩하는 방식.
    - 예를 들어 ASCII 코드상의 문자들은 1bytes로, 아시아 문자는 3bytes로 인코딩한다.
    - 표현 가능한 길이는 최대 66bytes지만 다른 인코딩과의 호환을 위해 46bytes까지만 사용한다.





# Shorts

- statement(문)와 expression(표현식)
  - expression
    - 하나 이상의 값으로 표현될 수 있는 코드를 말한다.
    - 평가가 가능해서 하나의 값으로 환원된다.
    - 예를 들어 `3+3`이라는 표현식은 평가 된 후 6이라는 값으로 환원된다.

  - statement
    - 실행 가능한 최소한의 독립적인 코드 조각을 말한다.
    - 표현식과 달리 평가와 평가에 따른 값의 환원이 존재하지 않는다.

  - expression은 statement에 포함되는 개념이다.
    - 즉 statement 중 평가되어 값을 반환하는 것들을 expression이라 부른다.




- 컴파일과 런타임
  - 컴파일: 소스 코드를 작성하고 해당 소스 코드를 기계어 코드로 변환하여 실행 가능한 프로그램이 되기 위한 편집 과정.
  - 런타임: 컴파일 과정을 마친 프로그램은 사용자에 의해 실행되며, 이러한 응용프로그램이 동작되는 시점을 런타임이라 부른다.




- 컴파일과 인터프리터
  - 컴파일러: 한 언어에서 다른 언어로 번역하는 역할을 수행, 프로그래밍 언어를 기계어 혹은 바이트 코드 등으로 번역하는 역할에 국한된 의미가 아니다 Java를 C로 번역한다면 이 역시 컴파일이라 할 수 있다.
    - 컴파일러가 실행되면 프로그래밍 언어를 번역해서 하나의 바이너리(혹은 어셈블리)파일로 저장하고 실제 프로그래밍 실행(런타임)은 이 파일을 실행함으로써 일어난다.
    - 즉 통으로 번역하고 번역한 파일을 실행한다.
    - 장점: 바이너리를 실행하기에 실행 속도가 인터프리터에 비해 빠르다.
    - 단점: 수정사항이 생길 때 마다 다시 컴파일을 진행해야 한다.
    - C, C++, Java 등은 컴파일 언어에 속한다.
    - Java의 경우 약간은 애매한 측면이 있다 컴파일러로 통으로 번역을 해 .class 파일을 생성한 뒤 .class 파일을 인터프리터를 통해 한 줄씩 실행한다.
  - 인터프리터:  번역해야 할 파일을 받아 한 줄씩 실행시키는 역할을 수행
    - 한 줄씩 번역하고 한 줄씩 실행한다.
    - 장점: 컴퓨터 마다 컴파일을 해주지 않아도 된다(플랫폼 독립적이다)
    - 단점: 컴파일 언어에 비해 속도가 느리다.
    - Python, Javascript, Ruby 등이 인터프리터 언어에 속한다.



- 배치 프로그램(Batch Program)

  - 정의: 사용자와 상호 작용 없이 일련의 작업들을 작업 단위로 묶어 정기적으로 반복 수행하거나 정해진 규칙에 따라 일괄 처리하는 방법

  - 배치 프로그램의 필수 요소
    - 이벤트 배치: 사전에 정의해 둔 조건 충족 시 자동으로 실행
    - 온디맨드 배치: 사용자의 명시적 요구가 있을 때마다 실행
    - 정기 배치: 정해진 시점(주로 야간)에 정기적으로 실행
  - 배치 스케줄러
    - 일괄 처리를 위해 주기적으로 발생하거나 반복적으로 발생하는 작업을 지원하는 도구.



- 데이터 마이닝(Data Mining)
  - 정의: 대용량의 데이터로부터 사용자의 요구사항에 맞는 의미있는 정보와 지식을 분석하여, 추출하는 방법
  - 등장 배경
    - 기술적 측면: 프로세싱 속도 및 자료저장 구조, 기계학습(ML)기술의 발전, 대량의 데이터 축적 및 데이터마이닝 도구의 발전
    - 비즈니스 측면: Mass 마케팅에서 Target 마케팅으로 패러다임 변화, 대량의 데이터로부터 의미있는 정보 추출을 통한 기업의 새로운 비즈니스 창출/개선/활용.



- 웹 마이닝(Web Mining)
  - 정의: 웹 환경에서 얻어지는 웹 문서, 고객의 정보 및 데이터로부터 특정 행위, 패턴 등의 유용한 정보를 이용하여 마케팅 및 의사결정에 활용하기 위한 마이닝 기법
  - 특징
    - 대용량: 대량의 웹로그를 기반으로 정보를 수집, 자료를 정제 및 클리닝 수행
    - 실시간성: Batch 작업(데이터를 실시간으로 처리하는 것이 아닌 일괄적으로 처리) 성격이 강한 일반 데이터 마이닝과 구별
    - One-to-One: 고객 행위 분석을 통한 개인화 지향(데이터 마이닝은 일반화)
    - 마이닝 기법: 신경망, 연관성, 순서화, 군집화, 의사결정 등에 마이닝 기법 사용



- BCP(Business Continuity Planning)
  - 정의: 지진, 홍수, 천재지변 발생 시, 시스템의 복구, 데이터 복원 등과 같은 단순 복구를 포함하여 기업 비즈니스의 연속성을 보장할 수 있는 체계
  - 등장 배경
    - 재해 대비 시스템 복구 기능이 정보시스템의 필수 요소로 인식되기 시작
    - 기업의 IT 시스템 안정성에 대한 법적 규제가 강화되는 추세
    - 시스템 중지로 인한 영업손실 방지
    - 재해 발생 시 조직 및 개인의 업무 정의 필요
    - 고객 정보 보호 및 업무 연속성 확보를 위한 안정장치 마련
    - 시스템 중단 시 발생하는 기업 이미지 실추 예방
  - 주요 계획
    - 재해 예방: 재해 발생 전 재해 발생 요인에 대응, 위기 관리를 통해 사전에 위기를 정성적, 정량적으로 분석
    - 대응 및 복구: 재해에 대한 정성적, 정량적 평가 항목을 도출, BIA(Business Impact Analysis)를 통한 파급 효과 분석 및 대응 방안 수립, Contingency Plan을 통한 복구 수립



- BCM(Business Continuity Management)
  - 정의: 예기치 않은 상황에서도 비즈니스를 지속적으로 운영하여 비즈니스의 연속성을 보장할 수 있는 경영 방식
  - 특징
    - 복원 능력(Resilience): 업무 중단 발생 시 견뎌낼 수 있는 능력
    - 반복 훈련(Simulation): 계획이 예상대로 수행되고 개선됨을 보장
    - 업무 중단 관리: IMP(Incident Management Plan, 사고 확산 통제), BCP를 통해 업무 중단 관리



- DRS(Disaster Recovery System)
  - 정의: 정보 시스템에 대한 비상 대비체계 유지와 각 업무 조직별 비상사태에 대비한 복구계획 수립을 통한 업무 연속성을 유지할 수 있는 체제
  - 필요성
    - 재해 상황에서 재해복구를 통한 서비스 연속성 확보
    - 연속성 확보를 통한 기업 신뢰도 확보
  - 구축 절차
    - 1단계: 업무 영향 분석
    - 2단계: 재해 복구 전략 수립
    - 3단계: 시스템 구축 및 복구 계획 수립
    - 4단계: 운영 및 모의 훈련



- BIA(Business Impact Analysis)
  - 재해 발생시 영향을 미칠 수 있는 위험을 정의하고, 업무 중단 영향에 대한 정량적, 정성적 분석을 통해 복구 우선순위를 도출하는 과정
  - 목적
    - 핵심 우선순위 결정: 모든 핵심점 사업의 프로세스에 우선순위를 부여함
    - 중단 시간 산정: 경쟁력 있는 기업으로 살아남기 위해 견딜 수 있는 최장시간의 산정
    - 자원 요구: 핵심 프로세스에 대한 지원 요구사항 정의, 시간에 민감한 프로세스에 대부분의 자원을 할당



- 클라우드 컴퓨팅

  - 정의: 하드웨어, 소프트웨어, 데이터 등의 IT 자원이 웹을 통해 표준화된 서비스의 형태로 제공되는 모델 

  - 클라우드로 제공되는 서비스에 대해 사용자는 언제, (IP지원이 되는) 어떤 장비를 통해서든, 원하는 만큼의 서비스를 골라서 사용할 수 있으며, 사용량에 기반하여 비용을 지불하는 비즈니스 모델

  - 3가지 서비스 모델

    > 사진 출처: https://www.redhat.com/ko/topics/cloud-computing/what-is-paas

    ![iaas-paas-saas-diagram](https://user-images.githubusercontent.com/60123095/108083318-4641ac80-70b6-11eb-9b4a-3cb3401ab225.png)

    - SaaS(Software as a Service)
    - PaaS(Platform as a Service)
    - IaaS(Infrastructure as a Service)

  - 4가지 전개 모델

    - Private Cloud: 자사의 내부에 직접 클라우드 인프라를 구축하여 내부에 소속된 사람만 이용
    - Community Cloud: 공통의 관심사를 가진 특정 커뮤니티의 여러 조직이 클라우드를 함께 이용
    - Hybrid Cloud: 내부에 사설 클라우드를 구축하여 운영하다가 필요에 따라 외부의 공용 클라우드를 함께 이용 하는 것
    - Public Cloud: 누구나 함께 이용할 수 있게 구축된 대규모 클라우드서비스

  - 5가지 특징

    - 사용자 중심 서비스: 사용자가 사용한 만큼 비용을 지불
    - 네트워크 접근: 네트워크 기반의 서비스
    - 신속한 서비스 제공
    - 계량 가능한 서비스
    - 컴퓨팅 자원 공유

  - 모바일 클라우드

    - 클라우드 컴퓨팅을 모바일 서비스에 접목시킨 것
    - 구성: 단말, 애플리케이션 제공자, 클라우드 컴퓨팅



- NoSQL	
  - 전통적인 관계형 데이터베이스 보다 덜 제한적인 일관성 모델을 이용하는 데이터의 저장 및 검색을 위한 매커니즘을 제공
  - NoSQL 데이터베이스는 단순 검색 및 추가 작업을 위한 매우 최적화된 키 값 저장 공간.
  - Not only SQL이라 불리기도 한다.
  - MongoDB가 대표적이다.



- TPS(Transaction for second)
  - 초당 트랜잭션의 개수
  - 일정 기간동안 실행된 트랜잭션의 개수를 구하고 다시 1초 구간에 대한 값으로 변경하여 구한다.



- boiler plate code
  - 판에서 찍어낸 듯한 코드라는 의미이다.
  - 아래 조건을 만족하는 코드를 일컫는다.
    - 꼭 필요하고 간단한 기능을 위한 코드다.
    - 반복적으로 사용해야 하는 코드다.
    - 중복되어 많은 양의 코드가 생산된다.



-  스키마(Schema)과 스킴(Scheme)
   - 스키마는 대략적인 계획이나 도식을 뜻한다.
   - 스킴은 구체적이고 확정된 것을 말한다.



- 오버헤드
  - 어떤 처리를 하기 위해 들어가는 간접적인 처리 시간, 메모리 등을 말한다.
  - 예를 들어 A라는 처리를 단순하게 실행한다면 10초가 걸리는데, 안전성을 고려하고 부가적인 B라는 처리를 추가한 결과 처리시간이 15초 걸렸다면, 오버헤드는 5초가 된다.



- mongkey patch

  - 런타임에 프로그램의 특정 기능을 수정하여 사용하는 기법.

    - test를 위해서가 아니라면 지양하는 것이 좋다.
    - 아래 예시를 보면 알 수 있듯, 코드를 예상치 못하게 동작하게 하므로 지양해야 한다.
    - 다만, test 할 때에는 예외로, 만일 의존성을 가지는 함수(예를 들어 API에 요청을 보내 그 응답을 받아오는 함수)를 monkey patch를 통해 다른 함수로 대체하도록 변경하는 등의 방식으로 활용이 가능하다.

  - 어원

    - 원래 이름은 게릴라 패치였다.

    - 이를 발음이 비슷한 고릴라 패치라고 부르다가, 고릴라의 어감이 너무 크고 거대한 느낌이 들어 보다 작은 종인 몽키 패치로 변경되었다.

  - 예시

  ```python
  class Monkey:
      def like_banana(self):
          print("I like banana!")
      
      def hate_banana(self):
          print("I hate Banana")
  
  Monkey.like_banana = hate_banana
  monkey = Monkey()
  monkey.like_banana() # I hate Banana
  ```

  