# CSS 문서 표현(상)

- CSS: Cascading Style Sheets의 약자로 HTML이 문서의 구조화하는 역할을 한다면 CSS는 스타일을 정의하는 역할을 한다.



- CSS의 특징
  -  HTML 요소에 스타일 적용하기 위해 사용
  - 스타일 시트 파일이라고도 한다.
  - HTML 요소의 시각적 특성을 변경함



- CSS의 장점
  - 디자인을 정의, 관리, 재활용하는데 용이
  - 하나의 CSS파일은 다수의 HTML에서 사용할 수 있어 체계적이고 경제적
  - HTML과 함께 사용되지만 HTML은 아님, CSS는 스타일언어
  - HTML 외에 다른프로그래밍 언어와 사용 가능



- CSS 작성 방법(HTML과 짝을 이루어 사용) 세 가지
  - HTML요소에 직접 CSS 정의(인라인): HTML 요소에 스타일 속성 이용
  - CSS를 모아서 정의(내부참조): HTML 헤더 부분에 stlye 요소 사용
  - CSS 파일을 만들어 HTML에 연결(외부참조): 세 방법 중 가장 권장되는 방법 방법
    - HTML이 서버에서 웹 브라우저로 로드 될 때 CSS 파일도 같이 로드
    - HTML 내용 화면에 나타낼 때 외형 디스플레이에 CSS파일 참고됨



- CSS의 화면 정의 내용
  - 텍스트의 크기 및 스타일
  - 요소들의 레이아웃
  - 그림, 섹션 요소들의 크기와 테두리, 배경 색 또는 이미지
  - 화면 전환이나 요소들의 움직임



- CSS 기술 방식

  - 기본 기술 방식

    - 형태: 선택자{속성 선언}

      - 선택자: HTML의 어떤 요소들에 속성들이 적용되는지 정의하는 곳, 형태는 단순한 요소명, 클래스, ID 또는 복잡한 논리 형 등으로 다양

      - 속성 선언: 선택자를 통해 선택된 HTML요소에 적용할 스타일 속성 내용, 속성(정의하는 스타일의 내용)과 값으로 구성됨.

        -하나의 선택지는 하나의 속성 선언을 가짐

        -각각의 속성 선언은 ;(세미콜론)으로 분리, 하나의 속성 선언만 쓰더라도 꼭 붙여야 한다.

        -속성 선언은 {}사용

    ```css
    #예시
    h1{font-size:1.5em;}  #h1요소에 {}안과 같은 속성을 적용하겠다.
    font-size는 속성을, 1.5em은 값을 의미한다.
    font-size외에도 width(넓이), height(높이), color(폰트 색), font-weight(폰트 크기) 등의 속성이 있으며 따로 설정하지 않으면 기본값으로 설정된다.
    ```



- HTML 문서에 CSS 적용과 연결

  - HTML 요소 속성으로 CSS 적용(임베딩 스타일)

    ```html
    <!DOCTYPE html>
    <html>
      <head>
        <style>
          h1 { color: red; }
          p  { background: aqua; }
        </style>
      </head>
      <body>
        <h1>Hello World</h1>
        <p>This is a web page.</p>
      </body>
    </html>
    ```

    

      - 선택지를 통하여 직접 요소에 CSS 스타일 추가

      - 방법: 스타일 속성을 통하여 CSS 스타일 적용

      - CSS 속성 선언: ;(세미콜론)으로 분리하여 선언

    - 이와 같은 방법은 편리하다는 장점이 있지만 아래와 같은 단점이 존재하므로 피해야하고 테스트용으로만 사용해야 한다.

      -동일 요소 공통으로 적용 불가

      -수정 및 변경 시 모든 HTML 코드 검토

      -체계적인 관리와 변경 불가능

  - Style 요소를 사용한 CSS적용(인라인 스타일)
  
    - 방법: head 부분에 선택자를 이용하여 style 요소 정의
    - CSS코드가 위치한 HTML 파일에만 적용
    - 전체 수정 시 모든 HTML 파일을 수정해야 한다는 단점이 존재
    - style요소의 속성
      - type:stlye언어가 어떤 MIME 타입인지 지정
      - media: 현재 CSS코드가 어떤 매체일 경우 지정되는지 지정
  
    ```html
    <!DOCTYPE html>
    <html>
      <body>
        <h1 style="color: red">Hello World</h1>
        <p style="background: aqua">This is a web page.</p>
      </body>
    </html>
    ```
  
  - 외부 CSS 파일을 HTML파일에 연결(링크 스타일)
  
    ```html
    <!DOCTYPE html>
    <html>
      <head>
          <link rel="stylesheet" href="css/style.css">
      </head>
      <body>
        <h1>Hello World</h1>
        <p>This is a web page.</p>
      </body>
    </html>
    ```
  
    ```css
      h1 { color: red; }
      p  { background: blue; }
    ```
  
    - 여러 HTML 파일에 공통으로 사용
  
      - 수정 시 HTML 파일을 전체 수정할 필요 없음
  
      - 체계적이고 구조적인 스타일 관리 가능
  
      - 파일 크기를 줄일 수 있어 전체 전송량이 줄어듬
  
      - 외부 스타일 시트 파일: .css를 가지는 파일, 텍스트로 이루어짐
  
      - HTML에서 외부 CSS 파일의 연결 순서
  
        -HTML 코드 작성
  
        -비어있는 파일을 작성하고 확장자 .css로 저장
  
        -CSS파일 경로 지정(HTML 코드 header 부분에 link요소 사용)
  
        -CSS 파일 열어 CSS 스타일 지정
  
      - link 요소: HTML 문서와 외부 리소스 연결을 위해 사용, 대부분 CSS 파일 연결
  
      - link 요소의 속성
  
        - rel: 생략 불가능한 속성, 현재 HTML과 연결할 파일 간의 관계를 나타냄, 다양한 값을 가진다.
        - href: 연결하고자 하는 리소스 파일 경로 지정



