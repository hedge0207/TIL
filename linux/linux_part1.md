# 리눅스 개요

- 리눅스의 탄생
  - 유닉스라는 운영체제는 리눅스가 탄생하기 이전부터 널리 사용되었다.
    - 현재까지도 가장 많이 사용되는 운영체제 중 하나이다.
    - 유닉스는 상용 소프트웨어로 발전됐고, 현재는 무척 비싼 비용을 지불해야 사용이 가능하다.
    - 여러 회사에서 제작/판매 중이며 IBM의 AIX, HP의 HP-UX, 오라클의 Solaris, DEC의 Tru64 Unix, Xinuos의 OpenServer 등이 많이 사용된다.
    - 리눅스는 무료 유닉스라고 생각할 수 있다.
  - 1991년 8월 리누스 토르발스는 어셈블리어로 리눅스 커널 0.01 버전을 처음 작성했다.
    - 그 당시 리누스 토르발스의 목표는 유닉스 시스템의 작은 버전인 미닉스보다 좋은 운영체제를 만드는 것이었다.
  - 이후 1992년에 0.02 버전을 작성하면서 인터넷에 소스코드를 공개했는데, 이것이 리눅스의 탄생이었다.
    - 실제로 리누스 토르발스는 커널이라고 부르는 리눅스의 핵심 부분만 작성해서 배포했다.
    - 현재의 리눅스는 여러 사람의 기여로 완성된 것이다.
  - 일반적으로 사람들이 이야기하는 리눅스는 리누스 토발스가 만든 커널에 컴파일러 쉘, 기타 응용 프로그램들이 조합된 배포판을 가리킨다.
    - 이러한 배포판은 여러 가지 응용 프로그램을 조합해 많은 리눅스 단체 또는 회사가 자신의 이름을 붙여서 판매/배포한다.
    - 우분투도 그 중 하나다.



- GNU 프로젝트
  - 토발즈가 리툭스 커널을 개발하기 전인 1984년, 리처드 스톨먼에 의해 GNU 프로젝트가 시작되었다.
    - GNU 프로젝트의 목표는 모두가 공유할 수 있는 소프트웨어를 만드넌 것이었다.
    - 리처드 스톨먼은 1985년 자유 소프트웨어 재단(Free Software Foundation, FSF)을 설립했다.
    - FSF는 GNU 프로젝트에서 제작한 소프트웨어를 지원함으로써 컴퓨터 프로그램의 복제, 변경, 소스코드  사용에 걸린 제한을 철폐하는 것을 목표로 삼았다.
  - FSF에서 제공하는 대부분의 소프트웨어는 GPL(General Public License)라는 라이선스를 따르도록 되어 있다.
    - 이 라이선스는 자유 소프트웨어의 수정과 공유에 있어서 기본적으로 자유를 보장한다.
    - 모든 소스코드가 완전히 공개되어 있는 자유 소프트웨어는 프리웨어라는 개념을 뛰어 넘어 다음과 같은 진정한 자유에 대한 개념을 내포하고 있다.
    - 소프트웨어 사용, 수정, 재배포에 대한 자유 및 수정된 소프트웨어의 이익을 전체가 얻을 수 있도록 배포할 수 있는 자유.



- 커널
  - 커널에는 아래와 같은 코드들이 포함되어 있다.
    - 현재 제어하는 하드웨어 장치의 지원 여부 정보
    - 하드웨어 성능
    - 하드웨어 제어
  - 리누스 토발즈는 이 커널이라고 부르는 리눅스의 핵심을 개발했고 지금도 계속 업그레이드 중이다.
    - 리눅스 커널 아카이브에서 항상 최신 버전의 리눅스 커널을 다운로드 할 수 있다.
  - 배포되는 리눅스 커널의 버전은 안정 버전과 개발 버전으로 나뉜다.
    - 안정 버전: 이미 검증된 개발 완료 코드로 구성.
    - 개발 버전: 현재 개발 중인 코드.
  - 리눅스의 가장 큰 특징 중 하나는 배포판(우분투 등)에 포함된 기본 커늘을 사용자가 직접 최신 커널로 업그레이드 할 수 있다는 점이다.
    - 이를 커널 업그레이드 혹은 커널 컴파일이라 부른다.



- 우분투 리눅스 배포판

  - 배포판

    - 일반 사용자의 경우 리눅스 커널만으로는 리눅스를 사용할 수 없다.
    - 때문에 여러 회사나 단체에서 리눅스 커널에 다양한 응용프로그램을 추가해 쉽게 설치 및 사용할 수 있도록 만든 것이 리눅스 배포판이다.
    - 배포판의 종류는 수십가지가 넘으며 우리나라에서 주로 사용하는 배포판도 10여 가지나 된다.

  - 데비안 리눅스

    - 데비안 리눅스는 이안 머독이 1993년 시작한 데비안 프로젝트에서 탄생했다.
    - 데비안 리눅스의 정시 버전은 1996년 1.1 버전(코드명 Buzz)으로 출시되었다.
    - 데비안의 코드명은 토이스토리에 나오는 캐릭터들의 이름으로 붙여졌다.
    - 데비안의 가장 큰 특징 중 하나는 패키지 설치 및 업그레이드가 상당히 단순하며 apt 프로그램을 통해 소프트웨어 설치나 업데이트 등이 자동으로 이루어진다는 것이다.

  - 우분투 리눅스

    - 데비안 리눅스를 기초로 그놈(GNOME) 데스크톱 환경을 사용하는 리눅스 배포판이다.
    - 캐노니컬사에서 개발하기 시작했으며 현재는 캐노니컬사의 지원을 받으며 우분투 재단에서 개발을 진행하고 있다.
    - 2004년 10월 4.10버전을 처음으로 출시했으며, 현재 가장 인기 있는 리눅스 배포판 중 하나가 되었다.
    - 우분투는 남아프리카 어느 부족의 언어로 '네가 있으니 나도 있다'라는 뜻으로, 로고 역시 이를 반영하여 여러 사람이 손을 마주잡고 빙 둘러 서 있는 모양이다.
    - 우분투의 버전은 팔표한 연도와 월로 짓는다. 예를 들어 20.04는 20년 4월에 발표한 버전이다.
    - 지원 기간이 9개월 정도로 짧은 일반 버전과 5년 정도로 긴 LTS(Long Term Support) 버전으로 나눠서 발표하는데 업무용으로는 LTS 버전이 바람직하다.




# 가상머신 준비하기

- 가상 머신 사양

  |               | Server_A                             | Server_B               | Client          | WinClient                |
  | ------------- | ------------------------------------ | ---------------------- | --------------- | ------------------------ |
  | 주 용도       | 서버 전용                            | 서버 전용(텍스트 모드) | 클라이언트 전용 | Windows 클라이언트 전용  |
  | OS            | Ubuntu 64-bit                        | 동일                   | 동일            | Windows 10               |
  | 설치할 ISO    | Ubuntu Desktop 20.04                 | Ubuntu Server 20.04    | Kubuntu 20.04   | Windows 10 평가판(32bit) |
  | 하드 용량     | 20GB                                 | 동일                   | 동일            | 60GB                     |
  | 하드 타입     | SCSI                                 | 동일                   | SCSI 또는 SATA  | 동일                     |
  | 메모리 할당   | 2GB(2048MB)                          | 동일                   | 동일            | 1GB                      |
  | 네트워크 타입 | Use network address translation(NAT) | 동일                   | 동일            | 동일                     |
  | CD/DVD        | O                                    | O                      | O               | O                        |
  | Floppy 장치   | X                                    | X                      | O               | X                        |
  | Audio 장치    | X                                    | X                      | O               | X                        |
  | USB 장치      | X                                    | X                      | O               | X                        |
  | Printer       | X                                    | X                      | O               | X                        |




- 가상 머신 생성

  > https://github.com/hedge0207/TIL/blob/master/etc/virtual_machine.md 

  - 위 markdown을 참고하여 가상 머신 및 필요한 운영체제를 설치한다.



# 리눅스 기본 개념

- 리눅스의 특징
  - 대소문자를 구분한다.
  - 일반 사용자는 프롬프트에 `#`으로 표시가 되며, root 사용자는 `$`으로 표시가 된다.



