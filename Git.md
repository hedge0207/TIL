# 참고 사이트

> https://git-scm.com/book/ko/v2/%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-%EB%B2%84%EC%A0%84-%EA%B4%80%EB%A6%AC%EB%9E%80%3F





# 초기 설정

- 최초 1회 실행

  ```bash
  git config --global user.name "your_name"
  ```

  ```bash
  git config --global user.email "your_email@example.com"
  ```



# git push

0. git 시작하기

```bash
$ git init
```

- 이제부터 해당 디렉토리를 git으로 관리하겠다.

- git init은 상위 폴더에서 수행했으면 하위 폴더에서는 하지 않아도 된다.

- 성공하면 뒤에 (master)가 뜬다. 이미 (master)가 붙어있다면  git init을 입력하지 않아도 된다.

- 이미 한 허브에 올린 후 다른 허브에 올릴 때도 하지 않아도 된다.



1. 상태 확인하기

```bash
$ git status
```

- 관리하고 있지 않은 파일(git hub에 올리지 않은 파일)은 빨간색으로 뜬다.



2. 스테이지에 올리기(완료 후 git status 실행하여 초록색으로 뜨는지 확인)

```bash
$ git add ㅏ파일명ㅓ
```

- add 취소하기

```bash
$ git reset HEAD ㅏ파일명ㅓ #입력하지 않을 경우 전부 초기화 된다.
```



3. 커밋하기(사진찍기)

```bash
$ git commit -m '메세지'
# -m과 같이 -뒤에 오는 것은  short name 옵션이고 --global같이 --뒤에 오는 것은 long name옵션이다.
```



4. 기록(log) 확인하기

```bash
$ git log
```



5. 리모트(원격 저장소) 등록하기

```bash
$ git remote add 식별자 ㅏ원격저장소 주소ㅓ
```

- origin은 식별자로, 아무 이름으로해도 상관없다. 또한 각기 다른 곳에 올리더라도(ex. lab과 git hub) 식별자를 다르게 할 필요는 없다.

- 주소는 프로젝트(lab의 경우 프로젝트 내의 clone클릭 후 http 복사), 혹은 repository에 들어가면 볼 수 있다.



6. 파일 푸쉬(업로드)하기

```bash
$ git push 식별자 master
```

- 로그인창에 git hub아이디와 비밀번호 입력

- 식별자는 remote add에 쓴 것과 동일해야 한다.

- add, commit, push가 한 세트



---







# git pull



1. 파일 다운 받기

```bash
$ git clone ㅏ다운받고자 하는 주소ㅓ(프로젝트 내에  clone or download에 있다)
```



2. 원래 있던 폴더(다운 받은 파일을 업로드한 폴더)에서 다운 받은 폴더에서 업로드한 파일을 받기

```bash
$ git pull origin master
```





---







# git branch

1. 브랜치 생성

   ```bash
   (master) $ git branch ㅏ브랜치명ㅓ
   ```

2. 브랜치 이동

   ```bash
   (master) $ git checkout ㅏ브랜치명ㅓ
   ```

3. 브랜치 생성 및 이동

   ```bash
   (master) $ git checkout -b ㅏ브랜치명ㅓ
   ```

4. 브랜치 삭제

   ```bash
   (master) $ git branch -d ㅏ브랜치명ㅓ
   ```

5. 브랜치 목록

   ```bash
   (master) $ git branch
   ```

6. commit, push, add

   ```bash
   $ git add .
   $ git commit -m '메세지'
   $ git push origin 브랜치명
   ```

   -----------여기까지-------------

7. git에 브랜치 생성

   ```bash
   $ git push origin branch명
   ```

8. 브랜치 병합

   ```bash
   (master) $ git merge ㅏ브랜치명ㅓ
   ```

   * master 브랜치에서 ㅏ브랜치명ㅓ을 병합

9. 브랜치 상황 그래프로 확인하기

   ```bash
   $ git log --oneline --graph
   ```

10. branch 삭제

    ```bash
    $ git branch -d 브랜치명
    ```

    

- 특정 branch 클론

  ```bash
  git clone -b branch명 --single-branch 저장소 URL
  ```

  



---





# 기타

1. 식별자 지우기

```bash
$ git remote rm 식별자
```

- 해당 식별자로 올라간 폴더도 함께 삭제된다.



2. repository에 push 된 내용 삭제하기

```bash
$ git rm -r --cached .
```



---



3. `.gitignore` 파일을 추가하기 전에 `.gitignore`에 포함된 파일을 올리면 `.gitignore`에 포함되어 있다고 하더라도 commit이 된다.



# git 저장소 옮기기

> https://ithub.tistory.com/258 참고

- 아래 방법을 사용하면 단순히 파일만 옮기는 것이 아니라 커밋 내역, 브랜치 등도 함께 옮길 수 있다.

1. 원본 저장소의 모든 이력 복사

```bash
$ git clone --mirror [원본 저장소 경로]
```

2. clone한 디렉터리 안으로 이동

```bash
$ cd [원본 저장소 이름].git 
```

3. 이동할 원격 저장소 경로 지정

```bash
$ git remote set-url --push origin [이동할 원격 저장소 경로] 
```

4. 원격 저장소로 push

```bash
$ git push --mirror 
```



- gitlab과 달리 github은 100MB 이상의 파일을 올릴 수 없다. 따라서 100MB이상의 파일이 존재하는 경우 error가 발생할 수 있다. 따라서 해당 커밋 내역을 삭제하여 옮겨야 한다.

```bash
# BFG Repo-Cleaner를 사용한다.
# https://rtyley.github.io/bfg-repo-cleaner에서 jar 파일을 다운 받는다.

# 2. 원본저장소를 clone한 디렉터리의 경로에서 아래 명령어를 사용하여 실행한다.
$ java -jar bfg_x.x.x.jar --strip-blobs-bigger-than 100M # bfg의 버전과 jar 파일의 경로에 주의해야 한다.
$ git push --mirror # 다시 원격 저장소로 push
```





# commit message 작성하기

- 커밋 템플릿 만들기

  - `gitmesssage.txt`파일 생성

  ```bash
  touch gitmessage.txt
  ```

  - 텍스트 에디터로 진입

  ```bash
  vim gitmessage.txt
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
  git config --global commit.template gitmessage.txt
  ```

  















