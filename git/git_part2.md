# Git 브랜치

## 브랜치란 무엇인가

- 브랜치
  - 개발을 하다 보면 코드를 여러 개로 복사해야 하는 일이 자주 생긴다. 
  - 코드를 통째로 복사하고 나서 원래 코드와는 상관없이 독립적으로 개발을 진행할 수 있는데, 이렇게 독립적으로 개발하는 것이 브랜치다.
  - Git이 브랜치를 다루는 과정을 이해하려면 우선 Git이 데이터를 어떻게 저장하는지 알아야 한다.



- Git은 어떻게 데이터를 저장하는가.
  - 커밋하면 Git은 현 Staging Area에 있는 데이터의 스냅샷에 대한 포인터, 저자나 커밋 메시지 같은 메타데이터, 이전 커밋에 대한 포인터 등을 포함하는 커밋 개체(커밋 Object)를 저장한다.
    - 이전 커밋 포인터가 있어서 현재 커밋이 무엇을 기준으로 바뀌었는지를 알 수 있다. 
    - 다시 파일을 수정하고 커밋하면 이전 커밋이 무엇인지도 저장한다.
    - 최초 커밋을 제외한 나머지 커밋은 커밋 포인터가 적어도 하나씩 있고 브랜치를 합친 Merge 커밋 같은 경우에는 이전 커밋 포인터가 여러 개 있다.
  - 파일 3개를 커밋하는 예시
    - 파일을 Stage 하면(`git add`) Git 저장소에 파일을 저장하고(Git은 이것을 **Blob**이라고 부른다) Staging Area에 해당 파일의 체크섬(SHA-1로 작성된 고유 번호의 일종)을 저장한다.
    - 커밋(`git commit`)하면 먼저 루트 디렉토리와 각 하위 디렉토리의 트리 개체를 체크섬과 함께 저장소에 저장한다. 
    - 그다음에 커밋 개체를 만들고 메타데이터와 루트 디렉토리 트리 개체를 가리키는 포인터 정보를 커밋 개체에 넣어 저장한다. 
    - 그래서 필요하면 언제든지 스냅샷을 다시 만들 수 있다.
    - 이 작업을 마치고 나면 Git 저장소에는 다섯 개의 데이터 개체가 생긴다. 
    - 각 파일에 대한 Blob 세 개, 파일과 디렉토리 구조가 들어 있는 트리 개체 하나, 메타데이터와 루트 트리를 가리키는 포인터가 담긴 커밋 개체 하나이다.
  - Git의 브랜치는 커밋 사이를 가볍게 이동할 수 있는 어떤 포인터 같은 것이다.
    - 기본적으로 Git은 `master` 브랜치를 만든다. 
    - 처음 커밋하면 이 `master` 브랜치가 생성된 커밋을 가리킨다. 
    - 이후 커밋을 만들면 `master` 브랜치는 자동으로 가장 마지막 커밋을 가리킨다.
    - Git 버전 관리 시스템에서 “master” 브랜치는 특별하지 않다. 
    - 다만 모든 저장소에서 “master” 브랜치가 존재하는 이유는 `git init` 명령으로 초기화할 때 자동으로 만들어진 이 브랜치를 애써 다른 이름으로 변경하지 않기 때문이다.



- 새 브랜치 생성하기

  - 새로 생성한 브랜치도 지금 작업하고 있던 마지막 커밋을 가리킨다.

  ```bash
  $ git branch <브랜치명>
  ```

  - 지금 작업 중인 브랜치가 무엇인지 Git은 어떻게 파악할까. 
    - 다른 버전 관리 시스템과는 달리 Git은 'HEAD’라는 특수한 포인터가 있다. 
    - 이 포인터는 지금 작업하는 로컬 브랜치를 가리킨다. 
    - 브랜치를 새로 만들었지만, Git은 아직 `master` 브랜치를 가리키고 있다. `git branch` 명령은 브랜치를 만들기만 하고 브랜치를 옮기지 않는다.
    - `git log`명령에 `--decorate` 옵션을 사용하면 쉽게 브랜치가 어떤 커밋을 가리키는지도 확인할 수 있다.

  ```bash
  $ git log --oneline --decorate
  ```
  - Git의 브랜치는 어떤 한 커밋을 가리키는 40글자의 SHA-1 체크섬 파일에 불과하기 때문에 만들기도 쉽고 지우기도 쉽다. 
    - 새로 브랜치를 하나 만드는 것은 41바이트 크기의 파일을(40자와 줄 바꿈 문자) 하나 만드는 것에 불과하다.
    - 브랜치가 필요할 때 프로젝트를 통째로 복사해야 하는 다른 버전 관리 도구와 Git의 차이는 극명하다. 
    - 통째로 복사하는 작업은 프로젝트 크기에 따라 다르겠지만 수십 초에서 수십 분까지 걸린다. 그에 비해 Git은 순식간이다. 
    - 게다가 커밋을 할 때마다 이전 커밋의 정보를 저장하기 때문에 Merge 할 때 어디서부터(Merge Base) 합쳐야 하는지 안다.