- 디스크 파티션과 크기

  - 리눅스 파티션은 루트 파티션이라 부르는 `/` 파티션과 swap 파티션 2개만 있어도 운영이 가능하다.
  - 일반적인 용도로는 다음과 같이 나눌 수 있다.
    - `/` 파티션과 swap 파티션 2개만 있어도 운영이 가능하다고 한 이유는 바로 아래에서 확인 가능하듯 나머지 파티션(/bin, /sbin, /home)이 루트 파티션(/)에 종속되기 때문이다.

  | 마운트 포인트 | 비고                                                         |
  | ------------- | ------------------------------------------------------------ |
  | /             | 루트 파티션                                                  |
  | /bin          | 기본 명령어가 저장된 곳                                      |
  | /sbin         | 시스템 관리용 명령어가 저장 된 곳                            |
  | /etc          | 시스템 환경 설정과 관련되 파일이 저장 된 곳                  |
  | /boot         | 부팅 커널이 저장 된 곳                                       |
  | /media        | 외부 장치를 마운트하기 위한 곳                               |
  | /usr          | 응용 프로그램이 주로 저장 됨                                 |
  | /lib          | 프로그램의 라이브러리가 저장됨                               |
  | /dev          | 장치 파일들이 저장됨                                         |
  | /proc         | 시스템의 프로세서 정보, 프로그램 정보, 하드웨어 정보 등이 저장 됨 |
  | /tmp          | 임시 파일들이 저장됨                                         |
  | /var          | 로그, 캐시 파일 등이 저장됨                                  |
  | /root         | 시스템 관리자인 root의 홈 디렉토리                           |
  | /home         | 사용자별 공간                                                |
  | /lost+found   | 파일 시스템 복구를 위한 디렉토리                             |
  | swap 파티션   | RAM 부족시 사용되는 공간                                     |




- X 윈도(X Window)
  - MS의 Windows와 같은 GUI를 리눅스에 제공한다.
  - Windows의 경우 그래픽 모드가 없으면 운영이 거의 불가능하지만 리눅스의 X 윈도는 하나의 편리한 유틸리티일 뿐이지 반드시 필요한 것은 아니다.



- 종료와 로그아웃

  - 아래 명령어들로 종료가 가능하다.
    - `-P` 또는 `-p` 옵션은 시스템 종료를 의미한다.

  ```bash
  $ poweroff
  $ shutdown -P now
  $ halt -p
  $ init 0
  ```

  - shutdown 상세
    - `shutdown`의 `now` 부분에 시간을 지정하면 지정한 시간에 시스템을 종료한다.

  ```bash
  $ shutdown -P +10	# 10분 후 종료
  $ shutdown -r 22:00 # 22시에 재부팅
  $ shutdown -c 		# 예약된 shutdown 취소
  $ shutdown -k +15	# 현재 접속한 사용자에게 15분 후 종료된다는 메시지를 보내지만 실제로 종료되지는 않음
  ```

  - 로그아웃
    - 로그아웃은 시스템 종료와 의미가 다르다.
    - 리눅스는 여러 사용자가 동시에 접속해서 사용하는 다중 사용자(Multi-User) 시스템이므로 자신만의 접속을 끝내는 로그아웃이 필요하다.
  
  ```bash
  # 아래 명령어로 로그아웃이 가능하다.
  $ logout
  $ exit
  ```



- 리부팅

  - 아래 명령어를 통해 리부팅이 가능하다.
  - init은 종료에도 쓰이고 리부팅에도 쓰이는데 init 뒤에 붙는 숫자는 아래의 런레벨에 관한 설명을 참고하면 된다.

  ```bash
  $ reboot
  $ init 6
  ```



- 가상 콘솔
  - 가상 콘솔이란 가상의 모니터라고 생각하면 이해하기 쉽다.
    - 우분투는 총 6개(2~7번)의 가상 콘솔을 제공한다.
    - 각각의 가상 콘솔로 이동하는 단축키는 `ctrl+alt+F2~F7`이다.
    - 위 단축키를 통해 이동하면 화면 최상단에 `tty<숫자>`와 같은 메시지가 출력되는데 숫자에 해당하는 콘솔이라는 가상 콘솔이라는 뜻이다.
  - 가상 콘솔을 활용하여 `shutdown` 명령어를 입력했을 때 다른 사용자에게 무슨일이 발생하는지 확인해본다.
    - `ctrl+alt+F3`을 입력하여 3번 콘솔로 이동 후 root 사용자로 로그인한다.
    - `ctrl+alt+F4`를 입력하여 4번 콘솔로 이동 후 일반 사용자로 로그인한다.
    - 다시 3번 콘솔로 이동 후 `shutdown -h +5`를 입력하여 5분 후에 종료하겠다는 명령을 날린다.
    - 4번 콘솔로 이동하면 `The system is going to down for poweroff at <날짜 및 시간>`이라는 메시지가 출력된 것을 확인 가능한데, 이 상태에서 `enter`를 누르면 다시 사용이 가능하지만 위 메시지는 매 분 뜨게 된다.
    - 다시 3번 콘솔로 이동하여 `shutdown -c`를 입력해 예약한 종료를 취소한다.
    - 다시 4번 콘솔로 이동하여 확인해보면 `The system shutdown has been cancelled`라는 메시지가 뜬 것을 확인 가능하다.
    - 3번, 4번 콘솔에서 모두 logout 한 뒤 2번 콘솔로 돌아간다.



- 런 레벨

  - 리눅스 시스템이 가동되는 방법을 7가지 런레벨로 나눌 수 있다.
  - init 명령어 뒤에 붙는 숫자가 바로 런레벨로, init은 런 레벨을 변경하는 명령어이다.
  - 일반적으로 런 레벨 3번을 Multi-User 모드로 사용한다.
    - 2번과 4번은 우분투에서 사용하지 않지만 다른 리눅스 기반 OS와의 호환성을 위해 런 레벨 3번과 동일한 것으로 취급한다.

  | 런레벨 | 영문 모드  | 설명                      | 비고                  |
  | ------ | ---------- | ------------------------- | --------------------- |
  | 0      | Power Off  | 종료 모드                 |                       |
  | 1      | Rescue     | 시스템 복구 모드          | 단일 사용 모드        |
  | 2      | Multi-User |                           | 사용하지 않음         |
  | 3      | Multi-User | 텍스트 모드의 다중 사용자 |                       |
  | 4      | Multi-User |                           | 사용하지 않음         |
  | 5      | Graphical  | 그래픽 모드의 다중 사용자 | X 윈도 사용시 지정 됨 |
  | 6      | Reboot     |                           |                       |

  - 런 레벨 모드 확인
    - `/lib/systemd/system` 디렉터리의 `runlevel?.target` 파일을 확인한다.
    - 7개의 `runlevel?.target` 파일을 확인 가능한데 `runlevel?.target` 파일은 모두 링크 파일이다.
    - 각각의 링크 파일은 실제 파일과 연결되어 있다.
    - 예를 들어 `runlevle0.target` 파일은 `poweroff.target` 파일을 가리킨다.
  
  ```bash
  $ cd /lib/systemd/system
  $ ls -l runlevle?.target
  ```
  
  - 현재 설정된 런 레벨 확인하기
    - `default.traget`과 링크 되어 있는 파일을 확인하면 런레벨을 확인 가능하다.
    - X 윈도를 사용할 경우 아래와 같이 `graphical.target`(런 레벨 5)로 설정되어 있다.
  
  ```bash
  $ ls -l /lib/systemd/system/default.target
  lrwxrwxrwx 1 root root 16 11월 13 13:46 default.target -> graphical.target
  ```
  
  - 런 레벨 변경하기
    - `default.target`에 링크 된 파일을 `multi-user.target`으로 변경하여 런 레벨 3번으로 변경할 수 있다.
    - 이후 재부팅하면 텍스트 모드로 실행된다.
    - `startx`를 통해 X 윈도로 다시 진입 가능하다.
  
  ```bash
  $ cd /lib/systemd/system
  # 링크 파일 변경
  $ ln -sf multi-user.target default-target
  # 변경 확인
  $ ls -l default.target
  ```
  
  - 다시 런 레벨 5로 변경하기
    - 이후 재부팅하면 X 윈도로 실행된다.
  
  ```bash
  $ cd /lib/systemd/system
  # 링크 파일 변경
  $ ln -sf graphical.target default-target
  # 변경 확인
  $ ls -l default.target
  ```



- 자동완성과 히스토리

  - 리눅스는 `tab`키를 사용하여 파일 이름 또는 폴더 이름 등을 자동으로 완성하는 기능을 제공한다.
    - 자동 완성 후보가 2개 이상일 경우 `tab` 키를 두 번 누르면 후보들을 보여준다. 
  - 도스 키(Dos Key)란 이전에 입력한 명령을 키보드의 `↑`, `↓` 키를 활용하여 다시 사용할 수 있게 하는 것을 말한다.

  - `history` 명령을 통해 기존에 사용했던 모든 명령을 볼 수 있다.
    - `-c` 옵션을 통해 저장된 모든 명령어를 삭제할 수 있다.

  ```bash
  $ history [옵션]
  ```

  - 리눅스는 대소문자를 구분하며, 파일, 폴더 이름 등에 공백이 존재할 경우 이를 쌍따옴표로 묶어줘야한다.



