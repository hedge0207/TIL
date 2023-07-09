# Semantic Versioning Specification

> https://semver.org/

- Semantic Versioning specification(SemVer)
  - 소프트웨어의 버전 번호를 어떻게 정하고, 증가시킬지에 관한 명세이다.
  - Gravatars의 창시자이자 github 공동 창업자인 Tom Preston Werner가 작성했다.
  - 만든 이유
    - 시스템의 규모가 커지고 의존성이 높아질수록, 시스템을 구성하는 각기 다른 패키지들의 버전을 관리하는 것이 힘들어진다.
    - 의존성 관리를 너무 엄격하게 하면 의존하는 모든 패키지의 새 버전을 배포하지 않고는 업데이트를 할 수 없게 되고, 너무 느슨하게 관리하면, 서로 버전이 엉켜 문제가 발생한다.
    - 따라서, 버전 번호를 어떻게 정하고 증가시킬지를 명시함으로써 의존성 관리를 보다 쉽게 하는 데 그 목적이 있다.
  - 2012년 처음 작성되어 현재 널리 사용되고 있다.
    - Node의 npm이 대표적이다.
    - 모든 개념을 베르너가 처음 만든 것은 아니고, 기존 오픈소스 커뮤니티들에서 널리 사용되던 방식들을 취합하여 작성한 것이다.



- 명세
  - 유의적 버전을 사용하는 소프트웨어는 반드시 공개 API를 선언한다.
    - 이 API는 코드 자체로 선언하거나 문서로 엄격히 명시해야한다.
    - 어떤 방식으로든, 정확하고 이해하기 쉬워야 한다.
  - 버전 번호는 X.Y.Z의 형태로 한다. 
    - X,Y,Z는 각각 음이 아닌 정수이다. 
    - 절대로 0이 앞에 붙어서는 안된다(e.g. 01과 같이 사용하지 않는다).
    - X는 주, Y는 부, Z는 수버전을 의미한다.
    - 각각은 반드시 증가하는 수여야한다(즉, 감소해서는 안된다).
  - 특정 버전으로 패키지를 배포하고 나면, 그 버전의 내용은 절대 변경하지 말아야한다.
    - 변경분이 있다면 반드시 새로운 버전으로 배포하도록 한다.
  - 주버전 0(0.Y.Z)은 초기 개발을 위해서 사용한다.
    - 이 공개 API는 안정판으로 보지 않는게 좋다.
  - 1.0.0 버전은 공개 API를 정의한다.
    - 이후으 버전 번호는 이때 배포한 공개 API에서 어떻게 변경되는지에 따라 올린다.
  - 수버전 Z(x.y.Z | x > 0)는 반드시 그전 버전 API와 호환되는 버그 수정의 경우에만 올린다.
    - 버그 수정은 잘못된 내부 기능을 고치는 것을 의미한다.
  - 공개 API에 기존과 호환되는 새로운 기능을 추가할 때는 부버전 Y(x.Y.z | x > 0)를 올린다.
    - 공개 API의 일부가 앞으로 deprecate 될 것으로 표시한 경우에도 반드시 올려야한다.
    - 내부 비공개 코드에 새로운 기능이 대폭 추가되었거나 개선사항이 있을 때도 올릴 수 있다.
    - 부버전을 올릴 때 수버전을 올릴 때 만큼의 변화를 포함할 수도 있다.
    - 부버전이 올라가면 수버전은 반드시 0에서 다시 시작한다.
  - 공개 API에 기존과 호환되지 않는 변화가 있을 때는 반드시 주버전(X,Y,Z | X>0)을 올린다.
    - 부버전이나 수버전급 변화를 포함할 수 있다.
    - 주버전을 올릴 때는 반드시 부버전과 수버전을 0으로 초기화한다.
  - 수버전 바로 뒤에 `-`를 붙이고, 마침표로 구분된 식별자를 더해서 정식 정식 배포를 앞둔(pre-release) 버전을 표기할 수 있다.
    - 식별자는 반드시 아스키문자, 숫자, `-`만으로 구성한다(`[0-9A-Za-z-]`).
    - 식별자는 반드시 한 글자 이상으로 한다.
    - 숫자 식별자의 경우 절대 앞에 0을 붙인 숫자로 표기하지 않는다.
    - 정식배포 전 버전은 관련한 보통 버전보다 우선순위가 낮다.
    - 정식배포 전 버전은 아직 불안정하며 연관된 일반 버전에 대하 호환성 요구사항이 충족되지 않을 수도 있다.
  - 빌드 메타데이터는 수버전이나 정식배포 전 식별자 뒤에 `+`기호를 붙인 뒤에 마침표로 구분된 식별자를 덧붙여서 표현할 수 있다.
    - 식별자는 반드시 아스키 문자와 숫자, `-`만으로 구성한다(`[0-9A-Za-z-]`).
    - 식별자는 반드시 한 글자 이상으로 한다.
    - 빌드 메타데이터는 버전 간의 우선순위를 판단하고자 할 때 만드시 무시해야한다.
    - 그러므로, 빌드 메타데이터만 다른 두 버전의 우선순위는 갖다.
  - 우선순위는 버전의 순서를 정령할 때 서로를 어떻게 비교할지를 나타낸다.
    - 우선순위는 반드시 주, 부, 수 버전, 그리고 정식 배포 전 버전의 식별자를 나누어 계산한다(빌드 메타데이터는 우선순위에 영향을 주지 않는다).
    - 우선순위는 다음의 순서로 차례로 비교하면서, 차이가 나는 부분이 나타나면 결정된다.
    - 주, 부, 수는 숫자로 비교한다.
    - 주, 부, 수 버전이 같을 경우, 정식 배포 전 버전이 표기된 경우의 우선순위가 더 낮다(e.g. 1.0.0-alpha < 1.0.0).
    - 주, 부, 수 ㅈ버전이 같은 두 배포 전 버전 간의 우선순위는 반드시 마침표로 구분된 식별자를 가각 차례로 비교하면서 차이를 찾는다(숫자로만 구성된 식별자는 수의 크기로 비교하고 알파벳이나 `-`가 포함된 경우에는 아스키 문자열 정렬을 하도록 한다).
    - 숫자로만 구성된 식별자는 어떤 경우에도 문자와 `-`가 있는 식별자보다 낮은 우선순위로 여겨진다.
    - 앞선 식별자가 모두 같은 배포 전 버전의 경우에는 필드 수가 많은 쪽이 더 높은 우선순위를 가진다.