- CSS 선택자(selecter)

  - 선택자는 스타일을 적용하고자 하는 HTML 요소를 선택하기 위한 수단이다.

  - 선택자로 HTML 요소를 선택하고 {}내에 속성과 값을 지정하여 다양한 스타일을 설정할 수 있다. 여러 개의 속성을 연속해서 지정할 수 있으며 ;으로 구분한다. 복수개의 셀렉터를 연속하여 지정할 수 있으며 쉼표( , )로 구분한다.

    ```css
    h1{color:red;font-size:12px;}
    선택자: h1
    선언: color:red;, font-size:12px;
    선언 블록: {color:red;font-size:12px;}
    속성(프로퍼티):color, font-size
    값: red, 12px
    
    /*복수의 선택자 지정*/
    h1, p { color: red; }
    ```

  

  - 타입 선택자(기초 선택자)

    - 가장 쉽고 기본이 되는 기초적인 선택자
      
    - HTML요소명, 요소의 클래스 속성 값, ID 값
      - HTML선택자(태그 셀렉터): HTML요소가 선택자인 선택자

        ```html
        <!--형식: 태그명-->
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            /* 모든 p 태그 요소를 선택 */
            p { color: red; }
          </style>
        </head>
        <body>
          <h1>Heading</h1>
          <div>
            <p>paragraph 1</p> p태그 요소 이므로 red로 출력
            <p>paragraph 2</p> p태그 요소 이므로 red로 출력
          </div>
          <p>paragraph 3</p>   p태그 요소 이므로 red로 출력
      </body>
        </html>
        ```

      - 클래스 선택자: HTML 클래스 속성 값, 요소들을 원하는 그룹으로 묶을 수 있음, HTML 문서 내의 동일한 클래스 값을 가지는 모든 요소에 적용, .(온점)으로 표시한다.

        ```html
        <!--형식: .class 어트리뷰트 값-->
        <!DOCTYPE html>
        <html>
        	<head>
                  <style>
                    /* class 어트리뷰트 값이 text-center인 모든 요소를 선택 */
                    .text-center { text-align: center; }
                    /* class 어트리뷰트 값이 text-large인 모든 요소를 선택 */
                    .text-large  { font-size: 200%; }
                    /* class 어트리뷰트 값이 text-red인 모든 요소를 선택 */
                    .text-red    { color: red; }
                    /* class 어트리뷰트 값이 text-blue인 모든 요소를 선택 */
                    .text-blue   { color: blue; }
                  </style>
            </head>
            <body>
                  <!--class 어트리뷰트 값이 text-center이므로 중앙에 표시됨-->
                  <p class="text-center">Center</p>
                  <!--class 어트리뷰트 값이 text-red이므로 빨강으로 표시됨-->
                  <!--class 어트리뷰트 값이 text-large이므로 200% 크기도 표시됨-->
                  <p class="text-large text-red">Large Red</p>
                  <!--class 어트리뷰트 값이 text-center, text-large, text-blue이므로
                	중앙에 빨강색으로 200%크기로 표시됨-->
                  <p class="text-center text-large text-blue">Center Large Blue</p>
            </body>
        </html>
        ```

      - ID 선택자: HTML ID 속성 값에 CSS를 적용, HTML ID 속성은 HTML 문서 내의 유일한 값으로 고유의 요소를 식별한다. 문서 내의 같은 ID를 가진 유일한 요소에 적용한다. #으로 표현한다.

        ```html
        <!--형식: #id 어트리뷰트 값-->
        <!DOCTYPE html>
        <html>
           <head>
             <style>
               /* id 어트리뷰트 값이 p1인 요소를 선택 */
               #p1 { color: red; }
             </style>
           </head>
           <body>
             <h1>Heading</h1>
             <div class="container">
               <p id="p1">paragraph 1</p> <!--id 어트리뷰트 값이 p1이므로 빨강으로 출력-->
               <p id="p2">paragraph 2</p>
             </div>
               <p>paragraph 3</p>
                </body>
        </html>
        ```

      - 그룹 지정: 여러 요소에 동일한 CSS 스타일 적용

      - 전체 셀렉터

        ```html
         <!--형식: * -->
        <!DOCTYPE html>
        <html>
            <head>
              <style>
                /* 모든 요소를 선택 */
                * { color: red; }
              </style>
            </head>
            <body>
              <h1>Heading</h1>
              <div>
                <p>paragraph 1</p>  <!--전체 셀렉터이므로 전부 빨강으로 출력-->
                <p>paragraph 2</p>  <!--전체 셀렉터이므로 전부 빨강으로 출력-->
              </div>
              <p>paragraph 3</p>    <!--전체 셀렉터이므로 전부 빨강으로 출력-->
           </body>
        </html>
        ```

    - 고급 선택자

      - HTML 문서의 요소들의 계층관계를 이용하여 선택하는 선택자

      - CSS는 상속을 통해 부모 요소의 속성을 자식에게 상속한다.

        - 상속 되는 것: Text 관련 요소(font, color 등)
        - 상속 되지 않는 것: Box model 관련 요소(width, height 등)와 position관련 요소(position, left, right 등)

        - MDN에서 상속 여부를 확인 할 수 있다.

      - HTML 요소들의 계층관계: 요소들 간의 포함 관계에 따라 자손요소, 직계 자손 요소, 형제 요소, 인접 형제 요소등으로 나뉜다.

        - 자손 요소: 특정 요소의 내부에 포함된 요소

        - 직계 자손 요소: 특정 요소의 바로 아래 있는 요소

        - 형제 요소: 같은 계층 단계에 있는 요소

        - 인접 형제 요소: 바로 아래 있는 형제 요소

        - 고급 선택자의 종류

          -하위 선택자: 어떤 요소 하위에 있는 특정 자손 요소 선택 시 사용. 대괄호로 표현

          -형제 선택자: 특정 요소 다음에 나오는 형제 관계 요소들 선택. ~(물결무늬)로 표현

          ```html
          <!DOCTYPE html>
          <html>
            <head>
                <style>
                  /* p 요소의 형제 요소 중에 p 요소 뒤에 위치하는 ul 요소를 모두 선택한다.*/
                  p ~ ul { color: red; }
                </style>
            </head>
            <body>
                <div>A div element.</div>
                <ul>
                  <li>Coffee</li>
                  <li>Tea</li>
                  <li>Milk</li>
                </ul>
              
                <p>The first paragraph.</p>
                <ul>
                  <li>Coffee</li>	<!--p 요소의 형제 요소 중에 p 요소 뒤에 위치하는 ul 요소-->
                  <li>Tea</li>	<!--p 요소의 형제 요소 중에 p 요소 뒤에 위치하는 ul 요소-->
                  <li>Milk</li>	<!--p 요소의 형제 요소 중에 p 요소 뒤에 위치하는 ul 요소-->
                </ul>
              
                <h2>Another list</h2>
                <ul>
                  <li>Coffee</li>	<!--p 요소의 형제 요소 중에 p 요소 뒤에 위치하는 ul 요소-->
                  <li>Tea</li>	<!--p 요소의 형제 요소 중에 p 요소 뒤에 위치하는 ul 요소-->
                  <li>Milk</li>	<!--p 요소의 형제 요소 중에 p 요소 뒤에 위치하는 ul 요소-->
              </ul>
            </body>
          </html>
          ```

          

          -직계 자손 선택자: 바로 하위에 있는 요소 선택 시 사용, 여러 단계에 있는 자손을 모두 선택하는 하위 선택자와는 다름. 꺽쇠로 표현

          ```html
          <!DOCTYPE html>
          <html>
          <head>
            <style>
              /* div 요소의 자식요소 중 p 요소 */
              div > p { color: red; }
            </style>
          </head>
          <body>
            <h1>Heading</h1>
            <div>
              <p>paragraph 1</p>	<!--div 요소의 자식요소 중 p 요소-->
              <p>paragraph 2</p>	<!--div 요소의 자식요소 중 p 요소-->
              <span><p>paragraph 3</p></span> <!--div요소의 자식요소지만 p요소가 아님-->
            </div>
          <p>paragraph 4</p>	<!--p요소지만 div 요소의 자식요소가 아님--
          </body>
          </html>
          ```

  				
  			
  				-인접 형제 선택자: 특정 요소 바로 다음에 오는 형제 관계 요소 선택.+로 표현
  				
  				```html
  				<!DOCTYPE html>
  				<html>
  				<head>
  				  <style>
  				    /* p 요소의 형제 요소 중에 p 요소 바로 뒤에 위치하는 ul 요소를 선택한다. */
  				    p + ul { color: red; }
  				  </style>
  				</head>
  				<body>
  				  <div>A div element.</div>
  				  <ul>
  				    <li>Coffee</li>
  				    <li>Tea</li>
  				    <li>Milk</li>
  				  </ul>
  				
  				  <p>The first paragraph.</p>
  				  <ul>
  				  	<!--p 요소의 형제 요소 중에 p 요소 바로 뒤에 위치하는 ul 요소-->
  				    <li>Coffee</li>
  				    <!--p 요소의 형제 요소 중에 p 요소 바로 뒤에 위치하는 ul 요소-->
  				    <li>Tea</li>
  				    <!--p 요소의 형제 요소 중에 p 요소 바로 뒤에 위치하는 ul 요소-->
  				    <li>Milk</li>	
  				  </ul>
  				
  				  <h2>Another list</h2>
  				  <ul>
  				    <li>Coffee</li>
  				    <li>Tea</li>
  				    <li>Milk</li>
  					</ul>
  				  </body>
  				</html>
  				```
  				
  				


