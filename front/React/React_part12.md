# 서버 사이드 렌더링 Part 2

## 데이터 로딩

- 데이터 로딩
  - 데이터 로딩이란 API 요청을 의미한다.
  - 서버 사이드 렌더링을 구현할 때 해결하기가 매우 까다로운 문제 중 하나이다.
    - 일반적인 브라우저 환경에서는 API를 요청하고 응답을 받아 와서 리액트 state 혹은 리덕스 스토어에 넣으면 자동으로 리렌더링되므로 크게 신경쓸 필요가 없다.
    - 그러나 서버의 경우 문자열 형태로 렌더링하는 것이므로 state나 리덕스 스토어의 상태가 바뀐다고 해서 자동으로 렌더링되지 않는다.
    - 그 대신 `renderToString` 함수를 한 번 더 호출해 주어야 한다.
    - 또한 서버에서는 `componentDidMount` 같은 라이프사이클 API도 사용할 수 없다.
  - 서버 사이드 렌더링에서 데이터 로딩을 해결하는 방법은 다양하다.
    - `redux-thunk` 혹은 `redux-saga`를 활용하는 방법이 있다.





### redux-thunk 사용

- redux-thunk 코드 준비하기

  - 필요한 라이브러리 설치

  ```bash
  $ yarn add redux react-redux redux-thunk axios
  ```

  - Ducks 패턴을 사용하여 리덕스 모듈 작성
    - JSONPlaceholder에서 제공하는 API를 호출하여 테스트용 데이터를 조회한다.

  ```react
  import axios from "axios";
  
  const GET_USERS_PENDING = "users/GET_USERS_PENDING";
  const GET_USERS_SUCCESS = "users/GET_USERS_SUCCESS";
  const GET_USERS_FAILURE = "users/GET_USERS_FAILURE";
  
  const getUsersPending = () => ({ tpye: GET_USERS_PENDING });
  const getUsersSuccess = (payload) => ({ type: GET_USERS_SUCCESS, payload });
  const getUsersFailure = (payload) => ({
    type: GET_USERS_FAILURE,
    error: true,
    payload,
  });
  
  export const getUsers = () => async (dispatch) => {
    try {
      dispatch(getUsersPending);
      const response = await axios.get(
        "https://jsonplaceholder.typicode.com/users"
      );
      dispatch(getUsersSuccess(response));
    } catch (e) {
      dispatch(getUsersFailure(e));
      throw e;
    }
  };
  
  const initialState = {
    users: null,
    user: null,
    loading: {
      users: false,
      user: false,
    },
    error: {
      users: null,
      user: null,
    },
  };
  
  function users(state = initialState, action) {
    switch (action.type) {
      case GET_USERS_PENDING:
        return {
          ...state,
          loading: { ...state.loading, users: true },
        };
      case GET_USERS_SUCCESS:
        return {
          ...state,
          loading: { ...state.loading, users: false },
          users: action.payload.data,
        };
      case GET_USERS_FAILURE:
        return {
          ...state,
          loading: { ...state.loading, users: false },
          error: { ...state.error, users: action.payload },
        };
      default:
        return state;
    }
  }
  
  export default users;
  ```

  - 루트 리듀서 생성

  ```react
  import React from "react";
  import ReactDOM from "react-dom";
  import "./index.css";
  import App from "./App";
  import reportWebVitals from "./reportWebVitals";
  import { BrowserRouter } from "react-router-dom";
  import { Provider } from "react-redux";
  import { applyMiddleware, createStore } from "redux";
  import rootReducer from "./modules";
  import thunk from "redux-thunk";
  
  const store = createStore(rootReducer, applyMiddleware(thunk));
  
  ReactDOM.render(
    <React.StrictMode>
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    </React.StrictMode>,
    document.getElementById("root")
  );
  
  reportWebVitals();
  ```



