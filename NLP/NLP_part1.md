> https://wikidocs.net/book/2155 참고



# 텍스트 전처리

## Tokenization

- Tokenization
  - 주어진 말뭉치(corpus)를 token이라 불리는 단위로 나누는 작업이다.
  - Token의 단위는 상황에 따라 다르지만 보통 의미 있는 단위로 token을 정의한다.
    - 예를 들어 단어 단위로 나누면 word tokenization, 문장 단위로 나누면 sentence tokenization이다.



- Tokenizing시에 고려할 사항들
  - 구두점이나 특수 문자를 어떻게 처리할 것인가.
    - 구두점이나 특수 문자를 무조건 제거해선 안된다.
    - Ph.D 처럼 단어 자체에 구두점이 있는 경우가 있다.
    - 3.141592와 같이 소수를 나타내는 경우에도 구두점이 사용된다.
  - 줄임말로 구성된 단어와 띄어쓰기는 어떻게 할 것인가.
    - 영어권 언어에서는 I'm과 같이 `'`를 사용하여 단어를 줄여서 사용하기도 한다(이 때 `'` 뒤에 오는 말을 접어(clitic)라고 한다).
    - 또한 New York과 같이 하나의 단어 내에 띄어쓰기가 있는 경우도 있다.



- 한국어 tokenizing

  - 교착어
    - 영어의 경우 New York이나 I'm 등과 같은 일부 경우만 제외하면 띄어쓰기를 기준으로 tokenizing을 해도 단어 토큰화가 가능하다.
    - 반면에 한국어는 조사, 어미 등을 붙여서 말을 만드는 교착어이기 때문에 띄어쓰기를 기준으로 tokenizing을 할 경우 단어 토큰화가 아닌 어절 토큰화가 되어버린다.
    - 따라서 조사를 분리해줄 필요가 있다.
  - 형태소(morpheme)
    - 뜻을 가진 가장 작은 말의 단위를 의미한다.
    - 자립 형태소: 체언(명사, 대명사, 수사), 수식언(관형사, 부사), 감탄사와 같이 접사, 어미, 조사와 무관하게 자립하여 사용할 수 있는 형태소로, 그 자체로 단어가 된다.
    - 의존 형태소: 접사, 어미, 조사, 어간과 같이 다른 형태소와 결합하여 사용되는 형태소이다.

  - 한국어는 띄어쓰기가 잘 지켜지지 않는다.
    - 한국어는 많은 경우에 띄어쓰기가 잘 지켜지지 않는다.
    - 영어권 언어에 비해 띄어쓰기가 어렵고, 띄어쓰기를 사용하지 않아도 글일 이해하는 데 큰 어려움이 없기 때문이다.



- Part-of-speech tagging
  - 단어는 표기는 같지만 품사에 따라 의미가 달라지기도 한다.
    - 예를 들어 못이라는 단어는 명사로는 무언가를 고정하는 데 사용하는 물건을 의미하지만 부사로서는 어떤 동사를 할 수 없다는 것을 의미한다.
    - 따라서 단어의 의미를 제대로 파악하기 위해서는 단어의 품사를 잘 파악해야한다.
  - 품사 태깅은 각 단어가 어떤 품사로 쓰였는지를 구분하는 작업이다.





## Cleaning & Normalization

- 정제(cleaning)

  - Noise data
    - 자연어가 아니면서 아무 의미도 갖고 있지 않은 글자들을 의미한다.
    - 분석하고자 하는 목적에 맞지 않는 불필요한 단어들을 의미하기도 한다.
  - 갖고 있는 말뭉치에서 noise data를 제거하는 과정이다.
    - Tokenization에 방해가 되는 부분들을 배제시키기 위해서 tokenizing 전에 수행되기도 하고, tokenizing 이후에 남아있는 noise들을 제거하기 위해 지속적으로 이루어지기도 한다.
    - 완벽한 정제 작업은 어려운 일이므로 대부분의 경우 타협점을 찾아서 진행한다.

  - 영어권 언어의 경우 길이가 짧은 단어를 삭제하는 것으로도 어느 정도 noise data를 제거하는 것이 가능하지만, 한국어의 경우에는 그렇지 않다.
    - 한국어에는 한자어가 많기 때문에 차, 용, 술, 글 등 한 글자로도 단어가 되는 경우가 많기 때문이다.
  - 불용어(Stopword)
    - 사용하지 않을 단어들을 의미한다.
    - 한국어의 경우 일반적으로 조사, 접속사 등을 제거한다.
  - 정규표현식을 사용하여 정제하기도 한다.



- 정규화(Normalization)
  - 표현 방법이 다른 단어들을 통합시켜 같은 단어로 만드는 과정이다.
    - 예를 들어 USA와 US는 같은 의미를 가지므로 하나의 단어로 정규화 할 수 있다.
  - 대소문자 통합
    - 대소문자를 통합하여 단어의 개수를 줄일 수 있다.
    - 대문자는 문장의 맨 앞과 같은 특수한 상황에서만 사용되기에 일반적으로 대문자를 소문자로 변환하는 방식으로 대소문자 통합을 진행한다.
    - 단 무작정 진행해서는 안된다.
    - 예를 들어 미국을 의미하는 US와 우리를 뜻하는 us는 구분되어야 하기 때문이다.
    - 일반적으로 고유 명사는 대문자를 유지한다.
  - 어간 추출(Stemming)
    - 형태소는 어간과 접사가 존재하는데, 어간(stem)은 단어의 의미를 담고 있는 핵심적인 부분, 접사(affix)는 단어에 추가적인 의미를 주는 부분이다.
    - 어간을 추출하는 작업을 어간 추출이라 하며 섬세한 작업은 아니기 때문에 어간 추출 후에 나오는 결과는 사전에 존재하지 않는 단어일 수도 있다.
  - 표제어 추출(lemmatization)
    - 표제어(Lemma) 추출은 단어들로부터 표제어를 찾아가는 과정이다.
    - 단어들이 다른 형태를 가지더라도, 그 뿌리 단어를 찾아가서 단어의 개수를 줄일 수 있는지를 판단한다.
    - 예를 들어 am, are, is, were 등은 모두 다른 형태를 가지고 있지만 결국 be라는 뿌리 단어를 공유한다.
    - 형태학적 파싱을 통해 어간과 접사를 분리하는 방식으로 표제어를 추출한다.
    - 어간 추출 보다 섬세한 방식이다.



