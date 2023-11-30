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

  
