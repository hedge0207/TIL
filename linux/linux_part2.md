# 네트워크 관련 설정과 명령어

## 네트워크 관련 필수 개념

- TCP/IP
  - 컴퓨터끼리 네트워크상으로 의사소통하는 약속을 프로토콜이라 부르는데, 그 중 가장 널리 사용되는 프로토콜의 종류 중 하나다.
  - 통신의 전송/수신을 다루는 TCP(Trasmission Control Protocol)와 데이터 통신을 다루는 IP(Internet Protocol)로 구성된다.



- 호스트 이름과 도메인 이름
  - 호스트 이름은 가각의 컴퓨터에 지정된 이름을 말한다.
  - 도메인 이름(혹은 도메인 주소)은 네트워크 상에서 컴퓨터를 식별하는 의미한다.
  - 호스트 이름이 this고 도메인 이름이 theo.co.kr이면 전체 이름은 this.theo.co.kr로 붙여서 부르며, 이를 FQDN(Fully Qualified Domain Name)이라고 부른다.



- IP 주소
  - 각 컴퓨터이 랜 카드(네트워크 카드)에 부여되며, 중복되지 않는 고유한 주소이다.
    - 즉 네트워크에 연결된 모든 컴퓨터에는 고유한 IP 주소가 있다.
    - 이들은 서로 다르기 때문에 특정 컴퓨터의 IP 주소를 알면 그 컴퓨터가 전 세계 어디에 있든지 접속할 수 있다.
  - 4바이트로 이루어져 있으며 각 자리는 0~255까지의 숫자가 올 수 있다.
    - 모든 컴퓨터에서 자기 자신을 의미하는 IP 주소는 127.0.0.1이다.



-  네트워크 주소
  - 같은 네트워크에 속해있는 공통 주소다.
  - 예를 들어 IP주소가 Server는 192.168.111.100, ServerB는 192.168.111.200, Client는 192.168.111.131라면 이 3대의 컴퓨터는 같은 네트워크에 있으며 서브넷 마스크는 C 클래스(255.255.255.0)를 사용하므로 공통된 네트워크의 주소는 앞의 3자리인 192.168.111.0이 된다.
  - 사설 네트워크
    - 192.168.xxx.xxx는 사설 네트워크의 주소다
    - 사설 네트워크는 외부와 분리된 내부의 별도 네트워크를 의미하며, 주로 공인된 IP 주소가 부족할 때 사용된다.



- 브로드캐스트 주소
  - 내부 네트워크의 모든 컴퓨터가 수신하는 주소를 말한다.
  - 현재 주소의 제일 끝자리를 255로 바꾼 주소다(C클래스의 경우).
  - 브로드 캐스트와 아파트 스피커의 비교
    - 아프트 관리사무실에서 방송을 할 경우, 각 집의 스피커를 통해 전달된다.
    - 하지만 모두가 다 해당 방송에 응답하는 것은 아니다.
    - 자신과 관련 있는 방송이면 응답하겠지만, 자신과 관련이 없다면 무시할 것이다.
    - 브로드 캐스트 주소도 이와 마찬가지로 모든 컴퓨터가 수신은 하지만 모든 컴퓨터가 응답을 하는 것은 아닌 주소이다.



-  게이트웨이
  - 내부 네트워크가 외부로 연결되기 위한 컴퓨터 또는 장비다.
  - 내부 네트워크에 있는 컴퓨터끼리 통신할 경우 외부로 나갈 필요가 없으므로 게이트웨이가 없어도 되지만, 인터넷을 사용하기 위해 외부에 접속하려면 반드시 게이트웨이의 IP 주소를 알아야한다.
  - 게이트웨이는 쉽게 말해 외부 네트워크로 나가기 위한 통로로 생각하면 된다.
  - 그러므로 게이트웨이는 내부로 향하는 문(네트워크 카드)과 외부로 향하는 문(네트워크 카드)이 있어야 한다.
  - 즉, 두 개의 네트워크 카드가 장착되어 있어야 한다.



- 넷마스크와 클래스
  - 넷마스크
    - 네트워크의 규모를 결정한다.



- DNS 서버 주소
  - 인터넷을 사용할 때 URL읠 해당 컴퓨터의 IP 주소로 변환해주는 서버 컴퓨터를 말한다.
  - DNS 서버의 주소를 사용하지 않거나 주소가 잘못 입력되어 있으면 웹사이트에 정상적으로 접속되지 않으므로 올바른 정보를 설정해야 한다.
  - 설정 파일은 `/etc/resolv.conf`이며, `nameserver <DNS서버 IP>` 형식으로 설정되어 있다.