- manual

  - 아래 명령어를 통해서 linux 명령어들의 설명을 볼 수 있다.

  ```bash
  $ man <설명을 보려는 명령어>
  ```

  - 명령어
    - 상, 하 이동은 화살표를 사용하거나 `k`/`j`키를 사용한다.
    - 페이지 단위의 이동은 `page up`/`down` 혹은 `spacebar`/`b`키를 사용한다.
    - `/찾으려는 단어`를 통해서 특정 단어를 찾는 것도 가능하며 `n`키를 통해 다음 단어로 넘어갈 수 있다.
    - `q`키로 종료한다.
  - `--help` 옵션을 통해서도 확인이 가능하다.

  ```bash
  $ <명령어> --help
  ```



- 숨김파일 및 현재 디렉터리
  - 리눅스는 파일 혹은 디렉터리 이름의 가장 첫 글자로 `.`을 넣으면 숨김 파일이 된다.
    - 리눅스에는 숨김 파일이라는 속성이 별도로 존재하지 않는다.
    - 이름 앞에 `.`만 붙여주면 된다.
  - 현재 디렉터리
    - 현재 디렉터리란 현재 위치한 디렉터리를 의미한다.



- 리눅스에서는 directory로 file이다.
  - directory 역시 다른 파일들을 담고 있는 file로 본다.
  - directory뿐 아니라 device(마우스, 키보드 등)도 파일이다.
  - 정확히는 여러 type의 파일이 존재하며, directory type의 파일, device type의 파일이 있는 것이다.



## 리눅스 에디터

- 리눅스 에디터

  - 리눅스에는 다양한 종류의 에디터가 존재한다.
    - gedit: window의 text와 유사하며, GUI에서만 사용이 가능하다.
    - nano: text 모드에서 사용할 수 있는 에디터이다.
    - vi: 모든 리눅스, 유닉스 계열에 존재하는 에디터로 우분투는 기존의 vi를 더 발전시킨 vim(Vi IMproved) 에디터를 사용한다.
  - nano
    - `-c` 옵션을 주면 하단에 커서의 위치 정보를 보여준다.
    - 파일명은 명령어를 실행할 때 입력해도 되고 안해도 되는데, 안 할 경우 종료할 때 파일명을 입력 가능하다.
    - `ctrl` + `X`로 종료가 가능하며 종료할 때 `Y`, `N`으로 저장 여부를 결정 가능하다.

  ```bash
  $ nano [옵션] [파일명]
  ```



- vi

  - vi 에디터 실행

  ```bash
  $ vi [파일명]
  ```

  - 기본 명령어

    - `esc`를 누른 후 `:q`를 입력하여 종료가 가능하다(변경 사항이 있을 경우 종료가 불가능한데 이 때는 `:q!`를 입력하면 된다).
    - `:wq`는 저장 후 종료하는 것이다.
  - `:set number`를 입력하면 매 행 숫자가 표시된다.
    - `:set nonumber`를 입력하면 숫자가 다시 사라진다.

  - 비정상적으로 종료될 경우 swap 파일이 생성되는데 해당 swap 파일을 삭제하면 다시 정상적으로 편집이 가능하다.
  - 입력 모드로 전환하는 명령어

  | 키   | 설명                                   | 키   | 설명                                       |
  | ---- | -------------------------------------- | ---- | ------------------------------------------ |
  | i    | 현재 커서의 위치부터 입력              | I    | 현재 커서가 위치한 줄의 맨 앞에서부터 입력 |
  | a    | 현재 커서의 다음 칸부터 입력           | A    | 현재 커서가 위치한 줄의 맨 뒤에서부터 입력 |
  | o    | 현재 커서의 다음 줄에 입력             | O    | 현재 커서의 이전 줄에 입력                 |
  | s    | 현재 커서 위치의 한 글자를 지우고 입력 | S    | 현재 커서의 한 줄을 지우고 입력            |

  - 커서 이동
    - 화살표, pageup, pagedown으로도 가능하지만 이런 키들이 없는 경우에 사용할 수 있다.

  | 키                  | 설명                     | 키                | 설명                         |
  | ------------------- | ------------------------ | ----------------- | ---------------------------- |
  | h                   | 커서 왼쪽으로 한 칸 이동 | j                 | 커서를 아래로 한 칸 이동     |
  | k                   | 커서 위로 한 컨 이동     | i                 | 커서를 오른쪽으로 한 칸 이동 |
  | ctrl+F(==page down) | 다음 화면으로 이동       | ctrl+B(==page up) | 이전 화면으로 이동           |
  | ^(==home)           | 현재 행의 처음으로 이동  | $(==end)          | 현재 행의 마지막으로 이동    |
  | gg                  | 맨 첫 행으로 이동        | G                 | 제일 끝 행으로 이동          |
  | 숫자G               | 해당 숫자의 행으로 이동  | :숫자+enter       | 해당 숫자의 행으로 이동      |

  - 삭제, 복사, 붙여넣기

  | 키       | 설명                                  | 키             | 설명                                  |
  | -------- | ------------------------------------- | -------------- | ------------------------------------- |
  | x(==del) | 현재 커서가 위차한 글자 삭제          | X(==backspace) | 현재 커서가 위차한 앞 글자 삭제       |
  | dd       | 현재 커서의 행 삭제                   | 숫자dd         | 현재 커서부터 숫자만큼의 행 삭제      |
  | yy       | 현재 커서가 있는 행을 복사            | 숫자yy         | 현재 커서부터 숫자만큼의 행을 복사    |
  | p        | 복사한 내용을 현재 행 이후에 붙여넣기 | P              | 복사한 내용을 현재 행 이전에 붙여넣기 |

  - 문자열 찾기, 치환

  | 키                            | 설명                                     | 키   | 설명                              |
  | ----------------------------- | ---------------------------------------- | ---- | --------------------------------- |
  | /문자열+enter                 | 현재 커서 이후로 해당 문자열을 찾음      | n    | 찾은 문자 중에서 다음 문자로 이동 |
  | :%s/기존문자열/새문자열+enter | 기존 문자열을 전부 새 문자열로 변경한다. |      |                                   |



## 마운트

- 마운트

  - mount

    - windows에서는 잘 사용하지 않으므로 생소한 개념일 수 있다.
    - 리눅스에서는 하드디스크의 파티션, CD/DVD, USB 메모리 등을 사용하려면 지정한 위치에 연결해줘야한다.

    - 이렇게 물리적인 장치를 특정한 위치(일반적으로 폴더)에 연결시키는 과정을 마운트라한다.

  - mount 확인하기

    - 아래와 같이 어디에 마운트 되었는지 표시된다.
    - `/dev/sda2`는 root 디렉토리(`/`)에 마운트 된 것을 확인 가능하다.

    ```bash
    $ mount
    
    # output
    (...)
    /dev/sda2 on / type ext4 (rw,relatime,errors=remount-ro)
    (...)
    ```

  - 마운트하기

    ```bash
    $ mount <마운트할 장치 이름> <마운트할 디렉토리>
    ```

  - unmount하기

    - 지금 작업중인 디렉터리를 언마운트 할 수는 없다.
    - 즉 예를 들어 예시에서 현재 디렉토리가 `/dev/sda2`인 상태에서 unmount를 시도하면 `target is busy`라는 메시지가 나오며 언마운트에 실패한다.
    - unmount할 장치와 디렉토리 중 어느 것을 입력해도 동일하게 동작한다.

    ```bash
    $ umount <unmount할 장치 이름 혹은 umount할 디렉토리 이름>
    
    # e.g.
    $ umount /dev/sda2
    ```



- iso 파일 마운트하기

  - iso 파일은 cd 혹은 dvd의 내용을 파일로 압축해놓은 것을 뜻한다.
  - iso 파일 생성하기
    - `-r -J` : 8글자 이상의 파일 이름 및 대소문자를 구분해서 인식하기 위한 옵션
    - `-o`: 명령어의 결과 출과로 나올 파일 이름을 작성한다. 

  ```bash
  $ genisoimage -r -J -o <파일명.iso>
  ```

  - 마운트하기

  ```bash
  $ mount -o loop <iso 파일명> <마운트할 디렉토리> 
  ```




