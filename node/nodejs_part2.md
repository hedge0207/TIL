# MongoDB와 연동

## MongoDB 사용 준비

- 설치

  > https://www.mongodb.com/try/download/community

  - 위 사이트에서 설치한다.
  - 설치 도중 Complete로 할지, Custom으로 할지 선택하는 부분이 나오는데, Complete로 설치하면 된다.
  - MongoDB Compass는 DB를 GUI로 확인할 수 있게 해주는 프로그램이다.
    - hostname에 localhost
    - port에 27017을 입력하면 하고 connect 버튼을 누르면 된다.



- 작동 확인

  - 터미널에서 MongoDB가 설치된 경로로 이동한 다음 `mongo`를 입력
    - 터미널 기반 MongoDB 클라이언트가 실행 된다.

  ```bash
  $ mongo
  ```

  - `version()` 명령어를 입력하고 버전이 잘 뜨는지 확인한다.

  ```bash
  $ version()
  ```



- mongoose

  - mongoose는 Node.js 환경에서 사용하는 MongoDB 기반 ODM(Object Data Modeling) 라이브러리이다.
  - 데이터베이스 문서들을 JS 객체처럼 사용할 수 있게 해준다.
  - 설치
    - dotenv는 환경변수들을 파일에 넣고 사용할 수 있게 하는 개발 도구이다.
    - mongoose를 사용하여 MongoDB에 접속할 때, 서버에 주소나 계정 및 비밀번호가 필요할 경우도 있다.
    - 이렇게 민감하거나 환경별로 달라질 수 있는 값은 코드 안에 직접 작성하지 않고, 환경변수로 설정하는 것이 좋다.
    - 프로젝트를 깃헙에 올릴 때는 환경변수가 들어 있는 파일은 제외시켜 줘야 한다.

  ```bash
  $ yarn add mongoose dotenv
  ```



- 환경 변수 사용하기

  - 환경 변수에는 서버에서 사용할 포트와 MongoDB 주소를 넣을 것이다.
  - 환경 변수 생성
    - 프로젝트의 루트 경로에 .env 파일을 만들고 다음 내용을 입력한다.
    - blog는 우리가 사용할 DB 이름이다.
    - 지정한 데이터베이스가 서버에 없다면 자동으로 생성해 주므로 사전에 직접 생성할 필요는 없다.

  ```
  PORT=4000
  MONGO_URI=mongodb://localhost:27017/blog
  ```

  - 환경 변수 조회하기
    - `src/main.js` 파일의 맨 위에 다음과 같이 dotenv를 불러와서 `config()` 함수를 호출한다.
    - `process.env` 값을 통해 환경 변수에 접근 가능하다.

  ```javascript
  require('dotenv').config();
  (...)
  
  // 비구조화 할당을 통해 process.env 내부 값에 대한 레퍼런스 만들기
  const { PORT } = process.env;
  
  (...)
  
  // PORT가 지정되어 있지 않다면 4000을 사용
  const port = PORT || 4000;
  app.listen(port, () => {
    console.log('Listening to port %d', port);
  });
  ```



- 서버와 데이터베이스 연결

  - mongoose를 이용하여 서버와 DB를 연결한다.
    - mongoose의 `connect` 함수를 사용한다.

  ```javascript
  require('dotenv').config();
  (...)
  const mongoose = require('mongoose');
  
  const api = require('./api');
  
  const { PORT, MONGO_URI } = process.env;
  
  mongoose
    .connect(MONGO_URI, { useNewUrlParser: true, useFindAndModify: false })
    .then(() => {
      console.log('Connected to MongoDB');
    })
    .catch((e) => {
      console.log(e);
    });
  
  (...)
  ```

  - 이후 서버를 실행했을 때 `Connected to MongoDB` 텍스트가 뜨면 잘 연결된 것이다.





# 데이터베이스 스키마와 모델

