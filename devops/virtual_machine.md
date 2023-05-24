# 가상머신 소개와 설치

> 아래 내용은 Windows 10 64 bit 기준이다.

- 가상 머신(Virtual Machine)
  - 이름 그대로 진짜 컴퓨터가 아닌 가상으로 존재하는 컴퓨터를 말한다.
    - 컴퓨팅 환경을 소프트웨어로 구현한 것이라고 생각하면 된다.
  - 가상 머신은 멀티 부팅과 개념이 다르다.
    - 멀티 부팅은 하드디스크나 SSD의 파티션을 분할한 후, 한 번에 하나의 운영체제만 가동할 수 있는 환경이다.
    - 가상 머신은 파티션을 나누지 않고 동시에 여러개의 운영체제를 가동한다.
  - 하이퍼바이저(Hypervisor)
    - VM을 생성하고 구동하는 소프트웨어.
    - 호스트 컴퓨터에서 다수의 운영 체제를 동시에 실행하기 위한 논리적 플랫폼이다.
  - 컨테이너와의 차이
    - Guest OS를 부팅하는 VM과 달리 container는 guest OS를 사용하지 않기에 VM보다 가볍다.
    - 대신 container는 host OS로부터 커널을 공유받아 사용한다.



- 가상 머신 소프트웨어
  - 컴퓨터에 설치된 운영체제 안에 가상의 컴퓨터를 만들고 그 가상의 컴퓨터 안에 또 다른 운영체제를 설치/운영할 수 있도록 제작된 소프트웨어
    - 즉, 가상 머신을 생성하는 소프트웨어를 가상 머신 소프트웨어라고 한다.
  - 용어 정리
    - 호스트 컴퓨터: 실제 컴퓨터
    - 게스트 컴퓨터: 생성된 가상 머신
    - 호스트 운영체제: 호스트 컴퓨터에 설치된 운영체제.
    - 게스트 운영체제: 게스트 컴퓨터에 설치한 소프트웨어.
  - 종류
    - VMware의 VMware vShpere, MS의 Hyper-V, Oracle의 Virtual Box 등이 있다.
    - 모두 무료로 사용이 가능하다.
    - 아래 실습에서는 VMware Workstation을 사용할 것이다.
  - VMware Workstation
    - Pro와 Player로 나뉘어져 있으며 Pro는 유료, Player는 무료이다.
    - Pro는 30일 무료 평가판을 사용 가능하다(평가 기간이 종료되면 가상 머신을 부팅할 수 없지만, 스냅숏이나 네트워크 설정 기능은 계속 사용할 수 있다).
    - Pro를 설치하면 Player도 함께 설치된다.
  
  |                           | Pro                                                          | Player                        |
  | ------------------------- | ------------------------------------------------------------ | ----------------------------- |
  | 호스트 운영체제           | Windows 7 이상의 64 bit Windows                              | 동일                          |
  | 게스트 운영체제           | 모든 16 bit, 32 bit, 64 bit Windows 및 대부분의 리눅스 운영체제 | 동일                          |
  | 라이선스                  | 유료                                                         | 유료 또는 무료(비상업적 용도) |
  | 가상머신 생성 기능        | O                                                            | O                             |
  | 스냅숏 기능               | O                                                            | X                             |
  | 가상 네트워크 사용자 설정 | O                                                            | X                             |
  | 부가기능                  | 여러 부가 기능이 있다.                                       | 부가 기능이 별로 없다.        |



- VMware의 특징
  - 장점
    - 1대의 컴퓨터 만으로 실무 환경과 거의 비슷한 네트워크 환경을 구성할 수 있다.
    - 운영체제의 특정 시점을 저장하는 스냅숏 기능을 사용할 수 있다.
    - 하드디스크 등의 하드웨어를 여러 개 장착해서 테스트가 가능하다.
    - 가상 머신 상태를 저장해두고, 다음에 사용할 때 저장된 상태를 이어서 구동할 수 있다.
  - 단점
    - 적당한 고사양의 컴퓨터가 필요하다.
    - 원할하게 운영하기 위해서는 쿼드 코어 이상급의 CPU와 8GB 이상의 메모리, 넉넉한 여유 공간의 SSD 또는 하드디스크 사용을 권장한다.



