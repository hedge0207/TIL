# 리덕스 미들웨어를 통한 비동기 작업 관리

- 미들웨어란
  - 미들웨어는 액션과 리듀서의 중간자 역할을 한다.
    - 미들웨어는 액션을 디스패치했을 때 리듀서에서 이를 처리하기에 앞서 사전에 지정된 작업들을 처리한다.
  - 리듀서가 액션을 처리하기 전에 미들웨어가 할 수 있는 작업은 여러 가지가 있다.
    - 전달 받은 액션을 단순히 콘솔에 기록하거나
    - 전달 받은 액션 정보를 기반으로 액션을 아예 취소하거나
    - 다른 종류의 액션을 추가로 디스패치 할 수도 있다.
  - 미들웨어(middleware)를 쓰는 이유
    - 리액트 웹 애플리케이션에서 API 서버를 연동할 때는 API 요청에 대한 상태도 잘 관리해야 한다.
    - 예를 들어 요청이 시작되었을 때는 로딩 중임을, 요청이 성공하거나 실패했을 때는 로딩이 끝났음을 명시해야 한다.
    - 요청이 성공하면 서버에서 받아 온 응답에 대한 상태를 관리하고, 요청이 실패하면 서버에서 반환한 에러에 대한 상태를 관리해야 한다.
    - 리액트 프로젝트에서 리덕스를 사용하고 있으며, 비동기 작업을 관리해야 한다면 미들웨어를 사용하여 효율적이고 편하게 상태 관리가 가능하다.



## 미들웨어 만들어보기

- 미들웨어가 어떻게 작동하는지 이해하려면 직접 만들어 보는 것이 가장 효과적이다.
  - 실제 프로젝트를 작업할 때 미들웨어를 직접 만들어서 사용할 일은 그리 많지 않다.
  - 다른 개발자가 만들어 놓은 미들웨어를 사용하면 되기 때문이다.



- 준비하기

  - 필요한 라이브러리들을 설치

  ```bash
  $ yarn add redux react-redux redux-actions
  ```

  - 리덕스 모듈을 작성(src/modules/counter.js)

  ```react
  import { createAction, handleActions } from "redux-actions";
  
  const INCREASE = "counter/INCREASE";
  const DECREASE = "counter/DECREASE";
  
  export const increase = createAction(INCREASE);
  export const decrease = createAction(DECREASE);
  
  // 상태가 꼭 객체일 필요는 없다.
  const initialState = 0;
  
  const counter = handleActions(
    {
      [INCREASE]: (state) => state + 1,
      [DECREASE]: (state) => state - 1,
    },
    initialState
  );
  
  export default counter;
  ```

  - 루트 리듀서를 생성

  ```react
  import { combineReducers } from "redux";
  import counter from "./counter";
  
  const rootReducer = combineReducers({ counter });
  
  export default rootReducer;
  ```

  - 스토어를 생성(src/index.js)
    - Provider로 리액트 프로젝트에 리덕스를 적용

  ```react
  import React from "react";
  import ReactDOM from "react-dom";
  import "./index.css";
  import App from "./App";
  import reportWebVitals from "./reportWebVitals";
  import rootReducer from "./modules";
  import { Provider } from "react-redux";
  import { createStore } from "redux";
  
  const store = createStore(rootReducer);
  
  ReactDOM.render(
    <React.StrictMode>
      <Provider store={store}>
        <App />
      </Provider>
    </React.StrictMode>,
    document.getElementById("root")
  );
  
  reportWebVitals();
  ```

  - 프레젠 테이셔널 컴포넌트 생성(src/components)

  ```react
  import React from "react";
  
  const Counter = ({ onIncrease, onDecrease, number }) => {
    return (
      <div>
        <h1>{number}</h1>
        <button onClick={onIncrease}>+1</button>
        <button onClick={onDecrease}>-1</button>
      </div>
    );
  };
  
  export default Counter;
  ```

  - 컨테이너 컴포넌트를 생성(src/containers)

  ```react
  import React from "react";
  import { connect } from "react-redux";
  import Counter from "../components/Counter";
  import { increase, decrease } from "../modules/counter";
  
  const CounterContainer = ({ number, increase, decrease }) => {
    return (
      <Counter number={number} onIncrease={increase} onDecrease={decrease} />
    );
  };
  
  export default connect((state) => ({ number: state.number }), {
    increase,
    decrease,
  })(CounterContainer);
  ```

  - App 컴포넌트에 렌더링

  ```react
  import React from "react";
  import CounterContainer from "./containers/CounterContainer";
  
  const App = () => {
    return (
      <div>
        <CounterContainer />
      </div>
    );
  };
  
  export default App;
  ```



