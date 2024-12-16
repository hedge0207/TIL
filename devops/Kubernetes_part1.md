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





## minikube 사용해보기

- minukube 실행하기

  - [minikube 사이트](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download)에서 minikube 설치 파일을 다운 받는다.
  - minikube 시작하기
    - minukube를 실행하기 위해서는 Docker, Hyper-V 등의 container 또는 virtual machine manager가 실행중이어야한다.
    - `--nodes` flag를 통해 node의 개수를 설정할 수 있다(기본값은 1).
    - `-p` flag를 통해 minikube VM이 사용할 이름을 설정할 수 있다(기본적 값은 minikube).

  ```bash
  $ minikube start
  ```

  - minikube dashboard 열기
    - 아래 명령어 실행시 자동으로 웹 브라우저가 열린다.
    - 만약 자동으로 웹 브라우저가 열리는 것을 원치 않는다면 `--url` 옵션을 주면되며, 이 경우 접속을 위한 url만 출력한다.
    - 만약 위에서 `-p` option을 준 경우 -p로 profile도 함께 지정해줘야한다.

  ```bash
  $ minikube dashboard
  ```




- minikube 명령어

  - Pause
    - 배포된 application에는 영향을 미치지 않고, Kubernetes를 일시 정지한다.

  ```bash
  $ minikube pause
  ```

  - Unpause

  ```bash
  $ minikube unpause
  ```

  - Stop
    - Cluster를 정지한다.

  ```bash
  $ minikube stop
  ```

  - Memory limit 변경
    - Memoery limit을 변경한다.
    - 실행 후 재시작을 해야 한다.

  ```bash
  $ minikube config set memory 9001
  ```

  - 이전 버전의 Kubernetes로 실행되는 cluster를 생성한다.

  ```bash
  $ minikube start -p aged --kubernetes-version=v1.16.1
  ```

  - 모든 minikube cluster를 삭제한다.

  ```bash
  $ minikube delete --all
  ```

  - minikube docker daemon에 연결하기
    - `minikube docker-env` 명령어는 터미널의 Docker CLI가 minikube 내부의 Docker engine을 가리키려면 어떻게 해야 하는지 출력하는 명령어이다.
    - `eval`을 통해 이 명령어들을 수행함으로써 터미널의 Docker CLI가 minikube 내부의 Docker engine을 가리키도록 한다.

  ```bash
  $ eval $(minikube docker-env)
  ```



- Deployment 생성하기

  - Deployment는 Pod들을 관리하고 scaling하는 데 도움을 준다.

    - Kubernetes Deployment는 Pod들의 상태를 확인하고, Pod의 container에 문제가 있을 경우 container를 재실행한다.

  - Deployment 생성

    > Windows의 경우 CMD에서 실행해야 한다.

    - `kubectl create` 명령어를 사용하여 Pod를 관리할 deployment를 생성한다.
    - `--`는 `kubectl` 명령어와 container의 실행 명령어를 구분하는 구분자이다.
    - `/agnhost netexec`는 container가 시작될 때 실행할 명령이다.
    - `--http-port`는 `netexec` 명령어의 인수이다.

  ```bash
  $ kubectl create deployment hello-node --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- /agnhost netexec --http-port=8080
  
  # 위 명령어는 아래와 같은 형식이다.
  $ kubectl <command> <resource_type> <resource_name> --image <image> -- <container_command> <container_command_arguments>
  ```

  - Deployment 확인
    - 가용해질 때 까지 시간이 좀 걸리므로, 만약 `READU`가 `0/1`이라면 잠시 후에 다시 시도하면 된다.

  ```bash
  $ kubectl get deployments
  
  # output
  NAME         READY   UP-TO-DATE   AVAILABLE   AGE
  hello-node   1/1     1            1           1m
  ```

  - Pod 확인하기

  ```bash
  $ kubectl get pods
  
  # output
  NAME                          READY     STATUS    RESTARTS   AGE
  hello-node-5f76cf6ccf-br9b5   1/1       Running   0          1m
  ```

  - Cluster event 확인하기

  ```bash
  $ kubectl get events
  ```

  - `kubectl` 설정 확인하기

  ```bash
  $ kubectl config view
  ```

  - Pod 내의 container에 대한 application log 확인

  ```bash
  $ kubectl logs hello-node-5f76cf6ccf-br9b5
  ```



- Service 생성하기

  - Kubernetes Service
    - 기본적으로, Pod는 오직 Kubernetes cluster내의 internal IP 주소로만 접근이 가능하다.
    - 위에서 생성한 `hello-node` container에 Kubernetes virtual network 외부에서도 접근할 수 있게 하려면 Pod를 Kubernetes Service로 expose해야한다.
  - Pod를 public internet으로 expose하기
    - `--type=LoadBalancer` flag는 Service를 cluster 외부로 expose하겠다는 것을 의미한다.

  ```
  kubectl expose deployment hello-node --type=LoadBalancer --port=8080
  ```

  - 생성한 service 확인하기

  ```bash
  $ kubectl get services
  
  # output
  NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
  hello-node   LoadBalancer   10.102.142.18   <pending>     8080:30369/TCP   21s
  kubernetes   ClusterIP      10.76.0.2       <none>        443/TCP          23m
  ```

  - `minikube`로 service에 연결하기

  ```bash
  $ minikube service hello-node
  ```



- Addon 활성화하기

  - minikube에는 addons들이 내장되어 있다.
    - 아래 명령어를 통해 addon들을 확인할 수 있다.

  ```bash
  $ minikube addons list
  ```

  - Addon 활성화하기

  ```bash
  $ minikube addons enable <addon>
  
  # e.g.
  $ minikube addons enable metrics-server
  ```

  - Addon을 설치하면서 생성된 Pod와 Service 확인하기

  ```bash
  $ kubectl get pod,svc -n kube-system
  ```

  - 위에서 설치한 `metrics-server`의 output 확인하기

  ```bash
  $ kubectl top pods
  ```

  - Addon 비활성화하기

  ```bash
  $ minikube addon disable <addon>
  
  # e.g.
  $ minikube addons disable metrics-server
  ```







# Kubernetes 기초