- CSS 적용 우선 순위(중요)
  - 중요도: !important가 정의 되면 다른 무엇이 있든 최우선 순위를 가진다.
    - 따라서 굉장히 주의해서 사용해야 한다.
  - 우선 순위: 인라인 > id선택자 > class 선택자 > 요소 선택자
  - 소스 순서(선언 순서, 뒤에 작성된 것이 최종적으로 적용 된다)
  
  ```html
  h3 { color: violet !important}
  p { color: green; }
  .blue { color: blue; }  <!--.blue에서 .은 클래스를 의미한다.-->
  .skyblue { color: skyblue; }
  #red { color: red; }   <!--#red에서 #은 아이디를 의미한다.-->
  
  소스코드가 위와 같을 때 아래의 숫자들은 무슨 색으로 출력 되겠는가?
  
  
  요소선택자 
  <p>1</p> 
  1은 초록 색으로 출력. ∵p { color: green; }
  
  요소선택자 VS class선택자
  <p class="blue">2</p> 
  2는 파란색으로 출력. ∵.blue { color: blue; }
  
  소스 순서
  <p class="blue skyblue">3</p> 
  3은 하늘색으로 출력.
  <p class="skyblue blue">4</p> 
  4는 하늘색으로 출력.
  
  id선택자 VS class 선택자
  <p id="red" class="blue">5</p> 
  5는 빨간색으로 출력.  ∵#red { color: red; }
  
  !important VS id선택자
  <h3 id="red" class="blue">6</h3> 
  6은 바이올렛색으로 출력 ∵h3 { color: violet !important}
  
  id VS 인라인
  <p id="red" class="blue" style="color: yellow;">7</p> 
  7은 노란색으로 출력 ∵style="color: yellow
  
  !important VS 인라인
  <h3 id="red" class="blue" style="color: yellow;">8</h3>
  8은 바이올렛색으로 출력 ∵h3 { color: violet !important}
  ```
  
  