- Users, UsersContainer 컴포넌트 준비하기

  - Users

  ```react
  import React from "react";
  import { Link } from "react-router-dom";
  
  const Users = ({ users }) => {
    if (!users) return null; // users가 유효하지 않다면 아무것도 보여 주지 않음
    return (
      <div>
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              <Link to={`/users/${user.id}`}>{user.username}</Link>
            </li>
          ))}
        </ul>
      </div>
    );
  };
  
  export default Users;
  ```

  - UserContainer
    - 서버 사이드 렌더링을 할 때는 이미 있는 정보를 재요청하지 않게 처리하는 작업이 중요하다.
    - 이 작업을 하지 않으면 서버 사이드 렌더링 후 브라우저에서 페이지를 확인할 때 이미 데이터를 가지고 있음에도 불구하고 불필요한 API를 호출하게 된다.

  ```react
  import React, { useEffect } from "react";
  import { connect } from "react-redux";
  import Users from "../components/Users";
  import { getUsers } from "../modules/users";
  
  const UsersContainer = ({ users, getUsers }) => {
    // 컴포넌트가 마운트 된 후 호출
    useEffect(() => {
      if (users) return; // users가 이미 유효하다면 요청하지 않음
      getUsers();
    }, [getUsers, users]);
    return <Users users={users} />;
  };
  
  export default connect((state) => ({ users: state.users.users }), { getUsers })(
    UsersContainer
  );
  ```

  - 컴포넌트를 보여 줄 페이지 컴포넌트를 만든다.

  ```react
  import React from "react";
  import UsersContainer from "../containers/UsersContainer";
  
  const UsersPage = () => {
    return <UsersContainer />;
  };
  
  export default UsersPage;
  ```

  - 라우트 설정을 해준다.

  ```react
  import React from "react";
  import { Route } from "react-router-dom";
  import Menu from "./components/Menu";
  import RedPage from "./pages/RedPage";
  import BluePage from "./pages/BluePage";
  import UsersPage from "./pages/UsersPage";
  
  const App = () => {
    return (
      <div>
        <Menu />
        <hr />
        <Route path="/red" component={RedPage} />
        <Route path="/blue" component={BluePage} />
        <Route path="/users" component={UsersPage} />
      </div>
    );
  };
  
  export default App;
  ```

  - 브라우저에서 더욱 쉽게 `/users` 경로로 이동할 수 있도록 Menu 컴포넌트도 수정한다.

  ```react
  import React from "react";
  import { Link } from "react-router-dom";
  const Menu = () => {
    return (
      <ul>
        <li>
          <Link to="/red">Red</Link>
        </li>
        <li>
          <Link to="/blue">Blue</Link>
        </li>
        <li>
          <Link to="/users">Users</Link>
        </li>
      </ul>
    );
  };
  
  export default Menu;
  ```

  - 아직 데이터 로딩에 대한 서버 사이드 렌더링 구현이 끝나진 않았지만, 데이터 로딩 자체가 잘 구현되는지 확인해본다.



- PreloadContext 만들기

  - 서버 사이드 렌더링에서의 API 요청
    - 현재 `getUsers` 함수(API 요청을 보내는 함수)는 UserContainer의 `useEffect` 부분에서 호출된다.
    - 이를 클래스형으로 작성했다면 `componentDidMount`에서 호출했을 것이다.
    - 서버 사이드 렌더링을 할 때는 `useEffect`나 `componentDidMount`에서 설정한 작업이 호출되지 않는다.
    - 렌더링하기 전에 API를 요청한 뒤 스토어에 데이터를 담아야 하는데, 서버 환경에서 이러한 작업을 하려면 클래스형 컴포넌트가 지니고 있는 `constructor` 메서드를 사용하거나 `render` 함수 자체에서 처리해야 한다.
    - 그리고 요청이 끝날 때까지 대기했다가 다시 렌더링해 주어야 한다.
  - 위 작업을 PreloadContext를 만들고, 이를 사용하는 Preloader 컴포넌트를 만들어 처리할 것이다.
    - src/lib/PreloadContext.js 작성
    - `PreloadContext`는 서버 사이드 렌더링 과정에서 처리해야 할 작업들을 실행하고, 만약 기다려야 하는 프로미스가 있다면 프로미스를 수집한다.
    - 모든 프로미스를 수집한 뒤, 수집된 프로미스들이 끝날 때까지 기다렸다가 그다음에 다시 렌더링하면 데이터가 채워진 상태로 컴포넌트들이 나타나게 된다.
    - `Preloader` 컴포넌트는 `resolve`라는 함수를 props로 받아 오며, 컴포넌트가 렌더링될 때 서버 환경에서만 resolve 함수를 호출해 준다. 

  ```react
  import { createContext, useContext } from "react";
  
  // 클라이언트 환경: null
  // 서버 환경: {done:false, promises: []}
  const PreloadContext = createContext(null);
  export default PreloadContext;
  
  // resolve는 함수 타입이다.
  export const Preloader = ({ resolve }) => {
    const preloadContext = useContext(PreloadContext);
    if (!preloadContext) return null; // context 값이 유효하지 않다면 아무것도 하지 않음
    if (preloadContext.done) return null; // 이미 작업이 끝났다면 아무것도 하지 않음
  
    // promises 배열에 프로미스 등록
    // 설령 resolve 함수가 프로미스를 반환하지 않더라도, 프로미스 취급을 하기 위해 Promise.resolve 함수 사용
    preloadContext.promises.push(Promise.resolve(resolve()));
    return null;
  };
  ```

  - UsersContainer에서 사용하기

  ```react
  (...)
  import { Preloader } from "../lib/PreloadContext"
  
  const UsersContainer = ({ users, getUsers }) => {
    (...)
    return (
      <>
        <Users users={users} />
        <Preloader resolve={getUsers} />
      </>
    );
  };
  
  (...)
  ```