- 배포할 application 생성하기

  - FastAPI application 작성

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  @app.get("/ping")
  def ping():
      return "pong"
  
  if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0", port=8098)
  ```

  - `requirements.txt` 작성

  ```txt
  pydantic==2.5.3
  pydantic_core==2.14.6
  pydantic-settings==2.1.0
  uvicorn==0.27.0.post1
  fastapi==0.109.0
  requests==2.31.0
  ```

  - Dockerfile 작성

  ```dockerfile
  FROM python:3.12.0
  
  COPY ./main.py /main.py
  COPY ./requirements.txt /requirements.txt
  
  RUN pip install -r requirements.txt
  
  ENTRYPOINT ["/bin/bash", "-c", "python -u main.py"]
  ```

  - Image build

  ```bash
  $ docker build -t ghcr.io/<user_name>/test-app:1.0.0 .
  ```

  - Kubernetes는 기본적으로 Docker Hub나 컨테이너 레지스트리에서 이미지를 가져온다.
    - 따라서 위와 같이 local에 image를 build하더라도 Kubernetes가 찾을 수 없다.
    - 사용을 위해선 Docker hub 등에 image를 push해야한다.
    - Docker registry를 local에 띄워서 사용하는 방식의 경우, local에 설치된 Docker registry가 https를 사용하도록 변경해줘야한다.
  - 위 이미지를 Github container registry에 push 한다.
    - 그 후, 별도의 인증 없이 kubectl에서 image에 접근하기 위해서 image의 visibility를 public으로 변경한다(선택).

  ```bash
  $ docker push ghcr.io/<user_name>/test-app:1.0.0
  ```



- Cluster 생성하기

  - Kubernetes cluster
    - Kubernetes는 컴퓨터들을 연결하여 단일 형상으로 동작하도록 컴퓨팅 클러스터를 구성하고 높은 가용성을 제공하도록 조율한다.
    - Kubernetes는 container화 된 application을 cluser에 배포할 수 있도록 해주는데, 이를 위해서는 application이 host machine과 분리되어 packaging되어야 한다(즉, host에 종속되어서는 안 된다).
    - Kubernetes는 cluster내에 있는 application들의 분배와 scheduling을 자동화해준다.
  - minikube를 사용하여 cluster 생성하기

  ```bash
  $ minikube start
  ```





## Deployment

- Application deploy하기

  > [그림 출처](https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/)

  ![module_02_first_app](Kubernates.assets/module_02_first_app.svg)

  - Kubernetes Deployments
    - Container화된 application을 Kubernetes cluster에 배포하기 위해서는 Kubernetes Deployment를 생성해야한다.
    - Deployment는 Kubernetes에게 어떻게 application의 instance를 생성하고 수정할지를 지시하는 역할을 한다.
    - Deployment가 한 번 생성되면, Kubernetes control plane은 Deployment에 포함된 application instance를 scheduling하여 cluster 내의 node에서 실행될 수 있도록 한다.
    - Application의 instance가 생성되면 Kubernetes Deployment controller는 지속적으로 해당 instance를 monitoring한다.
    - 먄약 instance를 hosting하던 Node에 문제가 생길 경우, Deployment controller는 instance를 cluster내의 다른 Node에 있는 instance로 대체한다.
  - Deployment 생성하기
    - 아래 명령어가 실행되면 application의 instance가 실행될 적합한 Node를 찾는다.
    - 그 후 위에서 찾은 Node에서 실행시키기 위해 application을 scheduling한다.
    - 필요할 때 새 노드에서 인스턴스를 다시 scheduling하도록 클러스터를 설정한다.

  ```bash
  $ kubectl create deployment <deployment_name> --image=<image>
  
  # e.g.
  $ kubectl create deployment test-deployment --image ghcr.io/<user_name>/test-app:1.0.0
  ```

  - Deployment 확인하기

  ```bash
  $ kubectl get deployments
  ```

  - `kubectl proxy`
    - 기본적으로 Kubernetes cluster 외부에서는 cluster 내부로 요청하는 것이 불가능하다.
    - 그러나 `kubectl proxy` 명령어를 통해 요청을 cluster로 forward하는 proxy를 생성할 수 있다.
    - `--port`로 port를 설정할 수 있으며, 기본 port는 8001이다.

  ```bash
  $ kubectl proxy
  ```

  - Proxy 테스트하기

  ```bash
  $ curl localhost:8001/version
  ```

  - API server는 각 Pod에 대한 endpoint를 자동으로 생성한다.
    - 이 endpoint 역시 proxy를 통해 접근 가능하다.

  ```bash
  $ curl http://localhost:8001/api/v1/namespaces/default/pods/test-deployment-2985we4287-8cgrh
  ```

  - 우리가 위에서 deploy한 app에도 접근할 수 있다.
    - 아래에서 살펴볼 Service를 생성할 경우 proxy 없이 접근이 가능해진다.

  ```bash
  $ curl http://localhost:8001/api/v1/namespaces/default/pods/test-deployment-2985we4287-8cgrh:8098/proxy/ping
  # "pong"
  ```

  - Pod의 container에 bash session을 연결할 수도 있다.

  ```bash
  $ kubectl exec -it <pod_name> -- bash
  ```



- Pod 확인하기

  > [그림 출처](https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/)

  ![module_03_pods](Kubernates.assets/module_03_pods.svg)

  - Pod
    - Deployment를 생성하면 Kubernetes는 Pod를 생성한다.
    - Pod는 application instance를 hosting하는 역할을 한다.
    - Pod는 하나 혹은 그 이상의 application container들의 집합이다.
    - Pod는 자신이 scheduling된 Node에 묶이게 되며, 종료될 때 까지 해당 Node에 남아있는다.
    - 만약 Node에 문제가 발생할 경우, 동일한 Pod가 cluster 내의 가용한 Node로 scheduling된다.
  - 같은 Pod에 속한 container들은 일부 resource를 공유하기도 한다.
    - Volume 형태로 storage를 공유한다.
    - Cluster IP address를 공유한다.
    - 각 container가 어떻게 실행되었는지(container image version, 사용하는 port 등)를 공유한다.
  - Pod 확인

  ```bash
  $ kubectl get pods
  ```

  - Pod 상세 정보 보기

  ```bash
  $ kubectl describe pods
  ```



- Node

  - Node는 Kubernetes의 worker machine이며 VM일 수도 있고, physical machine일 수도 있다.

    - 각 Node는 control plane에 의해 관리된다.
    - 모든 Pod는 Node 내에서 실행되며, 하나의 Node는 여러 개의 Pod를 가질 수 있다.
    - Control plane은 cluster 내의 Node들에서 실행될 Pod들의 scheduling을 자동으로 실행한다.
    - Control plane은 scheduling을 수행할 때 각 Node의 가용한 자원을 고려한다.

  - 모든 Kubernetes Node는 최소한 아래 두 개를 수행한다.

    - Kubelet: Node와 control plane사이의 통신을 담당하며, Node에서 실행중인 Pod들과 그 container들을 관리한다.

    - Container runtime: Registry로 부터 container를 pulling하고, container를 unpacking하며 application을 실행하는 역할을 한다.





## Service

- Kubernetes Service
  - Service
    - Kubernetes Service는 Pod들의 논리적 집합과, Pod이 접근하는 정책에 대한 정의이다.
    - Service는 traffic을 Pod들에게 route한다.
    - Service는 서로 의존관계에 있는 Pod들을 찾아내고 routing하는 역할을 한다.
    - Service를 통해 의존 관계에 있는 Pod들이 느슨하게 연결될 수 있다.
    - 각각의 Pod는 같은 Node에 속해있다 할지라도 고유한 IP를 가진다.
    - 이 IP들은 Service 없이는 cluster 내부로 노출되지 않는다.
  - Service는 아래와 같이 다양한 방식으로 노출이 가능하다.
    - ClusterIP(default): Service를 cluster 내의 internal IP에 노출한다. 이 방식은 cluster 내에서만 Service에 접근할 수 있도록 한다.
    - NodePort: NAT를 사용하여 cluster 내의 각 선택된 Node의 동일한 포트에 서비스를 노출한다. cluster 외부에서 `<NodeIP>:<NodePort>` 형식으로 접근할 수 있도록 한다.
    - LoadBalancer: 현재 cloud에 external load balancer를 생성하고, Service에 고정된 external IP를 할당한다.
    - ExternalName: Service를 `externalName` field의 값(e.g. foo.example.com)에 mapping한다.
  - Label
    - Service가 Pod들을 matching시킬 때 사용하는 거이 label과 selector이다.
    - Label은 key/value 쌍으로 이루어져 있으며, 당야한 방식으로 사용될 수 있다.



- Service 사용하기

  - Service 목록 확인
    - 목록을 확인해보면 `kubernetes`라는 생성한 적 없는 service가 보일텐데, 이는 minikube가 cluster를 시작할 때 기본으로 생성되는 service이다.

  ```bash
  $ kubectl get services
  ```

  - Service 생성
    - `type`은 `NodePort`로 생성한다.
    - 위에서 배포한 app이 사용하는 8098 port를 `--port` flag에 입력한다.

  ```bash
  $ kubectl expose deployment/test-deployment --type="NodePort" --port 8098
  ```

  - `NodePort` type으로 설정했을 때, 몇 번 port가 외부에 open되었는지를 확인하려면 아래와 같이 하면 된다.

  ```bash
  $ kubectl decribe services/test-deployment
  ```

  - 이제 우리가 생성한 application으로 요청을 보낼 수 있게 된다.

  ```bash
  $ curl http://<minikube_IP>:8098
  ```

  - 만약 Docker Desktop을 container driver로 사용하여 minikube를 실행한다면, minikube tunnel이 필요하다.
    - 이는 Docker Desktop의 container가 host computer로부터 격리되어 있기 때문이다.

  ```bash
  # 먼저 아래 명령어를 실행한다.
  $ minikube service test-deployment --url
  
  # 위 명령어를 실행하면 ttp://127.0.0.1:51082와 같은 url이 나올텐데, 위 명령어를 실행한 창을 그대로 띄워둔 상태에서 출력된 url로 요청을 보내면 된다.
  $ curl ttp://127.0.0.1:51082/ping
  ```



- Service를 Label과 함께 사용하기

  - Deployment는 자동으로 Pod에 대한 label을 생성한다.
    - 아래 명령어를 실행하면, deployment에 대한 설명이 나오는데, `Labels` 항목에서 label을 확인할 수 있다.

  ```bash
  $ kubectl describe deployment
  ```

  - Pod 정보 확인하기
    - 위에서 얻은 label 정보로 Pod의 정보를 확인한다.
    - `-l` flag 뒤에 label을 입력한다.

  ```bash
  $ kubectl get pods -l app=test-deployment
  ```

  - Service 정보 확인하기
    - 위에서 얻은 label 정보로 Service 정보를 확인한다.
    - `-l` flag 뒤에 label을 입력한다.

  ```bash
  $ kubectl
  ```

  - Pod에 새로운 label 적용하기
    - 아래와 같이 `kubectl label` 명령어를 사용하여 Pod에 새로운 label을 적용할 수 있다.

  ```bash
  $ kubectl label pods <pod_name> <key>=<value>
  
  # e.g.
  $ kubectl label pods test-deployment-2985we4287-8cgrh foo=bar
  ```

  - 새로 적용된 label 확인하기
    - 기존 label 외에 새로운 label이 추가된 것을 확인할 수 있다.

  ```bash
  $ kubectl describe pods test-deployment-2985we4287-8cgrh
  ```



- Service 삭제하기

  - Service 삭제

  ```bash
  $ kubectl delete service -l app=test-deployment
  ```

  - 삭제되었는지 확인

  ```bash
  $ kubectl get services
  ```

  - Route가 더 이상 expose 되지 않는지 확인하기
    - Docker desktop을 minikube container engine으로 사용할 경우 `minikube service test-deployment --url`를 통해 출력된 url로 요청을 보내봐야 한다.
    - 요청이 실패하면 더 이상 expose 되지 않는 것이다.

  ```bash
  $ curl http://<minikube_IP>:8098
  ```

  - Application에는 문제가 없는지 확인하기
    - Service 삭제 이후에 application에 문제가 없는지 확인하기 위해, cluster 내부에서 application으로 요청을 보내본다.

  ```bash
  $ kubectl exec -ti test-deployment-2985we4287-8cgrh -- curl http://localhost:8098
  ```



- Headless Service
  - `spec.clusterIP`를 `None`으로 설정한 Service를 Headless Service라 한다.
    - Cluster IP가 할당되지 않기 때문에 kube-proxy는 이 Service를 처리하지 않는다.
    - 또한 load balancing이나 proxing 역시 실행되지 않는다.
  - 사용하는 이유
    - 일반적으로 client에서 Pod로 가는 요청은 Service를 거치며, Service는 client로부터 요청을 받아서 Pod 중 하나에 요청을 전달한다.
    - 그러나 Headless Service의 경우 client가 자신이 원하는 Pod에 직접 요청을 보낼 수 있게 해준다.
    - 만약 모든 Pod들과 통신해야 하는 client가 있다고 가정했을 때, 이 client는 모든 Pod의 IP주소를 알아야한다.
    - 모든 Pod의 IP 주소를 알아내기 위해 Kubernetes API로 요청을 보내 해당 Pod들의 IP를 받아올 수도 있겠으나, 이는 client가 Kubernetes에 의존성이 생기는 것이므로 바람직한 방법은 아니다.
    - Kubernetes의 DNS Lookup을 통해 client에게 Pod IP 목록을 알려줄 수 있다.
    - 특정 Service에 대해 DNS Lookup을 수행하면 DNS 서버는 Service의 Cluster IP 하나를 반환한다.
    - 그러나 Headless Servie는 Cluster IP가 없으므로, Headless Service에 대한 DNS Lookup 요청이 DNS 서버에 들어가면, Service에 소속된 Pod IP 목록을 전부 반환한다.
    - Client는 이를 받아 이를 순회하면서 다시 DNS Lookup을 수행하고 Pod들의 IP를 알 수 있게된다.





## Scale Application

- Scale App
  - 여러 개의 instance가 실행되도록 scale up할 수 있다.
    - 새로운 Pod를 생성하고, traffic이 각 Pod로 분산되도록 하면 된다.
    - 새로운 Pod의 생성은 Deployment를 수정하면 가능하고, traffic이 각 Pod로 분산되도록 하는 것은 Service를 `LoadBalancer` type으로 생성하면 가능하다.
  - Service는 실행 중인 Pod들을 지속적으로 monitoring하고 요청을 받을 수 있는 Pod에게만 요청을 분산한다.



- Scaling a Deployment

  - Deployment를 확인한다.
    - `NAME`은 cluster 내의 Deployment의 이름을 보여준다.
    - `READY`는 CURRENT/DESIRED replica의 비율을 보여준다.
    - `UP-TO-DATE`는 desired state를 달성하기 위해 update 되어야 하는 replica의 수를 보여준다.
    - `AVAILABLE`은 application의 replica 중 얼마나 많은 수가 사용 가능한지를 보여준다.
    - `AGE`는 application이 실행 중인 시간을 보여준다.

  ```bash
  $ kubectl get deployments
  ```

  - ReplicaSet 확인하기
    - 아래 명령어를 통해 Deployment가 생성한 ReplicaSet을 확인할 수 있다.
    - `DESIRED`는 application의 instance 중 Deployment를 생성할 때 설정한 desired number를 보여준다.
    - `CURRENT`는 현재 실행 중인 replica의 수를 보여준다.

  ```bash
  $ kubectl get rs
  ```

  - Deployment를 scale하기
    - `kubectl scale` 명령어를 통해 instance의 desired number를 설정할 수 있다.

  ```bash
  $ kubectl scale deployments/test-deployment --replicas=4
  ```

  - Deployment 다시 확인하기
    - 출력 되는 값이 달라진 것을 확인할 수 있다.

  ```bash
  $ kubectl get deployments
  ```

  - Pod의 개수가 달라졌는지 확인하기

  ```bash
  $ kubectl get pods -o wide
  ```

  - 변경 사항은 Deployment events log에 기록된다.
    - 아래 명령어를 통해 확인이 가능하다.
    - `Events` 항목을 확인하면 된다.

  ```bash
  $ kubectl describe deployments/test-deployment
  ```



- Load Balancing

  - Load balancing을 위한 Service를 생성한다.
    - 생성한 후 시간이 지나도 계속 pending 상태일 텐데, 이는 external load balancer를 사용하지 않아서 그런 것이다.
    - 이 경우에도 테스트에는 문제가 없다.

  ```bash
  $ kubectl expose deployment/test-deployment --type="LoadBalancer" --port 8098
  ```

  - 요청을 보내고, 각 Pod의 log를 확인해보면, 각 Pod로 요청이 분배되는 것을 확인할 수 있다.

  ```bash
  $ kubectl logs <pod_name>
  ```



- Scale in

  - Scale out 때와 마찬가지로 `kubectl scale` 명령어를 사용하면 된다.
    - 기존 4개에서 2개로 줄인다.

  ```bash
  $ kubectl scale deployments/test-deployment --replicas=2
  ```

  - 확인하기

  ```bash
  $ kubectl get pods -o wide
  ```





## Rolling Update

- Rolling update
  - 필요성
    - 사용자는 항상 서비스에 접근할 수 있기를 원한다.
    - 개발자는 하루에도 여러 번 새로운 버전을 배포하기를 원한다.
    - 따라서 서비스의 중단 없이도 새로운 버전을 배포할 수 있어야 하는데 rolling update를 통해 이를 해결할 수 있다.
  - Kubernetes에서의 rolling update
    - Kubernetes는 기존의 Pod를 새로운 Pod로 교체하는 방식으로 rolling update를 수행한다.
    - 새로운 Pod는 가용한 자원과 함께 Node에 schedule된다.
    - Kubernetes에서 update는 version으로 기록되고, 이전 version으로 되돌리는 것도 가능하다.



- Update용 image 준비하기

  - `main.py` 파일을 수정한다.
    - `/foo` endpoint를 추가한다.

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  @app.get("/ping")
  def ping():
      return "pong"
  
  @app.get("/foo")
  def foo():
      return "bar"
  
  if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0", port=8098)
  ```

  - 새로운 tag를 붙여서 build한다.

  ```bash
  $ docker build -t ghcr.io/<user_name>/test-app:1.1.0 .
  ```

  - Github container registry에 push한다.

  ```bash
  $ docker push ghcr.io/<user_name>/test-app:1.1.0
  ```