- 리눅스에서 네트워크 장치 이름
  - 랜 카드가 리눅스에 장착되었을 때, Ubuntu 기준으로 해당 랜 카드의 이름을 ens32 또는 ens33으로 인식한다.





## 네트워크 관련 명령어

- 네트워크 관련 설정

  - 아래의 두 명령어를 주로 사용한다.
    - `nm`은 Network Manager의 약자다.
    - `nmtui`는 Network Manager Text User Interface의 약자다.

  ```bash
  $ nm-connection-editor
  $ nmtui
  ```

  - 위 명령으로 설정할 수 있는 것들은 다음과 같다.
    - 자동 IP 주소 또는 고정 IP 주소 사용 결정
    - IP 주소, 서브넷 마스크, 게이트웨이 정보 입력
    - DNS 정보 입력
    - 네트워크 카드 드라이버 설정
    - 네트워크 장치(ens32 또는 ens33) 설정



- 네트워크 설정 변경 사항 적용

  - 네트워크 설정을 변경한 후 변경된 내용을 시스템에 적용시키는 명령어이다.
    - 즉, `nm-connection-editor`, `nmtui`를 통해 네트워크 설정을 변경한 후에는 꼭 실행해야 하는 명령어이다.
  - 명령어
    - restart는 stop과 start가 합쳐진 것이다.
    - status 옵션은 작동 또는 정지 상태를 표시해준다.

  ```bash
  $ systemctl <start/stop/restart/status> networking
  ```



- IP 주소 관련 정보 출력

  - 해당 장치의 IP 주소와 관련된 정보를 출력한다.
  - 명령어

  ```bash
  $ ipconfig <장치 이름>
  ```



- DNS 서버의 작동을 테스트하는 명령어다.

  - 명령어

  ```bash
  $ nslookup
  ```



- 대상 컴퓨터가 네트워크 상에서 응답하는지 테스트하는 명령어

  - 대상 컴퓨터가 아무런 이상 없이 작동되는지를 네트워크상에서 체크할 때 사용한다.

  - 명령어

  ```bash
  $ ping <IP주소 또는 URL>
  ```





## 네트워크 설정과 관련된 주요 파일

- `/etc/netplan/*yaml`

  - 네트워크 기본 정보가 설정된 파일
    - 네트워크 정보가 모두 들어있다.
  - 에디터로 이 파일을 직접 편집해서 네트워크 정보를 수정할 수 있다.

  - 예시

  ```bash
  network:
  	ethernets:
  		ens33: # 네트워크 장치 이름
  			dhcp4: no #	자동 IP 사용 여부(no는 사용하지 않겠다는 의미이므로 고정 IP 방식을 사용한다)
  			addresses: [192.168.111.200/24]	# 고정 IP 주소와 넷마스크값을 지정(24는 255.255.255.0과 동일)
  			gateway4: 192.168.111.2		# 게이트웨이 장치의 주소
  			nameservers:	# DNS 서버의 주소
  				addresses: [192.168.111.2]	# DNS 서버의 IP 주소를 지정
  	version:2	
  ```

  



- `/etc/NetworkManager/system-connections/파일명`
  - X 윈도 모드에서 `nm-connection-editor` 또는 `nmtui` 명령어를 사용하면 위 디렉터리에 있는 파일이 수정된다.
  - 해당 파일을 에디터로 수정할 수도 있지만 `nm-connection-editor` 혹은 `nmtui` 명령어를 사용하는 것이 권장된다.



- `/etc/resolv.conf`
  - DNS 서버의 정보와 호스트 이름이 들어 있는 파일이다.
  - 임시로 사용되는 파일이며 네트워크가 재시작되면 다시 내용이 초기화된다.
  - 영구적으로 적용하려면 `/etc/netplan/*yaml` 파일을 편집해야 한다.



- `/etc/hosts`
  - 현 컴퓨터의 호스트 이름과 FQDN이 들어 있는 파일이다.



# Shell

