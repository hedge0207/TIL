# 리덕스 미들웨어를 통한 비동기 작업 관리

- 미들웨어란
  - 리듀서가 액션을 처리하기 전에 미들웨어가 할 수 있는 작업은 여러 가지가 있다.
    - 전달 받은 액션을 단순히 콘솔에 기록하거나
    - 전달 받은 액션 정보를 기반으로 액션을 아예 취소하거나
    - 다른 종류의 액션을 추가로 디스패치 할 수도 있다.
  - 미들웨어는 액션과 리듀서의 중간자 역할을 한다.
    - 미들웨어는 액션을 디스패치했을 때 리듀서에서 이를 처리하기에 앞서 사전에 지정된 작업들을 처리한다.
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
    - 미들웨어가 어떻게 작동하는지 이해하려면 직접 만들어 보는 것이 가장 효과적이다.
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
    - `next` 파라미터는 함수이며, `store.dispatch`와 비슷한 역할을 한다.
    - 그러나 `store.dispatch`와 큰 차이가 있는데, `next(action)`을 호출하면 그 다음 처리해야 할 미들웨어에게 액션을 넘겨주고, 만약 그 다음에 미들웨어가 없다면 리듀서에게 액션을 넘겨준다는 것이다.
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

  - 설치

  ```bash
  $ yarn add redux-logger
  ```

  - 적용

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



### redux-thunk

- Thunk란

  - Thunk는 특정 작업을 나중에 할 수 있도록 미루기 위해 함수 형태로 감싼 것을 의미한다.

  ```javascript
  const addOne = x => x+1;
  
  function addOneThunk(x){
      const thunk = () => addOne(x);
      return thunk
  }
  
  const fn = addOneThunk(1);
  setTimeout(()=>{
      const value=fn();	// fn()이 실행되는 시점에 연산
      console.log(value);
  },1000);
  ```

  - redux-thunk 라이브러리를 사용하면 thunk  함수를 만들어서 디스패치할 수 있다.
    - 그럼 리덕스 미들웨어가 그 함수를 전달받아 store의 `dispatch`와 `getState`를 파라미터로 넣어서 호출해 준다.



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

  - redux-thunk는 액션 생성 함수에서 일반 액션 객체를 반환하는 대신에 함수를 반환한다.
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
    - 또한 콘솔 창을 확인해 보면 처음 디스패치 되는 액션은 함수 형태고, 두 번째 액션은 객체 형태인 것을 확인 가능하다.



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

  