- Vmware Workstation 설치

  > https://www.vmware.com/kr.html

  - 위 사이트에 접속해서 VMware Workstation Pro(이하 Pro) 평가판의 설치 파일을 다운 받는다.
    - Pro를 설치하면 Player도 함께 설치된다.
  - 설치 파일을 실행하여 설치를 진행하면 되며, 설치 진행 중에 특별히 설정을 변경할 만한 것은 없다.
  - 설치가 완료되면 프로그램을 실행하여 `I want tp try VMware Workstation 16 for 30 days`를 클릭하고 진행한다.
    - 이후 창을 종료하고 VMware Workstation Player(이하 Player)를 실행한다.







# 가상 머신 생성

- 사전 준비
  - 가상머신은 `.vmdk`라는 확장명을 포함한 여러 개의 관련된 파일로 존재하며, 각각의 가상 머신은 지정한 폴더에 생성된다.
  - 폴더에 저장되므로 디스크 공간이 여유로운 드라이브에 생성하는 것을 권장한다.
  - Ubuntu20.04 폴더를 생성하고 그 하위 폴더로 Server, Server(B), Client, WinClient 폴더를 생성한다.
  - 가상 하드디스크의 내부 작동
    - 가상 하드디스크 장착 시 가상머신은 이를 진짜 하드디스크와 동일하게 취급하지만, 호스트 컴퓨터 입장에서 가상 하드디스크는 하나의 커다란 파일(`.vmdk`)이 된다.
    - 이 가상 하드디스크는 가상머신에 20GB(위에서 설정해준 기본 용량)라고 인식시키면서도 실제 물리 파일의 크기는 겨우 10MB 정도로 설정된다.
    - 즉 10MB짜리 하드디스크를 20GB라고 가상머신을 속이는 것이다.
    - 이후 가상머신에 운영체제 등을 설치하면 실제 공간이 필요해지면서 필요한 공간만큼 자동으로 조금씩 늘어나지만, 위에서 설정한 값 이상으로 늘어나지는 않는다.
- 각 가상 머신 별 상세 스펙은 아래 [운영체제 설치하기] 참조



- 가상 머신 생성하기
  - Player에서 `Create new virtual machine`, 혹은 `new virtual machine`을 클릭한다.
  - New Virtual Machine Wizard의 첫 화면은 운영체제를 설치하는 방법을 선택하는 창인데 우선은 가상 머신만 생성하고, 운영체제는 이후에 설치할 것이기에 `I will install the operating system later`를 체크 후 넘어간다.
  - 이후 운영체제를 선택하는 화면이 나오는데 Ubuntu 64-bit를 선택한다.
  - 이후 가상머신 이름과 가상머신을 저장할 폴더를 지정하는 화면이 나오는데, 이름을 지정해주고, 위에서 생성한 `Ubuntu20.04/Server` 디렉터리를 선택한다.
  - 다음으로 생성중인 가상 머신의 가상 하드디스크 용량을 지정하는 화면이 나온다. 
    - 일단 기본값인 20GB로 설정한다. 
    - `Store virtual disk as a single file`은 하드디스크 파일을 하나의 파일로 관리하겠다는 것이고, 그 뒤의 `Split virtual disk into multiple files`는 여러 개의 파일에 저장하겠다는 것인데, 실제 사용에는 차이가 없다.
    - `Allocate all disk space now`는 가상 하드디스크의 내부적인 작동 방식 처럼 가상 하드디스크를 관리하지 않으며, 실제 설정해준 용량 만큼의 여유 공간이 있어야 되도록 설정하는 것이다.
  - 이후 Finish를 클릭하고 가상 머신 생성을 완료한다.