- Shell

  - 사용자가 입력한 명령을 해석해 커널로 전달하거나 커널의 처리 결과를 사용자에게 전달하는 역할을 한다.

  - bash(Bourne Again Shell)
    - 우분투의 default 셸로, Bourne Shell(sh)을 기반으로 Korn Shell(ksh)과 C Shell(csh)의 장접을 합쳐 만든 것이다.
    - Alias, history(화살표로 이전 명령어 확인 가능), tab을 통한 자동 완성 기능 등을 제공한다.



- 환경변수

  - 셸은 여러가지 환경 변수 값을 갖는데, 설정된 환경 변수는 `echo $환경변수명` 명령어로 확인이 가능하다.
  - 주요 환경 변수

  | 환경변수 | 설명                        | 환경변수     | 설명                           |
  | -------- | --------------------------- | ------------ | ------------------------------ |
  | HOME     | 현재 사용자의 home 디렉터리 | PATH         | 실행 파일을 찾는 디렉터리 경로 |
  | LANG     | 기본 지원되는 언어          | PWD          | 사용자의 현재 작업 디렉터리    |
  | TERM     | 로그인 터미널 타입          | SHELL        | 로그인해서 사용하는 셸         |
  | USER     | 현재 사용자의 이름          | DISPLAY      | X 디스플레이 이름              |
  | COLUMNS  | 현재 터미널의 컬럼 수       | LINES        | 현재 터미널 라인 수            |
  | PS1      | 1차 명령 프롬프트 변수      | PS2          | 2차 명령 프롬프트              |
  | BASH     | bash 셸의 경로              | BASH_VERSION | bash 버전                      |
  | HISTFILE | 히스토리 파일의 경로        | HISTSIZE     | 히스토리 파일에 저장되는 개수  |
  | HOSTNAME | 호스트의 이름               | USERNAME     | 현재 사용자 이름               |
  | LOGNAME  | 로그인 이름                 | LS_COLORS    | ls 명령의 확장자 색상 옵션     |
  | MAIL     | 메일을 보관하는 경로        | OSTYPE       | 운영체제 타입                  |



- 셸 스크립트 프로그래밍

  - 리눅스의 shell 스크립트는 C 언어와 유사한 방법으로 프로그래밍할 수 있다.

    - 리눅스의 대부분이 C 언어로 작성됐기 때문이다.

    - 일반적인 프로그래밍 언어와 마찬가지로 변수, 반복문, 제어문 등을 사용할 수 있다.
    - 또한 별도로 컴파일하지 않고 텍스트 파일 형태로 셸에서 바로 실행할 수 있다.
  - 셸 스크립트 양식
    - `#!/bin/<shell>`은 어떠한 shell로 실행시킬지를 지정해주는 것이다.
    - linux 배포판의 경우 기본이 bash shell로 설정되어 있어, 입력하지 않으면 bash shell로 실행된다.
    - 셸 스크립트는 실행 중간에 문제가 생겨도 무조건 성공했다는 메시지를 반환하기에 마지막 행에서 직접 성공인지 실패인지를 반환하는 것이 좋다.
    - 0은 성공을 의미한다.

  
  ```bash
  # 특수한 주석으로, sh를 사용하겠다는 의미이다. 첫 행에 꼭 써줘야 한다.
  #!/bin/sh
  
  # 명령어를 써준다.
  echo "Hello World"
  
  # 종료 코드를 써준다.
  exit 0
  ```



- 셸 스크립트 실행 방법

  - sh 명령으로 실행
    - 셸 스크립트 파일의 속성을 변경할 필요가 없다는 장점이 있다.

  ```bash
  $ sh <실행할 shell script 파일>
  ```

  - 실행 가능 속성으로 변경 후 실행
    - 실행 가능 속성을 추가하면 `sh` 명령 없이도 실행이 가능하다.

  ```bash
  # 셸 스크립트 속성 변경
  $ chmod +x <변경할 shell script 파일>
  
  # 셸 스크립트 실행
  $ <실행할 shell script 파일>
  ```



