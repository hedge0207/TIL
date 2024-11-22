# 컨테이너와 Docker

## 개요

- Docker 개요
  - 애플리케이션의 실행에 필요한 환경을 하나의 이미지로 모아두고, 그 이미지를 사용하여 다양한 환경에서 애플리케이션 실행 환경을 구축 및 운용하기 위한 플랫폼이다.
    - 내부에서 컨테이너 기술을 사용한다.
    - 오픈 소스다.
  - Docker를 사용하는 이유
    - 개발을 하다 보면 개발 환경, 테스트 환경에서는 정상적으로 동작하는데, 스테이징 환경(제품 환경에 배포하기 직전에 확인하는 테스트 환경), 제품 환경에서는 동작하지 않는 경우가 존재한다.
    - 위와 같은 현상의 원인에는 여러 가지가 있지만, 그 중 대표적인 것이 각 환경별로 인프라가 다르기 때문이다.
    - 도커는 애플리케이션 실행에 필요한 모든 인프라를 컨테이너로 모아 각 환경에서 해당 컨테이너를 사용함으로써 인프라가 달라서 발생하는 문제를 방지하는 데 목적이 있다.



- 컨테이너
  - 호스트 OS상에 논리적인 구획(컨테이너)을 만들고, 애플리케이션을 작동시키기 위해 필요한 라이브러리나 애플리케이션 등을 하나로 모아, 별도의 서버인 것처럼 사용할 수 있게 만든 것.
    - 즉 앱이 구동되는 환경까지 감싸서 실행할 수 있도록 하는 격리 기술이다.
  - 호스트 OS의 리소스를 논리적으로 분리시키고, 여러 개의 컨테이너가 공유하여 사용한다.
    - 보통 물리 서버 상에 설치한 호스트 OS의 경우 하나의 OS 상에서 움직이는 여러 애플리케이션은 똑같은 시스템 리소스를 사용한다.
    - 이때 작동하는 여러 애플리케이션은 데이터를 저장하는 디렉토리를 공유하고, 서버에 설정된 동일한 IP 주소로 통신을 한다.
    - 따라서 여러 애플리케이션에서 사용하고 있는 미들웨어나 라이브러리의 버전이 다른 경우에는 각 애플리케이션이 서로 영향을 받지 않도록 주의해야 한다.
    - 이에 반해 컨테이너 기술을 사용하면 OS나 디렉토리, IP 주소 등과 같은 시스템 자원을 마치 각 애플리케이션이 점유하고 있는 것처럼 보이게 할 수 있다.
  - 컨테이너 런타임
    - 컨테이너를 다루는 도구를 컨테이너 런타임이라 한다.
    - Docker는 대표적인 컨테이너 런타임 중 하나이다.
    - Docker의 컨테이너 규격은 표준화되어 있기 때문에 Docker가 아닌 다른 컨테이너 런타임들도 Docker로 만든 컨테이너를 사용할 수 있다.



