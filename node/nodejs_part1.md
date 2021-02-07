# Node.js란

- 백엔드
  - 어떤 종류의 데이터를 어떻게 저장할지, 저장된 데이터를 어떻게 보여줄지 등에 관한 로직을 만드는 것이 서버 프로그래밍 또는 백엔드 프로그래밍이다.
  - 백엔드 프로그래밍은 여러 환경으로 진행이 가능하다.
    - 언어에 구애받지 않기 때문에 다양한 언어로 구현이 가능하다.
    - Node.js도 그중 하나로, 자바스크립트로 서버를 구현할 수 있게 해준다.



- Node.js
  - 처음에는 JS를 웹 브라우저에서만 사용했다.
  - 구글이 크롬 웹 브라우저를 소개하면서 V8이라는 JS 엔진을 공개했다.
    - 이 엔진을 기반으로 웹 브라우저뿐 아니라 서버에서도 JS를 사용할 수 있는 런타임을 개발했다.
    - 이것이 바로 Node.js다.



- Koa
  - Node.js 환경에서 웹 서버를 구축할 때는 보통 Express, Hapi, Koa 등의 웹 프레임워크를 사용한다.
  - Koa는 Express의 기존 개발 팀이 개발한 프레임워크이다.
    - 기존 Express에서 고치고 싶었던 점들을 개션하면 내부 설계가 완전히 바뀌기 때문에 개발 팀이 아예 새로운 프레임워크를 개발했다.
  - Express는 미들웨어, 라우팅, 템플릿, 파일 호스팅과 같은 다양한 기능이 자체적으로 내장되어 있는 반면, Koa는 미들웨어 기능만 갖추고 있으며 나머지는 다른 라이브러리를 적용하여 사용한다.
    - 즉, Koa는 우리가 필요한 기능들만 붙여서 서버를 만들 수 있기에 Express보다 훨씬 가볍다.
  - 또한 Koa는 async/await 문법을 정식으로 지원하기에 비동기 작업을 더 편하게 관리할 수 있다.



# 작업 환경 준비

- Node 설치

  > https://nodejs.org/ko/

  - 공식 페이지에서 설치한다.
  - 설치 후 아래 명령어로 정상적으로 설치 되었는지 확인한다.

  ```bash
  $ node -v
  ```



- 프로젝트 생성

  - blog 디렉터리 생성 후 그 내부에 blog-backend 디렉터리를 만든다.
  - 아래 명령어를 수행하여 디렉터리에 package.json 파일을 생성한다.

  ```bash
  $ yarn init -y
  ```

  - 제대로 생성 되었는지 확인한다.

  ```bash
  $ cat package.json
  ```

  - Koa 프레임워크 설치

  ```bash
  $ yarn add koa
  ```