- Rolling update 실행하기

  - 먼저 현재 image의 버전을 확인한다.
    - `Containers.<deployment_name>.Image`를 확인하면 된다.

  ```bash
  $ kubectl describe pods
  ```

  - Image를 변경한다.
    - `kubectl set image` 명령어를 통해 변경이 가능하다.

  ```bash
  $ kubectl set image deployments/<deployment_name> <container_name>=<image>:<tag>
  
  # e.g.
  $ kubectl set image deployments/test-deployment test-app=ghcr.io/<user_name>/test-app:1.1.0
  ```

  - 확인하기
    - 새로 추가된 `/foo` endpoint로 요청을 보내본다.

  ```bash
  $ curl http://<minikube_IP>:8098/foo
  ```

  - Update 확정하기
    - `kubectl rollout status`를 통해 update를 확정할 수 있다.

  ```bash
  $ kubectl rollout status deployments/test-deployment
  ```



- Roll back하기

  - 아래 명령어를 통해 roll back이 가능하다.

  ```bash
  $ kubectl rollout undo deployments/test-deployment
  ```

  - 다시 원래 image로 돌아왔는지 확인한다.

  ```bash
  $ kubectl describe pods
  ```







# Volume

- Volume
  - Volume이 필요한 이유
    - Container 내부의 file들은 일시적이다.
    - 따라서 container가 정지되면, container 내부에 저장된 모든 파일들은 사라지게 된다.
    - 또한 하나의 Pod에 여러 container가 file을 공유해야 하는 경우, volume 없이 이를 구현하는 것은 매우 까다롭다.
  - Kubernetes는 다양한 종류의 volume을 지원한다.
    - Pod는 다양한 종류의 volume을 동시에 사용할 수 있다.
    - Ephemeral volume은 Pod가 종료되면 함께 사라진다.
    - Persistent volume은 Pod가 종료되도 남아있다.
    - 두 종류의 volume 모두 container가 재실행되더라도 data를 보존한다.
  - Volume을 사용하는 방법
    - `.spec.volumes`에 Pod가 사용할 volume을 정의한다.
    - `.spec.containers[*].volumeMounts`에 위에서 정의한 volume을 어디에 mount할지를 정의한다.
    - Pod 내에서 실행되는 각 container에 대해 각 volume을 어디에 mount할지 개별적으로 지정해줘야한다.





