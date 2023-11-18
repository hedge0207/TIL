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





# API Gateway

> https://bcho.tistory.com/1006

- API Gateway
  - API server 앞단에 위치하여 모든 API server들의 endpoint들을 묶고, API server들의 공통 로직을 처리하는 기능을 담당하는 middleware이다.
    - 일반적으로 로깅, 인증/인가, 라우팅, 프로토콜 변환 등의 기능을 수행한다.
    - 공통된 기능을 처리함으로써 중복 개발을 방지하고, 표준을 설정하고 이를 준수하기가 보다 수월해진다.
  - 여러 API server로 구성되는 MSA(Micro Service Architecture)에서 주로 사용한다.
    - Client아 독립적으로 service들을 확장할 수 있다.
    - 제어 지점이 단일화되어 관리가 편리해진다.



- 인증/인가와 관련된 Gateway의 기능
  - Gateway의 가장 기본적인 기능이다.
    - 인증은 client의 신분을 확인하는 것이다.
    - 인가는 client가 API를 호출할 권한이 있는지를 확인하는 것이다.
  - API token 발급
    - 인증이 완료된 client를 대상으로 API token을 발급하는 역할을 한다.
    - 일반적인 흐름은 아래와 같다.
    - Client는 gateway에 인증을 위한 정보(ID/PW, 인증서, OTP 등)를 전송한다.
    - Gateway는 인증 정보를 인증 server로 전송한다.
    - 인증 server에서는 gateway가 보낸 인증 정보를 가지고 인증을 수행하고 그 결고를 gateway에 반환한다.
    - 인증 server에서 인증이 정상적으로 완료됐다는 응답을 받은 gateway는 API token을 생성하고 이를 client에 반환한다.
  - API token 검증
    - API token을 발급 받은 client는 발급 받은 token을 사용하여 API를 호출한다.
    - Gateway는 API token이 유효한지 검증 후, 유효한 경우에만 API를 호출한다.
  - Endpoint별 API 요청 인가
    - 사용자의 권한을 확인하고, 사용자가 요청을 보낸 API가 사용자의 권한으로 호출할 수 있는지를 확인한다.
    - 사용자가 해당 API를 호출할 권한이 있는 경우에먼 API server에 요청을 전달한다.



- API routing
  - Load balancing.
    - 여러 개의 API 서버로 부하를 분산하는 역할을 수행한다.
    - 부하 분산 방식, server 중 일부에 장애 발생시 요청을 어떻게 routing할지, 장애가 발생한 server가 다시 복구 됐을 때 어떻게 routing할지 등을 고려해야한다.
  - Client별 endpoint 제공.
    - 같은 API를 여러 개의 endpoint로 제공할 수 있다.
    - Gateway에서 같은 API로 요청을 보내더라도 endpoint이름을 다르게 하여 routing하는 것이 가능하다.
  - Message 혹은 header 기반 routing.
    - HTTP request의 message 혹은 header에 따라 각기 다른 API로 routing되도록 할 수 있다.



- 공통 로직 처리
  - Gateway는 모든 API server의 앞쪽에 위치하기 때문에 모든 API 호출이 gateway를 거쳐간다.
    - 따라서 모든 API가 공통으로 처리해야하는 공통 기능을 gateway에서 처리하면 API server에서는 이러한 기능을 개발할 필요가 없어진다.
  - Gateway에서 공통 로직을 처리함으로써 API server에서는 비즈니스 로직 구현에만 집중할 수 있게 된다.



- Mediation
  - Client가 원하는 API spec과 API server가 제공하는 API spec이 다를 때, gateway에서 이를 중재할 수 있다.
  - Message format 변환
    - Client의 요청을 다른 format으로 변환하여 API server로 전송한다. 
    - API server의 응답을 다른 format으로 변환하여 client로 반환한다.
  - Protocol 변환
    - API gateway에서 client로 들어온 요청의 protocol을 변환하여 API server로 전송한다.