- 미들웨어 만들기

  - 액션이 디스패치될 때마다 액션의 정보와 디스패치되기 전후의 상태를 콘솔에 보여주는 로깅 미들웨어를 만들어 볼 것이다.
    - 실제 프로젝트를 작업할 때 미들웨어를 직접 만들어서 사용할 일은 그리 많지 않다.
    - 다른 개발자가 만들어 놓은 미들웨어를 사용하면 되기 때문이다.
  - src/lib 디렉터리를 생성하고, 그 안에 loggerMiddleware.js를 생성

  ```react
  const loggerMiddleware = (store) => (next) => (action) => {
    // 미들웨어 기본 구조
  };
  
  /* 풀어서 작성하면 아래와 같다.
  const loggerMiddleware = function (store) {
    return function (next) {
      return function (action) {
        // 미들웨어 기본 구조
      };
    };
  };
  */
  export default loggerMiddleware;
  ```

  - 미들웨어는 결국 함수를 반환하는 함수를 반환하는 함수이다.
    - 파라미터로 받아 오는 `store`는 리덕스 스토어 인스턴스를, `action`은 디스패치된 액션을 가리킨다.
    - `next` 파라미터는 함수 형태이며, `store.dispatch`와 비슷한 역할을 한다.
    - 그러나 `store.dispatch`와 큰 차이가 있는데, `next(action)`를 호출하면 그 다음 처리해야 할 미들웨어에게 액션을 넘겨주고, 만약 그 다음에 미들웨어가 없다면 리듀서에게 액션을 넘겨준다는 것이다.
    - 반면에 `store.dispatch`의 경우, 미들웨어 내부에서 사용하면 첫 번째 미들웨어부터 다시 처리한다. 
    - 따라서 만약 미들웨어 내부에서 `next`를 사용하지 않으면 액션이 리듀서에 전달되지 않는다. 즉, 액션이 무시된다.
  - 이전 상태, 액션 정보, 업데이트된 상태를 보여주는 미들웨어 구현

  ```react
  const loggerMiddleware = (store) => (next) => (action) => {
    // 액션 타입으로 log를 그룹화
    console.group(action && action.type);
    console.log("이전 상태", store.getState());
    console.log("액션", action);
    next(action); // 다음 미들웨어 혹은 리듀서에게 전달
    console.log("업데이트 된 상태", store.getState());
    console.groupEnd(); // 그룹 끝
  };
  
  export default loggerMiddleware;
  ```

  - 미들웨어를 스토어에 적용
    - 스토어를 생성하는 과정에서 적용한다.
    - redux devtools를 사용중이라면 아래와 같이 `composeWithDevTools`의 인자로 준다.

  ```react
  (...)
  import { applyMiddleware, createStore } from "redux";
  import rootReducer from "./modules";
  import { composeWithDevTools } from "redux-devtools-extension";
  import loggerMiddleware from "./lib/loggerMiddleware";
  
  const store = createStore(
    rootReducer,
    composeWithDevTools(applyMiddleware(loggerMiddleware))
  );
  
  ReactDOM.render(...);
  
  reportWebVitals();
  ```



- redux-logger 사용하기

  - 오픈 소스 커뮤니티에 이미 올라와 있는 redux-logger 미들웨어를 설치하고 사용해본다.
- 위에서 직접 작성한 `loggerMiddleware`보다 다양한 정보를 보기 쉽게 보여 준다.
  - 설치

  ```bash
  $ yarn add redux-logger
  ```

  - 적용
  - 이제 +1,-1 버튼을 누를 때 마다 콘솔 창에 로그가 뜬다.
  
  ```react
  (...)
  import { applyMiddleware, createStore } from "redux";
  import rootReducer from "./modules";
  import { composeWithDevTools } from "redux-devtools-extension";
  import { createLogger } from "redux-logger";
  
  const logger = createLogger();
  const store = createStore(
    rootReducer,
    composeWithDevTools(applyMiddleware(logger))
  );
  
  ReactDOM.render(...);
  
  reportWebVitals();
  ```



## 비동기 작업을 처리하는 미들웨어 사용

- 비동기 작업을 처리할 때 도움을 주는 대표적인 미들웨어들.

  - redux-thunk

    - 비동기 작업을 처리할 때 가장 많이 사용하는 미들웨어.
    - 리덕스의 창시자인 댄 아브라모프가 제작.

    - 객체가 아닌 함수 형태의 액션을 디스패치 할 수 있게 해준다.

  - redux-saga

    - 두 번째로 많이 사용되는 비동기 작업 관련 미들웨어 라이브러리.
    - 특정 액션이 디스패치되었을 때 정해진 로직에 따라 다른 액션을 디스패치시키는 규칙을 작성하여 비동기 작업을 처리할 수 있게 해준다.

  - 비동기 작업을 처리할 때 미들웨어를 사용하는 이유는 좀 더 편하게 처리하기 위해서다.
    - 오히려 불편하다고 느낀다면 사용하지 않는 편이 좋을 수도 있다.