- 한국어의 어간 추출(stemming)

  - 한국어는 5언 9품사의 구조를 가지고 있다.
    - 이 중 용언에 해당하는 동사와 형용사는 어간(stem)과 어미(ending)의 결합으로 구성된다.

  | 언     | 품사               |
  | ------ | ------------------ |
  | 체언   | 명사, 대명사, 수사 |
  | 수식언 | 관형사, 부사       |
  | 관계언 | 조사               |
  | 독립언 | 감탄사             |
  | 용언   | 동사, 형용사       |

  - 활용(conjugation)
    - 활용이란 어간과 어미를 가지는 것을 말하며, 한국어뿐 아니라 인도유럽어에서도 볼 수 있는 언어적 특징이다.
    - 어간(stem): 용언을 활용할 때, 원칙적으로 모양이 변하지 않는 부분(때로는 모양이 변하기도 한다), 활용에서 어미에 선행하는 부분을 의미한다.
    - 어미(ending): 용언의 어간 뒤에 붙어서 활용에 따라 변하는 부분이며, 여러 문법적 기능을 수행한다.
  - 규칙 활용
    - 어간이 어미를 취할 때, 어간의 모습이 일정한 경우이다.
    - 예를 들어 "잡"이라는 어간과 "다"라는 어미가 합쳐져 "잡다"가 될 경우 어간의 모습이 변하지 않았으므로 규칙 활용이다.
    - 규칙 활용의 경우 단순히 어미를 분리해주면 어간이 추출된다.
  - 불규칙 활용
    - 어간이 어미를 취할 때, 어간의 모습이 바뀌거나 어미가 특수한 어미일 경우이다.
    - 어간의 모습이 바뀌는 경우: "걷"이라는 어간은 어미에 따라 "걸"이 되기도 한다(e.g. 걷다, 걸어서).
    - 특수한 어미를 취하는 경우: `푸르+어 → 푸르러`





## Integer Encoding

- Integer Encoding
  - 단어를 고유한 정수에 mapping시키는 기법이다.
    - 컴퓨터는 text보다 숫자를 더 잘 처리할 수 있다.
    - 따라서 자연어 처리에서는 text를 숫자로 바꾸는 여러 가지 기법들을 사용하는데, 다양한 기법을 적용하기 위한 첫 단계가 바로 정수 인코딩이다.
  - Integer encoding 과정
    - 단어 집합(vocabulary)을 만들고 빈도수 순으로 내림차순 정렬한다.
    - 빈도수가 높은 단어부터 차례대로 정수 번호를 부여한다.



- Python의 dictionary를 사용하여 구현하기

  - 먼저, 아래와 같이 원본 text를 가지고 setence tokenizing을 수행한다.

  ```python
  from collections import defaultdict
  
  from nltk.tokenize import sent_tokenize, word_tokenize
  from nltk.corpus import stopwords
  
  
  raw_text = """Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.
  Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), 
  object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library."""
  
  setences = sent_tokenize(raw_text)
  ```

  - 정제 및 정규화와 함께 word tokenizing을 수행한다.

  ```python
  # 단어 집합을 저장할 dictionary
  vocabulary = defaultdict(int)
  preprocessed_sentences = []
  # stopword를 생성한다.
  stop_words = set(stopwords.words("english"))
  
  for sentence in setences:
      # setence를 word 단위로 tokenizing한다.
      words = word_tokenize(sentence)
      # 유효한 token을 저장할 list
      valid_tokens = []
      for word in words:
          # 소문자로 변환한다.
          word = word.lower()
          # token이 불용어가 아니고, 길이가 3이상이면 유효한 token이다.
          if word not in stop_words and len(word) > 2:
              valid_tokens.append(word)
              vocabulary[word] += 1
      
      preprocessed_sentences.append(valid_tokens)
  ```

  - `vocabulary`를 빈도 순으로 정렬하고, 빈도에 따라 정수를 부여한다.
    - 이 과정에서 빈도가 1 이하인 token은 모두 제외시킨다.

  ```python
  vocabulary = sorted(vocabulary.items(), key=lambda x:x[1], reverse=True)
  
  word_to_index = {}
  for i in range(len(vocabulary)):
      token, frequency = vocabulary[i]
      if frequency > 1:
      	word_to_index[token] = i
  
  print(word_to_index)			# {'programming': 0, 'python': 1, 'language': 2}
  ```

  - 이제 이전에 문장 단위로 유효한 token들을 저장한 `preprocessed_setences`에서 요소들을 하나씩 빼어 mapping되는 정수로 encoding한다.
    - 예를 들어 `["python", "programming", "language"]`는 `[1, 0, 2]`로 encoding된다.
    - 문제는 위에서 빈도가 1 이하인 token을 제거했으므로 `word_to_index`에 포함되지 않는 단어가 있을 수 있다.
    - 이를 Out-Of-Vocabulary(OOV)문제라 부른다.
    - OOV를 해결하기 위해 `word_to_index`의 마지막 정수에 1을 더한 값을 `word_to_index`에 포함되지 않는 단어의 정수와 mapping시킨다.

  ```python
  OOV = len(word_to_index)
  encoded_sentences = []
  for sentence in preprocessed_sentences:
      encoded_sentence = []
      for word in sentence:
          if word_to_index.get(word):
              encoded_sentence.append(word_to_index[word])
          else:
              encoded_sentence.append(OOV)
      encoded_sentences.append(encoded_sentence)
  ```



- `nltk` package의 `FreqDist`를 사용하면 보다 간편하게 각 token의 빈도를 구할 수 있다.

  - 코드

  ```python
  from nltk.tokenize import sent_tokenize, word_tokenize
  from nltk.corpus import stopwords
  from nltk import FreqDist
  
  import numpy as np
  
  
  class IntegerEncoder:
      def __init__(self, raw_text: str):
          self.raw_text = raw_text
          self.preprocessed_sentences = []
          self._preprocess_text()
  
      def _preprocess_text(self):
          setences = sent_tokenize(self.raw_text)
          stop_words = set(stopwords.words("english"))
  
          for sentence in setences:
              words = word_tokenize(sentence)
              
              valid_tokens = []
              for word in words:
                  word = word.lower()
                  if word not in stop_words and len(word) > 2:
                      valid_tokens.append(word)
              
              self.preprocessed_sentences.append(valid_tokens)
      
      def _map_token(self):
          vocabulary = FreqDist(np.hstack(self.preprocessed_sentences))
          word_to_index = {}
          for i, word in enumerate(vocabulary, 1):
              frequency = vocabulary[word]
              if frequency > 1:
                  word_to_index[word] = i
          
          return word_to_index
      
      def encode(self):
          word_to_index = self._map_token()
          OOV = len(word_to_index) + 1
          encoded_sentences = []
          for sentence in self.preprocessed_sentences:
              encoded_sentence = []
              for word in sentence:
                  if word_to_index.get(word):
                      encoded_sentence.append(word_to_index[word])
                  else:
                      encoded_sentence.append(OOV)
              encoded_sentences.append(encoded_sentence)
          
          return encoded_sentences
      
      def show_result(self, encoded_sentences):
          for i, sentence in enumerate(self.preprocessed_sentences):
              for word in sentence:
                  print("|", word, end=" ")
              print("|")
  
              for i, encoded_value in enumerate(encoded_sentences[i]):
                  print("|", encoded_value, end=" "*len(sentence[i]))
              print("|")
              print("-"*150)
  
          return encoded_sentences
  
  
  if __name__ == "__main__":
      raw_text = """Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.
                  Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), 
                  object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library."""
      integer_encoder = IntegerEncoder(raw_text)
      integer_encoder.show_result(integer_encoder.encode())
  ```

  - `FreqDist(np.hstack(self.preprocessed_sentences))`
    - `FreqDist`는 `collections.Counter` 객체를 반환한다.
    - `np.hstack()`은 중첩된 list를 일차원 list로 변경해서 반환하는 함수이다.