## Persistent Volume

- PersistentVolume(PV)과 PersistentVolumeClaim(PVC)
  - PersistentVolume
    - 관리자에 의해 수동으로 프로비저닝 되거나, Storage Class에 의해 동적으로 프로비저닝된 cluster 내부의 storage이다.
    - PersistentVolume은 Node와 마찬가지로 cluster 내부의 resource이다.
    - PersistentVolume은 Volume과 같은 volume plugin이지만, PersistentVolume을 사용하는 Pod와는 독립적인 lifecycle을 가지고 있다.
  - PersistentVolumeClaim(PVC)
    - PVC는 사용자가 storage에 대해 보내는 요청이다.
    - Pod가 Node의 resource를 사용하는 것 같이, PVC는 PV의 resource를 사용한다.
    - Pod가 특정 level의 resource(CPU, Memory)를 요청할 수 있는 것 같이, claime은 특정한 크기와 access mode(ReadWriteOnce, ReadOnlyMany, ReadWriteMany, ReadWriteOncePod)를 요청할 수 있다.
  - PersistentVolume의 type
    - `csi`: Container Storage Interface(CSI)
    - `fc`: Fiber Channel(FC) storage
    - `hostPath`: HostPath volume은 오직 single node일 때만 동작하며, multi node cluster에서는 동작하지 않는다. Test용으로 사용해야한다.
    - `iscsi`: iSCSI(SCSI over IP) storage
    - `local`: Node에 mount되는 local storage device
    - `nfs`: Networ File System(NFS) storage