## 사용자 관리와 파일 속성

### 사용자와 그룹

- 리눅스는 다중 사용자 시스템(multi-user system)이다.

  - 1대의 리눅스에 여러 명이 동시에 접속해서 사용할 수 있는 시스템이다.
  - 리눅스를 설치하면 기본적으로 root라는 이름을 가진 슈퍼 유저(super-user)가 있다.
    - 이 root 사용자에게는 시스템의 모든 작업을 실행할 수 있는 권한이 있다.
    - 또한 시스템에 접속할 사용자를 생성할 수 있는 권한도 있다.

  - 모든 사용자는 하나 이상의 그룹에 소속되어 있어야 한다.



- 사용자 추가

  - 새로운 사용자를 추가한다.
  - 이 명령어를 실행하면 `/etc/passwd`, `/etc/shadow`, `/etc/group` 파일에 새로운 행이 추가된다.
  - 옵션
    - `--uid`: user id를 지정하여 생성한다.
    - `--gid`: group을 지정하여 생성한다.
    - `--home`: home 디렉토리를 지정하여 생성한다(기본값은 `/home/<사용자명>`).
    - `--shell`: 기본 셸을 지정하여 생성한다(기본값은 `/bin/bash`).
  - 새로운 사용자와 그룹
    - 새로운 사용자에 그룹을 따로 지정해주지 않을 경우 사용자 이름과 동일한 그룹이 생성되고 새로 생성된 사용자는 해당 그룹에 소속되게 된다.

  ```bash
  $ adduser --uid 1111 --gid 1234 --home /home/cha --shell /bin/bash cha
  ```



- 모든 사용자 확인하기

  - 사용자에 대한 정보는 `/etc/passwd` 파일에 저장되어 있다.

  ```bash
  $ cat /etc/passwd
  ```

  - 생각보다 많은 사용자가 보일텐데 모두 리눅스에 기본적으로 존재하는 표준 사용자다.
  - 각 행의 의미는 다음과 같다.
    - 암호가 x로 표시되는 경우 `/etc/shadow` 파일에 비밀번호가 저장되어 있다는 의미다.
    - 추가 정보에는 전체 이름, 사무실 호수, 직장 전화번호, 집 전화번호, 기타 등을 나타낸다.

  ```bash
  <사용자 이름>:<암호>:<사용자ID>:<사용자가 소속된 그룹>:<추가 정보>:<홈 디렉토리>:<기본 셸>
  
  # e.g.
  root:x:0:0:root:/root:/bin/bash
  ```



- 그룹 확인하기

  - 그룹에 대한 정보는 `/etc/group` 파일에 저장되어 있다.

  ```bash
  $ cat /etc/group
  ```

  - 역시 생성하지 않은 수 많은 그룹이 보일텐데 이 역시 리눅스에 기본적으로 존재하는 그룹이다.
  - 각 행의 의미는 다음과 같다.
    - 그룹에 속한 사용자 이름은 참조로 사용된다. 즉 해당 부분에 아무 것도 써 있지 않다고 해서 그룹에 소속된 사용자가 없다는 것은 아니다.

  ```bash
  <그룹 이름>:<비밀번호>:<그룹 id>:<그룹에 속한 사용자 이름>
  ```



- `/etc/skel`
  - 새로운 사용자가 생성될 때, 해당 사용자의 home 디렉토리가 자동으로 생성된다.
  - 이 때 `/etc/skel` 디렉터리의 모든 내용을 사용자의 홈 디렉터리에 복사하는 작업이 발생한다.
  - 따라서, 새로운 사용자를 생성할 때 해당 사용자의 home 디렉토리에 특정 파일을 미리 넣어두고자 한다면 `/etc/skel`에 파일을 추가하면 된다.
  - skel은 skeleton의 약자이다.



- X 윈도 환경에서도 사용자를 관리 가능하다.
  - 바탕 화면 우측 상단의 아래 화살표를 클릭한다.
  - 설정을 클릭 후 사용자를 선택한다.
  - 기본적인 사용자 관리가 가능하다.



- 사용자 변경

  - 사용자명에 `-`를 입력하면 root 사용자로 변경된다.

  ```bash
  $ su <사용자명>
  ```



- 비밀번호 변경

  ```bash
  $ passwd <사용자명>
  ```



- 사용자 속성 변경

  - 옵션
    - `--shell`: 기본 셸을 변경한다.
    - `--groups`: 사용자의 보조 그룹 추가

  ```bash
  $ usermod [옵션] <사용자명>
  
  # e.g.
  $ usermod --groups some cha
  $ usermod --shell /bin/sch cha
  ```



- 그룹 암호 설정 및 그룹 관리

  - 옵션
    - `-A`: 그룹의 관리자를 지정
    - `-a`: 그룹에 사용자를 추가
    - `-d`: 그룹에서 사용자를 제거

  ```bash
  # 그룹 암호 지정
  $ gpasswd <그룹명>
  
  # 그룹 관리
  $ gpasswd [옵션] <사용자명> <그룹명>
  
  # e.g. cha를 mygroup의 관리자로 설정
  $ gpasswd -A cha mygroup
  ```



- 사용자 암호를 주기적으로 변경

  - 옵션
    - `-l`: 설정 사항 확인
    - `-m`: 사용자에 설정한 암호를 사용해야 하는 최소 일자 지정
    - `-M`: 사용자에 설정한 암호를 사용할 수 있는 최대 일자 지정
    - `-E`: 사용자에 설정한 암호가 만료되는 날짜 지정
    - `-W`: 사용자에 설정한 암호가 만료되기 전에 경고 하는 기간. 지정하지 않을 경우 기본값은 7일
  - 기본형
    - `chage`는 CHange AGE의 약자이다. 

  ```bash
  $ chage [옵션] <사용자명>
  ```

  - 예시
    - 2022/02/01에 만료되며, 만료 되기 10 전부터 경고 메시지를 보여준다.

  ```bash
  $ chage -E 2022/02/01 -W 10
  ```



- 그룹 생성

  - 옵션
    - `--gid`: 그룹 id를 지정하여 생성한다.

  ```bash
  $ groupadd [옵션] <그룹명>
  ```



- 그룹의 속성을 변경한다.

  - 옵션
    - `--new-name`: 이름을 변경한다.

  ```bash
  $ groupmod [옵션] <변경할 내용>
  
  # e.g.
  $ groupmod --new-name oldgroup newgroup
  ```



- 그룹 확인

  - 사용자명을 입력하지 않을 경우 현재 사용자가 속한 그룹을 보여준다.

  ```bash
  $ groups [사용자명]
  ```



- 그룹 삭제

  - 삭제하려는 그룹을 주요 그룹으로 지정한 사용자가 없어야 한다.

  ```bash
  $ groupdel <삭제할 그룹 이름>
  ```



### 파일, 디렉터리의 소유권가 허가권

- 리눅스에는 각 파일과 디렉터리마다 소유권과 허가권이라는 속성이 있다.

  - `ls -l` 명령어로 확인이 가능하다.

  ```bash
  $ ls -l
  
  # 결과
  drwxr-xr-x 1 Dell 100230   0 Jan  9 23:02  test/
  -rw-r--r-- 1 Dell 100230   0 Jan  9 23:02  test.txt
  ```

  - 위 결과로 총 8가지 정보를 알 수 있다.
    - 파일 유형(`d`/`-`)
    - 파일 허가권(`rwxr-xr-x`)
    - 링크 수(`1`)
    - 파일 소유자 이름(`Dell`)
    - 파일 소유 그룹(`100230`)
    - 파일 크기(0)
    - 마지막 변경 시간/날짜(`Jan  9 23:02`)
    - 파일 이름(`test/`/`test.txt`)



- 파일 유형
  - 맨 첫 글자를 통해 파일인지 폴더인지를 알 수 있다.
    - `d`: 디렉터리
    - `-`: 파일
  - 그 외에 아래와 같은 것들이 있다.
    - `b`: 블록 디바이스
    - `c`: 문자 디바이스
    - `l` 링크



