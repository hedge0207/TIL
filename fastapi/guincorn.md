- gunicorn으로 여러 개의 워커 실행하기

  - fastapi는 내부적으로 uvicorn을 사용한다.
    - uvicorn은 ASGI 서버로 비동기적인 처리를 처리할 수 있다는 장점이 있다.
    - 그러나 single process이기에 한 번에 여러 요청을 처리해야 하는 상용 환경에서 사용하기에는 무리가 있다.
  - gunicorn은 WSGI 서버이다.
    - WSGI 서버이기에 비동기 요청은 처리가 불가능하다.
    - gunicorn은 WSGI 서버이면서 process manager의 역할도 한다.
    - 즉 클라이언트로부터 들어온 요청을 여러 프로세스로 분배하는 역할을 한다.
  - uvicorn과 gunicorn을 함께 사용하면 비동기 처리와 multi processing이라는 각자의 이점을 모두 누릴 수 있다.
    - 상기했듯 gunicorn은 process manager의 역할도 한다.
    - 따라서 복수의 uvicorn worker process를  gunicorn에 등록하면, gunicorn에 요청이 들어올 때 마다 gunicorn이 각 uvicorn worker process에 전달하여 처리하게 할 수 있다.
    - uvicorn worker는 gunicorn으로 부터 받은 정보를 fastapi에서 사용할 수 있도록 ASGI 표준에 맞게 변환하고 처리한다.
    - uvicorn도 이를 염두에 두고 개발하여 `uvicorn.workers.UvicornWorker`에 gunicorn에 등록할 수 있는 UvicornWorker class를 작성해 놓았다.
  - 설치
    - uvicorn의 확장 패키지들도 함께 받는다(`uvicorn[standard]`)

  ```bash
  $ pip install uvicorn[standard] gunicorn 
  ```

  - 실행

  ```bash
  $ gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
  ```

  - 옵션

    - `main:app`: `main`은 실행하려는 python module 이름을 이고, `app`은 fastapi application의 이름이다.

    - `--workers`: 실행하려는 uvicorn worker의 개수를 적는다.
    - `--worker-class`: worker process로 사용하려는 worker class를 입력한다.
    - `--bind`: gunicorn이 요청을 받은 IP와 port를 입력한다.

  - uvicorn 역시 process manager로 사용하는 것이 가능하다.

    - 그러나 worker process들을 관리하는 능력이 아직까지는 gunicorn에 비해 제한적이므로 gunicorn을 process manager로 사용하는 것이 더 낫다.

  ```bash
  $ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
  ```




- Logging

  - `--log-config` 옵션으로 logging을 위한 configuration 파일을 지정할 수 있다.
  - Python logging mudule과 동일한 형식으로 configuration 파일을 작성하면 된다.
    - `gunicorn.access` logger로 gunicron의 access log를 처리하고, `gunicorn.error` logger로 gunicorn의 error log를 처리한다.

  ```conf
  # logging.conf
  [loggers]
  keys=root,gunicorn.access
  
  [handlers]
  keys=consoleHandler
  
  [formatters]
  keys=simpleFormatter
  
  [logger_root]
  level=INFO
  handlers=consoleHandler
  
  [logger_gunicorn.access]
  level=INFO
  handlers=consoleHandler
  qualname=gunicorn.access
  
  [handler_consoleHandler]
  class=StreamHandler
  level=INFO
  formatter=simpleFormatter
  args=(sys.stdout,)
  
  [formatter_simpleFormatter]
  format=%(asctime)s - %(levelname)s - %(name)s - %(message)s
  ```

  - Fastapi app 생성

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  
  @app.get("/")
  def hello():
      return
  
  if __name__ == "__main__":
      uvicorn.run(app)
  ```

  - gunicorn으로 app 실행

  ```bash
  $ gunicorn main:app --bind 0.0.0.0:8080  --worker-class uvicorn.workers.UvicornWorker --log-config logging.conf
  ```

  - log 확인

  ```bash
  $ curl localhost:8080
  # 2023-06-21 10:26:44,125 - INFO - uvicorn.access - 127.0.0.1:12345 - "GET / HTTP/1.1" 200
  ```

  

  