- Volume과 claim의 lifecycle
  - PV는 cluster 내부의 resource이고, PVC는 해당 resource에 대한 요청이다.
    - PV와 PVC의 상호작용은 아래와 같은 lifecycle을 따른다.
  - Provisioning
    - PV가 provisioning 되는 방법에는 static한 방법과 dynamic한 방법이 있다.
    - Static한 방법의 경우 cluster 관리자가 PV를 생성한다. PV에는 real storage의 상세 정보가 담겨 있다.
    - Dynamic한 방법은 관리자가 생성한 static PV와 matching되는 PVC 없을 경우, cluster가 PVC에 대한 volume을 동적으로 provisioning한다.
    - Dynamic한 방법의 경우 StorageClass를 기반으로 한다.
    - PVC는 storage class에 요청을 보내는데, 해당 storage class는 관리자에 의해 생성된 상태여야한다.
    - 만약 claim이 `""`로 설정된 class에 요청을 보낼 경우, dynamic provisioning은 비활성화 된다.
    - Storage class 기반의 dynamic storage provisioning을 활성화하기 위해서는, API server의 `DefaultStorageClass` admission contoller가 활성화 되어야 한다.
  - Binding
    - Control plan의 control loop는 새로운 PVC가 있는지 지켜보다 matching되는 PV가 있으면, 그 둘을 binding한다.
    - 만약 PV가 새로운 PVC에 대해 동적으로 provisioning된 경우, control loop는 항상 PV를 PVC와 binding한다.
  - Using
    - Pod는 claim을 통해 volume을 사용한다.
    - Cluster는 claim을 검사하여 bound된 volume을 찾고, 해당 volume을 Pod에 mount한다.