### redux-thunk

- Thunk란

  - Thunk는 특정 작업을 나중에 할 수 있도록 미루기 위해 함수 형태로 감싼 것을 의미한다.
  - 액션 객체 대신 액션 생성 함수를 반환하는 함수를 작성할 수 있게 해준다.
      - 일반 액션 생성함수는 액션 객체를 생성하는 작업만 한다.
      - 액션 객체는 함수가 아니므로 특정 액션이 몇 초 뒤에 실행되게 하거나, 현재 상태에 따라 아예 액션이 무시되게 하는 등의 작업이 불가능하다.
  - redux-thunk는 액션 객체를 생성하는 것이 아닌 함수를 생성하는 액션 생성 함수를 작성할 수 있게 해준다.
  
  ```javascript
  const INCREMENT_COUNTER = 'INCREMENT_COUNTER';
  
  // increment는 단순히 액션 객체를 반환한다.
  function increment() {
    return {
      type: INCREMENT_COUNTER
    };
  }
  
  // 액션 객체가 단순히 액션 생성 객체가 아닌 몇 초 뒤 액션 객체를 반환하는 액션 생성 함수를 반환
  function incrementAsync() {
    return dispatch => {
      setTimeout(() => {
        // 1 초뒤 dispatch 한다.
        dispatch(increment());
      }, 1000);
    };
  }
  ```
  
  - redux-thunk 라이브러리를 사용하면 thunk 함수를 만들어서 디스패치할 수 있다.
      - 그럼 redux-thunk 미들웨어가 그 함수를 전달받아 store의 `dispatch`와 `getState`를 파라미터로 넣어서 호출해 준다.
  
  ```react
  const sampleThunk = () => (dispatch,getState) => {
      // getState로 현재 상태를 참조할 수도 있고,
      // dispatch로 새 액션을 디스패치 할 수도 있다.
  } 
  ```



- redux-thunk 적용하기

  - 설치

  ```bash
  $ yarn add redux-thunk
  ```

  - 적용

  ```react
  (...)
  import { applyMiddleware, createStore } from "redux";
  import rootReducer from "./modules";
  import { composeWithDevTools } from "redux-devtools-extension";
  import { createLogger } from "redux-logger";
  import ReduxThunk from "redux-thunk";
  
  const logger = createLogger();
  const store = createStore(
    rootReducer,
    composeWithDevTools(applyMiddleware(logger, ReduxThunk))
  );
  
  ReactDOM.render(
    <React.StrictMode>
      <Provider store={store}>
        <App />
      </Provider>
    </React.StrictMode>,
    document.getElementById("root")
  );
  
  reportWebVitals();
  ```



- Thunk 생성 함수 만들기

  - redux-thunk는 액션 생성 함수에서 일반 액션 객체를 반환하는 대신에 액션 객체를 생성하는 함수를 반환한다.
  - 함수를 반환하고 그 함수에 `dispatch`를 인자로 받는다.

  ```react
  import { createAction, handleActions } from "redux-actions";
  
  const INCREASE = "counter/INCREASE";
  const DECREASE = "counter/DECREASE";
  
  export const increase = createAction(INCREASE);
  export const decrease = createAction(DECREASE);
  
  const initialState = 0;
  
  // 새로운 액션 생성 함수(thunk 함수)
  export const increaseAsync = () => (dispatch) => {
    setTimeout(() => {
      dispatch(increase()); // increase의 결과로 액션 객체가 반환된다.
    }, 1000);
  };
  
  export const decreaseAsnyc = () => (dispatch) => {
    setTimeout(() => {
      dispatch(decrease());
    }, 1000);
  };
  
  const counter = handleActions(
    {
      [INCREASE]: (state) => state + 1,
      [DECREASE]: (state) => state - 1,
    },
    initialState
  );
  
  export default counter;
  ```

  - 액션 생성 함수를 호출하는 부분도 수정

  ```react
  import React from "react";
  import { connect } from "react-redux";
  import Counter from "../components/Counter";
  import { increaseAsync, decreaseAsync } from "../modules/counter";
  
  const CounterContainer = ({ number, increaseAsync, decreaseAsync }) => {
    return (
      <Counter
        number={number}
        onIncrease={increaseAsync}
        onDecrease={decreaseAsync}
      />
    );
  };
  
  export default connect((state) => ({ number: state.counter }), {
    increaseAsync,
    decreaseAsync,
  })(CounterContainer);
  ```

  - 이후 실행해보면 1초 뒤에 실행되는 것을 확인 가능하다.
    - 또한 콘솔 창을 확인해 보면 처음 디스패치 되는 액션은 함수 형태(`(dispatch) => {setTimeout(() => {dispatch(increase())}, 1000)}`)고, 두 번째 액션은 객체 형태(`{type:"counter/INCREASE"}`)인 것을 확인 가능하다.