- 가상화와 컨테이너

  > [그림 출처](https://kubernetes.io/ko/docs/concepts/overview/#%EC%97%AC%EC%A0%95-%EB%8F%8C%EC%95%84%EB%B3%B4%EA%B8%B0)

  ![Container_Evolution](https://kubernetes.io/images/docs/Container_Evolution.svg)

  - 전통적인 배포 방식
    - 가상화나 컨테이너가 등장하기 전의 전통적인 배포 방식이다.
    - 여러 개의 애플리케이션을 물리 서버에서 실행했다.
    - 물리 서버에서 여러 애플리케이션의 리소스 한계를 제한할 방법이 없었기에, 리소스 할당에 문제가 발생했다.
    - 예를 들어 한 애플리케이션이 대부분의 리소스를 사용하게 되면, 다른 애플리케이션이 리소스를 적게 할당 받아 성능이 떨어지는 문제 등이 발생했다.
    - 이를 해결하기 위한 방법으로 여러 대의 물리 서버를 구축하는 방법이 있었지만, 비용이 많이 든다는 문제가 있었다.
  - 가상화된 배포 방식
    - 전통적인 배포 방식의 문제점을 해결하기 위해 가상화가 도입되었다.
    - 단일 물리 서버의 CPU에서 여러 가상 시스템(Virtual Machine)을 실행할 수 있게 하는 기술이다.
    - 하이퍼바이저는 하나의 시스템 상에서 가상 컴퓨터를 여러 개 구동할 수 있도록 해주는 중간 계층이다.
    - 위 그림에서 `Bin/Library`는 프로그램이 실행되는데 필요한 환경과 관련된 파일을 나타낸다.
    - 각 VM은 가상화된 하드웨어 상에서 자체 OS를 포함한 모든 구성 요소를 실행하는 하나의 완전한 machine(컴퓨터)이다.
    - 따라서 컴퓨터에 CPU, memory 등을 장착하듯 가상머신에도 CPU, memory, storage 등을 개별적으로 할당할 수 있다.
    - 가상화를 사용하면 VM간에 애플리케이션을 격리하고, 애플리케이션의 정보를 다른 애플리케이션에서 자유롭게 접근할 수 없으므로 어느 정도의 보안성도 제공할 수 있다.
    - 물리 서버의 리소스를 보다 효율적으로 활용할 수 있으며, 하드웨어 비용을 절감할 수 있어 확장성도 높았다.
    - 전통적 배포 방식 보다는 효율적이지만, VM은 완전한 machine이므로 일일이 운영체제 설치 등의 세팅이 필요했기에 컨테이너 중심의 배포 보다는 복잡한 편이다.
  - 컨테이너 배포 방식
    - VM과 유사하지만 격리 속성을 완화하여 애플리케이션 간에 OS를 공유하므로, VM과 달리 프로그램 구동을 위해서 OS를 매번 설치할 필요가 없다.
    - VM과 마찬가지로 컨테이너에는 자체 파일 시스템, CPU 점유율, 메모리, 프로세스 공간 등이 있다.
    - 컨테이너는 "이 컴퓨터에서 자신만 구동되고 있다"고 판단할 수 있도록 각 컨테이너 사이에 간섭을 일으킬 수 없는 장벽을 친다.
    - 또한 OS는 각 컨테이너가 사용할 수 있는 CPU, memory 등의 자원 또한 독립적으로 사용할 수 있도록 할당하고 관리한다.
    - 모든 컨테이너가 같은 OS를 공유하므로, 컨테이너에서 실행 중인 프로그램이 OS에 문제를 발생시킬 경우, OS에서 구동 중인 모든 컨테이너에 문제가 생길 수 있다.



- Docker의 기능
  - Docker 이미지
    - 애플리케이션의 실행에 필요한 파일들이 저장된 디렉토리.
    - 실행 환경에서 움직이는 컨테이너의 바탕이 된다.
    - Docker에서는 하나의 이미지에는 하나의 애플리케이션만 넣어 두고, 여러 개의 컨테이너를 조합하여 서비스를 구축하는 방법을 권장하고 있다.
    - Docker 이미지는 겹쳐서 사용이 가능하다. 예를 들어 OS용 이미지에 웹 애플리케이션용 이미지를 겹쳐서 다른 새로운 이미지를 만들 수 있다.
  - 이미지를 만드는 기능(Build)
    - 애플리케이션의 실행에 필요한 라이브러리, 미들웨어, OS나 네트워크 설정 등을 하나로 모아서 Docker 이미지를 만든다.
    - Docker 이미지는 실행 환경에서 움직이는 컨테이너의 바탕이 된다.
    - Docker의 이미지는 Docker의 명령을 사용하여 수동으로 만들 수도 있으며, Dockerfile이라는 설정 파일을 만들어 그것을 바탕으로 자동으로 이미지를 만들 수도 있다.
    - 지속적인 인티그레이션과 지속적 딜리버리의 관점에서 코드에 의한 인프라의 구성 관리를 생가갛면 Dockerfile을 사용하여 관리하는 것이 바람직하다.
  - Docker 이미지를 공유하는 기능(Ship)
    - Docker 이미지는 Docker 레지스트리에서 공유가 가능하다.
    - Docker의 공식 레지시트리인 Docker Hub에서는 다양한 베이스 이미지들이 존재한다.
    - Docker Hub는 github이나 bitbucket과 연계하여 사용하는 것이 가능하다.
    - 예를 들어 깃헙 상에서 Dockerfile을 관리하고, 거기서 Docker 이미지를 자동으로 생성하여 Docker Hub에서 공개하는 것도 가능(Automated Build)하다.
  - Docker 컨테이너를 작동시키는 기능
    - Docker는 Linux 상에서 컨테이너 단위로 서버 기능을 작동시킨다.
    - 이 컨테이너의 바탕이 되는 것이 Docker 이미지로, Docker 이미지만 있으면 Docker가 설치된 환경이라면 어디서든 컨테이너를 작동시킬 수 있다.
    - Docker 이미지를 가지고 여러 개의 컨테이너를 가동시킬 수도 있다.



- Docker 컴포넌트
  - Docker는 아래와 같은 컴포넌트로 구성되어 있다.
    - 핵심 기능이 되는 Docker engine을 중심으로 컴포넌트를 조합하여 애플리케이션 실행 환경을 구축한다.
  - Docker Engine(Docker의 핵심 기능)
    - Docker 이미지를 생성하고 컨테이너를 기동시키기 위한 Docker의 핵심 기능.
    - Docker 명령의 실행이나 Dockerfile에 의한 이미지도 생성한다.
  - Docker Registry(이미지 공개 및 공유)
    - 컨테이너의 바탕이 되는 Docker 이미지를 공개 및 공유하기 위한 레지스트리 기능.
    - Docker의 공식 레지스트리 서비스인 Docker Hub도 이 Docker Registry를 사용하고 있다.
  - Docker Compose(컨테이너 일원 관리)
    - 여러 개의 컨테이너 구성 정보를 코드로 정의하고, 명령을 실행함으로써 애플리케이션의 실행 환경을 구성하는 컨테이너들을 일원 관리하기 위한 툴.
  - Docker Machine(Docker 실행 환경 구축)
    - 로컬 호스트용인 VirtualBox를 비롯하여 AWS EC2나 Azure와 같은 클라우드 환경에 Docker의 실행 환경을 명령으로 자동 생성하기 위한 툴이다.
  - Docker Swarm(클러스터 관리)
    - 여러 Docker 호스트를 클러스터화하기 위한 툴이다.
    - Docker Swarm에서는 클러스터를 관리하거나 API를 제공하는 역할은 Manager가, Docker 컨테이너를 실행하는 역할은 Node가 담당한다.
    - 오픈소스인 Kubernetes도 사용 가능하다.







## Docker의 작동 구조

- Docker는 리눅스 커널의 기술이 베이스로 되어 있다.



- 컨테이너를 구획화하는 장치(namespace)
  - 컨테이너라는 독립된 환경을 만들고, 그 컨테이너를 구획화하여 애플리케이션의 실행 환경을 만든다.
  - 컨테이너를 구획화하는 기술은 리눅스 커널의 namespace라는 기능을 사용한다.
    - namespace란 한 덩어리의 데이터에 이름을 붙여 분할함으로써 충돌 가능성을 줄이고, 쉽게 참조할 수 있게 하는 개념이다.
    - 이름과 연결된 실체는 그 이름이 어떤 namespace에 속해 있는지 고유하게 정해진다.
    - 따라서 namespace가 다르면 동일한 이름이라도 다른 실체로 처리된다.
  - 리눅스 커널의 namespace 기능은 리눅스의 오브젝트에 이름을 붙임으로써 다음과 같은 6개의 독립된 환경을 구축할 수 있다.
    - PID namespace: PID란 리눅스에서 각 프로세스에 할당된 고유한 ID를 말한다. PID namespace는 PID와 프로세스를 격리시키며, namespace가 다른 프로세스끼리는 서로 엑세스 할 수 없다.
    - Network namespace: 네트워크 디바이스, IP 주소, 포트 번호, 라우팅 테이블, 필터링 테이블 등과 같은 네트워크 리소스를 격리된 namespace마다 독립적으로 가질 수 있다. 이 기능을 사용하면 호스트 OS 상에서 사용 중인 포트가 있더라도 컨테이너 안에서 동일한 번호의 포트를 사용할 수 있다.
    - UID namespace: UID(사용자 ID), GID(그룹 ID)를 namespace별로 독립적으로 가질 수 있다. namespace 안과 호스트 OS 상의 UID,GID가 서로 연결되어 namespace 안과 밖에서 서로 다른 UID,GID를 가질 수 있다.
    - MOUNT namespace: 리눅스에서 파일 시스템을 사용하기 위해서는 마운트가 필요하다. 마운트란 컴퓨터에 연결 된 기기나 기억 장치를 OS에 인식시켜 이용 가능한 상태로 만드는 것을 말한다. MOUNT namespace는 마운트 조작을 하면 namespace 안에 격리된 파일 시스템 트리를 만든다.
    - UTS namespace: namespace별로 호스트명이나 도메인명을 독자적으로 가질 수 있다.
    - IPC namespace:  프로세스 간의 통신(IPC) 오브젝트를 namespace별로 독립적으로 가질 수 있다.



- 릴리스 관리 장치(cgroups)

  - Docker에서는 물리 머신 상의 자원을 여러 컨테이너가 공유하여 작동한다.

    - 이 때 리눅스 커널의 기능인 control groups 기능을 사용하여 자원의 할당 등을 관리한다.

  - 리눅스에서는 프로그램을 프로세스로서 실행한다.

    - 프로세스는 하나 이상의 스레드 모음으로 움직인다.
    - cgroups는 프로세스와 스레드를 그룹화하여, 그 그룹 안에 존재하는 프로세스와 스레드에 대한 관리를 수행하기 위한 기능이다.
    - 컨테이너 안의 프로세스에 대해 자원을 제한함으로써 특정 컨테이너가 호스트 OS의 자원을 모두 사용해 버려서 동일한 호스트 OS 상에서 가동되는 다른 컨테이너에 영향을 주는 일을 막을 수 있다.

  - cgroups으로 관리할 수 있는 사항들

    | 항목    | 설명                             |
    | ------- | -------------------------------- |
    | cpu     | CPU 사용량 제한                  |
    | cpuacct | CPU 사용량 통계 정보 제공        |
    | cpuset  | CPU나 메모리 배치 제어           |
    | memory  | 메모리나 스왑 사용량 제한        |
    | devices | 디바이스에 대한 액세스 허가/거부 |
    | freezer | 그룹에 속한 프로세스 정지/재개   |
    | net_cls | 네트워크 제어 태그를 부가        |
    | blkio   | 블록 디바이스 입출력량 제어      |

  - cgroups는 계층 구조를 사용하여 프로세스를 그룹화형 관리할 수 있다.



- 네트워크 구성(가상 브리지/가상 NIC)
  - 리눅스는 도커를 설치하면 서버의 물리 NIC가 docker0라는 가상 브리지 네트워크로 연결된다.
    - docker0는 Docker를 실행시킨 후에 디폴트로 만들어진다.
    - Docker 컨테이너가 실행되면 컨테이너에 172.17.0.0/16이라는 서브넷 마스크를 가진 프라이빗 IP 주소가 eth0으로 자동으로 할당된다.
    - 이 가상 NIC는 OSI 참조 모델의 레이어 2인 가상 네트워크 인터페이스로, 페어인 NIC와 터널링 통신을 한다.
  - NAPT(Network Address Port Translation)
    - Docker 컨테이너와 외부 네트워크가 통신을 할 때는 가상 브리지 docker0와 호스트 OS의 물리 NIC에서 패킷을 전송하려는 장치가 필요하다.
    - Docker에서는 NAPT 기능을 사용하여 연결한다.
    - NAPT란 하나의 IP 주소를 여러 컴퓨터가 공유하는 기술로, IP 주소와 포트 번호를 변환하는 기능이다.
    - 프라이빗 IP 주소와 글로벌 IP 주소를 투과적으로 상호 변환하는 기술로, TCP/IP의 포트 번호까지 동적으로 변환하기 때문에 하나의 글로벌 IP 주소로 여러 대의 머신이 동시에 연결할 수 있다.
    - Docker에서는 NAPT에 리눅스의 iptables를 사용하고 있다.



- Docker 이미지의 데이터 관리 장치
  - Copy on Write
    - 어떤 데이터를 복사할 필요가 생겼을 때는 새로운 빈 영역을 확보하고 거기에 복사를 한다.
    - 만일 복사한 데이터에 변경이 없었다면 그 복사는 불필요한 것이 된다.
    - 복사한 데이터의 용량이 크면 클수록 쓸데없는 낭비가 발생한다.
    - 만일 바로 복사하지 않고 원래의 데이터를 그대로 참조시켜, 원본 또는 복사 중 한 쪽에 수정이 발생한 시점에 새로운 빈 영역을 확보하고 데이터를 복사한다면 이러한 낭비를 막을 수 있다.
    - 위와 같은 방식을 Copy on Write라고 부른다.
    - Docker는 Copy on Write 방식으로 컨테이너의 이미지를 관리한다.
  - AUFS
    - 다른 시스템의 파일이나 디렉토리를 투과적으로 겹쳐서 하나의 파일 트리를 구성할 수 있는 파일 시스템이다.
  - Btrfs
    - 리눅스용 Copy on Write 파일 시스템.
    - 과거의 상태로 돌아갈 수 있는 롤백 기능이나 어떤 시점에서의 상태를 저장할 수 있는 스냅샷 기능을 갖고 있다.
  - Device Mapper
    - 리눅스의 블록 디바이스 드라이버와 그것을 지원하는 라이브러리들이다.
    - 파일 시스템의 I/O와 디바이스의 매핑 관계를 관리한다.
  - OverlayFS
    - UnionFS 중 하나로, 파일 시스템에 다른 파일 시스템을 투과적으로 머징하는 장치이다.
  - ZFS
    - 볼륨 관리, 스냅샷, 체크섬 처리, 리플리케이션 등을 지원하는 파일 시스템. 



- Docker는 컨테이너를 독립된 공간으로 관리한다.
  - Docker는 하나의 Linux 커널을 여러 개의 컨테이너에서 공유하고 있다.
  - 컨테이너 안에서 작동하는 프로세스를 하나의 그룹으로 관리하고, 그룹마다 각각 파일 시스템이나 호스트명, 네트워크 등을 할당하고 있다.
  - 그룹이 다르면 프로세스나 파일에 대한 엑세스를 할 수 없다.
  - 이러한 구조를 활용하여 컨테이너를 독립된 공간으로 관리한다.



- Docker Content Trust(DCT)

  - 도커 이미지의 위장이나 변조 방지

    - 도커에는 인프라 구성이 포함되기 때문에 제삼자가 악의적으로 이미지를 위장하거나 변조하지 못하도록 이미지를 보호해야 한다.

    - DCT를 활용하여 보호가 가능하다.

  - 서명

    - 이미지 작성자가 Docker 레지스트리에 이미지를 업로드하기 전에 로컬 환경에서 이미지 작성자의 비밀키를 사용하여 이미지에 서명한다.
    - 이 비밀 키를 Offline Key라고 한다.
    - 이 키는 보안상 매우 중요한 키이므로 엄중하게 관리할 필요가 있다.

  - 검증

    - 서명이 된 이미지를 다운로드 할 때 이미지 작성자의 공개키를 사용하여 이미지가 진짜인지 아닌지를 확인한다.
    - 만일 변조된 경우에는 그 이미지를 무효로 만든다.
    - 이 공개키를 Tagging Key라고 한다.

  - DCT 기능 유효화하기

    - 아래와 같이 작성한 후 이미지를 받아보면, 다운 받은 이미지에 대한 검증이 발생하는 것을 확인 가능하다.
    - 서명이 되어있지 않은 이미지를 사용하면 오류가 발생한다.

  ```bash
  # 아래 명령어에서 1만 0으로 변경하면 무효화하는 명령어이다.
  $ export DOCKER_CONTENT_TRUST=1
  ```





# Docker image

> https://www.44bits.io/ko/post/how-docker-image-work

- Docker image pull 받기

  - `docker pull python:3.9.0`을 실행하면 아래와 같이 출력된다.

  ```bash
  $ docker pull python:3.9.0
  3.9.0: Pulling from library/python
  756975cb9c7e: Pull complete 
  d77915b4e630: Pull complete 
  5f37a0a41b6b: Pull complete 
  96b2c1e36db5: Pull complete 
  c495e8de12d2: Pull complete 
  33382189822a: Pull complete 
  414ebfa5f45b: Pull complete 
  dd860911922e: Pull complete 
  b434dcf770b1: Pull complete 
  Digest: sha256:387f88e770ef8bbce23e57bc7627f71bde1d32888b3f08a857308444c3d29226
  Status: Downloaded newer image for python:3.9.0
  docker.io/library/python:3.9.0
  ```

  - Docker image의 이름은 docker registry에서는 `<namepsace>/<image_name>:<tag>`의 형식으로 저장된다.
    - 즉 `docker pull python:3.9.0`과 같이 입력하면, docker hub에서는 `docker.io/library/python:latest`라는 image를 찾는다.
    - `docker.io`는 docker hub에서 찾겠다는 것이고 `library`는 docker hub에서 공식 image들을 저장하는 namepsace이다.
  - 따로 namespace를 지정하지 않았는데도, docker hub에서 image를 찾는 이유는 Docker의 기본 registry가 docker hub이기 때문이다.
    - 아래와 같이 확인이 가능하다.

  ```bash
  $ docker info | grep Registry
  # Registry: https://index.docker.io/v1/
  ```

  - 또한 image를 pull 받을 때 sha256 digest 값이 있는 것을 확인할 수 있는데, 이 값을 가지고도 image를 pull 받을 수 있다.
    - 예를 들어 python:3.9.0 image를 받으면 아래와 같이 출려된다.

  ```bash
  Digest: sha256:387f88e770ef8bbce23e57bc7627f71bde1d32888b3f08a857308444c3d29226
  ```

  - 즉 아래의 5가지 주소는 모두 같은 이미지를 가리킨다.
    - `python:3.9.0`
    - `pythpn@sha256:387f88e770ef8bbce23e57bc7627f71bde1d32888b3f08a857308444c3d29226`
    - `library/python:3.9.0`
    - `docker.io/library/python:3.9.0`
    - `index.docker.io/library/python:3.9.0`



- Docker image

  - Docker image는 여러 개의 레이어들로 구성되어 있다.
    - Image를 pull 받으면 레이어들이 독립적으로 저장되며, 컨테이너를 실행할 때 이 레이어들을 차례로 쌓아올려서 특정 위치에 마운트한다.
    - 또한 이미지를 구성하는 레이어들은 읽기 전용이기에 절대 변하지 않는다.
    - 모든 레이어를 쌓아올린 뒤에 마지막으로 컨테이너 전용으로 쓰기가 가능한 레이어를 한 층 더 쌓고, 컨테이너에서 일어나는 모든 변경사항을 해당 레이어에 저장한다.
    - 컨테이너를 삭제하면 변경 사항들이 모두 날아가는 것은 이 때문으로, 모든 변경사항이 컨테이너 전용 레이어에 쌓이기 때문에, 컨테이너가 삭제되면 해당 레이어도 함께 삭제되기 때문이다.
  - Container layer는 어디 저장되는가?
    - 아래와 같이 container layer가 어디에 저장되는지를 알 수 있다.
    - `GraphDriver.Data.UpperDir`의 경로가 바로 container layer가 저장되는 경로다.

  ```bash
  $ docker inspect <container>
  ```

  - Dockerfile의 모든 명령어가 layer를 생성하는 것은 아니다.
    - `CMD`, `LABEL`, `ENV`, `EXPOSE` 등의 metadata를 다루는 부분은 레이어로 저장되지 않는다.
    - `ADD`나 `RUN` 등이 일어나는 겨우에만 layer로 저장된다.
    - 예를 들어 `python:3.9.0` image는 아래와 같이 다양한 과정을 거쳐 image가 생성되지만, 이 중에서 실제 layer를 생성하는 과정은  일부 뿐이다.

  ```bash
  $ docker history python:3.9.0
  
  IMAGE          CREATED       CREATED BY                                      SIZE      COMMENT
  0affb4652fc0   2 years ago   /bin/sh -c #(nop)  CMD ["python3"]              0B        
  <missing>      2 years ago   /bin/sh -c set -ex;   wget -O get-pip.py "$P…   7.3MB     
  <missing>      2 years ago   /bin/sh -c #(nop)  ENV PYTHON_GET_PIP_SHA256…   0B        
  <missing>      2 years ago   /bin/sh -c #(nop)  ENV PYTHON_GET_PIP_URL=ht…   0B        
  <missing>      2 years ago   /bin/sh -c #(nop)  ENV PYTHON_PIP_VERSION=20…   0B        
  <missing>      2 years ago   /bin/sh -c cd /usr/local/bin  && ln -s idle3…   32B       
  <missing>      2 years ago   /bin/sh -c set -ex   && wget -O python.tar.x…   57.2MB    
  <missing>      2 years ago   /bin/sh -c #(nop)  ENV PYTHON_VERSION=3.9.0     0B        
  <missing>      2 years ago   /bin/sh -c #(nop)  ENV GPG_KEY=E3FF2839C048B…   0B        
  <missing>      2 years ago   /bin/sh -c apt-get update && apt-get install…   17.9MB    
  <missing>      2 years ago   /bin/sh -c #(nop)  ENV LANG=C.UTF-8             0B        
  <missing>      2 years ago   /bin/sh -c #(nop)  ENV PATH=/usr/local/bin:/…   0B        
  <missing>      2 years ago   /bin/sh -c set -ex;  apt-get update;  apt-ge…   510MB     
  <missing>      2 years ago   /bin/sh -c apt-get update && apt-get install…   146MB     
  <missing>      2 years ago   /bin/sh -c set -ex;  if ! command -v gpg > /…   17.5MB    
  <missing>      2 years ago   /bin/sh -c apt-get update && apt-get install…   16.5MB    
  <missing>      2 years ago   /bin/sh -c #(nop)  CMD ["bash"]                 0B        
  <missing>      2 years ago   /bin/sh -c #(nop) ADD file:9a4fd72d749f4a791…   114MB
  ```

  - Docker image는 어디에 저장되는가?

    > Ubuntu 22.04 LTS, Docker 20.10.22 기준

    - `docker info | grep Storage`를 통해 확인해보면 `Storage Driver: overlay2`와 같이 나오는 것을 확인할 수 있다.
    - Docker의 데이터는 기본적으로 `/var/lib/docker`에 저장되며, overlay2로 저장된 레이어 데이터는 다시 `image/overlay2/layerdb/sha256`에 저장된다.

    - `docker image inspect python:3.9.0`을 입력하고 `Layers` 부분을 확인해보면, `/var/lib/docker/image/overlay2/layerdb/sha256` 디렉토리에 동일한 directory들이 생성되어 있는 것을 볼 수 있다.

  - 중간 layer를 가지고 container를 실행시킬 수 있는가?

    - 1.1 version 이전에서는 image와 layer가 명확히 구분되지 않아 가능했다.
    - 그러나 이후 version부터는 image와 layer를 명확히 구분하면서, 중간 단계의 layer로 container를 실행시키는 것이 매우 복잡해졌다.

  - Docker image가 만들어지는 기본적인 원리

    - 앞서 말했듯 Docker image는 계층적 구조를 가지고 있으며, image를 가지고 container 생성시, container는 쓰기가 가능한 layer를 최상단에 추가한다.
    - 또한 container에 변경사항이 생기면 container가 생성한 layer에 변경 사항이 추가된다.
    - 이렇게 변경 사항이 적용된 layer를 `docker commit` 명령어를 통해 commit하여 읽기 전용 layer로 만든 후, 이를 기존 image에 쌓아 새로운 image를 만들게 된다.
    - 따라서 Docker image를 build할 때는 이 점을 고려하여 순서를 정해야한다.



- Docker container로 Docker image 생성하기

  - Ubuntu image를 pull 받는다.

  ```bash
  $ docker pull ubuntu:20.04
  ```

  - `ubuntu:20.04` image의 history는 아래와 같다.

  ```bash
  $ docker history ubuntu:20.04
  IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
  d5447fc01ae6   6 months ago   /bin/sh -c #(nop)  CMD ["bash"]                 0B        
  <missing>      6 months ago   /bin/sh -c #(nop) ADD file:9d282119af0c42bc8…   72.8MB
  ```

  - 위에서 받은 이미지를 기반으로 container를 생성하고,  `apt`를 update 한다.

  ```bash
  $ docker run --name layer-container ubuntu:20.04 /bin/bash -c 'apt-get update'
  ```

  - `apt`를 업데이트 한 container를 commit 한다.

  ```bash
  $ docker commit layer-container ubuntu:apt-update
  ```

  - 새로 생성된 `ubuntu:apt-update` image의 history를 확인한다.
    - 기존과 달리 새로운 layer가 추가된 것을 확인할 수 있다.

  ```bash
  $ docker history ubuntu:apt-update
  IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
  ffcac381da1a   50 seconds ago   /bin/bash -c apt-get update                     44.2MB    
  d5447fc01ae6   6 months ago     /bin/sh -c #(nop)  CMD ["bash"]                 0B        
  <missing>      6 months ago     /bin/sh -c #(nop) ADD file:9d282119af0c42bc8…   72.8MB
  ```



- Dockerfile로 Docker image 생성하기

  - 위에서 container를 사용하여 만든 image를 이번에는 Dockefile을 통해 만들어 볼 것이다.
  - 아래와 같이 Dockerfile을 작성한다.

  ```dockerfile
  FROM ubuntu:20.04
  
  RUN apt-get update
  ```

  - 위 Dockerfile을 build한다.
    - 아래와 같이 다양한 메시지가 출력된다.
    - `d5447fc01ae6`는 `ubuntu:20.04`의 image id이다.
    - 그 뒤로 `Running in c46b120a81fc`라는 메시지를 볼 수 있는데, Dockerfile의 `RUN`은 단순히 쉘 명령어를 수행하는 작업이 아니라, 바로 이전 단계의 layer를 기반으로 컨테이너를 생성하고, `RUN`에 지정된 명령어를 실행한 후, 이 컨테이너를 commit해서 새로운 이미지로 저장하는 작업이다.
    - 즉 아래의 경우 `d5447fc01ae6` image를 기반으로 `c46b120a81fc` container를 생성하고, 해당 container에서 `apt-get update` 명령어를 수행한 후 해당 container를 commit하여 `a3bca4ab7b4f`라는 이미지를 만든 것이다.
    - 따라서 더 이상 필요 없어진 `c46b120a81fc` 컨테이너는 삭제한다(`Removing intermediate container c46b120a81fc`).

  ```bash
  $ docker build -t ubuntu:apt-update2 .
  
  Sending build context to Docker daemon  2.048kB
  Step 1/2 : FROM ubuntu:20.04
   ---> d5447fc01ae6
  Step 2/2 : RUN apt-get update
   ---> Running in c46b120a81fc
  # ...
  Removing intermediate container c46b120a81fc
   ---> a3bca4ab7b4f
  Successfully built a3bca4ab7b4f
  Successfully tagged ubuntu:apt-update2
  ```

  - 생성된 image의 history를 확인한다.

  ```bash
  $ docker history ubuntu:apt-update2
  IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
  a3bca4ab7b4f   7 minutes ago   /bin/sh -c apt-get update                       44.2MB    
  d5447fc01ae6   6 months ago    /bin/sh -c #(nop)  CMD ["bash"]                 0B        
  <missing>      6 months ago    /bin/sh -c #(nop) ADD file:9d282119af0c42bc8…   72.8MB    
  ```



- Docker pull을 통해 받은 image와 위 처럼 직접 build한 image의 가장 큰 차이는 바로 중간 layer가 남아있다는 점이다.

  - 위 두 방식(container를 commit하는 방식과 Dockerfile로 build하는 방식) 모두 history를 확인하면, 직접 build한 부분의 image가 `<missing>`이 아니라, 남아있는 것을 확인할 수 있다.
  - 따라서 위에 나와 있는 중간 image들로 Docker container를 실행하는 것이 가능하다.
    - 예를 들어 `ubuntu:apt-update2` 이미지의 경우 `apt-get update`를 실행하기 이전의 image가 남아 있으므로 아래와 같이 실행하면 `apt-get update`가 실행되지 않은 ubuntu image를 실행시킬 수 있다.

  ```bash
  $ docker run d5447fc01ae6
  ```



## Docker image 효율적으로 build하기

- Docker image는 계층적 구조를 가지고 있다.

  - 예를 들어 아래와 같은 app이 있고

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  @app.get("")
  def hello():
      return
  
  
  if __name__ == "__main__":
      uvicorn.run(app)
  ```

  - 위 app을 실행하기 위한 requirements.txt들이 아래와 같을 때

  ```bash
  anyio==3.7.0
  click==8.1.3
  exceptiongroup==1.1.1
  fastapi==0.98.0
  h11==0.14.0
  idna==3.4
  pydantic==1.10.9
  sniffio==1.3.0
  starlette==0.27.0
  typing_extensions==4.7.0
  uvicorn==0.22.0
  ```

  - 아래 Dockerfile을

  ```dockerfile
  FROM python:3.9.0
  
  ENV foo bar
  
  COPY main.py /app/main.py
  WORKDIR /app
  
  COPY requirements.txt /app/requirements.txt
  RUN pip install --upgrade pip
  RUN pip install -r requirements.txt
  
  CMD ["python", "main.py"]
  ```

  - build하면

  ```bash
  $ docker build -t test_image:1.0.0
  ```

  - 아래와 같은 계층 구조가 된다.
    - `python:3.9.0` image의 마지막 계층부터 표시하면 아래와 같다.

  ```bash
  $ docker history test_image:1.0.0
  
  IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
  ef7708dcc580   8 seconds ago    /bin/sh -c #(nop)  CMD ["python" "main.py"]     0B        
  d97a200eb65a   8 seconds ago    /bin/sh -c pip install -r requirements.txt      17.8MB    
  087b34aed24a   13 seconds ago   /bin/sh -c pip install --upgrade pip            16.4MB    
  8230ff82febb   20 seconds ago   /bin/sh -c #(nop) COPY file:8eb70513058f29ae…   177B      
  cdba6526752a   20 seconds ago   /bin/sh -c #(nop) WORKDIR /app                  0B        
  3c12e4d3f954   20 seconds ago   /bin/sh -c #(nop) COPY file:61fa4cf0b88ff0d3…   148B      
  1b2bf6c81145   20 seconds ago   /bin/sh -c #(nop)  ENV foo=bar                  0B        
  0affb4652fc0   2 years ago      /bin/sh -c #(nop)  CMD ["python3"]              0B  
  ```

  - 또한 직접 build한 image의 모든 계층은 파일로 저장되어, 특정 계층을 실행시키는 것도 가능하다.
    - 예를 들어 위 예시에서 pip를 통해 필요한 package를 설치하기 전 상태인 image `087b34aed24a`를 가지고 container를 실행하면 아무 package도 설치되지 않은 상태의 container가 실행된다.

  ```bash
  $ docker run --name update-pip 087b34aed24a /bin/bash -c 'pip list'
  
  Package    Version
  ---------- -------
  pip        23.1.2
  setuptools 50.3.2
  wheel      0.36.0
  ```

  - 또한 build 과정 중 일부가 변경된 경우, 모든 계층을 다시 생성하지 않고, 변경된 계층부터 다시 생성을 시작한다.



- 이러한 특징들 때문에, 어떤 순서로 build를 하는가에 따라 build 속도나 image size가 달라질 수 있다.

  - 예시1. source code만 변경할 경우
    - 예를 들어 위 예시와 같은 Dockerfile에서 source code가 아래와 같이 변경될 경우

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  @app.get("")
  def hello():
      return "Hello World"
  
  
  if __name__ == "__main__":
      uvicorn.run(app)
  ```

  - 다시 build하면 `COPY main.py /app/main.py` 계층부터 다시 생성을 시작한다.
    - `ENV foo bar`에 해당하는 계층인 `1b2bf6c81145`까지는 동일한데, 그 이후 계층은 모두 새로 생성된 것을 확인 할 수 있다.

  ```bash
  $ docker build -t test_image:1.1.0
  $ docker history test_image:1.1.0
  
  IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
  f0393b6ea6b4   8 seconds ago        /bin/sh -c #(nop)  CMD ["python" "main.py"]     0B        
  bd916ea37413   9 seconds ago        /bin/sh -c pip install -r requirements.txt      17.8MB    
  7a980c84083e   12 seconds ago       /bin/sh -c pip install --upgrade pip            16.4MB    
  5e28c2fb7e73   18 seconds ago       /bin/sh -c #(nop) COPY file:8eb70513058f29ae…   177B      
  9787f191f30c   18 seconds ago       /bin/sh -c #(nop) WORKDIR /app                  0B        
  237827f7fa3a   18 seconds ago       /bin/sh -c #(nop) COPY file:7c8c5f00e6553b99…   162B      
  1b2bf6c81145   About a minute ago   /bin/sh -c #(nop)  ENV foo=bar                  0B        
  0affb4652fc0   2 years ago          /bin/sh -c #(nop)  CMD ["python3"]              0B 
  ```

  - 예시2. requirements만 변경할 경우
    - 마찬가지로 requirements.txt file이 변경될 경우 `COPY requirements.txt /app/requirements.txt`부터 다시 생성을 시작한다.

  ```bash
  $ docker build -t test_image:1.2.0
  $ docker history test_image:1.2.0
  
  IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
  67f997b138f6   4 seconds ago        /bin/sh -c #(nop)  CMD ["python" "main.py"]     0B        
  6e022c1142a8   4 seconds ago        /bin/sh -c pip install -r requirements.txt      20.5MB    
  1f818c4a097f   8 seconds ago        /bin/sh -c pip install --upgrade pip            16.4MB    
  0c25d551c85c   13 seconds ago       /bin/sh -c #(nop) COPY file:4841ad04d11eec7f…   193B    
  # 여기까지는 동일하다.
  9787f191f30c   57 seconds ago       /bin/sh -c #(nop) WORKDIR /app                  0B        
  237827f7fa3a   57 seconds ago       /bin/sh -c #(nop) COPY file:7c8c5f00e6553b99…   162B      
  1b2bf6c81145   About a minute ago   /bin/sh -c #(nop)  ENV foo=bar                  0B        
  0affb4652fc0   2 years ago          /bin/sh -c #(nop)  CMD ["python3"]              0B  
  ```

  - 문제1. 하위 계층에 변경사항이 생겨 다시 build할 경우 상위 계층도 모두 새롭게 build된다.
    - 예시1에서는 source code만 변경되었는데도, 다시 `pip update`와 `pip install -r requirements.txt`가 실행된다.
    - 예시에서는 requirements들을 install하는데 시간이 오래 걸리지 않지만, 만약 오랜 시간이 걸린다고 하면, 실제로는 변경 사항이 없음에도 requirements를 설치하는데 많은 시간을 보내야 할 것이다.
  - 문제2. 계층은 해당 계층을 사용하는 모든 image가 삭제되지 않는 한 남아있다.
    - 각 계층은 개별적으로 저장된다.
    - 위 예시에서 가장 용량을 크게 증가시키는 부분은 `RUN pip install -r requirements.txt`부분이다.
    - 예시1에서는 source만 변경하고, requirements는 변경하지 않았으므로, 사실 requirements도 다시 build할 이유는 없다.
    - 그럼에도 더 아래 계층인 `COPY main.py /app/main.py` 계층부터 다시 생성하기 시작하므로, `RUN pip install -r requirements.txt` 계층도 다시 생성된다.
    - 즉 source code의 변경사항이 생기기 이전의 `bd916ea37413` 계층이나 source code의 변경으로 새롭게 build된 `6e022c1142a8` 계층은 설치된 requirements들은 동일함에도 서로 다른 계층으로 저장되어 있다.
    - 예시에서는 그렇게 큰 용량이 아니지만, 만약 requirements가 기가 단위가 되면, requirements는 동일한데도 기가 단위의 계층이 새롭게 생성되는 것이다.
  - 해결
    - 만일 source code의 변경이 잦고, requirements의 변경이 거의 없을 때는 아래와 같이 requirements를 먼저 install하고 source code를 copy하는 것이 좋다.
    - Source code만 변경될 경우 `COPY main.py /app/main.py` 계층부터 다시 생성될 것이기 때문이다.

  ```dockerfile
  FROM python:3.9.0
  
  ENV foo bar
  
  COPY requirements.txt /app/requirements.txt
  RUN pip install --upgrade pip
  RUN pip install -r requirements.txt
  
  COPY main.py /app/main.py
  WORKDIR /app
  
  CMD ["python", "main.py"]
  ```



- 결론
  - 위에서 본 것과 같이 어떤 순서로 build하는가에 따라서 계층의 크기나 build 속도가 크게 차이날 수 있다.
  - 따라서 build하려는 image의 특성에 따라 build 순서를 고려하여 build해야한다.



- Size를 줄이는 다른 방법들
  - alpine image를 사용하라
    - 정말 필요한 것들만 들어가 있는 경량화된 image이다.
  - Multi-stage build를 사용한다.
    - App을 빌드할 image와 실행할 image를 나눠서 build하는 방식이다.
    - Image가 2개 생성되긴 하지만 두 개의 Dockerfile에 따로 작성하지 않고, 하나의 Dockefile에 작성하는 것이 가능하다.



- Multi-stage build

  - 먼저 container로 실행시키고자하는 app을 생성한다.

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  
  @app.get("")
  def hello():
      return
  
  
  if __name__ == "__main__":
      uvicorn.run(app)
  ```

  - 그 후 일반적인 방식으로 Dockerfile을 작성한다.

  ```dockerfile
  # builder
  FROM python:3.9.0
  
  COPY . /app
  WORKDIR /app
  
  RUN pip install --upgrade pip
  RUN pip install -r requirements.txt
  
  CMD ["python", "main.py"]
  ```

  - 빌드 된 image의 크기는 923MB이다.

  ```bash
  REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
  test_image   origin    d58bf027806d   31 seconds ago   923MB
  ```

  - Multi-stage build를 적용하고

  ```dockerfile
  # builder
  FROM python:3.9.0 AS my_builder
  
  COPY . /app
  WORKDIR /app
  
  RUN pip install --upgrade pip
  RUN pip install -r requirements.txt
  
  # deployer
  FROM python:3.9.0
  # app 실행에 필요한 package들을 옮기고
  COPY --from=my_builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
  # source code를 옮긴다.
  COPY --from=my_builder /app /app
  
  CMD ["python", "main.py"]
  ```

  - Image의 size를 확인하면, 기존에 비해 8MB 정도 감소한 것을 볼 수 있다.

  ```bash
  REPOSITORY                                      TAG              IMAGE ID       CREATED             SIZE
  test_image                                      multi-stage      fe105498362c   3 seconds ago       915MB
  ```

  - History 확인
    - 기본 Python image에 package들과 source code만 복사하여 실행한다.

  ```bash
  $ docker history test_image:multi-stage
  
  IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
  9919acdc9b48   9 seconds ago   /bin/sh -c #(nop)  CMD ["python" "main.py"]     0B        
  36effa42202d   9 seconds ago   /bin/sh -c #(nop) COPY dir:cf86af1cbd34128a5…   727B      
  41439e081dd2   9 seconds ago   /bin/sh -c #(nop) COPY dir:1679144dabe104497…   29.2MB    
  0affb4652fc0   2 years ago     /bin/sh -c #(nop)  CMD ["python3"]              0B     
  ```

  - 위 예시에서는 크게 감소하지는 않았지만, build 과정이 길고 복잡해질수록 image의 크기도 커질 수 밖에 없다.
    - 따라서 이런 경우 보다 크게 감소시킬 수 있을 것이다.







# Docker 설치하기

> ubuntu 기준

- HTTP 패키지 설치

  - update apt

  ```bash
  $ sudo apt update
  ```

  - HTTP 패키지 설치

  ```bash
  $ sudo apt-get install -y ca-certificates curl gnupg lsb-release
  ```



- GPG key 추가 및 repository setup

  - GPG key 추가

  ```bash
  $ sudo mkdir -p /etc/apt/keyrings
  $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  ```

  - repository setup

  ```bash
  $ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  ```



- docker 설치

  - apt-get update

  ```bash
  $ sudo apt-get update
  ```

  - docker 설치

  ```bash
  $ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
  ```

  - test
    - test image를 다운 받아, 해당 이미지로 container를 실행한다.
    - 실행이 완료되면 메시지를 출력하고 종료된다.

  ```bash
  $ sudo docker run hello-world
  ```



- 권한 관리

  - docker group에 사용자 추가

  ```bash
  $ sudo usermod -a -G docker <사용자명>
  ```






# 도커 명령어

## Docker

- Docker 버전 확인

  ```bash
  $ docker version
  ```



- `docker system`

  - `docker system df`
    - Docker가 사용하는 disk 사용량을 보여준다.
    - `-v`(`--verbose`): 보다 상세한 정보를 보여준다(volume별 크기도 확인이 가능하다).
    - `--format`: format을 지정할 수 있다.

  ```bash
  $ docker system df [options]
  ```

  - `docker system info`
    - Docker와 관련된 정보를 보여준다.
    - `--format`: format을 지정할 수 있다.

  ```bash
  $ docker system info
  ```



- `docker history`

  - Docker image가 만들어지기까지의 과정 전체를 보여주는 명령어이다.
  - 결과는 아래에서부터 읽어 나가면 된다.

  ```bash
  $ docker history <image>
  ```



- `docker diff`

  - Image와 해당 image로 만든 container 사이의 차이를 보여준다.
  - `C`는 변경, `A`는 추가, `D`는 삭제를 의미한다.

  ```bash
  $ docker diff <container>
  ```



- `docker top`

  - Container 내에서 실행 중인 process들을 보여준다.

  ```bash
  $ docker top <container>
  ```



- `docker stats`

  - Container 별 resource 사용량을 보여준다.
  - 옵션
    - `--all`, `-a`: 모든 컨테이너의 상태를 보여준다.
    - `--format`: Go 템플릿을 통해 format을 설정할 수 있다.
    - `--no-stream`: 명령어 실행 시점의 상태를 보여준다.
    - `--no-trunc`: 결과를 잘라내지 않고 전부 보여준다.
  
  ```bash
  $ docker stats
  ```
  
  - 결과
    - `NET I/O`: 컨테이너가 네트워크 인터페이스를 통해 주고 받은 데이터의 양
    - `BLOCK I/O`: 컨테이너가 disk에서 읽고 쓴(read and write) 데이터의 양
  
  ```
  CONTAINER ID   NAME           CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O         PIDS
  34ac359a659b   container1     0.00%     41.64MiB / 125.6GiB   0.03%     392kB / 15.1MB    0B / 0B           49
  d71698367f39   container2     0.23%     227.7MiB / 125.6GiB   0.18%     168MB / 68.7MB    8.19kB / 0B       62
  d62202653708   container3	  0.19%     59.24MiB / 125.6GiB   0.05%     27.7MB / 11MB     4.1kB / 8.19kB    13
  4b6e5264a8f2   container4	  0.54%     368.5MiB / 125.6GiB   0.29%     2.98GB / 4.09GB   4.1kB / 0B        19
  ```




- `docker rename`

  - Container의 이름을 변경한다.

  ```bash
  $ docker rename <old_container_name> <new_container_name>
  ```





## Docker Hub

- Docker Hub에 공개된 이미지 검색

  - `--no-trunc`: 결과를 모두 표시
  - `--limit n`: n건의 검색 결과를 표시
  - `--filter=stars=n`: 즐겨찾기의 수가 n 이상인 이미지만 검색

  ```bash
  $ docker search [옵션] 키워드
  ```



- Docker Hub에 로그인

  - `-p(--password), -u(--username)`을 옵션으로 줄 수 있다.
    - 따로 지정해 주지 않고 입력하면 CLI로 물어본다.
  - 다른 환경에 Docker 리포지토리가 있는 경우에는 서버명을 지정해 줘야 한다.
    - 서버명을 지정하지 않았을 경우 Docker Hub에 엑세스한다.

  ```bash
  $ docker login [옵션] [서버]
  ```



- Docker Hub에서 로그아웃

  - 서버명을 지정하지 않았을 경우 Docker Hub에 엑세스한다.

  ```bash
  $ docker logout [서버명]
  ```



## Docker image

- Docker 이미지 다운로드 하기

  - 태그에는 일반적으로 버전 정보가 들어간다.
    - 태그를 생략할 경우 자동으로 latest가 태그로 들어가 최신버전이 다운로드 된다.
    - 그렇다고 태그가 무조건 버전을 뜻하는 것은 아니다.
    - 태그는 본래 이미지에 붙이는 표시 같은 것인데 버전이 주로 사용될 뿐이다.
  - `-a` 옵션을 주면 모든 태그의 Docker 이미지를 다운 받으며, 이 때는 태그명을 입력할 수 없다.
  - 이미지명 대신 이미지를 다운 받을 URL을 지정할 수도 있다.

  ```bash
  $ docker pull [옵션] 이미지명[:태그명]
  ```



- Docker Hub에 이미지 업로드하기

  - `docker login` 명령으로 로그인 해야 가능하다.
  - Docker Hub에 업로드할 이미지는 `<Docker Hub 사용자명>/이미지명:태그명`의 형태로 지정해야 한다.

  ```bash
  $ docker image push 이미지명[:태그명]
  ```



- Docker 이미지 리스트 보기

  - `-a`(`--all`): 모든 이미지를 표시한다.
  - `--digests`: 다이제스트를 표시할지 여부, 다이제스트는 Docker 레지스트리(Docker Hub 등)에 업로드된 이미지를 식별하기 위한 값이다.
  - `--no-trunc`: 결과를 모두 표시한다.
  - `--quiet,-q`:  이미지 ID만 표시한다.
  - image 명이 정확히 일치할 경우 `grep`을 사용하지 않아도 된다.
  
  ```bash
  $ docker images [옵션] [리포지토리명]
  $ docker image ls [옵션] [리포지토리명]
  ```



- 특정 이미지 정보 상세 보기

  - 이미지 ID, 작성일, docker 버전, CPU 아키텍처 등의 정보를 JSON 형태로 확인 가능하다.
  - `--format="{{필드명}}"` 옵션을 통해 JSON의 특정 필드만 확인이 가능하다.

  ```bash
  $ docker inspect [--format="{{필드명}}"] 이미지명
  ```



- 이미지 이름 변경하기

  - 아래 명령어를 입력 후 이미지 리스트를 보면 기존 이미지가 변경된 것이 아니라 새로운 이미지가 하나 더 생긴 것을 볼 수 있다.
    - 정확히 말하면 새로운 이미지가 생기거나 복제된 것이 아니다. 동일한 이미지에 다른 태그가 붙은 것 뿐이다.
    - 두 이미지의 ID를 확인해보면 동일한 것을 볼 수 있다.

  ```bash
  $ docker tag <기존 이미지명>:<기존 태그명> <태그를 붙일 이미지명>:<변경할 태그명>
  ```



- 이미지 삭제

  - `-f(--force)`: 이미지를 강제로 삭제
  - `--no-prune`: 중간 이미지를 삭제하지 않음
  - 이미지명 대신 이미지 ID를 입력해도 된다.
  - 여러 개의 이미지를 한 번에 삭제하려면 이미지명 사이에 공백을 두고 입력하면 된다.

  ```bash
  $ docker rmi [옵션] 이미지명 [이미지명2]
  ```



- 사용하지 않는 도커 이미지 삭제

  - `-a(--all)`: 사용하지 않는 Docker 이미지 전부 삭제
    - 기본적으로 아래 명령어는 dangling image만을 삭제한다.
    - 동일한 태그를 가진 Docker 이미지가 빌드될 경우, 기존에 있던 이미지는 삭제되지는 않고, tag가 none으로 변경된 상태로 남아 있게 되는데 이를 dangling image라 한다.
    - `-a`를 줄 경우 dangling image와 함께 현재 컨테이너에서 사용하지 않는 이미지들도 함께 삭제한다.
  - `-f(--force)`: 이미지를 강제로 삭제
  - `--filter 조건`: 조건에 부합하는 dangling image들을 삭제한다.

  ```bash
  $ docker image prune [옵션]
  ```





## Docker Container

- Docker Container
  - 이미지를 통해 컨테이너를 생성한다.
    - 이미지의 실체는 Docker에서 서버 기능을 작동시키기 위해 필요한 디렉토리 및 파일들이다.
    - 구체적으로는 리눅스의 작동에 필요한 /etc나 /bin 등과 같은 디렉토리 및 파일들이다.
  - 컨테이너를 생성하면 이미지에 포함된 리눅스의 디렉토리와 파일들의 스냅샷이 컨테이너로 들어가게 된다.
    - 스냅샷이란 스토리지 안에 존재하는 파일과 디렉토리를 특정 시점에서 추출한 것을 말한다.
  - 컨테이너는 아래와 같은 라이프 사이클을 지닌다.
    - 생성: 컨테이너가 생성되어 실행되고 있지 않은 상태
    - 실행: 컨테이너가 실행 중인 상태
    - 정지: 컨테이너가 실행 되었다 정지된 상태
    - 삭제: 컨테이너가 삭제 된 상태



- 컨테이너 생성하기

  - `--name`: 컨테이너의 이름을 지정할 수 있다.

  ```bash
  $ docker create [옵션] 이미지명[:태그]
  ```



- 컨테이너 리스트 보기

  ```bash
  $ docker ps [옵션]
  ```

  - `-a(--all)`: 현재 동작중이 아닌 컨테이너도 모두 보여준다.
  - `-f(--filter)`: 표시할 컨테이너의 필터링
  - `--format`: 표시 포맷을 지정
    - 이미지 ID, 실행 명령, 컨테이너 가동 시간, 컨테이너 디스크 크기, 볼륨 마운트, 네트워크명 등의 추가적인 정보를 볼 수 있다.
  - `-n(--last)`: 마지막으로 실행된 n건의 컨테이너만 표시
  - `-l(--latest)`: 마지막으로 실행된 컨테이너만 표시
  - `--no-trunc`: 정보를 생략하지 않고 표시
  - `-q(--quiet)`: 컨테이너 ID만 표시
  - `-s(--size)`: 파일 크기 표시



- 컨테이너 정보 보기

  - 옵션
    - `--all`, `-a`: 모든 컨데이터 보기(실행 중이 아닌 컨테이터 포함)
    - `--format`: 포맷을 설정해서 볼 수 있다.
    - `--no-stream`: stream 형태가 아닌 명령어를 입력한 순간의 결과만 본다.
    - `--no-trunc`: 정보를 생략하지 않고 표시
  
  ```bash
  $ docker stats
  ```
  
  - 특정 컨테이너 정보 보기
  
  ```bash
  $ docker stats 컨테이너명/컨테이너ID
  ```



- 컨테이너 시작하기

  - 공백으로 구분하여 복수의 컨테이너를 실행시킬 수 있다.
  - run 명령어와 일부 옵션을 공유한다.

  ```bash
  $ docker start [옵션] <컨테이너명 또는 ID> [컨테이너명 또는 ID]
  ```



- 컨테이너 생성 및 시작하기

  - create와 start를 동시에 수행하는 명령어
  - 컨테이너에서 실행할 명령의 예시로 `/bin/bash`를 입력할 경우 콘솔의 프롬프트가 $에서 #로 바뀌는 것을 확인 가능하다.

  ```bash
  $ docker run [옵션] 이미지명[:태그명] [컨테이너에서 실행할 명령]
  ```

  - 기본 옵션
    - `--cidfile`: 컨테이너 ID를 파일로 출력한다.
    - `-i(--interactive)`: 컨테이너의 표준 입력을 연다.
    - `-t(--tty)`: 단말기 디바이스를 사용한다.
    - `--name`: 컨테이너의 이름을 지정할 수 있다.
  - 컨테이너 실행 옵션
    - `-a(--attach)`: 표준 입력(STDIN), 표준 출력(STDOUT), 표준 오류 출력(STRERR)에 attach한다.
    - `-d(--detach)`: 백그라운드에서 실행한다.
    - `-u(--user)`: 사용자명을 지정한다.
    - `--restart=[no | on-failure | onfailure:횟수 | always | unless-stopped]`: 명령의 실행 결과에 따라 컨테이너를 재시작 한다.
    - `--rm`: 컨테이너가 종료될 때, container를 삭제하고 컨테이너가 사용한 anonymous volume도 함께 삭제한다.
  - 네트워크 설정 옵션
    - `--add--host=[호스트명:IP 주소]`: 컨테이너의 /etc/hosts에 호스트명과 IP 주소를 정의.
    - `--dns=[IP 주소]`: 컨테이너용 DNS 서버의 IP 주소 지정
    - `--expose`: 지정한 범위의 포트 번호를 할당
    - `--mac-address=[MAC 주소]`: 컨테이너의 MAC 주소를 지정
    - `--net=[bridge(기본값) | none | container:<name | id> | host | NETWORK]`: 컨테이너의 네트워크를 지정
    - `-h(--hostname)`: 컨테이너 자신의 호스트명을 지정
    - `-p(--publish)[호스트의 포트 번호]:[컨테이너의 포트 번호]`: 호스트와 컨테이너의 포트 매핑, 호스트의 포트 번호로 접근할 경우 컨테이너의 포트 번호에 접속된다.
    - `-P(--publish--all)`: 호스트의 임의의 포트를 컨테이너에 할당
    - `--network-alias`: Docker network 상에서 container에 어떤 이름으로 접근할지를 설정할 수 있다(기본값은 container name)
  - 자원 설정 옵션
    - `-c(--cpu-shares)`: CPU의 메모리 사용 배분(비율)
    - `-m(--memory)`: 사용할 메모리를 제한하여 실행(단위는 b,k,m,g 중 하나)
    - `-v(--volume)=[호스트의 디렉토리]:[컨테이너의 디렉토리]`: 호스트와 컨테이너의 디렉토리를 공유, 상대경로는 입력이 불가능하다.
  - 컨테이너 환경설정 옵션
    - `-e(--env)=환경변수`: 환경변수를 설정한다.
    - `--env-file=파일명`: 환경변수를 파일을 통해 설정한다.
    - `--read-only=[true|false]`: 컨테이너의 파일 시스템을 읽기 전용으로 만든다.
    - `-w(--workdir)=경로`: 컨테이너의 작업 디렉토리를 지정한다.
    - `-u(--user)=사용자명`: 사용자명 또는 UID를 지정한다.
  
  - 권한 관련 설정
  
    > https://docs.docker.com/engine/containers/run/#runtime-privilege-and-linux-capabilities
  
    - `--cap-add`: Linux capability를 추가한다.
    - `--cap-drop`: Linux capability를 제거한다.
    - `--privileged`: Container에게 host machine의 모든 capability와 device에 접근할 수 있는 권한을 준다.
    - `--device=[]`: Container에게 host machine의 device에 접근할 수 있는 권한을 준다.
  
  - restart 옵션은 되도록 지정해주는 것이 좋다.
    - 만일 Docker client자체가 내려갈 경우 Docker client를 재실행했을 때, restart 옵션을 주지 않은 컨테이너들을 자동으로 재생성되지 않기 때문이다.
    - 물론 수동으로 띄워도 되지만 만일 A, B, C 컨테이너가 하나의 서비스를 구성하고 있고, B, C 컨테이너가 A 컨테이너에 의존적이라 A 컨테이너가 정상적으로 떠있어야 B, C도 동작하는 경우에 문제가 생길 수 있다.
    - A에 restart 옵션이 없다면 Docker client가 재실행되면서 B, C는 자동으로 다시 생성되지만 A는 재생성되지 않아 B, C도 Error가 발생하는 경우가 있을 수 있기 때문이다.
    - 정확히는 위와 같이 복수의 컨테이너가 하나의 서비스를 구성하고 있을 경우 "restart 옵션을 설정해주는 것이 좋다"기 보다 하나의 서비스를 구성하고 있는 컨테이너들은 restart 설정을 맞춰주는 것이 좋다.
  - `publish` 옵션
    - `-p(--publish)[호스트의 포트 번호]:[컨테이너의 포트 번호]`는 컨테이너 외부의 `host:port`를 컨테이너 내부의 `host:port`와 연결하겠다는 의미이다.



- `--privileged` 옵션 관련 주의 사항
  - `--privileged` 옵션은 container에게 아래와 같은 capability를 준다.
    - 모든 Linux kernel capability
    - default seccomp profile 비활성화
    - default AppArmor profile 비활성화
    - SELinux process label 비활성화
    - Host machine의 모든 device에 대한 접근 권한
    - `/sys`를 읽고 쓸 수 있는 권한
    - cgroups mounts read-write
  - `--privileged` 옵션은 운영 환경에서는 사용하지 않는 것이 좋다.
    - `--privileged` 옵션은 host machine이 할 수 있는 거의 모든 권한을 부여 받는다.
    - 이 옵션은 container에게 과한 권한을 주기에 예상치 못한 문제가 발생할 수 있다.
    - 따라서 운영 환경에서는 container에 필요한 권한만 `--cap-add` 혹은 `--device`를 통해 부여해야한다.



- 컨테이너 정지

  - 공백으로 구분하여 복수의 컨테이너를 정지시킬 수 있다.
  - `-t(--time)`: 컨테이너를 몇 초 후에 정지시킬지 지정한다.

  ```bash
  $ docker stop [옵션] <컨테이너명 또는 ID> [컨텡너명 또는 ID]
  ```



- 컨테이너 재시작

  - 공백으로 구분하여 복수의 컨테이너를 재시작할 수 있다.
  - `-t(--time)`: 컨테이너를 몇 초 후에 재시작할지 지정한다.

  ```bash
  $ docker restart [옵션] <컨테이너명 또는 ID> [컨텡너명 또는 ID]
  ```



- 컨테이너 삭제

  - 공백으로 구분하여 복수의 컨테이너를 삭제할 수 있다.
  - `-f(--force)`: 실행 중인 컨테이너를 강제로 삭제
  - `-v(--volumes)`: 할당한 볼륨을 삭제

  ```bash
  $ docker rm [옵션] <컨테이너명 또는 ID> [컨텡너명 또는 ID]
  ```



- 컨테이너 중단/재개

  - 실행중인 컨테이너에서 작동 중인 프로세스를 중단시킬 때 사용한다.

  ```bash
  $ docker pause <컨테이너명 또는 ID>
  
  $ docker unpause <컨테이너명 또는 ID>
  ```



- 컨테이너 log 확인

  - `--details`: log를 보다 상세하게 출력한다.
  - `-f(--follow)`: log를 출력하고 종료하지 않고, log output을 지속적으로 follow한다.
  - `--since`, `--until`
    - Timestamp(e.g. 2023-10-11T10:17:23Z) 혹은 상대적 시간(e.g. 15m)을 받아 해당 시간 부터/까지의 log를 출력한다.
  - `-t(--timestamps)`: timestamp를 함께 출력한다.
  - `-n(--tail)`: 가장 최근 log부터 몇 개의 log를 보여줄지를 설정한다.

  ```bash
  $ docker logs [options] <container>





## 가동 중인 Docker Container 연결

- 컨테이너에 연결하기

  - 정확히는 host machin의 표준 입력(stdin)과 표준 출력(stdout), error stream을 실행중인 container에 연결하는 명령어이다.
    - Host machine의 stdin, stdout, error stream이 container의 root process에 연결되는 형식이다.
  
  - Container를 실행했을 때의 환경이 foreground로 보이게 된다.
  
  ```bash
  $ docker attach 컨테이너명
  ```



- 가동 컨테이너에서 프로세스 실행

  - 가동 중인 컨테이너에서 새로운 프로세스를 실행
    - 백그라운드에서 실행되고 있는 컨테이너에 액세스하고자 할 때는 attach  명령으로 연결해도 쉘이 작동하지 않는 경우 명령을 접수할 수 없다.
    - 따라서 아래 명령어를 입력하여 임의의 명령을 실행한다.
  - 옵션
    - `-d(--detach)`: 명령을 백그라운드에서 실행한다.
    - `-i(--interactive)`: 컨테이너의 표준 입력을 연다. 이를 통해 attach되어 있지 않아도 container의 stdin에 접근할 수 있게 되어, container 내부에 명령어를 입력할 수 있게 된다.
    - `-t(--tty)`: tty 디바이스를 사용한다.
    - `-u(--user)`: 사용자명을 지정한다.
  
  
  ```bash
  $ docker exec [옵션] <컨테이너 식별자> <실행할 명령> [인수]
  ```
  
  - `-it`
    - `--interactive` option과 `--tty` option은 주로 함께 사용한다.
    - 만일 `-i` 옵션만 줄 경우 아래와 같이 tty가 ?표 표시된다.
  
  ```bash
  $ docker exec -i <container> /bin/bash
  
  $ ps
  PID TTY          TIME CMD
  19 ?        00:00:00 bash
  25 ?        00:00:00 ps
  ```
  



- `attach`와 `exec`의 차이

  - `attach`는 실행 중인 컨테이너의 stdin, stdout, error stream을 container의 root 프로세스의 stdin, stdout, error stream과 연결되는 것이다.
  - 예를 들어 아래와 같이 container를 실행시키고

  ```bash
  $ docker run -it --name test ubuntu:20.04 /bin/bash
  ```

  - attach를 통해 접속한 뒤

  ```bash
  $ docker attach test
  ```

  - Process들을 확인하면, 새로운 process가 생성되지 않은 것을 확인할 수 있다.
    - 만약 이 상태에서 `exit` 명령을 입력할 경우 root process가 종료되고, container도 정지되게 된다.
  
  
  ```bash
  $ ps -ef
  UID          PID    PPID  C STIME TTY          TIME CMD
  root           1       0  0 04:26 pts/0    00:00:00 /bin/bash
  root          11       1  0 04:26 pts/0    00:00:00 ps -ef
  ```
  
  - 반면에 `exec`을 통해 접속할 경우
  
  ```bash
  $ docker exec -it test /bin/bash
  ```
  
  - 아래와 같이 새로운 프로세스가 생성되는 것을 확인할 수 있다.
  
  ```bash
  $ ps -ef
  
  UID          PID    PPID  C STIME TTY          TIME CMD
  root           1       0  0 04:26 pts/0    00:00:00 /bin/bash
  root          20       0  1 04:34 pts/1    00:00:00 /bin/bash
  root          28      20  0 04:34 pts/1    00:00:00 ps -ef
  ```



- 가동 컨테이너의 프로세스 확인

  ```bash
  $ docker top 컨테이너
  ```



-  가동 컨테이너의 포트 전송 확인

  ```bash
  $ docker port 컨테이너
  ```



- 컨테이너 이름 변경

  ```bash
  $ docker rename <기존 이름> <변경할 이름>
  ```



- 컨테이너 안의 파일을 복사

  ```bash
  # 컨테이너에서 호스트로 복사
  $ docker cp <컨테이너 식별자>:<컨테이너 안의 파일 경로> <호스트 디렉토리 경로>
  
  # 호스트에서 컨테이너로 복사
  $ docker cp <호스트 파일> <컨테이너 식별자>:<컨테이너 안의 파일 경로>
  ```



- 컨테이너의 변경 사항 확인

  - 컨테이너가 최초로 생성되었을 때와 달라진 점을 확인.
  - A는 파일의 추가, D는 파일의 삭제, C는 파일의 수정을 나타낸다.

  ```bash
  $ docker diff <컨테이너 식별자>
  ```





##  Docker Container Network

- Docker Container Network
  - Docker container 간의 통신을 수행한다.
  -  Docker는 기본값으로 bridge, host. none 세 개의 네트워크를 만든다.
    - 네트워크를 명시적으로 지정하지 않고 Docker 컨테이너를 시작하면 기본값인 bridge 네트워크로 Docker 컨테이너를 시작한다. 



- Docker 네트워크 목록 확인

  - `-f(--filter) key=value`: 출력을 필터링한다.
  - `--no-trunc`: 상세 정보를 출력한다.
  - `-q(--quiet)`: 네트워크  ID만 출력한다.

  ```bash
  $ docker network ls [옵션]
  ```



- 네트워크 상세 정보 확인

  - 아래 명령어를 통해 현재 해당 네트워크에 연결되어 있는 컨테이너를 확인 가능하다.
    - 반대의 경우도 마찬가지로 컨테이너에서도 inspect 명령어를 통해 컨테이너에 연결된 network를 확인 가능하다.
  
  ```bash
  $ docker network inspect [옵션] <네트워크명 혹은 id>
  ```



- 네트워크 작성

  - `-d(--driver)`: 네트워크 브리지 또는 오버레이(기본값은 bridge)
  - `--ip-range`: 컨테이너에 할당하는 IP 주소의 범위를 지정
  - `--subnet`: 서브넷을 CIDR 형식으로 지정
  - `--ipv6`: IPv6 네트워크를 유효화할지 말지(bool)
  - `-label`: 네트워크에 설정하는 라벨 

  ```bash
  $ docker network create [옵션] <네트워크명 혹은 id>
  ```



- 네트워크 연결

  - `--ip`: IPv4 주소
  - `--ip6`: IPv6 주소
  - `--alias`: 앨리어스명
  - `--link`: 다른 컨테이너에 대한 링크

  ```bash
  $ docker network connect [옵션] <네트워크명 혹은 id> <컨테이너명 혹은 id>
  ```



- 네트워크 연결 해제

  ```bash
  $ docker network disconnect <네트워크명 혹은 id> <컨테이너명 혹은 id>
  ```



- 연결 확인

  - `ping` 명령어를 container 내에서 실행한다.

  ```bash
  $ docker exec <컨테이너1 식별자> ping <컨테이너2 식별자>
  ```



- 네트워크 삭제

  ```bash
  $ docker network rm [옵션] <네트워크명 혹은 id>
  ```



- 일괄삭제

  - 아무 컨테이너에도 연결되지 않은 network를 모두 삭제한다.

  ```bash
  $ docker network prune
  ```



- 주의점

  - docker network에 container가 연결되는 순간 각 컨테이너에 IPAddress가 할당된다.
    - 예를 들어 network의 IP가 127.24.0.1일 때, 컨테이너 A, B를 순서대로 연결하면 A에는 127.24.0.2,  B에는  127.24.0.3이라는 IPAddress가 할당된다.
    - 만일 도중에 컨테이너 A가 내려가게 되면 B에 127.24.0.2가 할당되게 된다.

  - 주의할 점은 **순서대로** 할당된다는 점이다.
    - 예를 들어 기존 코드에서 B 컨테이너가 A 컨테이너로 요청을 보내기 위해서는 127.24.0.2로 요청을 보내야 했다.
    - 그런데 도중에 A 컨테이너가 내려가게 되면 기존에 B가 A 컨테이너에 요청을 보내기 위해 사용하던 127.24.0.2가 B 컨테이너 자신의 IP가 된다.
    - 또한 A 컨테이너 입장에서도 기존에 127.24.0.2로 바인드를 걸어 놨는데 A 컨테이너를 다시 띄울 경우 바인드를 걸어 놓은 127.24.0.2는 이제 B 컨테이너의 IP가 되었으므로 docker network와 연결이 되지 않는다.
    - 따라서 이 경우 B를 내리고 A를 먼저 띄운 후  B를 띄워야 한다.





## Docker 이미지 생성

- 컨테이너를 바탕으로 이미지 작성

  - `-a(--author)`: 작성자를 지정한다.
  - `-m(--message)`: 메시지를 지정한다.
  - `-c(--change)`:  커밋 할 때 Dockerfile 명령을 지정한다.
  - `-p(--pause)`: 컨테이너를 일시 정지하고 커밋한다.
    - 기본값은 true로 commit시에 container를 일시 정지시킨다.
    - 만약 정지를 원하지 않으면 명시적으로 false를 줘야한다.
  
  
  ```bash
  $ docker commit [옵션] <컨테이너 식별자> [이미지명[:태그명]]
  ```
  
  - Commit시에 volume이 설정되어 있는 data들은 포함되지 않는다.



- 컨테이너를 tar 파일로 출력

  - 다른 이름으로 출력하고 자 할 경우에는 `>` 를 사용한다.

  ```bash
  $ docker export <컨테이너 식별자> [> 다른 이름.tar]
  ```

  - 생성된 tar 파일의 상세 정보를 확인하면 컨테이너를 작동시키기 위해 필요한 파일을 확인할 수 있다.

  ```bash
  $ tar -tf <tar 파일명>
  ```



- tar 파일로 이미지 작성

  ```bash
  $ docker import <파일 또는 URL> [이미지명[:태그명]]
  ```



- 이미지 저장

  - Docker 이미지를 tar 파일로 저장
  - `-o`: 생성할 압축 파일의 이름
  
  ```bash
  $ docker save [옵션] [저장 파일명] <이미지명>
  ```



- 이미지 읽어 들이기

  - `-i`로 읽어 들일 파일명을 지정
  
  ```bash
  $ docker load [옵션]
  ```



- export와 save의 차이
  -  export
    - 컨테이너를 작동시키는 데 필요한 파일을 모두 압축 아카이브로 모을 수 있다.
    - Image의 layer는 포함되지 않는다.
    - 따라서 export를 통해 나온  tar 파일을 실행하면 컨테이너의 루트 파일 시스템을 그대로 추출할 수 있다.
  -  save
    - 이미지의 레이어 구조도 포함된 형태로 압축 아카이브로 모을 수 있다.
  - export 명령으로 작성한 것은 import로,   save 명령으로 작성한 것은 load로 읽어 들여야 한다.



