- Keras를 사용한 encoding

  - Keras는 기본적인 text 전처리를 위한 도구들을 제공한다.
    - 아래와 같이 `Tokenizer`객체의 `fit_on_texts()` method를 실행하고, `word_index` attribute를 확인하면, 빈도수가 높은 순으로 index가 부여되는 것을 볼 수 있다.
    - `word_counts` attribute에는 각 token이 몇 번 등장했는지가 저장되어 있다.

  ```python
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts(preprocessed_sentences)
  print(tokenizer.word_index)
  print(tokenizer.word_counts)
  
  
  """
  {'programming': 1, 'python': 2, 'language': 3, 'high-level': 4, 'general-purpose': 5, ...}
  OrderedDict([('python', 2), ('high-level', 1), ('general-purpose', 1), ('programming', 3), ...])
  """
  ```

  - `texts_to_sequences()`는 입력으로 들어온 corpus를 index로 변환까지 해준다.

  ```python
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts(preprocessed_sentences)
  print(tokenizer.texts_to_sequences(preprocessed_sentences))
  
  """
  [[2, 4, 5, 1, 3], [6, 7, 8, 9, 10, 11, 12, 13], [2, 14, 15, 16], ...]
  """
  ```

  - `Tokenizer` 객체 생성시에 `num_words` parameter로 빈도수로 정렬한 token 중 상위 몇 개의 token을 사용할 것인지를 지정할 수 있다.
    - 주의할 점은 사용하려는 숫자에 1을 더해야 한다는 점으로, 상위 5개를 사용할 것이라면 아래와 같이 6을 넣어야 1~5번 단어를 사용한다.
    - 이는 Keras tokenizer가 0번을 padding에 사용하기 때문이다.
    - 또한 `num_words` 값은 `texts_to_sequences()` method를 사용할 때만 적용되고, `word_index`, `word_counts` 등에는 적용되지 않는다.

  ```python
  vocab_size = 5
  tokenizer = Tokenizer(num_words=vocab_size+1) # 상위 5개 단어만 사용
  tokenizer.fit_on_texts(preprocessed_sentences)
  print(tokenizer.texts_to_sequences(self.preprocessed_sentences))
  ```

  - Keras tokenizer는 기본적으로 OOV를 아예 제거한다.
    - 만약 OOV를 보존하고 싶다면 `oov_token` parameter를 추가해야한다.
    - OOV의 index는 기본적으로 1이다.

  ```python
  vocab_size = 5
  tokenizer = Tokenizer(num_words=vocab_size+1, oov_token = 'OOV')
  tokenizer.fit_on_texts(preprocessed_sentences)
  print(tokenizer.texts_to_sequences(preprocessed_sentences))
  
  """
  [[3, 5, 1, 2, 4], [1, 1, 1, 1, 1, 1, 1, 1], [3, 1, 1, 1], [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2], [1, 1, 1, 1, 4, 1, 1, 1, 1]]
  """
  ```





## Padding

- 패딩(Padding)

  - 기계는 길이가 전부 동일한 문서들에 대해서는 하나의 행렬로 보고 한꺼번에 묶어서 처리할 수 있기 때문에 길이가 동일한 것이 좋다.
    - 자연어 처리를 하다보면 각 문장의 길이가 다를 수 있다.
    - 따라서 여러 문장의 길이를 임의로 동일하게 맞춰주는 작업이 필요할 수 있는데, 이를 패딩이라 한다.
  - 특정 문장을 기준으로, 해당 문장 보다 짧은 문장들에 PAD라 불리는 가상의 단어를 채워 넣어 길이를 맞춰준다.
    - 만약 PAD를 가리키는 숫자로 0을 사용한다면 zero padding이라 부른다.
    - 관례상 0으로 padding한다.
  - Numpy로 패딩하기

  ```python
  import numpy as np
  from tensorflow.keras.preprocessing.text import Tokenizer
  
  # 아래와 같이 각 길이가 다른 텍스트 데이터를
  preprocessed_sentences = [['python', 'high-level', 'general-purpose', 'programming', 'language'], ['design', 'philosophy', 'emphasizes', 'code', 'readability', 'use', 'significant', 'indentation'], ['python', 'dynamically', 'typed', 'garbage-collected'], ['supports', 'multiple', 'programming', 'paradigms', 'including', 'structured', 'particularly', 'procedural', 'object-oriented', 'functional', 'programming'], ['often', 'described', 'batteries', 'included', 'language', 'due', 'comprehensive', 'standard', 'library']]
  
  # 정수 인코딩을 수행한다.
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts(preprocessed_sentences)
  encoded = tokenizer.texts_to_sequences(preprocessed_sentences)
  print(encoded)
  # [[2, 4, 5, 1, 3], [6, 7, 8, 9, 10, 11, 12, 13], [2, 14, 15, 16], [17, 18, 1, 19, 20, 21, 22, 23, 24, 25, 1], [26, 27, 28, 29, 3, 30, 31, 32, 33]]
  
  # 모두 동일한 길이로 맞춰주기 위해 가장 길이가 긴 문장을 찾는다.
  max_len = max(len(item) for item in encoded)
  
  # 최대 길이보다 짧은 문장에는 PAD를 가리키는 0을 넣어준다.
  for sentence in encoded:
      while len(sentence) < max_len:
          sentence.append(0)
  
  padded_np = np.array(encoded)
  
  print(padded_np)
  ```

  - Keras로 padding하기
    - 기본적으로 앞에서부터 padding 값을 채워 나가며, `padding` parameter 값을 post로 줄 경우 뒤에서부터 채운다.

  ```python
  from tensorflow.keras.preprocessing.sequence import pad_sequences
  
  preprocessed_sentences = [['python', 'high-level', 'general-purpose', 'programming', 'language'], ['design', 'philosophy', 'emphasizes', 'code', 'readability', 'use', 'significant', 'indentation'], ['python', 'dynamically', 'typed', 'garbage-collected'], ['supports', 'multiple', 'programming', 'paradigms', 'including', 'structured', 'particularly', 'procedural', 'object-oriented', 'functional', 'programming'], ['often', 'described', 'batteries', 'included', 'language', 'due', 'comprehensive', 'standard', 'library']]
  encoded = tokenizer.texts_to_sequences(preprocessed_sentences)
  print(encoded)
  # [[2, 4, 5, 1, 3], [6, 7, 8, 9, 10, 11, 12, 13], [2, 14, 15, 16], [17, 18, 1, 19, 20, 21, 22, 23, 24, 25, 1], [26, 27, 28, 29, 3, 30, 31, 32, 33]]
  
  padded = pad_sequences(encoded, padding='post')
  print(padded)
  ```

  - 위에서는 가장 긴 문서의 길이를 기준으로 padding을 진행했지만, 꼭 그래야하는 것은 아니다.
    - 아래와 같이 `maxlen` parameter를 줘서 길이에 제한을 두고 padding하는 것도 가능하다.
    - 길이가 5보다 짧은 문서들은 0으로 패딩되고, 기존에 5보다 긴 부분은 손실된다.

  ```python
  padded = pad_sequences(encoded, padding='post', maxlen=5)
  ```

  - `value`로 0이 아닌 값으로 padding하도록 할 수 있다.

  ```python
  padded = pad_sequences(encoded, padding='post', value=last_value)
  ```