- Aggregation
  - 여러 개의 API를 묶어서 하나의 API로 만드는 작업이다.
    - 여러 개의 API를 순차적으로 호출해야 할 경우 유용하게 사용할 수 있다.
    - 예를 들어 은행 서비스에서 현금을 송금하는 기능은 잔액 확인, 출금, 입금으로 나눌 수 있다.
    - 만일 aggregation을 하지 않을 경우 client는 잔액을 확인하는 API, 출금하는 API, 입급하는 API를 모두 호출해야 할 것이다.
    - 반면에 aggregation 할 경우 이들 세 API를 하나의 API로 묶어 client가 세 API를 별도로 호출하는 것이 아니라, gateway를 통해 하나의 API만 호출하면 gateway 내에서 위 3가지 API를 호출하여 처리하도록 할 수 있다.
  - 단점
    - Gateway에서 여러 API를 호출하게 될 경우 gateway에 가해지는 부하가 커질 수 있다.
    - 따라서 aggregation 로직은 Mediator API server라는 별도의 계층을 만들어 gateway 밖에서 따로 처리하는 것이 권장된다.



- Logging, metering
  - API 호출 logging
    - 모든 API 호출은 gateway를 거쳐 가기에 gateway에 API호출에 대한 log를 수집하는 기능을 넣는 것이 좋다.
  - API metering & charging
    - Metering은 유료 API를 제공할 경우 과금을 위한 API 호출 횟수, client IP 등을 기록하는 기능이다.
    - Charging은 metering된 자료를 기반으로 요금을 계산하는 기능이다.



- Rate limiting and throttling
  - API gateway를 통해 모든 request가 이루이지므로 throttling을 하기 매우 적합하다.
  - Client의 요청을 제한하여 application에 과한 부하가 가해지는 것을 방지하고 악의적으로 과한 요청을 보내는 것을 막을 수 있다.



- Caching
  - Microservice들에서 받아온 요청을 cache하여 다음 번에 동일한 request가 들어왔을 때 server를 거치지 않고 응답을 반환할 수 있다.
  - 이를 통해 응답 속도를 향상시킬 수 있다.



- Circuit breaker
  - Circuit breaker pattern을 구현하기 위해 사용할 수 있다.
  - 단일 지점 장애가 system의 전체 장애로 이어지지 않도록 할 수 있다.



# Load balancing

- Load balancing
  - Traffic을 여러 server로 고르게 분산하는 역할을 한다.
    - 이를 통해 고가용성을 보장하고 신뢰도를 높이며, 한 server에 과도하게 부하가 가해지는 것을 방지해 성능을 높일 수 있다.
  - 일반적으로 load balancer는 client와 server 사이에 위치한다.
    - 그러나 부하를 분산시켜야 하는 곳이라면 어디에든 위치시킬 수 있다.
    - client와 web server 사이, web server와 application server 사이, application server와 DB server 사이 등 부하를 분산시킬 필요가 있는 곳에 배치할 수 있다.
  - 동작 방식
    - Client로 부터 요청을 받는다.
    - Request를 평가하고 어느 server에서 request를 처리해야하는지를 결정한다.
    - Server로 request를 전달한다.
    - Server는 request를 처리하고 response를 다시 load balancer로 전달한다.
    - Load balancer는 응답을 받아 client에게 전달한다.



- Load balancing을 하는 이유
  - 성능 향상
    - Traffic을 여러 server로 분산시켜 각 server에 가해지는 부하를 감소시킨다.
    - 이를 통해 보다 빠른 속도로 response를 전달할 수 있게 된다.
  - 고가용성(high availability)과 신뢰성(reliability)을 보장한다.
    - 여러 server에 부하를 분산시켜 단일 지점에서 failure가 발생하는 것을 방지한다.
    - 한 server가 실패하거나 장애가 발생하도, traffic을 다른 서버로 redirect하여 요청을 처리하게 할 수 있다.
  - 확장성
    - Traffic이 증가할 때 보다 쉽게 확장이 가능하다.
    - 추가된 server를 load balancing pool에 추가하기만 하면 된다.
  - 지리적 분산이 가능해진다.
    - 국제적인 service의 경우 여러 위치에 server를 두는 경우가 많은데, load balancer는 가장 적절한 위치에 있는 server로 요청을 분산할 수 있다.
    - 이를 통해 가장 가깝거나 최고의 성능을 낼 수 있는 server로 요청을 전송하여 응답 속도를 증가시킬 수 있다.
  - 보안
    - DDoS(Distributed Denial-of-Service) 공격을 막는데 도움을 준다.
    - Traffic을 분산하여 공격자가 단일 target에 과한 요청을 보내는 것을 막을 수 있다.
  - 비용 절감
    - 보다 효율적으로 traffic을 분산하여 비용 절감이 가능하다.
    - Hardware와 infrastructure에 드는 비용과 에너지 소비도 줄일 수 있다.
  - Caching
    - Image나 video 같은 정적 content를 caching 할 수도 있다.
    - 이렇게 cache된 content들은 server를 거치지 않고 load balancer가 바로 응답을 반환함으로써 응답 속도를 줄일 수 있다.