- ESLint와 Prettier 설정

  - JS 문법을 검사하고 깔끔한 코드를 작성하기 위해 설정한다.
  - 두 기능을 VSCode에서 사용하려면 아래 확장프로그램을 설치해 둔 상태여야 한다.
    - Prettier-Code
    - formatter
  - ESLint 설치하기
    - `yarn add`를 실행할 때 `--dev`는 개발용 의존 모듈로 설치한다는 의미이다.
    - 이렇게 설치하면 package.json에서 devDependencies 쪽에 모듈의 버전 정보가 입력된다.
    - 완료하면 .eslintrc.json 파일이 생성된다.

  ```bash
  $ yarn add --dev eslint
  $ yarn run eslint --init
  yarn run v1.22.10
  $ D:\github\node\blog\blog-backend\node_modules\.bin\eslint --init
  √ How would you like to use ESLint? · problems
  √ What type of modules does your project use? · commonjs
  √ Which framework does your project use? · none
  √ Does your project use TypeScript? · No / Yes
  √ Where does your code run? · node		# 선택할 때 spacebar를 눌러 browser를 해제하고 node를 체크한다.
  √ What format do you want your config file to be in? · JSON
  Successfully created .eslintrc.json file in D:\github\node\blog\blog-backend
  Done in 11.65s.
  ```

  - Prettier 설정
    - blog-backend 디렉터리에 .prettierrc 파일을 만든다.

  ```json
  {
      "singleQuote":true,
      "semi":true,
      "useTabs":false,
      "tabWidth":2,
      "trailingComma":"all",
      "printWidth":80
  }
  ```

  - Prettier에서 관리하는 코드 스타일은 ESLint에서 관리하지 않도록 eslint-config-prettier를 설치하여 적용한다.

  ```bash
  $ yarn add eslint-config-prettier
  ```

  - 그 후 eslint 설정 파일을 아래와 같이 수정한다.

  ```json
  {
      "env": {
          "commonjs": true,
          "es2021": true,
          "node": true
      },
      "extends": ["eslint:recommended", "prettier"],
      "parserOptions": {
          "ecmaVersion": 12
      },
      "rules": {
      }
  }
  ```

  - 제대로 동작하는지 확인하기
    - blog-backend 디렉터리에 src 디렉터리를 생성하고 그 안에 index.js 파일을 만든다.
    - prettier의 경우 쌍따옴표과 홀 따옴표로 잘 바뀌는지 확인하면 된다.

  ```javascript
  // ESLint는 선언했으나 사용하지 않은 변수를 에러로 간주한다.
  // foo에 붉은 밑줄이 가는데 이 위에 커서를 올리거나 VSCode 좌측 하단에 있는 ⓧ버튼을 누르면 상세 정보를 볼 수 있다.
  // 상세 정보에 에러의 이름이 나오는데 아래의 경우 no-unused-vars다.
  const foo = 'foo';
  ```

  - 원하는 대로 수정하기
    - ESLint 의 경우 오류 이름을 알면 해당 오류를 경고로 바꾸거나 비활성화가 가능하다.
    - `rules`에 추가한다.
    - 적용이 안 될 경우파일을 닫았다 다시 열면 적용된다.

  ```json
  {
      "env": {
          "commonjs": true,
          "es2021": true,
          "node": true
      },
      "extends": ["eslint:recommended", "prettier"],
      "parserOptions": {
          "ecmaVersion": 12
      },
      "rules": {
          "no-unused-vars":"warn", // 경고로 바꾼다.
          "no-console":"off"		// 비활성화 한다.
      }
  }
  ```



# Koa 기본 사용법

- 서버 띄우기

  - index.js 파일에 아래 코드를 입력한다.
    - 서버를 포트 4000번으로 열고, 서버에 접속하면 hello world라는 텍스트를 반환하도록 설정했다.

  ```javascript
  const Koa = require('koa');
  
  const app = new Koa();
  
  app.use((ctx) => {
    ctx.body = 'hello world';
  });
  
  // 서버를 포트 4000번으로 연다.
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  ```

  - 서버 실행하기
    - `node`를 통해 JS 파일을 실행할 때는 `node src/index.js`와 같이 전체 경로를 입력하는 것이 맞다.
    - 그러나 index.js 파일은 예외적으로, 디렉터리까지만 입력해도 실행이 가능하다.
    - index.js를 디렉터리를 대표하는 파일이라 생각하면 된다.

  ```bash
  # 아래 명령 입력 후 http://localhost:4000/에 접속하면 hello world라는 문구가 뜬다.
  $ node src
  ```