## One-Hot Encoding

- 사전 지식

  - 단어 집합(vocabulary)
    - 서로 다른 단어들의 집합을 의미한다.
    - Text에서 모든 단어를 중복 없이 모아놓으면 단어 집합이 된다.
    - 단어 집합에서는 apple, apples와 같이 다른 형태의 같은 단어도 다른 단어로 간주한다.
  - Encoding
    - 컴퓨터는 문자보다는 숫자를 더 잘 처리할 수 있다.
    - 이를 위해 자연어 처리에서는 문자를 숫자로 바꾸는 여러가지 기법들을 encoding이라 부른다.




- One-Hot Encoding이란

  - 단어 집합의 크기를 벡터의 차원으로 하고, 표현하고 싶은 단어의 index에 1의 값을 부여하고, 다른 index에는 0을 부여하는 단어의 벡터 표현 방식이다.
  - 이렇게 표현된 벡터를 One-Hot vector라 한다.

  ```python
  from konlpy.tag import Okt  
  from collections import Counter
  
  # 문장을 tokenizing한다.
  okt = Okt()
  tokens = okt.morphs("나는 나의 강아지를 사랑한다")  
  print(tokens)		# ['나', '는', '나', '의', '강아지', '를', '사랑', '한다']
  
  # 일반적으로 단어의 빈도수로 정렬하여 정수를 부여한다.
  tokens = sorted(Counter(tokens).items(), key=lambda i:i[1], reverse=True)
  word_to_index = {word[0]: i for i, word in enumerate(tokens)}
  print(word_to_index)	# {'나': 0, '는': 1, '의': 2, '강아지': 3, '를': 4, '사랑': 5, '한다': 6}
  
  # One-Hot vector를 생성한다.
  word = "강아지"
  one_hot_vector = [0]*(len(word_to_index))	# 모든 값을 0으로 초기화시킨다.
  index = word_to_index[word]
  one_hot_vector[index] = 1					# token에 해당하는 index만 1로 변경한다.
  print(one_hot_vector)						# [0, 0, 0, 1, 0, 0, 0]
  ```

  - Keras를 이용한 One-Hot Encoding
    - Keras package의 `to_categorical()` 메서드를 사용하면 보다 간단하게 구할 수 있다.

  ```python
  from tensorflow.keras.preprocessing.text import Tokenizer
  from tensorflow.keras.utils import to_categorical
  
  text = "가방 안에 가방, 그 안에 또 가방"
  
  # vocabulary를 생성한다.
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts([text])
  print(tokenizer.word_index)		# {'가방': 1, '안에': 2, '그': 3, '또': 4}
  
  # 일부 단어들로만 구성된 sub text를 정수 sequence로 변환
  sub_text = "그 안에 또 가방"
  encoded = tokenizer.texts_to_sequences([sub_text])[0]
  print(encoded)		# [3, 2, 4, 1]
  
  # 정수 encoding 된 결과를 가지고 One-Hot Encoding 실행
  one_hot = to_categorical(encoded)
  print(one_hot)
  
  """
  [[0. 0. 0. 1. 0.]	# index 3의 one-hot vector
   [0. 0. 1. 0. 0.]	# index 2의 one-hot vector
   [0. 0. 0. 0. 1.]	# index 4의 one-hot vector
   [0. 1. 0. 0. 0.]]	# index 1의 one-hot vector
  """
  ```

  - One-Hot Encoding에서는 단어의 개수가 늘어날 수록, vector를 저장하기 위해 필요한 공간이 계속 늘어난다.
    - 이를 vector의 차원이 늘어난다고 표현하는데, one-hot vector는 단어 집합의 크기가 곧 vector 차원 수가 된다.
    - 예를 들어 단어가 100개인 corpus를 가지고 one-hot vector를 만들면 모든 단어 각각은 모두 100개의 차원을 가진 vector가 된다.
    - 즉 모든 단어는 하나의 값만 1을 가지고, 99개의 값은 0의 값을 가지는 vector가 되는데, 이는 매우 비효율적이다.
  - 단어의 유사도를 표현할 수 없다.
    - 늑대, 호랑이, 강아지, 고양이라는 4개의 단어를 one-hot encoding하면 [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]이 된다.
    - 위 값만 보고서는 어떤 단어가 어떤 단어와 유사한지 파악할 수 없다.
    - 이는 특히 검색 시스템에서 연관 검색어와 같이 유사한 단어 기반의 기능을 구현하는데 문제가 될 수 있다.





## Data 분리하기

- Machine learning model을 학습시키고 평가하기 위해서는 data를 적절하게 분리하는 작업이 필요하다.
  - 지도 학습(Supervised Learning)은 정답이 적혀 있는 문제지를 학습시켜 추후에 정답이 없는 문제에서 정답을 예측할 수 있도록 하는 학습 방식이다.
    - 지도 학습의 훈련 데이터는 정답이 무언인지 맞춰야 하는 문제에 해당하는 데이터와 레이블이라고 부르는, 정답이 적혀 있는 데이터로 구성되어 있다.
    - Data를 적절히 분리해야 원할한 학습과 학습 후 test가 가능하다.
  - 예를 들어 10000개의 문제-답 쌍으로 이루어진 data가 있다고 해보자.
    - 10000개의 문제-답 쌍을 문제와 답으로 나누어야 한다.
    - 그리고 전체 data중 일부를 test 용 data로 다시 나눠야한다.
    - 결국 학습용 문제, test용 문제, 학습용 답, test용 답으로 전체 데이터를 4개로 나누어야한다.



- `zip`을 사용하여 분리하기

  - x가 문제, y가 답에 해당한다.

  ```python
  values = [['a', 1], ['b', 2], ['c', 3], ['d', 4], ['e', 5]]
  x, y = zip(*values)
  print(x)			# ('a', 'b', 'c', 'd', 'e')
  print(y)			# (1, 2, 3, 4, 5)
  ```

  - Pandas의 dataframe을 사용하여 분리하기

  ```python
  import pandas as pd
  
  columns = ['x', 'y']
  df = pd.DataFrame(values, columns=columns)
  print(df)
  """
     x  y        
  0  a  1        
  1  b  2        
  2  c  3        
  3  d  4        
  4  e  5
  """
  ```

  - Test data 분리하기
    - Scikit-learn의 `train_test_split()` method를 사용하면 간단하게 분리가 가능하다. 
    - 첫 번째 인자로 독립변수, 두 번째 인자로 종속변수를 받는다.
    - `test_size`에는 test용 data의 개수를 입력하는데, 1보다 작은 실수를 입력할 경우 비율을 나타낸다.
    - `random_state`로 받은 숫자를 기반으로 무선적으로 test용 data를 추출한다.

  ```python
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.4, random_state=1234)
  
  print(x_train)  # ['b', 'c', 'd']
  print(x_test)   # ['e', 'a']
  print(y_train)	# [2, 3, 4]
  print(y_test)	# [5, 1]
  ```






