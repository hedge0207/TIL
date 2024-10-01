# react-router로 SPA 개발하기

## SPA와 라우터

- SPA란(Single Page Application)
  - 전통적인 웹 페이지
    - 여러 페이지로 구성되어 있다.
    - 사용자가 다른 페이지로 이동할 때마다 새로운 html을 받아오고, 페이지를 로딩할 때마다 서버에서 리소스를 전달받아 해석한 뒤 화면에 보여줬다.
    - 이렇게 사용자에게 보이는 화면은 서버측에서 준비했다.
    - 사전에 html 파일을 만들어서 제공하거나, 데이터에 따라 유동적인 html을 생성해 주는 템플릿 엔진을 사용하기도 했다.
    - 그러나 웹에서 제공되는 정보가 많아지면서, 새로운 화면을 보여 주어야 할 때마다 서버 측에서 모든 뷰를 준비하면 성능상의 문제가 발생할 수 있다.
    - 또한, 애플리케이션 내에서 화면 전환이 일어날 때마다 html을 계속 서버에 새로 요청하면 사용자의 인터페이스에서 사용하고 있던 상태를 유지하는 것도 번거롭고, 바뀌지 않는 부분까지 불러와서 보여줘야 하기에 로딩에 있어서 비효율 적이다.
  - SPA
    - 리액트 같은 라이브러리 혹은 프레임워크를 사용하여 뷰 렌더링을 사용자의 브라우저가 담당하도록 한다.
    - 애플리케이션을 브라우저에 불러와서 실행시킨 후에 사용자와의 인터렉션이 발생하면 필요한 부분만 JS를 사용하여 업데이트 한다.
    - 만약 새로운 데이터가 필요하다면 서버 API를 호출하여 필요한 데이터만 새로 불러와 애플리케이션에서 사용할 수도 있다.
  - SPA의 단점
    - 앱의 규모가 커지면 JS 파일이 너무 커진다는 단점이 있다.
    - 페이지 로딩 시 사용자가 실제로 방문하지 않을 수도 있는 페이지의 스크립트를 불러오기 때문이다.
    - 그러나 **코드 스플리팅(code splitting)**을 활용하면 라우트별로 파일들을 나누어 트래픽과 로딩 속도를 개선할 수 있다.
  - 싱글 페이지라고 해서 화면이 한 종류인 것은 아니다.
    - 서버에서 사용자에게 제공하는 페이지는 한 종류지만, 해당 페이지에서 로딩된 JS와 현재 사용자 브라우저의 주소 상태에 따라 다양한 화면을 보여줄 수 있다.



- 라우터
  - 다른 주소에 다른 화면을 보여주는 것을 **라우팅**이라 한다.
  - 리액트 라이브러리 자체에 이 기능이 내장되어 있지는 않다.
  - 그 대신 브라우저의 API를 직접 사용하여 이를 관리하거나, 라이브러리를 사용하여 이 작업을 더욱 쉽게 구현 가능하다.
  - 리액트 라우팅 라이브러리에는 다음과 같은 것들이 있다.
    - react-router: 가장 역사가 길고 사용 빈도가 높다.
    - reach-router
    - Next.js
  - JS로 라우팅을 관리하는 방식의 단점
    - 리액트 라우터처럼 브라우저에서 JS를 사용하여 라우팅을 관리하는 것은 JS를 실행하지 않는 일반 크롤러에서는 페이지의 정보를 제대로 수집해 가지 못한다는 잠재적인 단점이 있다. 따라서 구글, 네이버 같은 검색 엔진의 검색 결과에 페이지가 잘 나타나지 않을 수 있다.
    - 또한 JS가 실행될 때까지 페이지가 비어 있기 때문에 JS 파일이 로딩되어 실행되는 짧은 시간 동안 흰 페이지가 나타날 수 있다는 단점도 있다.
    - 이러한 문제들은 **서버 사이드 렌더링(server-side rendering)**을 통해 모두 해결 가능하다.



## 리액트 라우터 사용하기