- 서버에서 리덕스 설정 및 PreloadContext 사용하기

  - 서버에서 리덕스를 설정해 준다.
    - 브라우저에서 할 때와 큰 차이가 없다.
    - 주의할 점은 서버가 실행될 때 스토어를 한 번만 만드는 것이 아니라, 요청이 들어올 때마다 새로운 스토어를 만든다는 것이다.

  ```react
  // index.server.js
  (...)
  import rootReducer from "./modules";
  import { applyMiddleware, createStore } from "redux";
  import thunk from "redux-thunk";
  import { Provider } from "react-redux";
  
  (...)
  
  const app = express();
  
  const serverRender = async (req, res, next) => {
    const context = {};
    const store = createStore(rootReducer, applyMiddleware(thunk));
  
    const jsx = (
      <Provider store={store}>
        <StaticRouter location={req.url} context={context}>
          <App />
        </StaticRouter>
      </Provider>
    );
  
    const root = ReactDOMServer.renderToString(jsx);
    res.send(createPage(root));
  };
  
  (...)
  ```

  - `PreloadContext`를 사용하여 프로미스들을 수집하고 기다렸다 다시 렌더링하록 코드를 작성

  ```react
  (...)
  import PreloadContext from "./lib/PreloadContext";
  
  (...)
  
  const serverRender = async (req, res, next) => {
    const context = {};
    const store = createStore(rootReducer, applyMiddleware(thunk));
  
    const preloadContext = {
      done: false,
      promise: [],
    };
  
    const jsx = (
      <PreloadContext.Provider value={preloadContext}>
        <Provider store={store}>
          <StaticRouter location={req.url} context={context}>
            <App />
          </StaticRouter>
        </Provider>
      </PreloadContext.Provider>
    );
  
    ReactDOMServer.renderToStaticMarkup(jsx); // renderToStaticMarkup으로 한번 렌더링
  
    try {
      await Promise.all(preloadContext.promises); // 모든 프로미스를 기다린다.
    } catch (e) {
      return res.status(500);
    }
    preloadContext.done = true;
    const root = ReactDOMServer.renderToString(jsx); // 렌더링을 하고
    res.send(createPage(root)); // 클라이언트에게 결과물을 응답한다.
  };
  
  (...)
  ```

  - 첫 번째 렌더링을 할 때는 `renderToString` 대신 `renderToStaticMarkup`라는 함수를 사용했다.
    - `renderToStaticMarkup`은 리액트를 사용하여 정적인 페이지를 만들 때 사용한다.
    - 이 함수로 만든 리액트 렌더링 결과물은 클라이언트 쪽에서 HTML DOM 인터렉션을 지원하기 힘들다.
    - 지금 단계에서 `renderToString`  대신 `renderToStaticMarkup`를 사용한 이유는 단지 Preloader로 넣어 주었던 함수를 호출하기 위해서이다.
    - 또한 `renderToStaticMarkup`가 `renderToString` 보다 처리 속도가 조금 더 빠르다.



