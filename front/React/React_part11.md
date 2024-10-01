# 코드 스플리팅

- 빌드

  - 리액트 프로젝트를 완성하여 사용자에게 제공할 때는 빌드 작업을 거쳐 배포해야 한다.

    - 빌드 작업을 통해 프로젝트에서 사용되는 JS 파일 안에서 불필요한 주석, 경고 메세지, 공백 등을 제거하여 파일 크기를 최소화한다.
    - 브라우저에서 JSX 문법이나 다른 최신 JS 문법이 원활하게 실행될 수 있도록 코드의 트랜스파일 작업도 할 수 있다.
    - 만약 프로젝트 내에 이미지와 같은 정적 파일이 있다면 해당 파일을 위한 경로도 설정된다.

  - 빌드 작업은 webpack이 담당한다.

    - 웹팩에서 별도의 빌드 설정을 하지 않으면 프로젝트에서 사용중인 모든 JS파일이 하나의 파일로 합쳐지고, 모든 CSS 파일이 하나의 파일로 합쳐진다.

  - CRA(create react app)로 프로젝트를 빌드할 경우 최소 두 개 이상의 JS파일이 생성된다.

    - CRA의 기본 웹팩 설정에는 **SplitChunks**라는 기능이 적용되어 node_modules에서 불러온 파일, 일정 크기 이상의 파일, 여러 파일 간에 공유된 파일을 자동으로 따로 분리시켜 캐싱의 효과를 제대로 누릴 수 있게 해준다.

  - 빌드하기

    ```bash
    $ yarn build
    ```

  - 빌드를 완료하면 build 디렉터리가 생성되는데 그 내부의 static 디렉터리를 보면 JS파일 여러개가 만들어 진 것을 확인 가능하다.

    - 파일 이름에 `58cd9e2f`같은 해시 값이 포함되어 있다.
    - 해시 값은 빌드하는 과정에서 해당 파일의 내용에 따라 생성되며, 이를 통해 브라우저가 새로 파일을 받아야 할지 받지 말아야 할지를 알 수 있다.
    - 2로 시작하는 파일에는 React, ReactDOM 등 node_modules에서 불러온 라이브러리 관련 코드가 있고, main으로 시작하는 파일에는 직접 프로젝트에 작성하는 App 같은 컴포넌트에 대한 코드가 들어 있다.
    - **SplitChunks**라는 웹팩 기능을 통해, 자주 바뀌지 않는 코드들이 2로 시작하는 파일에 들어 있기 때문에 캐싱의 이점을 더 오래 누릴 수 있다.
    - 실제로 컴포넌트의 코드를 변경하고 다시 빌드하면 2로 시작하는 파일명은 변경되지 않고, 컴포넌트 관련 코드가 들어 있던 main으로 시작하는 파일의 이름이 바뀐 것을 확인 가능하다.



- 코드 스플리팅
  - 위에서 설명한것 처럼 파일을 분리하는 작업을 코드 스플리팅이라 한다.
  - 프로젝트에 기본 탑재된 **SplitChunks** 기능을 통한 코드 스플리팅은 단순히 효율적인 캐싱 효과만 있을 뿐이다.
    - 예를 들어 A, B, C 컴포넌트가 있을 때, A페이지를 방문했다면, B, C 페이지에서 사용하는 컴포넌트 정보는 필요하지 않다.
    - 하지만 리액트 프로젝트에 별도로 설정하지 않으면 A, B, C 컴포넌트에 대한 코드가 모두 한 파일(main으로 시작하는 파일)에 저장되게 된다.
    - 애플리케이션의 규모가 커지면, 지금 당장 필요하지 않은 컴포넌트 정보도 모두 불러오면서 파일 크기가 매우 커진다.
    - 따라서 로딩이 오래 걸리게 되고 사용자 경험도 안좋아지고 트래픽도 많이 나오게 된다.
  - 이러한 문제점을 해결해 주는 것이 **코드 비동기 로딩**이다.
    - 이 또한 코드 스플리팅 방법 중 하나이다.
    - 코드 비동기 로딩을 통해 JS 함수, 객체 혹은 컴포넌트를 처음에는 불러오지 않고  필요한 시점에 불러와서 사용할 수 있다.



##  JS 함수 비동기 로딩

- 일반 JS 함수를 스플리팅하지 않고 빌드하기 

  - 함수를 생성

  ```javascript
  export default function notify() {
    alert("안녕하세요!");
  }
  ```

  - 함수를 실행하기

  ```react
  import logo from "./logo.svg";
  import "./App.css";
  import notify from "./notify";
  
  function App() {
    const onClick = () => {
      notify();
    };
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <button onClick={onClick}>Hello React!</button>
        </header>
      </div>
    );
  }
  
  export default App;
  ```

  - 빌드하기
    - 빌드하면 `notify` 코드가 main 파일에 들어가게 된다.