- 변수

  - 변수의 기본
    - 변수를 사용하기 전에 미리 선언하지 않으며, 처음 변수에 값이 할당되면 자동으로 변수가 생성된다.
    - 변수에 넣는 모든 값은 문자열로 취급된다.
    - 변수명은 대소문자를 구분한다.
    - 변수를 할당할 때 `=` 좌우에는 공백이 없어야한다.
    - 값에 공백이 있을 경우 큰 따옴표로 묶어야 한다.
    - `$` 문자가 들어간 글자를 출력하려면 작은 따옴표로 묶거나 `\`를 붙여야 한다.

  - 예시

  ```bash
  # 변수 할당
  $ var=theo
  $ Var="Hello World!"
  $ echo $var		# theo
  $ echo $Var		# Hello World!
  
  
  # $가 포함된 문자 출력
  $ echo $USERNAME 	# theo
  $ echo '$USERNAME' 	# $USERNAME
  $ echo \$USERANME	# $USERNAME
  ```



- 숫자 계산

  - 변수에 넣은 값은 모두 문자열로 취급한다.
    - 변수에 들어 있는 값에 숫자 연산을 하려면 `expr` 키워드를 사용해야 한다.
    - `expr`키워드를 수식과 함께 \`로 묶어줘야 한다.
    - 모든 단어마다 띄어쓰기를 해줘야 한다.
    - 괄호와 `*`(곱하기 연산자) 앞에는 `\`를 붙여줘야 한다.
  - 예시

  ```bash
  num1=100
  num2=2
  num3=`expr $num1 + $num2`
  echo $num3	# 102
  num4=`expr \( $num1 + $num2 \) \* $num3`
  echo $num4	# 10404
  ```

  









# 사양

## Load Average

- Load 값의 평균을 나타낸 수치
  - Load
    - 일반적으로 부하라고 번역한다.
    - Linux에서 특정 작업이 처리되기를 기다리는 정도를 표현한 값이다.
  - 프로세스들 중 실행중(R) 혹은 대기(D) 상태에 있는 프로세스들의 개수의 평균이다.
    - Running(R): 프로세스가 실행되어 CPU 자원을 사용하고 있는 상태
    - Uniterruotible Sleep(D): 네트워크 요청을 보낸 후 응답을 기다리거나 I/O 작업 처리를 대기중인 상태로, 응답이 오면 다시 R로 돌아가게 되어 CPU를 사용하게 된다.
    - Sleeping(S): 동작이 중지된 상태로, 신호를 받을 때 까지 멈춰있게 된다. 응답이 오면 R 상태로 진입하는 D와 달리 언제든 신호를 받으면 R로 진입하게 된다.
    - Zombie(Z): 부모 프로세스가 죽은 자식 프로세스를 의미한다. CPU 및 메모리를 사용하지는 않으나 PID를 점유하고 있으므로 PID 고갈이 일어날 수 있다.



- 아래의 명령어들로 확인이 가능하다.

  - `uptime`
    - load average만을 보여준다.
    - 순서대로 1, 5, 15분의 평균값을 보여준다.

  ``` bash
  $ uptime
  ```

  - top
    - load average외에도 cpu 사용량, memory 사용량등을 보여준다.

  ```bash
  $ top
  ```

  - w
    - 사용자 정보도 함께 보여준다.

  ```bash
  $ w
  ```



- Load Average의 판단 기준
  - 같은 값이라도 CPU core의 개수에 따라 달라진다.
    - 만일 load aveage 값이 8이고, CPU core가 4개라면 실질적인 load average 값은 2라고 볼 수 있다.
    - 따라서 CPU의 `core 개수*1`이면 CPU 전체를 사용하고 있는 상황이라 볼 수 있다.
  - load average는 다리 위를 지나는 차와 같다.
    - 1.00은 다리가 차로 꽉 들어차 있다는 것을 의미한다. 이 경우 차량 통행에 문제는 없지만, 새로 건너려는 차가 조금이라도 늘어나면 통행에 문제가 생긴다.
    - 1.00이 넘는다면 다리가 차로 꽉 차 있을 뿐 아니라, 다리를 건너기 위해 대기중인 차도 있다는 의미이다.
    - 만일 core가 2개라면 다리가 2개라는 뜻이고 load average가 1이라면 두 다리 중 하나만 꽉 찬 상태라른 뜻이다(혹은 두 다리가 반반 씩 찼다는 뜻이다).
  - 일반적으로 상한 값을 70%(싱글 코어에서 0.70) 정도로 본다.



# 페이지 캐시와 버퍼 캐시

- 페이지 캐시
  - 리눅스는 파일 I/O의 성능 향상을 위해 페이지 캐시라는 메모리 영역을 만들어서 사용한다.
    - 한 번 읽은 파일의 내용을 페이지 캐시라는 영역에 저장시켜놨다가 다시 한 번 동일한 파일 접근이 일어나면 디스크에서 읽지 않고 페이지 캐시에서 읽어서 제공해주는 방식이다.
    - 이를 통해 디스크 접근을 줄일 수 있고 파일에  대한 빠른 접근을 가능하게 한다.
  - free 명령을 통해 확인이 가능하다.
    - free 명령을 사용하여 cahed 영역을 확인하고, cat 명령어를 통해 10kb파일을 읽은 뒤 다시 free 명령을 실행하면, cached 영역이 10kb 정도 증가한 것을 확인 가능하다.



- 버퍼 캐시
  - 블록 디바이스가 가지고 있는 불록 자체에 대한 캐시이다.
    - 커널이 데이터를 읽기 위해서는 블록 디바이스의 특정 블록에 요청을 해야 한다.
    - 이 때 해당 블록에 대한 내용을 버퍼 캐시에 담아두고, 동일한 블록에 접근할 경우에는 블록 디바이스까지 요청을 하지 않고 버퍼 캐시에서 바로 읽어서 보여준다.
  - 즉, 버퍼 캐시는 파일 시스템의 메타 데이터와 관련된 블록들을 저장하고 있는 캐시이다.





# -dev 패키지

- 리눅스에서 `-dev`(Ubuntu와 같은 데비안 계열) 혹은 `--develop`CentOS와 같은 레드햇 계열 패키지는 컴파일을 위한 헤더 및 라이브러리 페이지이다.
  - 주요 역할은 다른 프로그램들을 위한 라이브러리 역할과 소스파일 컴파일이다.
    - 예를 들어 Python 실행을 위해서는 `openssl-devel`이라는 패키지가 필요하다.
  - 일반적으로 `.h`, `.so`, `.a` 확장자를 가진 파일로 구성되어 있다.
    - `.h`: 헤더 파일로 소스코드 파일
    - `.so`: 동적 라이브러리로 shared object의 약자, 윈도우의 DLL과 같은 역할을 한다.
    - `.a`: 정작 라이브러리로, archive library를 의미. 







# systemd

> centos:7 기준

- systemd
  - Linux의 init system이자 system 관리를 위한 software이다.
    - Init system의 주요 목적은 Linux kernel이 booting되고 나서 반드시 시작되어야 하는 component들을 실행시키는 것이다.
    - 본래 Linux 계열 OS에서는 init이라는 process가 pid 1번으로 실행되어 정해진 service 및 script들을 실행했다.
    - 그러나 이제는 이러한 작업을 systemd가 실행하도록 변경되었다.
  - Unit
    - systemd가 관리하는 resource를 unit이라 부른다.
    - Unit은 resource의 종류에 따라 분류되고, unit file이라 불리는 file로 정의할 수 있다.
    - 각 unit file의 suffix로 해당 file이 어떤 unit에 관해 정의한 것인지를 추론할 수 있다.
    - 예를 들어 service를 관리한다면, unit은 service가 되고, 해당 unit의 unit file은 `.service`라는 suffix가 붙게 된다.
  - Unit file
    - Unit을 정의하기 위해 작성하는 file이다.
    - `/etc/systemd/system`이나 `/usr/lib/systemd/system`에 작성한다.
    - 두 directory의 차이는, `/usr/lib/systemd/system`의 경우 package관리자(apt, rpm 등)에 의해 설치된 unit들이 위치하는 directory고,  `/etc/systemd/system`는 package 형태가 아닌 unit들이 저장되는 directory라는 것이다.
    - 작성 방식은 [링크](https://www.freedesktop.org/software/systemd/man/systemd.service.html) 참고
  - systemctl
    - systemd를 위한 CLI이다.



- 시스템 등록하기

  - 실행할 스크립트를 작성한다.
    - shebang(`#!/bin/bash`)을 반드시 넣어줘야한다.

  ```bash
  #!/bin/bash
  
  echo -e " Start Systemd Test " | logger -t Testsystemd
  
  while :
  do
  	echo -e "Running systemd"
  	sleep 30
  done
  ```

  - 시스템에 등록한다.
    - `/usr/lib/systemd/system` 디렉터리로 이동한다.
    - `service명.service`라는 파일을 아래와 같이 작성한다.
    - `Restart` 설정시 주의할 점은, 이는 service가 실행 중에 종료될 시 재실행할지를 설정하는 옵션이지, OS자체 reboot 될 경우 service를 재실행할지를 설정하는 옵션이 아니라는 점이다.

  ```bash
  [Unit]
  Description=Systemd Test
  
  [Service]
  Type=simple
  ExecStart=/home/theo/hello.sh	# 위에서 작성한 shell script 파일 경로
  Restart=on-failure
  
  [Install]
  WantedBy=multi-user.target
  ```