- mongoose에는 스키마와 모델이라는 개념이 있다.
  - 스키마
    - 컬렉션에 들어가는 문서 내부의 각 필드가 어떤 형식으로 되어 있는지 정의하는 객체.
    - 스키마를 통해 모델을 만든다.
  - 모델
    - 스키마를 사용하여 만드는 인스턴스.
    - 데이터베이스에서 실제 작업을 처리할 수 있는 함수들을 지니고 있는 객체.
  - 즉 스키마를 활용하여 모델을 만들고 모델을 통해 데이터베이스에서 작업을 처리한다.



- 스키마 생성

  - 관리하기 쉽도록 src/models 디렉터리에 작성한다.
  - mongoose 모듈의 `Schema`를 사용하여 정의한다.
    - 각 필드의 이름과 필드의 데이터 타입 정보가 들어 있는 객체를 작성한다.
    - 필드의 기본 값으로는 default 값을 설정해 주면 된다.

  ```javascript
  // src/models/post.js
  import mongoose from 'mongoose';
  
  const { Schema } = mongoose;
  
  const PostSchema = new Schema({
    title: String,
    body: String,
    tags: [String],   // 문자열로 이루어진 배열
    publishedData: {
      type: Date,
      default: Date.now,  // 현재 날짜를 기본값으로 지정
    },
  });
  ```

  - Schema에서 지원하는 타입

  | 타입                            | 설명                                            |
  | ------------------------------- | ----------------------------------------------- |
  | String                          | 문자열                                          |
  | Number                          | 숫자                                            |
  | Date                            | 날짜                                            |
  | Buffer                          | 파일을 담을 수 있는 버퍼                        |
  | Boolean                         | true, false                                     |
  | Mixed(Chema.types.Mixed)        | 어떤 데이터든 넣을 수 있는 형식                 |
  | ObjectId(Schema.Types.ObjectId) | 객체 아이디. 주로 다른 객체를 참조할 때 넣는다. |
  | Array                           | 배열 형태의 값으로 []로 감싸서 사용한다.        |

  - 스키마 내부에 다른 스키마를 내장시키는 것도 가능하다.
    - `authors: [AuthorSchema]`는 `AuthorSchema`로 이루어진 여러 개의 객체가 들어 있는 배열을 의미한다.

  ```javascript
  const AuthorSchema = new Schema({
      name: String,
      email: String,
  });
  const BookSchema = new Schema({
      title: String,
      description: String,
      authors: [AuthorSchema],
      meta:{
          likes:Number,
      },
      extra: Schema.types.Mixed
  })
  ```



- 모델 생성

  - `mongoose.model` 함수를 사용한다.
    - 첫 번째 파라미터는 스키마 이름을 받는다.
    - 두 번째 파라미터는 스키마 객체를 받는다.
    - 세 번째 파라미터는 컬렉션 이름을 받는다(옵션).

  ```javascript
  import mongoose from 'mongoose';
  
  const { Schema } = mongoose;
  
  const PostSchema = new Schema(...);
  
  const Post = mongoose.model('Post', PostSchema);
  // const Post = mongoose.model('Post', PostSchema, 'my_collection_name');
  export default Post;
  ```

  - 데이터 베이스는 스키마 이름을 정해주면 그 이름을 복수의 형태로 데이터베이스에 컬렉션 이름을 만든다.
    - 위의 경우 실제 데이터 베이스에 만드는 컬렉션 이름은 'posts'이다.
    - 컬렉션 이름을 만들 때 권장되는 컨벤션은 구분자를 사용하지 않고 복수 형태로 사용하는 것이다.
    - 이 컨벤션을 따르고 싶지 않다면 세 번째 파라미터에 원하는 이름을 입력하면 된다.
    - 이 경우 첫 번째 파라미터로 넣어 준 이름은 나중에 다른 스키마에서 현재 스키마를 참조해야 하는 상황에서 사용한다.



# 데이터 CRUD

