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







# 기본 사용법

## git push

- 시작하기

  ```bash
  $ git init
  ```

  - 이제부터 해당 디렉토리를 git으로 관리하겠다.
  - git init은 상위 폴더에서 수행했으면 하위 폴더에서는 하지 않아도 된다.
  - 성공하면 뒤에 (master)가 뜬다. 이미 (master)가 붙어있다면  git init을 입력하지 않아도 된다.
  - 이미 한 허브에 올린 후 다른 허브에 올릴 때도 하지 않아도 된다.



- 상태 확인하기

  ```bash
  $ git status
  ```

  - 관리하고 있지 않은 파일(git hub에 올리지 않은 파일)은 빨간색으로 뜬다.



- 스테이지에 올리기(완료 후 git status 실행하여 초록색으로 뜨는지 확인)

  ```bash
  $ git add ㅏ파일명ㅓ
  ```

  

- add 취소하기

  ```bash
  $ git reset HEAD ㅏ파일명ㅓ #입력하지 않을 경우 전부 초기화 된다.
  ```

  

- 커밋하기(사진찍기)

  ```bash
  $ git commit -m '메세지'
  # -m과 같이 -뒤에 오는 것은  short name 옵션이고 --global같이 --뒤에 오는 것은 long name옵션이다.
  ```



- 기록(log) 확인하기

  ```bash
  $ git log
  ```

  

- 리모트(원격 저장소) 등록하기

  ```bash
  $ git remote add 식별자 ㅏ원격저장소 주소ㅓ
  ```

  - origin은 식별자로, 아무 이름으로해도 상관없다. 또한 각기 다른 곳에 올리더라도(ex. lab과 git hub) 식별자를 다르게 할 필요는 없다.
  - 주소는 프로젝트(lab의 경우 프로젝트 내의 clone클릭 후 http 복사), 혹은 repository에 들어가면 볼 수 있다.



- 파일 푸쉬(업로드)하기

  ```bash
  $ git push 식별자 master
  ```

  - 로그인창에 git hub아이디와 비밀번호 입력
  - 식별자는 remote add에 쓴 것과 동일해야 한다.
  - add, commit, push가 한 세트

## git pull

- clone(파일 내려 받기)

  ```bash
  $ git clone ㅏ다운받고자 하는 주소ㅓ(프로젝트 내에  clone or download에 있다)
  ```

  

- 해당 저장소에서 클론 한 폴더에서 변경사항을 내려 받기

  ```bash
  $ git pull origin master
  ```

  





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

- 식별자 지우기

  ```bash
  $ git remote rm 식별자
  ```

  - 해당 식별자로 올라간 폴더도 함께 삭제된다.



- repository에 push 된 내용 삭제하기

  ```bash
  $ git rm -r --cached .
  ```

  

- `.gitignore` 파일을 추가하기 전에 `.gitignore`에 포함된 파일을 올리면 `.gitignore`에 포함되어 있다고 하더라도 commit이 된다.



