- 일반 JS 함수를 스플리팅하여 빌드하기

  - `import`를 함수로 사용하면 Promise를 반환한다.
    - `import`를 함수로 사용하는 문법은 비록 표준 자바스크립트가 아니지만 stage-3 단계에 있는 **dynamic import**라는 문법이다.
    - 현재 웹팩에서 지원하고 있으므로 별도의 설정 없이 프로젝트에 바로 사용 가능하다.
    - 이 함수를 통해 모듈을 불러올 때 모듈에서 `default`로 내보낸 것은 `result.default`를 참조해야 사용할 수 있다.
  - App 컴포넌트를 아래와 같이 수정한다.
    - 클릭 이벤트가 발생해야 import로 함수를 불러와서 사용한다.
    - 따라서 초기 렌더링에서 불러오지 않으므로 초기 렌더링 성능이 향상된다.

  ```react
  import logo from "./logo.svg";
  import "./App.css";
  
  function App() {
    const onClick = () => {
      // import를 함수로 사용
      import("./notify").then((result) => result.default());
    };
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <button onClick={onClick}>Hello React!</button>
        </header>
      </div>
    );
  }
  
  export default App;
  ```

  - 개발자 도구의 Network 탭을 연 다음 버튼을 클릭해야 `notify`와 관련된 코드가 들어있는 JS 파일을 불러오는 것을 확인 가능하다.
    - 해당 파일의 내용을 확인해보면 `notify`와 관련된 코드가 들어있다.
  - 빌드
    - 이후 빌드하면 3으로 시작하는 파일에 `notify` 관련 코드가 들어간다.



## 컴포넌트 코드 스플리팅

- 코드 스플리팅
  - 지금 당장 필요한 코드가 아니라면 따로 분리시켜서, 나중에 필요할때 불러와서 사용 하는것. 이를 통하여, 페이지의 렌더링 속도 개선을 기대할 수 있다.
  - 코드 스플리팅을 위해 내장된 기능
    - React.lazy: 유틸 함수
    - Suspense: 컴포넌트



- state를 사용한 코드 스플리팅

  - React.lazy를 사용하지 않고 컴포넌트의 코드를 스플리팅 하는 방법.
    - 클래스형 컴포넌트에서만 가능하다.
  - 코드 스플리팅을 할 컴포넌트 작성

  ```react
  import React from "react";
  
  const SplitMe = () => {
    return <div>SplitMe</div>;
  };
  
  export default SplitMe;
  ```

  - App 컴포넌트를 클래스형으로 전환
    - `handleClick` 메서드를 만들고 내부에서 `SplitMe` 컴포넌트를 불러와 state에 넣는다.
    - `render` 함수에서 state 안에 있는 `SplitMe`가 유효하다면 `SplitMe` 컴포넌트를 렌더링 한다.
    - 클릭 이벤트가 발생해야 import로 함수를 불러와서 사용한다.
    - 따라서 초기 렌더링에서 불러오지 않으므로 초기 렌더링 성능이 향상된다.

  ```react
  import React, { Component } from "react";
  import logo from "./logo.svg";
  import "./App.css";
  
  class App extends Component {
    state = {
      SplitMe: null,
    };
    handleClick = async () => {
      const loadModule = await import("./SplitMe");
      this.setState({
        SplitMe: loadModule.default,
      });
    };
    render() {
      const { SplitMe } = this.state;
      return (
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <p onClick={this.handleClick}>Hello React!</p>
            {SplitMe && <SplitMe />}
          </header>
        </div>
      );
    }
  }
  
  export default App;
  ```

  - 개발자 도구의 Network 탭을 열고 p태그를 클릭하면 JS 파일을 불러오는 것을 확인 가능하다.



- React.lazy, Suspense 사용하기

  - state를 따로 선언하지 않아도 간편하게 컴포넌트 코드 스플리팅을 할 수 있다.
  - `React.lazy`는 컴포넌트 렌더링을 하는 시점에서 비동기적으로 로딩할 수 있게 해 주는 유틸 함수다.

  ```react
  const SplitMe = React.lazy(()=>import('./SplitMe'))
  ```

  - Suspense는 리액트 내장 컴포넌트로서 코드 스플리팅된 컴포넌트를 로딩하도록 발동시킬 수 있고, 로딩이 끝나지 않았을 때 보여 줄 UI를 설정할 수 있다.
    - `fallback`이라는 props를 통해 로딩 중에 보여 줄 JSX를 지정할 수 있다.

  ```react
  import React, {Suspense} from 'react'
  
  (...)
  <Suspense fallback={<div>loading...</div>}
    <SplitMe />
  </Suspense>
  ```

  - 적용하기

  ```react
  import React, { useState, Suspense } from "react";
  import logo from "./logo.svg";
  import "./App.css";
  const SplitMe = React.lazy(() => import("./SplitMe"));
  
  const App = () => {
    const [visible, setVisible] = useState(false);
    const onClick = () => {
      setVisible(true);
    };
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p onClick={onClick}>Hello React</p>
          <Suspense fallback={<div>loading...</div>}>
            {visible && <SplitMe />}
          </Suspense>
        </header>
      </div>
    );
  };
  
  export default App;
  ```

  - Network 탭에서 Online을 클릭하여 Slow 3G를 선택하고 p 태그를 누르면 로딩 문구가 나타난다.