- 미들웨어

  - Koa 애플리케이션은 미들웨어듸 배열고 구성되어 있다.
    - 위에서 사용한 `app.use` 함수는 미들웨어 함수를 애플리케이션에 등록한다.
  - 미들웨어 함수는 다음과 같은 구조로 이루어져 있다.
    - 첫 번째 파라미터 ctx는 Context의 줄임말로 웹 요청과 응답에 대한 정보를 지니고 있다.
    - next는 현재 처리 중인 미들웨어의 다음 미들웨어를 호출하는 함수이다. 미들웨어를 등록하고 next 함수를 호출하지 않으면, 그 다음 미들웨어를 처리하지 않는다.
    - 만약 미들웨어에서 next를 처리하지 않으면 두 번째 인자는 받지 않아도 괜찮다. 주로 다음 미들웨어를 처리할 필요가 없는 라우트 미들웨어를 나중에 설정할 때 이러한 구조로 next를 생략하여 미들웨어를 작성한다.

  ```javascript
  (ctx,next)=>{ 
  }
  ```

  - 미들웨어는 app.use를 사용하여 등록되는 순서로 처리된다.
    - 다음 예시는 현재 요청을 받은 주소와 우리가 정해 준 숫자를 기록하는 두 개의 미들웨어다.

  ```javascript
  const Koa = require('koa');
  
  const app = new Koa();
  
  app.use((ctx, next) => {
    console.log(ctx.url);
    console.log(1);
    next();
  });
  
  app.use((ctx, next) => {
    console.log(2);
    next();
  });
  
  app.use((ctx) => {
    ctx.body = 'hello world';
  });
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  ```

  - 서버를 실행한 후(실행중이라면 재실행), `http://localhost:4000/`을 열어보면 서버가 실행되고 있는 터미널에 다음과 같은 결과물이 나타난다.
    - 크롬은 사용자가 웹 페이지에 들어가면 해당 사이트의 아이콘 파일인 `/favicon.ico` 파일을 서버에 요청하기 때문에 결과에 `/` 경로(`http://localhost:4000/`의 기본 경로)도 나타나고 `/favocion` 경로도 나타난다.
    - 즉 요청이 2번 가게 되어 1,2도 2번씩 뜨게 된다.

  ```bash
  # 우리가 보낸 요청
  /
  1
  2
  # 크롬이 보낸 요청
  /favicon.ico
  1
  2
  ```

  - 첫 번째 미들웨어의 `next` 함수를 주석 처리

  ```javascript
  const Koa = require('koa');
  
  const app = new Koa();
  
  app.use((ctx, next) => {
    console.log(ctx.url);
    console.log(1);
    // next();
  });
  
  app.use((ctx, next) => {
    console.log(2);
    next();
  });
  
  app.use((ctx) => {
    ctx.body = 'hello world';
  });
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  ```

  - 아래와 같은 결과가 나온다.
    - `next`를 호출하지 않으므로 첫 번째 미들웨어까지만 실행하고 그  아래에 있는 미들웨어는 모두 무시된다.
    - 이런 속성을 사용하여 조건부로 다음 미들웨어 처리를 무시하게 만들 수 있다.

  ```bash
  /
  1
  /favicon.ico
  1
  ```

  - 조건부로 다음 미들웨어 처리를 무시하게 만들기
    - 요청 경로에 authorized=1이라는 쿼리 파라미터가 포함되어 있으면 이후 미들웨어를 처리해 주고, 그렇지 않으면 이후 미들웨어를 처리하지 않는다.
    - 쿼리 파라미터는 문자열이기에 꼭 문자열 형태로 비교해야 한다.
    - `http://localhost:4000/`로 접속하면 Unauthorized라는 문구가 뜬다.
    - `http://localhost:4000/?authorized=1`로 접속하면 hello world가 뜬다.

  ```javascript
  const Koa = require('koa');
  
  const app = new Koa();
  
  app.use((ctx, next) => {
    console.log(ctx.url);
    console.log(1);
    if (ctx.query.authorized !== '1') {
      ctx.status = 401; // Unauthorized
      return;
    }
    next();
  });
  
  app.use((ctx, next) => {
    console.log(2);
    next();
  });
  
  app.use((ctx) => {
    ctx.body = 'hello world';
  });
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  ```

  - `next` 함수는 Promise를 반환한다.
    - Koa와 Express의 차이점이다.
    - `next` 함수가 반환하는 Promise는 다음에 처리해야 할 미들웨어가 끝나야 완료된다.
    - 

  ```javascript
  const Koa = require('koa');
  
  const app = new Koa();
  
  app.use((ctx, next) => {
    console.log(ctx.url);
    console.log(1);
    if (ctx.query.authorized !== '1') {
      ctx.status = 401; // Unauthorized
      return;
    }
    // next 함수 호출 이후에 then을 사용하여 Promise가 끝난 다음에 콘솔에 END가 기록되도록 수정
    next().then(() => {
      console.log('END');
    });
  });
  
  app.use((ctx, next) => {
    console.log(2);
    next();
  });
  
  app.use((ctx) => {
    ctx.body = 'hello world';
  });
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  
  /*
  /?authorized=1
  1
  2				
  END			// 다음에 처리해야 할 미들웨어들이 모두 끝난 후 END가 찍힌다.
  /favicon.ico
  1
  */
  ```

  - `async`/`await` 적용하기

  ```javascript
  const Koa = require('koa');
  
  const app = new Koa();
  
  app.use(async (ctx, next) => {
    console.log(ctx.url);
    console.log(1);
    if (ctx.query.authorized !== '1') {
      ctx.status = 401; // Unauthorized
      return;
    }
    await next();
    console.log('END');
  });
  
  app.use((ctx, next) => {
    console.log(2);
    next();
  });
  
  app.use((ctx) => {
    ctx.body = 'hello world';
  });
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  
  // 결과는 마찬가지다.
  /*
  /?authorized=1
  1
  2
  END
  /favicon.ico
  1
  */
  ```