- systemctl

  - systemctl 명령어 사용시 서비스명을 입력할 때 뒤에 `.service`라는 suffix는 붙여도 되고 붙이지 않아도 된다.
    - Suffix를 붙이지 않아도 systemd가 알아서 어떤 종류의 unit인지를 판단한다.
  - 아래 명령어로 등록 된 서비스들을 확인 가능하다.

  ```bash
  $ systemctl list-units --type=service
  
  # 또는
  $ systemctl list-unit-files
  ```

  - `.service` 파일을 수정했을 경우 아래 명령어로 변경 사항을 적용한다.
    - 이 명령어를 실행한다고 실행중인 service가 정지되진 않는다.
    - unit file을 수정하거나 unit file을 새로 생성하거나 삭제했을 경우, 아래 명령어를 실행해야 변경사항이 systemd에 반영된다.
  
  ```bash
  $ systemctl daemon-reload
  ```
  
  - reload
    - Service와 관련된 설정 file들을 reload한다.
    - 이는 unit file(`.service` file)을 reload하는 것이 아니라는 것에 주의해야한다.
    - 예를 들어 `systemctl reload apache`라는 명령어는 `apache.service` file을 reload하는 것이 아니라 `httpd.conf` 같은 apache에서 사용하는 configuration file을 reload한다.
  
  ```bash
  $ systemctl reload <서비스명>
  ```
  
  - 등록된 service 실행 또는 정지
  
  ```bash
  $ systemctl start | stop <서비스명>
  ```
  
  - 등록된 service 재실행
  
  ```bash
  $ systemctl restart <서비스명>
  ```
  
  - Service 상태 확인
  
  ```bash
  $ systemctl status <서비스명>
  ```
  
  - 부팅시에 자동으로 실행되도록 설정
    - 이 명령어를 실행시 `/etc/systemd/system`에 symbolic link를 생성한다.
    - 이 경로는 booting시에 systemd가 자동으로 시작시킬 file들을 찾는 위치이다.
  
  ```bash
  $ systemctl enable <서비스명>
  ```
  
  - 부팅시에 자동으로 실행되지 않도록 설정
    - 이 명령어를 실행시 `/etc/systemd/system`에 생성된 symbolic link를 제거한다.
  
  ```bash
  $ systemctl disable <서비스명>
  ```
  
  - 부팅시 자동으로 실행되도록 설정되어 있는지 확인
  
  ```bash
  $ systemctl is-enabled <서비스명>
  ```



