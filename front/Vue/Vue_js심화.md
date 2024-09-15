# 목차

- [Vue router](#Vue-router)
- [Youtube를 활용하여 페이지 만들기](#Youtube를-활용하여-페이지-만들기)
- [서버와 연결](#서버와-연결)
  - [사용자 인증](#사용자-인증)
- [믹스 인](#믹스-인)
- [이벤트 버스](#이벤트-버스)
- [기타 팁](#기타-팁)



# Vue router

- 모든 기능이 한 url에서 이루어지므로 특정 기능을 이용하기 위해 url을 입력하고 해당 기능으로 바로 이동하는 것이 불가능, 새로고침 없이 url을 설정할 수 있도록 해주는 것이 vue router다.
- url이 바뀔 때 마다 요청을 보내는 것은 아니다.
  - 최초로 페이지에 접속할 때 페이지에서 실행시켜야 하는 모든 기능에 대한 data를 다 받아온 후 url이 바뀔 때 마다 실행시키는 것이다. 
  - url에 #이 붙어 있으면 요청을 보내지 않았다는 것이다.
- `vue add router`: vue cli가 제공하는 vue router 구조를 잡아주는 명령어

```bash
$ vue add router

#commit을 하라고 하는데 완료가 되면 App.vue의 내용이 다 날아가기 때문이다. 따라서 프로젝트 생성하자마자 하는 것이 좋다.

#Use history mode for router? (Requires proper server setup for index fallback in production) (Y/n) 는 Y를 해준다. 이걸 y로 해줘야 뒤로가기를 눌러도 새로고침이 일어나지 않는다. URL 해시를 사용하여 URL이 변경될 때 페이지가 다시 로드되지 않도록 한다.

#완료되면 src폴더에 추가 폴더가 생기고 App.vue과 main.js에도 코드가 추가된다.
```



- `index.js`가 django의 urls.py의 역할을 하는 파일이다.
  - `index.js`에서 쓸 컴포넌트를 `views`에 작성
  - `views`에 작성된 컴포넌트를 다른 이름으로 페이지라고도 부른다. 
  - `views` 폴더에 작성된 컴포넌트에서 import 해서 쓸 컴포넌트를 `components`에 작성한다. 
  - 굳이 나누는 이유는 나중에 관리가 편하기 때문이다.

```js
//생성 후 아무 것도 수정하지 않은 상태
import Vue from 'vue'
import VueRouter from 'vue-router'   
import Home from '../views/Home.vue'   //from . import views와 유사한 코드
import About from '../views/About.vue' 

//src의 shortcut이 @다.
//from에서 확장자(.vue,js 등)는 생략할 수 있다.
//또한 index.js에서 가져올 때는 index.js라는 파일 자체가 상징적이므로 생략하고 불러올 수 있다.
//ex. import router from '../router/index.js'는 아래와 같이 쓸 수 있다.
// import router form @/router

Vue.use(VueRouter)

  //url_patterns와 유사한 코드
  //django와 달리 :로 variable routing을 표현한다.
  const routes = [
  {
    path: '/',    //이 경로로 접근하면
    name: 'Home',  //경로의 이름, django에서 처럼 url이름으로도 활용되지만 관리자 창에서 해당 component의 태그명으로 여기서 설정한 이름이 뜬다.
    component: Home  //(위에서 import한)Home이라는 component를 사용하겠다. 
  },
  {
    path: '/about',
    name: 'About',
  //routes 변수에 담긴 오브젝트를 일렬로 표현하면 다음과 같다. django의 url_pattern과 유사하다.
  //{path: '/', name: 'Home', component: Home},

    // 아래 코드는 최적화를 위한 코드, 아직 신경쓰지 않아도 된다.
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

//아래 코드가 뒤로가기를 눌러도 새로고침이 일어나지 않게 해주는 코드다.
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
```



- `App.vue`

```html
<template>
  <div id="app">
    <div id="nav">
      <!--
        <router-link>는 a태그와 달리 새로고침 없이 url을 이동시킨다.
        <a>태그를 사용한 것은 맞지만(관리자 창에 보면 a태그로 표시되고 router-link는 class로 들어가 있다)
	    JS를 통해 새로고침이 일어나지 않게 설계한 것이다.
        아래 링크를 눌러서 url이 바뀌는 것을 index.js가 인지하고 렌더링 해준다.
      -->
      <!--
        django와 딜리 url 경로 뒤가 아니라 앞에 /를 붙인다.
        이건 Vue가 특이한 것이 아니라 django가 특이한 것으로
        대부분의 경우에는 /를 경로 앞에 붙인다.
      -->
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>

    <!--
      아래 태그가 컴포넌트를 렌더링 하는 태그다.
      django의 {% block content %}와 유사하다.
	  url이 변경될 때 해당 경로에 해당하는 컴포넌트가 아래 태그의 위치에 띄어진다.
    -->
    <router-view/>
      
  </div>
</template>

<style>

</style>
```



- 순서
  - App.vue에 표시된 링크를 클릭한다.
  - index.js에서 url변화를 감지한다.
  - 해당 url경로에 정의된 컴포넌트(`views` 폴더에 정의된 컴포넌트)를 렌더링한다.
  - views에 정의된컴포넌트에 다른 컴포넌트(`components` 폴더에 정의된 컴포넌트)가 쓰였다면



- variable routing

  - `:`은 js 이외의 웹 개발에서도 variable routing에 일반적으로 사용되는 기호다.
  - `index.js`

  ```js
  //django에서는 varable routing을 할 때 <타입:변수명>으로 지정했지만 js에서는 그냥 :변수명을 사용한다.
  
  import Vue from 'vue'
  import VueRouter from 'vue-router'
  
  
  import HelloName from '../views/HelloName.vue'
  
  
  Vue.use(VueRouter)
  
  
  const routes = [
    { path: '/hello/:name', name: 'HelloName', component: HelloName },
  ]
  
  //후략
  ```

  - `views/HelloName.vue`
    - url에 입력된 변수(예시의 경우 name)는 route 내부의 params라는 곳에 저장되어 있다. 

  ```html
  <template>
    <div>
        <h1>Hello, {{ name }}</h1>
    </div>
  </template>
  
  <script>
  export default {
      name: 'HelloName',
      data: function() {
          return {
              name: this.$route.params.name,  //name이라고 뜨는 이유는 index.js에서 :name으로 정의했기 때문이다.
          }
      }
  }
  </script>
  
  <style>
  
  </style>
  ```

  

  - data를 GET요청으로 넘기는 방법(예시`ping-pong` 구현)

    - `index.js`

    ```js
    //전략
    
    import Ping from '../views/Ping.vue'
    import Pong from '../views/Pong.vue'
    
    Vue.use(VueRouter)
    
    const routes = [
      { path: '/ping', name: 'Ping', component: Ping },
      { path: '/pong', name: 'Pong', component: Pong },
    ]
    
    //후략
    ```

    - `views/ping.vue`

    ```html
    <!--ping.vue-->
    <template>
      <div>
          <h1>Ping</h1>    
          <!--enter를 누르면 sendToPong 함수를 실행, inputText변수를 양방향 연걸-->
          <input @keyup.enter="sendToPong" v-model="inputText" type="text">
      </div>
    </template>
    
    <script>
    export default {
        name: 'Ping',
        data: function() {
            return {
                inputText: '',
            }
        },
        methods: {
            sendToPong: function() {
                // route가 아닌 router라는 것에 주의
                // push라는 명령어를 통해 이루어진다(django의 redirect와 유사).
                // 원래 GET 요청은 url에 쿼리 스트링(?로 시작)에 담겨서 넘어가게 된다. 따라서 아래와 같이 쿼리 스트링을 적어서 넘겨준다.
                this.$router.push(`/pong?message=${this.inputText}`)
            }
        }
    }
    </script>
    
    <!--후략-->
    ```

    - `views/pong.vue`

    ```html
    <template>
      <div>
        <h1>Pong</h1>
        <h2>{{ messageFromPing }}</h2>
      </div>
    </template>
    
    <script>
    export default {
        name: 'Pong',
        data: function() {
          return {
            //ping에서 넘어온 정보는 route의 qurey의 message에 담겨 있다.
            messageFromPing: this.$route.query.message, //message인 이유는 ping에서 쿼리 스트링을 설정할 때 message라고 썼기 때문이다.
          }
        }
    }
    </script>
    
    <style>
    
    </style>
    ```

  

- url에 설정한 name을 활용하는 방법

  - 추가 url이 없을 경우
  
  ```html
  <template>
    <div id="app">
      <div id="nav">
          <!--바인드를 걸어준 후 to에 객체를 넘겨준다.-->
        <router-link :to="{ name: 'Ping' }">Ping</router-link>
      </div>
      <router-view/>
    </div>
  </template>
  
  <!--후략-->
  ```
  
  - 추가 url이 있을 경우
  
  ```html
  <template>
    <div>
        <h1>Ping</h1>
        <input @keyup.enter="sendToPong" v-model="inputText" type="text">
    </div>
  </template>
  
  <script>
  export default {
      name: 'Ping',
      data: function() {
          return {
              inputText: '',
          }
      },
      methods: {
          sendToPong: function() {
              // this.$router.push(`/pong?message=${this.inputText}`)  //위에서 이와 같이 쓴 코드는 아래와 같이 바꿀 수 있다.
              this.$router.push({ name: 'Pong', query: { message: this.inputText } })
          }
      }
  }
  </script>
  ```





- bootstrap 적용
  - CDN을 `public/index.html`에 붙여넣는다.
  - 결국 최종적으로 렌더링 되는 파일이 `index.html`이므로 여기다만 적으면 적용이 된다.



- `props` & `emit`

  - 상위 컴포넌트(부모)와 하위 컴포넌트(자식) 간의 데이터 전달 방식
  - props: 부모는 props를 통해 자식에게 데이터를 전달
    - 모든 prop들은 부모와 자식 사이에 단방향으로 내려가는 바인딩 형태를 취한다. 이 말은 부모의 속성이 변경되면 자식 속성에게 전달되지만, 반대 방향으로는 전달되지 않는 다는 것을 의미
    - props로 전달되는 데이터는 전달받은 컴포넌트의 `data`오브젝트에 작성하지 않는다. props를 전달한 부모 컴포넌트의 `data` 오브젝트에만 작성하면 된다.
    - 따라서 data를 정의할 때는 해당 데이터를 필요로하는 컴포넌트들의 가장 가까운 공통 부모에게 정의하는 것이 좋다.
    - 부모 컴포넌트의 데이터가 새로 갱신되는 경우에 자식 요소의 모든 prop들은 최신 값으로 새로고침된다.
  - emit: 자식이 부모의 데이터를 변경하는 등의 일이 필요할 때 emit을 통해 부모에게 events를 보내 부모에게 메시지를 보낸다.
  - 데이터는 부모에서 자식관계에서만 전달가능하다.
    - 까마득히 아래 있는 하위 컴포넌트가 까마득히 위에 있는 상위 컴포넌트의 데이터를 변경할 경우 데이터 흐름의 일관성이 사라지고 어디서 데이터가 변하고 있는지 추론하기 어려워진다.
    - 따라서 부모가 자식에게 데이터를 props로 내려 주는 것은 가능하지만 자식은 부모의 데이터를 바꾸거나 접근할 수 없다. 자식은 오직 이벤트를 통해 요청만 할 수 있다. 요청을 받은 부모는 `v-on` 을 통해 이벤트 이름과 동작(methods)를 정의한다.
    
    - 다른 말로 하면 모든 컴포넌트 인스턴스는 자체 격리 된 범위가 있기 때문에 중첩된 컴포넌트의 관계에서 하위 컴포넌트는 상위 컴포넌트를 직접 참조할 수없으며 그렇게 해서도 안된다.
  
  ```js
  //index.js
  import Vue from 'vue'
  import VueRouter from 'vue-router'
  import Parent from '../views/Parent.vue'
  
  Vue.use(VueRouter)
  
    const routes = [
    {
      path: '/parent',
      name: '부모',
      component: Parent
    },
  ]
  //후략
  ```
  
  ```html
  <!--views/Parent.vue-->
  
  <template>
    <div class="parent">
        <h1>부모 컴포넌트</h1>
        <!-- P1. prop 이름="내용"(propFromParent="parentMsg") -->
        <!-- 
            만일 아래 있는 data나 computed와 vind해서 넘기고 싶으면  
          :prop 이름="내용"(:propFromParent="parentMsg")
          아래의 경우 data에 정의된 parentMsg를 보내려고 하는 것이므로 :를 써준다.
        -->
        <Child @hungry="onHungrySignal" :propFromParent="parentMsg"/>
        <!-- E2. emit @customEvent 를 듣고, 그다음 일을 한다(@hungry="onHungrySignal"). -->
    </div>
  </template>
    
  <script>
    
  import Child from '../components/Child.vue'
    
  export default {
      name: 'Parent',
      data() {
          return {
              parentMsg: '부모에서 내리는 메시지',
          }
      },
      components: {
          Child,
      },
      methods: {
          // E3. 지정된 메소드를 실행시킨다.
          //자식에게 받은 인자 2개(예시의 경우 '햄버거','피자')
          onHungrySignal(menu1, menu2) {
              console.log(menu1, menu2)
          }
      }
  }
  </script>
    
  <style>
      .parent {
          border: 3px solid red;
          margin: 3px;
          padding: 3px;
      }
  </style>
  ```
  
  ```html
  <!--components/Child.vue-->
    
  <template>
    <div class="child">
        <h2>자식 컴포넌트</h2>
        <!-- P3. 부모에게 받은 데이터를 사용한다. -->
        {{ propFromParent }}
        <!--button을 클릭하게 되면 부모에게 에빈트가 방출(emit)-->
        <button @click="sendHungrySignal">배고파!</button>
      </div>
  </template>
  <script>
  export default {
      name: 'Child',
      // P2. 부모에게 받은 props 등록(반드시 Object로 써야지 유효성 검사(Validation) 가능)
      // 부모에게 받은 data가 해당 타입이 맞는지에 대해 유효성 검사를 하는 것이다.
      // 아래에서 확인할 수 있듯 props로 전달되는 데이터는 data로 쓰지 않는다.
      props: {
          //key값으론 변수명, value로는 type명을 쓴다.
          propFromParent: String,
      },
      methods: {
          sendHungrySignal() {
              // E1. emit 부모한테 이벤트(시그널) 방출
              //this.$emit('이벤트명','데이터1','데이터2',...)
              this.$emit('hungry', '짜장면', '짬뽕') //custom event
          }
      }
  }
  </script>
    
  <style>
  .child {
      border: 3px solid blue;
      margin: 3px;
      padding: 3px;
  }
  </style>
  ```
  
  - `App.vue`에서는 별도의 import 없이 `<router-view/>` 태그를 통해 emit과 props를 하면 된다.




- `<style>`을 특정 class나 선택자가 없이 태그로 줄 경우 자식 컴포넌트에 작성해도 모든 컴포넌트에 적용된다.
  - scoped 속성을 줄 경우(`<style scoped>`) 컴포넌트마다 독립적인 스타일링이 가능해진다.
  - 그렇다고 클래스를 지정해 주지 않아도 된다는 것은 아니다. 클래스는 항상 지정해줘야 한다.
  - 클래스를 써주지 않았을 경우 Vue가 해당 스타일링을 적용 받을 것들을 일일이 찾아야 하기 때문에 클래스를 써주는 것이 성능 면에서  더 좋다.











# Youtube를 활용하여 페이지 만들기

- 유튜브에서 `api key`와 `api url`을 받아서 직접 만든 페이지에 유튜브 동영상이 뜨게 하는 것이 목적 



- 환경변수 관리(`.env`)

  - 뷰 CLI로 생성하여 애플리케이션을 제작하게 되면 기본적으로 웹팩을 사용한다. 따라서, 모드에 따라 웹팩의 설정이 달라진다.

  - Vue CLI는 3가지 모드를 가지고 있다. 

    - development: 개발 용도, `npm run serve` 명령어로 실행할 때의 모드
    - production: 배포 용도, `npm run build` 명령어로 실행할 때의 모드
    - test: 테스트 용도, `npm run test:unit` 명령어로 실행할 때의 모드


  - 위의 3가지 모드 이외에 직접 모드를 커스텀 해서 사용할 수 있다.

    - 정의

    ```javascript
    //package.json
    
    "scripts": {
      //기존의 3가지 모드
      "serve": "vue-cli-service serve",
      "build": "vue-cli-service build",
      "lint": "vue-cli-service lint",
      
      //직접 커스텀한 모드
      "goguma":"vue-cli-service serve --mode goguma"
      //vue-cli-service serve까지는 그냥 입력하면 되며 --mode goguma는 goguma 모드로 사용하겠다는 뜻이다.
    },
    ```

    - 실행

    ```bash
    #아래와 같이 실행하면 goguma 모드로 실행된다.
    $npm run goguma
    ```

    

  

  - CLI에서는 프로젝트 루트 폴더에 아래와 같은 규칙으로 환경 변수 파일을 생성할 수 있다.

    - .env: 모든 모드에 적용되는 환경 변수 파일
    - .env.local: 모든 모드에 적용되나 개인만 사용하는 파일
    - .env.[mode]: 특정 모드에 해당하는 환경 변수 파일
    - .env.[mode].local: 특정 모드에 해당하지만 개인이 사용하는 파일

  

  - 예시

    - `NODE_ENV`: 애플리케이션 모드를 가리키는 변수(development, production, test)
    - `BASE_URL`: `vue.config.js` 파일에 정의된 `publicPath`의 값과 동일한 변수

    ```
    //.env.development
    
    VUE_APP_ANIMAL="cat"
    ```

    ```
    .env.goguma
    
    NODE_ENV="goguma"
    VUE_APP_ANIMAL="dog"
    ```

    - 위와 같이 각기 다른 모드에 대한 환경 변수 파일이 있을 때 `npm run serve`로 실행하면 아래와 같은 결과가 나온다.

    ```javascript
    console.log(env.proecess.VUE_APP_ANIMAL)
    
    //cat
    ```

    - `npm run goguma`로 실행하면 아래와 같은 결과가 나온다

    ```javascript
    console.log(env.proecess.VUE_APP_ANIMAL)
    
    //dog
    ```

    

  

  - 각 환경 변수 파일의 우선 순위는 모드에 따라 달라진다.

    - 예를 들어 배포 환경일 때는 `.env.production`의 우선권이 `.env.development`의 우선권 보다 높고, 개발 환경일 때는 그 반대이다.

  - API KEY는 관리를 철저히 해야 한다. github에 올라가지 않도록 gitignore로 관리를 해줘야 한다.

    - `.gitignore`에 최초 생성시에 `.env.local`파일이 포함되어 생성된다.

    - `.env.local`파일에 API KEY를 관리하면 된다.

    - 프로젝트 폴더 내부(최상위 폴더)에 `.env.local`파일 생성 후 API KEY를 입력한다.

      ```
      VUE_APP_API_KEY=AbCdEfGhIjK7LMNop9QrSTU1VWx7Yz
      
      -시작은 반드시 VUE_APP_로 시작해야 하며 = 앞뒤에 공백이 있어선 안된다.
      ```

    - API KEY를 입력했던 파일에 아래와 같이 입력한다.

      ```js
      const API_KEY = process.env.VUE_APP_API_KEY
      ```

    - 위 과정을 거친 후 serve를 한번 껐다 켜야한다.

    - 이렇게 한다고 완전히 숨길 수 있는 것은 아니지만 적어도 github에서는 숨길 수 있다.

  

- 구조(총 5개의 컴포넌트) 

  ```
  App.vue--searchBar
  	   --YoutubeList--YoutubeListItems
  	   --YoutubeDetail
         
  
  searchBar: 검색창
  YoutubeDetail: 영상 보기
  YoutubeList: 영상 목록 보기
  YoutubeListItems: 영상 상세 정보
  ```



- 코드
  - `App.vue`

  ```html
  <template>
    <div id="app" class="container">
        <!--search-videos이벤트가 발생하면 searchVideos메소드를 실행-->
        <SearchBar @search-videos="searchVideos"/>
      <div class="row">
        <!--selectedVideoId, selectedVideoTitle을 자식 컴포넌트에게 넘겨준다.-->
        <YoutubeDetail :selectedVideoId="selectedVideoId" :selectedVideoTitle="selectedVideoTitle"/>
        <!--영상 리스트를 띄워주는 컴포넌트-->
        <YoutubeList :videos="videos" @select-video="selectVideo"/>
      </div>
    </div>
  </template>
  
  <script>
  //$npm i axios를 통해 axios를 설치 한 후 import
  import axios from 'axios'
  
  //App.vue에서 사용할 컴포넌트들을 import
  import SearchBar from './components/SearchBar'
  import YoutubeList from './components/YoutubeList'
  import YoutubeDetail from './components/YoutubeDetail'
  
  //google 클라우드 플랫폼-새 프로젝트 생성-좌측 상단 햄버거-API 및 서비스-대시보드-
  //-API및 서비스 사용 설정-YouTube Data API v3-사용 설정-사용자 인증 정보 만들기-
  //-API선택, API를 호출할 위치는 웹브라우저(자바스크립트)선택, 엑세스할 데이터는 공개 데이터 선택
  //-어떤 사용자 인증 정보가 필요한가요? 클릭하면 API KEY를 발급 받을 수 있다.
  //발급 받은 이후부터는 사용자 인증 정보 탭에서 확인 할 수 있다.
  const API_KEY = process.env.VUE_APP_API_KEY
  
  //https://developers.google.com/youtube/v3/docs/search/list에 접속하면 HTTP 요청 url이 있다.
  const API_URL = 'https://www.googleapis.com/youtube/v3/search'
  
  
  export default {
    name: 'App',
    components:{
      SearchBar,
      YoutubeList,
      YoutubeDetail,
    },
    data: function(){
      return {
        videos: [],
        selectedVideoId: '',
        selectedVideoTitle:'',
      }
    },
    methods: {
      searchVideos: function(keyword){
        // axios를 통해 요청을 보내서 videos를 변경
        // 아래 경로는 관리자 도구-network-preview에서 확인 할 수 있다. 응답으로 json 오브젝트가 온다.
        // params 오브젝트에 들어가는 실제 내용은 아래와 같은 쿼리 스트링이다.
        //'?KEY=AbCdEfGhIjK7LMNop9QrSTU1VWx7Yz&part=video&part=snippet&q=임의의 값'
        axios.get(API_URL, {
          params:{
            key: API_KEY,
            type: 'video',
            part: 'snippet',
            q:keyword,
          },
          //화살표 함수 사용
          //응답으로 온 json 오브젝트의 response.data.items에 요청 받은 내용이 들어 있다.
        }).then((response)=>{
          this.videos = response.data.items
          //요청 받은 내용이 오지 않았을 경우 콘솔 창에 error를 출력
        }).catch((error)=>{
          console.error(error)
        })
      },
      selectVideo:function(videoId, videoTitle){
        this.selectedVideoId=videoId
        this.selectedVideoTitle=videoTitle
      },
    }
  }
  </script>
  
  <!--후략-->
  ```
  
  - `SearchBar.vue`
  
  ```html
  <template>
    <div class="row">
        <!--입력 받을 keyword 데이터에 v-model 설정, enter가 입력되면 searchVideos함수 실행-->
        <input type="text" v-model="keyword" @keypress.enter="searchVideos" placeholder="동영상을 검색하세요">
    </div>
  </template>
    
  <script>
  export default {
      name:'SearchBar',
     data:function(){
        return {
          keyword: '',
        }
      },
      methods: {
        searchVideos:function(){
          // trim은 좌우측 공백을 제거하는 함수, 만일 공백을 제거했을 때 빈 문자열이라면 입력된 것이 없다는 뜻이므로 알림창을 띄운다.
          if (!this.keyword.trim()){
            alert('검색어를 입력해 주세요.')
          }else{
            //공백이 아니라면 emit을 실행
            //search-videos이벤트를 실행하고 keyword.trim()을 인자로 넘긴다.
            this.$emit('search-videos', this.keyword.trim())
          }
        },
      },
  }
  </script>
    
  <style>
    input{
      width:75%;
      margin-bottom: 10px;
    }
  </style>
  ```
- `YoutubeList.vue`
  
  ```html
  <template>
  <ul class="list-group col-8">
        <!--v-for를 사용할 경우 key값을 줘야 하는데 video.etag가 유일한 값을 가지므로 key의 역할을 할 수 있다.-->
        <!--select-video 이벤트가 실행되면 selectVideo 메소드 실행-->
        <YoutubeListItem v-for="video in videos" :key="video.etag" :video="video" @select-video="selectVideo"/>
    </ul>
  </template>
  
  <script>
  import YoutubeListItem from './YoutubeListItem'
  
  export default {
      name:'YoutubeList',
      components:{
          YoutubeListItem,
      },
      props: {
          videos: Array,
      },
      methods:{
          selectVideo: function(videoId,videoTitle){
              //select-video이벤트를 실행하고 자식 컴포넌트인 YoutubeListItems에서 인자로 받은 videoId,videoTitle를 부모 컴포넌트로 넘긴다.
              //select-video는 위에서도 썼는데 자식 컴포넌트와 부모 컴포넌트의 이벤트명이 겹쳐도 상관 없다.
              this.$emit('select-video',videoId,videoTitle)
          },
      },
  }
  </script>
  <!--후략-->
  ```
  
  - `YoutubeListItem.vue`
  
  ```html
  <template>
    <li class="list-group-item" @click="selectVideo">
      <!--
        :src="video.snippet.thumbnails.default.url"로 써도 되지만 길어지므로 아래에 computed에 함수를 선언해서 짧게 써준다.
        videoTitle, videoDescription도 마찬가지로 그냥 video.snippet.title, video.snippet.description로 써도 되지만 짧게 써주기 위해 computed에 써준다.
      -->
      <div class="media">
        <img :src="thumbnailUrl" :alt="thumbnailUrl" class="mr-3">
          <div class="media-body">
            <h5 class="mt-0 mb-1" v-html="videoTitle"></h5>
            <p>{{ videoDescription }}</p>
          </div>
      </div>
    </li>
  </template>
  
  <script>
  export default {
      name:'YoutubeListItem',
      // 부모 컴포넌트에서 받은 videos를 props에 저장
      props: {
        video: Object,
      },
      computed: {
        thumbnailUrl: function () {
          return this.video.snippet.thumbnails.default.url
        },
        videoTitle: function(){
          return this.video.snippet.title
        },
        videoDescription: function(){
          return this.video.snippet.description
        },
      },
      methods:{
        selectVideo: function () {
          //아래 video.id.videoId는 개발자도구-network-preview에서 볼수 있다.
          this.$emit('select-video',this.video.id.videoId, this.videoTitle)
        },
      },
  }
  </script>
  
  <style>
  li{
    cursor: pointer;
  }
  li:hover{
    background-color: #eee;
  }
  </style>
  ```
  - `YoutubeDetail.vue`
  
  ```html
  <template>
    <div class="col-4 align-center">
        <!--
          영상을 클릭하지 않았을 때도 기본 영상이 뜨는 것을 막기 위해 v-if를 사용, 
          selectedVideoId가 지정되지 않았다면 빈 문자열일 것이므로 false가 되어 영상이 뜨지 않는다.
  
          iframe은 bootstrap-embeds에 있는 태그이다. iframeUrl은 굳이 함수로 선언하지 않고 
          `https://www.youtube.com/embed/${this.selectedVideoId}`를 그대로 적어도 되지만
          코드를 간결하게 작성하기 위해 computed에 작성해서 쓴다.
        -->
        <iframe 
          v-if="selectedVideoId" 
          :src="iframeUrl"
        ></iframe>
        <!--
          v-text로 적을 경우 특수문자가 제대로 표시되지 않는 문제(아스키코드로 나온다)가 있어 v-html을 사용
          v-html에 보안이슈가 있긴 하지만 아래의 경우 보안에 문제 될 것이 없다는 것이 확실하므로 사용한다.
        -->
        <h4 class="mt-0 mb-1" v-html="selectedVideoTitle"></h4>      
    </div>
  </template>
  
  <script>
  export default {
      name:"YoutubeDetail",
      //부모에게 받은 selectedVideoId, selectedVideoTitle를 props에 저장
      props:{
        selectedVideoId: String,
        selectedVideoTitle:String,
      },
      computed:{
        iframeUrl: function(){
          return `https://www.youtube.com/embed/${this.selectedVideoId}`
        },
      }
  }
  </script>
  
  <style>
  .align-center{
    display:flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  </style>
  ```







# 서버와 연결

> django 등을 활용하여 구축한 서버와 Vue를 연결

## 사용자 인증

- 로그인

  - django에서 설정한 URL로 username과 password를 담아서 POST 요청을 보낸다.

  - 쿠키에 token을 저장해야 한다.

    >  https://www.npmjs.com/package/vue-cookies

    - 설치

      ```bash
      $ npm i vue-cookies
      ```

    - `main.js`에 아래 코드를 추가(아무 데나 작성해도 되지만 일반적으로 main.js에 작성한다.)

      ```js
      import Vue from 'vue'
      import App from './App.vue'
      import router from './router'
      import VueCookies from 'vue-cookies'  //이 코드와
      
      Vue.use(VueCookies)  //이 코드를 추가
      
      Vue.config.productionTip = false
      
      new Vue({
        router,
        render: h => h(App)
      }).$mount('#app')
      ```

  - 예시

  ```js
  //전략
  import axios from 'axios'
  
  //django의 서버 주소, 반복해서 사용하므로 변수에 저장한다.
  const DURL = 'http://localhost:8000'
  
  export default {
    name: 'App',
    data() {
      return {
        isLoggedIn: false,  //로그인 상태인지 확인하기 위한 변수
        errorMessages: null,
        tmp_token:''
      }
    },
  
    methods: {
        /*
        cookieAndIsloggedin(token){
            this.$cookies.set('auth-token', token)
            this.isLoggedIn = true
        }
        */
        login(loginData) {
              //POST요청을 보내야 하므로 post를 써준다.
            	//.post(요청을 보낼 url, body에 담을 data, header에 담을 데이터)의 형식으로 작성한다. header에 담을 것이 없으므로 작성하지X
              axios.post(DURL + 'django에서 설정한 url', loginData)
                //이 요청에 대한 응답의 data에는 {key:'토큰값'} 형태의 오브젝트가 온다.
                .then(res => {
                  //이 토큰에 대한 정보를 저장해야 토큰을 활용할 수 있는데 아래와 같이 할 경우 새로고침을 하면 tmp_token이 다시 ''값으로 초기화 					된다. 따라서 아래 방법으로는 토큰을 저장할 수 없다.
                  //this.token=res.data.key
                  
                  //토큰을 로그아웃하기 전까지 저장하기 위해서 쿠키를 활용한다.
                  //쿠키는 documnet.cookie를 통해 접근 가능하다.
                  
                  //쿠키에 토큰값을 저장하기 위해서는 아래와 같이 작성해야 한다(token은 cookie의 key에 들어갈 변수명으로 아무거나 해도 된다).
                  //document.cookie = "token=토큰값"
                  
                  //보다 축약하면 아래와 같이 쓸 수 있지만 이 역시 불편하다.
                  //document.cookie = "token="+res.data.key
                  
                  //vue-cookies를 사용하면 훨씬 간략하게 작성 가능하다(auth-token은 cookie의 key에 들어갈 변수명으로 아무거나 해도 된다).
                  //set은 vue-cookies가 정의한 함수로 위와 같이 타이핑하지 않아도 cookie에 key:토큰값 형태로 저장되게 해준다.
                  //$는 vue-cookies제작자가 정한 기호이다.
                  this.$cookies.set('auth-token', res.data.key)
                  this.isLoggedIn = true //로그인 상태로 바꾼다.
                  //위 두 코드는 반복해서 쓸 것이 예상되므로 함수로 만들어서 써도 된다.  
                  //this.cookieAndIsloggedin(res.data.key) 위에 주석 처리한 함수, 토큰 정보를 인자로 받는다.
                    
                  //this.$router.push(경로)는 django의 redirect와 같은 역할을 한다.
                  this.$router.push({ name: 'Home' })
                })
                //에러 내용을 보고자 한다면 console.log(err.response)와 같이 보면 된다(catch의 첫 인자를 일반적으로 error, err로 정의한다). 
                //catch의 첫 인자의 response에 자세한 에러 내용이 담겨있다.
                .catch(err => this.errorMessages = err.response.data)
            },
      },
      mounted() {
      // .isKey는 vue-cookies에서 제공하는 함수로 cookie 에 auth-token 이 존재하는가 체크, 있으면 true, 없으면 false를 반환
      //토큰은 로그인시 발급되고 로그아웃시 삭제되므로 토큰이 존재한다는 것은 로그인 상태라는 뜻이다. 따라서 토큰 유무에 따라 로그인 유무를 판별할 수 		있고 아래가 그 코드다.
      //주의할 점은 회원가입을 할 경우 토근값을 리턴하는데 회원가입 로직을 짤 때 자동으로 쿠키에 토큰이 저장되도록 한다면 회원가입만 해도 isLoggedIn		이 true가 될 수 있다.
      this.isLoggedIn = this.$cookies.isKey('auth-token')
    },
  }
  
  //후략
  ```




- 로그 아웃

  ```html
  <template>
    <div id="app">
      <div id="nav">
        <router-link to="/">Home</router-link> |
        <!--컴포넌트는 이벤트를 들을 때 자식 컴포넌트에서 올라온 이벤트를 듣도록 설정되어 있다. 따라서 현재 컴포넌트에 설정한 이벤트를 듣게 하려면 			.navive를 붙여줘야 한다. router-link도 컴포넌트이므로 현재 컴포넌트에서 이벤트를 듣고자 한다면 .native를 붙여야 한다.-->
        <router-link v-if="isLoggedIn" to="/accounts/logout" @click.native="logout" >Logout</router-link>>
      </div>
      <router-view/>
    </div>
  </template>
  
  
  <script>
  //각종 변수명은 위 로그인 코드에 작성된 것을 그대로 쓴다고 가정
  //전략
  logout() {
        //Postman으로 요청을 보낼 때와 마찬가지로(django_part3 참고) header에 Authorization:Token 토큰값의 형태로 데이터를 보내야 한다.
        //따라서, 보다 간결하게 보내기 위해 아래와 같이 변수에 저장한다. 굳이 object안에 object의 형태로 보내는 이유는 이렇게 보내야하기 때문이다.
        const config = {
          headers: {
              //.get은 ue-cookies에서 제공하는 함수로 key(auth-token)에 해당하는 토큰값을 가져오는 함수다.
            'Authorization': `Token ${this.$cookies.get('auth-token')}` 
          }
        }
        //위 로그인 코드에서 보았듯 .post(요청을 보낼 url, body에 담을 data, header에 담을 데이터)의 형식으로 작성하는데 위에서 정의한 config는 body가 아닌 header에 담을 데이터이다. 따라서 body에는 보낼 것이 없지만 3번째 위치에 넣기 위해 body에 담을 data가 들어가는 두 번째 자리에 null값을 채워준다.
        axios.post(SERVER_URL + '/rest-auth/logout/', null, config)
          // .then(() => {})
          .catch(err => console.log(err.response))
          .finally(() => {
            //.remove역시 vue-cookies에서 제공하는 함수로 토큰을 제거하는 것이다. auth-token은 위(로그인 코드)에서 token을 담을 때 auth-token에 담았기에 써준 것이지 고정적인 변수가 아니다.
            this.$cookies.remove('auth-token')
            this.isLoggedIn = false
            this.$router.push({ name: 'Home' })
          })
      },
  </script>
  <!--후략-->
  ```



- 회원가입

  ```js
  //각종 변수명은 위 로그인 코드에 작성된 것을 그대로 쓴다고 가정
  //로그인 코드와 유사하다.
  
  //전략
  signup(signupData) {
         axios.post(SERVER_URL + '/rest-auth/signup/', signupData)
          .then(res => {
            this.$cookies.set('auth-token', res.data.key)
            this.isLoggedIn = true
          })
      	//errorMessages는 위 로그인 코드에 작성된 변수이다.
          .catch(err => this.errorMessages = err.response.data)
      },
  //후략
  ```

  

- loginrequired 구현하기: 아래 문서 참고하여 `index.js`에 코드 작성

  > https://router.vuejs.org/kr/guide/advanced/navigation-guards.html

  ```js
  //from에는 온 페이지가, to에는 가려는 페이지가 담긴다. 각기 찍어보면 오브젝트 형태로 name이라는 ket의 value로 가려는 페이지의 name이 담겨 있다.
  router.beforeEach((to, from, next) => {
    const publicPages = ['Login', 'Signup', 'Home', 'List']  // Login 안해도 되는 것들
    const authPages = ['Login', 'Signup']  // Login 되어있으면 안되는 것들
    
    //publicPages.include(to.name)은 publicPages에 to.name이 담겨 있다는 것이다.
    //따라서, !publicPages.includes(to.name)는 publicPages에 to.name이 담겨있지 않다는 것이다.
    //to.name에 어떤 값이 담겨 있는가에 따라 authRequired에 true 또는 false 값이 담기게 된다.
    const authRequired = !publicPages.includes(to.name)  // 로그인 해야 함.
    const unauthRequired = authPages.includes(to.name)  // 로그인 해서는 안됨.
    const isLoggedIn = !!Vue.$cookies.isKey('auth-token')
    
    //로그인 해서는 안되는 페이지에 로그인된 상태로 들어가려 할 경우 메인 화면으로
    if(unauthRequired && isLoggedIn) {
      next('/')
    }
      
    //로그인 해야하는 페이지에 로그인 하지 않은 상태로 들어가려 할 경우 login 페이지로'
    if (authRequired && !isLoggedIn){
        next({name:'Login'})
     //아니면 본래 가려 했던 페이지로
    }else{
        next()
    }
    //위 코드는 삼항연산자로 아래와 같이 표현 가능하다.
    //authRequired && !isLoggedIn ? next({ name: 'Login'}) : next()
  ```



- 백 엔드에서 유저 정보를 받아올 수 없을 경우 현재 유저 로그인한 유저 정보를 활용하는 방법

>  https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage 참고





# 믹스 인

- 함수를 재사용하기 위한 기능으로 한 컴포넌트에 정의된 함수를 다른 컴포넌트에서 사용할 수 있게 해준다.
- HTML, CSS 는 믹스 인을 사용하지 않으며 순수 JS만 믹스 인 한다.
  
  - 가능은 하지만 사용해선 안된다.
- 믹스 인과 믹스인을 사용하는 컴포넌트에 동일한 이름의 함수, 데이터를 선언할 경우 컴포넌트에 선언된 값을 우선하여 병합한다.

- 예시

  - myMixin.js

  ```js
  let myMixin = {
      data:function(){     //data에 정의한 변수 뿐 아니라 props에 정의한 변수도 사용이 가능하다.
          return{
              msg:'mixin!!'
          }
      },
      created() {
          console.log('mixin')
      },
      methods:{
          onClick(){
              this.data++;  //사용하려는 컴포넌트에 정의된 데이터를 사용 가능하고
          }
      }
  };
  export default myMixin;
  ```

  - app.vue

  ```html
  <template>
  <!--App.vue-->
      <div id="app">
          <div id="sub" @click="onClick" @contextmenu.prevent="onRightClick">{{data}}</div>
      </div>
  </template>
  
  <script>
      import myMixin from './components/myMixin' //import하고
  
      export default {
          mixins: [myMixin],  //등록한 후
          name: 'app',
          created(){
              console.log(this.data)
              console.log(this.msg)   //믹스 인에 저장된 데이터도 사용 가능하다.
          },
          data: function () {
              return {
                  data: 10,
              }
          },
          methods: {
              onRightClick(){
                  alert(this.msg)
              }
          }
      }
  </script>
  
  <style>
  
  </style>
  ```

  



# 이벤트 버스

- 이벤트 버스를 사용해야 하는 이유
  - Vue를 사용하다 보면 형제 컴포넌트 사이에 데이터를 주고 받아야 할 일이 빈번하게 생긴다.
  - 그때마다 부모 컴포넌트로 올린 후 다시 형제 컴포넌트에 내리는 과정을 거치면 지나치게 복잡해진다.
  - 이벤트 버스는 부모 컴포넌트를 거치지 않고도 형제 컴포넌트 사이에 데이터를 주고 받을 수 있게 해준다.



- 예시1

  > https://github.com/hedge0207/web/tree/master/Vue/vue_eventbus

  - main.js

  ```javascript
  //꼭 main.js에 하지 않아도 된다.
  import Vue from 'vue'
  import App from './App.vue'
  
  Vue.config.productionTip = false
  
  // new Vue()를 통해 새로운 Vue 인스턴스를 생성하고 이를 내보낸다(export)
  export const eventBus = new Vue()
  
  new Vue({
    render: h => h(App),
  }).$mount('#app')
  ```

  - Sender.vue

  ```vue
  <template>
    <div>
        <button @click="sendEventBus">클릭하세요</button>
    </div>
  </template>
  
  <script>
  import { eventBus } from '../main'  //main.js에서 export한 eventBus를 오브젝트 형태로 import 한다.
  export default {
      data(){
          return {
  
          }
      },
      methods:{
          sendEventBus(){
              // $emit을 통해 보내고자 하는 데이터와 이벤트 명을 보낸다.
              // 부모 컴포넌트에 데이터를 보낼 때도 $emit을 사용한다.
              // 마찬가지로 Vue 인스턴스인 evnetBus를 부모 컴포넌트처럼 사용하는 것이다.
              eventBus.$emit("eventWasSended", "잘 받으셨나요?")
              console.log("이벤트를 실은 버스가 출발했습니다.")
          }
      }
  }
  </script>
  //후략
  ```

  - Receiver.vue

  ```vue
  <template>
    <div>{{receivedMessage}}</div>
  </template>
  
  <script>
  import { eventBus } from "../main"
  export default {
      data(){
          return {
              receivedMessage: "아직 못 받았어요!!"
          }
      },
      created(){
          //eventBus에서 온 신호를 듣는다.
          eventBus.$on('eventWasSended', (msg)=>{
              this.receivedMessage = msg
          })
      }
  
  }
  </script>
  
  <style>
  
  </style>
  ```

  

- 예시2

  - 새로운 Vue 인스턴스를 생성하는 것이므로 아래와 같이 하는 것도 가능하다.

  - main.js

  ```javascript
  import Vue from 'vue'
  import App from './App.vue'
  
  Vue.config.productionTip = false
  
  //기존 방식
  export const eventBus = new Vue()
  
  //확장된 방식
  export const evnetBusTwo = new Vue({
    methods:{
      changeMessage(msg){
        this.$emit('MessageWasChanged',msg)
      }
    }
  })
  
  new Vue({
    render: h => h(App),
  }).$mount('#app')
  
  ```

  - Sender.vue

  ```vue
  <template>
    <div>
        <button @click="sendEventBus">클릭하세요</button>
        <button @click="changeMessage">메시지를 바꾸려면 클릭하세요</button>
    </div>
  </template>
  
  <script>
  import { eventBus,evnetBusTwo } from '../main'  //main.js에서 export한 eventBus를 오브젝트 형태로 import 한다.
  export default {
      data(){
          return {
  
          }
      },
      methods:{
          //기존 방식
          sendEventBus(){
              eventBus.$emit("eventWasSended", "잘 받으셨나요?")
              console.log("이벤트를 실은 버스가 출발했습니다.")
          },
          //확장된 방식
          changeMessage(){
              evnetBusTwo.changeMessage("메시지가 바뀌었나요???")
          }
      }
      
  
  }
  </script>
  
  <style>
  
  </style>
  ```

  - Receiver.vue

  ```vue
  <template>
    <div>
        <div>{{receivedMessage}}</div>
        <div>{{changedMessage}}</div>
    </div>
  </template>
  
  <script>
  import { eventBus,evnetBusTwo } from "../main"
  export default {
      data(){
          return {
              receivedMessage: "아직 못 받았어요!!",
              changedMessage: "아직 안 바뀌었어요!!"
          }
      },
      created(){
          //기존 방식
          eventBus.$on('eventWasSended', (msg)=>{
              this.receivedMessage = msg
          })
          //확장된 방식
          evnetBusTwo.$on('MessageWasChanged', (msg)=>{
              this.changedMessage=msg
          })
      }
  
  }
  </script>
  
  <style>
  
  </style>
  ```

  



# 기타 팁

- 자주 사용하는 값들을 저장하여 사용하는 방법

  - src폴더의 하부 폴더 하나 생성(이름은 마음대로 정해도 된다).
  - 생성한 폴더 내부에 `.js` 파일 생성(역시 이름은 마음대로 정해도 된다).
  - 이후 해당 파일에 자주 쓰는 값들을 아래와 같이 정리

  ```js
  //src/폴더명/파일명.js
  모든 이름은 마음대로 지정하면 된다.
  export default {
      BACK_URL: 'http://localhost:8000',
      BACK_ROUTES: {
          signup: '/rest-auth/signup/',
          login: '/rest-auth/login/',
          logout: '/rest-auth/logout/',
      }
  }
  ```

  - 사용할 때는 아래와 같이 import 해서 사용하면 된다.

  ```html
  <!--전략-->
  <script>
      
  import server from @/폴더명/파일명.js  //import하고
  
  export default {
      methods:{
          signup: function(signupData){
              //아래와 같이 적으면 위 파일에서 정의한대로 들어가게 된다.
              axios.post(server.BACK_URL+server.BACK_ROUTES.singup,signupData)
              .then((response)=>{
                  this.setCookiesAndLogin(response.data.key)
                  this.$router.push('/login')
              })
              .catch(()=>{
                  this.$alert("다시 입력 해주세요.");
              })
          },
      }
  }
  </script>
  <!--후략-->
  ```
  



- Vue는 template에 쓰인 data의 변화가 있을 때마다 자동으로 re-rendering한다.
  - 만일 re-rendering되지 않는다면 이는 data의 변화가 없기 때문이다.