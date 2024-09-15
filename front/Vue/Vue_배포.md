# 배포

- npm build
  - Vue 프로젝트를 HTML,JS,CSS파일로 묶어준다.
  - webpack이 묶어주는 것이다.
    - 배포시에 HTML, CSS, JS, 이미지 등의 코드를 묶어주는 역할을 한다.

```bash
$ npm run build

#위 코드를 입력하면 dist 폴더가 새로 생기고 그 안에 HTML,JS,CSS파일이 새로 생긴다.
```



- netlify

  > https://www.netlify.com/

  - 위 사이트에 로그인 후 sites 탭으로  이동해서 dist 폴더를 등록한다.
  - 간단한 배포 방식이 장점이지만 단점으로는 매번 코드를 수정 할 때 마다 다시 등록을 해야 한다는 것이다.
    - git과 연동하면 이런 단점도 사라진다.
  - git과 연동하기
    - `New site from git`으로 이동 후 연동된 사이트(github 등) 클릭-권한 허용-리포지토리 선택 후 install클릭
    - 이 경우 dist 폴더를 만든 것이 아니라 프로젝트 전체를 올린 것이므로 사이트에서 배포 전에 dist 폴더를 만들도록 해야한다.
    - Basic build settings에서 `bulid command`에 `npm run build`를 입력하면 배포하기 전에 netlify에서 해당 명령어를 실행해 준다.
    - `Publish directory`에는 dist를 입력한다.
    - `.gitignore`에 작성된 파일들은 git에 올라가지 않으므로 따로 관리하는 API_KEY와 같은 값들은  `Environment variables`에 입력해줘야 한다.



- git으로 관리하기
  - 기존에 git으로 관리하던 폴더(`.git`폴더가 있는 폴더) 내부에 Vue 프로젝트가 있다면 Vue 프로젝트 내부에도 `.git` 폴더가 있기 때문에 충돌이 날 수 있으므로 따로 빼서 관리해야 한다.
  - Vue 프로젝트 내부의 `node_modules` 폴더 내부에 많은 파일이 들어 있어 복사, 붙여넣기가 너무 오래 걸린다.
  - 따라서 `node_modules` 폴더를 통째로 지우고, 남은 폴더를 복사, 붙여넣기 한 후
  - 실행시켜서 터미널에 `$npm i`를 입력하면 `package.json`, `package-lock.json`을 읽어서 `node_modules`를 다시 만들어준다. 
  - `$ npm ls`는 설치한 모듈들을 보여준다.



- Babel
  - 브라우저마다 지원되는 ES 버전이 다르다.
  - ES6의 문법으로 코드를 작성하고 배포하면 ES6를 지원하지 않는 브라우저로 접속할 경우 사이트가 제대로 동작하지 않을 수 있다.
  - Babel은 ES6로 작성한 코드를 이전 버전으로 바꿔준다.