- Stateless load balancing & stateful load balancing
  - Stateless load balancer는 client의 session이나 client와의 연결 상태에 대한 어떠한 정보도 유지하지 않는다.
    - 오직 client의 IP나 request URL, headers 등의 request에 포함된 정보만을 가지고 request를 sever로 전달한다.
    - Session 정보를 저장하지 않기에 빠르고 효율적인 traffic 분산이 가능하다.
  - Stateful load balancer는 client의 session 정보를 보존한다.
    - 특정 server에 cleint를 할당하고 같은 client에서 오는 모든 순차적인 request가 같은 server로 전달되도록 보장한다.
  - Stateful load balancing은 크게 두 개의 type으로 나뉜다.
    - Source IP Affinity: client IP에 기반하여 client를 특정 sever에 할당하는 방식이다.
    - Session Affinity: cookie나 URL 등의 session identifier에 기반하여 client를 특정 server에 할당하는 방식이다.



- 고가용성과 장애허용성

  - 고가용성을 보장하기 위해서 load balancer는 복제본이 함께 배포되어야 한다.

    - 즉 복수의 load balancer instance들이 실행되어야 한다는 것이다.
    - 크게 아래와 같은 전략이 있다.
    - Active-passive configuration:하나의 load balancer가 정상 동작하는 동안 다른 load balancer는 대기하고 있다가, 요청을 처리하던 load balancer에 문제가 생기면 대기하던 load balancer가 활성화되어 요청을 처리하는 방식이다.
    - Active-active configuration: 복수의 load balancer가 모두 활성화 상태로 traffic을 동시에 처리하는 방식이다.

  - Health check와 monitoring

    - Health check는 일정 주기 마다 load balancer가 server들의 가용성과 성능을 확인하는 작업이다.
    - Server들의 상태를 monitoring함으로써 load balancer는 응답을 줄 수 없는 server들을 server pool에서 제거하여 해당 server로 요청이 가지 않도록 한다.

    - Monitoring은 load balancer 자체를 확인하는 작업으로, load balancer를 monitoring하여 잠재적인 실패를 방지할 수 있다.



- Load balancer 도입시 고려할 사항.

  - Single point of failure

    - 만약 load balancer를 단일 instance만 사용하거나 장애허용성을 염두에 두지 않으면, load balacer는 단일 장애점이 될 수도 있다.
    - 만약 load balancer에 문제가 생길 경우 전체 application에 영향을 주게 될 수 있다.
    - 따라서 이러한 위험을 완화시키기 위해 고가용성이나 장애허용성을 염두에 두고 load balancer를 운용해야한다.

  - 설정의 복잡함

    - Load balancer는 떄로 algorithm, timeout, health check 정책 등 광범위한 설정 값들을 필요로한다.

    - 또한 잘 못 설정할 경우 load balancer의 성능이 떨어지거나 traffic을 고르게 분산하지 못 하게 되거나, 최악의 경우 service가 중단될 수도 있다.
    - Load balancer를 운용하기 위해서는 적절한 설정값들로 설정하고 꾸준한 유지보수가 필요하며, 전문적인 지식을 갖춰야한다.

  - 확장성의 한계

    - Traffic이 증가함에 따라 load balancer는 bottleneck이 될 수 있다.
    - 특히 수직 혹은 수평 확장에 적합하게 설정되어 있지 않을 경우 더욱 그렇다.
    - 따라서 traffic 증가에 따라 load balander의 수용량을 잘 monitoring하고 조정해야한다.

  - Latency

    - Request-response 사이에 load balancer가 추가되면 추가적인 network hop이 생기는 것이므로 latency를 증가시킬 수 있다.
    - 일반적으로 이는 매우 미미한 수치이긴 하지만, load balancer가 latency를 증가시킬 수도 있다는 점은 항상 생각해야한다.

  - Sticky sessions

    - 어떤 application은 session이 유지되거나, 요청들 사이의 user context가 유지되어야한다.
    - 그러한 경우에 load balancer는 session persistence 혹은 sticky session을 고려하여 운용해야한다.
    - 그러나 이는 request가 고르게 분산되지 못하게 만들수도 있다.

  - 비용

    - Load balancer를 구축하고 관리하는데는 비용이 든다.
    - Hardware나 software license 비용등과 더불어, 이를 관리하는 데도 비용이 든다.