- 가상 머신에 장착된 부품 변경하기

  - 가상 머신을 선택 후 `Edit virtual machine settings`를 클릭한다.
  - Memory(==RAM) 부분은 호트스 컴퓨터가 가진 메모리를 가상머신과 나눠 갖게 하는 설정이다
    - 예를 들어 컴퓨터에 4GB의 메모리가 장착되어 있다면, 가상 머신을 부팅하는 순간 호스트와 게스트 컴퓨터가 2GB씩 나눠 갖게 된다. 
    - 우분투를 설치하려면 2GB(2048) 정도의 메모리가 필요하므로 최소한 2048로 설정해준다.
  - Processors(==CPU)
    - 호스트 컴퓨터의 CPU가 멀티코어라면 가상머신에도 CPU를 여러 개 할당할 수 있다.
    - 가상머신의 성능에 큰 의미는 없으므로 그냥 1로 둔다.
  - Hard Disk
    - 아래 설명 참조
    - 아래와 같이 20GB로 잡는다고 실제 20GB를 차지하는 것이 아니므로 필요한 만큼 설정해도 된다.
    - 만일 기존 Hard Disk를 삭제하고 80GB짜리 하드디스크를 추가하고 싶다면 기존 Hard Disk를 선택 후 Remove를 눌러 삭제 한 뒤 Add를 눌러 새로운 Hard Disk를 추가하면 된다.
    - Add시에 Select a Disk의 첫 번째 항목인 `Create a new virtual disk`는 새로운 virtual disk를 추가한다는 의미이고, 두 번째 항목인 `Use an existing virtual machine`은 기존에 사용하던 가상 하드디스크(`.vmdk`파일)를 그대로 사용한다는 의미이며, 마지막 항목인 `Use a physical disk`는 진짜 물리적인 하드디스크를 가상머신에 장착한다는 의미이다.
    - `.vmdk`파일의 naming은 `가상머신 이름-숫자.vmdk`와 같이 지정된다.
  - CD/DVD
    - 가상머신에 CD/DVD를 장착한다.
    - 가상 머신에 장착된 CD/DVD는 2가지 방식으로 사용할 수 있는 데, 그 중 하나는 호스트 컴퓨터에 부착된 CD/DVD 장치를 그대로 이용한ㄴ 것이고 다른 하나는 파일로 된 `.iso` 파일을 CD/DVD처럼 사용하는 것이다.
    - 우분투 리눅스 설치를 위해선 `Device status`는 꼭 `Connect at power on`으로 둬야 추후 우분투 리눅스의 설치 DVD를 자동으로 인식한다.

  - Natwork Adapter(==랜카드, NIC, 네트워크 카드)
    - 기본 설정이 NAT 방식이다.
  - 설정이 모두 완료되면 OK를 눌러 설정을 적용한다.



- 가상 머신을 목록에서 제거하고 다시 불러오기
  - 목록에서 제거하기
    - 생성한 가상 머신을 우클릭 후 `Remove from the Library`를 클릭하면 목록에서 제거된다.
    - `Delete from Disk`를 클릭하면 하드디스크에서 완전히 삭제되므로 주의해야 한다.
  - 다시 불러오기
    - 이후 `Player-file-Open` 혹은 `Open a Vritual Machine` 클릭 후 가상머신을 저장했던 폴더의 `.vmx`파일을 선택하면 다시 목록으로 불러와진다. 



- 가상 머신 부팅
  - 부팅 방법
    - 가상 머신 선택 후 `Play virtual machine`을 클릭
    - `Player-Power-Power On`을 클릭
    - 가상 머신 선택 후 우클릭하여 `Power on`을 클릭
    - 메뉴의 초록색 실행 버튼을 클릭
  - 부팅하기
    - `Cannot connect the virtual device sata0~`과 같은 메시지가 나올 수 있는데 컴퓨터에 DVD 장치가 없을 경우 나오는 메시지로, No를 누르고 넘어가면 된다.
    - Operating System not found라는 메시지가 출력되는데 아직 OS를 설치하지 않았기 때문이다.
    - `Player-Power-Shut Down Guest`를 클릭하여 종료한다(경고 메시지가 나올 경우 yes를 클릭한다).
    - 마우스가 작동하지 않을 경우 ctrl+alt를 눌렀다 뗀다.



# VMware 사용 방법

- VMware 핫 키
  - 가상 머신을 가동하면 현재 컴퓨터에서 작동하는 운영체제는 2개 가 된다.
    - 그러나 마우스와 키보드는 1개 밖에 없으므로 마우스의 포커스를 호스트OS와 게스트 OS 사이에 이동이 가능하기 해야 한다.
    - 게스트 OS로 초점을 이동하려면 가상 머신 화면 안의 아무 곳이나 마우스로 클릭하면 된다.
    - 다시 호스트 OS로 마우스 초점을 가져오려면 ctrl+alt를 동시에 눌렀다 떼면 된다.
  - ctrl+alt+delete
    - 이 세 키는 현재 포커스가 게스트OS에 있더라도 호스트 OS까지 영향을 미친다.
    - 따라서 VMware에서는 ctrl+alt+delete 대신 ctrl+alt+insert를 사용하도록 권장한다.
    - 즉, 게스트 OS에서는  ctrl+alt+delete 대신 ctrl+alt+insert를 사용한다.