- 파일 허가권

  - 파일 유형 뒤에 오는 문자들을 통해 파일의 허가권을 알 수 있다.
  - 파일 허가권은 3 글자씩 총 3개의 부분으로 나눌 수 있다.
    - 소유자의 파일 접근 권한
    - 그룹의 파일 접근 권한
    - 그 외 사용자의 파일 접근 권한
  - rwx순으로 표현한다.
    - `r`(read): 읽기 권한을 의미한다.
    - `w`(write): 쓰기 권한을 의미한다.
    - `x`(executable): 실행 권한을 의미한다.
    - `-`: 해당 권한이 없음을 의미한다.
  - 디렉터리는 기본적으로 실행 권한이 있어야 해당 디렉터리로 이동이 가능하다.
    - 따라서 기본적으로 모든 사용자에게 실행 권한이 설정되어 있다.
  - 2진수로 표현이 가능하다.
    - 권한이 있음을 1, 없음을 0으로 표기한다.
    - 이를 10진수로 표현하여 소유자, 그룹, 그 외 사용자의 권한을 순서대로 나열하여 권한을 표기할 수 있다.
    - 아래 예시에서 소유자 권한은 8진수로 7, 그룹 권한은 8진수로 5, 그 외 사용자 권한은 8진수로 3이므로 753으로 표현이 가능하다.

  |       | 소유자 |      |      | 그룹 |      |      | 그 외 사용자 |      |      |
  | ----- | ------ | ---- | ---- | ---- | ---- | ---- | ------------ | ---- | ---- |
  | 문자  | r      | w    | x    | r    | -    | w    | -            | x    | w    |
  | 2진수 | 1      | 1    | 1    | 1    | 0    | 1    | 0            | 1    | 1    |



- 파일 허가권 변경하기

  - chmod 명령어로 허가권 변경이 가능하다.
    - 숫자에는 위 표에서 처럼 소유자, 그룹, 그 외 사용자의 권한을 8진수로 변환한 숫자들을 나열한 숫자를 입력한다.
    - 예를 들어 777은 모든 사용자에게 읽기, 쓰기, 실행 권한을 주겠다는 의미이고, 753은 위 표와 같은 권한을 주겠다는 의미이다.
    - `-r` 옵션을 주면 하위 폴더, 파일까지 모두 적용된다.
  
  ```bash
  $ chmod <옵션> <숫자> <파일명>
  ```
  
  - `u`, `g`, `o`, `a`와 `+`, `-`, 그리고 `x`, `r`, `w` 를 조합하여 변경이 가능하다..
    - `u`는 사용자, `g`는 그룹, `o`는 다른 사용자, `a`는 전부를 의미한다.
    - `+`는 권한 추가, `-`는 권한 제거를 의미한다.
    - 예를 들어 아래 명령어는 사용자에게 읽고 쓰는 권한을 부여하는 것이다.
  
  ```bash
  $ chomd u+rx test.txt
  ```
  
  - 오직 root 사용자만이 변경이 가능하다.



- 특수한 형태의 파일 권한
  - rwx 외에도 특수한 용도의 setuid, setgud, stiky bit가 있다.
    - 따라서 사
  - 앞에서는 파일의 허가권을 8진수 000<sub>8</sub>~777<sub>8</sub>로 표현했으나 실제로는 8진수 0000<sub>8</sub>~0777<sub>8</sub>까지 네 자리로 표현할 수 있다.
  - 8진수 네 자리 중 첫 번째 값을 100<sub>2</sub>(==4)로 표현하는 것을 setuid라 부른다.
    - 리눅스 파일 주 비밀번호를 지정하는 `/bin/passwd`가 이에 해당한다.
    - 이 파일의 경우 파일의 소유자 권한 중 쓰기 권한이 x가 아닌 s로 표기된다.
    - 일반적으로 파일의 실행은 파일을 실행한 사람의 권한으로 실행이 된다.
    - 그러나 이 경우 파일의 소유자 권한으로 파일이 실행된다.
    - 따라서 보안상의 이유로 설정하지 않는 것을 추천한다.
    - 설정 방법: `chmod u+s <파일명>`(u가 아닌 g로 하면 setgid가 된다)
  - 8진수 네 자리 중 첫 번째 값을 010<sub>2</sub>(==2)로 표현하는 것을 setgid라 부른다.
    - 그룹의 권한 중 쓰기 권한이 x가 아닌 s로 표기된다.
    - 마찬가지로 파일을 실행한 사용자의 그룹이 아닌 생성한 자의 그룹으로 파일이 실행된다.
    - 또한 setgid가 설정된 디렉터리에 파일을 생성할 경우 파일을 생성한 사람이 아닌 setgid가 설정된 디렉터리의 소유자가 파일의 소유자가 된다.
    - 설정 방법: `chmod g+s <파일명>`
  - 8진수 네 자리 중 첫 번째 값을 001<sub>2</sub>(==1)로 표현하는 것을 stiky bit라 부른다.
    - 다른 사용자 권한 중 마지막 문자가 x가 아닌 t로 표기된다.
    - 여러 사람이 공유할 디렉터리에 주로 설정된다.
    - stiky bit로 설정된 디렉터리 안에는 모든 사용자가 파일/디렉터리를 생성해서 사용할 수 있지만, 다른 사용자의 파일을 삭제하지는 못한다.
    - 파일의 권한과는 무관하게 오직 파일의 소유자만이 삭제가 가능하다.
    - 설정 방법: `chmod o+t <파일명>`



- 파일 소유권

  - 파일 소유권은 파일을 소유한 사용자와 그룹을 의미한다.
  - 파일 소유권 변경하기

  ```bash
  $ chown <변경할 사용자 이름[.변경할 그룹 이름]> <파일명>
  
  # e.g. 파일 소유권을 cha 유저에게, 파일의 그룹을 ubuntu로 변경
  $ chown cha.ubuntu test.txt
  ```

  - 그룹만 변경하기

  ```bash
  $ chgrp <그룹명> <파일명>
  ```






## 링크

- 링크란
  - inode
    - 리눅스, 유닉스의 파일 시스템에서 사용하는 자료 구조.
    - 모든 파일 혹은 디렉터리는 각자 1개씩 inode를 가진다.
    - 파일이나 디렉터리의 여러 가지 정보(허가권, 소유권, 실제 위치 데이터 위치 등)가 담겨 있다.
    - 이러한 inode가 모여 있는 공간을 inode 블록이라 부르며, 일바적으로 전체 디스크 공간의 1%정도를 차지한다.
    - Data 블록은 실제 데이터가 저장된 디스크 공간으로 전체 디스크의 대부분을 차지한다.
    - `ls -i` 명령으로 inode 번호를 확인할 수 있다.
    - `original file -> inode -> original file data`의 형식이다.
  - 심볼릭 링크와 하드 링크 2가지가 있다.



- 심볼릭 링크
  - 심볼릭 링크는 윈도우의 바로가기와 유사하다.
  - 심볼릭 링크를 생성하게 되면 원본 파일을 가리키고 있는 링크 파일을 하나 만들게 된다.
    - 이 링크 파일은 원본 파일과는 다른 inode를 가지게 되며, 따라서 완전히 다른 파일로 관리된다.
    - 링크 파일의 inode는 original file을 가리키는 데이터를 가리키고 있다.
    - `link file -> inode2 -> original file pointer -> original file -> inode1 -> original file data`의 형식이다.
  - 원본 파일이 삭제될 경우 링크 파일은 아무런 역할을 하지 못하게 된다.
  - 심볼릭 링크 폴더에서의 생성, 수정, 삭제 등은 원본 폴더에도 그대로 적용된다.
    - 그러나 링크 폴더 자체를 삭제한다고 원본 폴더도 삭제되는 것은 아니다.



- 하드링크
  - 하드링크는 원본 파일과 동일한 inode를 지닌다.
  - 하드링크는 소프트링크와는 달리 파일에만 사용이 가능하다.
  - 심볼릭 링크와 마찬가지로 하드링크 역시 하드링크 파일에서의 수정이 원본 파일에도 그대로 적용된다.
  - 심볼릭 링크와 달리 원본 파일이 삭제되어도 하드링크 파일은 사용이 가능하다.



- 명령어

  - 링크 확인하기

  ```bash
  $ ls -l
  ```

  - 하드 링크 생성하기

  ```bash
  $ ln <원본 파일> <링크 파일>
  ```

  - 심볼릭 링크 생성하기
    - `-s` 옵션을 준다.
    - 만일 심볼릭 링크를 건 폴더 내에서 또 다른 폴더에 심볼릭 링크를 걸고 해당 폴더에 접근하려 할 경우 `Too many levels of symbolic link`라는 메시지가 뜨며 접근이 불가능하다.
  
  ```bash
  $ ln -s <원본 파일 혹은 폴더> <링크 파일 혹은 폴더>
  ```



- git 관련
  - vscode의 변경 사항 추적은 적용되지 않는다.
  - 그러나 git status로 확인해보면 실제로는 변경 사항이 그대로 추적되는 것을 확인 가능하다.
  - 따라서 링크 디렉토리에서도 그냥 사용하면 된다.