- 브랜치 이동하기

  - `git checkout` 명령으로 다른 브랜치로 이동할 수 있다.

  ```bash
  $ git checkout <브랜치명>
  ```

  - 이후 commit을 실행하면 새로 생성된 브랜치는 새로운 커밋을 가리키고 `master` 브랜치는 이전 커밋에 머물러 있다.
    - 이후 master 브랜치로 이동 후 다시 커밋을 하면 새로 생성된 브랜치가 가리키는 커밋이 아닌 새로운 커밋을 가리키게 된다.
    - 즉, master 브랜치와 새로 생성된 브랜치가 갈라지게 된다.
  - **브랜치를 이동하면 워킹 디렉토리의 파일이 변경된다.**
    - 이전에 작업했던 브랜치로 이동하면 워킹 디렉토리의 파일은 그 브랜치에서 가장 마지막으로 했던 작업 내용으로 변경된다. 
    - 따라서 지금은 작업하던 것을 모두 커밋하고 브랜치를 이동시켜야 한다.
    - 파일 변경시 문제가 있어 브랜치를 이동시키는게 불가능한 경우 Git은 브랜치 이동 명령을 수행하지 않는다.

  - 아래 명령어를 입력하면 브랜치 생성과 이동을 동시에 할 수 있다.

  ```bash
  $ git checkout -b <브랜치명>
  ```



- 브랜치 삭제하기

  ```bash
  $ git branch -d <브랜치명>
  ```

  



## 브랜치와 Merge의 기초

> https://git-scm.com/book/ko/v2/Git-%EB%B8%8C%EB%9E%9C%EC%B9%98-%EB%B8%8C%EB%9E%9C%EC%B9%98%EC%99%80-Merge-%EC%9D%98-%EA%B8%B0%EC%B4%88 그림 참고

- Merge하기

  - 아래 명령어를 입력하면 된다.

  ```bash
  $ git merge <merge할 브랜치명>
  ```

- Merge의 기초

  - Fast forward
    - merge를 수행하면 Fast forward라는 메세지를 볼 수 있다.
    - 특정 브랜치가 가리키는 커밋이 merge 할 다른 브랜치가 가리키는 커밋에 기반한 커밋이라면 브랜치 포인터는 merge 과정 없이 그저 최신 커밋으로 이동한다. 이와 같은 merge 방식을 Fast forward라고 한다.
    - 다시 말해 A 브랜치에서 다른 B 브랜치를 Merge 할 때 B 브랜치가 A 브랜치 이후의 커밋을 가리키고 있으면 그저 A 브랜치가 B 브랜치와 동일한 커밋을 가리키도록 이동시킬 뿐이다.

  ```
  # Fast forward 방식
  # MT는 master 브랜치
  # 아래에서 B1 브랜치는 C2에 기반한 C4 커밋을 가리키고 있다.
  # 이 때 B1 브랜치를 MT 브랜치에 merge하면 Fast forward 방식으로 merge 된다.
  
            MT   B1
  C0 ← C1 ← C2 ← C4
               ↖
                 C3
                 B2
  		       
                 MT
                 B1
  C0 ← C1 ← C2 ← C4
               ↖
                 C3
                 B2
  ```
  
  - merge commit
    - Fast forward와 같이 한 브랜치가 다른 브랜치에 기반한 커밋을 가리키는 것이 아니라 완전히 갈라져 있는 브랜치를 merge하는 경우이다.
    - 이 경우 두 브랜치의 공통 조상인 커밋과 각기 다른 두 브랜치가 가리키는 커밋 2개를 3-way Merge한다.
    - 3-way Merge 의 결과를 별도의 커밋으로 만들고 나서 해당 브랜치가 그 커밋을 가리키도록 이동시킨다.
  
  ```
  # merge commit 방식
  # C3, C4로 브랜치가 갈라진다.
                 MT
                 C3
               ↙
  C0 ← C1 ← C2 ← C4
                 B1
  
  # C3, C4와 그 둘의 공통 조상인 C2를 3-way Merge하여 그 결과로 C5가 생성된다.
                 C3
               ↙   ↖
  C0 ← C1 ← C2 ← C4 ← C5
                 B1   MT
  ```
  
  
  
  



- 충돌의 기초
  - 가끔씩 3-way Merge가 실패할 때도 있다. 
    - Merge 하는 두 브랜치에서 같은 파일의 한 부분을 동시에 수정하고 Merge 하면 Git은 해당 부분을 Merge 하지 못하고 아래와 같은 메세지가 뜬다. .
    - `CONFLICT (content): Merge conflict in <충돌 파일> Automatic merge failed; fix conflicts and then commit the result.`
    - 변경사항의 충돌을 개발자가 해결하지 않는 한 Merge 과정을 진행할 수 없다. 
  - Merge 충돌이 일어났을 때 Git이 어떤 파일을 Merge 할 수 없었는지 살펴보려면 `git status` 명령을 이용한다.
    - 충돌이 일어난 파일은 unmerged 상태로 표시된다. 
    - Git은 충돌이 난 부분을 표준 형식에 따라 표시해준다. 
    - 그러면 개발자는 해당 부분을 수동으로 해결한다.
    - `=======` 위쪽의 내용은 `HEAD` 버전(merge 명령을 실행할 때 작업하던 브랜치)의 내용이고 아래쪽은 merge하려 했던 브랜치의 내용이다.
  - 충돌을 해결하면 다시 `git add` 명령어부터 입력해야 한다.



- 다른 merge 도구로 충돌을 해결할 수 있다.

  - 아래 명령어로 실행한다.

  ```bash
  $ git mergetool
  ```

  - 기본 도구 말고 사용할 수 있는 다른 Merge 도구도 있는데, “one of the following tools.” 부분에 보여준다. 여기에 표시된 도구 중 하나를 고를 수 있다.
  - Merge 도구를 종료하면 Git은 잘 Merge 했는지 물어본다. 
    - 잘 마쳤다고 입력하면 자동으로 `git add` 가 수행되고 해당 파일이 Staging Area에 저장된다. 
    - `git status` 명령으로 충돌이 해결된 상태인지 다시 한번 확인해볼 수 있다.

  - 충돌을 해결하고 나서 해당 파일이 Staging Area에 저장됐는지 확인했으면 `git commit` 명령으로 Merge 한 것을 커밋한다. 