- 스크립트로 스토어 초기 상태 주입하기

  - 서버에서 만들어 준 상태를 브라우저에서 재사용하기
    - 지금까지 작성한 코드는 API를 통해 받아 온 데이터를 렌더링하지만, 렌더링하는 과정에서 서버에서 만들어진 스토어의 상태를 브라우저에서 재사용하지 못하는 상황이다.
    - 현재 스토어 상태를 문자열로 변환한 뒤 스크립트로 주입해주어 브라우저에서도 서버에서 만든 스토어의 상태를 사용할 수 있게 할 것이다.

  - index.server.js

  ```react
  (...)
  
  function createPage(root, stateScript) {
    return `<!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="utf-8" />
        <link rel="shortcut icon" href="/favicon.ico" />
        <meta
          name="viewport"
          content="width=device-width,initial-scale=1,shrink-to-fit=no"
        />
        <meta name="theme-color" content="#000000" />
        <title>React App</title>
        <link href="${manifest.files["main.css"]}" rel="stylesheet" />
      </head>
      <body>
        <noscript>You need to enable JavaScript to run this app.</noscript>
        <div id="root">
          ${root}
        </div>
        ${stateScript}
        <script src="${manifest.files["runtime-main.js"]}"></script>
        ${chunks}
        <script src="${manifest.files["main.js"]}"></script>
      </body>
      </html>
        `;
  }
  
  const app = express();
  
  const serverRender = async (req, res, next) => {
    (...)
  
    const root = ReactDOMServer.renderToString(jsx);
    // JSON을 문자열로 변환하고 악성 스크립트가 실행되는 것을 방지하기 위해 <를 치환 처리
    const stateString = JSON.stringify(store.getState()).replace(/</g, "\\u003c");
    const stateScript = `<script>__PRELOADED_STATE__=${stateString}</script>`; // 리덕스 초기 상태를 스크립트로 주입한다.
    res.send(createPage(root,stateScript)); // 클라이언트에게 결과물을 응답한다.
  };
  
  (...)
  ```

  - index.js

  ```react
  (...)
  
  const store = createStore(
    rootReducer,
    window.__PRELOADED_STATE__, // 이 값을 초기 상태로 사용한다.
    applyMiddleware(thunk)
  );
  
  ReactDOM.render(...);
  
  reportWebVitals();
  ```

  - 빌드 후 서버를 실행하여 결과물 확인하기
    - 개발자 도구의 Network 탭에서 users를 클릭 후 Repsonse를 확인.
  - 만약 문제가 있을 경우 build 폴더를 전부 지우고 아래 명령어를 다시 실행
  
  ```bash
  $ yarn build
  $ yarn build:server
  $ yarn start:server
  ```



### redux-saga 사용

- 필요한 라이브러리 설치

  ```bash
  $ yarn add redux-saga
  ```



