# Kubernates

> https://www.samsungsds.com/kr/insights/kubernetes-2.html

- Kubernetes(k8s)
  - 컨테이너 오케스트레이션 툴이다.
    - 컨테이너 런타임을 통해 컨테이너를 다루는 도구이다.
    - 여러 서버(노드)에 컨테이너를 분산 배치하거나, 문제가 생긴 컨테이너를 교체하거나, 컨테이너가 사용할 환경 설정을 관리하고 주입해주는 일 등을 한다.
  - Kubernetes라는 이름은 조종사 또는 조타수를 의미하는 그리스어에서 따왔다.



- Kubernetes를 구성할 수 있게 해주는 도구들
  - Minukube
    - 개발 및 학습 용도에 적합한 구성 방식이다.
    - Kubernetes 개발자들 중 특정한 주제에 관심을 가진 사람들이 모인 SIG(Special Interest Group)에서 만든 도구이다.
    - Linux, macOS, Windows를 지원하며 간단한 설치가 가능하다.
    - Kubernetes가 제공하는 대부분의 기능을 활용할 수 있으며, IntelliJ등의 다양한 개발 도구들과 연계할 수 있다.
    - 반면에, 단일 노드(서버) 형태로 동작하기 때문에 다중 노드를 구성하여 수행해야 하는 작업은 할 수 없다.
    - 또한 노드를 가상화된 형태로 생성하기 때문에 Docker 등의 가상화 도구가 추가로 필요하다.
  - k3s
    - 보다 실질적으로 활용 가능한 쿠버네티스 클러스터를 구성해야 할 때 적합한 도구이다.
    - Rancher Labs에서 개발한 경량화된 Kubernetes의 배포판으로 현재 Kubernetes를 관리하는 재단인 CNCF에서 샌드박스 프로젝트로 육성되고 있다.
    - 단일 파일로 이루어진 k3s 실행 파일을 통해 서버와 에이전트만 구동하면 Kubernetes의 각 구성 요소가 간편하게 설치되면서 Kubernetes 클러스터를 간편하게 구성할 수 있따.
    - 특히 Kubernetes의 각종 환경 정보를 저장하는 ETCD는 SQLite로 대체되어 매우 가볍게 동작한다.
    - 따라서 사물인터넷이나 라즈베리파이 같은 학습용 초소형 컴퓨터에도 사용할 수 있다는 장점이 있다.
    - 소규모 운영환경에도 적용이 가능하지만, 대부분의 구성 요소가 단순화되어 있어 높은 성능과 안정성을 요구하는 시스템에는 부적합할 수 있다.
  - Rancher
    - 조금 더 대규모 환경에 적합한 Kubernetes 구성 방법이다.
    - k3s와 마찬가지로 Rancher Labs에서 만들었으며, 대규모 클러서 및 기업용 환경에도 적합한 Kubernetes 관리 플랫폼이다.
    - 무료로 사용할 수 있는 오픈소스 버전과 기술 지원을 받을 수 있는 사용 버전을 함께 제공한다.
    - Kubernetes 클러스터뿐 아니라 운영에 필요한 모니터링, 보안 관련 기능을 쉽게 설치할 수 있다는 장점이 있다.
    - 다만, Rancher는 대규모 시스템 관리까지 염두에 둔 플랫폼이므로 자체적인 구성 요소가 많이 포함되어 있어 다른 도구에 비해 조금 더 무거운 면이 있다.
    - Rancher를 모니터링 및 대시보드를 자동으로 구성해주는 도구로 접근하는 경우가 있는데, 이는 잘못된 접근이다.
  - kubeadm
    - 위에서 살펴본 Kubernetes 구성 도구들은 Kubernetes의 전체적인 구성을 목적에 맞게 자동으로 설치해주는 도구인 반면, kubeadm은 기본적인 상태의 쿠버네티스를 시스템상에 구성해주는 도구이다.
    - kubeadm은 사용자가 기본적인 Kubernetes 클러스터 구성 외에 운영에 필요한 서비스 ,스토리지, 모니터링 등의 세부 구성 요소를 직접 설정해야한다.
    - 세부적인 설정을 할 수 있는 전문가에게 권장된다.
  - Managed Kubernetes Service
    - 퍼블릭 클라우드에서 제공하는 방식으로 사용자가 Kubernetes를 설치하는 부담 없이 클라우드 서비스에서 제공하는 콘솔만으로 Kubernetes 클러스터 생성이 가능하다.
    - 또한 클러스터의 관리까지 퍼블릭 클라우드에서 해주기 때문에 사용자는 Kubernetes 기능을 사용하는 데에만 집중할 수 있게 된다.
    - 대표적으로 AWS의 EKS, Azure의 AKS, GCP의 GKE 등이 있다.



- Kubernetes the hard way

  > https://github.com/kelseyhightower/kubernetes-the-hard-way

  - Kubernetes를 직접 설정하는 방법을 설명한 tutorial이다.
    - Kubernetes 클러스터를 구성하기 위해 필요한 모든 구성 요소를 단계별로 직접 설정하는 방법을 가이드해준다.
    - 실제 운영에서는 앞에서 살펴본 각종 도구를 사용하는 것이 권장된다.
    - 그러나Kubernetes 운영에 필요한 전문적인 지식 습득을 위해서는 세부 설정에 대한 이해가 필요할 수 있다.
  - 위 가이드를 실습하면 Kubernetes의 전체적인 구성을 이해할 수 있어 Kubernetes에 대한 더 많은 지식을 얻을 수 있다.







## Kubernetes 컴포넌트