## 브랜치 관리

- 브랜치 목록 보기

  - 아래 명령어를 수행하면 모든 브랜치의 목록이 나온다.
    - `*` 기호가 붙어 있는 브랜치는 현재 Checkout 해서 작업하는 브랜치를 나타낸다.

  ```bash
  $ git branch
  ```

  - `-v` 명령을 실행하면 브랜치마다 마지막 커밋 메시지도 함께 보여준다.

  ```bash
  $ git branch -v
  ```



- 브랜치가 merge 된 상태인지 확인하기

  - 이미 Merge 한 브랜치 목록 확인
    - `*` 기호가 붙어 있지 않은 브랜치는 `git branch -d` 명령으로 삭제해도 되는 브랜치다.
    - 즉, merge 했고 현재 작업중이지도 않은 브랜치라는 뜻이다.

  ```bash
  $ git branch --merged <브랜치명>
  ```

  - Merge 하지 않은 브랜치 목록 확인
    - 아직 Merge 하지 않은 커밋을 담고 있기 때문에 `git branch -d` 명령으로 삭제되지 않는다.
    - Merge 하지 않은 브랜치를 강제로 삭제하려면 `-D` 옵션으로 삭제한다.

  ```bash
  $ git branch --no-merged <브랜치명>
  ```

  - `--merged`, `--no-merged` 옵션을 사용할 때 커밋이나 브랜치 이름을 지정해주지 않으면 현재 브랜치를 기준으로 Merge 되거나 Merge 되지 않은 내용을 출력한다.



## 브랜치 워크플로우

- Long-Running 브랜치
  - 배포했거나 배포할 코드만 `master` 브랜치에 Merge 해서 안정 버전의 코드만 `master` 브랜치에 둔다. 
  - 개발을 진행하고 안정화하는 브랜치는 `develop` 이나 `next` 라는 이름으로 추가로 만들어 사용한다. 
    - 이 브랜치는 언젠가 안정 상태가 되겠지만, 항상 안정 상태를 유지해야 하는 것이 아니다. 
    - 테스트를 거쳐서 안정적이라고 판단되면 `master` 브랜치에 Merge 한다.

  - 코드를 여러 단계로 나누어 안정성을 높여가며 운영할 수 있다. 
  - 프로젝트 규모가 크면 `proposed` 혹은 `pu` (proposed updates)라는 이름의 브랜치를 만들고, 여기에 `next` 나 `master` 브랜치에 아직 Merge 할 준비가 되지 않은 것들을 일단 Merge 시킨다.
  - 중요한 개념은 브랜치를 이용해 여러 단계에 걸쳐서 안정화해 나아가면서 충분히 안정화가 됐을 때 안정 브랜치로 Merge 한다는 점이다.



- 토픽 브랜치
  - 어떤 한 가지 주제나 작업을 위해 만든 짧은 호흡의 브랜치다.
  - 보통 주제별로 브랜치를 만들고 각각은 독립돼 있기 때문에 매우 쉽게 컨텍스트 사이를 옮겨 다닐 수 있다. 
    - 묶음별로 나눠서 일하면 내용별로 검토하기에도, 테스트하기에도 더 편하다. 
    - 각 작업을 하루든 한 달이든 유지하다가 `master` 브랜치에 Merge 할 시점이 되면 순서에 관계없이 그때 Merge 하면 된다.





## 리모트 브랜치

- 리모트 Refs
  - 리모트 저장소에 있는 포인터인 레퍼런스다. 
  - 리모트 저장소에 있는 브랜치, 태그, 등등을 의미한다. 
  - `git ls-remote [remote]` 명령으로 모든 리모트 Refs를 조회할 수 있다. 
  - `git remote show [remote]` 명령은 모든 리모트 브랜치와 그 정보를 보여준다. 
  - 리모트 Refs가 있지만 보통은 리모트 트래킹 브랜치를 사용한다.



- 리모트 트래킹 브랜치
  - 리모트 브랜치를 추적하는 레퍼런스이며 브랜치다. 
    - 리모트 트래킹 브랜치는 일종의 북마크라고 할 수 있다. 
    - 리모트 저장소에 마지막으로 연결했던 순간에 브랜치가 무슨 커밋을 가리키고 있었는지를 나타낸다.
  - 리모트 트래킹 브랜치는 로컬에 있지만 임의로 움직일 수 없다. 
    - 리모트 서버에 연결할 때마다 리모트의 브랜치 업데이트 내용에 따라서 자동으로 갱신될 뿐이다. 
  - 리모트 트래킹 브랜치의 이름은 `<remote>/<branch>` 형식으로 되어 있다.
    - 예를 들어 리모트 저장소 `origin` 의 `master` 브랜치를 보고 싶다면 `origin/master` 라는 이름으로 브랜치를 확인하면 된다.
    - 즉 그냥 `<브랜치명>`만 하면 로컬에서 로컬 브랜치와 리모트 브랜치의 구분이 되지 않기에 `<remote>/<branch>`로 로컬의 리모트 브랜치라고 표시한 것이다.