- nodemon 사용하기

  - 코드를 변경할 때마다 서버를 자동으로 재시작해준다.
  - 설치하기
    - 개발용 의존 모듈로 설치한다.

  ```bash
  $ yarn add --dev nodemon
  ```

  - package.json의 scripts 부분 추가
    - `start`는 서버를 시작하는 명령어
    - `start:dev`는 nodemon을 통해 서버를 실행해 주는 명령어를 넣는다.
    - nodemon은 src 디렉터리를 주시하고 있다가 해당 디렉터리 내부의 어떤 파일이 변경되면, 이를 감지하여 src/index.js 파일을 재시작해 준다.

  ```json
  {
    (...)
    "scripts": {
      "start": "node src",
      "start:dev":"nodemon --watch src/ src/index.js"
    }
  }
  ```

  - 기존에 실행 중이던 서버를 종료한 뒤 `yarn start:dev` 명령어를 실행한다.
    - 이후 기존의 index.js 파일에서 기존의 미들웨어를 모두 삭제한다.
    - 그 후 저장하고 서버가 자동으로 재시작 되는지 확인한다.

  ```javascript
  const Koa = require('koa');
  
  const app = new Koa();
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  ```




## koa-router 사용하기

- koa-router

  - 다른 주소로 요청이 들어올 경우 다른 작업을 처리할 수 있도록 라우터를 사용해야 한다.
  - Koa 자체이 이 기능이 내장되어 있지는 않으므로 ,koa-router 모듈을 설치해야 한다.

  ```bash
  $ yarn add koa-router
  ```



- 기본 사용법

  - koa-router를 불러온 뒤 이를 사용하여 Router 인스턴스를 만든다.
  - 인스턴스의 메소드로 HTTP 메서드를 사용한다.
    - `get` 메서드의 경우, 첫 번째 인자로 라우트의 경로를 받고, 두 번째 인자로 해당 라우트에 적용할 미들웨어 함수를 넣는다.

  ```javascript
  const Koa = require('koa');
  // 불러오고
  const Router = require('koa-router');
  
  const app = new Koa();
  // 인스턴스를 생성한다.
  const router = new Router();
  
  // / 경로일 경우 홈 텍스트를 띄우고,
  router.get('/', (ctx) => {
    ctx.body = '홈';
  });
  
  // /about 경로로 들어올 경우 소개 텍스트를 띄운다.
  router.get('/about', (ctx) => {
    ctx.body = '소개';
  });
  
  // 미들웨어를 사용하기 위해 .use() 사용
  app.use(router.routes()).use(router.allowedMethods());
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  ```

  

