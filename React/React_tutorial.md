# 목차

- [React란](#React란)
- [JSX 소개](#JSX-소개)
- [엘리먼트 렌더링](#엘리먼트 렌더링)
- [Components와 Props](#Components와-Props)
- [State와 Lifecycle](#State와-Lifecycle)



# React란

- React
  - 프론트엔드 개발 도구
  - 페이스북에서 개발
  - Vue, Angular에 비해 월등히 높은 사용량



- 리액트는 라이브러리인가 프레임워크인가
  - Vue는 스스로 Framework이라고 소개한다.
  - React는 스스로 Library라고 소개한다.



- 리액트는 왜 만들었는가
  - 시간이 지나면서 변화하는 데이터를 표현하는 재사용 가능한 UI 컴포넌트를 만들기 위해서
  - UI 컴포넌트



- 리액트를 학습하는 방법
  - 리액트 공식 문서에서 제공하는 자습서를 참고
  - 리액트 공식 문서에서 제공하는 문서 카테고리를 참고



- 리액트의 Lifecycle
  - Mounting
    - 생성하는 단계
    - 렌더링(화면을 그리는) 단계
  - Updating
    - rerender 단계
    - props나 state가 변경되었을 때 다시 랜더링 한다.
  - Unmounting
    - 종료 단계



- 추가 학습 자료
  - Awesome React(https://github.com/enaqx/awesome-react)
  - Awesome React Components(https://github.com/brillout/awesome-react-components)
  - Awesome React Talks(https://github.com/tiaanduplessis/awesome-react-talks)





# JSX 소개

- JSX(Javascript XML): JS 코드 내에 HTML 태그를 넣는 방식으로 기존의 JS를 확장한 문법이다.
  - 기존 JS의 모든 기능을 포함하고 있다.
  - React를 꼭 JSX로 개발해야 하는 것은 아니지만, JSX로 개발하는 것이 권장된다.
  - 이벤트가 처리되는 방식, 시간에 따라 state가 변하는 방식, 화면에 표시하기 위해 데이터가 준비되는 방식 등 렌더링 로직이 본질적으로 다른 UI 로직과 연결되어 있기에 이러한 방식을 사용한다.
  - 마크업(HTML) 파일과 로직(JS)을 별도의 파일에 작성하여 기술을 인위적으로 분리하는 대신 둘 다 포함하는 컴포넌트라 부르는 느슨하게 연결된 유닛으로 관심사를 분리한다.



- 기초

  - JSX은 문자열도, HTML 태그도 아니다.
  - JSX는 HTML 보다는 JS에 가깝기 때문에 camelCase로 작성한다.
  - JSX 태그는 자식을 포함할 수 있다.

  ```react
function formatName(user){
    return user.firstName + ' ' + user.lastName;
  }
  
  const name = 'Cha';
  const user = {
    firstName: "GilDong",
    lastName: "Hong"
  };
  
  const element = (
    <div>		<!--<div>태그는 자식 태그들을 포함하고 있다.-->
      <h1>Hello! {name}</h1>  <!--{}안에 name이라는 변수를 비롯한 다양한 표현식(함수까지도)을 사용할 수 있다.-->
      <h1>2+2 = {2+2}</h1>
      <h1>Hello, {formatName(user)}</h1>
    </div>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```
  
  - JSX는 주입 공격을 방지한다.
  - React DOM은 JSX에 삽입된 모든 값을 렌더링하기 전에 **이스케이프**하므로, 애플리케이션에서 명시적으로 작성되지 않은 내용은 주입되지 않는다.
    - **이스케이프**: 값을 에러 없이 제대로 전달하기 위해 제어 문자로 인식될 수 있는 특정 문자 왼쪽에 슬래시를 붙이거나 URI(URL) 혹은 HTML 엔티티 등으로 인코딩하여 제어 문자(스크립트)가 아닌 일반 문자로 인식시켜 에러 또는 에러를 이용한 부정행위를 방지하는 것.
    - 즉, 모든 항목은 렌더링 되기 전에 문자열로 변환되므로 **XSS** 공격을 방지할 수 있다.
    - **XSS(cross-site scripting)**: 웹 사이트 관리자가 아닌 자가 웹 페이지에 악성 스크립트를 삽입할 수 있는 취약점
  - JSX는 객체를 표현한다.
    - babel은 JSX를 `React.createElement()` 호출로 컴파일한다.
    - 아래 두 코드는 동일한 코드다.
  
  ```react
const element = (
    <h1 className="greeting">
      Hello, world!
    </h1>
  );
  
  const element = React.createElement(
    'h1',
    {className: 'greeting'},
    'Hello, world!'
  );
  ```



- JSX도 하나의 표현식이다.

  - 변수에 할당할 수 있다.

  ```react
  const jsxVariable = <h1>JSX는 변수에 할당 가능합니다.</h1>;
  
  
  const element = (
    <h1>{jsxVariable}</h1>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  - 인자로 받을 수 있다.

  ```react
  function getJsxParameter(jsx){
    return <div>{jsx} 를 인자로 받았습니다.</div>
  }
  
  const jsxVariable = <span>JSX는 변수에 할당 가능합니다.</span>;
  
  const element = (
    <h1>{getJsxParameter(jsxVariable)}</h1>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  - 함수로 반환할 수 있다.

  ```react
  function returnJsx(){
    return <div>JSX를 반환합니다</div>
  }
  
  const element = (
    <h1>{returnJsx()}</h1>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  - if 구문 및 반복문 등에 사용 할 수 있다.

  ```react
  function useJsx(){
    if(jsxVariable){
      return "참인 조건입니다.";
    }else{
      return "거짓은 조건입니다.";
    }
  }
  
  const jsxVariable = <span>JSX는 변수에 할당 가능합니다.</span>
  
  
  const element = (
    <h1>{useJsx()}</h1>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  

- JSX 속성 정의

  - 속성에 따옴표를 이용해 문자열 리터럴을 정의할 수 있다.

  ```react
  const element = <div tabIndex="0"></div>;
  ```

  - 중괄호를 사용하여 어트리뷰트에 JS 표현식을 삽입할 수도 있다.
    - 어트리뷰트에 JS 표현식을 사용할 때 중괄호 주변에 따옴표를 입력해선 안된다. 
    - 따옴표 또는 중괄호 중 하나만 사용하고, 동일한 어트리뷰트에 두 가지를 동시에 사용해선 안된다.

  ```react
  const element = <img src={user.avatarUrl}></img>;
  ```

  



# 엘리먼트 렌더링

- 엘리먼트
  - React 앱의 가장 작은 단위
  - 화먄에 표시할 내용을 기술한 것
  - 브라우저 DOM 엘리먼트와 달리 React 엘리먼트는 일반 객체(plain object)이며 쉽게 생성할 수 있다.
  - React DOM은 React 엘리먼트와 일치하도록 DOM을 업데이트 한다.
  - 컴포넌트와 혼동할 수 있으나 엘리먼트는 컴포넌트의 구성 요소이다.



- DOM에 엘리먼트 렌더링 하기

  - HTML 파일 어딘가에 아래와 같이 `<div>`가 있다고 가정

  ```react
  <div id="root"></div>
  ```

  - 이 `<div>` 안에 들어가는 모든 엘리먼트를 React DOM에서 관리하기에 이것을 루트(root) DOM 노드라 부른다.
  - React로 구현된 애플리케이션은 일반적으로 하나의 루트 DOM 노드가 있다.
  - React를 기존 앱에 통합하려는 경우 원하는 만큼 많은 수의 독립된 루트 DOM 노드가 있을 수 있다.
  - React 엘리먼트를 루트 DOM 노드에 렌더링하려면 `ReactDOM.render(엘리먼트,루트 DOM 노드)`와 같이 사용하면 된다.

  ```react
  //예시
  const element = <h1>Hello, world</h1>;
  ReactDOM.render(element, document.getElementById('root'));
  ```

  

- 렌더링 된 엘리먼트 업데이트 하기

  - React 엘리먼트는 불변객체(생성 후 그 상태를 바꿀 수 없는 객체)이다.
  - 엘리먼트를 생성한 후에는 해당 엘리먼트의 자식이나 속성을 변경할 수 없다.
  - 엘리먼트는 영화의 특정 장면과 같이 특정 시점의 UI를 보여준다.
  - 따라서 UI, 즉 엘리먼트를 업데이트 하는 유일한 방법은 새로운 엘리먼트를 생성하고 이를 `ReactDOM.render()`로 전달하는 것이다.

  ```react
  function tick() {  
    const element = (  //tick() 함수가 실행될 때마다 엘리먼트를 새로 생성하고,
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {new Date().toLocaleTimeString()}.</h2>
      </div>
    );
    ReactDOM.render(element, document.getElementById('root'));  //tick() 함수가 실행될 때마다 전달한다.
  }
  
  //일정한 시간 간격으로 작업을 수행하기 위해서 setInterval 함수를 사용
  setInterval(tick, 1000);
  ```

  - React DOM은 해당 엘리먼트와 그 자식 엘리먼트를 이전의 엘리먼트와 비교하고 DOM을 원하는 상태로 만드는데 필요한 경우(즉 뭔가 변경이 있을 경우)에만 DOM을 업데이트한다.
    - 위 예시 코드를 실행해보면 매초 전체 UI를 다시 그리도록 엘리먼트를 만들었지만 React DOM은 내용이 변경된 텍스트 노드만 업데이트 하는 것을 확인 가능하다.





# Components와 Props

- 컴포넌트
  - UI를 재사용 가능하도록 여러 조각으로 나눈 것.
  - 개념적으로는 JS의 함수와 유사하다. props라고 하는 임의의 입력을 받은 후, 화면에 어떻게 표시되는지를 기술하는 React 엘리먼트를 반환한다.
    - props는 속성을 나타내는 데이터이다.
    - props의 이름은 그것이 사용 될 문맥이 아닌 컴포넌트 자체의 관점에서 짓는 것은 권장한다(아래 컴포넌트 추출에 예시가 있다).



- 함수 컴포넌트와 클래스 컴포넌트

  - 컴포넌트는 class 또는 함수로 정의할 수 있으며 class로 정의된 컴포넌트는 보다 많은 기능을 제공한다.
    - 어떤 방식으로 컴포넌트를 정의하든 컴포넌트명은 항상 대문자로 시작해야 한다.
    - 이는 React가 소문자로 시작하는 컴포넌트를 DOM 태그로 처리하기 때문이다(컴포넌트가 소문자로 시작할 경우에 이를 HTML 태그로 인식한다). 
    - 예를 들어 `<div>`는 HTML의 div 태그를 나타내지만 `<Welcome/>`은 컴포넌트를 나타내며, 범위 안에 Welcome이 있어야 한다.
  - 함수로 컴포넌트 정의하기
    - 아래 코드는 props 객체 인자를 받고 React 엘리먼트를 반환하므로 유효한 React 컴포넌트라고 할 수 있다.
    - 아래와 같은 컴포넌트는 JS 함수이기 때문에 말 그대로 **함수 컴포넌트**라고 호칭한다.

  ```react
  function Welcome(props){   //대문자로 시작
      return <h1>Hello, {props.name}</h1>
  }
  ```

  - ES6 class를 사용하여 컴포넌트 정의하기
    - 아래 코드는 위에서 함수로 정의한 코드와 동일하다.

  ```react
  class Welcome extends React.Component{  //대문자로 시작
      render(){
          return <h1>Hello, {this,props.name}</h1>
      }
  }
  ```

  

- 컴포넌트 렌더링

  - 지금까지는 React 엘리먼트를 DOM 태그로 나타냈다.
  - React 엘리먼트는 사용자 정의 컴포넌트로도 나타낼 수 있다.
    - React가 사용자 정의 컴포넌트로 작성한 엘리먼트를 발견하면 JSX 어트리뷰트와 자식을 해당 컴포넌트에 단일 객체로 전달한다.
    - 이 객체를 props라고 한다.
  - 위에서 정의한 Welcome 함수로 정의한 컴포넌트(사용자 정의 컴포넌트)를 아래와 같이 나타낼 수 있다

  ```react
  function Welcome(props){
      return <h1>Hello, {props.name}</h1>
  }
  
  const element = <Welcome name="Cha" />;
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  - 위 코드가 페이지로 나타나는 과정은 다음과 같다.
    - `const element = <Welcome name="Cha" />`엘리먼트로 `ReactDOM.render()`를 호출한다.
    - React는 `{name: 'Cha'}`를 props로 하여 `Welcome` 컴포넌트를 호출한다.
    - `Welcome` 컴포넌트는 결과적으로 `<h1>Hello, Cha</h1>` 엘리먼트를 반환한다.
    - React DOM은 `<h1>Hello, Cha</h1>` 엘리먼트와 일치하도록 DOM을 효율적으로 업데이트 한다.



- 컴포넌트 합성

  - 컴포넌트 안에 다른 컴포넌트를 사용할 수 있다.
  - 이는 모든 세부 단계에서 동일한 추상 컴포넌트를 사용할 수 있음을 의미한다.
  - 일반적으로 새로운 React 앱은 최상위에 단일 App 컴포넌트를 가지고 있다. 그러나 기존 앱에 React를 통합하는 경우에는 Button과 같은 작은 컴포넌트부터 시작해서 뷰 계층의 상단으로 올라가면서 점진적으로 작업해야 할 수도 있다.

  ```react
  function Welcome(props){
      return <h1>Hello, {props.name}</h1>
  }
  
  function App(){    //Welcome을 여러 번 렌더링하는 컴포넌트
      return (
      	<div>
          	<Welcome name="Cha" />
              <Welcome name="Kim" />
              <Welcome name="Lee" />
          </div>
      );
  }
  
  ReactDOM.render(
  	<App />,
      document.getElementById('root')
  );
  ```

  



- 컴포넌트 추출

  - 컴포넌트의 구성 요소들이 중첩 구조로 이루어져 있을 경우 변경이 어렵고 각 구성 요소를 개별적으로 재사용 하기도 어렵다.
  - 하나의 컴포넌트에서 여러 개의 작은 컴포넌트를 추출하여 나누는 것이 가능하다.
  - 아래 코드는 Comment라는 컴포넌트에 많은 구성요소들이 중첩 구조로 작성되어 있다.

  ```react
  function formatDate(date) {
    return date.toLocaleDateString();
  }
  
  function Comment(props) {
    return (
      <div className="Comment">
        <div className="UserInfo">
          <img
            className="Avatar"
            src={props.author.avatarUrl}
            alt={props.author.name}
          />
          <div className="UserInfo-name">
            {props.author.name}
          </div>
        </div>
        <div className="Comment-text">{props.text}</div>
        <div className="Comment-date">
          {formatDate(props.date)}
        </div>
      </div>
    );
  }
  
  const comment = {
    date: new Date(),
    text: 'I hope you enjoy learning React!',
    author: {
      name: 'Hello Kitty',
      avatarUrl: 'https://placekitten.com/g/64/64',
    },
  };
  ReactDOM.render(
    <Comment
      date={comment.date}
      text={comment.text}
      author={comment.author}
    />,
    document.getElementById('root')
  );
  ```

  - 위 코드에서 Avatar, UserInfo를 추출하여 분리하면 다음과 같은 코드가 된다.

  ```react
  function formatDate(date) {
    return date.toLocaleDateString();
  }
  
  function Avatar(props) {
    return (
      <img
        className="Avatar"
        src={props.user.avatarUrl}  //props의 이름이 작성자인 author user로 바뀌었다.
        alt={props.user.name}		  //SNS의 작성자를 뜻하므로 문맥상 user 보다는 author가 적절할 수 있다.
      />							  //그러나 props의 이름은 문맥이 아닌 컴포넌트 자체의 관점에서 작성해야 한다.
    );							  //Avatar 컴포넌트는 사용자를 받고 있으므로 user가 더 적절하다.
  }
  
  function UserInfo(props) {
    return (
      <div className="UserInfo">
        <Avatar user={props.user} />
        <div className="UserInfo-name">{props.user.name}</div>
      </div>
    );
  }
  
  function Comment(props) {
    return (
      <div className="Comment">
        <UserInfo user={props.author} />
        <div className="Comment-text">{props.text}</div>
        <div className="Comment-date">
          {formatDate(props.date)}
        </div>
      </div>
    );
  }
  
  const comment = {
    date: new Date(),
    text: 'I hope you enjoy learning React!',
    author: {
      name: 'Hello Kitty',
      avatarUrl: 'https://placekitten.com/g/64/64',
    },
  };
  ReactDOM.render(
    <Comment
      date={comment.date}
      text={comment.text}
      author={comment.author}
    />,
    document.getElementById('root')
  );
  ```

  - 이처럼 컴포넌트를 추출하는 과정은 다음과 같은 상황에서 더 빛을 발한다.
    - UI 일부가 여러 번 재사용되야하는 경우
    - UI 일부가 자체적으로 복잡한 경우(이미 복잡한데 굳이 다른 컴포넌트와 함께 작성하면 더 복잡해진다)



- props는 읽기 전용이다.

  - 함수 컴포넌트나 클래스 컴포넌트 모두 컴포넌트의 자체 props를 수정해서는 안된다.
  - 모든 React 컴포넌트는 자신의 props를 다룰 때 반드시 순수 함수처럼 동작해야 한다.
    - 순수함수: 입력값을 바꾸려 하지 않고 항상 동일한 입력값에 대해 동일한 결과를 반환하는 함수

  ```react
  //아래 sum 함수는 순수 함수다.
  function sum(a, b) {
    return a + b;
  }
  
  //아래 withdraw 함수는 자신의 입력값을 변경하기에 순수 함수가 아니다.
  function withdraw(account, amount) {
    account.total -= amount;
  }
  ```

  



# State와 Lifecycle

- 문제

  - 위 엘리먼트 렌더링 파트에서 살펴본 시간이 변할 때마다 다시 렌더링 하는 코드는 아래와 같았다. 아래 코드를 캡슐화하고 재사용 가능하도록 하며 컴포넌트가 스스로 타이머를 설정하여 매초 스스로 업데이트 하도록 변경하려 한다.

  ```react
  function tick() {  
    const element = (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {new Date().toLocaleTimeString()}.</h2>
      </div>
    );
    ReactDOM.render(element, document.getElementById('root'));
  }
  
  setInterval(tick, 1000);
  ```

  - Clock 컴포넌트를 만들어 캡슐화

  ```react
  function Clock(props) {   //Clock 컴포넌트를 함수로 정의
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {props.date.toLocaleTimeString()}.</h2>
      </div>
    );
  }
  
  function tick() {
    ReactDOM.render(
      <Clock date={new Date()} />,
      document.getElementById('root')
    );
  }
  
  setInterval(tick, 1000);
  ```

  - 캡슐화는 했지만 아직 Clock 컴포넌트가 스스로 타이머를 설정하지 않고 있고 매초 UI를 업데이트 하지도 않고 있다.
  - 이를 구현하기 위해서 Clock 컴포넌트에 **state**를 추가해야 한다.



- 함수로 정의한 컴포넌트를 클래스로 재정의하기

  - 재정의 순서
    - React.Component를 상속받는 ES6 class를 생성한다.
    - `render()`라는 빈 메서드를 추가한다.
    - 함수의 내용을 `render()` 메서드 안으로 옮긴다.
    - `render()` 안에 있는 props를 `this.props`로 변경한다.
    - 남아있는 빈 함수 선언을 삭제한다.
  - 재정의하는 이유
    - `render()` 메서드는 업데이트가 발생할 때마다 호출되지만, 같은 DOM 노드로 `<Clock />`을 렌더링하는 경우 Clock 클래스의 단일 인스턴스만 사용된다.
    - 이는 로컬 state와 생명주기 메서드와 같은 부가적인 기능을 사용할 수 있게 해준다.

  ```react
  class Clock extends React.Component {  //함수를 클래스로 변경
    render() {
      return (
        <div>
          <h1>Hello, world!</h1>
          <h2>It is {this.props.date.toLocaleTimeString()}.</h2>  <!--props를 this.props로 변경-->
        </div>
      );
    }
  }
  
  function tick() {
    ReactDOM.render(
      <Clock date={new Date()} />,
      document.getElementById('root')
    );
  }
  
  setInterval(tick, 1000);
  ```

  

- 클래스에 로컬 스테이트 추가하기

  - `render()` 메서드 안에 있는 `this.props.date`를 `this.state.date`로 변경

  - 초기 `this.state`를 지정하는 class constructor(생성자)를 추가
    - constructor: 객체를 생성하고 초기화하기 위한 특수한 메서드, 클래스 안에 한 개만 존재할 수 있다.
    - constructor는 `super`키워드로 부모 클래스의 constructor를 호출할 수 있다.
    - 클래스 컴포넌트는 항상 props로 기본(basic) constructor(React.Component의 constructor)를 호출해야 한다.
  - `<Clock />` 엘리먼트에서 date prop을 삭제.

  ```react
  class Clock extends React.Component {
    //constructor 생성
    constructor(props) { //props로 constructor 호출
      super(props);
      this.state = {date: new Date()};
    }
  
    render() {
      return (
        <div>
          <h1>Hello, world!</h1>
          <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
        </div>
      );
    }
  }
  
  ReactDOM.render(
    <Clock />,  //date prop 삭제
    document.getElementById('root')
  );
  ```

  - 위 코드도 아직까지는 타이머를 스스로 설정하고 매 초 스스로 업데이트 하지는 못한다.



- 생명주기 메서드를 클래스에 추가하기

  - 리액트에서는 컴포넌트가 처음 DOM에 의해 렌더링 될 때를 마운팅이라고 한다.
  - 마운팅 될 때마다 타이머를 설정하고 언마운트 될 때마다 타이머를 해제 하려고 한다.
  - 위와 같은 기능을 구현하기 위해서 컴포넌트 클래스에 특정한 메서드를 선언하여 컴포넌트가 마운트 되거나 언마운트 될 때 해당 메서드가 실행되도록 할 수 있다.
  - 이러한 메서드를 **생명주기 메서드**라 부른다.

  ```react
  class Clock extends React.Component {
    constructor(props) {
      super(props);
      this.state = {date: new Date()};
    }
  
    componentDidMount() {   //마운트 될 때 실행될 메서드
      this.timerID = setInterval(
        () => this.tick(),
        1000
      );
    }
  
    componentWillUnmount() {  //언마운트 될 때 실행될 메서드
      clearInterval(this.timerID);  //clearInterval()을 사용하여 타이머를 초기화
    }
  
    tick() {
      this.setState({
        date: new Date()
      });
    }
  
    render() {
      return (
        <div>
          <h1>Hello, world!</h1>
          <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
        </div>
      );
    }
  }
  
  ReactDOM.render(
    <Clock />,
    document.getElementById('root')
  );
  ```

  - 위 코드가 페이지로 나타나는 과정은 다음과 같다.

    - `<Clock />`이 `ReactDOM.render()`로 전달되었을 때 React는 Clock 컴포넌트의 constructor를 호출한다. Clock이 현재 시간을 표시해야 하기에 현재 시각이 포함된 채로 `this.state`를 초기화 한다.
    - React는 Clock 컴포넌트의 `render()` 메서드를 호출한다. 이를 통해 React는 화면에 표시되어야 할 내용을 알게 된다. 그 다음 React는 Clock의 렌더링 출력값을 일치시키기 위해 DOM을 업데이트 한다.
    - `lock` 출력값이 DOM에 삽입되면, React는 `componentDidMount()` 생명주기 메서드를 호출한다. 그 안에서 Clock 컴포넌트는 매초 컴포넌트의 `tick()` 메서드를 호출하기 위한 타이머를 설정하도록 브라우저에 요청한다.
    - 매초 브라우저가 `tick()` 메서드를 호출한다. 그 안에서 Clock 컴포넌트는 `setState()`에 현재 시각을 포함하는 객체를 호출하면서 UI 업데이트를 진행한다. `setState()` 호출 덕분에 React는 state가 변경된 것을 인지하고 화면에 표시될 내용을 알아내기 위해 `render()` 메서드를 다시 호출한다. 이 때 `render()` 메서드 안의 `this.state.date`가 달라지고 변경된 시간이 렌더링 되어 출력된다. React는 이에 따라 DOM을 업데이트한다.

    - Clock 컴포넌트가 DOM으로부터 한 번이라도 삭제된 적이 있다면 React는 타이머를 멈추기 위해 `componentWillUnmount()` 생명주기 메서드를 호출한다.



- State 올바르게 사용하기

  - 직접 state를 수정해선 안된다. `setState()`를 사용해야 한다.

  ```react
  // 틀린 방법, 이 방법은 컴포넌트를 다시 렌더링하지 않는다.
  this.state.comment = 'Hello';
  
  
  //올바른 방법
  this.setState({comment: 'Hello'});
  ```

  - `this.state`를 지정할 수 있는 유일한 공간은 바로 constructor다.
  - state 업데이트는 비동기적일 수도 있다.
    - React는 성능을 위해 여러 `setState()` 호출을 단일 업데이트로 한꺼번에 처리할 수 있다.
    - `this.props`와 `this.state`가 비동기적으로 업데이트될 수 있기 때문에 다음 state를 계산할 때 해당 값에 의존해서는 안 된다.

  ```react
  //아래 코드는 카운터 업데이트에 실패할 수 있다.
  this.setState({
    counter: this.state.counter + this.props.increment,
  });
  
  
  //이를 막기 위해서는 아래와 같이 객체보다는 함수를 인자로 사용하는 다른 형태의 setState()를 사용해야 한다.
  this.setState((state, props) => ({
    counter: state.counter + props.increment
  }));
  
  //꼭 위처럼 화살표 함수를 사용해야 하는 것은 아니다.
  this.setState(function(state, props) {
    return {
      counter: state.counter + props.increment
    };
  });
  ```

  - state 업데이트는 병합된다.
    - state는 다양한 독립적인 변수를 포함할 수 있다.
    - `setState()`를 호출할 때 React는 제공한 객체를 현재 state로 병합한다.
    - 별도의 `setState()` 호출로 이러한 변수를 독립적으로 업데이트할 수 있다.
    - 병합은 얕게 이루어지기 때문에 `this.setState({comments})`는 `this.state.posts`에 영향을 주진 않지만 `this.state.comments`는 완전히 대체 된다.

  ```react
  class User extends React.Component {
    constructor(props) {
      super(props);
      this.state = {    //posts, comments 라는 다양한 독립적인 변수를 포함한 state
          posts: [],
          comments: [],
      };
    }
  
    componentDidMount() {
      fetchPosts().then(response => {
        this.setState({        //독립적으로 업데이트, 이는 this.state.comments에는 영향을 주지 않지만 this.state.posts는 완전히 대체
          posts: response.posts
        });
      });
  
      fetchComments().then(response => {
        this.setState({         //독립적으로 업데이트, 이는 this.state.posts에는 영향을 주지 않지만 this.state.comments는 완전히 대체
          comments: response.comments
        });
      });
    }
      
   //후략
  }
  ```

  - 데이터는 아래로 흐른다.
    - 부모 컴포넌트나 자식 컴포넌트 모두 특정 컴포넌트가 유상태인지 또는 무상태인지 알 수 없고, 그들이 함수나 클래스로 정의되었는지에 대해서 관심을 가질 필요가 없다.
    - 이 때문에 state는 종종 로컬 또는 캡슐화라고 불린다. state가 소유하고 설정한 컴포넌트 이외에는 어떠한 컴포넌트에도 접근할 수 없습니다.
    - 컴포넌트는 자신의 state를 자식 컴포넌트에 props로 전달할 수 있다.
    - 이를 하향식(top-down) 또는 단방향 데이터 흐름이라 한다. 모든 state는 항상 특정한 컴포넌트가 소유하고 있으며 그 state로 부터 파생된 UI 또는 데이터는 오직 트리구조에서 자신의 아래에 있는 컴포넌트에만 영향을 미친다.

  - React 앱에서 컴포넌트가 유상태 또는 무상태에 대한 것은 시간이 지남에 따라 변경될 수 있는 구현 세부 사항으로 간주한다. 유상태 컴포넌트 안에서 무상태 컴포넌트를 사용할 수 있으며, 그 반대 경우도 마찬가지로 사용할 수 있다.

​		















