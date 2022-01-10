# Open API

## 기본 개념

- OpenAPI Specification(OAS)
  - Restful API를 기술하는 표준
    - 서비스에서 제공하는 API 기능과 End Point를 개발자나 시스템이 자동으로 발견하고 처리하는데 필요한 정보를 제공한다.
    - json이나 yml 형식으로 기술하여야 하며 OAS 파일을 읽어서 디플로이 해주는 도구(e.g. swagger-uri)를 사용하면 브라우저에서 편리하게 API를 볼 수 있다.
  - 이전에는 Swagger spec으로 불렸다.
    - 3.0부터 OpenAPI 3.0 Specification이라는 이름으로 표준화 되었다.
  - Swagger는 OAS에 맞게 디자인하고 빌드하기 위한 도구들의 모음으로 아래와 같은 요소로 이루어져 있다.
    - Swagger Editor: 브라우저 기반 편집기로 OAS를 쉽게 작성할 수 있게 해준다.
    - Swagger UI: OAS 문서를 디플로이하고 브라우저에서 예쁘게 표시할 수 있도록 해준다(redoc으로 대체 가능).
    - Swagger Codegen: OAS에 맞게 서버나 클라이언트의 stub code를 생성해 준다.
  - Redoc
    - OAS 파일을 읽어서 디플로이 해주는 도구로 Swagger-UI와 비슷한 역할을 수행한다.
    - 설치와 사용이 간편하다는 장점이 있지만, Swagger-UI와 달리 브라우저에서 API TEST 기능을 해볼수는 없다는 단점이 있다.



- FastAPI는 OpenAPI를 기반으로 한다.

  - 이를 통해 FastAPI에서 작성한 API들을 자동으로 문서화가 가능하다.
  - Swagger UI가 제공하는 문서와 Redoc이 제공하는 문서를 모두 자동으로 만들어 준다.
    - 각기 `/docs`, `/redoc` 으로 접근하면 된다.

  - 문서 생성 과정
    - fastapi 어플리케이션(인스턴스)은 OpenAPI 스키마(title, description, tags 등)를 반환하는 `.openapi()`라는 메서드를 가지고 있다.
    - application 인스턴스가 생성될 때,  `openapi_url`에 등록된 url(기본값은 `/openapi.json`)도 함께 등록된다.
    - 해당 url에 요청을 보내면 openapi 스키마 정보를 반환한다.
    - `.openapi()`는 등록된 스키마 정보가 있는지 확인해서 있으면 반환해주는 역할만 할 뿐이고, 실제 스키마 생성은 `.get_openapi()`메서드에서 이루어진다.



- 기본 예시

  - 코드 작성하기

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  # fastapi 인스턴스를 생성될 때 openapi_url에 등록된 url(이 경우 /openapi.json)도 함께 등록된다.
  app = FastAPI() 
  
  @app.get("/hello")
  def hello():
      return "Hello!"
  
  @app.get("/world")
  def world():
      return "World!"
  
  if __name__ == '__main__':
      uvicorn.run(app, host='0.0.0.0', port=8000)
  ```

  - `/openapi.json`
    - openapi 스키마 및 각 endpoint에 대한 정보가 반환된다.

  ```json
  // curl "localhost:8000/openapi.json"
  
  {
    "openapi": "3.0.2",
    "info": {
      "title": "FastAPI",
      "version": "0.1.0"
    },
    "paths": {
      "/hello": {
        "get": {
          "summary": "Hello",
          "operationId": "hello_hello_get",
          "responses": {
            "200": {
              "description": "Successful Response",
              "content": {
                "application/json": {
                  "schema": {}
                }
              }
            }
          }
        }
      },
      "/world": {
        "get": {
          "summary": "World",
          "operationId": "world_world_get",
          "responses": {
            "200": {
              "description": "Successful Response",
              "content": {
                "application/json": {
                  "schema": {}
                }
              }
            }
          }
        }
      }
    }
  }
  ```

  - `/docs`

  ![image-20220110140654146](open_api.assets/image-20220110140654146.png)

  - `/redoc`

  ![image-20220110140737431](open_api.assets/image-20220110140737431.png)







## 확장

- openapi 스키마 변경하기

  - fastapi app 인스턴스를 생성할 때, openapi 스키마 정보를 변경할 수 있다.
  - 아래와 같이 인스턴스를 생성할 때 아무 값도 넣지 않으면 전부 기본값으로 설정된다.

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  if __name__ == '__main__':
      uvicorn.run(app, host='0.0.0.0', port=8000)
  ```

  - 결과

  ```json
  // /openapi.json
  {"openapi":"3.0.2","info":{"title":"FastAPI","version":"0.1.0"},"paths":{}}
  ```

  - `docs`

  ![image-20220110145508722](open_api.assets/image-20220110145508722.png)

  - 스키마 변경하기
    - 아래와 같이 FastAPI 인스턴스 생성시에 변경하고자 하는 스키마 값들을 설정해준다.

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI(
      title="My OpenAPI Doc",
      version="0.0.1",
      openapi_url="/myopenapi",
      description="My First OpenAPI Doc")
  
  if __name__ == '__main__':
      uvicorn.run(app, host='0.0.0.0', port=8000)
  ```

  - 결과

  ```json
  // /myopenapi
  {"openapi":"3.0.2","info":{"title":"My OpenAPI Doc","description":"My First OpenAPI Doc","version":"0.0.1"},"paths":{}}
  ```

  - `/docs`

  ![image-20220110145449246](open_api.assets/image-20220110145449246.png)