## 언어 모델

- Language Model(LM)
  - 언어라는 현상을 모델링하고자 단어 시퀀스(문장)에 확률을 할당하는 모델이다.
    - 언어 모델을 만드는 방법은 크게 통계를 이용한 방법과 인공 신경망을 이용한 방법이 있다.
    - 최근에는 통계를 이용한 방법 보다는 인공 신경망을 이용한 방법이 더 좋은 성능을 보여주고 있다.
  - Language Modeling
    - 주어진 단어들로부터 아직 모르는 단어를 예측하는 작업을 말한다.
    - 단어 시퀀스에 확률을 할당하게 하기 위해서 가장 보편적으로 사용되는 방법은 이전 단어들이 주어졌을 때 다음 단어를 예측하도록 하는 것이다.
  - 단어 시퀀스에 확률을 할당함으로써 보다 적잘한 문장을 판단한다.
    - 예를 들어 "쓰레기를 버렸다"와 "쓰레기를 비렸다"라는 두 문장 중에서 "쓰레기를 버렸다가"에 더 높은 확률을 부여하도록 학습시켜, 이를 보다 적절한 문장이라고 판단하게 한다.
  - 주어진 이전 단어들로부터 다음 단어 예측하기
    - 하나의 단어를 w, 단어 시퀀스를 대문자 W라고 한다면, n개의 단어가 등장하는 단어 시퀀스 W의 확률은 아래와 같다.
    - $$P(W)=P(w_1,w_2,w_3,...,w_n)$$
    - n-1개의 단어가 나열된 상태에서 n번째 단어의 확률은 아래와 같다.
    - $$P(w_n|w_1,...,w_{n-1})$$
    - 전체 단어 시퀀스 W의 확률은 모든 단어가 예측되고 나서야 알 수 있으므로 단어 시퀀스의 확률은 다음과 같다.
    - $$P(W)=P(w_1,w_2,w_3,...,w_n) = \prod_{i=1}^n P(w_i|w_1,...,w_{i-1})$$



- 조건부 확률(Conditional Probability)

  - 조건부 확률은 두 확률 P(A), P(B)에 대해서 아래와 같은 관계를 갖는다.
    - $$P(B|A)=P(A,B)/P(A)$$
    - $$P(A,B)=P(A)P(B|A)$$
  - 조건부 확률의 연쇄 법칙
    - 위 관계를 더 많은 확률에 대해서 일반화하면 아래와 같다.
    - $$P(x_1,x_2,...,x_n)=P(x_1)P(x_2|x_1)P(x_3|x_1,x_2)...P(x_n|x_1...x_{n-1})= \prod_{i=1}^n P(x_i|x_1,...,x_{i-1})$$

  - 예시 data
    - 아래 표와 같은 data가 있다.
    - A = 학생이 남학생인 사건
    - B = 학생이 여학생인 사건
    - C = 학생이 중학생인 사건
    - D = 학생이 고등학생인 사건

  |          | 남   | 여   | 계   |
  | -------- | ---- | ---- | ---- |
  | 중학생   | 110  | 70   | 180  |
  | 고등학생 | 90   | 130  | 220  |
  | 계       | 200  | 200  | 400  |

  - 예시
    - 고등학생 중 한 명을 뽑았을 때(D), 남학생일 확률(A)을 구하면 아래와 같다.
    - 학생을 뽑았을 때 고등학생일 확률: $$P(D)=220/400$$
    - 학생을 뽑았을 때, 고등학생이면서 남학생일 확률: $$P(A \cap B)=90/400$$
    - 고등학생중 한 명(조건)을 뽑았을 때 남학생일 확률: $$P(A|D)=90/220=P(A \cap B)/P(D)=(90/400)/(220/400)=90/220$$



- 통계적 언어 모델(Statistical Language Model, SLM)

  - 조건부 확률을 사용하여 확률을 구한다.
    - 문장에서의 각 단어는 문맥이라는 관계로 인해 이전 단어의 영향을 받아 나온 단어이고, 모든 단어로부터 하나의 문장이 완성된다.
    - 따라서 조건부  확률을 사용하여 문장의 확률을 구할 수 있다.
  - 문장에 대한 확률
    - "He is interested in baseball"이라는 문장의 확률 P(He is interested in baseball)를 식으로 표현하면 아래와 같다.
    - 문장의 확률을 구하기 위해서 각 단어에 대한 예측 확률들을 곱한다.

  $$
  P(He\ \ is\ \ interested\ \ in\ \ baseball)=\\
  P(He) \times P(is|He) \times P(interested|He\ \ is) \times P(in|He\ \ is\ \ interested) \times P(baseball|He\ \ is\ \ interested\ \ in)
  $$

  - 카운트 기반의 접근

    - 이전 단어로부터 다음 단어에 대한 확률을 구하기 위해 카운트를 기반으로 확률을 계산한다.

    - "He is interested"가 나왔을 때 뒤에 "in"이 나올 확률인 $$P(in|He\ \ is\ \ interested)$$는 아래와 같이 구한다.
    - 예를 들어 기계가 학습한 corpus data에서 He is interested가 100번 등장했는데 그 다음에 in이 등장한 경우가 80번이라면 $$P(in|He\ \ is\ \ interested)$$는 80%가 된다.

    $$
    P(in|He\ \ is\ \ interested)={count(He\ \ is \ \ interested\ \ in) \over count(He\ \ is \ \ interested)}
    $$

  - 희소 문제(Sparsity Problem)

    - 언어 모델은 실생활에서 사용되는 언어의 확률 분포를 근사 모델링한다.
    - 현실에서도 정확히 알 수는 없지만 "He is interested"가 나왔을 때 뒤에 in이 등장할 확률이라는 것이 존재하는데, 이를 실제 자연어의 확률 분포 혹은 현실에서의 확률 분포라고 명명해보자.
    - 많은 corpus를 학습시켜 언어 모델을 통해 현실에서의 확률 분포를 근사하는 것이 언어 모델의 목표이다.
    - 그런데, 카운트 기반으로 접근할 경우 기계가 훈련하는 data는 정말 방대한 양이 필요하다.
    - 예를 들어 현실에서는 $$P(in|He\ \ is\ \ interested)$$의 확률이 매우 높다고 하더라도, 기계가 학습한 corpus에 He is interested in이라는 단어 시퀀스가 없었다면, 이 단어 시퀀스에 대한 확률은 0이 된다.
    - 또한 He is interested라는 시퀀스가 없었다면 분모가 0이 되어 확률이 정의되지 않는다.
    - 위와 같이 충분한 데이터를 관측하지 못하여 언어를 정확히 모델링하지 못하는 문제를 희소 문제라 하며, 카운트 기반 접근의 한계이다.
    - 이러한 한계로 인해 결국 언어 모델의 트렌드는 통계적 언어 모델에서 인공 신경망 언어 모델로 넘아가게 된다.