- 데이터 생성

  - `post/ctrl.js`의 기존 코드를 모두 지우고 아래와 같이 입력
    - 기존 PUT 메서드에 연결했던 replace 함수는 구현하지 않는다.

  ```javascript
  import Post from '../../models/post';
  
  export const write = (ctx) => {};
  
  export const list = (ctx) => {};
  
  export const read = (ctx) => {};
  
  export const remove = (ctx) => {};
  
  export const replace = (ctx) => {};
  
  export const update = (ctx) => {};
  ```

  - 기존 PUT 메서드에 연결했던 replace 함수는 구현하지 않으므로 src/api/posts/index.js에서도 관련 내용을 삭제한다.

  ```javascript
  import Router from 'koa-router';
  import * as postsCtrl from './posts.ctrl';
  
  const posts = new Router();
  
  posts.get('/', postsCtrl.list);
  posts.get('/:id', postsCtrl.read);
  posts.post('/', postsCtrl.write);
  posts.delete('/:id', postsCtrl.remove);
  posts.patch('/:id', postsCtrl.update);
  
  export default posts;
  ```

  - 블로그 포스트를 작성하는 API인 write를 구현

  ```javascript
  import Post from '../../models/post';
  
  /*
  POST /api/posts
  {
    title: '제목',
    body: '내용',
    tags:['태그1','태그2']
  }
  */
  
  export const write = async (ctx) => {
    const { title, body, tags } = ctx.request.body;
    const post = new Post({
      title,
      body,
      tags,
    });
    try {
      await post.save();
      ctx.body = post;
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  
  (...)
  ```

  - 코드 설명
    - 포스트의 인스턴스를만들 때는 `new` 키워드를 사용한다.
    - 생성자 함수의파라미터에 정보를 지닌 객체를 넣는다.
    - 인스턴스를 만든다고 바로 DB에 저장되는 것은 아니다. `save()` 함수를 실행시켜야 DB에 저장된다.
    - `save()` 함수의 반환 값은 Promise이므로 async/await 문법으로 DB 저장 요청을 완료할 때까지 await을 사용하여 대기할 수 있다.
    - await을 사용하기 위해 함수를 선언하는 부분에 async 키워드를 넣었다.
    - 또한 await을 사용할 때는 try/catch 문으로 오류를 처리해야 한다.
  - 이제 포스트맨을 통해 `http://localhost:4000/api/posts`로 요청을 보내본다.
    - MongoDB Compass에서 blog 데이터베이스를 선택한 뒤 posts 컬렉션을 열어 제대로 들어갔는지 확인한다.



- 데이터 조회

  - 모든 데이터 조회
    - 모델 인스턴스의 `find()`함수를 사용한다.
    - `find()` 함수를 사용한 뒤에는 `exec()`을 붙여 줘야 서버에 쿼리를 요청한다.

  ```javascript
  (...)
  
  export const list = async (ctx) => {
    try {
      const posts = await Post.find().exec();
      ctx.body = posts;
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  
  (...)
  ```

  - 특정 데이터 조회
    - 특정 id를 가진 데이터를 조회할 때는 `findById()` 함수를 사용한다.

  ```javascript
  (...)
  
  export const read = async (ctx) => {
    const { id } = ctx.params;
    try {
      const post = await Post.findById(id).exec();
      console.log(post);
      if (!post) {
        ctx.status = 404;
        return;
      }
      ctx.body = post;
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  (...)
  ```



- 데이터 삭제

  - 아래의 함수들을 사용하여 삭제가 가능하다.
    - `remove()`: 특정 조건을 만족하는 데이터를 모두 지운다.
    - `findByIdAndRemove()`: id가 일치하는 데이터를 지운다.
    - `findOneAndRemove()`: 특정 조건을 만족하는 데이터 하나를 찾아서 제거한다.

  - 적용

  ```javascript
  (...)
  export const remove = async (ctx) => {
    const { id } = ctx.params;
    try {
      await Post.findByIdAndRemove(id).exec();
      ctx.status = 204;
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  (...)
  ```



