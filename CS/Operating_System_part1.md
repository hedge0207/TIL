# 운영체제 개요

- 운영체제(OS, Operating System)
  - 정의
    - 사용자가 보다 편리하게 컴퓨터를 조작할 수 있도록 인터페이스를 제공하고, 컴퓨터 시스템의 자원을 효율적으로 관리하기 위한 소프트웨어.
  - 펌웨어(Firmware)
    - 운영체제 역시 일종의 소프트웨어이다.
    - 또한 하드웨어를 조정하고 관리하는 역할을 하는 운영체제의 특성 상 하드웨어의 도움 없이 작동하기 어렵다. 
    - 따라서 운영체제를 부를 때 소프트웨어와 하드웨어를 결합한 형태인 펌웨어라고 부르기도 한다.
  - 임베디드 운영체제(Embeded operating system, 임베디드 시스템)
    - CPU의 성능이 낮고 메모리 크기도 작은 시스템에 내장하도록 만든 운영체제.
    - 일반 운영체제에 비해 몇 가지 기능이 빠져있다.
    - 임베디드 운영체제를 사용하는 기계와 그렇지 않은 기계는 많은 차이가 있다.
    - 예를 들어 임베디드 운영체제가 없는 유선전화는 통화 외에 다른 기능을 추가할 수 없는 반면, 운영체제를 사용하는 스마트폰은 응용 프로그램인 앱을 설치하여 게임을 하거나 내비게이션 등으로 사용할 수 있다.



- 운영체제의 목표
  - 효율성
    - 운영체제의 목표는 자원을 효율적으로 관리하는 것이다.
    - 적은 자원을 사용하여 더 많은 작업량을 처리하거나, 같은 작업량을 처리하는 데 보다 적은 자원을 사용해야 한다는 의미이다.
  - 안정성
    - 운영체제는 하드웨어 전체를 관리하는 소프트웨어이므로 운영체제가 불안정하면 모든 작업이 불안정할 수 밖에 없다.
    - 따라서 운영체제는 안정적으로 자원을 보호하고, 자원을 관리해야한다.
  - 확장성
    - 다양한 시스템 자원을 추가하거나 제거하기 편리해야한다.
    - 운영체제는 하드웨어의 종류에 상관없이 연결하면 바로 실행할 수 있는 플러그 앤 플레이(Plug & Play) 기능을 제공해야한다.
  - 편리성
    - 사용자가 편리하게 작업할 수 있는 환경을 제공해야한다.
    - 응용 프로그램과 사용자에게 대양한 편리성을 제공하면서도 자원의 낭비는 막아야한다.



- 운영체제의 필요성
  - 컴퓨터는 운영체제 없이도 작동한다.
    - 초기의 컴퓨터는 정해진 계산만 수행했기에 특별한 사용 규칙이 필요없었다.
  - 그러나 메모리, CPU의 성능이 향상되고, 여러 작업을 동시에 할 수 있는 컴퓨팅 환경이 조성되면서 사용 규칙이 필요해졌다.
  - 복잡한 작업 환경에 규칙이 없으면 기계를 망가뜨릴 수도 있기 때문에 등장한 것이 운영체제이다.