- N-gram 언어 모델(N-gram Language Model)

  - N-gram 언어 모델 역시 카운트에 기반한 통계적 접근을 사용하므로 SLM의 일종이다.

    - 다만 모든 단어를 고려하는 것이 아니라 일부 단어만 고려하는 접근법을 사용한다.
    - 이 때 일부 단어를 몇 개 보느냐를 결정하는데, 이 개수가 n-gram에서 n의 값이 된다.

  - Corpus에서 카운트하지 못하는 경우를 줄이는 방식으로 동작한다.

    - SLM의 한계는 훈련 corpus에서 확률을 계산하고 싶은 문장이나 단어가 없을 수 있다는 점이다.
    - 그리고 확률을 계산하고자 하는 문장이 길어질수록 갖고 있는 corpus에서 해당 문장이 존재하지 않을 가능성이 높아진다(즉 카운트할 수 없을 가능성이 높아진다).
    - 그런데 아래와 같이 참고하는 단어들을 줄이면 카운트를 할 가능성을 높일 수 있다. 
    - 즉 He is interested가 나왔을 때 in이 나왈 확률을 그냥 interested가 나왔을 때 in이 나올 확률로 생각하는 것이다.

    - $$P(in|He\ \ is\ \ interested) \approx P(in|interested)$$
    - 즉, 앞의 모든 단어를 전부 포함해서 카운트하는 것이 아니라, 앞 단어 중 임의의 개수만 포함해서 카운트하여 근사하는 방식이다.

  - N-gram

    - 이 때 몇 개의 단어를 포함시켜 카운트 할 것인지를 정해야 하는데, n-gram의 n이 뜻 하는 것이 몇 개의 단어를 포함시킬지이다.
    - n-gram은 n개의 연속적인 단어 나열을 의미한다.
    - 갖고 있는 corpus를 n개의 단어 뭉치 단위로 끊어서 이를 하나의 token으로 간주한다.
    - n이 1일 때는 유니그램, 2일 때는 바이그램, 3일 때는 드라이그램이라고 하고, 4이상일 때는 gram 앞에 그대로 숫자를 붙여서 명명한다.

  | n        | tokens                                                     |
  | -------- | ---------------------------------------------------------- |
  | unigrams | he, is, interested, in, baseball                           |
  | bigrams  | he is, is interested, interested in, in baseball           |
  | trigrams | hi is interested, is interested in, interested in baseball |

  - n-gram을 통한 언어 모델에서는 다음에 나올 단어의 예측은 오직 n-1개의 단어에만 의존한다.
    - 예를 들어 He is interested 다음에 나올 단어를 예측하고자 할 때 trigram를 이용한 언어 모델을 사용한다고 가정해보자.
    - 이 경우 다음에 올 단어를 예측하는 것은 n-1에 해당하는 앞의 2개 단어만을 고려한다.
    - 즉 is interested만 고려하여 아래와 같이 구한다.
    - 이 때, is interested가 corpus에서 100번 등장했고, is interested in이 600번, is interested to가 200번 등장했다면, in이 등장할 확률이 60%로 가장 높으므로 in이 더 적잘하다고 판단하게 된다.

  $$
  P(in|is\ \ interested)={count(is \ \ interested\ \ w) \over count(is \ \ interested)}
  $$

  - N-gram Language Model의 한계
    - 앞의 단어 몇 개만 고려하므로 본래 의도에 맞는 단어를 선택하지 못할 확률이 높아므로, 전체 문장을 고려한 언어 모델보다는 정확도가 떨어질 수 밖에 없다
    - 희소 문제가 여전히 존재한다.
    - n을 크게 할 수록 정확도는 높아지지만 희소 문제가 발생할 가능성도 높아지고, 모델 사이즈가 커진다는 문제가 있다.



- Perplexity(PPL)

  - 모델 내에서 자신의 성능을 수치화하여 결과를 내놓는 평가 지표이다.

    - PPL이 낮을 수록 언어 모델의 성능이 좋다는 것을 의미한다.

  - PPL은 문장의 길이로 정규화된 문장 확률의 역수이다.

    - 문장 W의 길이가 N이라고 했을 때 PPL은 다음과 같다.

    $$
    PPL(W) = P(w_1,w_2,w_3,...,w_n)^{-{1 \over N}}=\sqrt[N]{1 \over P(w_1,w_2,...,w_N)}
    $$

    

    - 문장의 확률에 체인룰을 적용하면 아래와 같다.

    $$
    PPL(W) = \sqrt[N]{1 \over P(w_1,w_2,...,w_N)} = \sqrt[N]{1 \over \prod_{i=1}^n P(x_i|x_1,...,x_{i-1})}
    $$

    

    - 여기에 bigram을 적용하면 아래와 같다.

    $$
    PPL(W) = \sqrt[N]{1 \over \prod_{i=1}^n P(x_i|x_{i-1})}
    $$

  - 분기 계수(Branching factor)

    - PPL은  선택할 수 있는 가능한 경우의 수를 의미하는 분기계수이다.
    - PPL은 언어 모델이 특정 시점에서 평균적으로 몇 개의 선택지를 가지고 고민하고 있는지를 의미한다.
    - 예를 들어 어떤 언어 모델의 PPL이 10이라면 해당 언어 모델은 다음 단어를 예측하는 모든 시점(time step) 마다 평균적으로 10개의 단어를 가지고 어떤 것이 정답인지 고민하고 있다고 볼 수 있다.

  - PPL 사용시 주의사항

    - PPL이 낮다는 것은 테스트 데이터 상에서 높은 정확도를 보인다는 것만을 의미한다. 
    - 사람이 직접 느끼기에 좋은 언어모델이라는 것을 의미하지는 않는다.
    - 또한 언어 모델의 PPL은 테스트 데이터에 의존하므로 두 개 이상의 언어 모델을 비교할 때는 정량적으로 양이 많고, 도메인에 알맞은 동일한 test data를 사용해야 신뢰도가 높다.





## 카운트 기반의 단어 표현(Count Based word Representation)

- 단어의 표현 방법
  - 국소 표현(Local Representation, 이산 표현(Discrete Representation))
    - 해당 단어 그 자체만 보고 특정 값을 mapping하여 단어를 표현하는 방법.
    - 예를 들어 강아지, 귀여운 이라는 단어 각각에 1번, 2번 과 같은 숫자를 mapping하는 방식이다.
  - 분산 표현(Distributed Representation, 연속 표현(Continuous Representation))
    - 단어를 표현하고자 주변을 참고하여 단어를 표현하는 방법.
    - 예를 들어 강아지라는 단어 주변에 주로 귀여운이라는 단어가 자주 등장하므로 강아지라는 단어는 귀여운 느낌이다로 단어를 정의한다.
    - 국소 표현과 달리 분산 표현은 단어의 뉘앙스를 표현할 수 있게 된다.
  - 앞에서 살펴본 One-hot vector, N-gram과 뒤에서 살펴볼 BoW와 그 확장인 DTM은 국소 표현에 속한다.