- 의사 클래스(X)
  - 가짜 또는 모조 클래스로 클래스의 특징은 가진다.
  - 형식: :(콜론)의사 클래스 명
  - 링크와 관련된 의사 클래스
    - : link 링크 의사 클래스: 한 번도 방문하지 않은 링크
    - : visited 의사 클래스: 방문한 링크에 CSS 스타일 적용 시 사용
  - 동적 의사 클래스: 마우스와 커서에 관한 상태를 의사 클래스로 나타냄
    - active의사 클래스: 마우스로 클릭 했을 때의 상태 의미
    - hover 의사 클래스: 마우스 커서가 올라간 상태 의미
    - focus 의사 클래스: 서식 폼과 같은 요소에 마우스가 위치하여 입력 또는 선택 상황 의미
  - 구조적 의사 클래스: HTML 구조에 따른 의사 클래스
    - 형재와 자손 그리고 몇 번째 요소인지로 상태 구분
    - root 의사 클래스: 문서 최상위 요소 의미, 단독으로 사용
    - empty 의사 클래스: 비어 있는 요소 의미
    - only-child 의사 클래스: 형제가 없는 요소
    - only-of-type 의사 클래스: 같은 타입의 형제가 없을 때 사용
    - first-child, last-child 의사 클래스: 첫 번째 자손 요소와 마지막 자손 요소를 의미
    - nth-of-type(n), nth-last-of-type(n): 같은 부모 요소의 자손 요소로 특정 요소의 n번째 요소를 의미한다는 점은 같지만 전자는 위에서부터 세어가고 후자는 아래에서부터 세어감.
  - 기타 의사 클래스 
    - :lang() 의사 클래스 : 지정한 언어 속성을 가지는 요소
    - :not() 의사 클래스 : 부정을 의미
  - 의사 엘리먼트: 가짜 요소, 선택자에 따라 기존 요소에 추가로 새로운 요소 정의
    - :first-letter 의사 엘리먼트 : 선택자에서 선택한 요소의 첫 번째 글자를 새 요소로 만듦
    - :first-line 의사 엘리먼트 : 선택자에서 선택한 요소의 첫 번째 줄을 새 요소로 만듦 
    - :after, :before 의사 엘리먼트 : 선택자에 의해 선택된 요소 앞뒤에 요소를 만듦



- 미디어 쿼리: 현재 HTML 문서가 보여지는 화면이 어떤 것인지 파악

  ex.스마트 폰인지 pc인지 테블릿 pc인지를 파악

  

- 상속과 캐스케이딩: HTML 요소에 적용된 CSS 스타일 중 어떤 것들은 하위 자식에게 상속된다.
  - 적용 우선 순위
    - 사용자가 선택자를 통해 직접 정의한 스타일
    - HTML에 스타일 속성으로 적용한 인라인 스타일
    - 미디어 타입에서 지정한 속성
    - !important 구문을 추가한 CSS 속성
    - 구체적인 선택자
    - 뒷 부분에 정의된 스타일
    - 부모로부터 상속된 스타일
    - 웹 브라우저 기본 스타일 





---







# CSS 문서 표현(하)