- redux-saga 코드 준비하기

  - moudles/users.js

  ```react
  import axios from "axios";
  import { call, put, takeEvery } from "redux-saga/effects";
  
  (...)
  
  const GET_USER = "user/GET_USER";
  const GET_USER_SUCCESS = "user/GET_USER_SUCCESS";
  const GET_USER_FAILURE = "user/GET_USER_FAILURE";
  
  (...)
  
  export const getUser = (id) => ({ type: GET_USER, payload: id });
  const getUserSuccess = (data) => ({ type: GET_USER_SUCCESS, payload: data });
  const getUserFailure = (error) => ({
    type: GET_USER_FAILURE,
    payload: error,
    error: true,
  });
  
  const getUserById = (id) =>
    axios.get(`https://jsonplaceholder.typicode.com/users/${id}`);
  
  function* getUserSaga(action) {
    try {
      const response = yield call(getUserById, action.payload);
      yield put(getUsersSuccess(response.data));
    } catch (e) {
      yield put(getUserFailure);
    }
  }
  
  export function* usersSaga() {
    yield takeEvery(GET_USER, getUserSaga);
  }
  
  (...)
  
  function users(state = initialState, action) {
    switch (action.type) {
      (...)
      case GET_USER:
        return {
          ...state,
          loading: { ...state.loading, user: true },
          error: { ...state.error, user: null },
        };
      case GET_USER_SUCCESS:
        return {
          ...state,
          loading: { ...state.loading, user: false },
          user: action.payload,
        };
      case GET_USER_FAILURE:
        return {
          ...state,
          loading: { ...state.loading, user: false },
          error: { ...state.error, user: action.payload },
        };
      default:
        return state;
    }
  }
  
  export default users;
  ```

  - 리덕스 스토어에 적용하기 위해 루트 사가를 만든다.

  ```react
  import { combineReducers } from "redux";
  import { all } from "redux-saga/effects";
  import users, { usersSaga } from "./users";
  
  export function* rootSaga() {
    yield all([usersSaga()]);
  }
  
  const rootReducer = combineReducers({ users });
  export default rootReducer;
  ```

  - 스토어를 생성할 때 미들웨어를 적용하기

  ```react
  (...)
  import createSagaMiddelware from "redux-saga";
  
  const sagaMiddleware = createSagaMiddelware();
  
  const store = createStore(
    rootReducer,
    window.__PRELOADED_STATE__, // 이 값을 초기 상태로 사용한다.
    applyMiddleware(thunk, sagaMiddleware)
  );
  
  sagaMiddleware.run(rootSaga);
  
  ReactDOM.render(...);
  
  reportWebVitals();
  ```



- User, UserContainer 컴포넌트 준비하기

  - User 컴포넌트 만들기

  ```react
  import React from "react";
  
  const User = ({ user }) => {
    const { email, name, username } = user;
    return (
      <div>
        <h1>
          {username}({name})
        </h1>
        <p>
          <b>e-mail</b>
          {email}
        </p>
      </div>
    );
  };
  
  export default User;
  ```

  - UserContainer 컴포넌트 만들기
    - 컨테이너에서 유효성 검사를 할 때 아직 정보가 없는 경우에는 user 값이 null을 가리키므로 User 컴포넌트가 렌더링되지 않도록 컨테이너 컴포넌트에서 null을 반환 주어야 한다.
    - 하지만 이번에는 서버 사이드 렌더링을 해야 하기 때문에 null이 아닌 Preloader 컴포넌트를 렌더링하여 반환한다.
    - 이렇게 해 주면 서버 사이드 렌더링을 하는 과정에서 데이터가 없는 경우 `GET_USER` 액션을 발생시킨다.

  ```react
  import React, { useEffect } from "react";
  import { useDispatch, useSelector } from "react-redux";
  import User from "../components/User";
  import { Preloader } from "../lib/PreloadContext";
  import { getUser } from "../modules/users";
  
  const UserContainer = ({ id }) => {
    const user = useSelector((state) => state.users.user);
    const dispatch = useDispatch();
  
    useEffect(() => {
      // user객체 안에 있는 id(user.id)는 숫자인 반면, URL 파라미터로 받아 온 아이디는 문자열이므로 숫자로 변환해 준 다음 비교해야 한다.
      if (user && user.id === parseInt(id, 10)) return; // 사용자가 존재하고, id가 일치한다면 요청하지 않는다.
      dispatch(getUser(id));
    }, [dispatch, id, user]); // id가 바뀔 때 새로 요청해야 한다.
  
    // 컨테이너 유효성 검사 후 return null을 해야 하는 경우에 null 대신 Preloader 반환
    if (!user) {
      return <Preloader resolve={() => dispatch(getUser(id))} />;
    }
  
    return <User user={user} />;
  };
  
  export default UserContainer;
  ```

  - Userspage 컴포넌트에서 렌더링하기
    - Route에 component 대신 render를 설정해 줌으로써 UserContainer를 렌더링할 때 URL 파라미터 id를 props로 바로 집어넣어 줄 수 있다.

  ```react
  import React from "react";
  import { Route } from "react-router-dom";
  import UserContainer from "../containers/UserContainer";
  import UsersContainer from "../containers/UsersContainer";
  
  const UsersPage = () => {
    return (
      <>
        <UsersContainer />;
        <Route
          path="/users/:id"
          render={({ match }) => <UserContainer id={match.params.id} />}
        />
      </>
    );
  };
  
  export default UsersPage;
  ```

  - 제대로 동작하는지 확인
    - 사용자 링크를 클릭했을 때 아래에 사용자 정보가 제대로 뜨면 성공한 것이다.



- redux-saga를 위한 서버 사이드 렌더링 작업

  - redux-thunk와의 차이
    - redux-thunk의 경우 preloader를 통해 호출한 함수들이 Promise를 반환한다.
    - 하지만 redux-saga를 사용하면 Promise를 반환하지 않기 때문에 추가 작업이 필요하다.
  - 서버 사이드 렌더링을 위한 엔트리 파일에 redux-saga 미들워어 적용
    - 아래 코드까지는 브라우저용 인트리 index.js에서 해 준 것과 똑같다.

  ```react
  (...)
  import rootReducer, { rootSaga } from "./modules";
  import createSagaMiddleware from "redux-saga";
  
  (...)
  const serverRender = async (req, res, next) => {
    (...)
    const sagaMiddleware = createSagaMiddleware();
    const store = createStore(
      rootReducer,
      applyMiddleware(thunk, sagaMiddleware)
    );
  
    sagaMiddleware.run(rootSaga);
    (...)
  };
  
  (...)
  ```

  - 위 코드에서 아래와 같이 추가 작업을 해준다.
    - `toPromise`는  `sagaMiddleware.run`을 통해 만든 Task를 Promise로 변환한다.
    - 루트 사가에서 액션을 끝없이 모니터링하기 때문에 별도의 작업을 하지 않으면 이 Promise는 끝나지 않는다.
    - 따라서 redux-saga의 `END`라는 액션을 발생시켜 이 Promise를 끝내줘야 한다.
    - `END` 액션이 발생하면 액션 모니터링 작업이 모두 종료되고, 모니터링되기 전에 시작된 `getUserSaga`와 같은 사가 함수들이 있다면 해당 함수들이 완료되고 나서 Promise가 끝나게 된다.
    - 이 Promise가 끝나는 시점에 리덕스 스토어에는 우리가 원하는 데이터가 채워진다.
    - 그 이후에 다시 렌더링하면 원하는 결과물이 나타난다.

  ```react
  (...)
  import createSagaMiddleware, { END } from "redux-saga";
  
  (...)
  
  const serverRender = async (req, res, next) => {
    (...)
  
    // 기존의 sagaMiddleware.run(rootSaga) 코드를 아래와 같이 변경
    const sagaPromise = sagaMiddleware.run(rootSaga).toPromise();
  
  (...)
  
    ReactDOMServer.renderToStaticMarkup(jsx);
    store.dispatch(END); // redux-saga의 END 액션을 발생시키면 액션을 모니터링하는 사가들이 모두 종료된다.
  
    try {
      await sagaPromise; //기존에 진행 중이던 사가들이 모두 끝날 때까지 기다린다.
      await Promise.all(preloadContext.promises);
    } catch (e) {
      return res.staus(500);
    }
    (...)
  };
  
  (...)
  ```

  - 프로젝트를 빌드하고, 서버 사이드 렌더링 서버를 다시 실행한다.
    - 개발자 도구의 Network 탭을 연다.
    -  `http://localhost:5000/users/1`에 들어가서 새로고침을 한다.
    - 1 파일을 클릭하여 Response를 확인한다(하단의 `{}`를 클릭하여 더 보기 쉽게 한다).
    - 데이터가 채워진 상태로 렌더링 되었는지 확인한다.

  ```bash
  $ yarn build
  $ yarn build:server
  $ yarn start:server
  ```