- 라우트 파라미터와 쿼리

  - 라우트의 파라미터
    - 라우트의 파라미터를 설정 할 때는 콜론(`:`)을 사용하여 라우트 경로를 설정한다.
    - 파라미터가 있을 수도 있고 없을 수도 있으면 파라미터 뒤에 `?`를 사용한다.
    - 설정한 파라미터는 함수의  `ctx.params` 객체에서 조회 가능하다.
    - 일반적으로 파라미터는 처리할 작업의 카테고리를 받아오거나, 고유 ID 혹은 이름으로 특정 데이터를 조회할 때 사용한다.
  - URL 쿼리
    - `ctx.query`에서 조회할 수 있다.
    - 쿼리 문자열을 자동으로 객체 형태로 파싱해 주므로 별도로 파싱 함수를 돌릴 필요가 없다.
    - 만약 문자열 형태의 쿼리 문자열을 조회해야 한다면 `ctx.querystring`을 사용한다.
    - 일반적으로 쿼리는 옵션에 관련된 정보를 받아온다.

  ```javascript
  const Koa = require('koa');
  const Router = require('koa-router');
  
  const app = new Koa();
  const router = new Router();
  
  router.get('/', (ctx) => {
    ctx.body = '홈';
  });
  
  router.get('/about/:name?', (ctx) => {
    // name의 유무에 따라 다른 결과 출력
    const { name } = ctx.params;
    ctx.body = name ? `${name}의 소개` : '소개';
  });
  
  router.get('/posts', (ctx) => {
    const { id } = ctx.query;
    ctx.body = id ? `포스트 ${id}` : '포스트 아이디가 없습니다.';
  });
  
  // app 인스턴스에 라우터 적용
  app.use(router.routes()).use(router.allowedMethods());
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  ```



- REST API
  - 웹 애플리케이션을 만들려면 데이터베이스에 정보를 입력하고 읽어 와야 한다.
    - 웹 브라우저에서 데이터베이스에 직접 접속하여 데이터를 변경한다면 보안상 문제가 된다.
    - 따라서 REST API를 만들어서 사용한다.
    - 클라이언트가 서버에 자신이 데이터를 조회, 생성, 삭제, 업데이트하겠다고 요청하면, 서버는 필요한 로직에 따라 DB에 접근하여 작업을 처리한다.
  - REST API는 요청 종류에 따라 다른 HTTP 메서드를 사용한다.
    - HTTP 메서드는 여러 종류가 있으며 주로 사용하는 메서드는 아래와 같다.
    - GET: 데이터 조회
    - POST: 데이터 등록
    - DELETE: 데이터 삭제
    - PUT: 데이터를 새 정보로 통째로 교환.
    - PATCH: 데이터의 특정 필드 수정.



- 라우트 모듈화

  - 라우터를 여러 파일에 분리하기
    - 프로젝트를 진행하다 보면 여러 종류의 라우트를 만들게 된다.
    - 각 라우트를 index.js파일 하나에 모두 작성하면, 코드가 지나치게 길어질 뿐 아니라 유지보수도 힘들어진다.
  - `src/api/index.js`

  ```javascript
  const Router = require('koa-router');
  const api = new Router();
  
  api.get('/test', (ctx) => {
    ctx.body = 'test 성공!!';
  });
  
  // 라우터를 내보낸다.
  module.exports = api;
  ```

  - `src/index.js`
    - 아래 코드를 작성하고 `http://localhost:4000/api/test`에 접속하면 'test 성공!!' 텍스트가 뜬다.

  ```javascript
  const Koa = require('koa');
  const Router = require('koa-router');
  
  const api = require('./api');
  
  const app = new Koa();
  const router = new Router();
  
  // 라우터 설정
  router.use('/api', api.routes());
  
  app.use(router.routes()).use(router.allowedMethods());
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  ```