- 텍스트 표현(있다는 것만 알아 둘것)
  - 폰트 패밀리: 비슷한 모양의 서체를 묶어서 제시, 만일 지정한 서체가 없을 경우 대안 서체를 사용하게 된다.
  
  - 서체의 크기 조절
    - font-size: 서체 크기 조절
    
    - 서체의 크기 단위: px(픽셀), %, em(요소에 지정된 사이즈에 상대적인 사이즈를 지님), rem(최상위 요소(HTML)의 사이즈를 기준으로 배수 단위를 가짐, rootrem이라고 생각하면 된다), Viewport 기준 단위(vw,vh,vmin,vmax)
    
    - 다양한 변형 서체(쓰지 않는 것이 좋다)
      - Iralic: font-style 속성으로 설정한다.
      
        | 속성    | 설명                                                         |
        | ------- | ------------------------------------------------------------ |
        | italic  | italic 타입의 서체로 변환                                    |
        | oblique | 단순히 서체를 기울임, 이텔릭 타입 서체가 존재하지 않을 경우 사용 |
        | normal  | italic 타입의 서체 사용하지 않고 보통 서체로 보여줌          |
      
      - bold: font-weight 속성으로 설정한다.
      
        | 속성    | 설명                                                 |
        | ------- | ---------------------------------------------------- |
        | bold    | 해당 서체 bold타입의 서체로 변환                     |
        | bolder  | 부모 요소의 두께보다 좀 더 두꺼운 타입의 서체로 변환 |
        | ligther | 부모 요소의 두께보다 좀 더 얇은 타입의 서체로 변환   |
        | 100~900 | 100~900사이의 서체의 굵기로 변환                     |
        | normal  | bold 타입의 서체 일반 타입의 서체로 변환             |
    
  - 텍스트 스타일 설정
  
    - 텍스트 간격 설정: 글자와 글자의 간격 또는 단어와 단어의 간격 설정
      - 자간 설정 : letter-spacing 속성 사용
      - 단어 간격 설정 : word-spacing 속성 사용 
      - 행간 설정 : line-height 속성 사용
  
  - 기타 텍스트 꾸미기(X)
  
    - text-decoration 속성 사용
      - undrline: 밑줄 생성
      - overline: 텍스트 위에 줄 긑기
      - line-throught: 텍스트 중간에 줄을 그어줌
      - none: 밑줄 없앰
    - text-transform 속성 사용
      - capitalize: 각 단어의 첫 글자 대문자로 만드는 속성
      - uppercase: 모든 텍스트 대문자 변환
      - lowercase: 모든 텍스트 소문자 변환
      - none: 대소문자 변경 기능 없앰
    - text-shadow 속성 사용
      - x-offset: 그림자가 x축으로 얼마나 비껴 나타나는지 의미
      - y-offset: 그림자가 y축으로 얼마나 비껴 나타나는지 의미
      - blur: 그림자 테두리의 흐림 정도 설정
      - color: 그림자 색
      - none: 그림자 속성 해제
  



- 컬러 
  - 웹 색상 코드: 16진수 표현, 10진수 표현, HSL 표현, 색상 키워드
  - 투명도 표현: 컬러에 투명도 설정이 가능하며 10진수 색상 코드로만 가능하다.
  - 텍스트 색 지정: color 속성 사용



- 배경(있다는 것만 알아 둘 것)
  - 배경 색 설정: background-color 속성 
  - 배경 이미지 설정 : background-image 속성 사용 
  - 배경 이미지 반복 설정 : background-repeat 속성 사용 
  - 배경 이미지 고정 설정 : background-attachment 속성 사용
  - 배경 이미지 위치 설정 : background-position 속성 사용 
  - 배경 이미지 크기 설정 : background-size 속성 사용



- 목록, 표 꾸미기

  - 블릿 꾸미기
    - 블릿: 목록을 정리하여 예쁘게 보이도록 목록 아이템 앞에 붙는 숫자 또는 특수문자
    - 블릿 설정: list-style-type 속성 사용
      - 이미지 블릿 설정: list-style-image 속성 사용
      - 블릿 위치 설정: list-style-position 속성 사용

  

  - Margin과 Padding

    - 모든 블록 레벨 요소들은 박스 형태의 영역을 가지고 있는데 그 바깥쪽 여유 공간을 margin, 안쪽 여유 공간을 padding이라 한다.

    - 마진과 패딩은 상하좌우 개별적으로 설정할 수 있으며 코드 상으로는 시계방향으로 상우하좌 순서로 적게 된다.

      ```html
      margin: 10px, 5px, 12px, 8px;
      위와 같이 적으면 자동으로 상우하좌 순으로 적용된다.
      ```

      

  - border

    - margin과 pading사이의 경계
    - border 생성 속성 : border-width(굵기 지정), border-style(스타일 지정), border-color(색 지정). 이 세 가지가 가장 기본으로 축약하여 작성할 수 있다.

    ```css
    p {border: 1px solid red;} 각기 굵기, 스타일, 색이 들어가게 된다.
    ```
    - 셀 간격 설정: border-spacing: 수치;
    - 셀 간격 삭제: border-collapse:collapse;