- VMware Player 종료 시 닫기 옵션
  - 가상 머신을 구동하는 중에 Player 우측 상단의 창 닫기 버튼을 클릭하면 가상 머신의 현재 상태를 정지 또는 종료로 둘 수 있도록 선택하는 화면이 나온다.
  - 정지 상태는 절전 모드와 유사한 상태라고 보면 된다.



- 전체 화면으로 사용하기
  - 게스트 OS를 전체 화면으로 보고 싶다면 VMware 창의 최대화 아이콘을 클릭하거나 마우스의 초점을 VMware 내부로 옮긴 후 ctrl+alt+enter를 누른다.
    - 이전 화면 크기로 돌아가는 것 역시 동일한 방법으로 돌아가면 된다.
  - 전체 화면을 사용하려면 가상머신이 가동되고 있어야 한다.



- 여러 개의 가상머신을 동시에 부팅하기
  - Player는 하나의 가상 머신만 무팅이 가능하다.
  - 따라서 여러 개의 가상머신을 동시에 부팅하려면 Player를 여러 개 실행한 후 각각 다른 가상머신을 부팅해야 한다.



- 네트워크 정보 파악과 변경
  - 정상적인 네트워킹이 이루어지려면 아래 4 가지의 정보를 알아야 한다.
    - IP 주소
    - 서브넷 마스크
    - 게이트웨이 주소
    - DNS 서버 주소
  - cmd에 ipconfig/all을 입력하면 위 정보를 확인 가능하다.
  - 가상 IP를 생성한다.
    - Pro를 실행한다.
    - 메뉴의 `Edit-Virtual Network Editor`를 클릭한다.
    - 만일 우측 하단에 `Change Settings`가 있으면 클릭하고 경고창에서 <예>를 클릭한다.
    - VMnet8을 선택 후 하단의 Subnet IP의 3 번째 주소 값을 111로 변경하고 OK를 클릭한다(꼭 111일 필요는 없고 변경하고 싶은 값으로 변경해도 된다.).
    - cmd에 ipconfig/all을 입력한 후 `VMware Virtual Ethernet Adapter for VMnet8`부분에 IPv4 주소가 192.168.111.1로 보이면 성공한 것이다.



- 호스트 OS와 게스트 OS 사이의 파일 전송 방법
  - 가장 간편한 방법은 호스트 OS에서 게스트 OS로 보낼 파일을 ISO 파일로 만든 후, 게스트 OS에 CD/DVD를 넣어주는 방법을 사용할 수 있따.
    - ISO 파일을 만들어주는 프리웨어 중 가볍고 빠른 Free ISO Creator를 추천한다.
  - 아직 운영체제를 설치하지 않았으므로 해 볼 순 없지만 대략적인 순서는 다음과 같다.
    - Player 메뉴의 `Removable Devices - CD/DVD (SATA)- Settings`를 선택한다.
    - `Use ISO image file`을 선택한 후 Browse를 클릭해 ISO 파일을 선태한다.
    - 주의할 점은 `Device status` 부분에 `Connected`가 꼭 체크되어 있어야 한다는 것이다.



# 운영체제 설치하기

> https://ubuntu.com/
>
> https://cdimage.ubuntu.com/kubuntu/releases/20.04/release/

- 위 사이트에서 아래 파일들을 다운 받는다.
  - ubuntu-20.04.2-live-server-amd64.iso 
  - kubuntu-20.04.2.0-desktop-amd64.iso
  - ubuntu-20.04.2.0-desktop-amd64.iso
  - 대용량 파일이므로 상당한 시간이 소요된다.



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



## ubuntu desktop 설치하기