- Loadable Components를 통한 코드 스플리팅

  - Loadable Components
    - 코드 스플리팅을 편하게 해주는 서드파티 라이브러리.
    - 이 라이브러리의 이점은 **서버 사이드 렌더링**을 지원한다는 것이다(React.lazy, Suspense는 지원하지 않는다).
    - 또한 렌더링하기 전에 필요할 때 스플리팅된 파일을 미리 불러올 수 있는 기능도 있다.
  - **서버 사이드 렌더링**
    - 웹 서비스의 초기 로딩 속도 개선, 캐싱 및 검색 엔진 최적화를 가능하게 해 주는 기술.
    - 서버 사이드 렌더링을 사용하면 웹 서비스의 초기 렌더링을 사용자의 브라우저가 아닌 서버에서 처리한다.
    - 사용자는 서버에 렌더링한 html 결과물을 받아 와서 그대로 사용하기에 초기 로딩 속도도 개선되고, 검색 엔진에서 크롤링할 때도 문제 없다.
    - 지금은 서버 사이드 렌더링 없이 Loadable Components의 기본적인 사용법만 알아볼 것이다.
  - 설치

  ```bash
  $ yarn add @loadable/component
  ```

  - 적용하기
    - 두 번째 인자로 로딩 중에 보여줄 UI를 넘긴다.

  ```react
  import React, { useState, Suspense } from "react";
  import logo from "./logo.svg";
  import "./App.css";
  import loadable from "@loadable/component";
  const SplitMe = loadable(() => import("./SplitMe"), {
    fallback: <div>loading...</div>,
  });
  
  const App = () => {
    const [visible, setVisible] = useState(false);
    const onClick = () => {
      setVisible(true);
    };
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p onClick={onClick}>Hello React</p>
          {visible && <SplitMe />}
        </header>
      </div>
    );
  };
  
  export default App;
  ```

  - 컴포넌트를 미리 불러오는(preload) 방법	
    - 마우스를 p 태그에 올리기만 해도 로딩이 시작된다.
    - 클릭했을 때 렌더링 된다.
    - 개발자도구를 열고, 커서를 올리는 시점에 파일이 불러와 지는지 확인.
    - 이런 기능을 구현하면 사용자에게 더 좋은 경험을 제공할 수 있다.

  ```react
  import React, { useState, Suspense } from "react";
  import logo from "./logo.svg";
  import "./App.css";
  import loadable from "@loadable/component";
  const SplitMe = loadable(() => import("./SplitMe"), {
    fallback: <div>loading...</div>,
  });
  
  const App = () => {
    const [visible, setVisible] = useState(false);
    const onClick = () => {
      setVisible(true);
    };
    const onMouseOver = () => {
      SplitMe.preload();
    };
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p onClick={onClick} onMouseOver={onMouseOver}>
            Hello React
          </p>
          {visible && <SplitMe />}
        </header>
      </div>
    );
  };
  
  export default App;
  ```

  - Loadable Components는 미리 불러오는 기능 외에도 타임아웃, 로딩 UI 딜레이, 서버 사이드 렌더링 호환 등 다양한 기능을 제공한다.

  > https://loadable-components.com/docs/getting-started/



# 서버 사이드 렌더링 Part 1

- 서버 사이드 렌더링
  - UI를 서버에서 렌더링하는 것을 의미한다.
    - 이전까지 만들었던 리액트 프로젝트들은 기본적으로 클라이언트 사이드 렌더링을 한다.
    - 클라이언트 사이드 렌더링은 UI 렌더링을 브라우저에서 모두 처리하는 것이다.
    - 즉 JS를 실행해야 우리가 만든 화면이 사용자에게 보이게 된다.
  - 프로젝트를 실행하고 개발자 도구의 Network 탭에서 localhost를 클릭(안 뜰 경우 새로고침) 후 Response를 보면 root 아이디를 가진 div 태그가 비어 있는 것을 확인할 수 있다.
    - 즉 이 페이지는 처음에 빈 페이지라는 뜻이다.
    - 이후에 JS가 실행되고 리액트 컴포넌트가 렌더링되면서 우리에게 보이는 것이다.
    - 서버 사이드 렌더링을 구현하면 사용자가 웹 서비스에 방문했을 때 서버 쪽에서 초기 렌더링을 대신 해준다.
    - 그리고 사용자가 html을 전달받을 때 그 내부에 렌더링된 결과물이 보인다.