- usePreloader Hook 만들어서 사용하기

  - Preloader 컴포넌트 대신 커스텀 Hook 사용하기
    - 지금까지 만든 컨테이너에서는 Preloader 컴포넌트를 사용하여 서버 사이드 렌더링을 하기 전 데이터가 필요한 상황에 API를 요청했다.
    - usePreloader라는 커스텀 Hook 함수를 만들어 이 작업을 더욱 편하게 처리할 수 있게 한다.
    - 함수형 컴포넌트 에서는 아래와 같은 커스텀 Hook을 사용하고, 클래스형 컴포넌트에서는 Preloader 컴포넌트를 사용하면 된다.
  - 기존 lib/PreloadContext.js 파일에 커스텀 Hook 함수 작성
    - Preloader 컴포넌트와 코드가 매우 유사하다.
    - 차이가 있다면 `usePreloader`는 함수라는 것이다.

  ```react
  import { createContext, useContext } from "react";
  
  const PreloadContext = createContext(null);
  export default PreloadContext;
  
  export const Preloader = ({ resolve }) => {
    const preloadContext = useContext(PreloadContext);
    if (!preloadContext) return null;
    if (preloadContext.done) return null;
  
    preloadContext.promises.push(Promise.resolve(resolve()));
    return null;
  };
  
  // Hook 형태로 사용할 수 있는 함수
  export const usePreloader = (resolve) => {
    const preloadContext = useContext(PreloadContext);
    if (!preloadContext) return null;
    if (preloadContext.done) return null;
    preloadContext.promises.push(Promise.resolve(resolve()));
  };
  ```

  - Hook을 적용하기

  ```react
  import React, { useEffect } from "react";
  import { useDispatch, useSelector } from "react-redux";
  import User from "../components/User";
  import { usePreloader } from "../lib/PreloadContext";
  import { getUser } from "../modules/users";
  
  const UserContainer = ({ id }) => {
    const user = useSelector((state) => state.users.user);
    const dispatch = useDispatch();
  
    // 서버 사이드 렌더링을 할 때 API 호출하기
    usePreloader(() => dispatch(getUser(id)));
  
    useEffect(() => {
      if (user && user.id === parseInt(id, 10)) return;
      dispatch(getUser(id));
    }, [dispatch, id, user]);
  
    // 컴포넌트가 아닌 null을 반환
    if (!user) return null;
  
    return <User user={user} />;
  };
  
  export default UserContainer;
  ```

  - 실행하기

  ```bash
  $ yarn build
  $ yarn build:server
  $ yarn start:server
  ```



## 서버 사이드 렌더링과 코드 스플리팅

- 서버 사이드 렌더링을 구현한 프로젝트에 코드 스플리팅 도입하기

  - 리액트에서 공식적으로 제공하는 코드 스플리팅 기능인 React.lazy와 Suspense는 서버 사이드 렌더링을 아직 지원하지 않는다.
  - 현재로서는 리액트 공식 매뉴얼에서도 서버 사이드 렌더링과 코드 스플리팅을 함께 사용할 때는 Loadable Components를 사용할 것을 권장한다.
  - Loadable Components에서는 서버 사이드 렌더링을 할 때 필요한 서버 유틸 함수와 웹팩 플러그인, babel 플러그인을 제공해준다.

  - 관련 라이브러리 설치하기

  ```bash
  $ yarn add @loadable/component @loadable/server @loadable/webpack-plugin @loadable/babel-plugin
  ```