- 데이터 수정

  - 데이터를 업데이트 할 때는 `findByIdAndUpdate()` 함수를 사용한다.
    - 첫 번째 파라미터로 id를 받는다.
    - 두 번째 파라미터로 업데이트 할 내용을 받는다.
    - 세 번째 파라미터로 업데이트의 옵션을 받는다.

  - 적용

  ```javascript
  (...)
  export const update = async (ctx) => {
    const { id } = ctx.params;
    try {
      const post = await Post.findByIdAndUpdate(id, ctx.request.body, {
        new: true, // 이 값을 설정하면 업데이트 된 데이터를 반환한다. false일 때는 업데이트 되기 전의 데이터를 반환한다.
      }).exec();
      if (!post) {
        ctx.status = 404;
        return;
      }
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  ```





# 요청 검증하기

- ObjectId 검증하기

  - id가 어떻게 전달되었냐에 따라 다른 에러를 띄운다.
    - 잘못된 id를 전달했다면 클라이언트 잘못이니 400 Bad Request를 띄우고
    - id가 올바른 ObjectId 형식이 아니라면 500 에러를 띄운다.
  - read, remove,update 세 곳에서 검증을 해야 하므로 세 곳 모두 검증 코드를 넣지 말고 검증하는 미들웨어를 만든다.

  ```javascript
  // src/api/posts/posts.ctrl.js
  import Post from '../../models/post';
  import mongoose from 'mongoose';
  
  const { ObjectId } = mongoose.Types;
  
  export const chekcObjectId = (ctx, next) => {
    const { id } = ctx.params;
    // 유효하지 않은 ObjectId이면 클라이언트에서 잘못한 것이므로 400 에러를 띄운다.
    if (!ObjectId.isValid(id)) {
      ctx.status = 400;
      return;
    }
    return next();
  };
  
  (...)
  ```

  - src/api/posts/index.js에서 ObjectId 검증이 필요한 부분에 방금 만든 미들웨어를 추가한다.

  ```javascript
  import Router from 'koa-router';
  import * as postsCtrl from './posts.ctrl';
  
  const posts = new Router();
  
  posts.get('/', postsCtrl.list);
  posts.post('/', postsCtrl.write);
  posts.get('/:id', postsCtrl.chekcObjectId, postsCtrl.read);
  posts.delete('/:id', postsCtrl.chekcObjectId, postsCtrl.remove);
  posts.patch('/:id', postsCtrl.chekcObjectId, postsCtrl.update);
  
  export default posts;
  ```

  - 위 코드를 리팩토링하면 아래와 같다.
    - /api/posts/:id를 위한 새 라우터를 만들고 `posts`에 해당 라우터를 등록해준다.
    - 굳이 이렇게까지 리팩토링 하지 않아도 된다.

  ```javascript
  import Router from 'koa-router';
  import * as postsCtrl from './posts.ctrl';
  
  const posts = new Router();
  
  posts.get('/', postsCtrl.list);
  posts.post('/', postsCtrl.write);
  
  const post = new Router();
  post.get('/', postsCtrl.read);
  post.delete('/', postsCtrl.remove);
  post.patch('/', postsCtrl.update);
  
  // /:id 주소로 들어오면 postsCtrl.chekcObjectId 미들웨어가 실행된다.
  // 미들웨어의 실행 결과 next()로 빠지면
  // post.routes 중 http 메서드가 맞는 곳으로 빠지게 된다.
  posts.use('/:id', postsCtrl.chekcObjectId, post.routes());
  
  export default posts;
  ```