## 리눅스 패키지 설치

- dpkg와 apt
  - ubuntu에서 패키즈를 설치하는 데 가장 많이 사용되는 명령 들이다.
  - apt가 나오기 이전에는 주로 dpkg(Debian Package)가 많이 사용되었다.
  - 그러나 apt가 나온 지금, apt는 dpkg의 개념과 기능을 포함하므로 최신 버전 ubuntu에서는 apt를 사용한다.
  - apt가 별도로 존재한다기보다 dpkg를 포함한 확장 개념에 가까우므로 먼저 dpkg의 개념을 익혀야 한다.



### dpkg

- deb 파일
  - 초창기 리눅스는 새로운 프로그램을 설치하는 것이 꽤 어려웠다.
  - 이러한 점을 개선하여 데비안 리눅스에서 윈도우의 setup.exe와 비슷하게 프로그램을 설치한 후 바로 실행할 수 있는 설치 파일을 제작했다.
  - 설치 파일의 확장명은 *.deb이며 이를 패키지라고 부른다.



- 패키지 이름
  - deb 파일은 일반적으로 `패키지이름_버전-개정번호_아키텍처.deb`와 같이 명명한다.
  - 패키지 이름
    - 말 그래도 패키지 이름을 나타낸다.
    - 하이픈으로 연결하여 긴 이름으로 존재할 수도 있다.
  - 버전
    - 대부분 3자리 수로 구성된다.
    - 주 버전, 부 버전, 패치 버전 순이며 당연히 숫자가 높을수록 최신이다.
  - 개정번호
    - 문제점을 개선할 때마다 붙여지는 번호다.
    - 번호가 높을수록 많은 개정을 거쳤다는 말이다.
  - 아키텍처
    - 해당 파일을 설치할 수 있는 CPU를 나타낸다.



- dpkg 명령어

  - 설치

  ```bash
  $ dpkg -i <패키지 파일 이름>.deb
  ```

  - 삭제
    - `-r`: 기존에 설치된 패키지 삭제
    - `-P`: 기존에 설치된 패키지 및 설정 파일까지 모두 제거

  ```bash
  $ dpkg <옵션> <패키지 이름>
  ```

  - 패키지 조회
    - `-l`: 설치된 패키지에 대한 정보를 보여준다.
    - `-L`: 패키지가 설치한 파일 목록을 보여준다.

  ```bash
  $ dpkg <옵션> <패키지 이름>
  ```

  - deb 파일의 내용 조회

  ```bash
  $ dpkg --info <패키지 파일 이름>.deb
  ```



- dpkg 명령의 문제점
  - dpkg 명령은 설치 하려는 패키지에 의존성이 있을 경우 이를 해결해주지 않는다.
  - 예를 들어 A라는 패키지를 설치하기 위해서 B라는 패키지가 설치되어 있어야 할 경우 dpkg 명령을 통해 의존 관계에 있는 B 패키지를 먼저 다운 받아야 한다.
  - 문제는 실제 현실에서는 A 패키지를 설치하는데 필요한 패키지가 무엇인지 찾아봐야 한다는 것이며, 찾는다 하더라도 해당 패키지에도 의존성이 있을 수 있다.
  - 따라서 의존 관계를 일일이 다 찾아서 설치해줘야 하는 번거로움이 있다.
  - 이를 해결하기 위해 나온 것이 apt 명령이다.



## apt

- apt
  - dpkg의 의존성 문제를 완전히 해결해준다.
    - 즉 특정 패키지를 설치하고자 할 때, 의존성이 있는 다른 패키지를 자동으로 먼저 설치해준다.
  - 우분투가 제공하는 deb 파일 저장소에서 설치할 deb 파일은 물론, 해당 파일과 의존성이 있는 다른 deb 파일까지 인터넷을 통해 모두 알아서 다운로드 한 후 자동으로 설치해준다.
    - dpkg 명령어는 설치하려는 deb 파일이 DVD에 있거나 인터넷에서 미리 다운로드한 상태에거 설치해야 한다.
    - 단, 인터넷을 통해 다운로드한 후 설치하므로 당연히 인터넷에 정상적으로 연결된 상태여야 한다.



- 기본 사용법

  - 패키지 다운 및 설치
    - `-y`: 아래 명령어를 입력하면 패키지가 다운로드 된 후 사용자에게 설치 여부를 묻는 메시지가 나오는데 `-y` 옵션을 주면 해당 메시지에 yes를 입력한 것으로 간주하고 다운 후 바로 설치한다.

  ```bash
  $ apt install <패키지명>
  ```

  - 패키지 목록 업데이트
    - 실제 패키지를 업데이트 하는 것이 아니라 현재 설치된 패키지들의 최신 버전이 존재하는지를 확인하는 것이다.
    - 이 명령어가 실행되면 우분투 패키지 저장소에 요청을 보내 현재 설치된 패키지들 중 새로운 버전이 나온 패키지들의 목록을 받아온다.
    - 이후 `upgrade` 명령을 입력하면 이 때 받아온 패키지 목록을 기반으로 패키지 업그레이드를 진행한다.
    - `/etc/apt/sources.list` 파일의 내용이 수정되면 다운로드 받을 패키지 목록을 업데이트 하기위해 이 명령어를 실행해줘야 한다.

  ```bash
  $ apt update
  ```

  - 패키지 업그레이드
    - 업그레이드 할 패키지명을 입력하지 않으면 모든 패키지가 업그레이드 된다.

  ```bash
  $ apt upgrade [패키지명]
  ```

  - 패키지 삭제

  ```bash
  $ apt remove <패키지 이름>
  ```

  - 패키지를 설정 파일과 함께 삭제
    - 패키지와 패키지의 설정 파일을 모두 삭제한다.

  ```bash
  $ apt purge <패키지 이름>
  ```

  - 사용하지 않는 패키지 모두 삭제

  ```bash
  $ apt autoremove
  ```

  - 내려 받은 파일 제거
    - `autoclean`을 대신 사용해도 된다.

  ```bash
  $ apt clean
  ```

  - 패키지 정보 보기

  ```bash
  $ apt-cache show <패키지 이름>
  ```

  - 패키지 의존성 확인

  ```bash
  $ apt-cache depends <패키지 이름>
  ```

  - 패키지 역의존성 확인
    - 이 패키지에 의존하는 다른 패키지의 목록을 보여준다.

  ```bash
  $ apt-cache rdepends <패키지 이름>
  ```



- apt의 동작 방식
  - `sources.list`파일
    - `/etc/apt` 디렉터리에는 apt와 관련된 파일들이 존재한다.
    - 그 중 `sources.list` 파일에는 apt 명령을 실행했을 때 인터넷에서 해당 패키지 파일을 검색 할 네트워크의 주소가 저장되어 있다.
  - `apt install` 명령어를 입력할 경우 다음과 같은 과정이 실행된다.
    - `/etc/apt/sources.list`파일에서 우분투 패키지 저장소의 URL을 확인한다.
    - 패키지 저장소의 URL로 요청을 보내 설치할 패키지 목록을 받아온다.
    - 주의할 점은 실제 패키지 파일을 받아오는 것이 아니며, 설치할 패키지 파일들의 목록을 받아온다는 것이다.
    - 받아온 패키지 목록을 출력하고 설치 할 것 인지를 묻는다.
    - `yes`를 입력하면(혹은 `-y` 옵션을 줬다면) 우분투 패키지 저장소의 URL로 실제 패키지를 요청하여 받아온뒤 설치한다.