- 라우트 내부에 라우트 생성하기

  - api 라우트 내부에 posts 라우트 만들기
  - `src.api/posts/index.js`

  ```javascript
  const Router = require('koa-router');
  const posts = new Router();
  
  const printInfo = (ctx) => {
    ctx.body = {
      method: ctx.method,
      path: ctx.path,
      params: ctx.params,
    };
  };
  
  posts.get('/', printInfo);
  posts.get('/:id', printInfo);
  posts.post('/', printInfo);
  posts.delete('/:id', printInfo);
  posts.put('/:id', printInfo);
  posts.patch('/:id', printInfo);
  
  module.exports = posts;
  
  ```

  - `src/api/index.js`

  ```javascript
  const Router = require('koa-router');
  const posts = require('./posts');
  
  const api = new Router();
  
  api.use('/posts', posts.routes());
  
  module.exports = api;
  ```



- 컨트롤러 파일 작성

  - 라우트 작성 과정에서 특정 경로에 미들웨어를 등록할 때는 다음과 같이 두 번째 인자에 함수를 선언해 바로 넣어 줄 수 있다.

  ```javascript
  router.get('/',ctx=>{})
  ```

  - 그러나 각 라우트 처리 함수의 코드가 길어지면 라우터 설정을 한 눈에 보기 힘들어진다.
    - 이 라우트 처리 함수들을 다른 파일로 따로 분리해서 관리할 있다.
    - 이 라우트 함수만 모아 놓은 파일을 컨트롤러라 한다.
  - koa-bodyparser 미들웨어를 적용해야 한다.
    - 이 미들웨어는 HTTP 메서드의 Request Body에 JSON 형식으로 데이터를 넣어주면, 이를 파싱하여 서버에서 사용할 수 있게 한다.

  ```bash
  $ yarn add koa-bodyparser
  ```

  - 적용하기
    - 주의할 점은 router를 적용하는 코드의 윗부분에서 해야 한다는 것이다.

  ```javascript
  const Koa = require('koa');
  const Router = require('koa-router');
  const bodyParser = require('koa-bodyparser');
  
  const api = require('./api');
  
  const app = new Koa();
  const router = new Router();
  
  // api 라우트 적용
  router.use('/api', api.routes());
  
  // 라우터에 적용 전에 bodyParser 적용
  app.use(bodyParser());
  
  // app 인스턴스에 라우터 적용
  app.use(router.routes()).use(router.allowedMethods());
  
  app.listen(4000, () => {
    console.log('Listening to port 4000');
  });
  ```

  - `src/api/posts/posts.ctrl.js`
    - `exports.이름=...` 형식으로 함수를 내보내 준다.

  ```javascript
  let postId = 1; // id의 초깃값
  
  // posts 배열 초기 데이터, 아직 DB가 없으므로 이 배열을 DB 처럼 사용.
  const posts = [
    {
      id: 1,
      title: '제목',
      body: '내용',
    },
  ];
  
  /* 포스트 작성
  POST /api/posts
  {title, body}
  */
  exports.write = (ctx) => {
    // REST API의 Request Body는 ctx.request.body에서 조회 가능하다.
    const { title, body } = ctx.request.body;
    postId += 1;
    const post = { id: postId, title, body };
    posts.push(post);
    ctx.body = post;
  };
  
  /* 포스트 목록 조회
  GET /api/posts
  */
  exports.list = (ctx) => {
    ctx.body = posts;
  };
  
  /* 특정 포스트 조회
  GET /api//posts/:id
  */
  exports.read = (ctx) => {
    const { id } = ctx.params;
    // 주어진 id 값으로 포스트를 찾는다.
    // 파리미터로 받아 온 값은 문자열 형식이므로 파라미터를 숫자로 변환하거나 비교할 p.id 값을 문자열로 변경해야 한다.
    const post = posts.find((p) => p.id.toString() === id);
    if (!post) {
      ctx.status = 404;
      ctx.body = {
        message: '포스트가 존재하지 않습니다.',
      };
      return;
    }
    ctx.body = post;
  };
  
  /* 특정 포스트 제거 
  DELETE /api/posts/:id
  */
  exports.remove = (ctx) => {
    const { id } = ctx.params;
    // 해당 id를 가진 post가 몇 번째인지 확인
    const index = posts.findIndex((p) => p.id.toString() === id);
    // 포스트가 없으면 오류를 반환.
    if (index === -1) {
      ctx.status = 404;
      ctx.body = {
        message: '포스트가 존재하지 않습니다.',
      };
      return;
    }
    // index번째 아이템을 제거
    posts.splice(index, 1);
    ctx.status = 204; // No Content
  };
  
  /* 포스트 수정(교체)
  PUT /api/posts/:id
  { title, body }
  */
  exports.replace = (ctx) => {
    // PUT 메서드는 전체 포스트 정보를 입력하여 데이터를 통째로 교체할 때 사용.
    const { id } = ctx.params;
    // 해당 id를 가진 post가 몇 번째인지 확인.
    const index = posts.findIndex((p) => p.id.toString() === id);
    // 포스트가 없으면 오류를 반환.
    if (index === -1) {
      ctx.status = 404;
      ctx.body = {
        message: '포스트가 존재하지 않습니다.',
      };
      return;
    }
    // 전체 객체를 덮어씌운다.
    // 따라서 id를 제외한 기존 정보를 날리고, 객체를 새로 만든다.
    posts[index] = {
      id,
      ...ctx.request.body,
    };
    ctx.body = posts[index];
  };
  
  /* 포스트 수정(특정 필드 변경)
  PATCH /api/posts/:id
  { title, body }
  */
  exports.update = (ctx) => {
    // PATCH 메서드는 주어진 필드만 교체.
    const { id } = ctx.params;
    // 해당 id를 가진 post가 몇 번째인지 확인.
    const index = posts.findIndex((p) => p.id.toString() === id);
    // 포스트가 없으면 오류를 반환합니다.
    if (index === -1) {
      ctx.status = 404;
      ctx.body = {
        message: '포스트가 존재하지 않습니다.',
      };
      return;
    }
    // 기존 값에 정보를 덮어씌운다.
    posts[index] = {
      ...posts[index],
      ...ctx.request.body,
    };
    ctx.body = posts[index];
  };
  ```

  - 위에서 내보낸 함수를 받아서 사용한다.
    - `const 모듈이름=require('파일이름')`으로 불러온다.
    - `모듈이름.이름()`으로 사용한다.

  ```javascript
  const Router = require('koa-router');
  const postsCtrl = require('./posts.ctrl');
  
  const posts = new Router();
  
  posts.get('/', postsCtrl.list);
  posts.get('/:id', postsCtrl.read);
  posts.post('/', postsCtrl.write);
  posts.delete('/:id', postsCtrl.remove);
  posts.put('/:id', postsCtrl.replace);
  posts.patch('/:id', postsCtrl.update);
  
  module.exports = posts;
  ```

  - 포스트맨으로 테스트 한다.
    - PATCH의 경우 title만 변경했을 때, 기존 body 내용을 유지하며, title만 변경된다.
    - PUT의 경우 기존 내용을 유지하는 것이 아니라 전부 덮어써 버린다.
    - 따라서 title만 변경할 경우 body는 사라져 버린다.
    - 그러므로 PUT으로 변경할 때는 모든 필드가 다 있는지 검증하는 작업이 필요하다.





