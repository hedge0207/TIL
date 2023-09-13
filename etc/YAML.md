- 변수 선언(alias)

  - `&`기호로 변수를 사용하고, `*`기호로 변수를 사용할 수 있다.

  - `<<`를 사용하여 대입이 가능하다.

  ```yaml
  region: &default_region
    "name":"Seoul"
    "country":"Korea"
  
  people:
    - name: "김철수"
    <<: *default_region
  ```

  