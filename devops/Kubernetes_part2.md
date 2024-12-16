# Configuration

- 아래 내용을 테스트하기 위해서 control plane 역할을 하지 않는 2개의 노드를 cluster에 포함시키는 것이 권장된다.

  - minikube로 cluster 생성하기

  ```bash
  $ minikube start --nodes 3
  ```

  - 확인하기

  ```bash
  $ kubectl get nodes
  ```





## ConfigMap을 통해 설정 변경하기

- Volume으로 mount된 ConfigMap으로 설정 변경하기

  - 현재 ConfigMap 확인

  ```bash
  $ kubectl get configmaps
  ```

  - `kubectl create configmap`에 `--from-literal` 옵션을 주어 literal value를 사용하여 ConfigMap을 생성할 수 있다.

  ```bash
  $ kubectl create configmap <configmap_name> --from-literal=<key>=<value>
  
  # e.g.
  $ kubectl create configmap sport --from-literal=sport=football
  ```

  - 위에서 생성한 ConfigMap 확인

  ```bash
  $ kubectl get configmaps sport -o yaml
  ```

  - 출력되는 결과는 아래와 같다.
    - 위에서 literal value로 입력한 `sport=football`이 `data`에 추가된 것을 확인할 수 있다.

  ```yaml
  apiVersion: v1
  data:
    sport: football
  kind: ConfigMap
  metadata:
    creationTimestamp: "2024-11-27T01:20:05Z"
    name: sport
    namespace: default
    resourceVersion: "5475"
    uid: 5gh6484c-1d27-5t8d-asb1-a53f7wra6c2
  ```

  - Deployment를 생성한다.
    - `kubectl apply`의 경우 `kubectl create`와 유사하게 자원을 생성하는 명령어이다.
    - 다만 `kubectl apply`의 경우 생성하려는 자원이 없으면 자원을 생성하고, 자원이 이미 있으면 자원의 설정을 수정한다.
    - `-f` option 뒤에는 설정을 적용할 file 경로를 입력한다.

  ```bash
  $ kubectl apply -f https://k8s.io/examples/deployments/deployment-with-configmap-as-volume.yaml
  ```

  - 위에서 사용한 `deployments/deployment-with-configmap-as-volume.yaml`의 내용은 아래와 같다.
    - `spec.template.spec.containers.command`를 보면 `/etc/config/sport` 파일의 내용을 주기적으로 출력하는 application이라는 것을 알 수 있다.

  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: configmap-volume
    labels:
      app.kubernetes.io/name: configmap-volume
  spec:
    replicas: 3
    selector:
      matchLabels:
        app.kubernetes.io/name: configmap-volume
    template:
      metadata:
        labels:
          app.kubernetes.io/name: configmap-volume
      spec:
        containers:
          - name: alpine
            image: alpine:3
            command:
              - /bin/sh
              - -c
              - while true; do echo "$(date) My preferred sport is $(cat /etc/config/sport)";
                sleep 10; done;
            ports:
              - containerPort: 80
            volumeMounts:
              - name: config-volume
                mountPath: /etc/config
        volumes:
          - name: config-volume
            configMap:
              name: sport
  ```

  - 위에서 생성한 Deployment의 Pod들을 확인한다.
    - Selector를 사용하여 Pod를 matching시킨다.
    - 위 설정 파일에서 `metadata.labels`의 값을 `--selector` option에 준다.

  ```bash
  $ kubectl get pods --selector=app.kubernetes.io/name=configmap-volume
  
  # output
  NAME                                READY   STATUS    RESTARTS   AGE
  configmap-volume-6b976dfdcf-qxvbm   1/1     Running   0          72s
  configmap-volume-6b976dfdcf-skpvm   1/1     Running   0          72s
  configmap-volume-6b976dfdcf-tbc6r   1/1     Running   0          72s
  ```

  - Kubelet은 위 Pod들이 실행 중인 각 Node들에 ConfigMap에 대한 데이터를 가져와 local volume의 file로 변환한다.
    - 이후 kubelete은 위 설정 파일의 `spec.template.spec.container.volumeMounts`에 정의된대로 volume을 container에 mount한다.
    - 해당 container는 mount된 file에서 정보를 로드하여 `spec.template.spec.containers.command`를 실행시킬 때 사용한다.
    - Deployment에 속한 Pod의 log를 보면 출력 결과를 확인할 수 있다.

  ```bash
  $ kubectl logs deployments/configmap-volume
  
  # output
  Found 3 pods, using pod/configmap-volume-6b3qd48f2-qd1n8
  Wed Nov 27 01:28:42 UTC 2024 My preferred sport is football
  Wed Nov 27 01:28:52 UTC 2024 My preferred sport is football
  Wed Nov 27 01:29:02 UTC 2024 My preferred sport is football
  Wed Nov 27 01:29:12 UTC 2024 My preferred sport is football
  Wed Nov 27 01:29:22 UTC 2024 My preferred sport is football
  ```

  - Mount된 파일 확인하기
    - Pod 중 하나의 `/etc/config/sport`를 확인한다.

  ```bash
  $ kubectl exec -it configmap-volume-7b4bb95f8-n674r -- cat /etc/config/sport
  
  # output
  football
  ```

  - ConfigMap 수정하기
    - 아래 명령어를 입력하면 ConfigMap을 수정할 수 있는 editor가 실행된다.
    - Editor에서 `data.sport`의 값을 football에서 baseball로 변경한 뒤 창을 닫는다.
    - 성공적으로 변경 되면 `configmap/sport edited`와 같은 message가 출력된다.

  ```bash
  $ kubectl edit configmap sport
  ```

  - 다시 log를 확인한다.
    - 이전과는 달라진 것을 확인할 수 있다.

  ```bash
  $ kubectl logs deployments/configmap-volume --follow
  
  # output
  Wed Nov 27 01:52:43 UTC 2024 My preferred sport is football
  Wed Nov 27 01:52:53 UTC 2024 My preferred sport is football
  Wed Nov 27 01:53:03 UTC 2024 My preferred sport is baseball
  Wed Nov 27 01:53:13 UTC 2024 My preferred sport is baseball
  Wed Nov 27 01:53:23 UTC 2024 My preferred sport is baseball
  ```

  - 설정의 변경 사항이 항상 반영되는 것은 아닐 수 있다.
    - `configMap` volume이나 `projected` volume을 통해 실행 중인 Pod에 mapping된 ConfigMap이 있다면, ConfigMap의 변경 사항이 실행 중인 Pod에 반영될 것이다.
    - 그러나 app;ication은 변경 사항을 polling하거나 file의 update를 감시하도록 설정된 경우에만 변경 사항을 알 수 있다.
    - 만약 application이 최초 실행될 때만 설정을 load한다면, 설정의 변경 사항이 반영되지 않을 수 있다.

  - 변경된 설정이 반영되는 기간
    - ConfigMap이 수정되고, 변경 사항이 Pod에 반영되기 까지는 kubelet sync period만큼의 시간이 걸린다.
    - Kubelet은 mount된 ConfigMap에 변경 사항이 있는지 매 periodic sync마다 체크한다.
    - 그러나 kubelet은 현재 ConfigMap의 값을 가져오기 위해 자신의 local TTL-based cahce를 사용한다.
    - 그로 인해 ConfigMap이 수정되고, 변경 사항이 Pod에 반영되기 까지는 kubelet sync period(default: 1m) + ConfigMaps cache의 TTL(default: 1m)까지 걸릴 수 있다.



- ConfigMap을 통해 Pod의 환경 변수 수정하기

  - 위에서와 마찬가지로 literal value를 사용하여 ConfigMap을 생성한다.

  ```bash
  $ kubectl create configmap fruits --from-literal=fruits=apples
  ```

  - Deployment를 생성한다.

  ```bash
  $ kubectl apply -f https://k8s.io/examples/deployments/deployment-with-configmap-as-envvar.yaml
  ```

  - 위에서 Deployment 생성에 사용한 `deployments/deployment-with-configmap-as-envvar.yaml` 파일은 아래와 같다.
    - `spec.template.spec.containers.command`를 보면 환경 변수 `$FRUITS`를 주기적으로 출력하는 application이라는 것을 알 수 있다.
    - 이전과는 달리 volume을 생성하지는 않는다.

  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: configmap-env-var
    labels:
      app.kubernetes.io/name: configmap-env-var
  spec:
    replicas: 3
    selector:
      matchLabels:
        app.kubernetes.io/name: configmap-env-var
    template:
      metadata:
        labels:
          app.kubernetes.io/name: configmap-env-var
      spec:
        containers:
          - name: alpine
            image: alpine:3
            env:
              - name: FRUITS
                valueFrom:
                  configMapKeyRef:
                    key: fruits
                    name: fruits
            command:
              - /bin/sh
              - -c
              - while true; do echo "$(date) The basket is full of $FRUITS";
                  sleep 10; done;
            ports:
              - containerPort: 80
  ```

  - 위에서 생성한 Deployment에 대한 Pod를 확인한다.

  ```bash
  $ kubectl get pods --selector=app.kubernetes.io/name=configmap-env-var
  ```

  - 출력되는 내용을 확인한다.

  ```bash
  $ kubectl logs deployment/configmap-env-var
  
  # output
  Found 3 pods, using pod/configmap-env-var-7c994f7769-l74nq
  Wed Nov 27 02:17:24 UTC 2024 The basket is full of apples
  Wed Nov 27 02:17:34 UTC 2024 The basket is full of apples
  Wed Nov 27 02:17:44 UTC 2024 The basket is full of apples
  ```

  - ConfigMap을 수정한다.
    - editor에서 `data.fruits`의 값을 watermelons으로 수정한다.

  ```bash
  $ kubectl edit configmap fruits
  ```

  - 변경 사항이 적용되었는지 확인한다.
    - 변경 사항이 적용되지 않은 것을 확인할 수 있다.

  ```bash
  $ kubectl logs deployments/configmap-env-var --follow
  ```

  - 변경 사항이 적용되지 않는 이유
    - ConfigMap 내부의 key에 해당하는 value가 변경되었지만, Pod 내부의 환경 변수는 여전히 이전 값을 보여준다.
    - 이는 Pod 내부에서 실행 중인 process의 환경 변수가 source data의 변경으로는 변경되지 않기 때문이다.
    - 만약 강제로 변경하고자 한다면 Kubernetes가 기존의 Pod를 교체하도록 해야 한다.
    - 새로 교체된 Pod에는 변경 사항이 반영된다.
  - Pod 교체하기
    - Rollout은 Kubernetes가 Deployment에 대한 새로운 ReplicaSet을 만들도록 한다.
    - 이는 기존의 Pod들이 종료되고, 새로운 Pod들이 생성된다는 것을 의미한다.

  ```bash
  $ kubectl rollout restart deployment configmap-env-var
  
  # rollout이 완료되면 아래 명령어를 수행한다.
  $ kubectl rollout status deployment configmap-env-var --watch=true
  ```

  - Deployment와 Pod를 확인한다.
    - Deployment의 상태와 Pod들이 잘 교체되었는지 확인한다.

  ```bash
  $ kubectl get deployment configmap-env-var
  $ kubectl get pods --selector=app.kubernetes.io/name=configmap-env-var
  ```

  - 다시 log를 확인한다.
    - 잘 적용된 것을 확인할 수 있다.

  ```bash
  $ kubectl logs deployment/configmap-env-var
  
  # output
  Found 3 pods, using pod/configmap-env-var-694f488fd-rhkh6
  Wed Nov 27 02:34:57 UTC 2024 The basket is full of watermelons
  Wed Nov 27 02:35:07 UTC 2024 The basket is full of watermelons
  Wed Nov 27 02:35:17 UTC 2024 The basket is full of watermelons
  Wed Nov 27 02:35:27 UTC 2024 The basket is full of watermelons
  ```