- sources.list

  - 파일 내용
    - `deb <우분투 저장소 URL> <버전-코드명> <저장소 종류>` 형태로 작성한다.
    - 버전 코드명의 경우 아래와 같이 focal로 설치하면 현재 사용중인 버전의 우분투가 출시된 시점에 제공되는 패키지 버전만 설치하겠다는 의미이다.
    - 만일 현재 사용중인 우분투가 출시된 이후에 업그레이드된 패키지를 설치하고 싶다면 `focal-update`로 수정하면 된다.
    - 저장소 종류별로 URL을 2 개씩 적어 놓은 이유는 하나의 URL이 작동하지 않을 경우를 대비하기 위해서다.

  ```bash
  $ cat /etc/apt/sources.list
  
  deb http://ftp.daumkakao.com/ubuntu/ focal main
  deb http://archive.ubuntu.com/ubuntu/ focal main
  
  deb http://ftp.daumkakao.com/ubuntu/ focal universe
  deb http://archive.ubuntu.com/ubuntu/ focal universe
  
  deb http://ftp.daumkakao.com/ubuntu/ focal multiverse
  deb http://archive.ubuntu.com/ubuntu/ focal multiverse
  
  deb http://ftp.daumkakao.com/ubuntu/ focal restricted
  deb http://archive.ubuntu.com/ubuntu/ focal restricted
  ```

  - 위에서 볼 수 있듯 우분투 패키지 저장소에는 4가지 종류가 있다.
    - main: 우분투에서 공식적으로 제공하는 무료 소프트웨어
    - universe:우분투에서 지원하지 않는 무료 소프트웨어
    - restricted: 우분투에서 공식적으로 지원하는 유료 소프트웨어
    - multiverse: 우분투에서 지원하지 않는 유료 소프트웨어
  - 만일 무료 제품만 사용하고 싶다면 multiverse와 restricted 행을 주석처리하면 된다.

  - 우분투 저장소 미러 사이트

    - 우분투 패키지 저장소는 우분투 웹 사이트뿐 아니라 전 세계적으로 수백 개의 각기 다른 곳에서 제공된다.
    - 만약 저장소를 오직 우분투 웹 사이트에서만 제공했다면, 전 세계에서 들어오는 apt 명령어의 실행을 감당할 수 없을 것이다.
    - 대학, 연구소, 기업체 등에서 자발적으로 참여하여 저장소를 구축하고 있다.
    - 이렇게 동일한 저장소를 제공하는 각기 다른 사이트들을 미러 사이트라고한다.

    - 위에도 미러 사이트들이 적혀 있는데, 현재는 모두 정상적으로 동작하지만, 후에 미러 사이트가 삭제되는 등의 이유로 더 이상 사용할 수 없게 되면 다른 미러 사이트의 주소를 입력해주면 된다.



## 파일 압축과 묶기

- 파일 압축하기

  - 리눅스에서 많이 사용하는 압축 파일의 확장명은 다음과 같다.
    - `xa`, `bz2`, `gz`, `zip`, `Z` 등
  - `xz`
    - 확장명을 `xz`로 압축하거나 풀어준다. 비교적 최신 압축 명령으로 압축률이 뛰어나다.
    - `-d`: 압축을 푼다.
    - `-l`: 압축 파일에 포함된 파일 목록과 압축률 등을 출력한다.
    - `-k`: 압축 후 기존 파일을 삭제하지 않고 그대로 둔다.

  ```bash
  $ xz [옵션] <파일명>
  ```

  - `bzip2`
    - 확장명을 `bz2`로 압축하거나 푼다.
    - `-d`: 압축을 푼다.
    - `-k`: 압축을 푼 후 기존 파일을 삭제하지 않고 그대로 둔다.

  ```bash
  $ bzip2 [옵션] <파일명>
  
  # 예시. 아래 코드의 결과 test.bz2 파일이 생성된다.
  $ bzip2 test
  
  # -d 옵션을 주지 않아도 .bz2라고 압축 확장명을 입력하면 압축이 풀린다.
  # 아래 두 명령어는 완전히 같다.
  $ bzip2 -d test.bz2
  $ bzip2 test.bz2
  ```

  - gzip
    - 확장명을 `gz`로 압축하거나 푼다.
    - `-d`: 압축을 푼다.

  ```bash	
  $ gzip [옵션] <파일명>
  
  # bzip과 마찬가지로 압축파일의 확장명까지 입력하면 압축이 풀린다.
  # 아래 두 명령어는 완전히 같다.
  $ gzip -d test.gz
  $ gzip test.gz
  ```

  - zip/unzip
    - 윈도우화 호환되도록 zip으로 압축하거나 푼다.

  ```bash
  $ zip <새로 생성할 압축파일명.zip> <압축할 파일 이름>
  $ unzip <압축 풀 파일 이름.zip>
  ```



- 파일 묶기

  - 윈도우의 경우 zip파일을 생성할 때 파일 묶기와 압축이 동시에 실행된다.
    - 예를 들어 a.txt, b.txt, c.txt을 d.zip으로 만들면 d.zip 파일로 묶임과 동시에 압축이 진행된다.
  - 그러나 리눅스는 압축과 묶기가 별개로 진행된다.
  - `tar`
    - 파일 묶기를 실행하는 명령어이다.
    - `c`: 새로운 묶음을 만든다.
    - `x`: 묶인 파일을 푼다.
    - `t`: 묶음을 풀기 전에 묶인 경로를 보여준다.
    - `C`: 묶음을 풀 때 지정된 디렉터리에 압축을 풀어준다.
    - `f`: 묶음 파일 이름을 지정한다.
    - `v`: 파일을 묶거나 푸는 과정을 보여준다.
    - `J`: 묶고 난 후 `xz` 파일로 압축한다.
    - `z`: 묶고 난 후 `gzip` 파일로 압축한다.
    - `j`: 묶고 난 후 `bzip2` 파일로 압축한다.

  ```bash
  $ tar [옵션]
  ```



## 파일 위치 검색

- find
  - 옵션(아래는 대표적인 옵션일 뿐, 보다 다양한 옵션이 존재한다.)
    - `-name`: 파일 혹은 폴더 이름(기본값)
    - `-user`: 사용자 이름
    - `-newer`: 일정 파일이 생성된 이후에 생성된 파일을 찾는다.
    - `-perm`: 허가권
    - `-size`: 파일 사이즈
  - action
    - `-print`: 기본 옵션
    - `-exec`: 외부 명령 실행
  
  ```bash
  $ <파일을 찾을 위치> [옵션] [-exce <실행할 명령>] <찾을 파일 정보>
  ```
  
  - 예시
  
  ```bash
  $ find /home *.md
  $ find /home -user theo
  $ find /home -perm 644
  $ find /home -newer test.txt # test.txt보다 이후에 생성된 파일을 찾는다.
  $ find /home ! -newer test.txt # test.txt보다 이전에 생성된 파일을 찾는다.
  $ find /home -size +100k -size -300k # 100kb이상, 300kb이하인 파일을 찾는다.
  ```
  
  - `-exec` 옵션 예시
    - `\;`는 외부 명령어의 끝을 의미한다.
    - `{}`에 find 명령어의 결과(예시의 경우 `find /home -user theo` 명령의 결과가 들어간다고 생각하면 된다.)
  
  ```bash
  # home 디렉토리의 하위에서 사용자명이 theo인 파일을 모두 삭제
  $ find /home -user theo -exec rm {} \;
  ```



- 기타
  - `which`
    - PATH에 설정된 디렉터리만 검색(python, java 등과 같이 PATH에 설정된 것들만 검색한다).
    - 절대 경로를 포함한 위치를 검색한다.
  - `whereis`
    - 실행 파일 및 소스, man 페이지 파일까지 검색
  - `locate`



## cron과 at

- cron

  > https://crontab.guru 이 사이트에서 실행 주기별 설정을 미리 볼 수 있다.

  - 주기적으로 특정 명령을 실행할 수 있도록 시스템 작업을 예약해놓는 것이다.
  - cron과 관련된 데몬은 crond이고, 관련 파일은 /etc/crontab이다.




- crontab

  - 특정 시간에 특정 프로그램을 특정 주기로 실행시키는 프로그램
  - 설치

  ```bash
  $ apt-get install cron
  ```

  - 크론탭 설정하기
    - vi 에디터를 사용하여 크론탭 설정을 입력한다.
    - `*` , 숫자,  `,`, `-`를 조합해서 설정한다.

  ```bash
  $ corntab -e
  
  *			*			*			*			*	[사용자명] <실행할 명령>
  분(0-59)	   시간(0-23)   일(1-31)	 월(1-12)	요일(0-7, 0과 7은 일요일, 1-6은 월-토요일 순이다.)
  
  # 만일 아래와 같이 설정하면 test.sh를 매분 실행하겠다는 뜻이다.
  * * * * * test.sh
  # 매월 5,15,25일 10시 정각, 20분, 30분에 test.sh를 실행하겠다는 뜻이다.
  0,20,30 10 5,15,25 * * test.sh
  # 매월 10~20일 매 20분마다 test.sh를 실행하겠다는 뜻이다.
  */20 * 10-20 * * test.sh
  
  # 로그 남기기
  * * * * * test.sh > test.sh.log 2>&1
  ```

  - 크론탭 설정 내용 확인

  ```bash
  $ crontab -l
  ```

  - 크론탭 설정 내용 삭제

  ```bash
  $ crontab -r
  ```
  
  - crontab log
    - `/var/spool/mail/<사용자명>`과 `/var/log/cron`에서 확인 가능하다.
    - 아니면 아래와 같이 직접 로그 파일을 지정할 수도 있다.
  
  ```bash
  * * * * * <실행할 명령> > <log를 남길 파일 경로> 2>&1
  ```
  
  - crontab으로 shell script 실행
  
  ```bash
  # 아래와 같이 sh 명령어와 함께 입력한다.
  * * * * * sh /some/path/test.sh
  
  # 혹은 shell script 파일에 실행 권한을 추가한다.
  $ chmod +x /some/path/test.sh
  * * * * * /some/path/test.sh
  ```