- 옵션들

  > Unit, Service, Install로 나뉘며 아래 옵션들 외에도 많은 옵션이 존재한다.

  - Description

    - 해당 유닛에 대한 설명
  - Type
    - 유닛 타입을 선언한다.

    - simple: 기본값으로, 유닛이 시작된 즉시 systemd는 유닛의 시작이 완료됐다고 판단한다.
    - forking: 자식 프로세스 생성이 완료되는 단계까지를 systemd가 시작이 완료됐다고 판단한다.

  - ExecStart
    - 시작 명령을 정의한다.
  - ExecStop
    - 중지 명령을 정의한다.
    - WorkingDirectory: 해당 동작을 수행할 Directory를 지정한다.




- 실행이 안 될 경우
  - status 203이 뜨면서 실행이 안 될 경우 원인은 아래와 같다.
    - shebang을 추가하지 않은 경우.
    - 실행 파일 경로가 잘못된 경우.
    - 실행 파일에 실행 권한이 없을 경우.



- root 사용자가 아닌 사용자로 실행하려고 할 경우

  - `systemctl`은 기본적으로 root 권한이 있어야한다.
  - 만일 root 유저가 아닌 다른 사용자로 실행하고자 한다면 아래와 같이 `/etc/sudoers`에 추가해줘야한다.
    - `ALL=NOPASSWD`는 매번 아래 명령어들을 입력할 때마다 비밀번호를 입력하지 않아도 실행되도록 해준다.
    - 실행할 명령어를 `,`로 구분하여 나열해준다.

  ```bash
  <사용자명> ALL=NOPASSWD:/bin/systemctl start <service 명>, /bin/systemctl stop <service 명>, /bin/systemctl status <service 명>, /bin/systemctl restart <service 명>
  ```

  - 등록이 완료된 후에는 sudo를 붙여서 명령어를 실행하면 된다.
  - 또한 `/usr/lib/systemd/system` 내부의 파일들을 root 권한이 있어야 수정이 가능하므로 아래와 같이 root 이외의 사용자에게 읽고 쓰는 권한을 준다.

  ```bash
  setfacl -m u:<사용자명>:rw <service 파일 경로>
  ```



