# 목차

- [Vue.js](#Vue)
- [Vue 라이프 사이클](#Vue-라이프-사이클)

- [Vue 프로젝트](#vue-프로젝트)





# Vue

> https://kr.vuejs.org/v2/guide/index.html

- Vue 개요
  - Front-end Framework
  - SPA(Single Page Application):
    - 단일 페이지로 구성된 웹 어플리케이션, 화면이동 시에 필요한 데이터를 서버사이드에서 HTML으로 전달받지 않고(서버사이드 렌더링 X), 필요한 데이터만 서버로부터 JSON으로 전달 받아 동적으로 렌더링하는 것이다.
    - 요청에 의해 바뀌어야 하는 것은 일부분이라도 문서 전체를 다시 보내게 되는데 이는 비효율적이다. 따라서 최초 요청을 받았을 때 더 많은 것을 담은 문서를 보내고 이후 요청부터는 최초에 보낸 문서에서 조금씩 수정이 이루어지는 방식(비동기 요청)으로 응답을 보낸다. 최초에 보내야 하는 문서가 더 커지므로 최초에 시간이 더 걸릴 수 있다는 단점이 존재
  - Client Side Rendering: 기존에는 서버가 HTML파일을 렌더링해서 페이지를 보냈으나 이제는 서버는 HTML파일을 브라우저로 보내고 브라우저가 이를 받아서 렌더링한다. 브라우저에서 렌더링 하는데 JavaScript가 사용된다.
  - MVVM(Model, View, ViewModel) 패턴
    - Model: JavaScript Object,  데이터와 그 데이터를 처리하는 부분
    - View: DOM(HTML) 사용자에서 보여지는 UI 부분
    - ViewModel: Vue, View를 표현하기 위해 만든 View를 위한 Model, View를 나타내 주기 위한 Model이자 View를 나타내기 위한 데이터 처리를 하는 부분
  - 반응형(Reactive)/선언형(Declatative)
    - 반응형은 데이터가 변경되면 이에 반응하여 연결된 DOM(HTML)이 업데이트(다시 렌더링) 되는 것을 의미한다.
    - e.g. 페이스북에서 친구 차단을 했을 때 친구 목록, 게시글 페이지, 댓글 등에서 그 친구를 일일이 삭제해 주는 것이 아니라 반응형으로 모든 곳에서 삭제.



- 시작 전 준비 사항

  - VS code에서 `Vetur` 설치, 코드 작성에 도움을 준다.
  - Chrome에서 `Vue.js devtools` 설치-확장프로그램 관리-파일 URL에 대한 엑세스 허용 체크, 브라우저에서 볼 때 도움을 준다.
  - 아래 코드를 추가

  > https://kr.vuejs.org/v2/guide/installation.html

  - npm: Node Package Manager의 약자, 자바스크립트 런타임 환경 Node.js의 기본 패키지 관리자.
  
  ```html
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  ```




- 기본형

  
  - 모든 Vue 앱은 Class로부터 새로운 Vue 인스턴스를 생성하는 것부터 시작
  
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vue JS</title>
  </head>
  <body>
    <!--
  	div태그는 기본 태그로 어떤 태그인지 적지 않으면 div태그로 인식한다.
  	아래의 <div id="app">의 경우 그냥 #app만 입력하면 생성된다.
  	#은 id를 지정할 때 사용하고, .은 class를 지정할 때 사용한다.
  	e.g. li#abc => <li id="abc">  /  li.abc  =>  <li class="abc">
    -->
    <div id="app"> 
  
    </div>
    <!--Vue js 를 사용하기 위한 코드-->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      //Vue는 object다.
      const app = new Vue({  //new Vue를 통해 Vue라는 인스턴스(파이썬의 클래스와 유사)를 생성
        // Vue안에 들어가는 오브젝트({})는 Vue 인스턴스의 속성이다. 따라서 el, data 등은 Vue 인스턴스의 속성이다.
        // 이 속성들의 key값(el,data 등)은 쓰고 싶은 것을 쓰는 것이 아니라 Vue에서 정해진 대로 쓰는 것이다. 
        el: '#app', //el은 어떤 요소에 mount할지를 정하는 것이다.
        data: {  //data는 MVVM에서 Model에 해당한다. 
          message: 'Hello Vue'
            
      //Vue라는 오브젝트는 자신의 내부에 있는 요소들을 재정렬한다. 따라서,
      //console.log(app.data.message)라고 쓰지 않고 console.log(app.message)라고만 적어도 알아서 app내의 data 내	  부의 message를 가져온다.
        }
      })
    </script>
  </body>
  </html>
  ```



- JS와의 차이

  ```html
  <div id="app">
      {{ message }}
  </div>
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    //JS로 구현한 코드
    let message = '안녕하세요!'
    const app = document.querySelector("#app")
    app.innerText = message
    //여기서 message를 수정하고 싶다면 콘솔창에
    //message = '잘가요!'가 아닌
    //app.innerText=message를 입력해야 한다.
      
  
    //Vue로 구현한 코드
    const optionObj = {
      el:'#app',
      data:{
        message:'안녕하세요',
      }
    }
    const app = new Vue(optionObj)
  
  
    //위 코드를 간결하게 적은 코드
    const app = new Vue({
      el:'#app',
      data:{
        message:'안녕하세요',
      }
    })
    //message를 수정하고 싶다면 
    //app.message='잘가요'를 입력해주면 된다.
  </script>
  ```




- interpolation(보간법): `v-text`와 동일한 기능을 한다.

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vue JS</title>
  </head>
  <body>
    {{ message }} <!--이 메세지는 mount가 설정되지 않았으므로 메세지가 출력되지 않는다.-->
    
    <div id="app">
      {{ message }} <!--DTL과 유사하게 중괄호 두 개로 표현한다.-->
    </div>
  
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      const app = new Vue({
        el: '#app',
        data: {
          message: 'Hello Vue'
        }
      })
      
    </script>
  </body>
  </html>
  ```



- 디렉티브

  - `v-`를 접두사로 하는 모든 것들을 디렉티브(명령하는 것)라 부르며, HTML 속성이 아닌 Vue js에서 지원하는 것이다.
  - 디렉티브 안에 변수를 쓸 때는 `" "`를 사용한다.
  - 태그 밖에 변수를 쓸 때는 보간법을 사용한다.
  - `v-text`

  ```html
  <!--편의상 필요 없는 코드는 모두 걷어 냄-->
  
  <!-- v-text -->
  <div id="app">
    <!-- Vanilla Js의 domElement.innerText와 유사하다. -->
    <!-- v- 접두사로 시작하는 것들은 모두 디렉티브 라고 부른다. -->
    <p v-text="messagee"></p>  <!--이 코드와-->
    <p>{{ messagee }}</p>	  <!--이 코드는 단순 출력 내용이 동일한 것이 아니라 완전히 동일한 코드다.-->
  </div>
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el: '#app',
      data: {
        messagee: '완전히 같아요.'
    }
    })    
  </script>
  ```

  - `v-html`
    - `v-html(혹은 innerHTML)`은 보안상의 문제가 있다. `v-html`은 입력 받은 내용을 실제 html태그에 담아서 보여주는데, 만일 누군가 태그에 악의적인 의도를 가지고 `v-html`디렉티브를 넣고 JS를 활용하여 다른 사용자 브라우저의 쿠키나 세션에 접근하여 정보를 가져올 수 있는 코드를 작성할 경우 `v-html`로 작성한 글을 본 모든 사용자는 쿠키나 세션 정보를 뻬앗기게 된다. 따라서 써도 안전하다는 것이 확실하지 않다면 쓰지 않아야 한다.

  ```html
  <div id="app">
    <!--innerText와 동일-->
    <p v-text="abc"></p>
    <!--innerHTML과 동일-->
    <!--abc가 문자열이 아닌 실제 p태그로 표시된다.-->
    <p v-html="abc"></p>
  
    <!-- v-html의 위험성 -->
    <!--
      input창에 <button @click="change">바꾸기</button>와 같이 적으면
      실제 버튼이 생긴다. 이 상태에서는 눌러도 아무것도 달라지는 것이 없지만
      만일 누군가 이런 글을 등록 후 우리 데이터 베이스에 저장이 되면 그 때부터는
      실제 데이터를 건들 수 있게 된다. 따라서 누군가 악의적으로 v-html 디렉티브가
      달려있는 input창이나 textarea에 위와 같은 코드를 입력하고 게시글을 저장하면
      다음에 그 글을 본 누군가가 버튼을 누르게 되면 아래 change 메소드가 실행되어
      text는 false로 바뀌게 된다. 예시는 실제로 쓰이지 않는 변수의 진리값이 변하는 
      것에서 그치지만 실제로 위와 같은 방법이 악용될 경우에는 큰 피해를 불러올 수 있다.
    -->
    <input type="text" v-model="msg">
    <p v-text="msg"></p>
    <p v-html="msg"></p>
    <p>{{test}}</p>
  </div>
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el:"#app",
      data:{
        abc:"<p>v-text와 v-html의 차이</p>",
        msg:'',
        test:true,
      },
      methods:{
        change:function(){
          this.test=!this.test
        },
      }
    })
  </script>
  ```

  - `v-if`
    - 한 태그에 조건은 하나만 달 수 있다. 따라서 여러개의 조건문이 필요할 경우 HTML에 실제로 렌더링 되지 않는 태그인 `<template>`를 사용하여 여러개의 조건문을 달 수 있다.

  ```html
  <!-- v-if -->
  <!--아래 내용은 Vue.js가 아닌 JS의 기준에 따라 판단한다.-->
  <!--비어 있는 배열, 오브젝트는 True로 평가된다. 따라서 배열.length로 비어있는지 판단을 해야 한다. 배열이 비었다면 길이가 0일 것이고 0은 false를 뜻하므로 비여있는 배열인지 확인이 가능하다.-->
  <div id="app">
    <p v-if="bool1">
      true
    </p>
    <p v-if="bool2">   <!--false 이므로 출력 안됨-->
      false   
    </p>
  
    <p v-if="str1">
      'Yes'
    </p>
    <p v-if="str2">    <!--false 이므로 출력 안됨-->
      ''
    </p>
  
    <p v-if="num1">  
      1
    </p>
    <p v-if="num2">    <!--false 이므로 출력 안됨-->
      0
    </p>
  </div>
  
    
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el:'#app',
      data:{  
        bool1:true,
        bool2:false,
        str1:"Yes",
        str2:"",  //빈 문자열은 false
        num1:1,
        num2:0,  //0은 false
    }
    })
  </script>
  ```

  - `v-else-if`, `v-else`

  ```html
  <!-- v-else-if, v-else -->
  <div id="app">
    <p v-if="username === 'master'">
      hello master
    </p>
    <p v-else>
      hello user
    </p>
  
    <p v-if="number > 0">
      양수
    </p>
    <p v-else-if="number < 0">
      음수
    </p>
    <p v-else>
      0
    </p>
  </div>
  
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <!--아래 username이나 number를 바꿔주면 반응형으로 조건에 따라 출력 내용이 바뀐다.-->
  <script>
    const app = new Vue({
      el:'#app',
      data:{  
        username:"master",
        number:0,
    }
    })
  </script>
  ```

  - `v-for`

  ```html
  ㅂ<div id="app">
    <ul>
      <li v-for="number in numbers">{{ number + 1 }}</li>
    </ul>
  
    <ol>
      <!--teachers에는 object가 들어있으므로 teacher.name으로 이름을 출력한다.-->
      <li v-for="teacher in teachers">{{ teacher.name }}</li>
    </ol>
  </div>
  
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el:'#app',
      data:{  
        numbers: [0,1,2,3,4,5],
        teachers: [
          {name:'neo'},
          {name:'tak'},
        ]
    }
    })
  </script>
  ```

  - `v-for`를 쓸 때 `v-bind:key`를 함께 줘야 하는 경우
    - 반복을 수행하다가 출력되는 순서가 바뀔 경우 화면이 렌더링될 때 부자연스럽게 렌더링 되는 경우가 있다.
    - 순서가 바뀔 경우 배열의 인자들의 순서를 다시 파악해야 하기에, 어떤 인자가 이전에 몇 번째로 출력되던 인자였는지 파악하는데 시간이 걸린다(예를 들어 모양이 유사한 공 3개를 일렬로 배치한 후 다시 공을 섞어서 이전에 배치했던 자리를 피해서 배치하려고 하면 이전에 어떤 공이 어떤 자리에 놓였었는지를 알고 있어야 한다. 만일 공에 번호(고유한 값)가 붙어 있다면 금방 하겠지만 그렇지 않다면 공을 유심히 관찰하고 놓아야 할 것이다). 
    - 고유한 값을 줄 경우 보다 자연스럽게 렌더링 할 수 있다.

  ```html
  <!--위와 같은 문제가 생기면 v-bind:key를 작성하고-->
  <div v-for="fruit in fruits" v-bind:key="fruits.id">{{ fruits.name }}</div>
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      // 여기에 코드를 작성하시오
      const app = new Vue({
        el:"#app",
        data:{
          fruits:[
            {
              id: 1,  //인자마다 고유한 값을 준다(key값의 이름이 꼭 id일 필요는 없다. 고유한 값이기만 하면 된다.)
              name:'수박',
            },
            {
              id:2,
              name:'참외',
            },
            {
              id:3,
              name:'사과',
            },
          ],
    },
  ```

  - `v-bind`: 표준 HTML 속성과 Vue 인스턴스를 연동할 때 사용한다. 줄여서 `:`만 쓰는 것이 가능하다.

  ```html
  <!--
    아래 코드는 안된다.
    <a href="{{googleUrl}}">Google link</a>
  -->
  <div id="app">
    <a v-bind:href="googleUrl">Google link</a>
    <a v-bind:href="naverUrl">Naver link</a>
    <img v-bind:src="randomImageUrl" v-bind:alt="altText">
  </div>
  
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el:'#app',
      data:{  
        googleUrl:'https://google.com',
        naverUrl:'https://naver.com',
        randomImageUrl:'https://picsum.photos/200',
        altText: 'random-image',
    }
    })
  </script>
  ```
  
  - 클래스 바인딩
      - `v-bind:class="{클래스명:조건}"`
  
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
  
    <style>
      .darkmode{
        color:white;
        background-color: black;
      }
    </style>
  
  </head>
  <body>
    <div id="app" v-bind:class="{darkmode:isDarkMode}">  <!--isDarkMode가 true면 darkmode클래스를 적용하겠다.-->
      <h1>제목</h1>
      <button v-on:click="toggleMode">검은색</button>
    </div>
  
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      const app = new Vue({
        el:"#app",
        data:{
          isDarkMode:false
        },
        methods:{
          //함수가 실행될 때 마다 isDarkMode의 t/f가 전환
          toggleMode: function(){
            this.isDarkMode = !this.isDarkMode
          }
        }
      })
    </script>
  </body>
  </html>
  ```
  
  - `v-on`: event와 관련된 작업에 사용되는 디렉티브,  줄여서 `@`로 쓰는 것이 가능하다.

  ```html
  <div id="app">
    <h1>{{ message }}</h1>
    <!--
      buttom.addEventListener('click',callback)에서
      .addEventListener는 v-on:
      'click'은 click=
      callback은 "alertWarning"에 해당한다.
    -->
    <button v-on:click="alertWarning">Alert Warning</button>
    <button v-on:click="alertMessage">Alert Message</button>
    <button v-on:click="changeMessage">Change Message</button>
    <hr>
    <input v-on:keyup.enter="onInputChange" type="text">
      <!--위 처럼 키보드 관련 이벤트는 버튼을 설정하는 것이 가능하다.-->
  </div>
  
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el:'#app',
      data:{  
        message:'Hello'
      },
      methods:{
        alertWarning: function () {
          alert(this.message)
        },
        alertMessage () {
          alert(this.message)
        },
        changeMessage () {
          this.message = 'Bye'
        },
        //위 메소드들은 event를 적지 않아도 작동하는데 JS는 인자를 받는 것이 자유롭기 때문이다.
        onInputChange(event) {
          // if (event.key==="Enter"){
          this.message=event.target.value
          // }
          //v-on:keyup.enter가 주석처리한 if문의 역할을 대신한다.
        }
      }
    })
  </script>
  ```



- `v-model`: 사용자 입력과 data를 완전히 동기화(양방향 동기화) 시키기 위해 사용한다.
  - 사용자 입력과 data를 동기화 시키는 것이므로 사용자가 입력할 수 있는 `input`,`select`,`textarea`에서만 사용 가능하다.

  ```html
  <div id="app">
    {{message}}
    <hr>
    <!--단방향 바인딩( input => data )-->
    <!--
      입력창에 다른 것을 입력하면(event.target.value를 바꾸면, input이 바뀌면) message(data)가 바뀌지만,
      브라우저의 Vue창에서 message(data)를 바꾼다고 해서 input이 바뀌지는 않는다.
    -->
    <input @keyup="onInputChange" type="text">
  
    <!--양방향 바인딩( input <=> data)-->
    <input @keyup="onInputChange" type="text" :value="message">
  
    <!-- v-model을 사용한 양방향 바인딩-->
    <!--이 경우 아래 정의한 methods를 주석처리해도 작동한다.-->
    <input v-model="message" type="text">
  </div>
  
  <!--
  위 코드를 브라우저로 실행하면 입력창 3개가 뜨는데, 어느 검색창에 입력을 하든 data는 바뀌게 된다. 그러나 양방향 바인딩이 된 2,3번째 검색창은 data가 바뀔 경우엔 입력창에 입력된 input도 바뀌게 되는데 단방향 바인딩인 1번째 검색창의 input은 변하지 않는다.
  -->
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el:'#app',
      data:{  
        message:'Hi',
      },
      //model을 사용해 바인딩한 경우 아래 코드는 주석처리해도 된다.
      methods: {
        onInputChange(event) {
          this.message = event.target.value
        }
      }
    })
  </script>
  
  
  <!--
  input태그에서 type="checkbox"일때 v-model="t/f값을 가지는 데이터"를 입력하면
  체크 여부에 따라 자동으로 t/f가 바뀐다.
  -->
  ```

  - `v-show`

  ```html
  <!--if는 false일 때 아예 렌더링 자체를 하지 않지만 show는 false라도 렌더링은 하고 보이지 않도록 설정을 한다.-->
  <!--style="display: none;"으로 설정되어 있다.-->
  
  <!-- 
    if는 평가(t/f)가 자주 바뀌지 않을 때 좋다. 
    초기 렌더링 코스트가 적다. 
  -->
  <div id="app">
    <p v-if="t">
      This is v-if with true
    </p>
    <p v-if="f">
      This is v-if with false
    </p>
  
    <!-- 
      show는 평가(t/f)가 자주 바뀔 때 좋다. 
      평가가 바뀌었을 때 다시 렌더링을 하는게 아니라 보여주기만 하면 되기 때문이다.
      즉, 토글 코스트가 낮다.
    -->
    <p v-show="t">
      This is v-show with true
    </p>
    <p v-show="f">
      This is v-show with false
    </p>
    <button @click="changeF">Change</button>
  </div>
  
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el:'#app',
      data:{  
        t:true,
        f:false
      },
      methods: {
        changeF() {
          this.f = !this.f  //!가 붙으면 부정의 의미다. 즉, 클릭을 하면 참/거짓이 바뀌게 된다.
        }
      }
    })
  </script>
  ```

  - `v-for`,`v-if`는 한 태그에 같이 쓰면 안된다.
    - 공식문서에서도 둘을 같은 태그에 쓰지 않을 것을 강하게 권고
    - `v-for`가 우선 순위를 가진다.



- methods

  - 본래 el, data와 같은 Vue의 인스턴스지만 내용이 길어져 따로 작성함

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VueJS</title>
  </head>
  <body>
  
    <div id="app">
      {{message}}
    </div>
  
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      const app = new Vue({
        el:'#app',
        data:{  
          message:'Hello'
        },
        methods:{
          alertWarning: function () {
            alert(this.message)
          },
          //Syntactic Sugar 버전(위 코드와 동일한 코드다), :function을 전부 생략 가능하다.
          alertMessage () {
            //Vue에서 this는 JS와는 다르게 동작한다. 단순히 app을 가리키는 것이 아니라 this 뒤에 오는
            //것을 가지고 있는 것을 자동으로 가리키게 된다. 재정렬과 관련이 있다.
            //아래의 경우 message를 가져오려 하므로 this는 data를 자동으로 가리키게 된다.
            alert(this.message)
          },
          changeMessage () {
            this.message = 'Bye'
          }
          //콘솔 창에 app.changeMessage()를 입력하면 hello가 bye로 바뀐다.
          //이후부터는 app.alertMessage (), app.alertWarning()을 해도 bye가 뜬다.
        }
      })
    </script>
  </body>
  </html>
  ```

  - this

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>photo</title>
  </head>
  <body>
    <div id="photo">
      <!--
        v-if를 쓴 이유는 아직 가져온 사진이 없을 때 버튼만 띄우기 위함이다.
        만일 아무 사진도 가져오지 않았다면 아래 catImgUrl을 null로 설정했으므로 false값을
        가지게 될 것이다.
      -->
      <img v-for="photoImgUrl in photoImgUrls" v-if="photoImgUrls" v-bind:src="photoImgUrl" alt="사진" width="300px" height="300px">
      <button v-on:click="getphotoImgUrl">사진 가져오기</button>
    </div>
  
  
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script> 
    <script>
      const photo = new Vue({
        el:'#photo',
        data:{
          photoImgUrls:[],
        },
        methods:{
          //photoCatImgUrl을 method를 정의한 것이기 때문에 function으로 정의
          photoCatImgUrl:function(){
            //console.log(this)  //Vue가 잡히고
            const API_URL = 'https://api.thecatapi.com/v1/images/search'
            axios.get(API_URL)
              /*
              .then(function(response){
                console.log(this)  //Window가 잡힌다.
                //this가 쓰인 함수는 익명함수로 자동으로 Window의 자식이 된다.
                this.photoImgUrl = response.data[0].url
              })
              */
              //this가 Vue를 가리키게 하기 위해선 아래와 같이 적어야 한다.
              /*
              method를 선언 할 때는 function을 쓰고
              callback을 넘길 때(함수가 인자로 들어갈 때)는 화살표 함수를 써야 한다.
              */
              .then((response) => {
                console.log(this) //Vue를 가리킨다.
                this.photoImgUrls.push(response.data[0].url)
              })
              .catch((err) => {console.log(err)})
          },
        },
      })
    </script>
  </body>
  </html>
  ```

  - Vue에서 form 태그를 쓸 경우 아래와 같이 methods에  `event.preventDefault()`을 실행시키는 메소드를 넣어줘야 한다. 
    - `preventDefault()`는 Vue에서 제공하는 기능이다.


  ```js
  methods:{
        signup:function(){
          event.preventDefault()
          this.$emit('submit-signup-data',this.signupData)
        },
      },
  ```



- Lodash: JS 유틸리티 라이브러리

  - JS는 수학적 처리에 약한데 이를 보완해 줄 수 있는 라이브러리다.

  > https://lodash.com/
    >
      > https://cdnjs.com/libraries/lodash.js/

  ```html
  <!--적당한 것을 골라 복사 후 붙여넣기-->
  <script>
      https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.15/lodash.min.js
  </script>
  ```
  ```html
  <!--예시.lodash로 구현한 lotto-->
  <!--아래 코드에서 _.가 붙은 것은 전부 lodash에서 가져온 것이다.-->
  
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Document</title>
  </head>
  <body>
    <div id="app">
      <button @click="getLuckySix">GET LUCKY 6</button>
      <ul>
        <li v-for="number in myNumbers">
          {{ number }}
        </li>
      </ul>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.15/lodash.min.js"></script> <!--lodash를 가져오고-->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      const app = new Vue({
        el: '#app',
        // [1..45] 에서 6개를 '랜덤'하게 뽑는다.
        data: {
          allNumbers: _.range(1, 46),
          myNumbers: []
        },
        methods: {
          getLuckySix() {
            this.myNumbers = _.sampleSize(this.allNumbers, 6)
            //JS의 이상한 정렬(JS기초 참고)때문에 아래와 같이 정렬을 해줘야 한다.
            this.myNumbers.sort(function(a, b) {
              return a - b
            })
          }
        },
      })
    </script>
  </body>
  </html>
  ```






# Vue 라이프 사이클

> 공식문서-Vue인스턴스 탭에 문서가 존재

- Life Cycle Hook
  - 많은 부분이 있지만 지금은 생성(created), 부착(mounted), 반응(updated)만 기억하면 된다.
  - 각기 Vue가 생성될 때, mount될 때 , 데이터가 변경될 때를 말한다.
  - 이들 라이프 사이클 훅은 우리 마음대로 이름을 정할 수 있는 것이 아니라 정해진 대로 작성해야 하며, 우리가 실행시키는 것이 아니라 자동으로 실행되는 것이다.
  - 일반적으로 초기화 이후(새로고침 혹은 페이지 첫 생성 시) ajax 요청을 보내기 가장 적합한 시점은 created다.




- 무한 스크롤

  - scrollmonitor 사용
  
  >https://cdnjs.com/libraries/scrollmonitor
  >
  >https://github.com/stutrek/scrollMonitor
  
  ```vue
  <!--무한 스크롤로 본 Vue의 라이프 사이클-->
  <!DOCTYPE html>
  <html lang="en">
  
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      .button-bottom {
        position: fixed;
        right: 20vw;  
        bottom: 20vh;
      }
    </style>
    <!--vw(viewport width),vh(viewport height)는 각기 화면 비율에 따라 높이와 너비를 조정하는 단위이다.-->
    <title>Scroller</title>
  </head>
  
  <body>
    <div id="app">
      <div v-for="photo in photos">
        <h5>{{ photo.title }}</h5>
        <img :src="photo.thumbnailUrl" :alt="photo.title">  <!--thumbnailUrl은 사진을 받아온 사이트에서 제공된 object이다.-->
      </div>
        
      <!--버튼을 클릭하면 최상단으로 이동-->
      <button @click="scrollToTop" class="button-bottom">^</button>
      
      <!-- 
        HTML 이 Vue 인스턴스와 연결된 순간부터(div#app 에 포함된 순간부터), 
        Life cycle hook 의 영향을 받는다. 
      -->
      <!--이 태그에 도착하면 바닥에 도착했다는 것을 감지-->
      <div id="bottomSensor"></div>
    </div>
  
  
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <!--무한 스크롤 구현을 위한 cdn-->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/scrollmonitor/1.2.0/scrollMonitor.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      const app = new Vue({
        el: '#app',
        data: {
          photos: [],
          page: 1,
        },
  
        methods: {
          //사진을 불러오기 위한 메소드
          getPhotos: function () {
            //요청을 보낼 때 본래 쿼리스트링으로 넘기던 값을 아래와 같이 변수에 담아서 넘긴다.
            const options = {
              params: {
                _page: this.page++, //x++는 일단 기존 x값을 쓰고, 그 후에 올린다는 뜻이다.
                _limit: 3,
              }
            }
            axios.get('https://jsonplaceholder.typicode.com/photos', options)
              .then(res => {
                console.log("사진을 가져 온다")
         		  //JS에서는 배열을 특이하게 합친다.
                //먼저 응답으로 받은 사진 배열(this.photos)과 후에 응답으로 받은 사진 배열(res.data)을 합치기
                this.photos = [...this.photos, ...res.data]
              })
              //.catch((err) =>  { console.error(err) } ) 아래와 같은 코드
              .catch(err => console.error(err))
          },
          
          addScrollWatcher: function () {
            const bottomSensor = document.querySelector('#bottomSensor')
            const watcher = scrollMonitor.create(bottomSensor)
            // watcher 가 화면에 들어오면 실행할 내용을 .enterVieport 내부에 적는다.
            watcher.enterViewport(() => {
                console.log('바닥에 도달')
              /*
              요청이 왔을 때 약간의 딜레이를 주는 코드
              요청이 계속 오면 서버가 과부화 될 수 있으므로 천천히 응답을 보낼 수 있도록 약간의 딜레이를 줄 필요가 있다.
              기다리는 것이므로 non-blocking하게 처리 된다.
              setTimeout은 callback 함수를 사용하므로 화살표 함수로 정의
              setTimeout(()=>{실행할 내용},숫자) - 숫자는 100에 0.1초다.
              */
              setTimeout(() => {
                this.getPhotos()
              }, 500)
            })
          },
          
          //버튼을 클릭했을 때 최 상단으로 이동하게 해주는 함수
          scrollToTop: function () {
            scroll(0, 0)
          },
          
          //스크롤을 내려야 새 사진을 받아오는데 표시하고 있는 사진이 화면을 다 채우지 못하면 스크롤이 생기지 않는다. 
          //따라서 스크롤이 생길 정도로 사진을 받아오도록 하는 코드를 작성해야 한다.
          loadUntilViewportIsFull: function () {
            const bottomSensor = document.querySelector('#bottomSensor')
            //아래 한 줄의 코드는 scrollmonitor에서 지정한 양식에 따라 쓴 것이다.
            const watcher = scrollMonitor.create(bottomSensor)
            
            //isFullyInViewport는 scrollMonitor에 작성된 프로퍼티로 watcher가 화면 안에 있는지 확인하는 프로퍼티다.
            //만일 화면 내부에 있을 경우 true를 반환하고 화면 내부에 없을 경우 false를 반환한다.
            if (watcher.isFullyInViewport) {  
              this.getPhotos()
            }
          },
        },
  	
          
        //아래 created, mounted, updated에 함수를 정의하지 않고 굳이 methods에 정의하고 아래에서 실행시키는 이유는 
        //함수를 각 함수가 실행되는 사이클 훅 아래에 작성하면 나중에 특정 함수를 수정할 일이 있을 때, 
        //해당 함수가 어디에 작성됐는지 찾기 힘들기 때문이다. 따라서 methods에 몰아서 작성하고 아래에서는 실행만 시킨다. 
          
        // created: 초기화 이후 AJAX 요청을 보내기 좋은 시점(Data, Methods 에 접근 가능.)
        //Vue 생성시에 개입해서 할 일(실행시킬 함수)을 정하는 것
        //이 코드의 경우 페이지를 처음 띄울 때 부터 사진을 출력하고자 하는 것이다.
        created: function () {
          console.log("생성됨")
          this.getPhotos()
        },
  
        // mounted: DOM 과 Vue 인스턴스가 연동이 완료되고 난 이후에 실행할 일들.
        mounted: function() {
          console.log("부착됨")
          this.addScrollWatcher()
        },
          /*
          만일 addScrollWatcher()를 created에서 실행시키면 제대로 작동하지 않을 것이다.
          created가 실행될 때는 아직 Dom과 Vue 인스턴스가 연동이 되지 못했을 때(mount 되지 못했을 때)이므로 
          아직 연동도 되지 않았는데 감지를 하려 하니 잘 작동하지 않는 것이다.
          mounted가 된 이후부터 정상적으로 작동한다.
          */
        
        // updated: data({}) 가 바뀌고 나서, 화면이 다시 렌더된 이후,
        updated: function() {
          this.loadUntilViewportIsFull()
        },
      })
    </script>
  </body>
  
  </html>
  ```



- computed와 watch
  - computed
    - create,update,delete에 해당하는 것은 method에, read에 해당하는 것은 computed에 정의한다.
    - computed 속성은 해당 속성이 종속된 대상(아래 예시의 경우 'message')이 변경될 때만 함수를 실행한다. 매번 새로 계산해야될 필요 없는 것은, 저장(캐싱)해놓고 쓴다(메소드는 호출하면 렌더링을 다시 할 때마다 항상 함수를 실행).
    - 함수를 선언하지만 쓸 때는 데이터 처럼 사용한다.
    - method에 정의할 때는 이름을 동사형으로, computed에 정의할 때는 함수지만 명사형으로 정의한다.
    - computed의 함수는 함수의 결과를 얻기 위해 사용하는 것이므로 반드시 return이 필요 하다.
  - 기본적으로는 getter함수(인자를 받지 않는 함수)지만 설정하면 setter함수로 쓸 수 있다. 한 메소드 안에서 `get`, `set` 을 나누어 정의하여 실행한다.
    - computed는 메소드 내부에 선언된 값이 변할 때 다시 실행된다. 아래의 경우 만일 message가 변경된다면 다시 실행 될 것.
  
  ```html
  <div id="example">
    <p> 메시지(m): "{{ printMessage() }}"</p>
    <p> 메시지(m): "{{ printMessage() }}"</p>
    <p> 메시지(m): "{{ printMessage() }}"</p> <!--함수로 사용-->
    <p> 메시지(c): "{{ printedMessage }}"</p> <!--데이터처럼 ()없이 사용-->
    <p> 메시지(c): "{{ printedMessage }}"</p>
    <p> 메시지(c): "{{ printedMessage }}"</p>
  </div>
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    var vm = new Vue({
      el: '#example',
      data: {
        message: '안녕하세요'
      },
      methods: {
        //동사형(print)로 정의
        printMessage: function () {
          console.log('methods 함수 실행')
          return this.message
        }
      },
      computed: {
        //명사형(printedMessage)으로 정의
        printedMessage: function () {
          console.log('computed 함수 실행')
          return this.message
        }
      }
    })
  </script>
  
  out
  methods 함수 실행  <!--methods에 정의된 함수는 3번 다 실행이 되지만-->
  methods 함수 실행
  methods 함수 실행
  computed 함수 실행 <!--computed에 정의된 함수는 1번만 실행이 된다.-->
  ```

  - watch
    - data 옵션의 key값들의 변경을  관찰하고 이에 반응한다.
    - 어떤 return을 바라지 않는다.
    - watch와 computed를 동시에 사용할 경우 watch가 먼저 실행되는 것으로 보인다.
    - watch는 object나 array 내부의 변수에 사용할 경우 먹지 않는데  이를 가능하게 해주는 watch의 속성 중 deep이 있다.
    - 또한 데이터가 변화할 때 뿐만 아니라 최초 1회 실행되어야 할 때가 있는데 이를 가능하게 해주는 것이 immediate이다.
  
  ```html
  <div id="app">
    <input type="text" v-model="newInput">
  </div>
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el:"#app",
      data:{
        newInput:''  //data 옵션의 key값인 newInput
      },
      watch:{
        //반드시 data 옵션의 key값과 동일하게 적어야 한다.
        //newInput이 변화할 때 마다 watch가 이를 감지하고 아래 함수가 실행된다.
        //newValue에는 현재 input창의 텍스트가 그대로 들어간다.
        //따라서 stupi에서 d를 치는 순간 아래 if문에 걸리게 되고 경고창을 띄운 후 input창이 초기화 된다.
        newInput:function (newValue) {
          console.log('실행됨')
          if (newValue.includes('stupid')){
            alert('나쁜 말은 하지 마세요')
            this.newInput=''
          }
        }
      }
    })
  </script>
  <!--
    stupid를 입력했다고 했을 때
    out
    실행됨이 6번 출력(함수가 6번 실행)되고 입력 창이 초기화 되면서 1번 더 출력되어 함수가 총 7번 실행된다.
  ```
  
  ```html
  <template>
    <div>
        <p>원본 메시지: "{{ message }}"</p>
        <p>역순으로 표시한 메시지: "{{ reversedMessage }}"</p>
    </div>
  </template>
  
  <script>
  export default {
      name: 'test',
      data(){
          return {
              message: '안녕하세요',
              reversedMessage: ''
          }
      },
      watch: {
          message: function (newVal, oldVal) {
              this.reversedMessage = newVal.split('').reverse().join('')
          }
      }
  }
  </script>
  ```
  
  ```javascript
  //computed와 watch 실행 순서
  data(){
      return{
          nickname:'',
          lenCheck:'',
      }
  }
  
  computed: {
      nameState() {
          if(this.nickname.length>=2){
              this.lenCheck=true
          }else{
              this.lenCheck=false
          }
      }
  },
      watch:{
          nickname(){
              console.log(this.lenCheck)
          }   
      }
      
  //만일 nickname에 v-model을 걸었을 때 2자 이상 입력하면 computed가 먼저 실행될 경우 watch에 입력된 console.log(this.lenCheck)가 true 를 반환하겠지만 false를 반환한다. 이는 computed가 실행되기 전에 watch가 먼저 실행되기 때문일 것이다, 정확한 결과는 그 반대의 경우(watch에서 값을 변경한 후 computed에서 확인)도 확인해 봐야 알 수 있을 것이다.
  ```



- filter

  - 기본적인 사용법은 JS의 필터와 동일

  ```html
  <div id="app">
    <p>{{ findOdd() }}</p>
  </div>
  
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script>
    const app = new Vue({
      el:"#app",
      data:{
        arr:[1,2,3,4,5,6]
      },
      methods:{
        findOdd:function(){
          //arr의 인자가 순서대로 x에 들어간다.
          const result = this.arr.filter((x) => {
            return x%2==1  //결과가 true인 x만 result에 담긴다.
          })
          return result //필터링이 끝난 result를 반환
        }
      }
    })
  </script>
  
  
  out
  [1,3,5]
  ```







# Vue 프로젝트

- SPA(Single Page Application)와 SFC(Single File Component)
  - SPA: 기존 웹 서비스는 요청시마다 서버로부터 리소스들과 데이터를 해석하고 화면에 렌더링하는 방식이다. SPA는 브라우저에 최초에 한번 페이지 전체를 로드하고, 이후부터는 특정 부분만 Ajax를 통해 데이터를 바인딩하는 방식
  - SFC: 파일 하나당 하나의 컴포넌트를 작성하여 컴포넌트 들을 모아서 하나의 페이지를 구성하는 것
    - Vue 인스턴스와 Vue 컴포넌트는 다르다.



- 프로젝트 생성하는 방법

  - vue/cli 설치(최초 1회)
    - vue-cli없이도 프로젝트 시작은 가능하다.

  ```bash
  $ npm install -g @vue/cli
  ```

  - VScode extention에서 `Vetur` 설치

  - 프로젝트 생성

  ```bash
  $ vue create 프로젝트명
  
  #입력하면 디폴트 모드와 설정 모드 중 하나를 선택해 엔터
  #완료되면  $ cd 프로젝트명, $ npm run serve을 실행해 달라는 문구가 뜬다.
  
  $ cd 프로젝트명
  $ npm run serve
  ```




- 구성

  - src

    - `main.js`가 분리해서 개발한 모든 파일을 관리하는 최상위 파일이다. mount를 담담
    - `App.vue`: component들의 관리자, 최종 component

    ```html
    <!--기본 구조-->
    <template>
      <div id="app">
    
      </div>
    </template>
    
    <script>
    export default {
      name: 'App',    //name을 쓰지 않아도 에러가 발생하지 않지만 디버깅 할 때 필요하다.
      components: {
        
      }
    }
    </script>
    
    <style>
    
    </style>
    ```

    - `components`: component들을 모아 놓은 폴더 
    - `assets`: 정적인 파일들(img 등) 모아 놓은 곳

  - public: `main.js`가 바라보는 최종 HTML파일이 있는 곳

  - `bable`: Vue 코드를 vanilla JS로 번역해준다.

  - `package.json`, `package-lock.json`: `requirements.txt`와 유사한 역할

    - `package.json`은 django의 `manage.py`와 같이 루트라는 것을 알 수 있는 파일이다.
    - 둘 다 Vue를 동작하게 하는 라이브러리들이 작성되어 있다. 라이브러리가 설치되면 이 두 파일에 추가된다.

  - `node_modules`: python의 venv에 해당, 패키지를 설치할 경우 실제로 코드가 들어가게 되는 디렉토리



- `.Vue`파일: `component`라 불리며 하나의 `component`는 `template`, `script`, `style`로 이루어져 있다.
  - 파일명은 UpperCamelCase로 작성한다.
  - VScode에서 `Vetur` 확장 프로그램을 설치했다면 폴더를 열고 `<`를 입력하고 탭을 누르면 html에서 `!`를 입력하고 탭을 누르는 것 처럼 기본 구조를 잡아준다.
  - 기본 구조는 html에 해당하는 `<template>`,  js에 해당하는 `<script>`,  css에 해당하는 `<style>`의 세 부분이다.
    - 셋 중 하나가 없다고 동작하지 않는 것은 아니다.
  
  ```vue
  <!--template 태그 안에는 하나의 root element만 존재해야 한다. 하나의 태그 안에 자식 태그가 있는 것은 괜찮지만 root에는 오직 하나의 태그만 존재해야 한다.-->
  <template>
    <div>{{message}}</div>
  </template>
  
  <script>
  export default {
      name:'First',  //name은 default로 넘어가므로 아무렇게나 지정해도 된다.
      /*
      Vue에서 데이터는 함수로 넘긴다.
      data를 객체가 아닌 함수로 넘기는 이유는 component를 재사용하므로 component는 계속 새로고침 없이 재사용되는데,
      data를 객체로 선언하면 계속 같은 값이 변하게 된다. 
      예를 들어 데이터를 a=1이라는 데이터가 있고 component가 사용될 때 마다 a+=1씩 해주는 함수를 작성했을 때,
      a를 객체로 만들었을 경우 매번 component가 재사용 될 때 마다 계속 +1씩 증가한다.
      반면에 a를 함수로 선언하면 component가 재사용 될 때 마다 a를 선언하는 함수도 다시 실행되면서 a의 복사본이 생기므로 
      몇 번을 재사용해도 a=2가 된다.
      */
      data: function(){ 
          return {
              message: '안녕하세요'
          }
      }
  }
  </script>
  
  <style>
  
  </style>
  
  
  <!--export default 내보내고 싶은 대상-->
  <!--default는 옵션이다. default로 내보내면 다른 곳에서 import할 때 이름을 마음대로 붙여서 사용할 수 있다. default는 내보낼 것이 하나일 때만 사용할 수 있다.-->
  
  <template>
    <div>
      <h1>Hello World</h1>
  
      </div>
  </template>
  
  <script>
  const arr1 = [1,2,3]
  const arr2 = [4,5,6]
  //export default는 내보낼 것을 지정하는 것이다.
  //아래에 작성하지 않은 것은 다른 파일에서 이 파일을 import해도 사용할 수 없다.
  //arr1은 내보냈으므로 다른 곳에서 import해서 사용이 가능하지만 arr2는 불가능하다.
  export default arr1  //객체를 내보내는 것이 아니므로 {}는 쓰지 않아도 된다.
  
  </script>
  
  <style>
  
  </style>
  ```





- `component`
  - 하나의 페이지를 구성하는 여러 요소들
  - 재사용이 용이하므로 반복되는 일을 할 때 컴포넌트를 사용하면 더 편하게 할 수도 있다.
  - Vue는 흔히 컴포넌트가 트리 형태로 중첩되어 사용된다.
    - 최소 컴포넌트를 지정했다면, 컴포넌트를 그룹으로 묶어서 부모 컴포넌트를 만들 수 있다.
  - 모든 Vue 컴포넌트는 Vue 인스턴스이기도 하다.
  - 한 가지 컴포넌트가 하나의 일을 한다는 원칙에 기반해서 컴포넌트 설계 - 단일책임원칙



- `App.vue`파일은 `root`바로 아래의 component로 직접 작성한 component는 이곳을 통해 출력한다.

  ```vue
  <template>
    <div id="app">
      <!--3.사용하기-->
      <First />
  	<!--
  	  태그 안에 /가 있으면 닫힘태그를 쓰지 않아도 된다
  	  혹은 아래와 같이 써도 동작은 한다.
  	  <First></First>
  	  그러나 컨벤션에 어긋나므로 하지 않는다.
  	-->
    </div>
  </template>
  
  <script>
  //1. import하기
  // import 변수이름 from 경로
  // 만일 import한 파일에서 export할 때 default 설정을 줬다면 설정하고 싶은 대로 설정하면 된다.
  // 그러나 일반적으로 import한 파일명과 동일하게 설정하는 것이 관례다.
  import First from './components/FirstComponent.vue'
  
  export default {
    name: 'App',
    components: {
      HelloWorld,
      //2. 등록하기
      //본래 object이므로 'key':value(e.g. 'First':first)형태로 적어야 하지만
      //JS의 object에서 key는 ''를 생략 가능하고, key와 value가 같으면 value는 안 적어도 된다.
      First,
    }
  }
  </script>
  
  <!--후략-->
  ```



- axios 사용

  - 설치

  ```bash
  $ npm i axios
  ```

  - 사용

  ```vue
  <!--.vue파일-->
  <!--전략-->
  
  <script>
  import axios from 'axios'   //import해서 사용한다.
  import A from './components/A' //직접 작성한 컴포넌트보다 위에 import하는 것이 컨벤션이다.
  import B from './components/B'
  
  
  export default {
    name: 'App',
  </script>
  <!--후략-->
  ```



- router, params, go
  - vue에서 다른 페이지로 이동시켜주는 3가지