## Load Balancing algorithm

> https://www.designgurus.io/course-play/grokking-system-design-fundamentals/doc/641db0dec48b4f7de900fd04

- Round Robin
  - 가용한 server에 request를 순차적으로 분산하는 방식이다.
    - 가장 단순한 load balancing algorithm 중 하나이다.
  - 장점
    - 구현이 쉽다.
    - Server들의 처리 능력이 비슷할 경우 잘 동작한다.
  - 단점
    - Server들의 처리 능력이 각기 다를 경우 잘 동작하지 않을 수 있다.
    - Server health나 response time에 대해서는 고려하지 않는다.



- Least Connections
  - Request가 들어왔을 때 활성화된 connection이 가장 적은 server로 요청을 보내는 방식이다.
    - 예를 들어 A, B 두 개의 server가 있다고 가정하자.
    - 새로운 request가 들어왔을 때, A에는 2개의 connection이, B에는 1개의 connection이 연결되어 있다.
    - 이 경우 connection이 가장 적은 B에 새로운 request를 전달한다.
  - 장점
    - Server마다 처리 능력이 다를 때 사용하기 좋다.
    - Request를 처리하는 데 걸리는 시간이 다양할 때 보다 효과적으로 부하를 분산할 수 있다.
  - 단점
    - 각 server마다 활성화된 connection의 수를 추적해야한다.
    - Server health나 상태를 고려하지 않는다.



- Weighted Round Robin
  - Round Robin algorithm을 확장한 것으로 각 서버의 처리 능력에 따라 server마다 다른 가중치를 부여하고, 이 가중치에 비례하여 request를 분산한다.
  - 장점
    - 구현이 쉽다.
    - 각 server의 각기 다른 처리량을 고려한다.
  - 단점
    - 가중치를 수동으로 할당하고 관리해야한다.
    - Server health나 response time을 고려하지 않는다.



- Weighted Least Connection
  - 할당된 가중치에 따라 활성 연결 비율이 가장 낮은 server로 request를 전달한다.
    - Least Connection과 Weighted Round Robin을 결합한 방식이다.
  - 장점
    - Server의 처리량과 활성 연결의 수를 모두 고려하므로, 부하 분산이 효율적으로 이루어진다.
    - 할당된 가중치에 따라 활성 연결 비율이 가장 낮은 server로 request를 전달한다.
  - 단점
    - 활성화된 connection 수와 가중치를 모두 추적해야한다.
    - Server health나 response time을 고려하지 않는다.



- IP Hash
  - Source IP 주소 혹은 destination IP 주소를 기반으로 어떤 server로 보낼지 결정한다.
    - 이 방식은 session 지속성(persistence)를 유지한다.
    - 즉 특정 IP에서 온 request는 같은 server로 전송된다.
  - 장점
    - Session 지속성을 유지할 수 있으므로, 특정 client와 특정 server가 반복적으로 연결되어야 하는 경우 유용하다.
    - Hash 함수만 잘 구현한다면 부하를 고르게 분산할 수 있다.
  - 단점
    - 적은 수의 client가 많은 수의 요청을 보내는 상황에서는 부하가 잘 분산되지 않을 수 있다.
    - Server health나 response time, 그리고 server마다 각기 다른 처리 능력을 고려하지 않는다.