- journald

  - systemd의 log를 확인할 수 있게 해주는 daemon.
  - `/etc/systemd/journald.conf`를 수정하여 설정을 변경할 수 있다.
  - journalctl
    - systemd 로그를 보여주는 유틸리티이다.
    - 아무 옵션 없이 입력할 경우 모든 systemd의 log를 보여준다.

  ```bash
  $ journalctl
  ```

  - `--since`
    - 특정 시간 이후의 항목을 볼 수 있다.

  ```bash
  $ journalctl --since "2023-09-15 08:15:00"
  $ journalctl --since today
  $ journalctl --since yesterday
  ```

  - `-n`
    - 최근 n개의 log를 볼 수 있다.

  ```bash
  $ journalctl -n 20
  ```

  - `-u`
    - 특정 service의 log를 볼수 있다.

  ```bash
  $ journalctl -u docker.service
  ```

  - `-f`
    - Log를 실시간으로 볼 수 있다.

  ```bash
  $ journalctl -f
  ```

  - `-b`
    - 현재 부팅이후의 log 만을 보여준다.
    - 만일 이전 booting을 보려면 뒤에 음의 정수를 입력하면 된다.

  ```bash
  $ journalctl -b
  ```

  - `--no-pager`
    - Terminal의 너비가 짧을 경우 terminal의 너비를 넘어가는 log는 짤리게 되는데, 이 옵션을 줄 경우 개행을 해서 전부 보여준다.

  ```bash
  $ journalctl --no-pager
  ```

  

# umask

- Linux umask

  - 새로 생성되는 파일이나 directory의 권한을 제어하는 명령어.
    - root뿐 아니라 일반 사용자도 제어할 수 있다.
    - 이 값은 계정마다 별도로 적용된다.
  - 계산 방식은 아래와 같다.
    - 기본적으로 umask가 적용되지 않았을 때, file은 0666, directory는 0777권한으로 생성된다.
    - umask 값은 위 기본 권한에서 적용하고자 하는 값을 얻기 위해 빼야 하는 수를 입력하면 된다.
    - 예를 들어 directory의 기본 권한을 755로 설정하고자 한다면 umask 값을 0022로 설정하여, directory의 기본 권한 `0777`에서 umask 값`0022`를 빼면 `0777-0022=0755`가 되어 directory의 기본 권한을 0755로 설정할 수 있다.
    - File의 경우 file의 기본 권한 `0666`에서 umask 값 `0022`를 빼면 `0666-0022=0644`가 되어 file의 기본 권한은 0644가 된다.
  - umask 값 확인하기
    - 일반적으로 0002가 기본값으로 설정되어 있으며, 이 경우 directory는 775, file은 664로 권한이 설정된다.

  ```bash
  $ umask
  ```

  - 권한을 상세하게 확인하기

  ```bash
  $ umask -S
  ```

  - 임시로 umask 설정하기
    - 아래 방법은 임시로 설정하는 방식으로, 명령어를 실행한 셸이 종료되면 초기화된다.

  ```bash
  $ umask <mask>
  
  # e.g.
  $ mask 0002
  ```

  - 영구 적용하기
    - `.bashrc` 혹은 `.bash_profile`을 수정한다.

  ```bash
  $ vi ~/.bashrc
  
  # 아래와 같이 추가한다.
  umask 0002
  ```