- 설치하기
  - player를 실행 후 VMware Workstation 15 Player 창에서 위에서 생성한 Server_A를 선택하고 Edit virtual machine settings를 클릭한다.
  - CD/DVD 탭에서 Browse를 클릭하고 Server용으로 다운 받은 파일(ubuntu-20.04.2.0-desktop-amd64.iso)을 선택후 OK를 클릭한다. 
    - connect at power on을 체크해야 한다.
  - 그 후 Play virtual machine을 클릭하여 가상머신을 부팅한다.
    - 부팅 후 리눅스 설치가 진행된다.
    - X 윈도 창이 나오는데, X 윈도는 리눅스와 유닉스 대부분에서 사용되는 그래픽 환경 기반 시스템 소프트웨어로 1984년 MIT에서 최초 공개한 이후 지금까지 보편적으로 사용되고 있다.
    - 중간에 Welcome이라는 창에서 언어를 선택할 수 있는데 여기서 한국어를 선택 후 ubuntu 체험하기를 클릭한다.
    - 이후 우측 상단바를 클릭하여 settings를 클릭하고 원하는 해상도로 변경해준다.
  - 바탕화면에서 `ubuntu 20.04.X LTS 설치`를 클릭한다.
    - 언어는 한국어를 클릭하고, 가장 상단에 있는 Korean을 누르고 계속하기를 선택한다.
    - 이후 일반설치를 클릭하고, ubuntu 설치 중 업데이트 다운로드는 체크 해제한다.
    - 설치 형식은 기타를 클릭한다.
    - 다음 화면에서 dev/sda 선택 후 새 파티션 테이블을 클릭하고, 경고창이 나오면 계속하기를 클릭한다.
    - 이후 남은 공간을 선택 후 좌측 하단의 + 버튼을 클릭한다.
    - 파티션 만들기 창이 나오면 크기에 4096을, 용도를 스왑 영역으로 선택 후 OK를 클릭한다.
    - 다시 남은 공간을 선택 후 좌측 하단의 + 버튼을 클릭한다.
    - 크기는 그대로 두고 새 파티션의 종류를 주로 선택하고 용도는 EXT4 저널링 파일 시스템으로 설정 후 마운트할 위치를 `/`로 설정한다.
    - 이후 지금 설치를 클릭하고 바뀐 점을 디스크에 쓰겠습니까 라는 메시지가 나오면 계속하기를 클릭해 설치를 진행한다.
    - 설치가 완료되면 지금 다시 시작을 클릭하여 Server를 재부팅한다.
  - 재부팅이 완료되면 DVD 장치를 제거하라는 메시지와 Enter를 누르라는 메시지가 나온다.
    - 가상머신 안에서 Enter를 누른다.
    - VMware가 자동으로 DVD장치를 제거해주는데 그렇지 않을 경우에는 직접 제거해준다.
  - ubuntu가 부팅 되면 초기 설정을 진행한다.
    - 우선 로그인 창에서 비밀번호를 입력하고 접속하게 되면 소프트웨어 업데이트, 온라인 계정 연결 등의 창이 뜨게 되는데 모두 skip한다.
    - 시작할 준비가 되었습니다 창에서 완료를 클릭한다.



- root 사용자 활성화하기

  - root를 활성화시키기
    - 바탕화면에서 마우스 우클릭 후 Open in Terminal을 선택해 터미널을 연다.
    - 윈도우의 명령 프롬프트와 비슷한 것이다.
    - 리눅스는 마우스를 사용하는 일반적인 GUI보다 TUI(Text User Interface)가 일반적이다.
    - 다음 명령어를 입력하여 리눅스 관리자인 root를 활성화시키고 비밀번호를 지정한다.

  ```bash
  $ sudo su
  $ passwd
  <비밀번호 입력>
  ```

  - 우측 상단의 네비바를 클릭하고 설정을 선택한 후 설정 창의 메뉴에서 사용자를 선택한다.
    - 사용자의 우측 상단에 있는 잠금 해제를 클릭하고 ubuntu 암호를 입력 후 인증을 클릭한다.
    - 자동 로그인의 끔을 클릭해서 켬으로 만든다.
  - custom.conf 수정
    - 다시 터미널을 겨서 아래 명령어를 입력한다.
    - nano는 텍스트 편집기다.
    - 중간쯤의 `AutomaticLogin`을 `root`로 변경하고 `security` 아랫 부분에 `AllowRoot=True`를 추가한다.
    - 편집이 완료되면 ctrl+X를 누른 후 Y와 Enter를 눌러 변경 내용을 저장한다.

  ```bash
  $ nano /etc/gdm3/custom.conf
  ```

  - gdm-password 수정
    - 3행(`auth required ~`)을 `#`으로 주석처리한다.
    - 마찬가지로 변경 내용을 저장하고 종류한다.

  ```bash
  $ nano /etc/pam.d/gdm-password
  ```

  - gdm-autologin 수정
    - 위에서 했던 것과 마찬가지로 nano 명령으로 파일을 열고 3행 앞에 #을 붙인다.
    - 변경 내용을 저장하고 종료한다.

  ```bash
  $ nano /etc/pam.d/gdm-autologin
  ```

  - 여기까지 진행하면 별도의 입력 없이 root 사용자로 자동 로그인된다.



