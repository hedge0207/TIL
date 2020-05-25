# Vue.js 

> https://kr.vuejs.org/v2/guide/index.html

- What
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
    - 반응형은 데이터가 변경되면 이에 반응하여 연결된 DOM(HTML)이 업데이트 되는 것을 의미한다.
    - e.g. 페이스북에서 친구 차단을 했을 때 친구 목록, 게시글 페이지, 댓글 등에서 그 친구를 일일이 삭제해 주는 것이 아니라 반응형으로 모든 곳에서 삭제.



- Why
  - 배우기 쉽다.
  - UX 향상: 분절 없이 부드럽게 이어지는 웹 사이트
  - 프레임위크의 장점(DX 향상)
    - 선택과 집중이 가능
    - 유지/보수 용이
    - 커뮤니티와 라이브러리



- FaceBook에서 개발한 `React`도 동일한 작업을 해주는 프로그램이다.



- 시작 전 준비 사항

  - VS code에서 `Vetur` 설치, 코드 작성에 도움
  - Chrome에서 `Vue.js devtools` 설치-확장프로그램 관리-파일 URL에 대한 엑세스 허용 체크, 브라우저에서 볼 때 도움
  - 아래 코드를 추가

  > https://kr.vuejs.org/v2/guide/installation.html

  ```html
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  ```




- 기본형

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vue JS</title>
  </head>
  <body>
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
      //console.log(app.data.message)라고 쓰지 않고 console.log(app.message)라고만 적어도 알아서 app내의 data 내부의 message를 가져온다.
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

  

- interpolation

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

  - `v-if`

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
  <div id="app">
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
      <!--위 처럼 이벤트에 조건을 설정하는 것이 가능하다.-->
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
  
  