- Bag of Words(BoW)

  - 단어들의 순서는 전혀 고려하지 않고 단어들의 출현 빈도만 고려하는 텍스트 데이터의 수치화 방법이다.
    - 가방에 물건들이 순서 없이 들어가 있는 모습을 생각하면 된다.
    - 각 단어가 등장한 횟수를 수치화하는 표현 방법이므로 어떤 단어가 얼마나 등장했는지를 통해 문서가 어떤 종류의 문서인지를 판단하는 작업에 주로 쓰인다.
  - BoW 만들기

  ```python
  from konlpy.tag import Okt
  
  okt = Okt()
  
  def build_bag_of_words(sentence):
      # 온점 제거
      sentence = sentence.replace('.', '')
      # 형태소 분석
      tokens = okt.morphs(sentence)		# ['우리', '집', '강아지', '가', '옆', '집', '강아지', '보다', '순하다']
      print(tokens)
  
      word_to_index = {}
      bow = []
  
      for word in tokens:  
          if word not in word_to_index.keys():
              index = len(word_to_index)
              word_to_index[word] = index
              # BoW에 전부 기본값 1을 넣는다.
              bow.insert(index - 1, 1)
          else:
              # 만약 이미 bow에 포함된 단어일 경우
              index = word_to_index.get(word)
              # 단어에 해당하는 인덱스의 위치에 1을 더한다.
              bow[index] = bow[index] + 1
  
      return word_to_index, bow
  
  
  vocabulary, bow = build_bag_of_words("우리 집 강아지가 옆 집 강아지 보다 순하다.")
  print(vocabulary)		# {'우리': 0, '집': 1, '강아지': 2, '가': 3, '옆': 4, '보다': 5, '순하다': 6}
  print(bow)				# [1, 2, 2, 1, 1, 1, 1]
  ```

  - `sklearn`의 `CountVectorizer`을 사용하면 보다 간단하게 BoW를 만들 수 있다.
    - 단, 띄어쓰기로만 tokenizing을 하는 수준이므로 한글 문장을 가지고는 사용할 수 없다.

  ```python
  from sklearn.feature_extraction.text import CountVectorizer
  
  def build_bag_of_words_by_sklearn(sentence):
      vector = CountVectorizer()
      # list 형태로 넘겨야한다.
      bow = vector.fit_transform([sentence]).toarray()
      print(bow)						# [[2 1 2 1 1 1]]
      print(vector.vocabulary_)		# {'my': 2, 'dog': 0, 'is': 1, 'nicer': 4, 'than': 5, 'neighbor': 3}
  
  build_bag_of_words_by_sklearn("My dog is nicer than my neighbor's dog.")
  ```

  - 불용어를 제거하고 BoW 만들기
    - `CountVectorizer`에 임의의 불용어를 설정하거나, 자체적으로 내장된 불용어를 사용할 수 있다.
    - `nltk`에서 제공하는 불용어를 사용하는 방법도 있다.

  ```python
  from sklearn.feature_extraction.text import CountVectorizer
  from nltk.corpus import stopwords
  
  def build_bag_of_word_with_stopword(sentence, stopwords):
      vector = CountVectorizer(stop_words=stopwords)
      bow = vector.fit_transform([sentence]).toarray()
      print(bow)
      print(vector.vocabulary_)
      
  
  # 사용자 지정 불용어 사용
  build_bag_of_word_with_stopword("My dog is nicer than my neighbor's dog.", ["neighbor"])
  
  # CountVectorizer가 제공하는 stopword 사용
  build_bag_of_word_with_stopword("My dog is nicer than my neighbor's dog.", "english")
  
  # nltk에서 지원하는 stopword 사용
  build_bag_of_word_with_stopword("My dog is nicer than my neighbor's dog.", stopwords.words("english"))
  ```



- 문서 단어 행렬(Document-Term Matrix, DTM)

  - 다수의 문서에 등장하는 각 단어들의 빈도를 행렬로 표현한 것이다.
    - 문서 각각의 BoW를 하나의 table 형태로 만든 것이라고 생각하면 된다.
    - 행과 열을 반대로 선택할 경우 TDM이라 부르기도 한다.
  - DTM의 표기법
    - 아래와 같은 문서들은 아래 표와 같은 DTM으로 표기할 수 있다.
    - 문서1: 귀여운 비숑.
    - 문서2: 귀여운 포메.
    - 문서3: 귀여운 비숑 귀여운 포메

  |       | 귀여운 | 비숑 | 포메 |
  | ----- | ------ | ---- | ---- |
  | 문서1 | 1      | 1    | 0    |
  | 문서2 | 1      | 0    | 1    |
  | 문서3 | 2      | 1    | 1    |

  - 희소 표현(Sparse representation)
    - 수 많은 문서들 중 단 한 문서에만 등장하는 단어가 있다고 할 때, 그 단어를 위해서 열을 하나 추가해야하고, 다른 모든 문서에 0을 채워 넣어야 한다.
    - 원-핫 벡터나 DTM 등에서 대부분의 값이 0인 표현을 희소 벡터 또는 희소 행렬이라 부른다.
    - 희소 벡터는 저장 공간 증가와 계산의 복잡도를 증가시킨다.





### TF-IDF

- TF-IDF(Term Frequency-Inverse Document Frequency)

  - 모든 문서에 자주 등장하는 단어는 중요도가 낮은 것으로, 특정 문서에만 자주 등장하는 단어는 중요도가 높은 것으로 판단하는 중요도 계산 방식이다.
    - 문서 사이의 유사도 계산하거나 검색 시스템에서 검색 결과의 점수를 계산 하거나 문서 내에서 특정 단어의 중요도를 계산 할 때 사용한다.
  - tf(d, t)
    - d는 문서, t는 단어를 의미하며 tf(d, t)는 특정 문서 d에서 특정 단어 t가 등장하는 횟수를 의미한다.
    - DTM의 각 cell의 숫자 값들이 이에 해당한다.
    - 예를 들어 tf(문서3, 귀여운)의 값은 2가 된다.
  - df(t)
    - df(t)는 전체 문서 중에서 특정 단어 t가 등장한 문서의 개수이다.
    - t가 문서에 등장했는지 여부만 따지며, 문서에 몇 번 등장했는지는 고려하지 않는다.
    - 예를 들어 위 예시에서 "귀여운"이라는 t는 3개의 문서에 4번 등장하는데, 이 경우 df(귀여운)의 값은 3이다.
  - idf(t)
    - df(t)에 반비례하는 수이다.
    - 아래 식에서 n은 전체 문서의 개수를 의미한다.
    - log를 취하지 않으면 총 문서의 개수 n이 커질수록 값이 기하급수적으로 커지기 때문에 log를 취한다.
    - log의 밑은 사용자가 임의로 정할 수 있으나 대부분의 경우 자연 로그를 사용한다.
    - 분모에 1을 더해주는 이유는 특정 단어가 어떤 문서에도 등장하지 않을 경우 분모가 0이 될 수 있기에 이를 방지하기 위함이다.

  $$
  idf(t)=log({n \over 1+df(t)})
  $$

  

  - 주의사항
    - TF-IDF 구현을 제공하는 여러 패키지들이 있으며 이들의 구현 방식이 약간씩 다르다.
    - 위 식은 TF-IDF의 가장 기본적인 식이지만 위 기본 식을 바탕으로 구현할 경우 몇 가지 문제가 발생할 수 있다.
    - 예를 들어 n이 4인데 df(t)의 값이 3일 경우 로그의 진수값이 1이 되어 idf(d, t)의 값이 0이 된다.
    - 따라서 더 이상 가중치의 역할을 수행할 수 없게 된다.