- Request Body 검증

  - 검증 내용
    - 포스트를 작성할 때 서버는 title, body, tags 값을 모두 받아야 한다.
    - 그리고 클라이언트가 값을 빼먹었을 때는 400 오류가 발생해야 한다.
  - if 문을 사용해도 되지만 수월하게 하기 위해 Joi 라이브러리를 사용할 수도 있다.
    - 보내야 할 값을 안보내거나 타입을 다르게 보내면 응답으로 어떤 것이 문제인지 보내준다.

  ```bash
  $ yarn add joi
  ```

  - write 함수에서 Joi를 활용하여 요청 내용 검증
    - `.required()`인 경우 필수 값이다.

  ```javascript
  (...)
  import Joi from '../../../node_modules/joi/lib/index';
  (...)
  
  export const write = async (ctx) => {
    const schema = Joi.object().keys({
      title: Joi.string().required(),
      body: Joi.string().required(),
      tags: Joi.array().items(Joi.string()).required(),
    });
  
    // 검증 후 실패인 경우 에러 처리
    const result = schema.validate(ctx.request.body);
    if (result.error) {
      ctx.status = 400;
      ctx.body = result.error;
      return;
    }
  
    const { title, body, tags } = ctx.request.body;
    const post = new Post({
      title,
      body,
      tags,
    });
    try {
      await post.save();
      ctx.body = post;
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  
  (...)
  ```

  - update 함수에도 적용

  ```javascript
  (...)
  export const update = async (ctx) => {
    const schema = Joi.object().keys({
      title: Joi.string(),
      body: Joi.string(),
      tags: Joi.array().items(Joi.string()),
    });
  
    // 검증 후 실패인 경우 에러 처리
    const result = schema.validate(ctx.request.body);
    if (result.error) {
      ctx.status = 400;
      ctx.body = result.error;
      return;
    }
    const { id } = ctx.params;
    try {
      const post = await Post.findByIdAndUpdate(id, ctx.request.body, {
        new: true,
      }).exec();
      console.log(post);
      if (!post) {
        ctx.status = 404;
        return;
      }
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  ```



# 페이지네이션 구현

- 가짜 데이터 생성하기

  - src/createFakeData.js

  ```javascript
  import Post from './models/post';
  
  export default function createFakeData() {
    const posts = [...Array(40).keys()].map((i) => ({
      title: `포스트${i}`,
      body:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc nec rutrum est. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed nec enim quis sem tincidunt vehicula ac et sem. Donec interdum ut purus non aliquet. Cras eros odio, egestas in velit et, facilisis lacinia neque. Nulla lobortis mi ut nunc rhoncus, eu ultricies libero consectetur. Donec at mollis tortor, quis maximus enim. Donec scelerisque aliquam faucibus. Pellentesque consectetur porta felis, ut elementum velit fringilla et. Pellentesque est dolor, luctus sed est in, auctor facilisis felis.',
      tags: ['가짜', '데이터'],
    }));
    Post.insertMany(posts, (err, docs) => {
      console.log(docs);
    });
  }
  ```

  - main.js에서 위에서 만든 함수 호출하기

  ```javascript
  (...)
  import createFakeData from './createFakeData';
  
  const { PORT, MONGO_URI } = process.env;
  
  mongoose
    .connect(MONGO_URI, { useNewUrlParser: true, useFindAndModify: false })
    .then(() => {
      console.log('Connected to MongoDB');
      createFakeData();
    })
    .catch((e) => {
      console.log(e);
    });
  
  (...)
  ```

  - 서버 재시작 후 잘 등록 됐으면 main.js에서 `createFakeData`함수를 호출하는 부분을  지운다.



- 페이지 기능을 위한 준비
  - 포스트를 역순으로 불러오기
    - `list` API에서 `exec()`하기 전에 `sort()` 구문을 넣으면 된다.
    - 파라미터는 `{key:-1/1}` 형식으로 넣는다.
    - key에는 정렬할 필드를 넣고,
    - 1로 설정하면 오름차순, -1로 설정하면 내림차순으로 정렬한다.

  ```javascript
  (...)
  
  export const list = async (ctx) => {
    try {
      const posts = await Post.find().sort({ _id: -1 }).exec();
      ctx.body = posts;
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  
  (...)
  ```
  - 불러오는 개수 제한
    - 한 번에 불러오는 개수를 제한할 때는 `limit()`함수를 사용하고 파라미터에는 제한할 숫자를 넣는다. 

  ```javascript
  (...)
  export const list = async (ctx) => {
    try {
      const posts = await Post.find().sort({ _id: -1 }).limit(10).exec();
      ctx.body = posts;
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  (...)
  ```