- 기본적인 라우터 사용법

  - 리액트 라우터 설치하기

  ```bash
  $ yarn add react-router-dom
  ```

  - 프로젝트에 라우터 적용하기
    - `src/index.js` 파일에서 import 후 `BrowserRouter` 컴포넌트를 사용하여 감싸면 된다.
    - 반드시 아래와 같이 `{ }`로 감싸서 import 해야 한다.
    - 이 컴포넌트는 웹 애플리케이션에 HTML5의 History API를 사용하여 페이지를 새로고침하지 않고도 주소를 변경하고, 현재 주소에 관련된 정보를 props로 쉽게 조회하거나 사용할 수 있게 해준다.

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
  reportWebVitals();
  ```

  - 페이지 만들기

  ```react
  import React from "react";
  
  const Home = () => {
    return (
      <div>
        <h1>Home</h1>
        <p>가장 먼저 보이는 페이지</p>
      </div>
    );
  };
  
  export default Home;
  ```

  ```react
  import React from "react";
  
  const About = () => {
    return (
      <div>
        <h1>About</h1>
        <p>이 프로젝트는 리액트 라우터의 기초를 실습하는 프로젝트입니다!</p>
      </div>
    );
  };
  
  export default About;
  ```

  - `Route` 컴포넌트로 특정 주소에 컴포넌트 연결
    - Route 컴포넌트를 사용하여 사용자의 현재 경로에 따라 다른 컴포넌트를 보여준다.
    - 이후 실행해보면 `Home` 컴포넌트가 보이는 것을 확인 가능하다.
  - 라우트로 사용된 객체는 따로 props를 내려주지 않아도 `history` , `match`, `location` 등의 객체가 props로 내려가게 된다.
  
  ```react
  import React from "react";
  import { Route } from "react-router-dom";
  import About from "./About";
  import Home from "./Home";
  
  const App = () => {
    return (
      <div>
        <Route path="/" component={Home} />
        <Route path="/about" component={About} />
      </div>
    );
  };
  
  export default App;
  ```
  
  - `exact`
    - 위 예시에서 `localhost:3000/about`으로 들어가면 `Home` 컴포넌트와 `About` 컴포넌트가 함께 뜬다.
    - 이는 두 컴포넌트의 라우트 경로가 겹치기 때문으로, `exact`라는 속성을 주면 해결 된다.
    - 이제 주소가 정확히 일치해야만 해당 컴포넌트로 이동하게 된다.
    - props를 설정할 때 값을 지정해주지 않으면 자동으로 true가 되므로 `exact={true}` 대신 `exact`라고만 써도 된다.
  
  ```react
  import React from "react";
  import { Route } from "react-router-dom";
  import About from "./About";
  import Home from "./Home";
  
  const App = () => {
      return (
        <div>
          <Route path="/" component={Home} exact={true} />
          <Route path="/about" component={About} />
        </div>
  );
  };
  
  export default App;
  ```
  - 컴포넌트가 아닌 특정 JSX를 띄우는 페이지로 이동하게 할 수도 있다.
  
  ```react
  import React from "react";
  import { Route } from "react-router-dom";
  
  const App = () => {
    return (
      <div>
        <Route
          path="/element"
          render={() => <div>꼭 컴포넌트일 필요는 없습니다.</div>}
        />
      </div>
    );
  };
  
  export default App;
  ```



- `Link` 컴포넌트를 사용하여 주소 이동하기

  - `Link` 컴포넌트는 클릭하면 다른 주소로 이동시켜주는 컴포넌트이다.
  - `<a>`는 페이지를 전환하는 과정에서 페이지를 새로 불러오기 때문에 애플리케이션이 들고 있던 상태들을 모두 날려버리게 된다.
  - 따라서 리액트 라우터를 사용할 때는 `<a>`를 직접 사용하면 안된다.
  - `Link` 컴포넌트를 사용하여 페이지를 전환하면, 새로운 페이지를 불러오는 것이 아니라 애플리케이션을 유지한 상태에서 HTML5 History API를 사용하여 사용자의 페이지 주소만 변경해준다.
  - `Link`는 기본적으로 `<a>`로 이루어져 있지만, 페이지 전환을 방지하는 기능이 내장되어 있다.

  ```react
  import React from "react";
  import { Link, Route } from "react-router-dom";
  import About from "./About";
  import Home from "./Home";
  
  const App = () => {
      return (
        <div>
            <ul>
                <li>
                    <Link to="/">Home</Link>
                </li>
                <li>
                    <Link to="/about">About</Link>
                </li>
            </ul>
            <hr />
            <Route path="/" component={Home} exact={true} />
            <Route path="/about" component={About} />
        </div>
    );
  };
  
  export default App;
  ```



- Route 하나에 여러 개의 path 설정하기

  - 리액트 라우터 v5에서 추가된 기능
  - `path` props를 배열로 설정해 주면 여러 경로에서 같은 컴포넌트를 보여 줄 수 있다.

  ```react
  import React from "react";
  import { Link, Route } from "react-router-dom";
  import About from "./About";
  import Home from "./Home";
  
  const App = () => {
    return (
      <div>
        <Route path="/" component={Home} exact={true} />
        <Route path={["/about", "/info"]} component={About} />
      </div>
    );
  };
  
  export default App;
  ```



- URL 파라미터와 쿼리

  - 페이지 주소에 유동적인 값을 추가해야 할 때 파라미터와 쿼리를 사용한다.
    - 파라미터와 쿼리 중 어떤 상황에 무엇을 사용해야 할지에 대한 규칙은 없다.
    - 일반적으로 파라미터는 특정 아이디 혹은 이름을 사용하여 조회할 때 사용한다(e.g. `/about/cha`)
    - 일반적으로 쿼리는 어떤 키워드를 검색하거나 페이지에 필요한 옵션을 전달할 때 사용한다(e.g. `/about?details=true`)
  - URL 파라미터
      - URL 파라미터를 넘길 때 뒤에 `?`를 붙여주면 해당 파라미터가 있을 수도 있고 없을 수도 있다는 뜻이다(e.g. `<Route path="/profile/:city?" component={Profile} />`)
      - `props`로 받은 `match` 객체 안에는 현재 컴포넌트가 어떤 경로 규칙에 의해 보이는지에 대한 정보가 들어있다.
  
  ```react
  import React from "react";
  import { Link, Route } from "react-router-dom";
  import Profile from "./Profile";
  
  const App = () => {
    return (
      <div>
        <ul>
          <li>
            <Link to="/profile/daejeon">대전</Link>
          </li>
          <li>
            <Link to="/profile/daegu">대구</Link>
          </li>
        </ul>
        <hr />
        <Route path={["/about", "/info"]} component={About} />
        {/* city라는 이름의 파라미터를 넘긴다. */}
        <Route path="/profile/:city" component={Profile} />
      </div>
    );
  };
  
  export default App;
  ```
  
  ```react
  import React from "react";
  
  const data = {
    daejeon: {
      description: "교통의 중심",
    },
    daegu: {
      description: "대프리카",
    },
  };
  // 디스트럭처링을 통해 props에서 match를 뽑는다.
  const Profile = ({ match }) => {
    console.log(match); // {path: "/profile/:city", url: "/profile/daegu", isExact: true, params: {…}}
    console.log(match.prams)	// {city: "daegu"}
    const { city } = match.params;
    const profile = data[city];
    console.log(profile); // {description: "대프리카"}
    if (!profile) {
      return <div>존재하지 않는 사용자입니다!</div>;
    }
    return (
      <div>
        <h3>
          {city}({profile.description})
        </h3>
      </div>
    );
  };
  
  export default Profile;
  ```
  
  - URL 쿼리
    - 쿼리를 사용하기 위해선 쿼리 문자열을 객체로 변환해주는 `qs` 라이브러리를 설치해야 한다(`$ yarn add qs`).
    - 라우트로 사용된 컴포넌트에는 props로 웹 애플리케이션의 현재 주소에 대한 정보를 지닌 객체(`location`)가 전달된다. 
    - 쿼리 문자열을 객체로 파싱하는 과정에서 나온 결과 값은 언제나 문자열이므로 숫자를 받아와야 하면 `parseInt` 함수로 숫자로 변환해야 한다.
  
  ```react
  import React from "react";
  import qs from "qs";
  
  // // 디스트럭처링을 통해 props에서 location을 뽑는다.
  const About = ({ location }) => {
    console.log(location); // {pathname: "/about", search: "?detail=true", hash: "", state: undefined}
    // location.search에 담긴 쿼리 스트링을 객체로 변환한다.
    const query = qs.parse(location.search, { ignoreQueryPrefix: true });
    // 쿼리 문자열을 객체로 파싱하는 과정에서 나온 결과 같은 언제나 문자열이므로 아래와 같이 문자열 "true"와 비교해야 한다.
    const showDetail = query.detail === "true";
    return (
      <div>
        <h1>About</h1>
        <p>이 프로젝트는 리액트 라우터의 기초를 실습하는 프로젝트입니다!</p>
        {showDetail && <p>detail값을 true로 설정하셨군요!</p>}
      </div>
    );
  };
  
  export default About;
  ```
  
  ```react
  import React from "react";
  import { Link, Route } from "react-router-dom";
  import About from "./About";
  
  const App = () => {
    return (
      <div>
        <Link to={`/about?detail=${true}`}>About</Link>
        <hr />
        <Route path={["/about", "/info"]} component={About} />
      </div>
    );
  };
  
  export default App;
  ```



- 서브 라우트

  - 라우트 내부에 또 라우트를 정의하는 것.

  ```react
  import React from "react";
  import { Link, Route } from "react-router-dom";
  import Profiles from "./Profiles";
  
  const App = () => {
    return (
      <div>
        <Link to="/profiles">프로필</Link>
        <hr />
        <Route path="/profiles" component={Profiles} />
      </div>
    );
  };
  
  export default App;
  ```

  - 라우트로 사용되고 있는 컴포넌트 내부에 Route 컴포넌트를 또 사용하면 된다.

  ```react
  import React from "react";
  import { Link, Route } from "react-router-dom";
  import Profile from "./Profile";
  
  const Profiles = () => {
    return (
      <div>
        <h3>사용자 목록</h3>
        <ul>
          <li>
            <Link to="/profiles/daejeon">대전</Link>
          </li>
          <li>
            <Link to="/profiles/daegu">대구</Link>
          </li>
        </ul>
        <Route
          path="/profiles"
          exact
          render={() => <div>도시를 선택해 주세요</div>}
        />
        <Route path="/profiles/:city" component={Profile} />
      </div>
    );
  };
  
  export default Profiles;
  ```





## react-router 부가 기능

- `history`

  - `history` 객체는 라우트로 사용된 컴포넌트에 `match`, `location`과 함께 전달되는 props 중 하나.
  - 이 객체를 통해 컴포넌트 내에 구현하는 메서드에서 라우터 API를 호출할 수 있다.
  - 특정 버튼을 눌렀을 때 뒤로 가거나, 로그인 후 화면을 전환하거나, 다른 페이지로 이탈하는 것을 방지해야 할 때 사용한다.
  - 메서드(자주 사용하는 것들)
    - `goBack()`: 뒤로 이동
    - `goForward()`: 앞으로 이동
    - `push()`: 입력한 주소로 이동
    - `block()`: 입력한 메세지를 alert로 띄워 이동을 방지한다.

  ```react
  import React, { Component } from "react";
  
  class HistorySample extends Component {
    // 뒤로 가기
    handleGoBack = () => {
      this.props.history.goBack();
    };
  
    // 홈 화면으로 이동
    handleGoHome = () => {
      this.props.history.push("/");
    };
  
    componentDidMount() {
      // this는 컴포넌트를 가리킨다.
      // 컴포넌트에 unblock이라는 key와 this.props.history.block("정말 떠나실 건가요?")라는 value로 프로퍼티를 생성
      this.unblock = this.props.history.block("정말 떠나실 건가요?");
    }
  
    // 페이지에 변화가 생기려고 할 때마다 정말 나갈 것인지 묻는다.
    // 컴포넌트가 언마운트 되면 질문을 멈춘다.
    componentWillUnmount() {
      // componentDidMount에서 성공적으로 객체의 프로퍼티가 생성되었다면 실행
      if (this.unblock) {
        this.unblock();
      }
    }
  
    render() {
      return (
        <div>
          <button onClick={this.handleGoBack}>뒤로</button>
          <button onClick={this.handleGoHome}>홈으로</button>
        </div>
      );
    }
  }
  
  export default HistorySample;
  ```
  
  - 이탈 방지 코드 상세 설명
      - 클래스형 컴포넌트에서 라이프사이클 메서드 내부의 `this`는 컴포넌트 객체 자신을 가리킨다.
      - `componentDidMount()` 메서드를 통해 마운트가 완료된 시점에 컴포넌트 객체에 `unlock`이라는 key와 그 value로 `this.props.history.block("정말 떠나실 건가요?")`를 추가한다(`HistorySample:{unlock:this.props.history.block("정말 떠나실 건가요?")}`).
      - 변화가 생기려고 할 때 `componentWillUnmount()`가 호출되고 컴포넌트의 `unlock`이라는 key에 할당한 `this.props.history.block("정말 떠나실 건가요?")`를 실행한다.



- `withRouter`

  - **HoC(Higher-order Component)**로, 라우트로 사용된 컴포넌트가 아니어도 `match`, `location`, `history` 객체에 접근하게 해준다.
  - 아래와 같이 `withRouter`를 사용할 때는 컴포넌트를 내보낼 때 `withRouter` 함수의 인자로 넣는다.

  ```react
  import React from "react";
  import { withRouter } from "react-router-dom";
  
  const WithRouterSample = ({ location, match, history }) => {
      return (
          <div>
              <h4>location</h4>
              <textarea
                  value={JSON.stringify(location, null, 2)}
                  row={7}
                  readOnly={true}
                  />
              <h4>match</h4>
              <textarea
                  value={JSON.stringify(match, null, 2)}
                  row={7}
                  readOnly={true}
                  />
              <button onClick={() => history.push("/")}>홈으로</button>
          </div>
      );
  };
  
  export default withRouter(WithRouterSample);
  ```

    - 렌더링 할 때는 특별히 해줘야 할 것이 없다.

  ```react
  import React from "react";
  import { Link, Route } from "react-router-dom";
  import Profile from "./Profile";
  import WithRouterSample from "./WithRouterSample";
  
  const Profiles = () => {
      return (
          <div>
              (...)
              <WithRouterSample />
          </div>
      );
  };
  
  export default Profiles;
  ```

    - `withRouter`를 사용했을 때 `match`는 현재 자신을 보여주고 있는 컴포넌트를 기준으로 전달된다.
      - 위 예시에서 `<WithRouterSample />`을 보여주고 있는 컴포넌트는 `Profiles`다.
      - `profiles`에는 params로 받는 값이 없다.
      - 따라서 위 결과에서 `match`에는 params가 비어있다고 나온다.
      - 아래와 같이 prams를 받는 다른 컴포넌트에 띄우면 값이 제대로 들어가 있는 것을 확인 가능하다.
      - `Profile` 컴포넌트는 `city`를 params로 받는다.

  ```react
  import React from "react";
  import WithRouterSample from "./WithRouterSample";
  
  (...)
  
   const Profile = ({ match }) => {
      (...)
       return (
       <div>
           <h3>
               {city}({profile.description})
           </h3>
           <WithRouterSample />
       </div>
      );
  };
  
  export default Profile;
  ```



  

- `Switch`

  - 여러 Route를 감싸서 그중 일치하는 단 하나의 라우트만을 렌더링시켜 주는 컴포넌트.
  - 모든 규칙과 일치하지 않을 때 보여 줄 Not Found 페이지도 구현이 가능하다.

  ```react
  import React from "react";
  import { Link, Route, Switch } from "react-router-dom";
  import About from "./About";
  import HistorySample from "./HistorySample";
  import Home from "./Home";
  import Profiles from "./Profiles";
  
  const App = () => {
    return (
      <div>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to={`/about?detail=${true}`}>About</Link>
          </li>
          <li>
            <Link to="/profiles">프로필</Link>
          </li>
          <li>
            <Link to="/history">History 예제</Link>
          </li>
        </ul>
        <hr />
        {/* Switch 컴포넌트로 감싼다. */}
        <Switch>
          <Route path="/" component={Home} exact={true} />
          <Route path={["/about", "/info"]} component={About} />
          <Route path="/profiles" component={Profiles} />
          <Route path="/history" component={HistorySample} />
          {/* 모든 경로가 일치하지 않을 때 보여줄 JSX */}
          <Route
            render={({ location }) => (
              <div>
                <h2>이 페이지는 존재하지 않습니다.</h2>
                <p>{location.pathname}</p>
              </div>
            )}
          />
        </Switch>
      </div>
    );
  };
  
  export default App;
  ```



- `NavLink`

  - 현재 경로와 `NavLink`에서 사용하는 경로가 일치하는 경우 특정 스타일 혹은 CSS 클래스를 적용할 수 있는 컴포넌트
  - `NavLink`에서 링크가 활성화 되었을 때의 스타일을 적용할 때는 `activeStyle`값을, CSS 클래스를 적용할 때는 `activeClassName` 값을 props로 넣는다.

  ```react
  import React from "react";
  import { NavLink, Route } from "react-router-dom";
  import Profile from "./Profile";
  
  const Profiles = () => {
    const activeStyle = {
      background: "black",
      color: "white",
    };
    return (
      <div>
        <h3>사용자 목록</h3>
        <ul>
          <li>
            <NavLink activeStyle={activeStyle} to="/profiles/daejeon">
              대전
            </NavLink>
          </li>
          <li>
            <NavLink activeStyle={activeStyle} to="/profiles/daegu">
              대구
            </NavLink>
          </li>
        </ul>
        <Route
          path="/profiles"
          exact
          render={() => <div>도시를 선택해 주세요</div>}
        />
        <Route path="/profiles/:city" component={Profile} />
      </div>
    );
  };
  
  export default Profiles;
  ```



# React에서 axios 사용

- axios
  - 현재 가장 많이 사용되고 있는 JS HTTP 클라이언트.
  - HTTP 요청을 Promise 기반으로 처리한다는 특징이 있다.



- 사용하기

  - 설치

  ```bash
  $ yarn add axios
  ```

  - 사용 예시

  ```react
  import axios from "axios";
  import React, { useState } from "react";
  
  const App = () => {
    const [data, setData] = useState(null);
    const onClick = () => {
      axios
        .get("https://jsonplaceholder.typicode.com/todos/1")
        .then((response) => {
          setData(response.data);
        });
    };
    return (
      <div>
        <div>
          <button onClick={onClick}>불러오기</button>
        </div>
        {data && (
          <textarea
            rows={7}
            value={JSON.stringify(data, null, 2)}
            readOnly={true}
          />
        )}
      </div>
    );
  };
  
  export default App;
  ```



- async도 사용 가능하다.

  - 화살표 함수에 사용할 때는 `async ()=>{}`와 같은 형식으로 사용한다.

  ```react
  import axios from "axios";
  import React, { useState } from "react";
  
  const App = () => {
    const [data, setData] = useState(null);
    const onClick = async () => {
      try {
        const response = await axios.get(
          "https://jsonplaceholder.typicode.com/todos/1"
        );
        setData(response.data);
      } catch (e) {
        console.log(e);
      }
    };
    return (
      <div>
        <div>
          <button onClick={onClick}>불러오기</button>
        </div>
        {data && (
          <textarea
            rows={7}
            value={JSON.stringify(data, null, 2)}
            readOnly={true}
          />
        )}
      </div>
    );
  };
  
  export default App;
  ```

  

- 함수형 컴포넌트에서 `useEffect`에는 async를 사용해선 안된다.
  
  - async 키워드를 붙인 함수는 프로미스를 반환하는데, `useEffect`는 뒷정리 함수를 반환해야 하기 때문이다.
  - 따라서 `useEffect`에서  async를 사용해야 한다면, `useEffect` 함수 내부에 async 키워드가 붙은 또 다른 함수를 만들어서 사용해야 한다.



- Promise를 사용해야 하는 경우 더욱 간결하게 코드를 작성할 수 있도록 커스텀 Hook 만들기

  > news-viewer 프로젝트를 기반으로 작성

  - 일반적으로 프로젝트의 다양한 곳에서 사용될 수  있는 유틸 함수들을 보통 src 디렉토리에 lib 디렉토리를 만들고 그 안에 작성한다.
  - `usePromise` Hook은 Promise의 대기 중, 완료 결과, 실패 결과에 대한 상태를 관리한다.
    - 첫 번째 인자로 Promise를 실행할 함수를 받는다.
    - 두 번째 인자로`usePromise` 의 의존 배열 `deps`를 받는다.

  ```react
  import { useState, useEffect } from 'react';
  
  export default function usePromise(promiseCreator, deps) {
    const [loading, setLoading] = useState(false);
    const [resolved, setResolved] = useState(null);
    const [error, setError] = useState(null);
  
    useEffect(() => {
      const process = async () => {
        setLoading(true);
        try {
          const resolved = await promiseCreator();
          setResolved(resolved);
        } catch (e) {
          setError(e);
        }
        setLoading(false);
      };
      process();
    }, deps);
  
    return [loading, resolved, error];
  }
  ```
  
  - 적용하기
  
  ```react
  import React from 'react';
  import styled from 'styled-components';
  import axios from '../../node_modules/axios/index';
  import NewsItem from './NewsItem';
  import usePromise from '../lib/usePromise';
  
  const NewsListBlock = styled.div`
    box-sizing: border-box;
    padding-bottom: 3rem;
    width: 768px;
    margin: 0 auto;
    margin-top: 2rem;
    @media screen and (max-width: 768px) {
      width: 100%;
      padding-left: 1rem;
      padding-right: 1rem;
    }
  `;
  
  const NewsList = ({ category }) => {
      // 기존 코드
      /*
      const [articles, setArticles] = useState(null);
      const [loading, setLoading] = useState(false);
  
      // useEffect 내부에서 async를 사용하려면 함수 내부에 async 키워드가 붙은 또 다른 함수를 만들어서 사용해야 한다.
      useEffect(() => {
        const fetchData = async () => {
          setLoading(true);
          try {
            const query = category === 'all' ? '' : `&category=${category}`;
            const response = await axios.get(
              `http://newsapi.org/v2/top-headlines?country=kr${query}&apiKey=b3b1cffe26e14aa88dff0880a41bdfbc`,
            );
            setArticles(response.data.articles);
          } catch (e) {
            console.log(e);
          }
          setLoading(false);
        };
        fetchData();
      }, [category]);
      */
  
      // usePromise를 사용한 코드
      const [loading, response, error] = usePromise(() => {
          const query = category === 'all' ? '' : `&category=${category}`;
          return axios.get(
              `http://newsapi.org/v2/top-headlines?country=kr${query}&apiKey=b3b1cffe26e14aa88dff0880a41bdfbc`,
          );
      }, [category]);
  
      // 대기중일 때
      if (loading) {
          return <NewsListBlock>대기 중...</NewsListBlock>;
      }
  
      if (!response) {
          return null;
      }
  
      if (error) {
          return <NewsListBlock>에러 발생!</NewsListBlock>;
      }
  
      const { articles } = response.data;
  
      return (
          <NewsListBlock>
              {articles.map((article) => (
                  <NewsItem key={article.url} article={article} />
              ))}
          </NewsListBlock>
      );
  };
  
  export default NewsList;
  ```
  
  

  

