- CSS 박스 모델
  - HTML문서 body 부분의 모든 요소가 사각형 영역을 가지고 있는데 박스 모델은 요소를 박스로 나타낼 때 어떻게 구성되며 박스들의 위치와 상관관계를 지정하는 방식을 정의하는 것이다.

  - 박스 모델의 구성은 외부부터 내부순서로 margin-border-padding-content로 구성된다.

    - margin: 테두리(border) 바깥의 외부 여백으로 배경색을 지정할 수 없다
    - border: 테두리 영역
    - padding: 테두리 안쪽의 내부 여백으로, 요소에 적용된 배경의 컬러, 이미지는 패딩까지 적용된다.
    - content: 실제 내용이 위치

  - 아래와 같이 영역을 설정할 수 있다.

    ```css
    .margin{
    margin-top: 수치px;
    margin-right: 수치px;
    margin-bottom: 수치px;
    margin-top: 수치px;
    }
    
    혹은 margin과 padding을 동시에 설정할 수도 있다.
    .margin-padding{
    margin: 수치px;   이 경우 상하좌우가 모두 동일하게 설정된다.
    padding: 수치px;
    }
    
    혹은 아래와 같이 쓸 수도 있다.
    하나만 쓸 경우 4방이 모두 동일한 수치로 설정됨
    .margin-1{      
    margin: 수치px;
    }
    두 개를 쓸 경우 상하는 앞의 수치로, 좌우는 뒤의 수치로 적용됨
    .margin-2{      
    margin: 수치px 수치px;
    }
    세 개를 쓸 경우 첫번째 수치는 상, 두번째는 좌우, 세번째는 하에 적용됨
    .margin-3{      
    margin: 수치px 수치px 수치px;
    }
    네 개를 쓸 경우 시계방향(상우하좌 순)으로 적용됨
    .margin-3{      
    margin: 수치px 수치px 수치px 수치px;
    }
    
    border의 경우 굵기, 스타일, 색이 들어가는데 아래와 같이 쓸 수도 있고
    .border{
    border-width: 수치px;
    border-style: 스타일;
    border-color: 색;
    }
    
    아래와 같이 쓸 수도 있다.
    .border{
    border: 수치 스타일 색;
    }
    ```

  

  - 블록 레벨 요소의 margin과 padding은 상하좌우 사방으로 margin과 padding이 적용되지만 인라인 레벨 요소의 margin과 padding은 좌우만 적용된다(즉 width, height, margin-top, margin-bottom을 지정할 수 없다). 따라서 상하 여백은 line-height로 지정한다.

  - width, height 속성 : 블록 레벨 요소의 크기 설정, 인라인 레벨 요소에는 적용 안됨 
    - width 속성 : 요소의 넓이 설정
    - height 속성 : 요소의 높이 설정

  - 요소의 크기는 width와 height로 설정한 대로 나오지 않는데 그 이유는 이 외에도 요소의 크기에 영향을 미치는 것들이 있기 때문이다. 요소의 크기는 아래의 것들을 모두 합한 값이다.
    - width와 height로 정한 값

    - padding값과 margin값

    - border의 굵기 값

      

  - 기본적으로 모든 요소의 box-sizing은 content-box이다. 즉 padding을 제외한 순수 content영역만 box로 지정한다. 다만 일반적으로 영역을 볼 때는 border까지 포함시킨 너비를 지정하려함. 따라서 이러한 경우 box-sizing을 border-box로 설정한다.

  

  - margin 겹침(상쇄) : 두 개의 margin 연속 적용으로 margin이 겹치는 현상 발생 

  

  - display
    - HTML 4.1까지는 인라인과 블록으로 태그를 구분하였음
    - 블록과 인라인의 차이(HTML 문서 구조(상) 부분에 적어 놓았으니 참고)
    - inline-block은 block과 inline 레벨 요소의 특징을 모두 갖는 것으로 inline처럼 한 줄에 표시 가능하며, block처럼 width, height, margin 속성을 모두 지정할 수 있다.
    - 속성에 따른 수평 정렬

  

  - Position 속성:  특정 요소가 다른 요소들과 어떠한 관계 속에서 위치를 결정하는 지 설정

    - static: 디폴트 값(기준 위치)

      -기본적인 요소의 배치 순서에 따름(좌측상단)

      -부모 요소 내에서 배치될 때는 부모 요소의 위치를 기준으로 배치된다.

    - position 속성의 속성 값 : 상대 위치, 절대 위치, 고정 위치  

    - 아래는 좌표 프로퍼티(top,bottom,left,right)를 사용하여 이동이 가능하다(음수값도 가능)

    - 상대 위치(relative) : static 위치를 기준으로 이동. 

      -position: relative;

    - 절대 위치(absolute) : 가장 가까이 있는 부모/조상 요소중에 static이 아닌  것을 기준으로 이동 

      -position: absolute;

    - z-index 속성 : 어떤 요소가 다른 요소 위에 나타나는지 설정, 속성 값이 높게 설정 될 수록 앞에 배치됨

    - 절대 위치 (fixed) : 부모의 좌표와 관계 없이 브라우저 원점에서 좌표를 정한다. 스크롤 해도 고정되어 있다. (ex. 맨 위로 이동하는 버튼은 스크롤을 내려도 계속 화면을 따라 움직이듯이 우측 하단에 고정되어 있다)

      -position: fixed;





---







# 레이아웃과 고급 CSS 기능

- HTML 요소들은 문서의 위에서부터 아래로 순차적으로 나열되지만 아래의 방법들을 통해 변경될 수 있다.

  - diplay 속성을 통해 요소가 보여지는(표현되는) 방식 변경
    - block,inline,inline-block
    - table, flexible box, grid 등의 레이아웃을 활용
    - position 속성을 통해 위치 자체를 변경
    - float 속성을 통 해 떠 있도록 만듦