- 운영체제의 역할
  - 운영체제는 컴퓨터 자원(computer resource)을 관리한다.
    - 컴퓨터에 부착된 모든 장치를 컴퓨터 자원이라한다.
    - 운영체제는 컴퓨터에서 사용하는 자원을 관리(resource management)하는 역할을 수행한다.
    - 컴퓨터에서 여러 응용 프로그램(application program)을 동시에 실행할 경우 각 응용프로그램은 컴퓨터 자원을 독차지하려고 한다.
    - 운영체제는 이러한 응용 프로그램들 사이에서 컴퓨터 자원을 적절하게 분배하는 역할을 한다.
    - 예를 들어 채팅 프로그램과 문서 작성 프로그램은 둘 다 키보드와 모니터라는 공통의 컴퓨터 자원을 필요로 한다.
    - 이 때 운영체제는 누구에게 먼저 키보드의 제어권을 주어야할지, 누구에게 모니터의 제어권을 주어야 할지 등을 결정한다.
  - 사용자와 하드웨어 사이의 중계자 역할을 한다.
    - 운영체제는 사용자가 컴퓨터 자원에 직접 접근하는 것을 막는다.
    - 예를 들어 사용자가 하드디스크의 특정 위치에 데이터를 저장하려 한다고 생각해보자.
    - 사용자는 하드디스크의 특정 위치에 데이터를 저장할 수 없으며, 운영체제에게 데이터의 저장을 요청하면 운영체제가 하드디스크의 적절한 위치에 데이터를 저장한다.
    - 이처럼 운영체제는 사용자와 하드웨어 사이의 중계자 역할을 함으로써 컴퓨터 자원을 보호하고 관리한다.
  - 하드웨어 인터페이스를 제공한다.
    - 하드웨어 장치와 상호작용하기 위해 만들어진 응용 프로그램을 드라이버(장치 드라이버, 디바이스 드라이버, 소프트웨어 드라이버 등으로도 부른다)라고 부른다. 
    - 일반적으로 드라이버는 운영체제를 설치할 때 자동으로 설치되지만, 일부 하드웨어의 경우 따로 설치해야 하는데, 이렇게 따로 설치해야하는 드라이버를 하드웨어 인터페이스라 부른다.  
    - 운영체제는 일관된 하드웨어 인터페이스를 제공함으로써 하드웨어가 변경되더라도, 사용자가 일관된 방식으로 컴퓨터를 사용할 수 있게 해준다.
  - 운영체제를 통해 새로운 기능의 추가나 성능의 향상이 가능하다.
    - 운영체제가 없는 기계는 기능을 추가하거나 성능을 향상시키기 위해선 기계 자체를 변경시켜야한다.
    - 그러나 운영체제가 있을 경우, 많은 경우 기계 자체를 변경시키지 않고도 운영체제를 통해 기능의 추가와 성능의 향상이 가능하다.