- 서버 사이드 렌더링의 장점
  - 검색 엔진 최적화
    - 구글, 네이버 등의 검색 엔진이 우리가 만든 웹 애플리케이션의 페이지를 원활하게 수집할 수 있다.
    - 리액트로 만든 SPA는 검색 엔진 크롤러 봇처럼 JS가 실행되지 않는 환경에서 페이지가 제대로 나타나지 않는다. 
    - 구글 검색 엔진은 다른 검색 엔진과 달리 검색 엔진에서 JS를 실행하는 기능이 탑재되어 있으므로 제대로 페이지를 크롤링해 갈 때도 있지만, 모든 페이지에 대해 JS를 실행해 주지는 않는다.
    - 따라서 서버에서 클라이언트 대신 렌더링을 해 주면 검색엔진이 페이지의 내용을 제대로 수집해 갈 수 있다.
    - 그러므로 웹 서비스의 검색 엔진 최적화를 위해서라면 서버 사이드 렌더링을 구현하는 것이 좋다.
  - 초기 렌더링 성능 개선
    - 자바스크립트가 로딩되고 실행될 때까지 사용자는 비어있는 페이지를 보며 대기해야 한다.
    - 여기에 API까지 호출해야 한다면 사용자의 대기 시간이 더더욱 길어진다.
    - 서버 사이드 렌더링을 구현한 웹 페이지라면 JS 파일 다운로드가 완료되지 않은 시점에서도 HTML상에서 사용자가 볼 수 있는 콘텐츠가 있기 때문에 대기 시간이 최소화되고, 사용자 경험도 향상된다.



- 서버 사이드 렌더링의 단점
  - 서버 리소스 사용
    - 결국 브라우저가 해야 할 일을 서버가 대신 처리하는 것이므로 서버 리소스가 사용된다는 단점이 있다.
    - 갑자기 수많은 사용자가 동시에 접속하면 서버에 과부하가 발생할 수 있다.
    - 따라서 사용자가 많은 서비스라면 캐싱과 로드 밸런싱을 통해 성능을 최적화해 주어야 한다.
  - 개발 난이도 상승
    - 프로젝트의 구조가 복잡해진다.
    - 데이터 미리 불러오기, 코드 스플리팅과의 호환 등 고려해야 할 사항이 더 많아진다.



- 서버 사이드 렌더링과 코드 스플리팅 충돌
  - 서버 사이드 렌더링과 코드 스플리팅을 함께 적용하면 작업이 꽤 까다롭다.
  - 별도의 호환 작업 없이 두 기술을 함께 적용하면, 다음과 같은 흐름으로 작동하면서 페이지가 나타났다 없어졌다 다시 나타나게 된다.
    - 서버 사이드 렌더링된 결과물이 브라우저에 나타남.
    - JS 파일 로딩 시작.
    - JS가 실행되면서 아직 불러오지 않은 컴포넌트를 null로 렌더링함.
    - 페이지에서 코드 스플리팅된 컴포넌트들이 사라짐(페이지 일부 혹은 전부가 사라짐).
    - 코드 스플리팅된 컴포넌트들이 로딩된 이후 제대로 나타남
  - 이러한 이슈를 해결하여면 라우트 경로마다 코드 스플리팅된 파일 중에서 필요한 모든 파일을 브라우저에서 렌더링하기 전에 미리 불러와야 한다.
    - Loadable Components 라이브러리에서 제공하는 기능을 사용하여 서버 사이드 렌더링 후 필요한 파일의 경로를 추출하여 렌더링 결과에 스크립트/스타일 태그를 삽입해 주는 방식으로 해결 할 수 있다.
    - 위 해결법이 유일한 해결법은 아니다.



## 프로젝트 준비하기

- 라이브러리 설치하기

  ```bash
  $ yarn add react-router-dom
  ```