- Persistent Volume

  - PV 설정
    - 각 PV는 volume의 spec과 상태를 포함하고 있다.
    - PersistentVolume object의 이름은 반드시 유효한 DNS subdomain name이어야 한다.

  ```yaml
  apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: pv0003
  spec:
    capacity:
      storage: 5Gi
    volumeMode: Filesystem
    accessModes:
      - ReadWriteOnce
    persistentVolumeReclaimPolicy: Recycle
    storageClassName: slow
    mountOptions:
      - hard
      - nfsvers=4.1
    nfs:
      path: /tmp
      server: 172.17.0.2
  ```

  - `spec.capacity`

    - 일반적으로 PV는 특정한 storage capacity를 가지고 있으며, 이 값은, `spec.capacity`를 통해 설정할 수 있다.
    - 현재로서는 storage size가 유일한 설정이다.

  - `spec.volumeMode`

    - PV의 경우 `Filesystem`과 `Block`이라는 두 개의 mode를 설정할 수 있다(기본 값은 `Filesystem`).
    - `Filesystem`으로 설정할 경우 volume이 Pod의 directory에 mount된다.
    - `Block`으로 설정하면 volume을 raw block device로 사용할 수 있으며, 이 경우 volume은 Pod에 filesystem 없이 block device로 제공된다.

  - `spec.accessModes`

    - `ReadWriteOnce`(`RWO`): Volume을 단일 node에 read-write로 mount한다.
    - `ReadOnlyMany`(`ROX`): 여러 node에 read-only로 mount한다.
    - `ReadWriteMany`(`RWX`): 여러 node에 read-write로 mount한다.
    - `ReadWriteOncePod`(`RWOP`): 단일 Pod에 read-write로 mount한다.

  - `spec.persistentVolumeReclaimPolicy`

    - `Retain`: 수동 reclamation
    - `Recycle`: basic scrub(`rm -rf /<volume>/*`)
    - `Delete`: volume 삭제

  - `spec.storageClassName`

    > 과거에는 `volume.beta.kubernetes.io/storage-class`를 사용했으나, deprecate 될 예정이다.

    - `spec.storageClassName`에 StorageClass의 이름을 설정하여 PV의 class를 설정할 수 있다.
    - 특정 class의 PV는 오직 해당 class에 요청을 보내는 PVC에만 binding될 수 있다.
    - `spec.storageClassName`이 없는 PV는 특정 class에 요청을 보내지 않는 PVC에만 binding될 수 있다.



- PersistentVolumeClaim

  - PVC 설정
    - 각 PVC는 각각의 spec과 status를 포함하고 있다.
    - PVC object의 이름은 유효한 DNS subdomain name이어야한다.

  ```yaml
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: myclaim
  spec:
    accessModes:
      - ReadWriteOnce
    volumeMode: Filesystem
    resources:
      requests:
        storage: 8Gi
    storageClassName: slow
    selector:
      matchLabels:
        release: "stable"
      matchExpressions:
        - {key: environment, operator: In, values: [dev]}
  ```

  - `spec.accessModes`
    - PV와 동일하다.
  - `spec.volumeMode`
    - PV와 동일하다.
  - `spec.resources`
    - Pod와 마찬가지로 claim 역시 특정한 양의 resource를 요청할 수 있다.
    - 설정 방식은 PV의 `spec.capacity`와 동일하다.
  - `spec.storageClassName`
    - Claim은 StorageClass의 이름을 `spec.storageClassName`에 정의하여 특정 class에 요청을 보낼 수 있다.
    - PVC와 동일한 `spec.storageClassName`을 가진 PV만 PVC에 binding될 수 있다.
    - PVC가 꼭 class에 요청을 보내야 하는 것은 아니다.
    - `spec.storageClassName`이 `""`로 설정된 PVC는 class가 설정되지 않은 PV에 요청을 보내는 것으로 해석되므로, class가 지정되지 않은 PV에만 binding 될 수 있다.
  - `spec.selector`
    - Claim은 여러 volume들을 filtering하기 위해 label selector를 설정할 수 있다.
    - `matchLabels`: Volume에 이 값에 해당하는 label이 있어야한다.
    - `matchExpressions`: key, value 목록, key와 value를 연결하는 연산자를 지정하여 만든 requirements 목록으로, 유효한 연산자에는 `In`, `NotIn`, `Exists`, `DoesNotExist`가 있다.





## Ephemeral Volume

- Ephemeral volume
  - Pod의 lifecycle을 따르는 volume이다.
    - 즉, Pod가 생성될 때 함께 생성되고, Pod가 삭제될 때 함께 삭제된다.
  - 주요 용도
    - Application에 추가적인 storage가 필요하지만, 그 곳에 저장되는 데이터가 영구적으로 저장될 필요는 없는 경우.
    - 예를 들어 caching application을 사용하려고 하는데, memory에 더 이상 여유가 없고, caching 속도가 memory에 비해 조금 느려도 무방하다면, Ephemeral volume을 사용하는 것을 고려할 수 있다.
    - 또는 설정 파일이나 secret key 등의 data가 read-only로 file 형태로 저장되어야 할 경우에도 사용할 수 있다.
  - Ephemeral volume의 type
    - `emptyDir`: 처음 생성될 때 비어 있는 volume.
    - `configMap`, `downwardAPI`, `secret`: Kubernetes의 data를 Pod에 주입하기 위해 사용하는 volume.
    - `CSI ephemeral volumes`: CSI driver에 의해 제공되는 volume.
    - `generic ephemeral volumes`: 모든 storage driver에 의해 제공되는 volume.



- Ephemeral volume 생성하기

  - PV 혹은 PVC와는 달리 Pod 생성시에 inline으로 생성한다.
  - Generic ephemeral volume을 생성하는 예시이다.

  ```yaml
  kind: Pod		# Pod를 생성할 때 함께 생성한다.
  apiVersion: v1
  metadata:
    name: my-app
  spec:
    containers:
      - name: my-frontend
        image: busybox:1.28
        volumeMounts:
        - mountPath: "/scratch"
          name: scratch-volume
        command: [ "sleep", "1000000" ]
    volumes:
      - name: scratch-volume
        ephemeral:
          volumeClaimTemplate:
            metadata:
              labels:
                type: my-frontend-volume
            spec:
              accessModes: [ "ReadWriteOnce" ]
              storageClassName: "scratch-storage-class"
              resources:
                requests:
                  storage: 1Gi
  ```





## Storage Class

- StorageClass
  - StorageClass는 아래와 같은 field들을 가지고 있으며, 이 값들 PVC를 충족하는 PV를 동적으로 provisioning할 때 사용한다.
    - `provisioner`
    - `parameters`
    - `reclaimPolicy`
  - 아래와 같은 순서로 동작한다.
    - StorageClass 정의.
    - StorageClass를 참조하는 PVC 생성.
    - PVC의 StorageClass 설정에 따라 PV가 동적으로 provisioning.
    - Pod가 PVC를 mount하여 storage를 사용.
  - 사용자가 특정 class에 요청을 보낼 때, StorageClass의 이름을 사용하므로 이름을 잘 지어야한다.
    - StorageClass가 생성될 때 관리자가 이름을 포함한 다른 parameter들을 설정한다.