- 컴퓨팅 환경의 역사
  - 초창기 컴퓨터(1940년대)
    - 최초의 컴퓨터는 미사일 탄도를 계산하기 위해 제작된 에니악으로 18,000개 가량의 백열전구 모양의 진공관을 조합하여 제작된 30톤 큐모의 거대한 계산기였으며, 운영체제는 없었다.
    - 사용하여 진공관이 켜지면 1, 꺼지면 0이 되는 방식으로 계산이 이루어졌는데, 이는 컴퓨터가 2진법을 사용하는 계기가 되었다.
    - 각 진공관을 전선으로 연결하는 방식으로 프로그래밍이 이루어졌는데, 이렇게 전선을 연결하여 논리회로를 구성하는 것을 하드 와이어링 방식이라고 한다.
    - 하드 와이어링은 전선으로 논리회로를 구성하여 원하는 결과만 얻는 방식이므로 다른 계산이나 수식을 사용하려면 전선을 다시 연결해야 했다. 
  - 일괄 작업 시스템(1950년대)
    - 초창기 컴퓨터는 기술 발전을 거쳐 IC(integrated Circuit)라는 칩으로 만들어졌다.
    - 진공관과 전선으로 만들어진 논리회로를 아주 작은 크기로 구현한 것으로, 현대적인 모습의 컴퓨터가 탄생했다.
    - 카드에 구멍을 뚫어 문자나 숫자를 표현하고, 이 카드를 읽는 천공카드 리더를 입력장치로, 문자를 한 번에 한 줄씩 출력하는 라인 프린터를 출력장치로 사용했다.
    - 이를 통해 현재의 프로그래밍과 유사한 방식으로 다양한 소프트웨어를 개발할 수 있게 되었다.
    - 하드 와이어링은 다른 작업을 하려면 전선을 일일이 다시 연결해야 가능했지만, 천공 카드 리더를 사용하면, 천공카드만 바꾸면 다른 작업이 가능했다.
    - 현재와는 달리 작업에 필요한 프로그램과 데이터를 한꺼번에 입력해야 작업이 가능했는데, 이처럼 모든 작업을 한꺼번에 처리해야 하고 프로그램 실행 중간에 사용자가 데이터를 입력하거나 수정하는 것이 불가능한 시스템을 일괄 작업 시스템(batch job system) 혹은 일괄 처리 시스템(batch processing system)이라 부른다.
    - 일괄 작업 시스템은 작기는 하지만 운영체제가 사용되었기에 현재까지도 그 흔적이 남아있는데, 대표적으로 `.bat` 파일은 batch job을 의미한다.
  - 대화형 시스템(1960년대 초반)
    - 1960년대 초반에 키보드와 모니터가 등장했는데, 이로 인해 비효율적이었던 일괄 작업 시스템 방식이 획기적으로 변화되었다.
    - 키보드와 모니터가 개발됨으로써 프로그램 실행 중에 중간 결과값을 확인할 수 있게 되었고, 중간에 데이터를 입력할 수 있게 되었다.
    - 프로그램이 실행되는 도중에 사용자로부터 입력을 받아 입력값에 따라 작업의 흐름을 바꾸는 것도 가능했는데, 이 모습이 사용자와 컴퓨터 간의 대화를 통해 이루어지는 것 같다 하여 대화형 시스템(interactive system)이라고 부른다.
    - 단, 중간에 입출력 될 일이 없어 작업 시간을 예측하기 쉬웠던 일괄 작업 시스템과 달리, 대화형 시스템의 경우 중간에 어떤 값이 입력되는지에 따라 작업 시간이 달라지기에 작업 시간을 예측하기도 어렵다는 문제가 있었다.
  - 시분할 시스템(1960년대 후반)
    - 1960년 후반에 컴퓨터의 크기가 작아지고 계산 능력이 향상이 이루어졌다.
    - 향상된 컴퓨터의 성능을 보다 효율적으로 사용하기 위해서 다중 프로그래밍(multiprogramming) 기술이 개발되었다.
    - 다중 프로그래밍은 하나의 CPU로 여러 작업을 동시에 실행하는 기술로, 한 번에 하나의 작업만 가능한 일괄 작업 시스템에 비해서 효율이 뛰어났다.
    - 실제로 여러 작업이 동시에 실행되는 것은 아니고 CPU 사용 시간을 잘게 쪼개에 여러 작업들에 나눠주고, 각 작업들이 매우 짦은 간격으로 돌아가면서 CPU를 사용하는 방식이었는데, 그 간격이 매우 짧아 마치 동시에 실행되는 것 처럼 보이는 것이다.
    - 이처럼 여러 작업을 조금씩 처리하여 작업이 동시에 이루어지는 것처럼 보이게 하는 것을 시분할 시스템(time sharing system, 혹은 multitasking)이라 부르며, 오늘날 대부분의 컴퓨터에서 사용된다.
    - 이 때 잘게 나뉜 시간 한 조각을 time slice 혹은 time quantum이라 부르고, 시분할 시스템에서 동시에 실행되는 작업의 개수를 멀티 프로그래밍 수준(level of multoprogramming) 혹은 멀티 프로그래밍 정도(multiprogramming degree)라 부른다.
    - 시분할 시스템을 통해 여러 사용자가 하나의 컴퓨터에서 작업하는 다중 사용자 시스템이 가능해졌다.
    - 시분할 시스템의 단점은 여러 작업을 동시에 처리하기 위한 추가 작업이 필요하다는 것이다.
    - 또한 시스템 내에 많은 양의 작업이 있을 경우, 특정 작업이 일정 시간 내에 끝날 것을 보장하지 못한다.
  - 분산 시스템(1970년대 후반)
    - 스티브 잡스가 최초의 개인용 컴퓨터인 애플Ⅱ를 발표했으며, 이후 개인용 컴퓨터가 이전보다 널리 보급되기 시작한다.
    - 또한 소프트웨어도 급속도로 발전하여 개인용 컴퓨터 운영체제로 애플의 매킨토시와 MS의 MS-DOS등이 등장했다.
    - 인터넷이 등장한 것도 이 시기이다.
    - 개인용 컴퓨터의 보급과 인터넷의 등장으로 값이 싸고 크기가 작은 컴퓨터들을 하나로 묶어 대형 컴퓨터에 버금가는 시스템을 만들게 되었는데, 이를 분산 시스템이라 부른다.
    - 분산 시스템은 네트워크상에 분산되어 있는 여러 컴퓨터로 작업을 처리하고 그 결과를 상호 교환하도록 구성한 시스템이다.
  - 클라이언트/서버 시스템(1990년대 ~ 현재)
    - 분산 시스템은 시스템에 참가하는 모든 컴퓨터가 동일한 지위를 가지기에 새로운 컴퓨터가 추가되거나 기존 컴퓨터가 제거되면 작업을 분배하고 결과를 모으기 쉽지 않다.
    - 클라이언트/서버 시스템은 이러한 문제를 해결하기 위한 기술로, 모든 컴퓨터의 지위가 동일한 분산 시스템과 달리 요청하는 클라이언트와 응답하는 서버의 이중 구조로 구성된다.
    - 서버가 과부화 될 수 있다는 문제가 있다.
  - P2P 시스템(2000년대 초반 ~ 현재)
    - 서버를 거치지 않고 사용자와 사용자를 직접 연결하는 시스템으로, 서버의 과부하 문제를 해결하기 위해 등장했다.
    - 메신저, 파일 공유 등에 널리 쓰인다.