> https://www.samsungsds.com/kr/insights/kubernetes-3.html

- Kubernetes 컴포넌트

  - 전체 구성

    > [그림 출처](https://kubernetes.io/docs/concepts/overview/components/)

  ![components-of-kubernetes](Kubernates.assets/components-of-kubernetes-17322566561595.svg)

  - Kubernetes 컴포넌트는 크게 컨트롤 플레인(Control Plane) 컴포넌트와 노드(Node) 컴포넌트로 나눌 수 있다.
    - 컨트롤 플레인: Kubernetes 기능 제어, application scheduling, application유지 application scaling, rolling out updates 등 전체적인 기능을 담당한다.
    - 노드: 컨트롤 플레인 컴포넌트의 요청을 받아 각 노드에서 동작을 담당하는 VM 혹은 physical computer이다.



- Control Plane component
  - kube-apiserver
    - Kubernetes 클러스터로 들어오는 요청을 가장 앞에서 받아주는 역할을 한다.
    - 예를 들어 `kubectl`을 사용해 각종 명령을 수행할 경우 이 명령은 kube-apiserver로 전송된다.
    - 이렇게 전달된 요청에 대해 kube-apiserver는 이 요청의 처리 흐름에 따라 적절한 컴포넌트로 요청을 전달한다.
  - etcd(엣시디)
    - Kubernetes 클러스터가 동작하기 위해 필요한 클러스터 및 리소스의 구성 정보, 상태 정보 및 명세 정보 등을 key-value 형태로 저장하는 저장소.
    - 안정적인 동작을 위해 자료를 분산해서 저장하는 구조를 채택하고 있다.
  - kube-scheduler
    - Kubernetes 클러스터는 여러 노드로 구성되어 있는데, 기본적인 작업 단위라고 할 수 있는 파드는 여러 노드 중 특정 노드에 배치되어 동작하게 된다.
    - 이 때 새로 생성된 파드를 감지하여 어떤 노드로 배치할지 결정하는 작업을 스케줄링이라 하며, 이를 담당하는 컴포넌트가 kube-scheduler이다.
    - 스케줄링을 위해 노드 및 파드의 각종 요구사항과 제약사항을 종합적으로 판단할 필요가 있는데, 이러한 판단 또한 kube-scheduler의 역할이다.
  - kube-controller-manager
    - Kubernetes 클러스터에 다운된 노드가 없는지, 파드가 의도한 replica 숫자를 유지하고 있는지, 서비스와 파드는 적절하게 연결되었는지, 네임스페이스에 대한 기본 계정과 토큰이 생성되어 있는지를 확인하는 역할을 한다.
    - 만약 적절하지 않은 부분이 발견되면 적절한 수준을 유지하기 위해 조치를 취하는 역할을 한다.



- Node component

  - kubelet(쿠블릿)
    - 노드에서 컨테이너가 동작하도록 관리해 주는 핵심 요소이다.
    - 각 노드에서 파드를 생성하고 정상적으로 동작하는지 관리하는 역할을 한다.
    - 실제로 Kubernetes의 워크로드를 관리하기 위해 내리는 명령은 kubelet을 통해 수행된다고 볼 수 있다.
    - Kubernetes 파드를 관리하기 위해 작성하는 YAML을 쿠버네티스 클러스터에 적용하기 위해 kubectl 명령어를 사용할 때, 이 YAML이 kube-apiserver로 전송된 후 kubelet으로 전달된다.
    - kubelet은 이 YAML을 통해 전달된 파드를 생성 혹은 변경하고, 이후 YAML에 명시된 컨테이너가 정상적으로 실행되고 있는지 확인한다.

  - container runtime
    - 파드에 포함된 컨테이너 실행을 실질적으로 담당하는 애플리케이션이다.
    - 컨테이너 런타임은 쿠버네티스 구성 요소에 기본적으로 포함되어 있거나, 특정 소프트웨어를 지칭하는 것은 아니다.
    - Kubernetes가 컨테이너를 제어하기 위해 제공하는 표준 규약인 컨테이너 런타임 인터페이스(Container Runtime Interface, CRI)를 준수하여 Kubernetes 와 함께 사용할 수 있는 외부 애플리케이션들을 의미한다.
    - Kubernetes는 컨테이너 관리를 위해 특정 애플리케이션을 사용할 것을 강제하지는 않고, 단지 Kubernetes 가 제공하는 규약에 따라 Kubernetes 와 연계할 것을 요구한다.
    - Kubernetes 1.24부터 Docker는 container runtime으로 사용할 수 없게 되었다.
  - kube-proxy
    - Kubernetes 클러스터 내부에서 네트워크 요청을 전달하는 역할을 한다.
    - Kubernetes 파드 IP는 파드가 배포될 때마다 매번 바뀌기 때문에, IP를 통해 파드에 요청을 전달하는 것은 쉽지 않다.
    - Kubernetes는 파드가 매번 바뀌는데서 오는 어려움을 해결하기 위해 오브젝트를 통해 고정적으로 파드에 접근할 수 있도록 하는 방법을 제공한다.
    - 그리고 서비스로 들어온 요청이 파드에 실제로 접근할 수 있는 방법을 관리한다.
    - 이 때 관리를 담당하는 컴포넌트가 kube-proxy이다.
    - 즉 파드의 IP는 매번 변하지만 kube-proxy가 이 파드에 접근할 수 있는 방법을 그때마다 관리하고 갱신하며, 서비스 오브젝트는 이 정보를 사용하여 파드가 외부에서 접근할 수 있는 경로를 제공한다.