- 소프트웨어 업데이트 기능 끄기

  - 소프트웨어 & 업데이트 클릭
    - 바탕화면 좌측 하단에서 프로그램 표시를 클릭하면 소프트웨어 & 업데이트 아이콘을 찾을 수 있다.
  - 소프트웨어 & 업데이트 창의 업데이트 탭에서 설정 변경
    - `[자동으로 업데이트 확인]`을 `하지 않기`로 설정
    - `[새 우분투 버전 알려주기]`를 `하지 않기` 로 설정
    - 닫기 클릭
  - 기존 소프트웨어 설치의 설정 파일 이름을 변경한다.
    - 터미널에 접속 후 다음 명령을 차례로 입력.

  ```bash
  $ cd /etc/apt
  # sources.list 파일 이름 변경
  $ mv sources.list sources.list.bak
  ```

  - 다음 명령으로 수정된 source.list를 다운 받는다.
    - `이것이 우분투 리눅스다`의 저자가 올려놓은 파일이다.
    - 만약 다운에 실패했다면 네트워크 문제일 수 있으므로 reboot 명령으로 재부팅하고 다시 진행한다.

  ```bash
  $ wget http://dw.hanbit.co.kr/ubuntu/20.04/sources.list
  ```

  - 설정한 내용 적용하기

  ```bash
  $ apt update
  ```




- IP 주소 변경하기

  - 서버에 고정 IP 할당하기

    - 우측 상단의 네비바를 클릭하고 `[유선 연결됨]`->`[유선 네트워크 설정]`을 선택한다.
    - `유선`-`연결됨-1000 Mb/s`칸에 있는 설정 버튼을 클릭하고 설정을 변경한다.
    - 케이블 연결 창에서 `IPv4 탭`을 선택하고 `IPv4 방식`을 수동으로 변경한다.
    - `주소` 에 `주소`는 192.168.111.100, 네트마스크에 255.255.255.0, 게이트웨이에 192.168.111.2를 입력한다.
    - `네임 서버(DNS)`부분에 192.168.111.2를 입력하고 네임서버 우측의 `자동`을 클릭해서 수동으로 변경한다.

    - `적용`을 클릭한다.

  - 재부팅하기

    - 터미널에서 `reboot` 명령을 실행하여 컴퓨터를 재부팅한다.
    - 재부팅이 완료되면 터미널에 `ip addr` 명령어로 네트워크에 위에서 설정한 내용이 적용되었는지 확인한다.
    - `ens32` 부분에 `inet`이 위에서 `주소`-`주소`에 설정한 대로(192.168.111.100) 나오면 제대로 설정 되었으면 된 것이다.



- 기타 설정

  - 화면 보호기 끄기
    - 설정에 들어가서 전원을 클릭한 후 절전의 빈 화면을 안함으로 선택한다.
  - 한글 키보드 설정
    - 설정 창에서 지역 및 언어를 선택하고 입력 소스에서 첫 번째 `한국어`의 삭제 아이콘을 클릭해 제거한다.
    - 즉 한글은 `한국어(Hangul)` 하나만 남아있으면 된다.
  - 터미널에서 한글 사용하기
    - 한/영 전환은 shift + space다.
  - 필수 패키지 설치하기
    - 아래 명령으로 필수 패키지를 설치한다.

  ```bash
  $ apt -y install net-tools
  ```

  - 방화벽 켜기
    - ufw는 우분투에서 제공하는 방화벽이다.

  ```bash
  $ ufw enable
  ```

  - 시스템 종료하기

  ```bash
  $ halt -p
  ```



- 마무리
  - VMPlayer를 실행시키고 Server_A의 CD/DVD설정을 변경한다.
    - connect at power on 체크 해제
    - Use phsical driver 체크
  - 설정 완료 된 Server_A를 스냅숏하기
    - 실행 중인 VMPlayer를 모두 종료한다.
    - VMPro를 실행한다.
    - `File`-`Open`을 클릭하고 Server_A를 저장한 폴더의 Server_A.vmx 파일을 선택한다.
    - `VM`-`Snapshot`-`Snapshot Manager`를 선택한다.
    - `Take Snapshot`을 클릭하고 Name을 `설정완료`로 입력한 후 `Take Snapshot`을 클릭한다.
    - `Close`를 입력하여 스냅숏을 완료한다.
    - `File`-`Close Tab`을 선택해서 `Server_A` 가상머신을 닫는다.
    - VMPro를 종료한다.





