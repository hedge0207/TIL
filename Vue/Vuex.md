# 목차

- [Vuex 기초](#Vuex-기초)
- [Vuex로 사용자 인증 구현](#Vuex로-사용자-인증-구현)
- [Vuex로 게시글 생성 및 조회 구현](#Vuex로-게시글-생성-및-조회-구현)





# Vuex 기초

> https://vuex.vuejs.org/kr/

- Vue.js 애플리케이션에 대한 상태 관리 패턴 + 라이브러리, 모든 컴포넌트에 대한 중앙 집중식 저장소 역할
  - 그 동안은 emit과 props를 통해 부모자식 간에 정보를 주고받았다. 그러나, 지나치게 중첩된 컴포넌트를 통과하는 prop는 장황할 수 있으며 형제 컴포넌트에서는 작동하지 않는다는 문제가 있다.
  - 이를 해결해 주는 것이 `Vuex`로, 이는 데이터 혹은 요청을  자식 혹은 부모가 아닌 중계소로 보내, 중계소에서 해당 데이터 혹은 요청을 받을 곳으로 바로 보내주는 것이다. 
  - 데이터 관리가 보다 쉬워지지만 배우기 어렵다는 단점이 존재한다.



- 관리자 도구의 Vue탭 내부의 2번째 탭은 Vuex가 실행되는 것을 보여준다.



- 사용법

  - Vuex를 불러오기

  ```bash
  $ vue add vuex
  
  #router와 유사하게 여러 파일에 새로운 코드가 추가되고 새로운 폴더, 파일이 생성된다.
  ```

  - 성공적으로 불러오면 `main.js`에 아래 코드가 추가된다.

  ```js
  import Vue from 'vue'
  import App from './App.vue'
  import router from './router'
  import store from './store' //추가된 코드
  //실제 import하는 것은 store 폴더가 아닌 store 폴더 내부의 index.js파일이므로 아래와 같이 써야한다. 
  //import store from './store/index.js'
  
  //그럼에도 이와 같이 쓴 이유는 다음과 같다.
  //첫째, import할 때 뒤의 확장자는 생략 가능하다.
  //import store from './store/index'
  //둘째, import 구문에서 파일명이 생략되면 자동으로 index파일을 탐색한다(index는 특수한 파일명으로 import문이 자동으로 탐색해준다). 
  
  
  Vue.config.productionTip = false
  
  new Vue({
    router,
    store,  //추가된 코드
    render: h => h(App)
  }).$mount('#app')
  
  ```

  

- 구성

  - `src/store/index.js`

  ```js
  import Vue from 'vue'
  import Vuex from 'vuex'
  import axios from 'axios'
  
  Vue.use(Vuex)
  
  //기본 구성은 state,mutations,modules뿐으로 getters는 추가한 것이다.
  export default new Vuex.Store({
    
    // data 의 집합, 중앙 관리할 모든 데이터(혹은 상태)
    state: {
    },
      
    
    // state(data) 를 (가공해서 혹은 그대로)가져올 함수들, computed와 동일
    getters: {
    },
      
    
    // state 를 변경하는 함수들(state를 변경하는 코드는 mutations에 작성해야한다)
    // mutations가 아닌 곳에서도 state를 변경하는 것이 가능하지만 그렇게 해선 안된다. vuex의 큰 장점 중 하나는 action-	mutations-state로 이어지는 state의 변경 내역 추적이 가능하다는 것인데 다른 곳에서 수정할 경우 이러한 vuex의 장점이 	사라지는 것이므로 명백한 안티 패턴이다.
    // 모든 mutation 함수들은 동기적으로 동작하는 코드여야 한다.
    // commit 을 통해 실행한다.
    // mutations에 작성한 함수들중 상수나 매우 중요한 함수는 함수명을 전부 대문자로 정의하기도 한다.
    // mutations에 정의한 한 함수에서 mutations에 정의한 다른 함수를 호출할 수는 없다.
    mutations: {
    },
      
    
    // 범용적인 함수들을 작성(범용적인 함수를 작성하기에 state, mutations 등 위에 있는 모든 것들에 접근이 가능하다), 	mutations 에 정의한 함수를 actions 에서 실행 가능하다.
    // 비동기 로직은 actions 에서 정의한다.
    // dispatch 를 통해 실행한다. actions에 정의된 함수에서 actions에 정의된 다른 함수를 실행시키는 것이 가능하며 이 때에도 dispatch를 사용한다.
    actions: {
    },
      
    
    //당장은 몰라도 된다.
    modules: {}
  })
  ```



- `v-model`은 해당 컴포넌트의 data 중 하나와  연결이 되는데 이 경우 다른 코드를 Vuex로 옮기는 것에 비해 까다로울 수 있다.

  > https://vuex.vuejs.org/kr/guide/forms.html

  - Vuex를 엄격히 적용하고자 하는 경우 위의 공식 문서를 참고해서 하면 된다.
  - 그러나 굳이 Vuex에 옮겨적지 않고 개별 컴포넌트에 그대로 두는 것도 하나의 방법일 수 있다.
    - 일반적으로 v-model과 연결된 데이터는 local한 데이터이기에 굳이 Vuex로 옮기지 않아도 된다.



- 사용 예시

  - 파일 구조
  
```
  App-A-Aa-Ca
  	 -Ab
     -B-Ba-Cb
  	 -Bb
```

  - Ca에서 Cb까지 데이터를 보내려면 Ca-Aa-A-App-B-Ba-Cb의 여러 단계를 거쳐야 한다.
    
    - Vuex를 사용하면 이를 훨씬 편하게 보낼 수 있다.
    
    ```html
    <!--Cb.vue-->
    <template>
      <div>
          <h1>Ca</h1>
          <div>{{Aac}},Ca</div>
          <button @click="sendToAa">Send To A</button>
          <button @click="sendToCb">Send To Cb</button>
      </div>
    </template>
      
    <script>
    export default {
        name: 'Ca',
        data: function(){
            return {
                CaToA:'message from Ca to A',
                CaToCb:'message from Ca to Cb',
            }
        },
        props:{
            Aac:String,
        },
        methods:{
            sendToAa(){
                this.$emit('sendToAa',this.CaToA)
            },
            sendToCb(){
                this.$emit('sendToCb',this.CaToCb)
            },
        }
    }
    </script>
      
    <style>
      
    </style>
    ```
    
    

  



- 실제 활용 코드

  - 아래 예시 코드는 실제로 동작하지는 않는다. 중간 중간 수정하지 않은 것도 있고 모든 component파일을 가져온 것도 아니며 모든 코드를 옮긴 것이 아니라 이해에 필요한 부분만 작성한 것이므로 동작하는 완전한 코드를 보고자 한다면 gitlab을 참고(교수님 코드)할 것
  - `App.vue`

  ```html
  <template>
    <div class="container">
      <!--
        <SearchBar @input-change="onInputChange" />
  	-->
      <SearchBar/>
      <div class="row">
        <!--
  	    만일 VideoDetail.vue의 코드를 아래와 같이 수정했다면 내려줄 필요가 없다.
          <VideoDetail :video="selectedVideo"/>
  	  -->
        <VideoDetail/>
        <!--
          <VideoList @video-select="onVideoSelect" :videos="videos" />
  	  -->
        <VideoList/>
      </div>
    </div>
  </template>
  
  <script>
  /*
  import axios from 'axios'
  */
  import SearchBar from './components/SearchBar.vue'
  import VideoList from './components/VideoList.vue'
  import VideoDetail from './components/VideoDetail.vue'
  
  /*
  const API_KEY = process.env.VUE_APP_YOUTUBE_API_KEY
  const API_URL = 'https://www.googleapis.com/youtube/v3/search'
  */
  
  export default {
    name: 'App',
    components: { SearchBar, VideoList, VideoDetail },
    /*최종 수정이 완료되면 아래 코드 전부가 필요 없는 코드가 된다.
    data() {
      return {
        //아래 3개의 데이터를 index.js의 state로 옮긴다.
        inputValue: '',
        videos: [],
        selectedVideo: null,
      }
    },
    methods: {
      onInputChange(inputText) {
        //data를 변경하는 로직이므로 mutations에 적어야 한다.
        this.inputValue = inputText
        axios.get(API_URL, {
          params: {
            key: API_KEY,
            part: 'snippet',
            type: 'video',
            q: this.inputValue,
          }
        })
          .then(res => { 
            res.data.items.forEach(item => {
              const parser = new DOMParser()
              const doc = parser.parseFromString(item.snippet.title, 'text/html')
              item.snippet.title = doc.body.innerText
            })
            //data를 변경하는 로직이므로 mutations에 적어야 한다.
            this.videos = res.data.items
          })
          .catch(err => console.error(err))
      },
      onVideoSelect(video) {
        //data를 변경하는 로직이므로 mutations에 적어야 한다.
        this.selectedVideo = video
      }
    }
    */
  }
  </script>
  ```

  - `VideoDetail.vue`

  ```html
  <template>
    <!--
      <div v-if="video" class="col-lg-8">
      index.js 수정이 완료되면 위와 같이 적지 않고 아래와 같이 적는다
    -->
    <div v-if="$store.state.selectedVideo" class="col-lg-8">
      <div class="embed-responsive embed-responsive-16by9">
  
        <!--
            <iframe 
              class="embed-responsive-item"
              :src="videoUrl" 
              allowfullscreen
            ></iframe>
  	  -->
        <!--
  		  원래 위와 같이 쓰지만 getters에서 받아온 것을 쓰고자 한다면 아래와 같이 쓰면 된다. ':src=' 부분을 바꿔준다
            <iframe 
              class="embed-responsive-item"
              :src="$store.getters.videoUrl"
              allowfullscreen
            ></iframe>
  	  -->
        <!--computed와 getters를 매핑하면 위보다 간결하게 아래와 같이 쓸 수 있다.-->
        <iframe 
          class="embed-responsive-item"
          :src="videoUrl" 
          allowfullscreen
        ></iframe>
      </div>
        
        
      <div class="details">
         
        <!--version1, 원래 코드
  		<h4 v-html="video.snippet.title"></h4>
          <p>{{ video.snippet.description }}</p>
  		위 코드는 부모에게 받아온 video 정보를 활용하는 코드이고, 아래 코드는 index.js의 state에 저장된 video 정보를 활용하는 코드이다.
  	  -->
          
        <!--version2, state를 활용한 코드
        	<h4 v-html="$store.state.selectedVideo.snippet.title"></h4>
        	<p>{{ $store.state.selectedVideo.snippet.description }}</p>
       	위 코드는 props나 emit을 거치지 않는다는 점에서는 간편하지만 너무 장황하다는 단점이 있으므로 이 코드 역시 getters에 저장한 후 아래처럼
  		불러와서 사용한다.
  	  -->
        
        <!--version3, getters를 활용한 코드
          <h4 v-html="$store.getters.videoTitle"></h4>
          <p>{{ $store.getters.videoDescription }}</p>
  		확실히 짧아지긴 했지만 더 줄이는 방법이 있다. 아래에서 cumputed를 getters에 옮겨 적었다고 지우는 것이 아니라 computed와 getters를 매핑		   하는 것이다.
  	  -->
        <!--computed와 getters를 매핑 3)코드로 작성-->
        <h4 v-html="videoTitle"></h4>
        <p>{{ videoDescription }}</p>
          
      </div>
    </div>
  </template>
  
  <script>
  //computed와 getters를 매핑 1)import
  import { mapGetters } from 'vuex' //computed와 getters 매핑을 위해 import(공식문서에 코드가 있다.) 
  //아래와 같이 한 번에 import도 가능하다.
  //import {mapGetters, mapState, mapMutatsions, mapActions} from 'vuex'
      
  export default {
      name: 'VideoDetail',
      props: {
        video: Object,
      },
      
      //computed는 Vuex에서 getters와 유사하므로 getters에 쓸 수 있다. 따라서 computed의 내용을 getters에 옮겨 적는다.
      /*
      computed: {
        videoUrl() {
          return `https://youtube.com/embed/${this.video.id.videoId}`
        }
      }
      */
      
      //computed와 getters를 매핑 2)매핑하기, 아래 코드를 적기 위해서는 위에서 import를 해줘야 한다.
      computed:{
          ...mapGetters([   //...mapGetters([매핑하고자 하는 변수들])
          'videoUrl',
          'videoTitle',
          'videoDescription'
          
          //아래와 같이 key값을 주고 key값을 대신 쓸 수도 있다.
          //...mapGetters([   //...mapGetters([매핑하고자 하는 변수들])
          //url: 'videoUrl',
          //title: 'videoTitle',
          //description: 'videoDescription'
          //위와 같이 하면 {{url}}과 같이 작성 가능하다.
        ])
      }
  }
  </script>
  ```

  - `VideoListItem.vue `

  ```html
  <template>
    <!--
  	클릭하면 onVideoSelect가 실행되고 emit되어 App.vue의 onVideoSelect함수가 실행된다.
  	이렇게 단계를 거치지 않고 한 번에 고쳐지게 하기 위해서는 표시한 코드를 추가
    -->
    <li @click="onVideoSelect" class="video-list-item list-group-item">
        <img :src="thumbnailUrl" class="mr-3" alt="youtube-thumbnail-image">
        <div class="media-body">
          {{ video.snippet.title }}
        </div>
    </li>
  </template>
  
  <script>
  export default {
      name: 'VideoListItem',
      
      props: {
          video: Object,
      },
      
      methods: {
          onVideoSelect() {
              /*
              this.$emit('video-select', this.video)
              */
  
              //mutations는 commit을 통해 실행되므로 아래에 commit을 써준다.
              //첫 번째 인자에는 mutations에서 실행시킬 함수를, 두번째 인자에는 넘길 데이터를 적으면 된다.
              //이제 onVideoSelect함수가 실행되면 index.js의 setSelectedVideo함수가 실행된다.
              this.$store.commit('setSelectedVideo', this.video)
          }
      },
      computed: {
          thumbnailUrl() {
              return this.video.snippet.thumbnails.default.url
          }
      }
      
  }
  </script>
  ```

  - `searchBar.vue`

  ```html
  <template>
    <div class="search-bar">
        <!--
         <input @keypress.enter="onInput">
         마찬가지로 enter를 눌렀을 때 emit이 수행되는 것이 아니라 바로 inputValue를 변경
        -->
        <input @keypress.enter="$store.commit('fetchVideos')">
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex' //actions와 매핑을 위한 코드, 공식문서 참고
  //만일 mutations와 매핑하고 싶다면 아래와 같이 적으면 된다.
  import { mapMutations } from 'vuex'
      
  export default {
      name: 'SearchBar',
      methods: {
          /*emit하는 것이 아니라
          onInput(event) {
              this.$emit('input-change', event.target.value)
          */
          //actions에 정의한 함수를 사용
           ...mapActions([
              'fetchVideos'
          }
      },
  }
  </script>
  ```

  - `src/store/index.js`

  ```js
  import Vue from 'vue'
  import Vuex from 'vuex'
  
  //기존에 App.vue에서 실행하던 axios관련 코드를 아래 actions에 정의했으므로 import해야 한다.
  import axios from 'axios'
  
  Vue.use(Vuex)
  
  //기존에 App.vue에서 실행하던 코드를 실행하기 위해 이것도 옮겨온다.
  const API_KEY = process.env.VUE_APP_YOUTUBE_API_KEY
  const API_URL = 'https://www.googleapis.com/youtube/v3/search
  
  
  //관리자 도구에서 Vue탭을 보면 넘겨받은 데이터,이벤트 등이 payload에 담겨서 넘어오게 된다. 아래에 payload라고 적은 것은 인자 이름이므로, payload라고 적는 것 보다는 실제 payload에 담겨 넘어온 것을 명시적으로 알 수 있도록 하는 것이 더 낫다.
  export default new Vuex.Store({
  
    state: {
      inputValue: '',
      videos: [],
      selectedVideo: null,
    },
  
    getters: {
      //getters는 mutations와 마찬가지로 반드시 state를 첫 인자로 받는다.
      //state를 첫 인자로 받는 이유는 getters의 존재 이유가 state(data)의 가공이기 때문이다.
      videoUrl(state){
        //return `https://youtube.com/embed/${this.video.id.videoId}`
        //원 코드는 위와 같지만 여기서는 this를 쓸 수 없으므로 아래와 같이 수정해서 적는다.
        return `https://youtube.com/embed/${state.selectedVideo.id.videoId}`
      },
      videoTitle(state){
        return state.selectedVideo.snippet.title
      },
      //화살표 함수로는 아래와 같이 표현 가능하다. 화살표함수는 사용을 지양하는 것이 좋으나 이 경우 공식문서에서도 화살표 함수를 사용하므로 써도 된다.
      //videoTitle: state => state.selectedVideo.snippet.title,
      videoDescription(state){
        return state.selectedVideo.snippet.description
      },
    },
  
    mutations: {
     	//django의 views.py에 작성한 함수들이 무조건 request를 첫 인자로 받는 것과 마찬가지로 mutations는 반드시 첫 인자로 state를 받는다.
      //단 js는 인자를 적지 않아도 작동하므로 굳이 적지 않아도 되지만 적어주는 것이 좋다.
      //state를 첫 인자로 받는 이유는 mutations의 존재 이유가 state(data)의 변경이기 때문이다.
  
      //inputValue를 변경하는 함수
      //inputValue에는 아래 actions의 fetchVideos함수에서 넘어온 event.target.value가 들어가게 된다.
      setInputValue(state, inputValue) {
        state.inputValue = inputValue
      },
  
      //videos를 변경하는 함수
      //videos에는 아래 actions의 fetchVideos함수에서 넘어온 res.data.items가 들어가게 된다.
       setVideos(state, videos) {
        state.videos = videos
      },
  
      //selectedVideo를 변경하는 함수
      //payload보다는 payload에 담겨온 것이 video이므로 video라고 적는 것이 더 명시적이지만 처음 배우는 것이므로 payload라고 적는다.
      setSelectedVideo(state, payload){
          state.selectedVideo = payload
      },
      
    },
  
    actions: {
      //원래 actions 내부에 정의하는 모든 함수는 첫 번째 인자로 context를 받는데 commit과 state는 모두 context내부의 요소다.
      //context를 console창에 찍어보면 감이 올 것이다.
      //fetchVideos(context , event)와 같이 적어도 상관 없다. 단, 일부 코드를 수정해야 한다. -1),2),3)
      //event listener에 의해 실행되는 함수들은 두 번째 인자로 event를 넘기는데 넘어온 event는 payload에 담겨서 온다.
      fetchVideos({ commit, state } , event) {
        // 1. inputValue 를 바꾼다.
        //inputValue는 state에 정의된 변수이고 state를 변경하는 것은 mutations에서만 해야 하므로 actions에서 직접 변경하는 것이 아니라 			mutations에서 해당 코드를 실행시키는 코드를 작성한다.
        commit('setInputValue', event.target.value)  //1)context.commit('setInputValue', event.target.value)
          
        // 2. state.inputValue를 포함시켜 요청을 보낸다. 본래 App.vue에서 하던 일을 이제 이 함수에서 한다.
        axios.get(API_URL, {
          params: {
            key: API_KEY,
            part: 'snippet',
            type: 'video',
            q: state.inputValue, //2)context.state.inputValue
          }
        })
          .then(res => { 
            res.data.items.forEach(item => {
              const parser = new DOMParser()
              const doc = parser.parseFromString(item.snippet.title, 'text/html')
              item.snippet.title = doc.body.innerText
            })
            
            // 3. state.videos 를 응답으로 바꾼다.
            // 1과 마찬가지 이유로 mutations에서 해당 코드를 실행시키는 코드를 작성한다.
            commit('setVideos', res.data.items)  //3)context.commit('setVideos', res.data.items)
          })
          .catch(err => console.error(err))
      }
    },
    modules: {}
  })
  ```

  

- state, getters,mutations,actions 모두 매핑이 가능하다.

  - state는 data에 mapping이 가능은 하지만 주로 computed 내부에 매핑한다.
  - actions는 methods에 매핑한다.







# Vuex로 사용자 인증 구현

- auth-token을 state에 구현

  ```js
  import Vue from 'vue'
  import Vuex from 'vuex'
  
  import cookies from 'vue-cookies'  //1)import하고
  import axios from 'axios'
  
  import router from '@/router'
  import SERVER from '@/aaa/bbb'
  
  Vue.use(Vuex)
  
  export default new Vuex.Store({
    state: {
      // auth
   	//auth-token의 경우 아래와 같이 쓸 수도 있으나
      //authToken:document.cookies.auth-token
      
      //아래와 같이 쓰는 것이 권장된다.
      authToken: cookies.get('auth-token'), //2)사용
      // articles
      articles: []
    },
  //후략
  ```

- 로그인 구현

  - `Login.vue`

  ```html
  <template>
    <div>
      <h1>Login</h1>
      <div>
        <label for="username">username:</label>
        <input v-model="loginData.username" id="username" type="text" />
      </div>
      <div>
        <label for="password">password:</label>
        <input v-model="loginData.password" id="password" type="password" />
      </div>
      <div>
        <!--state에 정의되지 않고 특정 컴포넌트에만 있는 local한 변수를 index.js에 있는 함수에 인자로 넘기려 한다면 아래와 같이 하면 된다.-->
        <!--아래에서 mapping한 login 함수를 실행하면 아래 data에 정의된 loginData가 인자로 넘어가게 된다.-->
        <!--loginData는 state에 정의하지 않고 local변수로 남겨뒀는데 그 이유는 v-model과 연결되어 있고 local한 변수이기 때문이다.-->
        <button @click="login(loginData)">Login</button>
      </div>
    </div>
  </template>
  <script>
  import { mapActions } from 'vuex' //mapping하기 위해 import
  export default {
    name: "LoginView",
    data() {
      return {
        loginData: {
          username: null,
          password: null
        }
      }
    },
    //index.js에 작성한 login함수와 mapping
    methods: {
      ...mapActions(['login'])
    }
  };
  </script>
  ```

  - `index.js`

  ```js
  import Vue from 'vue'
  import Vuex from 'vuex'
  
  import cookies from 'vue-cookies'
  import axios from 'axios'
  
  import router from '@/router'  //router를 import해야 한다.
  import SERVER from '@/aaa/bbb' //server_url을 저장해 놓은 파일
  
  Vue.use(Vuex)
  
  export default new Vuex.Store({
    state: {
      authToken: cookies.get('auth-token'),
    },
      
      
    getters: {
      //화살표 함수 에서는 화살표가 return을 대신하므로 isLoggedIn 함수는 true나 false 값을 리턴한다.
  	isLoggedIn: state => !!state.authToken,
      config: state => ({ headers: { Authorization: `Token ${state.authToken}` } })
    },
      
      
    mutations: {
      SET_TOKEN(state, token) {
        state.authToken = token
        cookies.set('auth-token', token)
      },
    },
  
    actions: {
      //destructuring으로 context 오브젝트 내부의 여러 key값중 사용할 값만 중괄호 안에 넣으면 해당 값만 사용할 수 있게 된다.
      login({commit},loginData){
        axios.post(SERVER.BACK_URL+SERVER.BACK_ROUTES.login,loginData)
          .then(res =>{
            commit('SET_TOKEN',res.data.key)
            router.push({name:'Main'})
          })
          .catch(err=>console.log(err))
      }
    },
      
      
    modules: {
    }
  })
  ```

  - 순서
    - `Login.vue`에서 Login버튼을 클릭하면 `Login.vue`의 data에 정의된 loginData가 인자로 넘어가고 `index.js`의 actions에 있는 login 함수가 실행된다.
    - login함수는 서버에서 받아온 토큰값을 인자로 넘겨 mutations에 있는 SET_TOKEN함수를 실행시키고 state의 authToken변수에 인자로 받아온 토큰값이 담기게 되고 cookie에 토큰값이 저장된다.



- 회원가입 구현

  - `Signup.vue`

  ```html
  <template>
    <div>
      <h1>Signup</h1>
      <div>
        <label for="username">id:</label>
        <input v-model="signupData.username" id="username" type="text" />
      </div>
      <div>
        <label for="password1">password:</label>
        <input v-model="signupData.password1" id="password1" type="password" />
      </div>
      <div>
        <label for="password2">password2:</label>
        <input v-model="signupData.password2" id="password2" type="password" />
      </div>
      <div>
        <button @click="signup(signupData)">Signup</button>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions } from "vuex"
  export default {
    name: "SignupView",
    data() {
      return {
        signupData: {
          id: null,
          password1: null,
          password2: null
        }
      };
    },
    methods: {
      ...mapActions(["signup"])
    }
  };
  </script>
  <!--후략-->
  ```

  - `index.js`

  ```js
  //전략, login 파트에 적은 index.js와 동일
  actions: {
    signup({commit},signupData){
      axios.post(SERVER.BACK_URL+SERVER.BACK_ROUTES.signup,signupData)
        .then(res =>{
          commit('SET_TOKEN',res.data.key)
          router.push({name:'Main'})
        })
        .catch(err=>console.log(err))
    }
  },
  //후략, login 파트에 적은 index.js와 동일
  ```

  

- 로그인, 회원가입 통합

  - 위에서 확인할 수 있듯이 로그인과 회원가입은 로직이 상당히 유사하다. 따라서 공통되는 부분을 따로 빼서 하나의 함수를 만들고 로그인과 회원가입 함수 각각에서 해당 함수를 실행시키도록 코드를 작성할 수도 있다.

  ```js
  //전략, login 파트에 적은 index.js와 동일
  actions: {
      //login, signup 함수에 공통으로 들어가던 부분을 따로 뽑아 만든 함수
      postAuthData({ commit }, info) {
        axios.post(SERVER.URL + info.location, info.data)
          .then(res => {
            commit('SET_TOKEN', res.data.key)
            router.push({ name: 'Main' })
          })
          .catch(err => console.log(err.response.data))
      },
       
          
      //actions에 정의된 함수는 dispatch로 실행한다.
  	login({ dispatch }, loginData) {
        //굳이 아래와 같이 오브젝트를 선언해서 인자로 넘기는 이유는 dispatch에는 인자를 하나 밖에 넘길 수 없기 때문이다. 
        const info = {
          data: loginData,
          location: SERVER.ROUTES.login
        }
        dispatch('postAuthData', info) //상단에 정의한 공통 로직을 수행하는 함수를 실행
      },
              
  
      signup({ dispatch }, signupData) {
        const info = {
          data: signupData,
          location: SERVER.ROUTES.signup
        }
        dispatch('postAuthData', info) //상단에 정의한 공통 로직을 수행하는 함수를 실행
      },.       
  }
  //후략, login 파트에 적은 index.js와 동일
  ```



- 로그아웃 구현

  - `Logout.vue`

  ```html
  <template>
    <div></div>
  </template>
  <!--위와 같이 아무런 내용을 띄우지 않아도 사용자는 전혀 어색함을 느끼지 못할 것인데 그 이유는 index.js에 정의된 logout함수는 함수 실행이 완료되면 Main페이지로 이동되기 때문에 이 페이지는 사실상 볼 틈도 없기 때문이다.-->
  <script>
  import { mapActions } from 'vuex'
  
  export default {
      name: 'LogoutView',
      methods: {
          ...mapActions(['logout'])
      },
      created() {
          this.logout()
      }
  }
  </script>
  ```

  - `index.js`

  ```js
  //전략, login 파트에 적은 index.js와 동일
  actions: {
    logout({ getters, commit }) {
        //logout 요청을 보낼 때에는 data는 담아서 보낼 필요가 없으므로 null값을 주었으나 header에는 토큰을 담아서 보내야 하므로 getters.config			와 같이 써준다.
        axios.post(SERVER.URL + SERVER.ROUTES.logout, null, getters.config)
        	// 요청이 성공적으로 보내진 순간(then으로 빠진 순간) Django DB 에서는 삭제되지만 cookie, state 에는 아직 남아있다.
          .then(() => {
            //state에서 삭제하기 위해서는 아래와 같이 state의 authToken값을 null값으로 변경해야 한다.
            //state는 오직 mutations에 정의된 함수에 의해서만 변경해야 하므로 mutations함수를 실행
         	  //반드시 state에서 먼저 지운 후 cookies에서 지워야 한다.
            commit('SET_TOKEN', null)
            // cookie 에서도 삭제
            cookies.remove('auth-token')  
            router.push({ name: 'Main' })
          })
          .catch(err => console.log(err.response.data))
      },
  },
  //후략, login 파트에 적은 index.js와 동일
  ```

  





# Vuex로 게시글 생성 및 조회 구현

- 게시글 조회

  - `PostList.vue`

  ```html
  <template>
    <div>
      <h1>Article List</h1>
      <ul>
        <li v-for="post in posts" :key="`post_${post.id}`">
          {{ post.title }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { mapState, mapActions } from 'vuex'
  export default {
    name: "PostList",
    computed: {
      ...mapState(['posts'])
    },
    methods: {
      ...mapActions(['fetchPosts'])
    },
    created() {
      this.fetchPosts()
    }
  };
  </script>
  
  <style>
  </style>
  
  ```

  - `index.js`

  ```js
  import Vue from 'vue'
  import Vuex from 'vuex'
  
  import axios from 'axios'
  
  import router from '@/router'
  import SERVER from '@/aaa/bbb'
  
  Vue.use(Vuex)
  
  export default new Vuex.Store({
    state: {
      posts: []
    },
    getters: {
      config: state => ({ headers: { Authorization: `Token ${state.authToken}` } })
    },
    mutations: {
      GET_POSTS(state, posts) {
        state.posts = posts
      }
    },
    actions: {
      getPosts({ commit }) {
        axios.get(SERVER.URL + SERVER.ROUTES.postList)
          .then(res => commit('SET_ARTICLES', res.data))
          .catch(err => console.error(err))
      },
  
      createPost({ getters }, postData) {
        axios.post(SERVER.URL + SERVER.ROUTES.createPost, postData, getters.config)
          .then(() => { 
            router.push({ name: 'List' })
          })
          .catch(err => console.log(err.response.data))
      },
  
    },
    modules: {
    }
  })
  ```

  



- 게시글 생성

  - `CreatePost.vue`

  ```html
  <template>
    <div>
      <h1>새 글 쓰기<h1>
      <div>
        <label for="title">title:</label>
        <input v-model="postData.title" id="title" type="text" />
      </div>
      <div>
        <label for="content">content:</label>
        <textarea v-model="postData.content" id="content" cols="30" rows="10"></textarea>
      </div>
      <div>
        <button @click="createPost(postData)">작성하기</button>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex'
  export default {
    name: "CreatePost",
    data() {
      return {
        postData: {
          title: null,
          content: null,
        }
      }
    },
    methods: {
      ...mapActions(['createPost'])
    },
  };
  </script>
  
  <style>
  </style>
  
  ```

  - `index.js`

  ```js
  import Vue from 'vue'
  import Vuex from 'vuex'
  
  import axios from 'axios'
  
  import router from '@/router'
  import SERVER from '@/aaa/bbb'
  
  Vue.use(Vuex)
  
  export default new Vuex.Store({
    state: {
      posts: []
    },
    getters: {
      config: state => ({ headers: { Authorization: `Token ${state.authToken}` } })
    },
    mutations: {
      GET_POSTS(state, posts) {
        state.posts = posts
      }
    },
    actions: {
      createPost({ getters }, postData) {
        axios.post(SERVER.URL + SERVER.ROUTES.createPost, postData, getters.config)
          .then(() => { 
            router.push({ name: 'List' })
          })
          .catch(err => console.log(err.response.data))
      },
  
    },
    modules: {
    }
  })
  ```

  