# Node.js에서 ES 모듈 import/export 문법 사용하기

- ES 모듈 import/export 문법은 Node.js에서 아직 정식으로 지원되지 않는다.
  - Node.js에 해당 기능이 구현되어 있기는 하지만 아직 실험 단계이기에 기본 옵션으로는 사용할 수 없다.
  - 확장자를 .mjs로 사용하고 node를 실행할 때 `--experimental-modules`라는 옵션을 넣어 주어야 한다.
  - Node.js에서 꼭 import/export 문법을 사용해야 할 필요는 없지만, 이 문법을 사용하면 코드가 더욱 깔끔해진다.
  - esm이라는 라이브러리를 사용하면 사용이 가능하다.



- esm 사용하기

  - 설치

  ```bash
  $ yarn add esm
  ```

  - 기존 src/index.js 파일을 main.js로 변경하고, index.js 파일을 새로 생성해서 아래 코드를 작성한다.

  ```javascript
  // 이 파일에서만 no-global-assign Eslint 옵션을 비활성화 한다.
  /* eslint-disable no-global-assign */
  
  require = require('esm')(module /*, options*/);
  module.exports = require('./main.js');
  ```

  - package.json의 scripts 부분을 수정한다.

  ```json
  "scripts": {
    "start": "node -r esm src",
    "start:dev": "nodemon --watch src/ -r esm src/index.js"
  }
  ```

  - ESLint에서 import/export 구문을 사용해도 오류로 간주하지 않도록 다음과 같이 수정한다.
    - sourceType 값을 module로 설정한다.

  ```json
  {
      (...)
      "parserOptions": {
          "ecmaVersion": 12,
          "sourceType": "module",
      },
      (...)
  }
  ```