## ubuntu Server 설치하기

- 설치하기

  - player를 실행 후 VMware Workstation 15 Player 창에서 위에서 생성한 Server_B를 선택하고 Edit virtual machine settings를 클릭한다.
    - CD/DVD 탭에서 Browse를 클릭하고 Server용으로 다운 받은 파일(ubuntu-20.04.2-live-server-amd64.iso )을 선택후 OK를 클릭한다. 
    - connect at power on을 체크해야 한다.
  - Play virtual machine을 클릭하여 가상머신을 부팅한 뒤 설치를 진행한다.
    - 언어 선택에서는 English를 선택하고 enter를 누른다.
    - 전부 Done을 누른다.
    - Profile setup에서는 사용자명과 서버명, 비밀번호 등을 설정한다.
    - 중간에 나오는 것들은 전부 Done을 누른다.
    - 설정을 모두 완료하면 설치가 진행되는데 설치가 완료되면 하단에 Reboot가 활성화된다. 이를 선택하여 재부팅한다.
    - Server_A와 마찬가지로 DVD를 제거하라는 메시지가 출력되는데 VMware가 자동으로 제거해준다.
  



- 초기 설정
  - 처음 실행 시 로그인 하라는 메시지가 나오는데 위에서 설정한 유저명과 비밀번호를 입력하면 된다.
  - ubuntu 20.04의 초기 소프트웨어만 설치되도록 설정한다.
    - `이것이 우분투 리눅스다`의 저자가 올려놓은 파일을 다운 받는다.

  ```bash
  $ cd /etc/apt
  # 원본 파일을 백업파일로 변경
  $ sudo mv sources.list sources.list.bak
  # sources.list 다운
  $ sudo wget http://dw.hanbit.co.kr/ubuntu/20.04/sources.list
  # 새로 받은 파일로 설정
  $ sudo apt update
  ```

  - IP 변경하기
    - 수정을 완료하면 ctrl+x와 y, enter를 차례로 눌러 저장하고 종료한다.

  ```bash
  # 네트워크 장치 이름 확인(ens32가 기본값이다)
  $ ip addr
  
  # 관련 디렉터리로 이동 후 파일 편집
  $ cd /etc/netplan
  $ sudo nano 00-installer-config.yaml
  
  # 00-installer-config.yaml의 4행에 장치 이름, 5 행의 dhcp4:true는 자동으로 IP 주소를 할당 받는다는 의미이다.
  # 5행을 다음과 같이 수정 및 추가한다.
  network:
  	ethernets:
  		ens32:
  			dhcp4: no
  			addresses: [192.168.111.200/24]
  			gateway4: 192.168.111.2
  			nameservers:
  				addresses:[192.168.111.2]
  ```
  
  - root 계정 활성화
    - 활성화 한 뒤 재부팅하여 root 계정으로 로그인한다.
  
  ```bash
  $ sudo su - root
  $ passwd
  ```
  
  - IP 변경이 적용되었는지 확인.
    - 적용이 안됐다면 `reboot`를 통해 재부팅 후 확인한다.

  
  ```bash
  # ens32의 inet 부분이 설정한 대로 변경되었는지 확인한다.
  $ ip addr
  # 네트워크 정상 작동 확인
  $ ping -c 3 www.google.com
  ```
  
  - 방화벽 켜기
  
  ```bash
  $ ufw enable
  ```
  
  - 필수 패키지 설치
  
  ```bash
  $ apt -y install net-tools
  ```
  
  - 종료
  
  ```bash
  $ halt -p
  ```



- 마무리
  - 메모리 조정 및 DVD 제거
    - Player에서 Server_B의 설정으로 들어가 `Memory` 탭에서 메모리를 1024MB(==1GB)로 변경한다.
    - `CD/DVD` 탭에서 `Connect at power on`을 체크 해제하고, `Use physical drive`를 선택한다.
  - 스냅숏 생성하기
    - Pro를 실행하고 `File`-`open`을 클릭하여 Server_B가 저장된 폴더에서 `*.vmx`파일을 연다.
    - `VM`-`Snapshot`-`Snapshot Manager`를 선택한다.
    - `Take Snapshot`을 클릭하고 Name을 `설정완료`로 입력한 후 `Take Snapshot`을 클릭한다.
    - `Close`를 입력하여 스냅숏을 완료한다.
    - `File`-`Close Tab`을 선택해서 `Server_B` 가상머신을 닫는다.
    - VMPro를 종료한다.



