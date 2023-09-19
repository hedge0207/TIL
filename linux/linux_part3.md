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

  - `reload`
    - Service와 관련된 설정 file들을 reload한다.
    - 이는 unit file(`.service` file)을 reload하는 것이 아니라는 것에 주의해야한다.
    - 예를 들어 `systemctl reload apache`라는 명령어는 `apache.service` file을 reload하는 것이 아니라 `httpd.conf` 같은 apache에서 사용하는 configuration file을 reload한다.

  ```bash
  $ systemctl reload <서비스명>
  ```

  - 등록된 service를 실행한다.

  ```bash
  $ systemctl start <서비스명>
  ```

  - service를 정지한다.

  ```bash
  $ systemctl stop <서비스명>
  ```

  - 실행중인 service를 재시작한다.

  ```bash
  $ systemctl restart <서비스명>
  ```

  - 특정 서비스의 상태 확인

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