- Least Response Time

  - 응답 시간이 가장 짧고, 활성화된 connection의 개수가 가장 적은 server로 request를 전달한다.
    - 가장 빨리 응답을 줄 수 있는 server에 우선 순위를 주기에 사용자 경험을 최적화하는데 도움을 준다.
  - 장점
    - Server의 response time을 고려하여 사용자 경험을 향상시킬 수 있다.
    - 활성 connection과 response time을 모두 고려하므로 효율적인 부하 분산이 가능하다.

  - 단점
    - Server의 response time을 추적하고 monitoring해야한다.
    - Server health나 server 마다 각기 다른 처리 능력을 고려하지 않는다.



- Random
  - 무선적으로 아무 server에나 request를 전송한다.
    - 모든 server가 비슷한 처리 능력을 가지고 있고 session persistence가 필요하지 않을 때 유용하다.
  - 장점
    - 구현이 쉽다.
    - Server들의 처리 능력이 비슷할 경우 잘 동작한다.
  - 단점
    - Server health나 response time, 그리고 server마다 각기 다른 처리 능력을 고려하지 않는다.
    - Session persistence가 요구되는 경우 사용할 수 없다.



- Least Bandwidth

  - Request가 들어왔을 때, 가장 가장 적은 대역폭을 사용하는 server로 request를 전달한다.

  - 장점
    - Network 대역폭을 고려하므로, network 자원을 관리하는 데 도움을 준다.
    - Server들이 각기 다른 대역폭을 가지고 있을 때 유용하다.
  - 단점
    - Server의 대역폭을 추적하고 monitoring해야한다.
    - Server health나 response time, 그리고 server마다 각기 다른 처리 능력을 고려하지 않는다.



- Custom Load
  - 특정 요구사항이나 조건에 따라 직접 구현한 load balancing algorithm을 사용하는 방식이다.
    - Server health, 위치, 처리 능력 등을 고려할 수 있다.
  - 장점
    - 커스터마이징이 가능하므로 특정 use case에 맞는 부하 분산이 가능하다.
    - 여러 요소를 고려하여 구현할 수 있다.
  - 단점
    - 직접 개발하고 유지보수 해야 하므로 시간이 많이 든다.
    - 성능 최적화를 위해 많은 광범위한 test가 필요하다.



## Load balncing의 유형

- Hardware Load Balancing
  - 물리적 장치를 통해 load balancing을 수행하는 것이다.
    - Application-Specific Integrated Circuits(ASICs) 혹은 Field-Programmable Gate Arrays(FPGAs)와 같은 특수 hardware component를 사용한다.
  - 장점
    - Load balancing에 특화된 장비들을 사용하므로 높은 성능을 보인다.
    - 종종 보안, monitoring 등의 부가적인 기능이 추가된 장비들도 있다.
  - 단점
    - 가격이 비쌀 수 있다.
    - 초기에 구성하고 사용하는데 전문적인 지식을 필요로한다.
    - 확장시에 추가적인 장비 구입이 필요할 수 있다.



- Software Load Balancing
  - Software를 사용하여 load balancing을 하는 것이다.
  - 장점
    - 일반적으로 hardware load balancer 보다 구축하기 쉽다.
    - 확장이 쉽다.
    - 클라우드 환경을 비롯한 다양한 platform에 배포가 가능하다.
  - 단점
    - Hardware load balancer에 비해 낮을 성능을 보일 수 있다.
    - Host system의 자원을 소비하므로, 같은 host system을 사용하는 다른 application에 영향을 줄 수 있다.
    - 지속적인 software update가 필요할 수 있다.



- Cloud-based Load Balancing

  - Cloud 제공자가 제공하는 load balancer이다.

  - 장점
    - 확장성이 높다.
    - Cloud 제공자가 관리에 필요한 기능과 update를 제공하므로 관리가 쉽다.
    - 사용한 만큼만 비용을 지불하면 된다.
  - 단점
    - Cloud 제공자에게 의존할 수 밖에 없다.
    - Custom이 제한적이다.



- DNS Load Balancing

  - DNS infrastructure를 사용하여 load balancing하는 방식이다.
    - 예를 들어 CDN(Content Delivery Network)은 DNS load balancing을 사용하여 사용자와 가장 가까운 지리적 위치에 있는 server로 요청을 보낸다.

  - 장점
    - 상대적으로 구현하기 쉬우며 전문적인 hardware나 software를 필요로하지 않는다.
    - 지리적 정보에 기반하여 요청을 분산할 수 있다.
  - 단점
    - DNS resolution time이 제한되므로 다른 load balancing 기법에 비해 update 속도가 느릴 수 있다.
    - Server의 상태나 response time 등에 대해 고려하지 않는다.
    - Session persistence 요구되거나 섬세한 부하 분산에는 적절하지 않다.