- 웹 요청 비동기 작업 처리하기

  > https://jsonplaceholder.typicode.com/posts/:id (id는 1~100사이 숫자)
  >
  > https://jsonplaceholder.typicode.com/users (모든 사용자 정보 불러오기)

  - JSONPlaceholder에서 제공되는 가짜 API를 사용
  - axios 설치

  ```bash
  $ yarn add axios
  ```

  - API를 함수화
    - 각 API를 호출하는 함수를 따로 작성하면, 나중에 사용할 때 가독성도 좋고 유지 보수도 쉬워진다.
    - 다른 파일에서 사용할 수 있도록 `export`로 내보낸다.

  ```react
  // src/lib/api.js
  import axios from "axios";
  
  export const getPost = (id) =>
    axios.get(`https://jsonplaceholder.typicode.com/posts/${id}`);
  export const getUsers = () =>
    axios.get("https://jsonplaceholder.typicode.com/users");
  ```

  - 리듀서 생성
    - API를 사용하여 받은 데이터를 관리할 리듀서.

  ```react
  import { handleActions } from "redux-actions";
  import * as api from "../lib/api";
  
  const GET_POST = "sample/GET_POST";
  const GET_POST_SUCCESS = "sample/GET_POST_SUCCESS";
  const GET_POST_FAILURE = "sample/GET_POST_FAILURE";
  
  const GET_USERS = "sample/GET_USERS";
  const GET_USERS_SUCCESS = "sample/GET_USERS_SUCCESS";
  const GET_USERS_FAILURE = "sample/GET_USERS_FAILURE";
  
  // thunk 함수 생성
  export const getPage = (id) => async (dispatch) => {
    dispatch({ type: GET_POST });
    try {
      const response = await api.getPost(id);
      dispatch({
        type: GET_POST_SUCCESS,
        payload: response.data,
      });
    } catch (e) {
      dispatch({
        type: GET_USERS_FAILURE,
        payload: e,
        error: true,
      });
      // error를 던져 나중에 컴포넌트 단에서 조회할 수 있도록 해 준다.
      throw e;
    }
  };
  
  export const getUsers = (id) => async (dispatch) => {
    dispatch({ type: GET_USERS });
    try {
      const response = await api.getUsers();
      dispatch({
        type: GET_USERS_SUCCESS,
        payload: response.data,
      });
    } catch (e) {
      dispatch({
        type: GET_USERS_FAILURE,
        payload: e,
        error: true,
      });
      throw e;
    }
  };
  
  // 초기 상태 선언
  // 요청의 로딩 중 상태는 loading 객체에서 관리
  const initialState = {
    loading: {
      GET_POST: false,
      GET_USERS: false,
    },
    post: null,
    users: null,
  };
  
  const sample = handleActions(
    {
      [GET_POST]: (state) => ({
        ...state,
        loading: {
          ...state.loading,
          GET_POST: true, // 요청 시작
        },
      }),
      [GET_POST_SUCCESS]: (state, action) => ({
        ...state,
        loading: {
          ...state.loading,
          GET_POST: false, // 요청 완료
        },
        post: action.payload,
      }),
      [GET_POST_FAILURE]: (state) => ({
        ...state,
        loading: {
          ...state.loading,
          GET_POST: false, // 요청 완료
        },
      }),
      [GET_USERS]: (state) => ({
        ...state,
        loading: {
          ...state.loading,
          GET_USERS: true, // 요청 시작
        },
      }),
      [GET_USERS_SUCCESS]: (state, action) => ({
        ...state,
        loading: {
          ...state.loading,
          GET_USERS: false, // 요청 완료
        },
        users: action.payload,
      }),
      [GET_USERS_FAILURE]: (state) => ({
        ...state,
        loading: {
          ...state.loading,
          GET_USERS: false, // 요청 완료
        },
      }),
    },
    initialState
  );
  
  export default sample;
  ```

  - 리듀서를 루트 리듀서에 포함시킨다.

  ```react
  import { combineReducers } from "redux";
  import counter from "./counter";
  import sample from "./sample";
  
  const rootReducer = combineReducers({ counter, sample });
  
  export default rootReducer;
  ```

  - 프레젠테이션 컴포넌트를 작성
    - 데이터를 불러와서 렌더링해 줄 때는 유효성 검사를 해 주는 것이 중요하다.

  ```react
  import React from "react";
  
  const Sample = ({ loadingPost, loadingUsers, post, users }) => {
    return (
      <div>
        <section>
          <h1>포스트</h1>
          {loadingPost && "로딩중..."}
          {!loadingPost && post && (
            <div>
              <h3>{post.title}</h3>
              <h3>{post.body}</h3>
            </div>
          )}
        </section>
        <hr />
        <section>
          <h1>사용자 목록</h1>
          {loadingUsers && "로딩중..."}
          {!loadingUsers && users && (
            <ul>
              {users.map((user) => (
                <li key={user.id}>
                  {user.username}({user.email})
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    );
  };
  
  export default Sample;
  ```

  - 컨테이너 컴포넌트 만들기

  ```react
  import React from "react";
  import { connect } from "react-redux";
  import Sample from "../components/Sample";
  import { getPost, getUsers } from "../modules/sample";
  
  const { useEffect } = React;
  const SampleContainer = ({
    getPost,
    getUsers,
    post,
    users,
    loadingPost,
    loadingUsers,
  }) => {
    useEffect(() => {
      getPost(1);
      getUsers(1);
    }, [getPost, getUsers]);
    return (
      <Sample
        post={post}
        users={users}
        loadingPost={loadingPost}
        loadingUsers={loadingUsers}
      />
    );
  };
  
  export default connect(
    // 디스트럭처링을 활용
    ({ sample }) => ({
      post: sample.post,
      users: sample.users,
      loadingPost: sample.loading.GET_POST,
      loadingUsers: sample.loading.GET_USERS,
    }),
    { getPost, getUsers }
  )(SampleContainer);
  ```



- 리팩토링

  - 반복되는 로직을 따로 작성하기
    - API를 요청해야 할 때마다 긴 thunk 함수를 작성하고, 로딩 상태를 리듀서에서 관리하는 작업은 귀찮을 뿐 아니라 코드도 길어지게 만든다.
  - thunk 함수 따로 작성하기

  ```react
  // src/lib/createRequestThunk.js
  export default function createRequestThunk(type, request) {
    // 성공 및 실패 액션 타입을 정의한다.
    const SUCCESS = `${type}_SUCCESS`;
    const FAILURE = `${type}_FAILURE`;
    return (params) => async (dispatch) => {
      dispatch({ type }); // 시작됨
      try {
        const response = await request(params);
        dispatch({
          type: SUCCESS,
          payload: response.data,
        }); // 성공
      } catch (e) {
        dispatch({
          type: FAILURE,
          payload: e,
          error: true,
        }); // 에러 발생
        throw e;
      }
    };
  }
  ```

  - 따로 작성한 thunk 함수 적용하기

  ```react
  import { handleActions } from "redux-actions";
  import createRequestThunk from "../lib/createRequestThunk";
  import * as api from "../lib/api";
  
  const GET_POST = "sample/GET_POST";
  const GET_POST_SUCCESS = "sample/GET_POST_SUCCESS";
  const GET_POST_FAILURE = "sample/GET_POST_FAILURE";
  
  const GET_USERS = "sample/GET_USERS";
  const GET_USERS_SUCCESS = "sample/GET_USERS_SUCCESS";
  const GET_USERS_FAILURE = "sample/GET_USERS_FAILURE";
  
  // thunk 함수 대체
  export const getPost = createRequestThunk(GET_POST, api.getPost);
  export const getUsers = createRequestThunk(GET_USERS, api.getUsers);
  
  const initialState = {
    loading: {
      GET_POST: false,
      GET_USERS: false,
    },
    post: null,
    users: null,
  };
  
  const sample = handleActions(...))
  
  export default sample;
  ```

  - 로딩 상태를 관리하는 작업 개선하기
    - 기존에는 리듀서 내부에서 각 요청에 관련된 액션이 디스패치될 때마다 로딩 상태를 변경해 주었다.
    - 이 작업을 로딩 상태만 관리하는 리덕스 모듈을 따로 생성하여 처리한다.

  ```react
  // src/modules/loading.js
  import { createAction, handleActions } from "redux-actions";
  
  const START_LOADING = "loading/START_LOADING";
  const FINISH_LOADING = "loading/FINISH_LOADING";
  
  // 요청을 위한 액션 타입을 payload로 설정한다.
  // e.g.sample/GET_POST
  export const startLoading = createAction(
    START_LOADING,
    (requestType) => requestType
  );
  
  export const finishLoading = createAction(
    FINISH_LOADING,
    (requestType) => requestType
  );
  
  
  const initialState = {};
  
  /* 포스트를 받아오는 요청이 시작될 때 디스패치할 액션
  {
      type:'loading/START_LOADING',
      payload:'sample/GET_POST'
  }
  위 액션이 디스패치되면 loading 리듀서가 관리하고 있는 상태에서 sample/GET_POST 값을 true로 설정해준다.
  만약 기존 상태에 sample/GET_POST 필드가 존재하지 않으면 새로 값을 설정해준다.
  */
  
  /* 요청이 끝나면 디스패치할 액션
  {
  	tpye:'loading/FINISH_LOADING',
  	payload:'sample/GET_POST'
  }
  */
  
  const loading = handleActions(
    {
      [START_LOADING]: (state, action) => ({
        ...state,
        [action.payload]: true,
      }),
      [FINISH_LOADING]: (state, action) => ({
        ...state,
        [action.payload]: false,
      }),
    },
    initialState
  );
  
  export default loading;
  ```

  - 루트 리듀서에 포함시키기

  ```react
  import { combineReducers } from "redux";
  import counter from "./counter";
  import sample from "./sample";
  import loading from "./loading";
  
  const rootReducer = combineReducers({ counter, sample, loading });
  
  export default rootReducer;
  ```

  - createRequestThunk.js에 적용하기

  ```react
  import { finishLoading, startLoading } from "../modules/loading";
  
  export default function createRequestThunk(type, request) {
    const SUCCESS = `${type}_SUCCESS`;
    const FAILURE = `${type}_FAILURE`;
    return (params) => async (dispatch) => {
      dispatch({ type }); // 시작됨
      dispatch(startLoading(type));
      try {
        const response = await request(params);
        dispatch({
          type: SUCCESS,
          payload: response.data,
        }); // 성공
        dispatch(finishLoading(type));
      } catch (e) {
        dispatch({
          type: FAILURE,
          payload: e,
          error: true,
        }); // 에러 발생
        dispatch(finishLoading(type));
        throw e;
      }
    };
  }
  ```

  - 이제 로딩 상태를 다음과 같이 조회하는 것이 가능해진다.

  ```react
  (...)
  
  export default connect(
    ({ sample, loading }) => ({
      post: sample.post,
      users: sample.users,
      loadingPost: loading['sample/GET_POST'],
      loadingUsers: loading['sample/GET_USERS'],
    }),
    { getPost, getUsers }
  )(SampleContainer);
  ```

  - 리듀서에서 로딩 상태 관리 코드 제거하기

  ```react
  import { handleActions } from "redux-actions";
  import createRequestThunk from "../lib/createRequestThunk";
  import * as api from "../lib/api";
  
  const GET_POST = "sample/GET_POST";
  const GET_POST_SUCCESS = "sample/GET_POST_SUCCESS";
  
  const GET_USERS = "sample/GET_USERS";
  const GET_USERS_SUCCESS = "sample/GET_USERS_SUCCESS";
  
  // thunk 함수 대체
  export const getPost = createRequestThunk(GET_POST, api.getPost);
  export const getUsers = createRequestThunk(GET_USERS, api.getUsers);
  
  const initialState = {
    post: null,
    users: null,
  };
  
  const sample = handleActions(
    {
      [GET_POST_SUCCESS]: (state, action) => ({
        ...state,
        loading: {
          ...state.loading,
          GET_POST: false, // 요청 완료
        },
        post: action.payload,
      }),
      [GET_USERS_SUCCESS]: (state, action) => ({
        ...state,
        loading: {
          ...state.loading,
          GET_USERS: false, // 요청 완료
        },
        users: action.payload,
      }),
    },
    initialState
  );
  
  export default sample;
  ```



### redux-saga

- redux-saga
  - redux-thunk는 함수 형태의 액션을 디스패치하여 미들웨어에서 해당 함수에 스토어의 `dispatch`와 `getState`를 파라미터로 넣어서 사용하는 원리이다.
  - 대부분의 경우에는 redux-thunk로 구현이 가능하지만 redux-saga는 아래와 같이 까다로운 상황에서 유용하다.
    - 기존 요청을 취소 처리해야 할 때(불필요한 중복 요청 방지)
    - 특정 액션이 발생했을 때 다른 액션을 발생시키거나, API 요청 등 리덕스와 관계 없는 코드를 실행할 때
    - 웹소켓을 사용할 때
    - API 요청 실패 시 재요청을 해야 할 때
  - ES6의 제너레이터에 대한 이해가 필요하다.
    - 제네레이터 함수 문법을 기반으로 비동기 작업을 관리한다.
    - 아래 코드와 비슷한 원리로 동작한다.

  ```react
  function* watchGenerator() {
    console.log("모니터 중...");
    let prevAction = null;
    while (true) {
      const action = yield;
      console.log("이전 액선: ", prevAction);
      prevAction = action;
      if (action.type == "HELLO") {
        console.log("안녕하세요!");
      }
    }
  }
  
  const watch = watchGenerator();
  
  watch.next(); // 모니터 중...
  watch.next({ type: "TEST" }); // 이전 액선:  null
  watch.next({ type: "HELLO" });
  // 이전 액선:  { type: 'TEST' }
  // 안녕하세요!
  ```



- 비동기 카운터 만들기

  - redux-saga 설치

  ```bash
  $ yarn add redux-saga
  ```

  - `counter` 리덕스 모듈에서 기존 thunk 함수를 제거하고 새로운 액션 타입을 선언
  - 제네레이터 함수도 만든다.
    - 이 제네레이터 함수를 사가라 부른다.
  
  ```react
  import { createAction, handleActions } from "redux-actions";
  import { delay, put, takeEvery, takeLatest } from "redux-saga/effects";
  
  const INCREASE = "counter/INCREASE";
  const DECREASE = "counter/DECREASE";
  
  // 새로운 액션 타입을 선언
  const INCREASE_ASYNC = "counter/INCREASE_ASYNC";
  const DECREASE_ASYNC = "counter/DECREASE_ASYNC";
  
  export const increase = createAction(INCREASE);
  export const decrease = createAction(DECREASE);
  
  // 어떤 인자를 받아도 payload에 들어가지 않도록 undefined를 반환하는 함수를 두 번째 파라미터로 넣는다.
  export const increaseAsync = createAction(INCREASE_ASYNC, () => undefined);
  export const decreaseAsync = createAction(DECREASE_ASYNC, () => undefined);
  
  // 사가
  function* increaseSaga() {
    yield delay(1000); // 일 초를 기다리고,
    yield put(increase()); // 특정 액션을 디스패치한다.
  }
  
  function* decreaseSaga() {
    yield delay(1000);
    yield put(decrease());
  }
  
  export function* counterSaga() {
    // takeEvery는 들어오는 모든 액션에 대해 특정 작업을 처리해 준다.
    // INCREASE_ASYNC 액션이 생성되면 increaseSaga 작업을 처리한다.
    yield takeEvery(INCREASE_ASYNC, increaseSaga);
    // takeLatest는 기존에 진행 중이던 작업이 있다면 취소 처리하고, 가장 마지막으로 싱행된 작업만 수행한다.
    yield takeLatest(DECREASE_ASYNC, decreaseSaga);
}
  
  (...)
  ```

  - 루트 리듀서를 만드는 것처럼 루트 사가를 만들어야 한다.
    - 추후 다른 리듀서에서도 사가를 만들어 등록할 것이기에 루트 사가를 만들어야 한다.
    - `all` 함수는 여러 사가를 합쳐주는 역할을 한다.
  
  ```react
  import { combineReducers } from "redux";
  import counter, { counterSaga } from "./counter";
  import sample from "./sample";
  import loading from "./loading";
  import { all } from "redux-saga/effects";
  
  const rootReducer = combineReducers({ counter, sample, loading });
  export function* rootSaga() {
    yield all([counterSaga()]);
}
  
  export default rootReducer;
  ```
  
  - 스토어에 redux-saga 미들웨어를 적용한다.
  
  ```react
  (...)
  import rootReducer, { rootSaga } from "./modules";
  import createSagaMiddleware from "redux-saga";
  
  const logger = createLogger();
  const sagaMiddleware = createSagaMiddleware();
  const store = createStore(
    rootReducer,
    composeWithDevTools(applyMiddleware(logger, ReduxThunk, sagaMiddleware))
  );
  sagaMiddleware.run(rootSaga);
  (...)
  ```
    - 잘 적용 되었는지 확인하기
      - App 컴포넌트에 Counter 컴포넌트를 랜더링 한 후 아래와 같이 실행한다.
      - `+1` 버튼을 빠르게 두 번 클릭하고 +2가 되는지 확인한다.
      - `-1`버튼을 빠르게 두 번 클릭하고 -1이 한 번만 동작하는지 확인한다.
      - `increaseSaga`는 `takeEvery`를 사용하여 등록했으므로 디스패치 되는 모든 `INCREASE_ASYNC` 액션에 대해 `INCREASE` 액션을 발생시킨다.
      - `decreaseSaga`는 `takeLatest`를 사용하여 등록했으므로 여러 액션이 중첩되어 디스패치되었을 때는 기존의 것들은 무시하고 가장 마지막 액션만 처리한다.



- API 요청 상태 관리하기

  - 기존에 thunk로 관리하던 액션 생성 함수를 없애고 사가를 사용하여 처리
    - API를 호출해야 하는 상황에는 사가 내부에서 직접 호출하지 않고 `call` 함수를 사용한다.

  ```react
  import { createAction, handleActions } from "redux-actions";
  import * as api from "../lib/api";
  import { call, put, takeLatest } from "redux-saga/effects";
  import { startLoading, finishLoading } from "./loading";
  
  const GET_POST = "sample/GET_POST";
  const GET_POST_SUCCESS = "sample/GET_POST_SUCCESS";
  const GET_POST_FAILURE = "sample/GET_POST_FAILURE";
  
  const GET_USERS = "sample/GET_USERS";
  const GET_USERS_SUCCESS = "sample/GET_USERS_SUCCESS";
  const GET_USERS_FAILURE = "sample/GET_USERS_FAILURE";
  
  export const getPost = createAction(GET_POST, (id) => id);
  export const getUsers = createAction(GET_USERS);
  
  function* getPostSaga(action) {
    yield put(startLoading(GET_POST)); // 로딩 시작
    // 파라미터로 action을 받아오면 액션의 정보를 조회할 수 있다.
    try {
      // call을 사용하면 Promise를 반환하는 함수를 호출하고, 기다릴 수 있다.
      // 첫 번째 파라미터는 함수, 나머지 파라미터는 해당 함수에 넣을 인수이다.
      const post = yield call(api.getPost, action.payload);
      yield put({
        type: GET_POST_SUCCESS,
        payload: post.data,
      });
    } catch (e) {
      yield put({
        type: GET_POST_FAILURE,
        payload: e,
        error: true,
      });
    }
    yield put(finishLoading(GET_POST)); // 로딩 완료
  }
  
  function* getUsersSaga() {
    yield put(startLoading(GET_USERS));
    try {
      const users = yield call(api.getUsers);
      yield put({
        type: GET_USERS_SUCCESS,
        payload: users.data,
      });
    } catch (e) {
      yield put({
        type: GET_USERS_FAILURE,
        payload: e,
        error: true,
      });
    }
    yield put(finishLoading(GET_USERS));
  }
  
  export function* sampleSaga() {
    yield takeLatest(GET_POST, getPostSaga);
    yield takeLatest(GET_USERS, getUsersSaga);
  }
  
  (...)
  ```

  - 루트 사가에 등록하기

  ```react
  import { combineReducers } from "redux";
  import counter, { counterSaga } from "./counter";
  import { sampleSaga } from "./sample";
  import sample from "./sample";
  import loading from "./loading";
  import { all } from "redux-saga/effects";
  
  const rootReducer = combineReducers({ counter, sample, loading });
  export function* rootSaga() {
    yield all([counterSaga(), sampleSaga()]);
  }
  
  export default rootReducer;
  ```

  - 정상적으로 받아오는지 확인한다.



- 리팩토링

  - `src/lib/createRequestSaga.js`만들기

  ```react
  import { call, put } from "redux-saga/effects";
  import { finishLoading, startLoading } from "../modules/loading";
  
  export default function createRequestSaga(type, request) {
    const SUCCESS = `${type}_SUCCESS`;
    const FAILURE = `${type}_FAILURE`;
    return function* (action) {
      yield put(startLoading(type));
      try {
        const response = yield call(request, action, payload);
        yield put({
          type: SUCCESS,
          payload: response.data,
        });
      } catch (e) {
        yield put({
          type: FAILURE,
          payload: e,
          error: true,
        });
      }
      yield put(finishLoading(type));
    };
  }
  ```

  - 기존의 사가를 보다 짧은 코드로 구현 가능해진다.

  ```react
  import { createAction, handleActions } from "redux-actions";
  import * as api from "../lib/api";
  import { takeLatest } from "redux-saga/effects";
  import createRequestSaga from "../lib/createRequestSaga";
  
  const GET_POST = "sample/GET_POST";
  const GET_POST_SUCCESS = "sample/GET_POST_SUCCESS";
  
  const GET_USERS = "sample/GET_USERS";
  const GET_USERS_SUCCESS = "sample/GET_USERS_SUCCESS";
  
  export const getPost = createAction(GET_POST, (id) => id);
  export const getUsers = createAction(GET_USERS);
  
  const getPostSaga = createRequestSaga(GET_POST, api.getPost);
  const getUsersSaga = createRequestSaga(GET_USERS, api.getUsers);
  
  export function* sampleSaga() {
    yield takeLatest(GET_POST, getPostSaga);
    yield takeLatest(GET_USERS, getUsersSaga);
  }
  
  (...)
  ```



- 알아두면 유용한 기능들

  - 사가 내부에서 현재 상태를 조회하는 방법
    - 사가 내부에서 현재 상태를 참조해야 하는 상황에서는 `select` 함수를 사용한다.

  ```react
  (...)
  
  function* increaseSaga() {
    yield delay(1000);
    yield put(increase());
    const number = yield select((state) => state.counter);
    console.log(`현재 값은 ${number}입니다.`);
  }
  
  (...)
  ```

  - 사가 실행 주기를 제한하는 방법
    - `takeEvery` 대신 `throttle` 함수를 사용
    - 첫 번째 인자로 시간을 받는다.

  ```react
  (...)
  export function* counterSaga() {
    yield throttle(3000, INCREASE_ASYNC, increaseSaga); // 3초에 한번만 호출된다.
    yield takeLatest(DECREASE_ASYNC, decreaseSaga);
  }
  ```

  - 외에도 다양한 기능이 있다.

  > https://redux-saga.js.org/ 참고