- 유의적 버전의 BNF(Backus-Naur Form) 문법

  ```
  <유의적 버전> ::= <버전 몸통>
               | <버전 몸통> "-" <배포 전 버전>
               | <버전 몸통> "+" <빌드>
               | <버전 몸통> "-" <배포 전 버전> "+" <빌드>
  
  <버전 몸통> ::= <주> "." <부> "." <수>
  
  <주> ::= <숫자 식별자>
  
  <부> ::= <숫자 식별자>
  
  <수> ::= <숫자 식별자>
  
  <배포 전 버전> ::= <마침표로 구분된 배포 전 식별자들>
  
  <마침표로 구분된 배포 전 식별자들> ::= <배포 전 식별자>
                                | <배포 전 식별자> "." <마침표로 구분된 배포 전 식별자들>
  
  <빌드> ::= <마침표로 구분된 빌드 식별자들>
  
  <마침표로 구분된 빌드 식별자들> ::= <빌드 식별자>
                              | <빌드 식별자> "." <마침표로 구분된 빌드 식별자들>
  
  <배포 전 식별자> ::= <숫자와 알파벳으로 구성된 식별자>
                  | <숫자 식별자>
  
  <빌드 식별자> ::= <숫자와 알파벳으로 구성된 식별자>
               | <숫자들>
  
  <숫자와 알파벳으로 구성된 식별자> ::= <숫자 아닌 것>
                               | <숫자 아닌 것> <식별자 문자들>
                               | <식별자 문자들> <숫자 아닌 것>
                               | <식별자 문자들> <숫자 아닌 것> <식별자 문자들>
  
  <숫자 식별자> ::= "0"
               | <양의 숫자>
               | <양의 숫자> <숫자들>
  
  <식별자 문자들> ::= <식별자 문자>
                 | <식별자 문자> <식별자 문자들>
  
  <식별자 문자> ::= <숫자>
               | <숫자 아닌 것>
  
  <숫자 아닌 것> ::= <문자>
                | "-"
  
  <숫자들> ::= <숫자>
           | <숫자> <숫자들>
  
  <숫자> ::= "0"
          | <양의 숫자>
  
  <양의 숫자> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
  
  <문자> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"
          | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"
          | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d"
          | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n"
          | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x"
          | "y" | "z"
  ```





# CNCF(Cloud Native Computing Foundation)

- Cloud Native
  - 클라우드 컴퓨팅 모델의 이점을 활용하는 애플리케이션 구축 방법론이다.
    - 클라우드가 제공하는 확장성, 탄력성, 복원성, 유연성 등의 이점을 활용하여 애플리케이션을 구축하는 방법론이다.
  - 애플리케이션이 클라우드에 상주하도록 애플리케이션을 설계한다.
  - Cloud Native를 적용한 애플리케이션을 클라우드 네이티브 앱이라고 부른다.
    - 클라우드 네이티브 애플리케이션은 아래와 같은 이점들이 있다.
    - 독립성: 클라우트 네이티브 앱을 서로 독립적으로 구축할 수 있도록 해준다.
    - 복원성: 인프라스트럭쳐가 중단되어도 온라인 상태를 유지할 수 있다.
    - 자동화: DevOps 자동화 기능을 사용하여 정기적으로 릴리스되는 소프트웨어 변경 사항을 지속적으로 전달 및 배포할 수 있다.
  - 클라우드 네이티브 아키텍처
    - 온프레미스 인프라가 아닌 클라우드에 존재하도록 특별히 설계된 애플리케이션 또는 서비스의 설계를 의미한다.
    - 성공적인 클라우드 네이티브 아키텍처는 유지보수가 용이하고, 비용 효율적이며 자가 복구가 가능하고, 높은 수준의 유연성을 가진다.



- CNCF
  - 클라우드 네이티브 기술의 채택을 촉진하는 오픈 소스 소프트웨어 재단.
    - 리눅스 재단이 설립하였다.
    - 퍼블릭 클라우드 공급 업체, 엔터프라이즈 소프트웨어 기업, 스타트업 등 400명 이상의 회원을 보유하고 있다.
    - 클라우드 네이티브 오픈소스들을 관리하고 장려하는 단체이다.
  - CNCF에서 관리되는 모든 프로젝트들은 성숙도 평가를 받아야 한다.
    - 성숙도에 따라 Sandbox, Incubating, Graduated라는 세 단계로 나뉜다.
    - 이 중 Graduated 단계의 경우 평가자 3분의 2이상의 찬성이 필요하다.
    - Graduated 프로젝트에는 Kubernetes(첫 Graduated 등급의 프로젝트), Prometheus, fluentd 등이 있다.





# Stream Backpressure

> https://doublem.org/stream-backpressure-basic/

- Backpressure(배압, 역압)
  - 파이프를 통한 유체 흐름에 반하는 저항을 말한다.
    - 액체나 증기가 관을 통해 배출 될 때, 유체가 흐르는 방향과 반대 방향으로 작용하는 저항 압력이다.



- 소프트웨어에서의 backpressure
  - 소프트웨어에도 Stream과 PIpe가 존재한다.
    - 두 용어 모두 유체의 흐름(stream)과 이를 이동시키는 pipe에서 따온 것이다.
    - 단지 내용물이 유체가 아닌 data라는 차이가 있을 뿐이다.
  - 마찬가지로, 소프트웨어에도 backpressure가 존재한다.
    - Data의 흐름이 일정치 않거나 예상치 못하게 높아질 경우 발생할 수 있다.
    - 예를 들어 A에서 B로 data를 옮길 때, B가 처리할 수 있는 데이터 양 보다 많은 양을 A가 지속적으로 보낼 경우 backpressure가 발생할 수 있다.
  - 소프트웨어에서 backpressure가 발생할 경우 아래와 같은 현상이 발생할 수 있다.
    - Network I/O
    - Disk I/O
    - Out of Memory
    - Drop data



- Backpressure를 방지할 수 있는 방법
  - Buffer를 사용하여 backpressure를 방지할 수 있다.
    - Buffer란 데이터를 한 곳에서 다른 곳으로 전송하는 동안 일시적으로 그 데이털를 보관하는 메모리 영역을 말한다.
    - Buffering이란 버퍼를 활용하는 것 혹은 버퍼를 채우는 것을 말한다.
    - 구현에 queue를 사용한다.
  - Pull 기반의 데이터 처리
    - Consumer가 처리할 수 있는 만큼만 producer로 부터 data를 받아와서 처리한 후 처리가 완료되면 다시 data를 받아오는 방식이다.



# Standard Stream, Standard Input, Output

> https://shoark7.github.io/programming/knowledge/what-is-standard-stream

- 표준 스트림
  - 컴퓨터 프로그램에서 표준적으로 입력으로 받고 출력으로 내보내는 데이터와 매체의 총칭.
  - Stream
    - 프로그램을 드나드는 데이터를 바이트의 흐름(stream)으로 표현한 단어이다.
    - 여러 종류의 하드웨어로부터 data를 읽어 오고, 일련의 처리를 거쳐서 이를 다시 출력하는 일은 매우 번거로운 일이었다.
    - Unix는 이런 번거로움을 해소하기 위해 장치를 추상화해서 각 장치를 파일처럼 다루는 것으로 이 문제를 해결했다.
    - 하드웨어의 종류별로 입력과 출력을 위한 설정을 따로 하는 대신, 파일을 읽고 쓰는 한 가지 작업으로 통일시킨 것이다.
    - 그리고 이 파일에서 읽히고 나가는 데이터를 stream이라고 정의했다.



- 표준 입출력
  - Standard
    - 많은 프로그램이 입력과 출력을 필요로 한다.
    - 만약 어떤 프로그램이 대부분의 입력과 출력이 한 출처로부터만 발생한다면, 사용자가 명시하지 않더라도 기본적으로 사용할 입력과 출력을 설정할 수 있으면 훨씬 간편할 것이다.
    - 이렇게 한 프로그램이 기본적으로 사용할 입출력 대상을 표준 입출력이라 한다.
  - 표준 입출력은 표준 입력과 표준 출력으로 나뉜다.
  - 표준 입력
    - 프로그램에 입력되는 데이터의 표준적인 출처를 일컬으며, stdin으로 줄여서 표현한다.
    - 유닉스 쉘에서는 표준 입력이 키보드로 설정되어 있다.
  - 표준 출력
    - 프로그램에서 출력되는 데이터의 표준적인 방향을 일컫는다.
    - 표준 출력(stdout)과 표준 에러(stderr)로 구분할 수 있다.
    - 유닉스에서는 표준 출력, 표준 에러 모두 콘솔로 설정되어 있다.
    - 표준 출력은 정상적인 출력이 반환되는 방향을 말하고, 표준 에러는 프로그램의 비정상 종료 시에 반환되는 방향을 말한다.