- float은 요소를 일반적인 흐름에서 벗어나도록 하는 속성 중 하나

  - 반드시 clear 속성을 통해 초기화가 필요하다.

- float을 사용하는 경우 block사용을 뜻하며, display값이 inline인 경우 block으로 계산한다. 즉 float을 사용한다는 것은 block을 사용한다는 것을 뜻하며 display 값이 inline이라도 block으로 취급한다.

- float 속성을 사용한 2단 레이아웃

  - 한 화면에 많은 정보를 담으면 가독성이 떨어질 수 있으므로 화면을 분할하여 정보를 나눠 담아야 한다.

  - 다단 레이아웃 : 화면을 세로로 여러 개의 단으로 나눠 콘텐츠를 보여주는 형태

  - HTML 문서는 오로지 위에서 아래로 콘텐츠 제시 따라서, 다단 레이아웃을 만들기 위해 floating 또는 positioning 레이아웃 활용

  - float 속성을 사용한 2단 레이아웃 설정 방법

    ① HTML 문서 준비하기 

    ```html
    <!DOCTYPE html>
    <html lang = "ko">
        <head>            		   
        	<meta charset="UTF-8">   
            <title>Title</title>
            <link rel="stylesheet" href="style.css">
        </head>
    <body>
        <div id="wrapper">  <!--HTML 문서의 콘텐츠 영역 속성을 설정하기 위한 요소-->
            <header><h1>Site Title</h1></header>
            <section></section>
    ```

    ② 섹션 요소의 넓이 설정하기 

    	- CSS를 이용하여 HTML 요소의 스타일 지정
    	- 모든 요소의 margin과 padding을 0으로 설정
    	- wrapper: HTML 페이지 고정된 크기 설정
    	- 최종 요소의 넓이: : margin넓이+padding넓이+border의 굵기

    ③ float 속성 설정하기 

    - float 속성에는 left와 right가 있다.
    - 2단 레이아웃 만들기: nav 요소는 왼쪽으로 floating, nav+section요소는 오른쪽으로 floating
    - footer 요소도 설정해줘야 하는데 설정하지 않을 경우 맨 아래에 위치하지 않고 위에 표시되게 된다.
      - nav요소와 nav+section요소의 높이를 같게 설정하거나
      - footer요소에 clear속성을 설정하면 해결된다.

    ④ 2단 레이아웃 완성하기

    - 디자인 스타일을 적용하여 정리하고 꾸밈

  - float 속성 설정보다 position 속성 사용 시 몇 가지 더 신경 써야 함

    - 상대위치와 절대위치
      - 상대위치는 요소 위치 설정 시 초기 위치에 자신의 볼륨을 그대로 유지한다. 따라서 좌표의 원점 파악이 어렵다
      - 절대 위치는 요소들의 원점을 부모요소의 왼쪽 상단으로 통일한다. 그러나 요소의 볼륨에 따른 레이아웃 변화에 적용되지 않는다. 절대위치로 포지션 설정 시 주의사항은 절대 요소로 설정한 요소의 형제와 자식 요소 대부분을 절대요소로 지정하여 수치로 위치를 조정해야 한다는 점이다.

  - display 속성을 이용한 2단 레이아웃 설정하기 
    - 블록 레벨 요소들을 inline-block 형태로 줄바꿈 없이 나란히 놓을 수 있음
    - inline-block으로 디스를레이를 설정하면 블록이 글자와 같이 취급된다.



- CSS네비게이션(X)

  - 인터렉티브 이미지 버튼:  HTML 이용 시 이미지 버튼 만들 수 있음 

  - 텍스트 네비게이션

    - 네비게이션 : 웹 사이트에서 분류된 영역으로 쉽게 갈 수 있는 링크의 모음 
    - 초창기 : 텍스트 네비게이션 → 현재 : 그래픽 네비게이션으로 발전
    - 웹 초창기 : 텍스트 네비게이션 - 제작하기 쉽고 로딩이 빨라 현재도 많이 사용 

  - HTML로 텍스트 네비게이션 구조 작성하기

    - nav 요소 안에서 작성 
    - 네비게이션 HTML 작성 방법 : 목록 형태 → 링크의 목록으로 작성
    - 목록 작성 시 순서는 상관 없음 : \<ol>(순서 있는 목록), \<ul>(순서 없는 목록) 

  - CSS로 텍스트 네비게이션 스타일 적용 하기

    - Key Point! 목록 아이템의 display 속성 : inline 

      ① 링크에 설정되어 있는 기본 스타일 초기화 

      ② 목록 요소에 배경색을 검정으로 설정

      ③ 웹 브라우저 margin, padding 0 으로 설정 

      ④ 마우스 롤 오버 설정하기 : a:hover 선택자