- 리모트 브랜치 정보를 업데이트

  - 로컬 저장소에서 어떤 작업을 하고 있는데 동시에 다른 팀원이 리모트 서버에 Push 하고 `master` 브랜치를 업데이트한다. 
    - 그러면 팀원 간의 히스토리는 서로 달라진다. 
    - 서버 저장소로부터 어떤 데이터도 주고받지 않아서 나의 `origin/master` 포인터는 그대로다.

  - 리모트 서버로부터 저장소 정보를 동기화하려면 `git fetch origin` 명령을 사용한다.
    - 명령을 실행하면 우선 “origin” 서버의 주소 정보를 찾아서, 현재 로컬의 저장소가 갖고 있지 않은 새로운 정보가 있으면 모두 내려받고, 받은 데이터를 로컬 저장소에 업데이트한다.
    - 그 후 `origin/master` 포인터의 위치를 최신 커밋으로 이동시킨다.

  ```bash
  $ git fetch <remote>
  ```

  - Fetch 명령으로 리모트 트래킹 브랜치를 내려받는다고 해서 로컬 저장소에 수정할 수 있는 브랜치가 새로 생기는 것이 아니다. 
    - 다시 말해서 브랜치가 생기는 것이 아니라 그저 수정 못 하는 `<remote>/<branch>` 브랜치 포인터가 생기는 것이다.
  - 새로 받은 브랜치의 내용을 Merge 하려면 아래 명령을 사용한다. 

  ```bash
  $ git merge <remote>/<브랜치명>
  ```

  - Merge 하지 않고 리모트 트래킹 브랜치에서 시작하는 새 브랜치를 만들려면 아래와 같은 명령을 사용한다.

  ```bash
  git checkout -b <브랜치명> <remote>/<브랜치명>
  ```



- push하기

  - 로컬의 브랜치를 서버로 전송하려면 쓰기 권한이 있는 리모트 저장소에 Push 해야 한다. 
    - 로컬 저장소의 브랜치는 자동으로 리모트 저장소로 전송되지 않는다. 
    - 명시적으로 브랜치를 Push 해야 정보가 전송된다. 
    - 따라서 리모트 저장소에 전송하지 않고 로컬 브랜치에만 두는 비공개 브랜치를 만들 수 있다. 
    - 또 다른 사람과 협업하기 위해 토픽 브랜치만 전송할 수도 있다.

  - 아래 명령어를 사용하여 push 한다.
    - “로컬의 브랜치를 리모트 저장소의 브랜치로 Push 하라” 라는 뜻이다.

  ```bash
  $ git push <remote> <branch>
  ```

  - 로컬 브랜치의 이름과 리모트 서버의 브랜치 이름이 다를 때는 아래 명령어를 수행하여 push할 수 있다.

  ```bash
  $ git push origin <로컬 브랜치>:<리모트 서버 브랜치>
  ```