- at

  - cron이 주기적으로 반복하는 작업을 예약하는 것이지만, at 명령어는 일회성 작업을 예약하는 것이다.
    - 즉, 예약하면 한 번만 실행하고 소멸된다.

  - 설치
    - 기본 패키지가 아니므로 설치가 필요하다.

  ```bash
  $ apt install rdate at
  ```

  - 명령어

  ```bash
  $ at <시간>
  
  # 예시
  $ at 3:00am tomorrow
  $ at 7:00:pm January 30
  $ at now + 1 hours
  ```

  - 예약 확인

  ```bash
  $ at -l
  ```

  - 취소

  ```bash
  $ atrm <작업번호>
  ```




## 파이프, 필터, 리디렉션

- 파이프

  - 2개의 프로그램을 연결하는 연결 통로를 의미한다.
  - `|`를 사용한다.
  - 예시

  ```bash
  $ ls -l /etc | less
  ```



- 필터

  - 필요한 것만 걸러주는 명령어
  - `grep`, `tail`, `wc`, `sort`, `awk`, `sed` 등이 있다.
  - 주로 파이프와 같이 사용된다.

  - 예시

  ```bash
  $ ps -ef | grep python
  ```



- 리디렉션

  - 표준 입출력의 방향을 바꿔준다.
    - `>`는 output을, `<`는 input을 의미한다.
  - 표준 입력은 키보드, 표준 출력은 모니터이지만 이를 파일로 처리하고 싶을 때 주로 사용한다.

  - 예시

  ```bash
  # ls -s 명령어의 결과를 list.txt파일에 저장한다(기존에 파일이 존재하는 경우 덮어쓴다).
  $ ls -l > list.txt
  
  # ls -s 명령어의 결과를 list.txt파일에 저장한다(기존에 파일이 존재하는 경우 이어쓴다).
  $ ls -l >> list.txt
  
  # list.txt 파일을 정렬해서 out.txt 파일에 쓴다.
  $ sort < list.txt > out.txt
  ```



## 프로세스, 데몬, 서비스

- 프로세스
  - 하드디스크에 저장된 실행 코드(프로그램)가 메모리에 로딩되어 활성화된 것이다.
  - 예를 들어 웹 브라우저 프로그램인 Firefox는 하드 디스크의 어딘가에 저장되어 있을 것이다.
  - 이렇게 하드에 저장된 파일을 프로그램이라 부르며, Firefox를 실행해서 화면에 나타난 상태(메모리에 로딩된 상태)를 프로세스라고 부른다.



- 프로세스 관련 개념

  - 포그라운드 프로세스
    - Foreground Process란 화면에서 실행되는 것이 보이는 프로세스라고 생각하면 된다.
  - 백그라운드 프로세스
    - Background Process는 실행은 되고있지만 화면에 나타나지 않고 뒤에서 실행되는 프로세스를 말한다.

  - 프로세스 번호
    - 메모리에 로딩되어 활성화된 프로세스를 구분하려면 각각의 고유 번호가 필요하다.
    - 이렇게 각각의 프로세스에 할당된 고유 번호를 프로세스 번호라고 한다.
  - 작업 번호
    - 현재 실행되는 백그라운드 프로세스의 순차 번호를 의미한다.
  - 부모 프로세스와 자식 프로세스
    - 모든 프로세스는 혼자서 독립적으로 실행되는 것이 아니라 부모 프로세스의 하위에 종속되어 실행된다.
    - 예를 들어 X 윈도에서 Firefox를 실행한다면 X 윈도는 Firefox의 부모 프로세스, Firefox는 X 윈도의 자식 프로세스라고 부른다.
    - 부모 프로세스를 종료하면 그에 종속된 자식 프로세스도 모두 종료된다.



### 프로세스 관련 주요 명령어

- `ps`

  - 현재 프로세스의 사태를 확인하는 명령어
  - 옵션
    - `-e`: 모든 프로세스를 출력한다.
    - `-f`: 모든 포맷을 보여준다.
    - `-l`: 긴 포맷으로 보여준다.
    - `-p`: 특정 PID의 프로세스를 보여준다.
    - `-u`: 특정 사용자의 프로세스를 보여준다(지정하지 않으면 현재 사용자가 기준이 된다).

  ```bash
  $ ps <옵션>
  
  # UID: 실행 유저
  # PID: 프로세스 ID
  # PPID: 부모 프로세스 ID
  # C: CPU 사용량
  # STIME: Start Time
  # TTY: 프로세스 제어 위치
  # TIME: 구동 시간
  # CMD: 실행 명령어
  UID        PID  PPID  C STIME TTY      TIME 	CMD
  root     13723 13008  1 Sep26 ?        08:43:35 python3.7 /svc/main.py
  ```



- kill

  - 프로세스를 강제로 종료하는 명령어
  - `-l` 옵션으로 signal의 종류를 출력한다.
  - `-9` 옵션과 함께 사용하면 무조건 프로세스가 종료된다(`-9` 옵션은 `-SIGKILL` signal을 의미한다).

  ```bash
  $ kill <옵션> <PID>
  ```



- pstree

  - 부모 프로세스와 자식 프로세스의 관계를 트리 형태로 모여준다.

  ```bash
  $ pstree
  ```



- 프로세스 상태 변경하기

  - 포그라운드, 백그라운드로 프로세스의 상태를 변경 가능하다.
  - 포그라운드 프로세스는 `ctrl+z`로 일시 중지가 가능하다.

  - 백그라운드로 변경하기

  ```bash
  $ bg %<작업번호>
  ```

  - 프로세스 작업번호 확인하기
    - `nohup`으로 실행한 프로세스는 jobs에서 보이지 않는다.

  ```bash
  $ jobs
  
  # [<작업번호>]+ <상태> <명령어>
  ```

  - 포그라운드로 변경하기

  ```bash
  $ fg <작업번호>
  ```

  - 백그라운드로 실행하기
    - 명령어 뒤에 `&`를 붙이면 백그라운드로 실행된다.

  ```bash
  $ python test.py &



### 서비스

- 서비스와 소켓
  - 서비스
    - 데몬이라고도 부르는 서비스는 서버 프로세스를 말한다.
    - 서비스는 눈에 보이지 않지만 현재 시스템에서 동작 중인 프로세스이므로 백그라운드 프로세스의 일종이라고 할 수 있다.
  - 서비스는 평상시에도 늘 가동하는 서버 프로세스며, 소켓은 필요할 때만 작동하는 서버 프로세스다.
  - 서비스와 소켓은 systemd라는 서비스 매니저 프로그램으로 작동시키거나 관리한다.



- 서비스의 특징
  - 시스템과 독자적으로 구동되어 제공하는 프로세스를 말한다. 
    - 웹 서버, DB 서버, FTP 서버 등이 있다.
  - 실행 및 종료는 대개 `sytemctl <start/stop/restart/status> <서비스 이름>`으로 사용한다.
  - 서비스의 실행 스크립트 파일은 `/lib/systemd/system` 디렉터리에 `서비스명.service`라는 이름으로 확인 할 수 있다.
    - 이 디렉터리에 있는 파일들은 대부분 `systemctl` 명령으로 시작, 정지, 재시작 할 수 있다.
  - 부팅과 동시에 서비스의 자동 실행 여부를 `systemctl list-unit-files` 명령으로 확인이 가능하다. 



- 소켓의 특징
  - 서비스는 항상 가동되지만 소켓은 외부에서 특정 서비스를 요청할 경우 systemd가 구동시킨다.
    - 요청이 끝나면 소켓도 종료된다.
  - 소켓으로 설정된 서비스를 요청할 때 처음 연결되는 시간은 서비스에 비해 약간 오래 걸릴 수 있다.
    - systemd가 서비스를 새로 구동하는 데 시간이 소요되기 때문이다.
    - 이와 같은 소켓의 대표적인 예로 텔넷 서버를 들 수 있다.
  - 소켓과 관련된 스크립트 파일은 `/lib/systemd/system` 디렉터리에 `소켓명.socket`이라는 파일로 존재한다.