- 라우트 컴포넌트 스플리팅하기

  - BluePage,RedPage,UserPage를 스프리팅 할 것이다.

  ```react
  // App.js
  import React from "react";
  import { Route } from "react-router-dom";
  import Menu from "./components/Menu";
  import loadable from "@loadable/component";
  const RedPage = loadable(() => import("./pages/RedPage"));
  const BluePage = loadable(() => import("./pages/BluePage"));
  const UsersPage = loadable(() => import("./pages/UsersPage"));
  
  const App = () => {
    return (
      <div>
        <Menu />
        <hr />
        <Route path="/red" component={RedPage} />
        <Route path="/blue" component={BluePage} />
        <Route path="/users" component={UsersPage} />
      </div>
    );
  };
  
  export default App;
  ```

  - 여기까지 작성 후 프로젝트를 빌드하고 서버 사이드 렌더링 서버도 재시작한다.
    - 크롬 개발자 도구의 Network 탭에서 인터넷 속도를 Slow 3G로 선택한 후 `http://localhost:5000/users/1`에서 새로고침 했을때 어떤 일이 발생하는지 확인한다.
    - 페이지가 처음에 나타났다가, 사라졌다가, 다시 나타난다.
    - 이러한 현상은 사용자에게 불쾌한 사용자 경험을 제공할 수 있다.

  ```bash
  $ yarn build
  $ yarn build:server
  $ yarn start:server
  ```



- 웹팩과 babel 플러그인 적용

  - Loadable Components에서 제공하는 웹팩과 babel 플러그인을 적용하면 깜빡임 현상을 해결할 수 있다.
  - babel 플러그인 적용하기
    - package.json에서 babel을 찾은 뒤, 그 안에 다음과 같이 plugins를 설정한다.

  ```json
  "babel": {
      "presets": [
          "react-app"
      ],
      "plugins":[
          "@loadable/babel-plugin"
      ]
  }
  ```

  - webpack 설정하기
    - config/webpack.config.js를 열어서 상단에 `LoadablePlugin`을 불러오고, 하단에서 plugins를 찾아서 해당 플러그인을 적용한다.

  ```javascript
  "use strict";
  
  const LoadablePlugin = require("@loadable/webpack-plugin");
  (...)
      plugins: [
        new LoadablePlugin(),
        // Generates an `index.html` file with the <script> injected.
        new HtmlWebpackPlugin(...),
        (...)
      ].filter(Boolean),
      (...)
  ```

  - 빌드 후 build 디렉터리에 loadable-start.json 파일이 생성되었는지 확인
    - 이 파일은 각 컴포넌트의 코드가 어떤 청크(chunk) 파일에 들어가 있는지에 대한 정보를 가지고 있다.
    - 서버 사이드 렌더링을 할 때 이 파일을 참고하여 어떤 컴포넌트가 렌더링되었는지에 따라 어떤 파일들을 사전에 불러와야 할지 설정 가능하다.

  ```bash
  $ yarn build
  ```



- 필요한 청크 파일 경로 추출하기

  - 서버 엔트리 코드를 아래와 같이 수정한다.
    - 서버 사이드 렌더링 후 브라우저에서 어떤 파일을 사전에 불러와야 할지 알아내고 해당 파일들의 경로를 추출하기 위해 Loadable Components에서 제공하는 `ChunkExtractor`와 `ChunkExtractorManager`를 사용한다.
    - 이제 Loadable Components를 통해 파일 경로를 조회하므로 기존에 asset-manifest.json을 확인하던 코드는 지운다.

  ```react
  (...)
  import ChunkExtractor, { ChunkExtractorManager } from "@loadable/server";
  
  // 기존에 asset-manifest.json을 확인하던 코드는 지운다.
  const statsFile = path.resolve("./build/loadable-stats.json");
  
  function createPage(root, tags) {
    return `<!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="utf-8" />
        <link rel="shortcut icon" href="/favicon.ico" />
        <meta
          name="viewport"
          content="width=device-width,initial-scale=1,shrink-to-fit=no"
        />
        <meta name="theme-color" content="#000000" />
        <title>React App</title>
        ${tags.styles}
        ${tags.links}
      </head>
      <body>
        <noscript>You need to enable JavaScript to run this app.</noscript>
        <div id="root">
          ${root}
        </div>
        ${tags.scripts}
      </body>
      </html>
        `;
  }
  
  const app = express();
  
  const serverRender = async (req, res, next) => {
    (...)
  
    // 필요한 파일을 추출하기 위한 ChunkExtractor
    const extractor = new ChunkExtractor({ statsFile });
    const jsx = (
      // ChunkExtractorManager 태그로 감싼다.
      <ChunkExtractorManager extractor={extractor}>
        <PreloadContext.Provider value={preloadContext}>
          <Provider store={store}>
            <StaticRouter location={req.url} context={context}>
              <App />
            </StaticRouter>
          </Provider>
        </PreloadContext.Provider>
      </ChunkExtractorManager>
    );
  
  (...)
    const stateString = JSON.stringify(store.getState()).replace(/</g, "\\u003c");
    const stateScript = `<script>__PRELOADED_STATE__ = ${stateString}</script>`;
  
    const tags = {
      scripts: stateScript + extractor.getScriptTags(), // 스크립트 앞부분에 리덕스 상태 넣기
      links: extractor.getLinkTags(),
      styles: extractor.getStyleTags(),
    };
  
    res.send(createPage(root, tags));
  };
  (...)
  ```