- Global Server Load Balancing(GSLB)

  - 지리적으로 분산된 data center로 부하를 분산하는 방식이다.

    - DNS load balancing 방식에 server health check 등 보다 향상된 기능을 추가한 방식이다.

  - 장점

    - 여러 지리적 위치에 있는 data center로 요청을 분산시킬 수 있다.

    - 사용자의 요청을 가장 가까운 곳으로 분산시켜 응답 속도를 높일 수 있다.
    - Server 상태 확인, session persistence, custom routing 정책 등을 설정할 수 있다.

  - 단점

    - 초기 구성과 이후의 유지보수가 상대적으로 복잡하다.
    - 전문적인 hardware나 software가 필요할 수 있다.
    - 느린 update나 caching 문제 등 DNS의 제한 사항이 문제가 된다.



- Layer 4 Load Balancing
  - Transport layer라고 불리는 4 계층에서 load balancing을 수행한다.
    - Traffic을 TCP 또는 UDP header의 정보(IP 주소나 port)를 기반으로 분산시킨다.
  - 장점
    - 제한된 정보만을 가지고 결정을 내리기 때문에 빠르고 효율저이다.
    - 광범위한 protocol과 traffic type을 처리할 수 있다.
    - 상대적으로 구현과 관리가 쉽다.
  - 단점
    - Application 수준의 정보는 사용하지 않으므로 특정 시나리오에서 효율성이 떨어질 수 있다.
    - Server 상태, response time 등을 고려하지 않는다.
    - Session persistence가 요구되거나 fine-grained 작업을 처리해야 하는 상황에서는 부적절 할 수 있다.



- Layer 7 Load Balancing

  - Application layer라 불리는 7계층에서 load balancing을 수행한다.
    - Application과 관련된 정보(HTTP header, cookies, URL 경로 등)를 기반으로 load balancing을 수행한다.

  - 장점

    - Application 수준의 정보를 고려하므로 보다 섬세한 load balancing이 가능하다.
    - Session persistence나 content-based routing, SSL offloading 등의 기능을 제공할 수 있다.

    - 특정 application의 요구사항이나 protocol에 적합하도록 수정이 가능하다.

  - 단점
    - Layer 4 load balancing과 비교했을 때 보다 많은 정보를 고려하므로, 상대적으로 느리고 자원 집약적이다.
    - 전문적인 software나 hardware가 필요할 수 있다.
    - 상대적으로 복잡도가 높아 관리가 힘들 수 있다.





# API Gateway vs. Load Balancer vs. Reverse proxy

> https://medium.com/geekculture/load-balancer-vs-reverse-proxy-vs-api-gateway-e9ec5809180c

- Load Balancer, Reverse Proxy, API Gateway는 software architecture에서 매우 중요한 역할을 담당하는 component들이다.
  - 이들은 고유한 목적을 가지고 있으므로, 이들을 잘 구분하여 필요에 따라 적절한 component를 선택할 수 있어야한다.
    - 그러나 이들은 비슷한 역할을 공유하기도 해서 이들을 구분하는 것이 쉽지 않을 수 있다.

  - 식당의 비유
    - 만약 application이 식당이라면 아래와 같은 비유가 가능하다.
    - Load Balancer는 headwaiter로써 모든 고객들이 식탁에 고르게 앉을 수 있도록한다.
    - Reverse proxy는 숙련된 waiter로써 주문을 처리하고, 모든 고객들이 최상의 경험을 할 수 있도록 돕는다.
    - API Gateway는 식당의 관리인으로써 식당의 모든 과정을 감독하고 통제하는 역할을 한다.