- StorageClass 예시

  - 설정 파일

  ```yaml
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
  metadata:
    name: low-latency
    annotations:
      storageclass.kubernetes.io/is-default-class: "false"
  provisioner: csi-driver.example-vendor.example
  reclaimPolicy: Retain
  allowVolumeExpansion: true
  mountOptions:
    - discard
  volumeBindingMode: WaitForFirstConsumer
  parameters:
    guaranteedReadWriteLatency: "true"
  ```

  - `provisioner`
    - 모든 StorageClass는 어떤 volume plugin을 사용하여 PV를 provisioning할 것인지를 결정하는 `provisioner` field가 설정되어야한다.
    - Provisioner에는 Kubernetes가 제공하는 internal provisioner와 Kubernetes spec에 따라 외부에서 만들어진 external provisioner가 있다.
    - Internal provisioner는 `kubernetes.io`라는 prefix가 붙어있다.

  - `reclaimPolicy`
    - StorageClass에 의해 동적으로 생성된 PV의 reclaim policy는 StorageClass의 `reclaimPolicy ` field에 따라 결정된다.
    - `reclaimPolicy`는 `Delete`나 `Retain` 둘 중 하나의 값을 가질 수 있으며, 기본 값은 `Delete`이다.
    - 수동으로 생성되어 StorageClass에 의해 관리되는 PV에는 PV 생성시에 설정된 reclaim policy가 적용된다.
  - `allowVolumeExpansion`
    - PV는 확장 가능하게 설정될 수 있다.
    - PV에 해당하는 PVC를 수정하여 volume의 크기를 조정할 수 있다.
    - 모든 volume type이 지원하는 것은 아니다.
  - `mountOptions`
    - StorageClass에 의해 동적으로 생성된 PV의 mount option은 StorageClass의 `mountOptions ` field에 따라 결정된다.
    - 만약 volume plugin이 mount option을 지원하지 않음에도 `mountOptions`가 설정되었을 경우, provisioning은 실패하게 된다.
  - `volumeBindingMode`
    - Volume binding과 dynamic provisioning이 언제 실행되어야 하는지를 설정한다.
    - 기본 값은 `Immediate`로, PVC가 생성되는 즉시 volume binding과 dynamic provisioning이 실행된다.
  - `parameters`
    - StorageClass의 volume에 적용할 parameter를 설정한다.
    - `provisioner`에 따라 각기 다른 parameter를 설정해야한다.



- Default StorageClass

  - 하나의 StorageClass를 cluster의 default StorageClass로 설정할 수 있다.
    - PVC에 `storageClassName`을 설정하지 않으면 default StorageClass가 적용된다.
    - 만약 여러 개의 default StorageClass가 설정되었을 경우, Kubernetes는 가장 최근에 생성된 default StorageClass를 사용한다.
    - Cluster에 default StorageClass가 없을 수도 있다.
  - Default StorageClass가 없을 경우에도 `storageClassName`을 설정하지 않고 PVC를 생성할 수 있다.
    - 이 경우 default StorageClass가 생성되기 전까지 `storageClassName`은 아무 값도 없는 상태가 된다.
    - 만약 추후에 defaut StorageClass가 생성되면, control plane은 `storageClassName`이 설정되지 않은(빈 값으로 설정되었거나, 아예 key 자체를 선언하지 않은) 모든 PVC를 찾아낸다.
    - 그 후 control plane은 이러한 PVC에 대해 default StorageClass를 적용한다.
    - 단, 만약 `storageClassName`이 `""`로 설정된 경우, 이러한 PVC에 대해서는 적용되지 않는다.
  - Default StorageClass를 생성하는 방법
    - StorageClass를 생성할 때, 아래와 같이 `metadata.annotations.storageclass.kubernetes.io/is-default-class`의 값을 `"true"`로 설정하면 된다.

  ```yaml
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
  metadata:
    name: low-latency
    annotations:
      storageclass.kubernetes.io/is-default-class: "true"
  provisioner: csi-driver.example-vendor.example
  reclaimPolicy: Retain
  allowVolumeExpansion: true
  mountOptions:
    - discard
  volumeBindingMode: WaitForFirstConsumer
  parameters:
    guaranteedReadWriteLatency: "true"
  ```

  - Default StorageClass를 변경하는 방법
    - 만약 `standard`와 `gold`라는 두 개의 StorageClass가 있고, 현재 default StorageClass가 `standard`라고했을 때, default StorageClass를 `gold`로 바꾸려면 아래와 같이 하면 된다.
    - 기존 default StorageClass의 `storageclass.kubernetes.io/is-default-class` 값을 `"false"`로 변경하고, 새로 default StorageClass로 사용할 StorageClass의 `storageclass.kubernetes.io/is-default-class`값을 `"true"`로 변경한다.

  ```bash
  # 기존 default StorageClass의 설정 변경
  $ kubectl patch storageclass standard -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
  
  # 새로운 default StorageClass의 설정 변경
  $ kubectl patch storageclass gold -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
  ```





# Kubelet을 Standalone mode로 실행하기

- 실행 전 준비

  - Swap memory 비활성화하기
    - 기본적으로 kubelet은 node에 swap memory가 활성화되어 있을 경우 시작되지 않는다.
    - 따라서 kubelet이 swap을 허용하도록 하거나, swap을 비활성화해야한다.
    - 만약 kubelet이 swap을 허용하도록 하고자 한다면, kubelet 설정 파일에 `failSwapOn: false`와 같이 작성하면 된다.

  ```bash
  # Swap이 활성화되어 있는지 확인한다. 아래 명령어를 실행했을 때, 아무 메시지도 출력되지 않으면, 이미 비활성화 되어 있는 것이다.
  $ sudo swapon --show
  
  # Swap 비활성화
  $ sudo swapoff -a
  ```

  - IPv4 packet forwarding 활성화

  ```bash
  # IPv4 packet forwarding이 활성화 되어 있는지 확인한다. 만약 1이 출력되면, 활성화되어 있는 것이다.
  $ cat /proc/sys/net/ipv4/ip_forward
  
  # 활성화하기
  $ sudo tee /etc/sysctl.d/k8s.conf <<EOF
  net.ipv4.ip_forward = 1
  EOF
  
  # 적용하기
  $ sudo sysctl --system
  ```