# 2진수 음수 표현

> https://st-lab.tistory.com/189

- 부호 절대값(Sign-Magnitude)
  - 최상위 비트(가장 왼쪽의 비트)를 부호로 사용하는 방법
    - 부호를 나타내는 최상위 비트를 MSB(Most Significant Bit)라 부른다.
    - 비트가 아닌 바이트를 사용하는 경우도 있는데, 이 경우 구분을 위해 MSBit, MSByte와 같이 표현한다.
    - MSB가 0이면 양수, 1이면 음수로 본다.
  - 예시
    - 10진수 5를 진수로 표현하면 0101이다.
    - 부호 절대값 방식을 적용하면, 최상위 비트에 음수를 뜻하는 1을 넣어 1101이 된다.
  - 문제
    - 0이 음수(1000)와 양수(0000)로 나뉜다.
    - 뺄셈을 위해 각 수가 음수인 경우와 아닌 경우를 고려해야한다.
    - 정확히는 뺄셈은 음수의 덧셈으로 구현되어 있으므로 음수의 덧셈을 위해 각 수가 음수인 경우와 아닌 경우를 고려해야한다.
    - 예를 들어 3-5는 3 + (-5)로 구현되어 있다.



- 부호 절대값 방식에서 음수의 덧셈
  - 두 수의 덧셈에서 음수가 포함되는 경우는 두 수 모두 음수인 경우, 두 수 중 하나만 음수인 경우가 있다.
  - 두 수 모두 음수인 경우는 상대적으로 간단한데, 아래와 같이 계산하면 된다.
    - 예를 들어 -3과 -5을 더하려고 한다고 하자.
    - -3은 이진수로 1000 0011, -5는 이진수로 1000 0101이다.
    - 두 수의 최상위 비트가 같다면 결과값의 최상위 비트도 같다.
    - 따라서 두 수의 합은 1000 1000이다.
  - 두 수 중 하나만 음수인 경우
    - 첫 번째 수의 절대값이 두 번째 수의 절대값보다 작을 경우 문제가 생긴다.
    - 예를 들어 -3과 5를 더하려고 한다고 하자.
    - -3은 이진수로 1000 0011, 5는 이진수로 0000 0101이다.
    - 이 때 두 수를 더하면 ?000 1000이 나온다.
    - MSB 자리에 1이 오면 -8, 0이 오면 8이 되는데, 어느 쪽이든 값이 아니다.
    - 정확한 값을 구하기 위해서는 뺄셈기를 구현해야한다.
  - 뺄셈을 하기위해서는 덧셈기 이외에 뺄셈기도 구현해야한다.
    - 그러나 비교적 간단하게 구현 가능한 덧셈기와 달리 뺄셈기는 고려해야 할 사항(MSB와 절대값을 따로 고려하여 계산해야 하는 등)이 많다.
    - 따라서 뺄셈기를 사용하지 않고 덧셈기만을 사용하여 뺄셈을 구현해야하는데, 부호 절대값 방식은 적절한 방식이 아니다.



- 보수
  - 보수(Complement)
    - 보충해주는 수로 어떤 수를 만들기 위해 필요한 수를 의미한다.
    - 즉 n의 보수는 어떤 수에 대해 n의 제곱수가 되도록 만드는 수이다.
    - n진법의 보수는 n의 보수와 n-1의 보수가 사용된다.
  - 10진법에서의 보수
    - 예를 들어 6에 대한 10의 보수는 6에서 10을 만들기 위한 어떤 수인 4다.
    - 또한 60에 대한 10의 보수는 60에서 100을 만들기위한 40이다.
    - n진법에서 n-1의 보수는 n의 보수에서 -1을 한 값이 된다.
    - 즉 60에 대한 9의 보수는 60에 대한 10의 보수인 40에서 1을 뺀 39가 된다.
    - 이를 조금 바꾸어 표현하면 다음과 같이 표현할 수 있다.
    - (100-1) - 60 = 99 - 60 = 39
    - 즉 10의 제곱수에서 1을 뺀 값에서 보수를 구하려는 수를 빼면 9의 보수를 얻을 수 있다.
  - 보수를 음수 덧셈에 활용
    - 보수를 사용하여 뺄셈이 가능한데, 이를 사용하면 음수, 양수 상관 없이 덧셈만으로 뺄셈이 가능해진다.
    - 예를 들어 -3+5를 먼저 10진법으로 보수를 사용하여 계산해보면 다음과 같다.
    - 보수를 구할 때 부호는 무시하므로 -3의 10에 대한 보수는 3에 대한 10의 보수와 같고, 3에 대한 10의 보수는 10-3=7이다.
    - 이 때 +10은 보수를 구하기 위한 값이므로 다시 빼줘야한다.
    - 결국 정리하면 {(10-3) + 5} - 10 = (7+5) -10 = 2가 된다.
    - 우리의 목적은 뺄셈 없이 덧셈 만으로 뺄셈을 구현하는 것이므로 -10을 빼는 과정을 없애준다(보수를 구할 때 뺄셈을 하는 것은 당장은 무시한다).
    - 만약 보수를 구하기 위해 더해준 10을 다시 빼지 않으면 12가 되는데, 여기서 가장 왼쪽 값인 1은 올림으로 발생한 수이다.
    - 이 같은 자리 올림을 캐리라고 한다.
  - 캐리(Carry)
    - 최상위 비트 MSB에서 자리 올림이나 자리 빌림이 있는 것을 의미한다.
    - 캐리가 발생했을 경우(양수일 경우) 자리 올림된 값을 버리면 최종 결과값을 얻을 수 있다(12에서 자리올림된 값인 1을 버리면 답인 2만 남는다).
    - **보수를 더했을 때** 캐리가 발생할 경우 값은 양수가 되고, 캐리가 발생하지 않을 경우 값은 음수가 된다.
  - 10진수의 보수 덧셈에서 캐리가 발생하지 않을 경우
    - 10진수의 보수 덧셈에서 캐리가 발생하지 않을 경우(음수일 경우) 해당 값의 보수값에 음수 부호를 붙인 값이 최종 결과값이 된다.
    - 예를 들어 -5 + 3의 경우 -5에 대한 5의 보수는 5이므로 5+3와 같이 계산할 수 있고 이 결과값은 8이다.
    - 캐리가 발생하지 않았으므로 음수이고, 8의 보수인 2를 구한 뒤 음수 부호를 붙이면 최종 결과값은 -2가 된다.
  - n-1의 보수를 사용할 경우 캐리가 발생했다면 결과값에서 1을 더해줘야 최종 결과값을 얻을 수 있다.
    - 예를 들어 9의 보수를 사용하여 -3+5를 계산한다고 해보자.
    - (9 - 3) + 5 = 11이고, 캐리가 발생했으므로 1을 떼면 1이 된다.
    - n-1의 보수인 9의 보수를 활용했으면서 캐리가 발생했으므로 결과 값에 1을 더해주어 최종 결과값은 2가 된다.
  - 보수를 음수 덧셈에 활용하는 이유
    - 보수를 활용하여 음수 덧셈을 하는 과정은 아래와 같다.
    - 음수에 대한 보수를 구한다 → 구한 보수 값에 다른 수를 **더한다** → 올림이 발생할 경우 해당 수는 버린다.
    - 따라서 음수에 대한 보수를 활용하면 덧셈만을 활용하여 뺄셈도 가능해진다.
    - 결국 보수를 구할 때 뺄셈을 하게 되는 것 아닌가 하고 생각할 수도 있지만 이는 10진수라서 그렇다.
    - 2진법에서는 뺄셈 없이 보수를 구할 수 있다.
    - 따라서 더 정확히는 2진법에서 보수를 사용하면 덧셈만으로 뺄셈이 가능해진다.