- 브랜치 추적

  - 리모트 트래킹 브랜치를 로컬 브랜치로 Checkout 하면 자동으로 “트래킹(Tracking) 브랜치” 가 만들어진다. 
    - 트래킹 하는 대상 브랜치를 **Upstream 브랜치** 라고 부른다.
    - 트래킹 브랜치는 리모트 브랜치와 직접적인 연결고리가 있는 로컬 브랜치이다.
    - 트래킹 브랜치에서 `git pull` 명령을 내리면 리모트 저장소로부터 데이터를 내려받아 연결된 리모트 브랜치와 자동으로 Merge 한다.
  - 서버로부터 저장소를 Clone을 하면 Git은 자동으로 `master` 브랜치를 `origin/master` 브랜치의 트래킹 브랜치로 만든다. 
    - 트래킹 브랜치를 직접 만들 수 있는데 리모트를 `origin` 이 아닌 다른 리모트로 할 수도 있고, 브랜치도 `master` 가 아닌 다른 브랜치로 추적하게 할 수 있다. 
    - `git checkout -b <branch> <remote>/<branch>` 명령으로 간단히 트래킹 브랜치를 만들 수 있다. 
    - `--track` 옵션을 사용하여 로컬 브랜치 이름을 자동으로 생성할 수 있다.

  ```bash
  git checkout --track <remote>/<branch>`
  ```

  - 리모트 브랜치와 다른 이름으로 브랜치를 만들려면 로컬 브랜치의 이름을 아래와 같이 다르게 지정한다.

  ```bash
  $ git checkout -b <다르게 지정할 이름> <remote>/<branch>
  ```

  - 이미 로컬에 존재하는 브랜치가 리모트의 특정 브랜치를 추적하게 하려면  `-u` 나 `--set-upstream-to` 옵션을 붙여서 아래와 같이 설정한다.

  ``` bash
  $ git branch -u <remote>/<branch>
  ```

  - 추적 브랜치가 현재 어떻게 설정되어 있는지 확인하려면 `git branch` 명령에 `-vv` 옵션을 더한다.
    - 이 명령을 실행하면 로컬 브랜치 목록과 로컬 브랜치가 추적하고 있는 리모트 브랜치도 함께 보여준다. 
    - 또한 로컬 브랜치가 앞서가는지 뒤쳐지는지에 대한 내용도 보여준다.
    - `ahead`: 로컬 브랜치가 커밋이 앞서 있다.
    - `behind`: 로컬 브랜치가 커밋이 뒤쳐져 있다.
    - 만일 `ahead 3, behind 1`이면 브랜치에 서버로 보내지 않은 커밋이 3개, 서버의 브랜치에서 아직 로컬 브랜치로 머지하지 않은 커밋이 1개 있다는 말이다.
    - `trying something new`: 추적하는 브랜치가 없는 상태.

  ```bash
  $ git branch -vv
  ```

  - 위 명령을 실행했을 때 나타나는 결과는 모두 마지막으로 서버에서 데이터를 가져온(fetch) 시점을 바탕으로 계산한다.
    - 현재 시점에서 진짜 최신 데이터로 추적 상황을 알아보려면 먼저 서버로부터 최신 데이터를 받아온 후에 추적 상황을 확인해야 한다. 
    - 아래처럼 두 명령을 이어서 사용하는 것이 적당하다 하겠다.

  ```bash
  $ git fetch --all; git branch -vv
  ```



- pull 하기
  - `git fetch` 명령을 실행하면 서버에는 존재하지만, 로컬에는 아직 없는 데이터를 받아와서 저장한다. 
    - 이 때 워킹 디렉토리의 파일 내용은 변경되지 않고 그대로 남는다.
    - 서버로부터 데이터를 가져와서 저장해두고 사용자가 Merge 하도록 준비만 해둔다. 
  - 간단히 말하면 `git pull` 명령은 대부분 `git fetch` 명령을 실행하고 나서 자동으로 `git merge` 명령을 수행하는 것 뿐이다.
    - `git pull` 명령은 서버로부터 데이터를 가져와서 현재 로컬 브랜치와 서버의 추적 브랜치를 Merge 한다.
    - 일반적으로 `fetch` 와 `merge` 명령을 명시적으로 사용하는 것이 `pull` 명령으로 한번에 두 작업을 하는 것보다 낫다.



- remote 브랜치 삭제

  ```bash
  $ git push origin --delete <브랜치>
  ```





## Rebase

- 한 브랜치에서 다른 브랜치로 합치는 방법으로는 두 가지가 있다. 하나는 Merge 이고 다른 하나는 Rebase 다.



- Rebase 기초

  - Rebase 는 브랜치가 갈라진 경우 한 브랜치의 변경 사항을 Patch로 만들고 이를 다른 브랜치에 적용시키는 방법이다.
    - 두 브랜치가 나뉘기 전인 공통 커밋으로 이동한다.
    - 그 커밋부터 지금 Checkout 한 브랜치가 가리키는 커밋까지 diff를 차례로 만들어 어딘가에 임시로 저장해 놓는다.
    - Rebase 할 브랜치가 합칠 브랜치가 가리키는 커밋을 가리키게 하고 아까 저장해 놓았던 변경사항을 차례대로 적용한다.
    - 그리고 나서 합칠 브랜치를 Fast-forward 시킨다
  
  ```
  # C3, C4로 브랜치가 갈라진다.
                 B1
                 C3
             ↙
  C0 ← C1 ← C2 ← C4
                 MT
    			   
  # 두 브랜치가 나뉘기 전인 공통 커밋 C2로 이동한다.
  # 그 후 C2에서부터 C3까지의 diff를 차례로 만들어 임시로 저장한다.
  # Rebase 할 브랜치(B1)가 합칠 브랜치(MT)가 가리키는 커밋을 가리키게 한다.
  # 저장해 놓았던 변경 사항들을 차례로 (합칠 브랜치가 가리키는 커밋에)적용한다.
                (C3)
               ↙   
  C0 ← C1 ← C2 ← C4 ← C3'
                 MT   B1
  
  # 이렇게 하면 C4에 기반한 C3'라는 커밋이 생기게 된 셈이다.
  # 따라서 Fast-forward가 가능해지므로 MT 브랜치를 Fast-forward한다.
  # `$ git checkout master` 이후 `$ git merge B1`
                      B1
  C0 ← C1 ← C2 ← C4 ← C3'
                      MT
  ```
  
    - 아래 명령어로 실행 가능하다.
  
  ```bash
  # 합쳐질 브랜치에서 합칠 브랜치(일반적으로 master)에 수행해야 한다.
  $ git rebase <합칠 브랜치>
  ```
  
    - Merge 이든 Rebase 든 둘 다 합치는 관점에서는 서로 다를 게 없다. 
      - 하지만, Rebase가 좀 더 깨끗한 히스토리를 만든다. 
      - Rebase 한 브랜치의 Log를 살펴보면 히스토리가 선형이다. 
      - 일을 병렬로 동시에 진행해도 Rebase 하고 나면 모든 작업이 차례대로 수행된 것처럼 보인다.
    - Rebase는 보통 리모트 브랜치에 커밋을 깔끔하게 적용하고 싶을 때 사용한다.
      - 아마 이렇게 Rebase 하는 리모트 브랜치는 직접 관리하는 것이 아니라 그냥 참여하는 브랜치일 것이다. 
      - 메인 프로젝트에 Patch를 보낼 준비가 되면 하는 것이 Rebase이므로, 브랜치에서 하던 일을 완전히 마치고 `origin/master` 로 Rebase 한다. 
      - 이렇게 Rebase 하고 나면 프로젝트 관리자는 어떠한 통합작업도 필요 없다. 그냥 master 브랜치를 Fast-forward 시키면 된다.



- Rebase 활용

  - 다른 토픽 브랜치에서 갈라져 나온 토픽 브랜치 같은 히스토리가 있다고 하자. 
    - `server` 브랜치를 만들어서 서버 기능을 추가하고 그 브랜치에서 다시 `client` 브랜치를 만들어 클라이언트 기능을 추가한다. 
    - 마지막으로 `server` 브랜치로 돌아가서 몇 가지 기능을 더 추가한다.
    - 이때 테스트가 덜 된 `server` 브랜치는 그대로 두고 `client` 브랜치만 `master` 로 합치려는 상황을 생각해보자.
  
  ```
  # 아래와 같은 상황이다.
                 MT
  C1 ← C2 ← C5 ← C6
          ↖          SV
            C3 ← C4 ← C10
              ↖      CL
                 C8 ← C9
  ```
  
    - `server` 와는 아무 관련이 없는 `client` 커밋을 `master` 브랜치에 적용하기 위해서 `--onto` 옵션을 사용하여 아래와 같은 명령을 실행한다.
      - 이 명령은 `master` 브랜치부터 `server` 브랜치와 `client` 브랜치의 공통 조상까지의 커밋을 `client` 브랜치에서 없애고 싶을 때 사용한다. 
      - `client` 브랜치에서만 변경된 Patch를 만들어 `master` 브랜치에서 `client` 브랜치를 기반으로 새로 만들어 적용한다. 
  
  ```bash
  $ git rebase --onto master server client
  ```
  
  - 위 명령어의 결과
  
  ```
                 MT         CL
  C1 ← C2 ← C5 ← C6 ← C8' ← C9'
          ↖           SV
    		C3 ← C4 ← C10
              ↖
               (C8) ← (C9)
  ```
  
    - 이제 `master` 브랜치로 돌아가서 Fast-forward 시킬 수 있다
  
  ```bash
  $ git checkout master
  $ git merge client
  ```
  
  ```
  # Fast-forward	   
                            MT
                            CL
  C1 ← C2 ← C5 ← C6 ← C8' ← C9'
          ↖           SV
            C3 ← C4 ← C10
  ```
  
    - `server` 브랜치의 작업이 다 끝나면 `git rebase <basebranch> <topicbranch>` 라는 명령으로 Checkout 하지 않고 바로 `server` 브랜치를 `master` 브랜치로 Rebase 할 수 있다. 
      - 이 명령은 토픽(`server`) 브랜치를 Checkout 하고 베이스(`master`) 브랜치에 Rebase 한다.
  
  ```bash
  $ git rebase master server
  ```
  
  - 위 명령어의 결과
  
  ```bash
  # 위 명령어의 결과	   
                            MT
                            CL                SV
  C1 ← C2 ← C5 ← C6 ← C8' ← C9' ← C3' ← C4` ← C10`
          ↖
            (C3) ← (C4) ← (C10)
  ```
  
    - 그리고 나서 `master` 브랜치를 Fast-forward 시킨다.
  
  ```bash
  $ git checkout master
  $ git merge server
  ```
  
  - 위 명령어의 결과
  
  ```
  # Fast-forward	   
                                              MT
                            CL                SV
  C1 ← C2 ← C5 ← C6 ← C8' ← C9' ← C3' ← C4` ← C10`
  ```



  - 모든 것이 `master` 브랜치에 통합됐기 때문에 더 필요하지 않다면 `client` 나 `server` 브랜치는 삭제해도 된다. 
    
    - 브랜치를 삭제해도 커밋 히스토리는 여전히 남아 있다.
    
    ```
    # 토픽 브랜치 삭제   
                                                MT
    C1 ← C2 ← C5 ← C6 ← C8' ← C9' ← C3' ← C4` ← C10`
    ```



- Rebase의 위험성

  - 공개 저장소에 이미 push 한 커밋을 Rebase해선 안된다.
    - 이 지침만 지키면 Rebase를 하는 데 문제 될 게 없다. 
    - 하지만, 이 주의사항을 지키지 않으면 사람들에게 욕을 먹을 것이다.
  - Rebase는 기존의 커밋을 그대로 사용하는 것이 아니라 내용은 같지만 다른 커밋을 새로 만든다는 것을 주의해야 한다.
  - 예시
    - 아래 예시에서는 팀원이 "공개 저장소에 이미 push 한 커밋을 Rebase해선 안된다."는 원칙을 어겼다.

  ```
  1.리모트 레포지토리를 clone하고 일부 수정한 후 커밋하면 커밋 히스토리는 다음과 같다.
  RM
  C1 
     ↖
       C2 ← C3
            MS
  
  
  2.이제 팀원중 누군가가 리모트를 클론하여 새로운 브랜치를 파서 작업한 다음, merge하고 서버에 push한다.
       C5
     ↙   ↖
  C1 ← C4 ← C6
            MS(팀원 로컬의 master 브랜치)
            RM(서버에 push 했으므로 RM도 C6 커밋을 가리키게 된다)
  
  
  3.이를 나의 로컬 리포지토리에 pull하면 커밋 히스토리는 아래와 같이 된다.
       C5
     ↙   ↖ RM
  C1 ← C4 ← C6
     ↖        ↖
       C2 ← C3 ← C7(pull하면 자동으로 merge가 이루어지므로 C1,C6,C3의 3-ways merge로 C7 커밋이 생긴다)
                 MS
  
  
  4.그런데 push했던 팀원이 merge 했던 커밋(C6)을 되돌리고 다시 rebase하려 한다.
  # 서버의 히스토리를 덮어 씌우려고 git push --force 명령어를 사용하여 리모트에 push하였다고 가정하면 커밋 히스토리는 다음과 같이 된다.
  
              RM(서버에 push 했으므로 RM도 C4' 커밋을 가리키게 된다)
              팀원MS
        C5  ← C4'
     ↙     ↖ 
  C1 ← (C4) ← (C6)
     ↖           ↖
        C2  ←  C3 ← C7
                    내MS
  
  
  5. C7이 참조하고 있는 C6 커밋이 사라졌기에 이미 처리한 일이라고 해도 또 다시 merge 해야 한다.
  # Rebase는 커밋의 SHA 해쉬값을 바꾸기 때문에 Git은 새로운 커밋으로 C4'를 받아들인다. 
  # 사실 C4'는 이미 히스토리에 적용되어 있지만, Git은 이를 알지 못한다.
  
               RM
        C5  ←  C4'
     ↙     ↖      ↖
  C1 ← (C4) ← (C6)    ↖
     ↖            ↖    ↖
        C2  ←  C3  ← C7 ← C8
                          MS
  
  # git log 명령으로 히스토리를 확인해 보면 저자, 커밋 날짜, 메시지가 동일하지만 SHA 해쉬 값이 다른 커밋이 두 개가 있다(C4, C4'). 
  # 게다가 이 히스토리를 서버에 push 하면 같은 커밋이 두 개가 존재하기 때문에 협업하는 사람들도 혼란스러워한다.
  # C4와 C6는 포함되지 말아야 할 커밋이지만, rebase 하기 전에 이미 다른 사람들이 해당 커밋을 참조하기 때문에 이러한 사고가 발생한 것이다.
  ```



- 해결법

  - 위와 같은 상황이 발생했을 때 해결 법은 Rebase 한 것을 다시 Rebase하는 것이다.

  ```bash
  $ git rebase <remote>/<branch>
  ```

  - 위 예시의 4번 상황에서 merge 하는 대신 `$ git rebase teamone/master` 명령을 실행하면 Git은 아래와 같은 작업을 한다.
    - 동료가 생성했던 C4와 C4' 커밋 내용이 완전히 같을 때만 이렇게 동작된다. 
    - 커밋 내용이 아예 다르거나 비슷하다면 커밋이 두 개 생긴다.
    - 같은 내용이 두 번 커밋될 수 있기 때문에 깔끔하지 않다.

  ```
  # 현재 브랜치(내MS)에만 포함된 커밋을 찾는다. (C2, C3, C4, C6, C7)
  # 위에서 찾은 커밋들 중 C7에 merge된 커밋을 가려낸다(C2, C3, C4, C6).
  # 이 중 C4'에 Rebase되지 않은 커밋들만 골라낸다(C2, C3).
  # 이 커밋들만 다시 RM 바탕으로 커밋을 쌓는다.
              RM
        C5  ← C4'
     ↙     ↖ 
  C1 ← (C4) ← (C6)
     ↖           ↖
        C2  ←  C3 ← C7
                    내MS
  
  # 아래와 같은 결과를 얻게 된다.
            RM          MS
  C1 ← C5 ← C4' ← C2' ← C3' 
  ```

  - `git pull` 명령을 실행할 때 옵션을 붙여서  Rebase 할 수도 있다.

  ```bash
  $ git pull --rebase
  
  # 아래와 같이 해도 결과는 동일하다.
  $ git fetch
  $ git rebase teamone/master
  ```

  - `git pull` 명령을 실행할 때 기본적으로 `--rebase` 옵션이 적용되도록 `pull.rebase` 설정을 추가할 수 있다. 

  ```bash
  $ git config --global pull.rebase true
  ```

  

  



- Rebase VS Merge

  - merge
    - 히스토리를 보는 관점 중에 하나는 작업한 내용의 기록으로 보는 것이 있다. 
    - 작업 내용을 기록한 문서이고, 각 기록은 각각 의미를 가지며, 변경할 수 없다. 
    - 이런 관점에서 커밋 히스토리를 변경한다는 것은 역사를 부정하는 꼴이 된다. 언제 무슨 일이 있었는지 기록에 대해 거짓말 을 하게 되는 것이다. 
    - 역사는 후세를 위해 기록하고 보존해야 한다.

  - rebase
    - 히스토리를 프로젝트가 어떻게 진행되었나에 대한 이야기로도 볼 수 있다. 
    - 소프트웨어를 주의 깊게 편집하는 방법에 메뉴얼이나 세세한 작업내용을 초벌부터 공개하고 싶지 않을 수 있다. 
    - 나중에 다른 사람에게 들려주기 좋도록 Rebase 나 filter-branch 같은 도구로 프로젝트의 진행 이야기를 다듬으면 좋다.

  - 일반적인 해답은 로컬 브랜치에서 작업할 때는 히스토리를 정리하기 위해서 Rebase 할 수도 있지만, 리모트 등 어딘가에 Push로 내보낸 커밋에 대해서는 절대 Rebase 하지 말아야 한다는 것이다.



# commit message 작성하기

- 커밋 메세지 컨벤션

  - 동명사 보다는 명사를 사용한다
    - 동사를 명사화시키지 말고 그 의미를 잘 표현하는 명사를 찾아서 사용한다.
    - 문장이 장황하지 않고 간결해진다.

  - 꼭 필요한 경우가 아니면 관사는 사용하지 않는다.
  - 부정문은 Don't를 사용한다(ex.  Not use가 아니라 Don’t use).

  - 오타 수정은 ` Fix typo`라고만 하면 된다.



- 커밋 메세지를 위한 영단어 목록

  > https://blog.ull.im/engineering/2019/03/10/logs-on-git.html 참고

  - Fix: 올바르지 않은 동작을 고친 경우에 사용
    - `Fix A`: A를 수정
    - `Fix A in B`: B의 A를 수정
    - `Fix A which B`, `Fix A that B`: B절인 A를 수정
    - `Fix A to B`, `Fix A to be B`: B를 위해 A를 수정
    - `Fix A so that B`: A를 수정해서 B가 되었다.
    - `Fix A where B`: B라는 문제가 발생하는 A를 수정
    - `Fix A when B`: B일때 발생하는 A를 수정
  - Add: 코드, 테스트, 예제, 문서 등의 추가가 있을 때 사용
    - `Add A`: A를 추가
    - `Add A for B`: B를 위해 A를 추가
    - `Add A to B`: B에 A를 추가
  - Remove: 코드의 삭제가 있을 때 사용,  ‘Clean’이나 ‘Eliminate’를 사용하기도 한다.
    - `Remove A`: A를 삭제
    - `Remove A from B`: B에서 A를 삭제
  - Use: 무언가를 사용해 구현하는 경우
    - `Use A`: A를 사용
    - `Use A for B`: B에 A를 사용
    - `Use A to B`: B가 되도록 A를 사용
    - `Use A in B`: B에서 A를 사용
    - `Use A instead of B`: B 대신 A를 사용
  - Refactor: 전면적인 수정이 있을 때 사용
    - `Refactor A`: A를 전면적으로 수정
  - Simplify: 복잡한 코드를 단순화 할 때 사용
    - `Simplify A`: A를 단순화
  - Update: 개정이나 버전 업데이트가 있을 때 사용, Fix와는 달리 잘못된 것을 바로잡는 것이 아님에 주의, 코드보다는 주로 문서나 리소스, 라이브러리등에 사용
    - `Update A to B`: A를 B로 업데이트 한다, A를 B하기 위해 업데이트 한다.
  - Improve: 향상이 있을 때 사용
    - `Improve A`: A를 향상시킨다.
  - Make: 기존 동작의 변경을 명시
    - `Make A B`: A를 B하게 만든다.
  - Implement: 코드가 추가된 정도보다 더 주목할 만한 구현체를 완성시켰을 때 사용
    - `Implement A`: A를 구현한다.
    - `Implement A to B`: B를 위해 A를 구현한다.
  - Revise: update와 비슷하나 주로 문서의 개정이 있을 때 사용
    - `Revise A`: A 문서를 개정
  - Correct: 주로 문법의 오류나 타입의 변경, 이름 변경 등에 사용
    - `Correct A`: A를 고친다.
  - Ensure: 무엇이 확실하게 보장받는다.
    - `Ensure A`: A가 확실히 보장되도록 수정.
  - Prevent: 특정 처리를 못하게 막는다.
    - `Prevent A`: A를 못하게 막는다.
    - `Prevent A from B`: A를 B하지 못하게 막는다.
  - Avoid: 막는 것은 아니지만 회피하게 한다.
    - `Avoid A`: A를 회피한다.
    - `Avoid A if B`, `Avoid A when B`: B라면 A를 회피한다.
  - Move: 코드의 이동이 있들 때 사용한다.
    - `Move A to B`, `Move A into B`: A를 B로 옮긴다.
  - Rename: 이름 변경이 있을 때 사용한다.
    - `Rename A to B`: A를 B로 이름을 변경한다.
  - Allow: Make와 비슷하지만, 허용을 표현할 때 사용한다.
    - `Allow A to B`: A가 B를 할 수 있도록 허용한다.
  - Verify: 검증 코드를 넣을 때 주로 사용한다.
    - `Verify A`: A를 검증한다.
  - Set: 변수 값을 변경하는 등의 작은 수정에 주로 사용
    - `Set A to B`: A를 B로 설정한다.
  - Pass: 파라미터를 넘기는 처리에 주로 사용한다.
    - `Pass A to B`: A를 B에 넘긴다.



- 커밋 템플릿 만들기

  - `gitmesssage.txt`파일 생성(꼭 파일 이름이 동일할 필요는 없다)

  ```bash
  touch ~/.gitmessage.txt  #~는 home 디렉토리를 뜻하므로 일반적으로 c/user 에 생성되게 된다.
  ```

  - 텍스트 에디터로 진입

  ```bash
  vim ~/.gitmessage.txt
  ```

  - 아래 내용을 복붙 후 저장(`esc` -> `:wq`)

  ```txt
  # <타입>: <제목>
  
  ##### 제목은 최대 50 글자까지만 입력 ############## -> |
  
  
  # 본문은 위에 작성
  ######## 본문은 한 줄에 최대 72 글자까지만 입력 ########################### -> |
  
  # 꼬릿말은 아래에 작성: ex) #이슈 번호
  
  # --- COMMIT END ---
  # <타입> 리스트
  #   feat    : 기능 (새로운 기능)
  #   fix     : 버그 (버그 수정)
  #   refactor: 리팩토링
  #   style   : 스타일 (코드 형식, 세미콜론 추가: 비즈니스 로직에 변경 없음)
  #   docs    : 문서 (문서 추가, 수정, 삭제)
  #   test    : 테스트 (테스트 코드 추가, 수정, 삭제: 비즈니스 로직에 변경 없음)
  #   chore   : 기타 변경사항 (빌드 스크립트 수정 등)
  # ------------------
  #     제목 첫 글자를 대문자로
  #     제목은 명령문으로
  #     제목 끝에 마침표(.) 금지
  #     제목과 본문을 한 줄 띄워 분리하기
  #     본문은 "어떻게" 보다 "무엇을", "왜"를 설명한다.
  #     본문에 여러줄의 메시지를 작성할 땐 "-"로 구분
  # ------------------
  ```

  - commit.template에 이 파일을 저장

  ```bash
  git config --global commit.template ~/.gitmessage.txt
  ```

  - add 후 `git commit`을 입력하면 위에서 등록한 템플릿이 나오게 되고 해당 템플릿을 수정하여 commit message를 작성하면 된다.



- commit message 변경 방법

  - 아직 push 하지 않은 커밋 메세지 변경

  ```bash
  #가장 마지막에 커밋한 메세지를 수정하는 방법
  #아래 명령어를 입력하면 커밋을 수정할 수 있는 창이 뜨는데 수정 후 esc -> :wq를 입력하면 된다.
  git commit --amend
  
  #더 오래 된 커밋 메세지 혹은 여러 커밋 메세지 동시 수정
  #아래 명령어를 입력하면 커밋을 수정할 수 있는 창이 뜨는데 수정하고 싶은 커밋 옆의 pick 이라는 문구를 reword 로 바꿔 주고 수정 후 esc->:wq를 입력하면 된다.
  git rebase -i HEAD~불러올 커밋 숫자
  
  ```

  - 이미 push 한 커밋 메세지를 수정하고자 할 때
    - 위 방법으로 수정 후 아래 명령어를 입력한다.
    - 단, push 된 커밋의 로그를 갖고 있던 다른 팀원들이 로그를 수동으로 수정해줘야 하기 때문에 이는 지양해야 한다.

  ```bash
  git push 식별자명 --force 브랜치이름
  ```