## 운영체제의 구조

- 커널과 인터페이스
  - 운영체제는 크게 커널과 인터페이스로 구성된다.
  - 커널(Kernel)
    - 프로세스 관리, 메모리 관리, 저장장치 관리와 같은 운영체제의 핵심적인 기능을 모아놓은 것이다.
    - 운영체제의 성능은 커널이 좌우한다.
  - 인터페이스
    - 인터페이스는 사용자의 명령을 커널에 전달하고 실행 결과를 사용자에게 전달하는 역할을 한다.
    - 커널과 인터페이스가 분리되어 있으므로 같은 커널이라도 다른 인터페이스를 사용할 수 있다.
    - 예를 들어 유닉스의 사용자 인터페이스은 shell은 Cshell(csh), Tshell(tsh), bash 등 여러 종류의 shell이 있다.



- 시스템 호출(System Call)과 드라이버(Driver)
  - 시스템 호출
    - 커널이 제공하는 시스템 관련 서비스를 모아놓은 것으로, 함수 형태로 제공된다.
    - 커널이 자신을 보호하기 위해 만든 인터페이스로, 사용자나 응용 프로그램으로부터 컴퓨터 자원을 보호하기 위해 자원에 직접 접근하는 것을 차단한다.
    - 따라서 자원을 이용하려면 시스템 호출이라는 인터페이스를 이용하여 접근해야한다.

  - 시스템 호출을 통한 접근의 이점
    - 사용자가 컴퓨터 자원에 직접 접근할 경우 사용자가 모든 것을 처리해야한다.
    - 따라서 사용자가 잘못된 방식으로 컴퓨터 자원에 접근할 경우 컴퓨터 자원에 이상이 생길 수 있다.
    - 반면에 시스템 호출을 통해 접근할 경우 커널을 통해 시스템 자원에 접근하므로 이러한 위험이 줄어들게 된다.

  - 드라이버
    - 커널과 응용 프로그램 사이의 인터페이스가 시스템 호출이라면, 커널과 하드웨어의 인터페이스가 드라이버이다.
    - 운영체제가 많은 하드웨어를 다 사용할 수 있는 환경을 제공하려면 각 하드웨어에 맞는 프로그램을 직접 개발해야하지만, 커널이 모든 하드웨어에 맞는 인터페이스를 다 개발하기는 어렵다.
    - 따라서 커널은 입출력의 기본적인 부분만 제작하고, 하드웨어의 특성을 반영한 소프트웨어를 하드웨어에 대해서 가장 잘 아는 하드웨어를 제작한 사람에게 전달받아 커널이 실행될 때 함께 실행되도록 한다.
    - 여기서 하드웨어를 제작자가 만든 소프트웨어를 드라이버라한다.
    - 물론 마우스, 키보드 같은 간단한 하드웨어를 위한 드라이버의 경우 커널에 포함되어 있는 경우도 있다.
  - API와 SDK
    - API(Application Programming Interface)란 응용 프로그램이 자신과 연관된 프로그램을 만들 수 있도록 제공하는 인터페이스이다.
    - SDK(Software Developer's Kit)는 프로그램 개발자를 위해 API 및 API 용 메뉴얼뿐만 아니라 개발에 필요한 코드 편집기와 에뮬레이터 같은 각종 개발용 응용 프로그램까지 하나로 묶어서 배포하는 개발 툴이다.




- 커널의 구성

  - 커널의 주요 역할

  | 역할                                                   | 설명                                                         |
  | ------------------------------------------------------ | ------------------------------------------------------------ |
  | 프로세스 관리                                          | 프로세스에 CPU를 배분하고, 작업에 필요한 제반 환경을 제공한다. |
  | 메모리 관리                                            | 프로세스에 작업 공간을 배치하고 실제 메모리보다 큰 가상공간을 제공한다. |
  | 파일 시스템 관리                                       | 데이터를 저장하고 접근할 수 있는 인터페이스를 제공한다.      |
  | 입출력 관리                                            | 필요한 입력과 출력 서비스를 제공한다.                        |
  | 프로세스간 통신(IPC, Inter-Process Communication) 관리 | 공동 작업을 위핸 각 프로세스 간 통신 환경을 지원한다.        |

  - 커널의 종류
    - 커널의 주요 기능들을 어떻게 구현하는가에 따라 아래와 같이 나뉜다.
    - 단일형 구조 커널
    - 계층형 구조 커널
    - 마이크로 구조 커널
  - 단일형 구조 커널(Monolithic Architecture Kernel)
    - 초창기의 운영체제 구조로 커널의 핵심 기능을 구현하는 모듈들이 구분 없이 하나오 구성되어 있다.
    - 모듈이 거의 분리되지 않았기 때문에 모듈 간의 통신 비용이 줄어 효율적인 운영이 가능하다는 장점이 있지만, 아래와 같은 단점들이 있다.
    - 버그나 오류를 처리하기 힘들다.
    - 상호 의존성이 높아 기능상의 작은 결함이 시스템 전체로 확산될 수 있다.
    - 수정이 어렵기에 다양한 환경의 시스템에 적용하기 어렵다.
    - 현대의 크고 복잡한 운영체제를 구현하기에는 부적절하다.
    - MS-DOS, VMS, 초기의 유닉스 등이 이에 해당한다.
  - 계층형 구조 커널(Layered Archtecture Kernel)
    - 단일형 구조 커널이 발전된 형태로, 비슷한 기능을 가진 모듈을 묶어서 하나의 계층으로 만들고 계층 간의 통신을 통해 운영체제를 구현하는 방식이다.
    - 비슷한 기능을 모아 모듈화했기 때문에 단일형 구조보다 버그나 오류를 쉽게 처리할 수 있다.
    - 오류가 발생했을 때 해당 계층만 수정하면 되기에 디버깅도 쉽다.
    - Windows를 비롯한 오늘날 대부분의 운영체제는 이 구조로 개발되었다.
  - 마이크로 구조 커널(Micro Architecture Kernel)
    - 하드웨어의 다양화, 이에 따른 운영체제의 기능 추가에 따라 계층형 커널 구조에  점차 새로운 계층이 추가됐다.
    - 이에 따라 커널의 크기도 지속적으로 증가하고 소스도 방대해져 오류를 잡기가 점점 힘들어졌다.
    - 이러한 한계를 극복하기 위해 등장한 것이 마이크로 구조 커널이다.
    - 마이크로 구조 커널의 운영체제는 프로세스 관리, 메모리 관리, IPC 관리 등의 가장 기본적인 기능만 제공하고, 운영체제의 많은 부분이 사용자 영역에 구현되어 있다.
    - 각 모듈이 독립적으로 작동하고, IPC 모듈로 각 모듈 사이의 통신이 이루어지므로, 하나의 모듈이 실패하더라도 전체 운영체제가 멈추지 않는다.
    - 애플의 OS X와 iOS가 사용하는 마하(Mach)가 이 구조를 사용한다.



- 가상머신
  - 초기의 응용 프로그램은 일반적으로 운영체제에 종속적이었다.
    - 예를 들어 유닉스에서 개발한 응용 프로그램은 Windows에서는 동작하지 않았다.
  - 따라서 각 운영체제별로 응용프로그램을 따로 제작해야했다.
  - 이러한 호환성 문제를 해결한 것이 바로 가상머신이다.
    - 가상머신은 운영체제와 응용 프로그램 사이에서 동작하는 프로그램으로, 응용 프로그램이 운영체제와 독립적으로 실행되도록 해준다.
    - JVM이 대표적인 예이다.



- Unix의 간략한 역사
  - 유닉스(Unix)
    - 1969년, AT&T의 연구원인 켄 톰프슨(Ken Tompson), 데니스 리치(Dennis Ritchie), 피터 뉴만(Peter Neumann)은 어셈블리어를 사용하여 프로그램을 실행하는 데에만 중점을 둔 단순한 운영체제를 개발했다.
    - 단순함을 강조하기 위해 유닉스라는 이름을 붙였다.
    - 데니스 리치는 B언어에서 출발한 C 언어를 고안했다.
    - C 언어는 어셈블리어로 번역하기 쉬워 많은 컴퓨터에 이식할 수 있었다.
    - 1973년 어셈블리어로 개발된 유닉스를 C 언어로 다시 제작했고, 다른 기계로 이식이 쉬웠던 C 언어 특성 덕에 많은 인기를 끌게 되었다.
    - 또한 유닉스는 소스코드가 공개되어 계속 다른 기종의 컴퓨터로 이식되며 여러 기업과 연구 기관에서 이를 이용한 연구가 거듭되며 발전해나갔다.
  - BSD(Berkeley Software Distribution) Unix
    - 1970년대 말 캘리포니아 대학의 버클리 캠퍼스에서 빌 조이(Bill Joy)와 척 헤일리(Chuck Haley)라는 학생이 소스코드를 조금 수정한 유닉스를 BSD라는 이름으로 발표했다.
    - 기존 AT&T 유닉스와는 달리 다중 작업과 네트워킹 기능이 추가되어 큰 인기를 끌었다.
    - AT&T는 이에 위협을 느껴 USG(Unix Support Group)을 설립하고 자신의 유닉스를 AT&T System V라고 명명했다.
    - 이때부터 유닉스는 크게 System V 계열과 BSD 계열로 나뉘게 되었다.
  - GNU(GNU is Not Unix)
    - 리터드 스톨먼(Richard Stallman)이 창설한 프로젝트로, 소프트웨어를 돈 주고 사지 말고 누구나 자유롭게 실행, 복사, 수정, 배포할 수 있게 하자는 프로젝트이다.
    - 이러한 정신에 입각해서 만든 소프트웨어에 주어진 라이선스를 GPL(General Public Licence)라고 부른다.
    - GPL은 copyright의 반대 개념으로 copyleft를 내세웠다.
  - Linux
    - 1991년 리누스 토르발스(Linus Torvalds)가 PC에서 동작하는 유닉스 호환 커널의 작성하여 GPL로 배포하고, 소스코드도 공개했다.
    - 이것이 바로 리눅스이다.





# 컴퓨터의 구조

## 컴퓨터의 기본 구성

- 하드웨어의 구성

  - 컴퓨터는 중앙처리장치(CPU), 메인메모리, 입력장치, 출력장치, 저장장치로 구성된다.
    - 컴퓨터로 하는 작업의 대부분은 중앙처리장치와 메인메모리의 협업으로 이루어지기에 중앙처리장치와 메인메모리는 필수 장치로 분류된다.
    - 그 외의 부품은 주변장치라 부른다.
  - CPU
    - 명령어를 해석하여 실행하는 장치.
  - 메인 메모리
    - 전력이 끊기면 데이터를 잃어버리기에 데이터를 영구히 보관하려면 하드디스크나 USB 메모리를 사용해야한다.
    - 따라서 메인메모리를 제1저장장치(first storage), 하드 디스크 혹은 USB 메모리를 제2저장장치(second storage)라 부른다.
  - 입출력장치
    - 외부의 데이터를 컴퓨터에 입력하고, 컴퓨터에서 처리한 결과를 사용자가 원하는 형태로 출력하는 장치이다.

  - 저장장치
    - 메인 메모리와 달리 데이터를 영구적으로 저장하는 장치이다.
    - 메모리보다 느리지만 저렴하고 용량이 크다.
  - 메인보드
    - 컴퓨터의 다양한 부품은 버스로 연결된다.
    - 실제 세상의 버스와 마찬가지로 컴퓨터의 버스도 일정한 규칙에 따러 각 장치에 데이터를 전송하는 역할을 한다.
    - 메인보드는 다양한 부품을 연결하는 커다란 판이다.



- 폰노이만 구조(von Neumann achitecture)
  - 폰 노이만 구조는 CPU, 메모리 입출력장치, 저장장치가 버스로 연결되어 있는 구조를 말한다.
    - 폰 노이만 구조가 등장하기 이전의 컴퓨터는 전선을 연결하여 회로를 구성하는 하드와이어링 형태였기에 다른 용도로 사용하여면 전선을 바꿔야했다.
    - 존 폰 노이만(John von Neumann)은 이를 해결하기 위해 메모리를 이용하여 프로그래밍이 가능한 구조를 제안했다.
    - 하드웨어는 그대로 두고 실행할 프로그램만 교체하여 메모리에 올리는 방식이었다.
  - 폰노이만 구조에서 가장 중요한 점은 모든 프로그램은 메모리에 올라와야 실행할 수 있다는 것이다.



- 하드웨어 사양 관련 용어
  - 클록(clock)
    - CPU의 속도오 관련된 단위.
    - CPU가 작업을 실행할 때 일정한 박자가 있는데, 이 박자를 만들어내는 것이 클록이다.
    - 클록이 일정 간격으로 tick을 만들면 거기에 맞추어 CPU안의 모든 구성 부품이 작업을 한다.
    - 틱은 펄스(pulse) 혹은 clock tick이라고도 부른다.
    - 메인보드의 클록이 틱을 보낼 때 마다 버스를 통해 데이터를 보내거나 받는다.
  - 헤르츠(Hz)
    - 클록틱이 발생하는 속도를 나타내는 단위이다.
    - 1초에 클록틱이 몇 번 발생하는지를 나타낼 때 1초에 클록틱이 한 번 발생하면 1Hz와 같은 식이다.
    - 예를 들어 1kHz(==1000Hz)이면 초당 1천 번의 데이터 이동이 가능하다는 의미이다.
  - 시스템 버스와 CPU 내부 버스
    - 시스템 버스는 메모리와 주변장치를 연결하는 버스로 FSB(Front-Side Bus)라고 부른다.
    - CPU 내부 버스는 CPU 내부에 있는 장치를 연결하는 버스로 BSB(Back Side Bus)라고 부른다.
    - CPU 내부 버스의 속도는 CPU의 클록과 같아서 시스템 버스보다 훨씬 빠르다.
    - CPU는 BSB의 속도로 작동하고, 메모리는 FSB의 속도로 작동하기에 두 버스의 속도 차이로 인해 작업이 지연되는 문제가 있다.







## CPU와 메모리

- CPU의 구성
  - 아래와 같은 장치들의 협업으로 작업이 이루어진다.
  - 산술논리 연산장치(Arithmetic and Logic Unit, ALU)
    - CPU에서 데이터를 연산하는 장치
    - 덧셈, 뺄셈, 곱셈, 나눗셈과 같은 산술 연산과 and, or과 같은 논리 연산을 수행한다.
  - 제어장치(Cotrol Unit)
    - CPU에서 작업을 지시하는 장치이다.
  - 레지스터(Register)
    - CPU 내에 데이터를 임시로 보관하는 곳이다.



- CPU의 명령어 처리 과정

  - C언어로 작성된 아래와 같은 짧은 코드가 있을 때, CPU는 어떻게 아래 코드를 처리하는가.

  ```c
  int D2=2, D3=3, sum;
  sum=D2+D3
  ```

  - 위에서 작성된 코드는 어셈블리어로 변환된 뒤 게계어로 변환되어 CPU에 의해 실행된다.
    - 우선 선언된 변수들이 메모리에 저장된다.
    - 제어장치는 레지스터에게 신호를 보내 레지스터가 메모리에 저장된 변수들을 읽어와서 레지스터에 저장하도록 한다.
    - 제어장치는 산술논리 연산장치에게 신호를 보내 덧셈을 수행하게 하며, 이 값은 다시 레지스터에 저장된다.
    - 제어장치는 레지스터에게 신호를 보내 결과값을 메모리에 옮겨놓도록 한다.



- 레지스터의 종류

  - 데이터 레지스터(Data Register, DR)

    - 메모리에서 가져온 데이터를 임시로 보관할 때 사용한다.
    - CPU에 있는 대부분의 레지스터가 데이터 레지스터이기 때문에 일반 레지스터 또는 범용 레지스터라고 부른다.

  - 주소 레지스터(Address Register, AR)

    - 데이터 또는 명령어가 저장된 메모리의 주소는 주소 레지스터에 저장된다.

  - 특수 레지스터

    - 데이터 레지스터와 주소 레지스터 외에 특별한 용도로 사용되는 레지스터들로, 사용자가 임의로 변경할 수 없기에 사용자 불가 레지스터(User-Invisible Register)라고 부른다.
    - 프로그램 카운터(Program Counter, PC)는 다음에 실행할 명령어의 주소를 기억하고 있다가 제어장치에 알려주는 역할을 하는데, 이 때문에 명령어 포인터(instruction pointer)라고도 부른다.

    - 명령어 레지스터(Instruction Register, IR)은 현재 실행중인 명령어를 저장하며, 제어장치는 명령어 레지스터에 있는 명령을 해석하여 적절한 제어 신호를 보낸다.
    - 메모리 주소 레지스터(Memory Address Register, MAR)는 메모리에서 데이터를 가져오거나 반대로 메모리로 데이터를 보낼 때 주소를 지정하기위해 사용한다.
    - 메모리 버퍼 레지스터(Memory Buffer Register, MBR)는 메모리에서 가져온 데이터나 메모리로 옮겨 갈 데이터를 임시로 저장하며, 항상 메모리 주소 레지스터와 함께 동작한다.
    - 프로그램 상태 레지스터(Program Status Register, PSR)는 산술논리 연산장치와 관련이 있으며, 연산 결과가 양수인지 음수인지, 0인지 아닌지, 자리 올림 여부 등을 저장한다.



- 버스의 종류
  - 버스는 CPU와 메모리, 주변장치 간에 데이터를 주고받을 때 사용하며, 아래와 같은 종류가 있다.
  - 제어 버스(Control Bus)
    - 다음에 어떤 작업을 할지 지시하는 제어 신호가 오고 간다.
    - 제어버스는 CPU의 제어장치와 연결되어 있다.
    - CPU, 메모리, 주변장치와 양방향으로 오고 간다.
  - 주소 버스(Address Bus)
    - 메모리의 데이터를 읽거나 쓸 때 어느 위치에서 작업할 것인지를 알려주는 주소가 오고 간다.
    - 주변 장치의 경우도 마찬가지로, 하드디스크의 어느 위치에서 데이터를 읽어올지, 어느 위치에 저장할지에 대한 정보가 주소 버스를 통해 전달된다.
    - 메모리 주소 레지스터와 단방향으로 연결되어 있다.
    - 즉 CPU에서 메모리나 주변장치로 나가는 주소 정보는 있지만 주소 버스를 통해 CPU로 전달되는 정보는 없다.
  - 데이터 버스(Data Bus)
    - 제어 버스가 어떤 작업을 할지 신호를 보내고, 주소 버스가 위치 정보를 전달하면 데이터가 데이터 버스에 실려 목적지까지 이동한다.
    - 메모리 버퍼 레지스터와 연결되어 있으며 양방향이다.



- 메모리의 종류
  - RAM과 ROM으로 구분된다.
    - RAM(Random Access Memory): 읽기와 쓰기가 모두 가능한 메모리.
    - ROM(Read Only Memory): 읽기만 가능한 메모리
    - ROM은 RAM과 달리 전력이 끊겨도 데이터를 보관할 수 있지만, 한 번 저장하면 바꿀 수 없다는 단점이 있다.
  - 휘발성 메모리(Volatility memory)
    - 전력이 끊기면 데이터가 사라지는 휘발성 메모리.
    - DRAM(Dynamic RAM)과 SRAM(Static RAM)이 있다.
    - DRAM은 저장된 데이터가 일정 시간이 지나면 사라지므로, 일정 시간마다 다시 재생시켜한다.
    - SRAM은 전력이 공급되는 동안에는 데이터를 보관할 수 있어 재생할 필요가 없으므로 속도가 빠르지만 가격이 빘다ㅏ.
    - 일반적으로 메인메모리에는 DRAM을 사용하고, 캐시 같은 고속 메모리에는 SRAM을 사용한다.
    - SDRAM(Synchronous Dynamic Random Access Memory)은 DRAM이 발전된 형태로, 클록틱(펄스)이 발생할 때마다 데이터를 저장하는 동기 DRAM이다.
  - 비휘발성 메모리(Non-volatility memory)
    - 플래시 메모리(flash memory), FRAM(Ferroelectric RAM), PRAM(Phase change RAM) 등이 있다.
    - 이 중 플래시 메모리는 디지털카메라, MP3, USB 드라이버 같이 전력 없이도 데이터를 보관하는 저장장치로 많이 사용된다.
    - 그러나 플래시 메모리의 각 소자는 사용 횟수가 제한되어 보통 소자 하나당 몇 천번에서 만 번 정도 사용하면 기능을 잃게 된다.
    - 하드디스크를 대체하도록 만든 SSD도 비휘발성 메모리이다. 