- Load Balancer
  - Service가 대량의 traffic을 처리할 수 있도록 아래와 같은 역할을 수행한다.
    - 자원을 최적으로 활용할 수 있도록 한다.
    - 처리량(throughput)을 최대화한다.
    - 응답 시간을 최소화한다.
  - Layer 4 vs. Layer 7 load balancer
    - Load balancer는 OSI 7계층 중 4 계층과 7 계층에서 각기 다른 역할을 수행한다.
    - Transport layer에서 동작하는 layer 4 load balancer는 IP 주소와 TCP/UDP port 같은 network 수준의 정보에 기반해서 결정을 내린다.
    - Application layer에서 동작하는 layer 7 load balancer는 HTTP header, cookie, URL path와 같은 정보를 활용하여 보다 세부적인 결정을 내린다.
    - 둘 중 어느 것이 더 적당한지는 service에 따라 달라진다.
  - Load balancing algorithm
    - Load balancer는 traffic을 분산시키기 위해 다양한 algorithm을 사용한다.
    - 어떤 algorithm을 사용하는지가 application의 성능과 확장성에 큰 영향을 미친다.
  - DDoS(Distributed Denial-of-Service) 방지
    - Traffic을 분산시키고 일반적이지 않은 traffic pattern을 monitroing하여 잠재적인 위협을 탐지할 수 있다.



- Reverse Proxy
  - Application layer인 7 계층에서 동작한다.
    - HTTP 수준에서 request와 response를 처리한다.
    - URL 재작성, SEO 향상과 같은 추가적인 기능을 제공할 수 있다.
  - 기능
    - Server가 핵심 기능에만 집중할 수 있도록 해주어 server의 성능을 높이고 부하를 줄이는 역할을 한다.
    - Server로의 접근을 단일 지점을 통해 하도록 함으로써 server를 보다 간편하게 확장시킬 수 있게 해준다.
  - 보안
    - Request가 들어왔을 때 이들을 filtering하여 악의적인 traffic이 server로 전달되지 못하도록 막는 역할을 한다.



- API Gateway

  - Microservice 기반의 application에서 service들을 관리하기 위한 방식이다.
    - 여러 개의 service들을 중앙 집중화 하여 관리한다.
    - 모든 API의 호출에 대한 단일 entry point처럼 동작한다.
  - 기능
    - Request와 response를 필요에 따라 수정하여 유연성을 향상시킬 수 있다.
    - 모든 요청이 gateway를 거쳐가므로, 전체 application에 대한 monitoring 기능을 개발하기 수월하다.
  - 보안
    - Authentication을 담당한다.
    - 중앙 집중화된 authentication과 authorization을 구현하여 각 service마다 이들을 중복하여 구현해야 하는 번거로움을 제거해준다.



- Load Balancer, Reverse Proxy, API Gateway의 핵심적인 차이
  - Load balacner와 reverse proxy의 차이
    - 둘 다 요청을 분산한다는 공통첨이 있다.
    - 그러나 load balancer는 여러 backend server에 traffic을 분산하여 성능과 가용성, 그리고 장애 허용성을 향상시키는 데 초점이 맞춰져있다.
    - 반면에 reverse proxy는 application layer에 위치하여 URL rewriting, content compression, access control과 같은 추가적인 기능을 제공하는 데 초점이 맞춰져있다.
  - API gateway의 경우에는 다른 두 component와 달리 요청을 분산하는 역할을 하지는 않는다.
    - 정확히는 API gateway는 request를 routing하고, 다른 두 component는 요청을 distributing한다.
    - API gateway의 주요 목적은 microservice architecture에서 여러 API들을 중앙집중화하여 관리하는 것이다.
    - Loac balancer나 reverse proxy와는 달리 인증, rate limiting, request/response 변환, monitoring과 같은 향상된 기능을 제공한다.



- 많이 사용되는 tool과 solution
  - Load balancer
    - HAProxy, Nginx, Amazon ELB(Elastic Load Balaning) 등이 있다.
    - 이중 HAProxy는 Github이나 Stack Overflow 등이 사용하는 신뢰도 높은 open source load banacer이다.
  - Reverse proxy
    - Nginx, Apache HTTP Server, Microsoft IIS 등이 있다.
    - Nginx는 web server, reverse proxy, load balancer의 역할을 모두 할 수 있는 open source로 개발된 tool이다.
  - API gateway
    - Kong, Amazon API Gateway, Apigee 등이 있다.
    - Kong은 Nginx 기반으로 만들어진 open source API gateway이다.