- 1의 보수법(One's Complement)
  - 1의 보수 구하기
    - 1의 보수는 2의 제곱수에서 1을 뺀 값에서 보수를 구하려는 값을 빼면 구할 수 있다.
    - 예를 들어 이진수 0011(10진수 3)의 보수를 구하려 한다고 가정해보자.
    - 1111은 2의 제곱수인 16에서 1을 뺀 십진수 15를 2진수로 표현한 것이다.
    - 1111에서 0011을 빼면 0011에 대한 1의 보수인 1100을 얻을 수 있다.
    - 계산시에 MSB는 계산에서 제외한다.
  - 캐리가 발생하지 않을 경우
    - 10진수와는 달리 2진수에서는 MSB로 양수, 음수 여부를 판별한다.
    - 따라서 캐리가 발생하지 않았다 하더라고 보수를 다시 구할 필요가 없다.
  - 1의 보수는 뺄셈 없이 구하는 것이 가능하다.
    - 위에서는 1111에서 0011을 빼는 방식으로 1의 보수를 구했다.
    - 그러나 자세히 살펴보면 0011에 대한 1의 보수는 결국 0011의 비트를 반전시킨 것일 뿐이다.
    - 따라서 뺄셈 없이 보수를 구하려는 값의 비트만 반전시키면 1에 대한 보수를 구할 수 있다.
  - 예시1. -3 + 5
    - 8비트 기준 -3은 2진수로 1000 0011이고, 5는 0000 0101이다.
    - 이 때 -3에 대한 1의 보수는 MSB를 제외하고 모두 반전시켜 구하면 1111 1100이 되고, 이 둘을 더하면 1 0000 0001이 된다.
    - 캐리가 발생했으므로 올림 값은 버린다(0000 0001이 된다).
    - n-1의 보수를 사용했고, MSB 자리를 넘어 캐리가 발생했으므로 결과값에 +1을 해준다.
    - 최종 결과 값은 0000 0010(2)이 된다.
  - 예시2. -3 + -5
    - 8비트 기준 -3은 2진수로 1000 0011이고, -5는 1000 0101이다.
    - 두 값의 1의 보수를 구하면 1111 1100, 1111 1010이 되고, 이 둘을 더하면 1 1111 0110이 된다.
    - 캐리가 발생했으므로 올림 값은 버린다(1111 0110이 된다).
    - n-1의 보수를 사용했고, MSB 자리를 넘어 캐리가 발생했으므로 결과값에 +1을 해준다.
    - 최종 결과 값은 1111 0111(-8)이 된다.
  - 남아 있는 문제
    - 이제 뺄셈 없이 덧셈만으로 뺄셈이 가능해졌으므로 별도의 뺄셈기를 구현할 필요는 없여졌다.
    - 그러나 아직 남아 있는 문제가 있다. 
    - 하나는 부호 절대값 방식과 마찬가지로 1의 보수 표현도 0이 음수 0과 양수 0 두 개가 있다는 점이다.
    - 다른 하나는 1의 보수는 n-1의 보수이기 때문에 캐리가 발생하면 결과값에 +1을 해줘야 최종 결과값을 얻을 수 있다는 점이다.



- 2의 보수

  - 2의 보수 구하기
    - 이진수 0011의 2의 보수를 구하려고 한다고 가정해보자.
    - 2의 보수는 2의 제곱수에서 보수를 구하려는 값을 빼면 구할 수 있다.
    - 10000에서 0011을 빼면 1101이 된다.
  - 2의 보수 역시 뺄셈 없이 구하는 것이 가능하다.
    - 1의 보수의 문제느 음수 0이 존재하다는 것이었다.
    - 따라서 음수 0을 없애고 음수들에 +1씩을 해준다.
    - 즉 기존에 1의 보수에서는 1111(-0), 1110(-1), 1101(-2), ... 와 같이 2진수가 진행됐는데, -0을 없앴으므로 기존에 -1이었던 1110에 1을 더해 1111로, 기존에 -2였던 1101에 1을 더해 1110으로 만드는 식으로 모든 음수에 1씩 더해준다.
    - 결국 2의 보수는 1의 보수에 +1을 해준 것과 같다.

  - 예시1. -3 + 5
    - 8비트 기준 -3은 2진수로 1000 0011이고, 5는 0000 0101이다.
    - -3에 대한 2의 보수는 1111 1101이고, 이 둘을 더하면 1 0000 0010이 된다.
    - 캐리가 발생했음에도 +1을 더해주는 과정 없이 올림 된 부분만 버리면 값인 0000 0010을 얻을 수 있다.
  - 예시2. -3 + -5
    - 8비트 기준 -3은 2진수로 1000 0011이고, 5는 0000 0101이다.
    - -3에 대한 2의 보수는 1111 1101이고, -5에 대한 2의 보수는 1111 1011이고, 이 둘을 더하면 1 1111 0100이 된다.
    - 이번에도 마찬가지로 캐리가 발생했지만 +1을 더해주는 과정 없이 올림 된 부분만 버리면 값인 1111 0100을 얻을 수 있다.





## Method Dispatch

- Method Dispatch

  - 어떤 메서드를 호출할 것인가를 결정하고 실행하는 과정을 의미한다.
  - Static Method Dispatch
    - 컴파일 시점에 호출되는 메서드가 결정되는 method dispatch
    - 아래 코드에서 `foo()` 메서드는 아래 코드가 컴파일 되는 시점에 실행될 것이 결정된다.

  ```python
  def foo():
      return
  
  foo()
  ```

  - Dynamic Method Dispatch
    - 실행 시점에 호출되는 메서드가 결정되는 method dispatch
    - 아래의 경우 obj를 Abstract class type이라고 지정해줬기에 다른 코드는 보지 않고 `obj.foo()`만 봤을 때는 어떤 class의 `foo` method가 실행될지 컴파일 타임에는 알 수 없고, 런타임에 결정된다.
    - 또한 이 때 receiver parameter가 전달되는데, 이는 객체 자신이다(`self`와 동일하다).

  ```python
  from abc import ABCMeta
  
  class Abstract(metaclass=ABCMeta):
      pass
  
  class ConcreteA(Abstract):
      def foo(self):
          return
      
  class ConcreteB(Abstract):
      def foo(self):
          return
      
  obj: Abstract = ConcreteA()
  obj.foo()
  ```



- Double Dispatch

  > [참고 영상](https://www.youtube.com/watch?v=s-tXAHub6vg&list=PLv-xDnFD-nnmof-yoZQN8Fs2kVljIuFyC&index=17)

  - Dynamic dispatch를 두 번 한다는 의미이다.
    - 즉, 실행 시점에 호출할 메서드를 결정하는 과정을 2번에 걸쳐서 한다는 의미이다.

  - 예를 들어 아래와 같이 `Post` interface와 `SNS` interface가 있다고 가정해보자.

  ```python
  from __future__ import annotations
  from abc import ABCMeta, abstractmethod
  from typing import List
  
  
  class Post(metaclass=ABCMeta):
  
      @abstractmethod
      def post_on(self, sns:SNS):
          pass
  
  
  class Text(Post):
      def post_on(self, sns:SNS):
          pass
  
  
  class Picture(Post):
      def post_on(self, sns:SNS):
          pass
  
  
  class SNS(metaclass=ABCMeta):
      pass
  
  
  class FaceBook(SNS):
      pass
  
  
  class Instagram(SNS):
      pass
  
  
  posts: List[Post] = [Text(), Picture()]
  snss: List[SNS] = [FaceBook(), Instagram()]
  for post in posts:
      for sns in snss:
          post.post_on(sns)
  ```

  - 이 때 SNS의 종류에 따라 다른 작업을 하기 위해 Post의 concrete class들을 아래와 같이 변경했다.

  ```python
  class Text(Post):
      def post_on(self, sns:SNS):
          if isinstance(sns, FaceBook):
              pass
          elif isinstance(sns, Instagram):
              pass
  
  
  class Picture(Post):
      def post_on(self, sns:SNS):
          if isinstance(sns, FaceBook):
              pass
          elif isinstance(sns, Instagram):
              pass
  ```

  - 위와 같은 방식의 문제는 새로운 SNS가 추가될 때 마다 분기를 추가해줘야 한다는 점이다.
    - 예를 들어 새로운 SNS로 Line이 추가되었을 경우 `post_on()` 메서드는 다음과 같이 변경되어야한다.
    - SNS가 추가될 때 마다 Post도 변경해줘야하므로 이는 OCP 위반이다.

  ```python
  def post_on(self, sns:SNS):
      if isinstance(sns, FaceBook):
          pass
      elif isinstance(sns, Instagram):
          pass
      elif isinstnace(sms, Line):
          pass
  ```

  - Double dispatch를 사용하면 이와 같은 문제를 해결할 수 있다.
    - 아래 코드에서는 dynamic dispatch가 2번 일어난다.
    - `post.post_on(sns)`가 실행될 때 한 번, `post_on()` 메서드 안에서 `sns.post()`가 실행될 때 한 번.
    - `post.post_on(sns)`가 실행될 때는 Post의 concreate class 중 어떤 class의 method가 실행될 지 실행될 때까지 알 수 없으므로 dynamic dispatch이다.
    - `sns.post()`도 마찬자기로 SNS의 concreate class 중 어떤 class의 method가 실행될 지 실행될 때까지 알 수 없으므로 dynamic dispatch이다.

  ```python
  from __future__ import annotations
  from abc import ABCMeta, abstractmethod
  from typing import List
  
  
  class Post(metaclass=ABCMeta):
  
      @abstractmethod
      def post_on(self, sns:SNS):
          pass
  
  
  class Text(Post):
      def post_on(self, sns:SNS):
          sns.post(self)
  
  
  class Picture(Post):
      def post_on(self, sns:SNS):
          sns.post(self)
  
  
  class SNS(metaclass=ABCMeta):
      @abstractmethod
      def post(self, post: Post):
          pass
  
  
  class FaceBook(SNS):
      def post(self, post: Post):
          pass
  
  class Instagram(SNS):
      def post(self, post: Post):
          pass
  
  
  
  posts: List[Post] = [Text(), Picture()]
  snss: List[SNS] = [FaceBook(), Instagram()]
  for post in posts:
      for sns in snss:
          post.post_on(sns)
  ```

  - Visitor Pattern의 보다 일반적인 형태이다.



# DI

- Dependency

  - 의존성의 의미
    - A가 B를 class 변수 혹은 instance 변수로 가지고 있는 경우
    - B가 A의 메서드의 parameter로 전달되는 경우.
    - A가 B의 메서드를 호출하는 경우
    - 이들 모두 A가 B에 의존하고 있다고 표현한다.
  - 예시
    - 아래 예시에서 Qux는 Foo, Bar, Baz 모두에게 의존하고 있다.

  ```python
  class Foo:
      pass
  
  class Bar:
      def do_something(self):
          pass
  
  class Baz:
      @classmethod
      def do_something(self):
          pass
  
  class Qux:
      def __init__(self, foo: Foo):
          self.foo = foo
      
      def do_somthing_with_bar(self, bar: Bar):
          bar.do_something()
      
      def do_somthing(self):
          Baz.do_something()
  
  
  qux = Qux(Foo())
  qux.do_somthing_with_bar(Bar())
  qux.do_somthing()
  ```

  - 의존성의 문제
    - 만약 위 예시에서 Foo, Bar, Baz  중 하나에라도 변경사항이 생긴다면 Qux도 함께 변경해주어야한다.
    - 따라서 코드의 유지보수가 어려워지고, 코드의 재사용성도 떨어지게 된다.
    - 예를 들어 아래 예시에서 Zookeeper는 Lion class에 강하게 의존하고있다.
    - 만약 Tiger class가 추가된다면 Zookeeper class의 feed 메서드도 함께 변경하거나 TigerZookeeper class를 생성해야한다.
    - 즉, Zoopkeeper class는 유지보수도 어려우며 따로 떼서 사용할 수도 없으므로 재사용성도 떨어진다.

  ```python
  class Lion:
      def eat(self):
          pass
  
  
  class Zookeeper:
      def __init__(self, lion: Lion):
          self.lion = lion
      
      def feed(self):
          self.lion.eat()
  ```



- DIP(Dependency Inversion Principle, 의존성 역전 원칙)

  - 정의
    - 고차원 모듈은 저차원 모듈에 의존하면 안 된다.
    - 추상화 된 것은 구체적인 것에 의존하면 안 된다.
    - 구체적인 것이 추상화된 것에 의존해야한다.
  - 위에서 살펴본 Zookeeper 예시에 DIP 원칙을 적용하면 아래와 같다.
    - Zookeeper class는 더 이상 Lion class라는 구상 class에 의존하지 않고, Animal이라는 추상 class에 의존한다.
    - 이제 새로운 동물이 추가되더라도, 그것이 Animal class를 상속 받기만 한다면 Zookeepr class를 변경할 필요가 없어진다.

  ```python
  from abc import ABCmeta, abstractmethod
  
  
  class Animal(metaclass=ABCmeta):
      @abstractmethod
      def eat(self):
          pass
  
  
  class Lion(Animal):
      def eat(self):
          pass
  
  
  class Zookeeper:
      def __init__(self, animal: Animal):
          self.animal = animal
      
      def feed(self):
          self.animal.eat()
  ```

    - 의존성 역전(dependency inversion)
      - 전통적으로 의존 주체 모듈과 의존 대상 모듈 사이에 의존 관계가 생성되어 왔다.
      - 그러나, 더 이상 의존 주체 모듈이 의존 대상 모듈을 직접적으로 의존하게 하지 말고, 의존 대상의 고차원 모듈, 혹은 의존 대상을 추상화한 모듈에 의존하도록 하는 것을 가리키는 용어가 의존성 역전이다.



- 의존성 주입(Dependency Injection, DI)

  - 의존성을 의존 주체가 생성하지 않고, 외부에서 생성하여 의존 주체에게 주입해주는 방식이다.

  - 의존성 주입을 사용하지 않을 경우
    - 아래 코드에서는 Lion을 의존하는 Zookeeper class에서 Lion class의 instance를 직접 생성한다.

  ```python
  class Lion:
      def eat(self):
          pass
      
      
  class Zookeeper:
      def __init__(self):
          self.lion = Lion()
      
      def feed(self):
          self.lion.eat()
  ```

  - 이 때, DIP를 적용하기 위해 Lion의 상위 class인 Animal class를 생성했다고 가정해보자.
    - 구상 클래스가 아닌 추상 클래스에 의존하기 위해 Animal class를 생성했으나, 여전히 Zookeeper class에서 Lion class를 직접 생성하고 있으므로, Animal class에 의존할 수 없는 상황이 된다.
    - 따라서 다형성을 활용할 수 없는 상황이 되는 것이다.

  ```python
  from abc import ABCmeta, abstractmethod
  
  class Animal:
      @abstractmethod
      def eat(self):
          pass
      
  class Lion(Animal):
      def eat(self):
          pass
  
  class Zookeeper:
      def __init__(self):
          self.lion = Lion()
      
      def feed(self):
          self.lion.eat()
  ```

  - DI 적용하기
    - 따라서 아래와 같이 Lion을 외부에서 생성해서 Zookeeper로 **주입**해준다.

  ```python
  from abc import ABCmeta, abstractmethod
  
  class Animal(metaclass=ABCmeta):
      @abstractmethod
      def eat(self):
          pass
  
  class Lion(Animal):
      def eat(self):
          pass
  
  class Zookeeper:
      def __init__(self, animal: Animal):
          self.animal = animal
      
      def feed(self):
          self.animal.eat()
  ```

  - DIP와 자주 엮이는 개념이라 DIP와 DI를 혼동하기도 하지만 명백히 별개의 개념이다.
    - 위에서 확인했듯이 DI를 사용하여 DIP를 구현할 수 있다.



- 제어의 역전(Inversion of Control, IoC)

  > https://martinfowler.com/bliki/InversionOfControl.html
  >
  > https://martinfowler.com/articles/injection.html

  - 정의
    - 프로그램의 제어 흐름을 한 곳에서 다른 곳으로 전환시키는 원칙이다.
    - 주로 객체들 사이의 의존성을 낮추기 위해 사용한다.
    - DIP와 마찬가지로 하나의 원칙이다.
    - 디자인 패턴이 아닌 하나의 원칙이기에 구체적인 구현 방식을 정의하지는 않는다.

  - IoC는 UI 프레임워크의 등장과 함께 등장한 개념이다.
    - GUI 등장 이전의 UI는 프로그램이 사용자에게 언제 입력을 받을지, 언제 입력 받은 내용을 처리할지를 정했다.
    - 그러나 UI 프레임워크가 나오면서 이러한 제어권이 프로그램이 아닌 UI 프레임워크로 이동했다.
    - 즉 이전에는 아래 코드와 같이 프로그램이 제어권을 가지고 있었으나, UI 프레임워크의 등장과 함께 UI 프레임워크가 프로그램의 동작에 대한 제어권을 가져가게 된다.
    - 예를 들어 사용자가 UI 상에 입력값을 넣으면 UI 프레임워크가 프로그램을 실행시킨다.

  ```python
  # 기존에는 아래와 같이 프로그램이 제어권을 가지고 있었다.
  print("이름을 입력하세요")
  name = input()
  process_name(name)
  print("나이를 입력하세요")
  age = input()
  process_age(age)
  ```

  - IoC는 framework과 library를 가르는 중요한 기준 중 하나이다.
    - Framework는 code에 대한 주도권을 가져가는 반면, library는 code에 대한 주도권은 여전히 프로그래머에게 있다.
    - 즉, framework에서는 IoC가 존재하는 반면, library에서는 IoC가 발생하지 않는다.
  - DI와의 관계
    - DI는 IoC를 구현하는 하나의 방식일 뿐이다.
    - 이전에는 DI라는 용어가 존재하지 않았지만, IoC에서 현재의 DI의 개념을 분리하기 위해 DI라는 용어를 만들어 낸 것이다.
  - 예시
    - 위의 의존성 주입에서도 IoC를 찾아낼 수 있다.
    - DI를 적용하기 이전의 Zookeeper class는 Lion class를 강하게 의존하고 있었으며, Lion instance를 언제 생성할지에 대한 통제권을 Zookeeper class가 가지고 있었다.
    - 그러나 DI를 적용함으로써 Zookeeper class가 사용할 Animal instance의 생성에 관한 통제권이 Zookeeper class가 아닌 client code로 옮겨가게 되었다.
    - 즉 위 예시는 DI를 사용하여 IoC를 구현한 것이기도 하다.

  - IoC Container
    - DI가 자동적으로 이루어지도록 하기 위한 framework를 의미한다.
    - 객체의 생성과 생명주기를 관리하며, 다른 class들에 의존성을 주입하는 역할을 한다.







# CI/CD

> https://www.redhat.com/en/topics/devops/what-is-ci-cd

- CI(Continuous Integration)

  > https://martinfowler.com/articles/continuousIntegration.html

  - 정의
    - 같은 프로젝트를 진행중인 팀원들이 각자의 작업물을 빈번하게 통합하는 소프트웨어 개발 방식이다.
    - 일반적으로 각 팀원은 최소한 하루에 한 번은 작업물을 통합한다.
    - 각각의 통합은 (테스트를 포함하여) 통합과정의 에러를 최대한 빨리 탐지할 수 있는 자동화된 빌드로 정의된다.
  - 등장 배경
    - CI가 등장하기 이전의 전통적인 소프트웨어 개발에서는 팀원들이 각자의 작업물을 합치는 데 많은 자원이 들어갔다.
    - 여러 명의 작업물을 합쳐야 하다 보니 팀원들 간의 코드가 충돌하는 경우도 있었고, 기존 코드와 충돌하는 경우도 있었으며, 기존 코드나 다른 팀원이 작성한 코드와의 의존성도 고려해야해서, 작업물을 통합하는 일은 매우 길고 복잡하며, 언제 끝날지도 예측할 수 없는 작업으로, integration hell이라는 용어도 생길 정도였다.
    - 소프트웨어 개발을 위해서 반드시 거쳐야 하는 통합 작업이 이토록 고되다 보니 이를 해결하고자 하는 방법론들이 등장하게 되었는데, CI가 바로 이러한 방법론들의 종합이라 할 수 있다.
  - CI의 일반적인 흐름
    - main code로부터 code를 가져온다.
    - 위에서 받아온 코드를 수정, 추가해서 작업을 완료한다.
    - 작업이 완료된 코드를 컴파일하고, 기능이 정상적으로 작동하는지 테스트하는 빌드를 수행하는데, 빌드는 자동화되어야한다.
    - 만약 테스트가 성공적으로 실행되었다면, 변경사항을 중앙 repoistory에 commit한다.
    - 일반적으로, 중앙 repository에서 code를 가져온 시점부터, 해당 code를 기반으로 작업을 완료하고 commit 하는 사이에, 다른 개발자가 commit을 했을 것이다.
    - 따라서 해당 변경 사항을 다시 가져와서 현재 code를 update하고 다시 빌드한다.
    - 만약 이 때 다른 개발자가 작업한 부분과 내가 작업한 부분 사이에 충돌이 있을 경우, 컴파일이나 테스트가 실패하게 될 것이다.
    - 따라서 충돌이 발생한 부분을 수정하고 다시 빌드한 후 main code에 commit 한다.
    - 이제 main code의 code를 기반으로 다시 빌드를 수행한다.
    - main code에서의 빌드도 무사히 완료되면 한 번의 통합이 완료된 것이다.
  - CI의 이점
    - 짧은 단위로 주기적 통합이 이루어지기 때문에 이전처럼 통합이 언제 끝날지 모른다는 위험성을 줄여준다.
    - CI가 버그를 제거해주지는 않지만, 매 빌드시에 자동으로 테스트를 실행하므로 버그를 훨씬 쉽게 찾을 수 있게 해준다.
  - CI의 핵심 요소들
    - 소스 코드, 라이브러리, 구성 파일 등의 전체 코드 베이스를 관리할 수 있는 버전 관리 시스템
    - 자동화된 빌드 스크립트
    - 자동화된 테스트



- CD(Continuous Delivery, Continuous Deployment)
  - 정의
    - CD라는 용어는 Continuous Delivery, Continuous Deployment의 두문자어로, 두 용어는 서로 대체하여 사용할 수 있지만, 맥락에 따라 의미가 약간씩 달리지기도 한다.
    - Continuous Delivery(지속적 제공)는 일반적으로 개발자들이 애플리케이션에 적용한 변경 사항이 테스트를 거쳐 github 등의 repository에 자동으로 업로드되는 것을 뜻한다.
    - Continusous Deployment(지속적 배포)는 일반적으로 애플리케이션의 변경사항이 고객이 사용할 수 있도록 프로덕션 환경으로 자동으로 릴리즈 되는 것을 의미한다.
  - 지속적 제공
    - CI가 빌드 자동화에 관한 개념이라면, continuous delivery는 빌드 후 유효한 코드를 repository에 자동으로 release하는 것과 관련된 개념이다.
    - 따라서 지속적 제공을 실현하기 위해서는 개발 파이프라인에 CI가 먼저 구축되어 있어야한다.
    - 지속적 제공의 목표는 프로덕션 환경으로 배포할 수 있는 코드베이스를 확보하는 것이다.
  - 지속적 배포
    - 프로덕션 환경에 배포할 준비가 완료된 코드를 프로덕션 환경으로 배포한다.



- CI/CD

  - 지속적 통합과 지속적 제공만을 지칭할 때도 있고, 지속적 통합, 지속적 제공, 지속적 배포를 모두 지칭할 때도 있다.
  - 목적
    - 애플리케이션 개발 단계를 자동화하여 애플리케이션을 더욱 짧은 주기로 고객에게 제공한다.
    - 모든 과정을 자동화 함으로써 사람이 수동으로 했을 때 발생할 수 있는 실수를 줄인다.
    - 개발부터 운영 환경에 배포하기까지의 과정을 세분화함으로써 error 발생시 빠른 대응을 가능하게 한다.
  - CI/CD가 적용된 개발 파이프라인은 아래의 순서를 거친다.
    - 개발자가 완료된 작업을 기존 code, 혹은 다른 개발자의 code화 통합한다(CI).
    - 성공적으로 통합된 코드를 운영 환경에 배포하기 위해 repository에 릴리즈하고, 배포할 준비를 마친다(Continuous Delivery).
    - 운영 환경에 배포할 준비가 완료된 코드를 운영 환경에 배포한다(Continuous Deployment).

  - 대표적인 CI/CD 도구에는 아래와 같은 것들이 있다.
    - Jenkins
    - TeamCity
    - CircleCI
    - Github actions
    - Gitlab







# Shorts

- Type system

  - 모든 프로그래밍 언어는 어떤 category에 속한 object가 어떤 작업을 할 수 있고, 어떤 category가 어떻게 처리될지를 형식화하는 type system을 가지고 있다.
  - Dynamic Typing
    - Type checking을 run time에 수행하고, 변수의 type이 변경되는 것을 허용하는 방식을 말한다.
    - 대표적으로 Python이 있는데, 아래 코드는 절대 error가 발생하지 않는다.

  ```python
  # 1과 "foo"를 더하는 것은 불가능하지만, 해당 코드는 실행되지 않으므로 에러가 발생하지 않는다.
  if False:
      1 + "foo"
  ```

  - Static Typing
    - Type checking을 compile time에 수행하고, 일반적으로 변수의 type 변경이 불가능하다.
    - 대표적으로는 Java가 있는데, 아래 코드는 compile time에 error가 발생한다.

  ```java
  String foo;
  foo = 1;
  ```



- duck typing

  > if it walks like a duck and it quacks like a duck, then it must be a duck
  >
  > 만일 어떤 것이 오리 처럼 걷고 오리처럼 꽥꽥거린다면, 그것은 오리일 것이다.

  - duck test에서 개념을 따 왔다.
  - 동적 타이핑 언어 및 다형성과 관련된 개념이다.
  - 객체의 type보다 해당 객체에 정의되어 있는 method 혹은 attribute가 더 중요하다는 개념이다.
    - 객체에 이미 존재하는 메서드를 호출하기 위해, 객체가 해당 메서드를 갖는 타입인지 확인하지 말고, 해당 메서드를 가지고 있다면 해당 타입으로 간주하라는 것이다.

  - 예시

  ```python
  class Duck:
      def fly(self):
          print("fly with wings")
  
          
  class Plane:
      def fly(self):
          print("fly with fuel")
          
          
  class Ostrich:
      def walk(self):
          print("walking")
  
          
  def fly_duck(duck):
      duck.fly()
  
  # Ostrich는 fly라는 메서드를 가지고 있지 않기에 error가 발생한다.
  for obj in [Duck(), Plane(), Ostrich()]:
      obj.fly()
  ```

  - 코드가 특정 type에 강하게 결합되지 않게 해준다는 장점이 있지만, 문제가 생길 경우 디버깅이 어려워진다는 단점이 있다.
  - Duck typing 덕분에 Python에서는 interface를 구현해야 하는 번거로움이 많이 줄어들었다.
    - Interface가 하는 역할을 duck typing이 해주고 있는 것이다.
    - 물론 그렇다고 Python에서 interface 자체가 쓸모 없다는 것은 아니다.

  



- Call by value, Call by reference, Call by sharing

  > https://en.wikipedia.org/wiki/Evaluation_strategy

  - 평가 전략(Evaluation Strategy)

    - 프로그래밍 언어에서 평가 전략이란 표현식을 평가하는 규칙들의 집합이다.
    - 그러나 주로 parameter 전달 전략(Parameter-passing strategy)의 개념을 가리킨다.
    - Parameter-passing strategy란 function에 전달되는 각 parameter의 값의 종류를 정의하고, 함수 호출시의 parameter를 평가할지 여부를 결정하고, 만약 평가한다면, 평가 순서를 결정하는 전략을 의미한다.

  - Parameter와 argument

    - Parameter(매개변수, 형식 매개변수(formal parameter))란 함수에 정의된 매개변수를 의미한다.
    - Argument(인자, 실인자(actual parameter))란 함수에 전달하는 값을 의미한다.
    - Parameter는 함수 선언부에 정의되고, argument는 함수 호출부에서 사용된다.

  ```python
  def f(a):	# 함수에 정의된 매개변수 a는 parameter
      return a
  
  f(1)		# 함수에 실제로 넘어가는 값인 1은 argument
  ```

  - Call by value
    - Argument 표현식의 평가된 값이 함수 내에서 일치하는 변수에 binding된다.
    - 주로 새로운 메모리에 값을 복사하는 방식으로 이루어진다.
    - 즉, 먼저 argument 표현식을 평가한다.
    - `f(1)`에서 argument 표현식에 해당하는 `1`이라는 표현식을 평가하면 `1`이라는 값을 얻게 된다.
    - 이 평가된 값을 함수 내에서 일치하는 변수인 `a`에 binding한다.
    - 이 때, 주로 1이라는 값을 복사하여 새로운 메모리 영역에 생성하는 방식을 사용한다.
    - 따라서 함수 내에서 값이 변경되어도 원본 값은 변경되지 않는다.
  - Call by reference
    - Parameter가 argument의 reference에 bound된다.
    - 이는 function이 argument로 사용된 변수를 변경할 수 있다는 것을 의미한다.
    - 이 방식은 프로그래머가 함수 호출의 영향을 추적하기 힘들게 만들고, 사소한 버그를 유발할 수도 있다.
  - Call by sharing(call by object, call by object-sharing)
    - Caller와 callee가 object를 공유하는 것이다.
    - 값이 원시 타입이 아니라 객체에 기반하고 있음을 표현하기 위해 주로 사용한다.
    - Callee에게 전달 된 값이 변경된다는 점에서 call by value와 다르고, 주소가 아닌 object를 공유한다는 점에서 call by reference와는 다르다.
    - Immutable object의 경우 call by value와 실질적인 차이가 존재하지 않는다.

  - Python과 Java, Javascript등의 언어는 Call by sharing 방식을 사용한다.

    - 그러나 일반적으로 call by sharing이라는 용어를 사용하지는 않는다.
    - Python community에서는 이를 call by assignment라 부른다.



- 도메인 로직(domain logic, 비즈니스 로직(Business logic))

  > https://velog.io/@eddy_song/domain-logic
  >
  > https://enterprisecraftsmanship.com/posts/what-is-domain-logic/

  - Problem space와 solution space
    - 하나의 프로젝트는 크게 problem space와 solution space라는 두 개의 영역으로 나눠진다.
    - Problem space는 일반적으로 domain 혹은 problem domain, core domain이라 부르며, software를 통해 해결하고자 하는 현실의 문제들을 의미한다.
    - Solution space는 business logic, business rules, domain logic, domain knowledge라 부르며, problem domain을 해결하기 위한 방안들을 의미한다.

  - 비즈니스 혹은 도메인
    - 소프트웨어 공학에서 비즈니스 혹은 도메인이라는 말은 소프트웨어가 해결하고자 하는 현실의 문제를 가리킨다.
    - 즉 소프트웨어의 존재 이유이다.
  - 도메인 로직
    - 소프트웨어가 해결하고자 하는 현실 문제를 해결하는 데 직접적으로 관련된 로직을 의미한다.
    - Software는 도메인 로직으로만 구성되지 않는다.
    - 개발을 하다 보면 다양한 코드를 작성하게 되며, 이들이 모두 domain model을 작성하는 것과 관련되지는 않는다.
    - 대부분의 경우 domain model을 DB 등의 data store, 외부 서비스, 사용자와 연결하기위해 많은 코드를 작성하게 된다.
    - 따라서 domain model과 직접적으로 관련된 코드와 그렇지 않은 코드를 구분하는 것은 쉽지 않다.
  - 애플리케이션 서비스 로직
    - 비즈니스 로직과 구분되는 현실 문제 해결에 직접적으로 관여하지 않는 로직을 의미한다.
    - 애플리케이션 서비스 로직은 애플리케이션 서비스 계층에서 결정들을 조율하고 의사결정 결과를 반영하는 등의 역할을 한다.
  - 도메인 로직과 애플리케이션 서비스 로직의 구분
    - 어떤 코드가 비즈니스에 대한 의사결정을 하고 있는가로 구분한다.

  - 왜 구분해야 하는가
    - 관심사의 분리를 가능하게 해준다.
    - 이를 통해 도메인과 관련된 로직에 보다 집중할 수 있게 된다.

  - 예시
    - 아래 코드는 application service layer를 보여준다.
    - 실제 비즈니스 로직은 atm 객체에서 처리하고 application service는 비즈니스에 관한 의사 결정 결과를 조율하고 반영하는 역할을 한다.
    - 비즈니스와 직접적으로 관련된 코드만 보고 싶다면 atm만 확인하면 된다.
    - 즉 아래와 같이 계층을 구분함으로써 코드를 보다 쉽게 읽을 수 있게 되고, 도메인 로직에 집중할 수 있게 된다.

  ```python
  class Bank:
      def __init__(self):
          self.atm = ATM()
          self.payment_gateway = None
          self.repository = None
  	
      # take_money 메서드 자체는 아무런 의사 결정을 하지 않는다.
      def take_money(amount):
          # 돈을 출금할 수 있는지에 대한 의사 결정은 atm 객체의 can_take_money 메서드를 통해 이루어진다.
          if self.atm.can_take_money(amount):
              # 수수료를 포함한 금액이 얼마인지에 대한 의사 결정 역시 atm 객체에서 이루어진다.
              amount_with_commision = self.amount.calculate_amount_with_commision(amount)
              
              self.payment_gateway.charge_payment(amount_with_commision)
              self.repository.save(self.atm)
          else:
              return "Not enough meney to withdraw"
  ```




- TTY
  - TTY의 기원
    - 1830년대에 와이어를 통해 message를 주고 받을 수 있는 teleprinter(전신인자기)가 개발되었다.
    - 기존에는 전송자가 모스 부호 입력하고, 수신자가 모스 부호를 받는 형식이었지만, teleprinter는 전송자가 문자를 입력하면 이를 모스 부호로 변환하여 전달하고, 수신자 측에 모스 부호로 도착하면 이를 다시 문자로 변환하여 수신자에게 출력해주었다.
    - 이후 개량을 거쳐 1908년 Teletypewriter가 발명되었다.
    - 컴퓨터가 개량되면서, 컴퓨터에도 입출력 장치가 필요하게 되었고, 컴퓨터에도 teletypewriter가 입출력장치로 사용되기 시작했다.
    - Teletypewriter은 시간이 흐르면서 teletype으로 줄여서 불리기 시작했고, 결국 현재는 TTY로 줄여서 부른다.
  - PTY(Pseudo-TeletYpes)
    - TTY는 Unix 계열 운영체제에서 software화 되었는데, 이를 물리적인 TTY와 구분하기 위해서 PTY라고 부른다.
    - Software로서의 TTY 역시 그냥 TTY라고 부르기도 한다.
    - Terminal과 동의어로 쓰인다.
  - PTS(Pseudo Terminal Slave)
    - `ssh` 등으로 서버에서 원격으로 접속했을 때 열리는 TTY이다.