- Python으로 TF-IDF 직접 계산하기

  - 먼저 `DataFrame`을 사용하여 DTM을 저장한다.
    - tf(t, d)를 사용하여 DTM에 값을 채워 넣는다.

  ```python
  import pandas as pd
  from math import log
  
  
  def tf(t, d):
    return d.count(t)
  
  def idf(t):
      df = 0
      for doc in docs:
          df += t in doc
      return log(N/(df+1))
  
  def tfidf(t, d):
    return tf(t,d)* idf(t)
  
  def build_dtm(vocabulary):
      result = []
      for i in range(N):
          result.append([])
          d = docs[i]
          for j in range(len(vocabulary)):
              t = vocabulary[j]
              # tf 함수를 사용하여 DTM에 값을 채워 넣는다.
              result[-1].append(tf(t, d))
      return pd.DataFrame(result, columns = vocabulary)
  
  
  docs = [
      "귀여운 비숑",
      "귀여운 포메",
      "귀여운 비숑 귀여운 포메",
      "깜찍한 아기 사슴"
  ]
  
  N = len(docs)
  vocabulary = list(set(word for doc in docs for word in doc.split()))
  print(vocabulary)		# ['깜찍한', '귀여운', '아기', '사슴', '포메', '비숑']
  
  dtm = build_dtm(vocabulary)
  print(dtm)
  """
     깜찍한  귀여운  아기  사슴  포메  비숑
  0    0    1      0    0    0    1
  1    0    1      0    0    1    0
  2    0    2      0    0    1    1
  3    1    0      1    1    0    0
  """
  ```

  - 각 단어에 대한 IDF 값을 구한다.

  ```python
  idf_result = [idf(t) for t in vocabulary]
  idf_ = pd.DataFrame(idf_result, index=vocabulary, columns=["IDF"])
  print(idf_)
  """
            IDF
  깜찍한  0.693147
  귀여운  0.000000
  아기   0.693147
  사슴   0.693147
  포메   0.287682
  비숑   0.287682
  """
  ```

  - TF-IDF 행렬을 출력한다.

  ```python
  result = []
  for i in range(N):
      result.append([])
      d = docs[i]
      for j in range(len(vocabulary)):
          t = vocabulary[j]
          result[-1].append(tfidf(t,d))
  
  tfidf_ = pd.DataFrame(result, columns = vocabulary)
  print(tfidf_)
  """
          깜찍한        비숑        아기  귀여운        사슴        포메
  0  0.000000  0.287682  0.000000  0.0  0.000000  0.000000
  1  0.000000  0.000000  0.000000  0.0  0.000000  0.287682
  2  0.000000  0.287682  0.000000  0.0  0.000000  0.287682
  3  0.693147  0.000000  0.693147  0.0  0.693147  0.000000
  """
  ```

  - 전체 code

  ```python
  import pandas as pd
  from math import log
  
  
  def tf(t, d):
    return d.count(t)
  
  def idf(t):
      df = 0
      for doc in docs:
          df += t in doc
      return log(N/(df+1))
  
  def tfidf(t, d):
    return tf(t,d)* idf(t)
  
  def build_dtm(vocabulary):
      result = []
      for i in range(N):
          result.append([])
          d = docs[i]
          for j in range(len(vocabulary)):
              t = vocabulary[j]
              # tf 함수를 사용하여 DTM에 값을 채워 넣는다.
              result[-1].append(tf(t, d))
      return pd.DataFrame(result, columns = vocabulary)
  
  
  docs = [
      "귀여운 비숑",
      "귀여운 포메",
      "귀여운 비숑 귀여운 포메",
      "깜찍한 아기 사슴"
  ]
  N = len(docs)
  vocabulary = list(set(word for doc in docs for word in doc.split()))
  print(vocabulary)
  
  dtm = build_dtm(vocabulary)
  print(dtm)
  
  idf_result = [idf(t) for t in vocabulary]
  idf_ = pd.DataFrame(idf_result, index=vocabulary, columns=["IDF"])
  print(idf_)
  
  result = []
  for i in range(N):
      result.append([])
      d = docs[i]
      for j in range(len(vocabulary)):
          t = vocabulary[j]
          result[-1].append(tfidf(t,d))
  
  tfidf_ = pd.DataFrame(result, columns = vocabulary)
  print(tfidf_)
  ```



- Scikit-Learn으로 DTM과 TF-IDF 구하기

  - DTM 생성하기

  ```python
  from sklearn.feature_extraction.text import CountVectorizer
  
  corpus = [
      "귀여운 비숑",
      "귀여운 포메",
      "귀여운 비숑 귀여운 포메",
      "깜찍한 아기 사슴"
  ]
  
  vector = CountVectorizer()
  
  # corpus부터 각 단어의 빈도수를 기록한다.
  print(vector.fit_transform(corpus).toarray())
  
  # 각 단어와 맵핑된 인덱스를 출력한다.
  print(vector.vocabulary_)
  
  """
  [[1 0 1 0 0 0]
   [1 0 0 0 0 1]
   [2 0 1 0 0 1]
   [0 1 0 1 1 0]]
  {'귀여운': 0, '비숑': 2, '포메': 5, '깜찍한': 1, '아기': 4, '사슴': 3}
  """
  ```

  - TF-IDF 계산하기
    - 위에서 계산한 DTM을 사용하지는 않는다.

  ```python
  from sklearn.feature_extraction.text import TfidfVectorizer
  
  
  corpus = [
      "귀여운 비숑",
      "귀여운 포메",
      "귀여운 비숑 귀여운 포메",
      "깜찍한 아기 사슴"
  ]
  
  tfidfv = TfidfVectorizer().fit(corpus)
  print(tfidfv.transform(corpus).toarray())
  print(tfidfv.vocabulary_)
  
  """
  [[0.62922751 0.         0.77722116 0.         0.         0.        ]
   [0.62922751 0.         0.         0.         0.         0.77722116]
   [0.75316704 0.         0.46515557 0.         0.         0.46515557]
   [0.         0.57735027 0.         0.57735027 0.57735027 0.        ]]
  {'귀여운': 0, '비숑': 2, '포메': 5, '깜찍한': 1, '아기': 4, '사슴': 3}
  """
  ```