## Clinet 설치하기

- kubuntu 설치하기
  - Client 가상 머신 설정 변경
    - `CD/DVD` 탭에서 탭에서 Browse를 클릭하고 Server용으로 다운 받은 파일(kubuntu-20.04.2.0-desktop-amd64.iso)을 선택후 OK를 클릭한다. 
    - connect at power on을 체크해야 한다.
    - 가상 머신을 부팅한다.
  - 설치하기
    - 부팅을 시작하면 kubuntu로고가 뜨면서 DVD의 이상 여부를 체크한다.
    - 완료되면 Welcome 창이 뜨는데 상단 바를 더블클릭하여 화면에 꽉 차도록 조정한다.
    - 언어는 한국어를 선택하고 `kubuntu 설치하기`를 클릭한다.
    - 그 뒤의 언어설정은 수정하지 말고 계속하기를 클릭한다.
    - 업데이트 및 기타 소프트웨어에서는 `일반 설치`를 선택하고 `Kubuntu 설치 중 업데이트 다운로드`를 체크 해제한다.
    - 다음 창에서도 아무 설정도 변경하지 않고 `지금 설치`를 클릭한다.
    - 국가와 시간대를 선택하고 이름, 사용자명, 비밀번호, 컴퓨터 이름을 설정하고 자동으로 로그인을 체크한다.
    - 설치가 완료되면 재부팅을 해야 하며 재부팅 할 때 DVD 장치를 제거하고 Enter를 누르라는 메시지가 나오는데 VMware가 자동으로 제거해주므로 Enter를 누른다.



- 초기 설정

  - 디스플레이 설정
    - 20.04 버전의 버그로 디스플레이 변경이 불가능하다.
    - 시스템 설정-디스플레이에서 변경하면 된다.
  - 20.04 LTS 초기 패키지 설치하기
    - Server에서 했던 것과 동일한 작업이다.
    - Konsole 터미널을 클릭하여 터미널을 열어 아래 명령어를 입력한다.

  ```bash
  $ cd /etc/apt
  $ sudo mv sources.list sources.list.bak
  $ sudo wget http://dw.hanbit.co.kr/ubuntu/20.04/sources.list
  $ sudo apt update
  $ sudo apt -y install net-tools
  # 터미널 닫기
  $ exit
  ```

  - 화면 보호기 끄기
    - `시스템 설정-전원관리-에너지 절약`에서 `화면 에너지 절약`을 체크 해제한다.
  - 한글 입력 확인
    - 터미널에서 ctrl+space를 눌러 한영을 전환하고 한글을 써본다.
  - `halt -p`를 입력하여 종료한다.



- 마무리
  - DVD를 제거하고 메모리를 조절한다.
  - 스냅숏을 만든다.





## Windows Client 설치

> https://www.microsoft.com/ko-kr/evalcenter/evaluate-windows-10-enterprise

- 윈도우 평가판 다운로드
  - 위 사이트에서 윈도우 평가판을 다운로드한다.
  - 만일 이미 평가판을 사용했거나 기간이 다 된 경우 사용하는 컴퓨터가 윈도우라면 그냥 사용중인 컴퓨터로 진행해도 된다.



- 설치하기
  - 그 동안 했던 것과 동일한 방식으로 window10 설치를 진행한다.
  - 설치 선택 화면에서 고급 설치를 선택한다.
    - 그 밖의 옵션은 모두 기본으로 두고 다음을 클릭하여 설치한다.



- 마무리
  - 역시 마찬가지로 CD/DVD에서 ISO 파일을 제거하고 스냅숏을 생성한다.
  - WinClient는 설치 완료 후에 VMware Tools를 설치하는 것이 좋다.
    - WinClient의 가상머신을 실행시킨 상태에서 메뉴의 Player-Manager-Install VMware Tools를 선택하면 자동으로 설치된다.
    - 만일 자동으로 설치되지 않는다면 가상머신의 파일 탐색기에서 D:\ 폴더에 있는 setup.exe를 실행한다.
    - VMware Tools는 가상머신에 여러 가지 드라이버 파일을 설치해서 VMware 안에 설치된 Windows를 부드럽게 사용하도록 도와준다.
