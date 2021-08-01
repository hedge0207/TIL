# AWS EC2 인스턴스 생성하기

> https://aws.amazon.com/ko/

- EC2(Elastic Compute Cloud)
  - AWS에서 제공하는 가상 서버
  - 인스턴스는 운영체제가 포함된 가상 서버를 뜻한다.



- 인스턴스 생성
  - 위 사이트에 접속 후 회원가입
    - 회원가입시에 카드 등록을해야 하는데 해외 결제가 가능한 VISA나 MASTER 카드를 사용하는 것이 좋다.
    - VISA나 MASTER 이외의 카드는 결제가 정상적으로 이루어지지 않을 수 있기 때문이다,

  - EC2 대시보드에 접근 후 AMI(Amazon Machine Image)를 선택한다.
    - AMI는 서버 운영에 필요한 운영체제와 여러 소프트웨어가 조합된 템플릿이다.
    - 프리티어로 사용 가능한 템플릿을 선택한다.
    - Amazon Linux 2 AMI는 Amazon에서 직접 만든 템플릿으로 EC2 성능에 최적화 되어 있다.
  - 인스턴스 유형 선택하기
    - 인스턴스 유형이란 EC2 인스턴스 서버의 CPU, 메모리, 네트워크 성능과 같은 서버 스펙을 뜻한다.
    - 역시 프리티어가 가능한 유형을 선택한다.
  - 키 페어 생성하기
    - 인스턴스 검토 후 시작하기 버튼을 누르면 키 페어 설정 화면으로 넘어가게 된다.
    - 이전에 사용하던 키 페어가 있다면 해당 키 페어를 사용하고 없다면 원하는 이름으로 지정 후 키 페어를 생성한다.



- 보안 그룹 설정하기
  - Inbound
    - 발급받은 인스턴스 외부로 부터 들어오는 트래픽을 뜻한다.
    - 기본 설정은 ssh(22번 포트)만 가능하도록 되어있다,
  - Outbound
    - 인스턴스로부터 나가는 트래픽을 뜻한다.
    - 기본 설정은 모든 IP, port가 접속 가능하도록 되어 있다.
  - 필요한대로 Inbound와 Outbound를 설정하면 된다.



# 인스턴스에 접속하기

- ssh 명령어로 접속하기

  - ssh는 네트워크 상의 다른 컴퓨터에 접속할 때 사용하는 명령어이다.
  - 발급받은 EC2 인스턴스에 접속하려면 `-i` 옵션을 사용하여 위에서 생성한 키 페어를 프라이빗 키로 추가해야 한다.
  - Amazon Linux 2 AMI의 기본 사용자명은 ec2-user이고, 퍼블릭 IP는 EC2 대시보드에서 확인이 가능하다.

  ```bash
  $ ssh -i <발급 받은 key 페어 파일명> ec2-user@<퍼블릭 IP>
  ```




- putty로 접속하기

  - ssh 명령이 설치되어 있지 않은 운영체제에서는 putty를 통해 접속할 수 있다.
    - putty는 서버에 접속하기 위한 프로그램으로 원격으로 접속하기 위한 여러 명령어를 GUI로 제공한다.
  - Putty key generator를 통해 key 페어를 ppk(Putty Private Key) 파일로 변환하는 과정이 필요하다.
    - putty key generator를 실행한 후 `type of key to generate`는 RSA를 선택하고, Actions-Load를 클릭하여 키 페어 파일을 선택한다.
    - 그럼 `Save private key` 버튼이 활성화되는데 해당 버튼을 눌러 ppk파일로 변환된 키 페어를 저장한다.
  - putty를 실행 후 Session탭에서 IP와 Port를 입력 후 connection type은 ssh를 선택한다.
    - 이후 `Connection SSH AUTH` 탭으로 이동하여 생성된 ppk 키 페어를 `Private key file for authentication` 아래 Browse를 눌러 추가해주면 된다.
    - 이제 Open 버튼을 누르면 인스턴스 접속이 시작되고 터미널이 실행된다.
  - login as에 Amazon Linux 2 AMI의 기본 유저명인 ec2-user를 입력하면 인스턴스 접속이 완료된다. 



- VSCode에서 접속하기
  - Remote - SSH extension 설치
  - config 파일에 다음과 같이 입력

  ```bash
  Host <호스트명>
      HostName <퍼블릭 IP>
      User <User 명>
      IdentityFile <pem 파일 경로>
  ```

  - `프로세스에서 없는 파이프에 쓰려고 했습니다` 에러가 발생할 경우
    - known_hosts 파일을 삭제 후 VScode도 재실행한다.
    - 이후 다시 접속한다.