- 기존 코드 ES Module 형태로 변경하기

  - src/posts/posts.ctrl.js 파일에서 `exports` 코드를 `export const`로 모두 변환한다.

  ```javascript
  (...)
  export const write = (ctx) => {(...)}
  export const list = (ctx) => {(...)}
  export const read = (ctx) => {(...)}
  export const remove = (ctx) => {(...)}
  export const replace = (ctx) => {(...)}
  export const update = (ctx) => {(...)};
  ```

  - src/api/posts/index.js 파일을 수정한다.
    - 여기까지 작성하고 저장하면 서버에서 오류가 발생할 것인데, 정상이다.

  ```javascript
  import Router from 'koa-router';
  import * as postsCtrl from './posts.ctrl';
  
  const posts = new Router();
  
  posts.get('/', postsCtrl.list);
  posts.get('/:id', postsCtrl.write);
  posts.post('/', postsCtrl.read);
  posts.delete('/:id', postsCtrl.remove);
  posts.put('/:id', postsCtrl.replace);
  posts.patch('/:id', postsCtrl.update);
  
  export default posts;
  ```

  - src/api/index.js 파일을 수정한다.

  ```javascript
  import Router from 'koa-router';
  import posts from './posts';
  
  const api = new Router();
  
  api.use('/posts', posts.routes());
  
  export default api;
  ```

  - src/main.js 파일을 수정한다.

  ```javascript
  require('dotenv').config();
  import Koa from 'koa';
  import Router from 'koa-router';
  import bodyParser from 'koa-bodyparser';
  import mongoose from 'mongoose';
  import api from './api';
  
  (...)
  ```

  - 여기까지 하고 서버를 구동시킨 후 `http://localhost:4000/api/posts`에 요청을 보내 잘 동작하는지 확인한다.
  - 마지막으로 루트 디렉토리에 jsconfig.json을 작성한다.
    - 아래와 같이 작성해 주면 나중에 자동 완성을 통해 모듈을 불러올 수 있다.

  ```json
  {
      "compilerOptions": {
          "target": "es2015",
          "module": "es2015",
      },
      "include": ["src/**/*"]
  }
  ```

  





