- CSS변형과 트랜지션(X)

  - 요소의 변형

    - 요소 숨기기: 요소가 웹 브라우저에서 보이지 않게 하는 것, 웹 브라우저 내 차지하고 있던 영역사라짐

    - 요소를 숨기는 이유

      ① CSS가 지원되지 않는 웹 브라우저 사용자에게 추가 정보 제공 

      ② 시각 장애를 가진 사용자에게 안내 및 추가 정보 제공 ex) 스크린 리더 

      ③ 웹 문서에서 제공하는 정보가 많을 경우 문서의 가독성을 높이기 위해 ex) 펼쳐지는 콘텐츠 : 사용자 동작으로 콘텐츠가 보였다 가려졌다 하는 기능 

    - CSS에서 요소 숨김 속성

      ① visibility: hidden, 요소를 감출 뿐 사라지게는 하지 않으므로 영역은 계속 차지한다.

      ② display: none , 요소뿐만 아니라 영역도 함께 감춘다.

  - 요소 클리핑
    - clip 속성 : 이미지 또는 요소의 특정 부분 만을 보이게 할 때
      - rect(상, 우, 하, 좌): 요소 내의 상하좌우 좌표를 설정하여 클리핑
    - 요소 클리핑 시, 먼저 요소의 포지션 속성을 절대위치로 설정해야 한다.



- CSS를 어렵게 만드는 요소
  - 일반적인 흐름을 바꿔버리는 경우
  - Normal flow
    - inline, block, relative position
  - Floats
  - Absolute positioning 









---









# CSS 기타

- 프로퍼티

  - 프로퍼티에는 키워드, 크기 단위, 색상 표현 단위 등의 특정 단위를 갖는 값을 지정한다.
  - 각각의 프로퍼티에 따라 사용할 수 있는 키워드가 존재한다.

  ```css
  h1{color:red; font-size:12px; display: block}
  h1: 셀렉터
  color, font-size, display: 프로퍼티
  red,12px: 특정 단위를 갖는 값
  block: 키워드
  ```
  - 크기 단위
    - px: 픽셀 단위, 디바이스 해상도에 따라 상대적인 크기를 갖는다.
    - %: 백분율 단위, 요소에 지정된 사이즈(상속된 사이즈나 디폴트 사이즈)에 상대적인 사이즈를 설정함.
    - em: 배수단위, 요소에 지정된 사이즈(상속사이즈, 디폴트 사이즈)에 상대적인 사이즈를 설정함. 예를 들어 상속받은 사이즈가 14px면 2em은 14*2가 되어 28px가 된다. 중첩된 자식 요소에 em을 지정하면 모든 자식 요소의 사이즈에 영향을 미치기 때문에 주의하여야 한다.
    - rem:  최상위 요소(html)의 사이즈를 기준으로 삼는다. r은 root를 의미한다.
  - 색상 단위
    - RGB: red, green,blue순으로 입력
    - RGBA: red, green,blue, 투명도 순으로 입력(투명도는 0~1까지)
    - HEX코드 단위



- 박스 모델

  - width와 heigth 프로퍼티

    - 각기 요소의 너비와 높이를 지정하기 위해 사용되는 것으로 이때 지정되는 요소의 너비와 높이는 콘텐츠 영역을 대상으로 한다.

      -이는 box-sizing프로퍼티에 기본값인 **content-box**가 적용되었기 때문이다. box-sizing 프로퍼티에 **border-box**를 적용하면 콘텐츠 영역, padding, border가 포함된 영역을 width / height 프로퍼티의 대상으로 지정할 수 있다.

    - width와 height 프로퍼티의 초기값은 auto로써 이것은 브라우저가 상황에 따라 적당한 width와 height 값을 계산할 것을 의미한다.

    - 만일 width와 height로 지정한 콘텐츠 영역보다 실제 콘텐츠가 크면 콘텐츠 영역을 넘치게 된다는 것에 유의하여야 한다.

    -  width와 height 프로퍼티는 **콘텐츠 영역**을 대상으로 요소의 너비와 높이를 지정하므로 박스 전체 크기는 다음과 같이 계산할 수 있다.

      -전체 너비: width + left padding + right padding + left border + right border + left margin + right margin

      -전체 높이: height + top padding + bottom padding + top border + bottom border + top margin + bottom margin

    - width와 height 프로퍼티를 비롯한 모든 박스모델 관련 프로퍼티(margin, padding, border, box-sizing 등)는 상속되지 않는다.

  - margin과 padding 프로퍼티(상기하였으므로 pass)

    - 요소 너비가 브라우저 너비보다 크면 가로 스크롤바가 만들어진다. 이 문제를 해결하기 위해서 max-width 프로퍼티를 사용할 수 있다. max-width 프로퍼티를 사용하면 브라우저 너비가 요소의 너비보다 좁아질 때 자동으로 요소의 너비가 줄어든다.
    - border-style: 테두리의 선의 스타일을 지정. 프로퍼티 값의 갯수에 따라 4개 방향(top, right, left, bottom)에 대하여 지정이 가능하다.
    - border-radius: 테두리 모서리를 둥글게 표현하도록 지정한다. 기본 좌상, 좌하, 우상, 우하 4방향 설정 가능하며 각 방향을 다시 둘로 나눠 총 8방향 설정 가능하다.
    - border: `border` 프로퍼티는 `border-width`, `border-style`, `border-color`를 한번에 설정하기 위한 shorthand 프로퍼티이다(상기함).

  - box-sizing: width와 heigth 프로퍼티 대상 영역을 변경할 수 있다. box-sizing 프로퍼티의 값을 border-box로 지정하면 마진을 제외한 박스 모델 전체를 width, height 프로퍼티의 대상 영역으로 지정할 수 있어서 CSS Layout을 직관적으로 사용할 수 있게 한다.