- loadableReady와 hydrate

  - `loadableReady`
    - Loadable Components를 사용하면 성능을 최적화하기 위해 모든 JS 파일을 동시에 받아 온다.
    - 모든 스크립트가 로딩되고 나서 렌더링하도록 처리하기 위해서는 `loadableReady`라는 함수를 사용해야 한다.
  - `hydrate`
    - `render` 대신 사용할 수 있는 함수
    - 기존에 렌더링된 결과물이 이미 있을 경우 새로 렌더링하지 않고 기존에 존재하는 UI에 이벤트만 연동하여 애플리케이션을 초기 구동할 때 필요한 리소스를 최소화함으로써 성능을 최적화해 준다.
  - index.js를 아래와 같이 수정한다.

  ```react
  (...)
  import { loadableReady } from "@loadable/component";
  
  (...)
  
  sagaMiddleware.run(rootSaga);
  
  // 같은 내용을 쉽게 재사용할 수 있도록 렌더링할 내용을 하나의 컴포넌르로 묶는다.
  const Root = () => {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    );
  };
  
  const root = document.getElementById("root");
  
  // 프로덕션 환경에서는 loadableReady와 hydrate를 사용하고
  // 개발 환경에서는 기존 방식으로 처리
  if (process.env.NODE_ENV === "production") {
    loadableReady(() => {
      ReactDOM.hydrate(<Root />, root);
    });
  } else {
    ReactDOM.render(<Root />, root);
  }
  
  reportWebVitals();
  ```



- 프로젝트 빌드하고 확인해보기

  - 빌드하기

  ```bash
  $ yarn build
  $ yarn build:server
  $ yarn start:server
  ```

  - `http://localhost:5000/users`에 들어가서 새로고침을 해본다.
    - Network 탭에서 users 파일을 클릭하고 Response를 확인해본다.
    - 렌더링 결과물의 아래 script태그에 청크파일이 제대로 주입되었는지 확인한다.



## 서버 사이드 렌더링의 환경 구축을 위한 대안

- 서버 사이드 렌더링은 번거로운 작업이다.
  - 서버 사이드 렌더링 자체만 보면 꽤나 간단한 작업이지만 데이터 로딩, 코드 스플리팅까지 고려하면 상당히 번거로운 작업이다.
  - 이렇게 설정을 하나 하나 직접 하는 것이 귀찮다면 아래와 같은 대안이 있다.
    - Next.js
    - Razzle



- Next.js
  - Next.js라는 리액트 프레임워크를 사용하면 이 작업을 최소한의 설정으로 간단하게 처리할 수 있다.
  - 몇 가지 제한이 존재한다.
    - 대표적으로 리액트 라우터와 호환되지 않는다는 제한이 존재한다.
    - 리액트 라우터는 컴포넌트 기반으로 라우트를 설정하는 반면 Next.js는 파일 시스템에 기반하여 라우트를 설정한다.
    - 따라서 이미 작성된 프로젝트에 적용하기 까다롭다.
    - 다양한 작업들을 모두 대신해 주기 때문에 실제 작동 원리를 파악하기 힘들어질 수 있다.
  - 그러나 사용하기 쉽다는 장점이 있다.



- Razzle
  - Next.js처럼 서버 사이드 렌더링을 쉽게 할 수 있도록 해 주는 도구이다.
  - 프로젝트 구성이 CRA와 매우 유사하다는 장점이 있다.
    - 그렇기에 프로젝트의 구조를 마음대로 설정할 수 있으며, 리액트 라우터와도 잘 호환된다.
  - 그러나 코드 스플리팅 시 발생하는 깜빡임 현상을 해결하기 어렵다는 단점이 있다.
  - 또한, 이 프로젝트에서 최신 버전의 Loadable Components가 기본 설정으로는 작동하지 않아서 적용하기 까다롭다.