- 모든 사용자에게 적용하기(ubuntu 기준)

  - `/etc/login.defs`에서 기본 umask를 설정할 수 있다.

  ```bash
  # If USERGROUPS_ENAB is set to "yes", that will modify this UMASK default value
  # for private user groups, i. e. the uid is the same as gid, and username is
  # the same as the primary group name: for these, the user permissions will be
  # used as group permissions, e. g. 022 will become 002.
  
  # ...
  
  UMASK           022
  
  # ...
  
  USERGROUPS_ENAB yes
  ```

  - `USERGROUPS_ENAB`
    - 만약 yes로 설정되어 있으면, `userdel`을 통해 user를 삭제할 때, 해당 user가 속해 있던 group에 더 이상 user가 남아있지 않으면 해당 group도 삭제한다.
    - 또한 `useradd`를 통해 user를 생성할 때 user name과 같은 이름으로 group을 생성한다.

  - 위 설명에 나와 있듯이 `USERGROUPS_ENAB`값이 `yes`로 설정되어 있을 경우 기본 값이 group permission에 맞춰지게 된다.
    - 즉 uid가 gid와 같고 username이 group name과 같으면 user permission을 group permission으로 사용하게 된다.
    - 예를 들어, 기본 umask가 022일 때, directory의 permission은 755가 된다. 그런데 이 때 `USERGROUPS_ENAB`값이 `yes`로 설정되어 있고, 어떤 user의 uid와 gid가 같고, user name과 group name이 같으면 user permission인 7을 group permision으로 사용하게 되므로 directory의 permission은 775가 되고, 이는 umask가 002인 것과 동일하다. 
    - 당연히 file에도 마찬가지로 적용된다.





# Shorts

- GPG(GNU Privacy Guard)
  - RFC(Request for Comments)4880(PGP라고도 불린다)에서 정의된 OpenPGP 표준의 구현체이다.
  - 공개 키 암호화 방식을 사용하여, 개인 간, machine 간 교환되는 메시지나 파일을 암호화하거나 서명을 추가하여 작성자를 확인하고 변조 유무를 식별하는 데 사용한다.



- `/etc/apt/sources.list`
  - ubuntu, debian에서 사용하는 apt(advanced package tool)가 패키지를 가져 올 소스 저장소(repository)를 지정하는 파일이다.
  - 파일 내부에는 아래와 같은 정보가 작성된다.
    - `deb`: 이미 컴파일된 바이너리 패키지
    - `deb-src`: 소스 상태의 오리지널 프로그램과 데비안 컨트롤 파일
  - `/etc/apt/sources.list.d` 
    - 패키지별로 보다 편하게 관리하기 위해서, 패키지별로 `sources.list` 파일을 작성한 것을 모아놓은 디렉터리이다.
    - 확장자는 `.list` 또는 `.sources`를 사용한다.



- FUSE(Filesystem in Userspace)
  - Unix 계열 OS에서 root 권한이 없는 사용자들이 kernel 코드를 수정하지 않고도, 자신들만의 파일 시스템을 만들 수 있게 해주는 프로그램이다.
    - Linux, macOS, Windows 등에서 모두 사용이 가능하다.
    - Linux kernel 2.6.15부터는 기본적으로 탑재되어 있다.
  - 아래 세 가지로 구성된다
    - kernerl module인 fuse.ko
    - Userspace library인 libfuse.*
    - Mount utility인 fusermount



- 대상 서버의 포트가 열려 있는지 확인하는 방법

  > https://meetup.nhncloud.com/posts/204

  - telnet
    - 연결이 되면, `Ctrl + ]`를 입력하고 `quit`을 입력하면 해제가 가능하다.
    - 요즘은 telnet이 기본적으로 설치되어 있지 않은 경우가 많다.

  ```bash
  $ telnet <IP> <PORT>
  ```

  - bash의 built-in 기능 사용하기
    - 포트가 열려있는 경우라면 아무 메시지가 나오지 않은 상태로 끝난다.
    - 포트가 열려있지 않은 경우에는 에러 메시지가 출력된다.

  ```bash
  $ echo > /dev/tcp/<IP>/<PORT>
  ```



- whereis

  - 명령어의 실행파일 위치, 소스 위치 등을 찾아주는 명령어이다.

  ```bash
  $ whereis <명령어>
  ```

  - `which`로 나오지 않더라도 whereis로 나오는 경우가 있을 수 있다.



# etc

> 추후 필요할 때 공부 할 것들의 목록



- 응급복구

  > p.260~

  - root 계정의 비밀번호를 잊어버렸을 때 사용할 수 있는 방법



- GRUB

  > p.263

  - 우분투를 부팅할 때 처음 나오는 선택화면



- 커널 업그레이드

  > p.268

  - 커널 컴파일과 업그레이드



- X 윈도

  > p.283



- 하드디스크 관리

  > p.335

  - 하드디스크, 파티션, 사용자별 공간 할당