- Component 설정하기

  - Container runtime 설치하기
    - 여기서는 [CRI-O container runtime](https://github.com/cri-o/cri-o)을 사용한다.
    - 아래 방법 외에도 다양한 설치 방법이 있다.

  ```bash
  # 설치 script 다운
  $ curl https://raw.githubusercontent.com/cri-o/packaging/main/get > crio-install
  
  # 설치
  $ sudo bash crio-install
  
  # crio service 시작
  $ sudo systemctl daemon-reload
  $ sudo systemctl enable --now crio.service
  
  # test
  $ sudo systemctl is-active crio.service
  ```

  - Network plugin 설치
    - `cri-o` installer는 `cni-plugins` package를 설치한다.
    - 아래 명령어를 실행하여 설치 여부를 확인할 수 있다.
    - 설정을 확인했을 때,  subnet range의 값(예시의 경우 10.85.0.0/16)이 현재 활성화된 network와 겹치지 않는지 확인해야한다.
    - 만약 겹칠 경우, 겹치지 않게 설정 파일을 수정한 뒤 service를 다시 시작해야한다.

  ```bash
  # 설치 확인
  $ /opt/cni/bin/bridge --version
  
  # 설정 확인
  $ cat /etc/cni/net.d/11-crio-ipv4-bridge.conflist
  
  # output
  {
    "cniVersion": "1.0.0",
    "name": "crio",
    "plugins": [
      {
        "type": "bridge",
        "bridge": "cni0",
        "isGateway": true,
        "ipMasq": true,
        "hairpinMode": true,
        "ipam": {
          "type": "host-local",
          "routes": [
              { "dst": "0.0.0.0/0" }
          ],
          "ranges": [
              [{ "subnet": "10.85.0.0/16" }]
          ]
        }
      }
    ]
  }
  ```



- Kubelet 설치

  - Kubelet 다운

  ```bash
  $ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubelet"
  ```

  - 설정 파일 만들기
    - 지금은 테스트용으로 kubelet을 실행하므로, 보안과 port 관련 설정을 최대한 단순하게 설정했지만, 실제 운영 환경에서는 아래와 같이 설정해선 안 된다.

  ```bash
  $ sudo mkdir -p /etc/kubernetes/manifests
  $ sudo tee /etc/kubernetes/kubelet.yaml <<EOF
  apiVersion: kubelet.config.k8s.io/v1beta1
  kind: KubeletConfiguration
  authentication:
    webhook:
      enabled: false # 실제 운영 환경에선 이렇게 설정하면 안 된다.
  authorization:
    mode: AlwaysAllow # 실제 운영 환경에선 이렇게 설정하면 안 된다.
  enableServer: false
  logging:
    format: text
  address: 127.0.0.1 # Restrict access to localhost
  readOnlyPort: 10255 # 실제 운영 환경에선 이렇게 설정하면 안 된다.
  staticPodPath: /etc/kubernetes/manifests
  containerRuntimeEndpoint: unix:///var/run/crio/crio.sock
  EOF
  ```

  - 설치

  ```bash
  $ chmod +x kubelet
  $ sudo cp kubelet /usr/bin/
  ```

  - `systemd` service unit file 생성
    - 아래에서 `[Service]`를 설정하는 부분을 보면 `--kubeconfig`가 argument가 빠져있는 것을 볼 수 있다.
    - `--kubeconfig` argument는 kubeconfig file의 경로를 설정하는 것인데, 아래와 같이 이를 설정하지 않으면 standalone mode로 동작하게 된다.

  ```bash
  $ sudo tee /etc/systemd/system/kubelet.service <<EOF
  [Unit]
  Description=Kubelet
  
  [Service]
  ExecStart=/usr/bin/kubelet \
   --config=/etc/kubernetes/kubelet.yaml
  Restart=always
  
  [Install]
  WantedBy=multi-user.target
  EOF
  ```

  - `kubelet` service 시작하기

  ```bash
  $ sudo systemctl daemon-reload
  $ sudo systemctl enable --now kubelet.service
  ```

  - 실행 됐는지 확인

  ```bash
  $ sudo systemctl is-active kubelet.service
  ```

  - Kubelet의 `/healthz` endpoint를 통해 정상 실행중인지 확인

  ```bash
  $ curl http://localhost:10255/healthz?verbose
  
  # output
  [+]ping ok
  [+]log ok
  [+]syncloop ok
  healthz check passed
  ```

  - Kubelet의 `/pods` endpoint를 통해 Pod 확인하기
    - 아직 Pod를 생성한 적 없으므로 아무것도 출력되지 않는다.

  ```bash
  $ curl http://localhost:10255/pods | jq '.'
  
  # output
  {
    "kind": "PodList",
    "apiVersion": "v1",
    "metadata": {},
    "items": null
  }
  ```



- Kubelet에서 Pod 실행하기

  - Standalone mode에서는 Pod manifest를 통해 Pod를 실행할 수 있다.
    - Manifest는 local filesystem에서 불러오거나, configuration source에서 HTTP를 통해 가져올 수 있다.
  - Manifest 생성하기

  ```bash
  $ cat <<EOF > static-web.yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: static-web
  spec:
    containers:
      - name: web
        image: nginx
        ports:
          - name: web
            containerPort: 80
            protocol: TCP
  EOF
  ```

  - 위에서 생성한 manifest 파일을 `/etc/kubernetes/manifests` directory에 복사한다.

  ```bash
  $ sudo cp static-web.yaml /etc/kubernetes/manifests/
  ```



- Kubelet과 Pod 정보 확인하기

  - Pod 정보 확인하기
    - Pod networking plugin은 network bridge를 생성하고, 각 Pod에 대한 `veth`  interface 쌍을 생성한다(하나는 Pod 내부에 위치하고, 다른 하나는 host level에 위치한다).

  ```bash
  $ curl http://localhost:10255/pods | jq '.'
  ```

  - `static-web` Pod의 IP 주소 확인하기

  ```bash
  $ curl http://localhost:10255/pods | jq '.items[].status.podIP'
  
  # output
  "10.85.0.4"
  ```

  - `nginx` Pod로 요청 전송하기
    - 기본 port가 80이므로, port는 명시하지 않는다.

  ```bash
  $ curl http://10.85.0.4
  ```