- 컴포넌트 만들기

  - components 디렉터리에 아래의 파일들 생성
  - Red.js

  ```react
  import React from "react";
  import "./Red.css";
  
  const Red = () => {
    return <div className="Red">Red</div>;
  };
  
  export default Red;
  ```

  - Red.css

  ```css
  .Red {
    background: red;
    font-size: 1.5rem;
    color: white;
    width: 128px;
    height: 128px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  ```

  - Blue.js

  ```react
  import React from 'react';
  import './Blue.css';
  
  const Blue = () => {
    return <div className="Blue">Blue</div>;
  };
  
  export default Blue;
  ```

  - Blue.css

  ```css
  .Blue {
    background: blue;
    font-size: 1.5rem;
    color: white;
    width: 128px;
    height: 128px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  ```

  - menu.js

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
      </ul>
    );
  };
  
  export default Menu;
  ```



- 페이지 컴포넌트 만들기

  - 각 라우트를 위한 페이지 컴포넌트를 pages 디렉터리에 생성
  - RedPage.js

  ```react
  import React from 'react';
  import Red from '../components/Red';
  
  const RedPage = () => {
    return <Red />;
  };
  
  export default RedPage;
  ```

  - BluePage.js

  ```react
  import React from "react";
  import Blue from "../components/Blue";
  
  const BluePage = () => {
    return <Blue />;
  };
  
  export default BluePage;
  ```



- 라우터 적용하기

  - App 컴포넌트에 라우트 설정하기

  ```react
  import React from "react";
  import { Route } from "react-router-dom";
  import Menu from "./components/Menu";
  import RedPage from "./pages/RedPage";
  import BluePage from "./pages/BluePage";
  
  const App = () => {
    return (
      <div>
        <Menu />
        <hr />
        <Route path="/red" component={RedPage} />
        <Route path="/blue" component={BluePage} />
      </div>
    );
  };
  
  export default App;
  ```

  - BrowserRouter를 사용하여 프로젝트에 리액트 라우터를 적용

  ```react
  import React from "react";
  import ReactDOM from "react-dom";
  import "./index.css";
  import App from "./App";
  import reportWebVitals from "./reportWebVitals";
  import { BrowserRouter } from "react-router-dom";
  
  ReactDOM.render(
    <React.StrictMode>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </React.StrictMode>,
    document.getElementById("root")
  );
  
  // If you want to start measuring performance in your app, pass a function
  // to log results (for example: reportWebVitals(console.log))
  // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
  reportWebVitals();
  ```



## 서버 사이드 렌더링 구현하기

- 서버 사이드 렌더링을 구현하려면 웹팩 설정을 커스터마이징해 줘야 한다.

  - CRA로 만든 프로젝트에서는 웹팩 관련 설정이 기본적으로 모두 숨겨져 있으므로 `yarn eject` 명령어로 꺼내줘야 한다.
  - `yarn ejcet` 실행 전에 커밋을 해줘야 한다.

  ```bash
  $ git add .
  $ git commit
  $ yarn eject
  ```



- 서버 사이드 렌더링용 엔트리 만들기

  - 엔트리(entry)는 웹팩에서 프로젝트를 불러올 때 가장 먼저 불러오는 파일이다.
    - 예를 들어 현재 작성 중인 리액트 프로젝에서는 index.js를 엔트리 파일로 사용한다.
    - 이 파일부터 시작하여 내부에서 필요한 다른 컴포넌트와 모듈을 불러오는 것이다.
  - 서버 사이드 렌더링을 할 때는 서버를 위한 엔트리 파일을 따로 생성해야 한다.
    - `src/index.server.js` 생성

  ```react
  import React from "react";
  import ReactDOMServer from "react-dom/server";
  
  const html = ReactDOMServer.renderToString(
    <div>Hello Server Side Rendering!</div>
  );
  
  console.log(html);
  ```

  - 서버에서 리액트 컴포넌트를 렌더링할 때는 `ReactDOMServer`의 `renderToString()` 함수를 사용한다.
    - `renderToString` 함수에 JSX를 넣어서 호출하면 렌더링 결과를 문자열로 반환한다.



- 서버 사이드 렌더링 전용 웹팩 환경 설정 작성하기

  - 작성한 엔트리 파일을 웹팩으로 불러와서 빌드하려면 서버 전용 환경 설정을 만들어 줘야 한다.
  - `config/paths.js` 파일에서 `modules.exports` 부분에 아래와 같이 두 줄을 추가한다.
    - `ssrIndexJs`는 불러올 파일의 경로, `ssrBuild`는 웹팩으로 처리한 뒤 결과물을 저장할 경로다.

  ```javascript
  module.exports = {
    (...)
    ssrIndexJs: resolveApp("src/index.server.js"), // 서버 사이드 렌더링 엔트리
    ssrBuild: resolveApp("dist"), // 웹팩 처리 후 저장 경로
    publicUrlOrPath,
  };
  ```

  - 웹팩 환경 설정 파일 작성
    - `config/webpack.config.server.js`

  ```javascript
  const paths = require("./path");
  
  module.exports = {
    mode: "production", // 프로덕션 모드로 설정하여 최적화 옵션들을 최적화
    entry: paths.ssrIndexJs, // 엔트리 경로
    target: "node", // node 환경에서 실행될 것이라는 점을 명시
    output: {
      path: paths.ssrBuild, // 빌드 경로
      filename: "server.js", // 파일 이름
      chunkFilename: "js/[name].chunk.js", // 청크 파일 이름
      publicPath: paths.publicUrlOrPath, // 정적 파일이 제공될 경로
    },
  };
  ```

  - 웹팩 로더 설정
    - 웹팩의 로더는 파일을 불러올 때 확장자에 맞게 필요한 처리를 해준다.
    - 예를 들어 JS는 babel을 사용하여 트랜스파일링을 해 주고, CSS는 모든 CSS 코드를 결합해주고, 이미지 파일은 파일을 각자 다른 경로에 따라 저장하고 그 파일에 대한 경로를 JS에서 참조할 수 있게 해준다.
    - 서버 사이드 렌더링을 할 때 CSS 혹은 이미지 파일은 그다지 중요하지 않다. 그러나 가끔 JS 파일 내부에서 파일에 대한 경로가 필요하거나 CSS Module처럼 로컬 className을 참조해야 할 수도 있기에 완전히 무시할 수는 없다.
    - 그래서 해당 파일을 로더에서 별도로 설정하여 처리하지만 따로 결과물에 포함되지 않도록 구현할 수 있다.

  ```javascript
  // config/webpack.config.server.js
  const paths = require("./paths");
  const getCSSModuleLocalIdent = require("react-dev-utils/getCSSModuleLocalIdent");
  
  const cssRegex = /\.css$/;
  const cssModuleRegex = /\.module\.css$/;
  const sassRegex = /\.(scss|sass)$/;
  const sassModuleRegex = /\.module\.(scss|sass)$/;
  
  module.exports = {
    mode: "production", // 프로덕션 모드로 설정하여 최적화 옵션들을 최적화
    entry: paths.ssrIndexJs, // 엔트리 경로
    target: "node", // node 환경에서 실행될 것이라는 점을 명시
    output: {
      path: paths.ssrBuild, // 빌드 경로
      filename: "server.js", // 파일 이름
      chunkFilename: "js/[name].chunk.js", // 청크 파일 이름
      publicPath: paths.publicUrlOrPath, // 정적 파일이 제공될 경로
    },
    module: {
      rules: [
        {
          oneOf: [
            // 자바스크립트를 위한 처리
            // 기존 webpack.config.js 를 참고하여 작성
            {
              test: /\.(js|mjs|jsx|ts|tsx)$/,
              include: paths.appSrc,
              loader: require.resolve("babel-loader"),
              options: {
                customize: require.resolve(
                  "babel-preset-react-app/webpack-overrides"
                ),
                presets: [
                  [
                    require.resolve("babel-preset-react-app"),
                    {
                      runtime: "automatic",
                    },
                  ],
                ],
                plugins: [
                  [
                    require.resolve("babel-plugin-named-asset-import"),
                    {
                      loaderMap: {
                        svg: {
                          ReactComponent:
                            "@svgr/webpack?-svgo,+titleProp,+ref![path]",
                        },
                      },
                    },
                  ],
                ],
                cacheDirectory: true,
                cacheCompression: false,
                compact: false,
              },
            },
            // CSS 를 위한 처리
            {
              test: cssRegex,
              exclude: cssModuleRegex,
              //  exportOnlyLocals: true 옵션을 설정해야 실제 css 파일을 생성하지 않는다.
              loader: require.resolve("css-loader"),
              options: {
                importLoaders: 1,
                modules: {
                  exportOnlyLocals: true,
                },
              },
            },
            // CSS Module 을 위한 처리
            {
              test: cssModuleRegex,
              loader: require.resolve("css-loader"),
              options: {
                importLoaders: 1,
                modules: {
                  exportOnlyLocals: true,
                  getLocalIdent: getCSSModuleLocalIdent,
                },
              },
            },
            // Sass 를 위한 처리
            {
              test: sassRegex,
              exclude: sassModuleRegex,
              use: [
                {
                  loader: require.resolve("css-loader"),
                  options: {
                    importLoaders: 3,
                    modules: {
                      exportOnlyLocals: true,
                    },
                  },
                },
                require.resolve("sass-loader"),
              ],
            },
            // Sass + CSS Module 을 위한 처리
            {
              test: sassRegex,
              exclude: sassModuleRegex,
              use: [
                {
                  loader: require.resolve("css-loader"),
                  options: {
                    importLoaders: 3,
                    modules: {
                      exportOnlyLocals: true,
                      getLocalIdent: getCSSModuleLocalIdent,
                    },
                  },
                },
                require.resolve("sass-loader"),
              ],
            },
            // url-loader 를 위한 설정
            {
              test: [/\.bmp$/, /\.gif$/, /\.jpe?g$/, /\.png$/],
              loader: require.resolve("url-loader"),
              options: {
                emitFile: false, // 파일을 따로 저장하지 않는 옵션
                limit: 10000, // 원래는 9.76KB가 넘어가면 파일로 저장하는데
                // emitFile 값이 false 일땐 경로만 준비하고 파일은 저장하지 않는다.
                name: "static/media/[name].[hash:8].[ext]",
              },
            },
            // 위에서 설정된 확장자를 제외한 파일들은
            // file-loader 를 사용한다.
            {
              loader: require.resolve("file-loader"),
              exclude: [/\.(js|mjs|jsx|ts|tsx)$/, /\.html$/, /\.json$/],
              options: {
                emitFile: false, // 파일을 따로 저장하지 않는 옵션
                name: "static/media/[name].[hash:8].[ext]",
              },
            },
          ],
        },
      ],
    },
  };
  ```

  - 이후 코드에서 node_modules 내부의 라이브러리를 불러올 수 있게 설정한다.
    - 아래와 같이 작성하면, react, react-dom/server 같은 라이브러리를 `import` 구문으로 불러오면 node_modules에서 찾아 사용한다.
    - 라이브러리를 불러오면 빌드할 때 결과물 파일 안에 해당 라이브러리 관련 코드가 함께 번들링된다. 

  ```react
  // config/webpack.config.server.js
  (...)
  
  module.exports = {
   (...)
    module: {
      rules: [
        {
          oneOf: [(...)],
        },
      ],
    },
    // 라이브러리를 불러올 수 있게 설정
    resolve: {
      modules: ["node_modules"],
    },
  };
  ```

  - node_modules에서 불러오는 것을 제외하고 번들링하기
    - 브라우저에서 사용할 때는 결과물 파일에 리액트 라이브러리와 우리의 애플리케이션에 관한 코드가 공존해야 한다.
    - node_modules를 통해 바로 불러와서 사용할 수 있기 때문에 서버에서는 굳이 결과물 파일 안에 리액트 라이브러리가 들어 있지 않아도 된다.
    - 따라서 서버를 위해 번들링 할 때는 node_modules에서 불러오는 것을 제외하고 번들링하는 것이 좋다.
    - 이를 위해 `webpack-node-externals`라는 라이브러리를 사용해야 한다.
  - `webpack-node-externals` 설치하기

  ```bash
  $ yarn add webpack-node-externals
  ```

  - `webpack-node-externals` 라이브러리를 설정에 적용하기

  ```react
  // config/webpack.config.server.js
  const nodeExternals = require('webpack-node-externals');
  (...)
  
  module.exports = {
   (...)
    resolve: {
      modules: ["node_modules"],
    },
    externals: [
      nodeExternals({
        allowlist: [/@babel/],
      }),
    ],
  };
  ```

  - 마지막으로 환경변수 주입하기
    - 환경 변수를 주입하면 프로젝트 내에서 `process.env.NODE_ENV` 값을 참조하여 현재 개발 환경인지 아닌지 알 수 있다.

  ```react
  // config/webpack.config.server.js
  const webpack = require("webpack");
  const getClientEnvironment = require("./env");
  (...)
  
  const env = getClientEnvironment(paths.publicUrlOrPath.slice(0, -1));
   
  module.exports = {
    (...)
    externals: [
      nodeExternals({
        allowlist: [/@babel/],
      }),
    ],
    plugins: [
      new webpack.DefinePlugin(env.stringified), // 환경변수를 주입해준다.
    ],
  };
  ```



- 빌드 스크립트 작성하기

  - 위에서 만든 환경 설정을 사용하여 웹팩으로 프로젝트를 빌드하는 스크립트 작성하기
  - `scripts/build.js`파일은 클라이언트에서 사용할 빌드 파일을 만드는 작업을 한다.
  - `scripts/build.js`와 비슷한 형식으로 `scripts/build.server.js` 스크립트 작성

  ```react
  process.env.BABEL_ENV = "production";
  process.env.NODE_ENV = "production";
  
  process.on("unhandledRejection", (err) => {
    throw err;
  });
  
  require("../config/env");
  const fs = require("fs-extra");
  const webpack = require("webpack");
  const config = require("../config/webpack.config.server");
  const paths = require("../config/paths");
  
  function build() {
    console.log("Creating server build...");
    fs.emptyDirSync(paths.ssrBuild);
    let compiler = webpack(config);
    return new Promise((resolve, reject) => {
      compiler.run((err, stats) => {
        if (err) {
          console.log(err);
          return;
        }
        console.log(stats.toString());
      });
    });
  }
  
  build();
  ```

  - 아래 명령어를 입력하여 빌드가 잘 되는지 확인

  ```bash
  $ node scripts/build.server.js
  ```

  - 아래 명령어를 입력하여 작성한 결과물이 잘 작동하는지 확인

  ```bash
  $ node dist/server.js
  
  # <div data-reactroot="">Hello Server Side Rendering!</div>
  ```

  - 더 편하게 명령어 입력하는 방법
    - 매번 빌드하고 실행할 때마다 파일 경로를 입력하는 것이 번거로울 수 있으니 package.json에서 스크립트를 생성하여 더 편하게 명령어를 입력.
    - `$ yarn start:server`로 `node dist/server.js` 명령어 대체.
    - `$ yarn build:server`로 `node scripts/build.server.js`  명령어 대체.

  ```json
  // package.json의 스크립트 부분에 추가
  
  "scripts": {
    "start": "node scripts/start.js",
    "build": "node scripts/build.js",
    "test": "node scripts/test.js",
    "start:server": "node dist/server.js",
    "build:server": "node scripts/build.server.js"
  },
  ```



- 서버 코드 작성하기

  - 서버 사이드 렌더링을 처리할 서버를 작성하기.
    - Express라는 Node.js 웹 프레임워크를 사용한다.
    - 꼭 Express가 아니어도 상관 없으며 Koa, Hapi 또는 connect 라이브러리를 사용해도 구현 가능하다.
    - 다만 Express가 사용률이 가장 높고, 추후 정적 파일들을 호스팅할 때도 쉽게 구현 가능하다.
  - Express 설치하기

  ```bash
  $ yarn add express
  ```

  - index.server.js 코드 작성하기
    - 지금은 JS 파일과 CSS 파일을 웹 페이지에 불러오는 것은 생략하고, 리액트 서버 사이드 렌더링을 통해 만들어진 결과만 보여주도록 처리한다.

  ```react
  import React from "react";
  import ReactDOMServer from "react-dom/server";
  import express from "express";
  import { StaticRouter } from "react-router-dom";
  import App from "./App";
  
  const app = express();
  
  // 서버 사이드 렌더링을 처리할 핸들러 함수.
  const serverRender = (req, res, next) => {
    // 이 함수가 404가 떠야 하는 상황에 404를 띄우지 않고 서버 사이드 렌더링을 해 준다.
    const context = {};
    const jsx = (
      <StaticRouter location={req.url} context={context}>
        <App />
      </StaticRouter>
    );
    const root = ReactDOMServer.renderToString(jsx); // 렌더링을 하고
    res.send(root);	// 결과물을 응답한다.
  };
  
  app.use(serverRender);
  
  // 5000 포트로 서버를 가동한다.
  app.listen(5000, () => {
    console.log("Running on http://localhost:5000");
  });
  ```

  - 리액트 라우터의 `StaticRouter`를 사용했다.
    - 이 라우터 컴포넌트는 주로 서버 사이드 렌더링 용도로 사용되며 props로 넣어준 `location` 값에 따라 라우팅해 준다.
    - 예시의 경우 `req.url`이라는 값을 넣어 주었는데, `req` 객체는 요청에 대한 정보를 지니고 있다.
    - `context` props는 나중에 렌더링한 컴포넌트에 따라 HTTP 상태 코드를 설정할 수 있다.
  - 서버를 다시 빌드하고 실행하기
    - 아직 CSS를 불러오지 않았기에 스타일은 적용되어 있지 않을 것이다.
    - 브라우저에서 JS도 실행되지 않기 때문에, 현재 브라우저에 나타난 정보는 모두 서버 사이드에서 렌더링된 것으로 간주할 수 있다.

  ```bash
  $ yarn build:server
  $ yarn start:server
  ```

  - 현재 브라우저에서 보이는 데이터가 서버에서 렌더링된 것인지 확인
    - 개발자 도구의 Network을 열고 새로고침을 한다.
    - 새로고침을 하고 나서 맨 위에 있는 항목(예시의 경우  red)을 누른 후 우측의 Response를 눌렀을 때 컴포넌트 렌더링 결과가 문자열로 전달되고 있는지 확인한다.
    - 하단의 `{}` 버튼을 누르면 들여쓰기되어 더욱 읽기 쉬워진다.



- 정적 파일 제공하기

  - Expess에 내장되어 있는 static 미들웨어를 사용하여 서버를 통해 build에 있는 JS, CSS 정적 파일들에 접근할 수 있도록 해준다.
  - `index.server.js`에 아래와 같이 작성

  ```react
  (...)
  import path from "path";
  
  (...)
  
  const serve = express.static(path.resolve("./build"), {
    index: false, // "/" 경로에서 index.html을 보여주지 않도록 설정
  });
  
  app.use(serve);			// 순서가 중요하다. serverRender 전에 위치해야 한다.
  app.use(serverRender);
  
  (...)
  ```

  - 다음으로 JS와 CSS 파일을 불러오도록 html에 코드를 삽입한다.
    - 불러와야 하는 파일 이름은 매번 빌드할 때마다 바뀌기 때문에 빌드하고 나서 만들어지는 assets-manifest.json 파일을 참고하여 불러오도록 작성.
    - `$ yarn build`(`$ yarn build:server`가 아니다) 실행 후 assets-manifest.json 파일에서 `main.css`, `main.js`, `runtime-main.js`, `static/js/2.48cb853b.chunk.js` 파일을 html 내부에 삽입해야 한다.

  ```react
  (...)
  import fs from "fs";
  
  // asset-manifest.json에서 파일 경로들을 조회한다.
  const manifest = JSON.parse(
    fs.readFileSync(path.resolve("./build/asset-manifest.json"), "utf8")
  );
  
  
  // static/js/2.48cb853b.chunk.js 파일은 해시 값(이 경우 48cb853b)이 매번 변경되기 때문에 아래와 같이 key를 찾아줘야 한다.
  // 나머지 파일들은 그냥 오브젝트에 접근하듯이 접근하면 된다(e.g. main.css의 value에 접근하려면 manifest.files['main.css']로 접근한다).
  const chunks = Object.keys(manifest.files)
    .filter((key) => /chunk\.js$/.exec(key)) // chunk.js로 끝나는 키를 찾아서
    .map((key) => `<script src="${manifest.files[key]}"></script>`) // 스크립트 태그로 변환하고
    .join(""); // 합친다.
  
  function createPage(root) {
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
        <script src="${manifest.files["runtime-main.js"]}"></script>
        ${chunks}
        <script src="${manifest.files["main.js"]}"></script>
      </body>
      </html>
        `;
  }
  
  const app = express();
  
  const serverRender = async (req, res, next) => {
    const context = {};
  
    const jsx = (
      <StaticRouter location={req.url} context={context}>
        <App />
      </StaticRouter>
    );
  
    const root = ReactDOMServer.renderToString(jsx); // 렌더링을 하고
    res.send(createPage(root)); // 클라이언트에게 결과물을 응답한다.
  };
  
  (...)
  ```

  - 서버를 다시 빌드하고 다시 시작한다.
    - CSS, JS가 정상적으로 적용 되었는지 확인한다.

  ```bash
  $ yarn build:server
  $ yarn start:server
  ```

  