- 페이지 기능 구현하기

  - `skip()` 함수를 사용한다.
    - 파라미터로 받은 수 만큼의 데이터를 제외하고 그 다음 데이터를 불러온다.
    - 즉, 파라미터에는 (page-1)*10을 넣어주면 된다.

  - 구현

  ```javascript
  (...)
  export const list = async (ctx) => {
    // query는 문자열이기에 숫자로 변환해 줘야한다.
    // 값이 주어지지 않았다면 1을 기본으로 사용하여 첫 페이지를 보내준다.
    const page = parseInt(ctx.query.page || '1', 10);
  
    if (page < 1) {
      ctx.status = 400;
      return;
    }
  
    try {
      const posts = await Post.find()
        .sort({ _id: -1 })
        .limit(10)
        .skip((page - 1) * 10)
        .exec();
      ctx.body = posts;
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  (...)
  ```

  - 마지막 페이지 번호 알려주기
    - 커스텀 헤더를 설정하는 방법을 사용한다.
    - 포스트맨으로 요청을 보낸 후 Header가 제대로 설정되었는지 확인한다.

  ```javascript
  (...)
  export const list = async (ctx) => {
    // query는 문자열이기에 숫자로 변환해 줘야한다.
    // 값이 주어지지 않았다면 1을 기본으로 사용하여 첫 페이지를 보내준다.
    const page = parseInt(ctx.query.page || '1', 10);
  
    if (page < 1) {
      ctx.status = 400;
      return;
    }
  
    try {
      const posts = await Post.find()
        .sort({ _id: -1 })
        .limit(10)
        .skip((page - 1) * 10)
        .exec();
      // 전체 게시글의 개수를 센 후
      const postCount = await Post.countDocuments().exec();
      // Last-Page라는 커스텀 HTTP 헤더를 설정한다.
      ctx.set('Last-Page', Math.ceil(postCount / 10));
      ctx.body = posts;
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  (...)
  ```



- 내용 길이 제한

  - `find()`를 통해 조회한 데이터는 mongoose 문서 인스턴스의 형태이므로 데이터를 바로 변형할 수 없다.
  - 따라서 `toJSON()` 함수를 실행하여 JSON 형태로 변환한 뒤 필요한 변형을 일으켜 줘야 한다.

  ```javascript
  (...)
  export const list = async (ctx) => {
    // query는 문자열이기에 숫자로 변환해 줘야한다.
    // 값이 주어지지 않았다면 1을 기본으로 사용하여 첫 페이지를 보내준다.
    const page = parseInt(ctx.query.page || '1', 10);
  
    if (page < 1) {
      ctx.status = 400;
      return;
    }
  
    try {
      const posts = await Post.find()
        .sort({ _id: -1 })
        .limit(10)
        .skip((page - 1) * 10)
        .exec();
      const postCount = await Post.countDocuments().exec();
      ctx.set('Last-Page', Math.ceil(postCount / 10));
      ctx.body = posts
        .map((post) => post.toJSON())
        .map((post) => ({
          ...post,
          body:
            post.body.length < 200 ? post.body : `${post.body.slice(0, 200)}...`,
        }));
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  (...)
  ```

  - 다른 방법으로 `lean()` 함수를 사용하는 방법도 있다.
    - 이 함수를 사용하면 데이터를 처음부터 JSON 형태로 조회할 수 있다.

  ```javascript
  (...)
  export const list = async (ctx) => {
    // query는 문자열이기에 숫자로 변환해 줘야한다.
    // 값이 주어지지 않았다면 1을 기본으로 사용하여 첫 페이지를 보내준다.
    const page = parseInt(ctx.query.page || '1', 10);
  
    if (page < 1) {
      ctx.status = 400;
      return;
    }
  
    try {
      const posts = await Post.find()
        .sort({ _id: -1 })
        .limit(10)
        .skip((page - 1) * 10)
        .lean()		// lean() 함수를 쓴다.
        .exec();
      const postCount = await Post.countDocuments().exec();
      ctx.set('Last-Page', Math.ceil(postCount / 10));
      ctx.body = posts.map((post) => ({
        ...post,
        body:
          post.body.length < 200 ? post.body : `${post.body.slice(0, 200)}...`,
      }));
    } catch (e) {
      ctx.throw(500, e);
    }
  };
  (...)
  ```

  

