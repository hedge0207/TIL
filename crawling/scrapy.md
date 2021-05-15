# scrapy

-  scrapy

  - 웹 크롤링을 위한 python 패키지
    - python으로 작성되었다.
    - spider를 작성해서 크롤링을 한다.
    - 프레임워크에 가깝다.
  - beautiful soup과 비교
    - beautiful soup은 자체적으로 웹 사이트를 크롤링 할 수 없다.
    - `urlib2`와 `requests`를 사용하여 HTML 소스를 가져와야만 한다.

  |          | Beautiful Soup                          | Scrapy                               |
  | -------- | --------------------------------------- | ------------------------------------ |
  | 진입장벽 | 쉽다                                    | 비교적 어렵다                        |
  | 자료량   | 부족하다                                | 많다                                 |
  | 확장성   | 확장성이 낮다.                          | middlware를 커스터마이징 할 수 있다. |
  | 성능     | multiprocessing을 사용하면 매우 빠르다. | 빠른 편이다.                         |

  - 설치

  ```bash
  pip install scrapy