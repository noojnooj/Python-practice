# Python-practice

### 순수 Python으로 웹서버 생성하기

프레임워크 없이도 HTTP 서버가 동작하는 원리를 알고 넘어가려고함.

```python
from http.server import BaseHTTPRequestHandler, HTTPServer  # Python 내장 HTTP 서버 모듈에서 요청 처리 클래스와 서버 클래스 가져옴

class Handler(BaseHTTPRequestHandler):  # 요청을 처리할 사용자 정의 핸들러 클래스 정의 (BaseHTTPRequestHandler 상속)
    def do_GET(self):  # 클라이언트가 GET 요청을 보냈을 때 호출되는 메서드
        self.send_response(200)  # HTTP 응답 코드 200(성공)을 클라이언트에 보냄
        self.send_header('Content-type', 'text/html')  # 응답 헤더 설정 (HTML 형식으로 응답)
        self.end_headers()  # 헤더 전송 완료 (이후부터는 본문 전송)
        self.wfile.write(b"<h1>안녕하세요. Python으로 서버 생성해보았습니다.</h1>")  # 클라이언트에 HTML 본문 전송 (바이트 형식)

server = HTTPServer(('localhost', 8080), Handler)  # 서버 객체 생성 (localhost의 8080 포트에서 Handler로 요청 처리)
print("서버 도는 중... http://localhost:8080")  # 서버 실행 안내 메시지 출력
server.serve_forever()  # 서버를 무한 루프로 실행하여 계속 요청을 받도록 설정
```

시작 부터 문제 등장

![스크린샷 2025-07-14 19.38.01.png](attachment:e9063426-8f7f-4129-9a23-d889e389568a:스크린샷_2025-07-14_19.38.01.png)

한글로 작성해서 그런가 영어로 바꿔보니 오류는 바로 사라짐.

![스크린샷 2025-07-14 19.39.11.png](attachment:3de474c8-1fae-485e-a6cc-e0d07b17383a:스크린샷_2025-07-14_19.39.11.png)

앞에 붙힌 바이트 문자열 리터럴(`b""`)를 사용했기 때문이였음.

`b”<내용>”`은 Python에서 문자열이 아닌 bytes 객체를 생성함.

이건 텍스트가 아니라 0과 1로 된 데이터 시퀀스.

이걸 왜 사용하냐면 HTTP 응답을 보낼 때는 텍스트가 아니라 바이트 스트림을 전송해야 하기 때문에

wfile.write() 같은 메서드는 bytes 타입을 요구함.

```python
self.wfile.write(b"<h1>Hello</h1>")  # OK
self.wfile.write("<h1>Hello</h1>")   # TypeError 발생 (str 타입이라서)
```

`b""`는 **ASCII 문자만 허용. → 유니코드 문자열을 .encode( )로 바이트로 변환하자.**

```python
# 기존
self.wfile.write("b<h1>안녕하세요. Python으로 서버 생성해보았습니다.</h1>")

# 바꾸기
self.wfile.write("<h1>안녕하세요. Python으로 서버 생성해보았습니다.</h1>".encode("utf-8"))
```

추가로 응답 헤더에서 charset=utf-8을 꼭 추가해주자

```python
self.send_header('Content-type', 'text/html; charset=utf-8')
```

출력 확인 할 수 있다!

![스크린샷 2025-07-14 19.53.06.png](attachment:f24c941b-3824-471a-b852-9d10a90e5780:스크린샷_2025-07-14_19.53.06.png)

---

## Client - Server 구조 분리

예시 폴더구조

```python
Python-practice/
├── client/
│   └── index.html           # 클라이언트: 브라우저에서 띄울 HTML
├── server/
│   └── server.py            # 서버: HTTP 요청 수신 및 정적 파일 서빙
```

**client/index.html**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Python Practice</title>
  </head>
  <body>
    <h1>Python 클라이언트에서 접속했음.</h1>
  </body>
</html>
```

**server/server.py**

```python
from http.server import BaseHTTPRequestHandler, HTTPServer  # Python 내장 HTTP 서버 모듈에서 요청 처리 클래스와 서버 클래스 가져옴
import os # os 모듈 가져오기 (현재 코드에서는 사용되지 않지만, 파일 경로 처리 등에서 유용할 수 있음)

class Handler(BaseHTTPRequestHandler):  # 요청을 처리할 사용자 정의 핸들러 클래스 정의 (BaseHTTPRequestHandler 상속)
    def do_GET(self):  # 클라이언트가 GET 요청을 보냈을 때 호출되는 메서드
     if self.path == '/' or self.path == '/index.html':  # 요청 경로가 루트 또는 index.html인 경우
        file_path = os.path.join(os.path.dirname(__file__), '..client/index.html') # index.html 파일 경로 설정
        try:
            with open(file_path, "r", encoding="utf-8") as file: # index.html 파일을 읽기 모드로 열기
               content = file.read() # 파일 내용을 읽어옴

            self.send_response(200)  # HTTP 응답 상태 코드 200 (성공) 전송
            self.send_header("Content-Type", "text/html; charset=utf-8")  # 응답 헤더에 콘텐츠 타입 설정
            self.end_headers()  # 헤더 전송
            self.wfile.write(content.encode("utf-8"))  # 파일 내용을 UTF-8로 인코딩하여 응답 본문에 작성

        except FileNotFoundError:   # 파일이 존재하지 않을 경우
            self.send_error(404, "File not found") # HTTP 404 오류 응답 전송
            self.end_headers()  # 헤더 전송
            self.wfile.write("404 오류".encode("utf-8"))  # 오류 메시지를 UTF-8로 인코딩하여 응답 본문에 작성
        else:  # 요청 경로가 루트나 index.html이 아닌 경우
           self.send_error(404, "File not found")  # HTTP 404 오류 응답 전송
           self.end_headers()  # 헤더 전송
           self.wfile.write("404 오류".encode("utf-8"))  # 오류 메시지를 UTF-8로 인코딩하여 응답 본문에 작성

server = HTTPServer(('localhost', 8080), Handler)  # HTTP 서버 인스턴스 생성 (localhost:8000에서 요청을 처리하도록 설정)
print("서버 도는 중... http://localhost:8080")
server.serve_forever()
```

**실행하기**

```bash
cd server
python server.py
```

**??**

![스크린샷 2025-07-14 20.18.50.png](attachment:668ac32c-f4af-4767-8320-9db46e1cd73e:스크린샷_2025-07-14_20.18.50.png)

터미널 출력을보니 200코드 다음에 404, 404 두번 더 나오는 것을 볼 수 있음.

![스크린샷 2025-07-14 20.19.59.png](attachment:b45a800f-14e6-43d9-bca2-076efef9374b:스크린샷_2025-07-14_20.19.59.png)

try except else에서 계속 도나보다 생각함. 보니까 들여쓰기 문제라고함..

python에서는 들여쓰기도 잘해야한다니.. if문과 열을 맞춰야함 개 억울탱

**변경 전**

```python
     if self.path == '/' or self.path == '/index.html':
        file_path = os.path.join(os.path.dirname(__file__), '..client/index.html')
        try:
            with open(file_path, "r", encoding="utf-8") as file:
               content = file.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        except FileNotFoundError:
            self.send_error(404, "File not found")
            self.end_headers()
            self.wfile.write("404 오류".encode("utf-8"))
        else:
           self.send_error(404, "File not found")
           self.end_headers()
           self.wfile.write("404 오류".encode("utf-8"))

```

**변경 후 - 이미지**

![스크린샷 2025-07-14 20.26.57.png](attachment:bd21a84c-649a-480a-a892-e6577d998bb7:스크린샷_2025-07-14_20.26.57.png)

**성공**

![스크린샷 2025-07-14 20.30.08.png](attachment:59e54434-f0cf-4e25-b041-bef4ccf561b4:스크린샷_2025-07-14_20.30.08.png)

---

### 스타일(CSS)도 추가해보기

```python
Python-practice/
├── client/
│   ├── index.html
│   └── style.css     ← 이 파일을 새로 만듬
├── server/
│   └── server.py
```

1. **client/style.css**

```css
h1 {
  color: red;
}
```

1. **client/index.html 수정**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Python Practice</title>
    <!-- link로 CSS 파일 연결  -->
    <link rel="stylesheet" href="/style.css" />
  </head>
  <body>
    <h1>Python 클라이언트에서 접속했음.</h1>
  </body>
</html>
```

1. **server.py 수정: CSS 파일 응답 추가**

html파일 응답과 else사이에 추가해주자.

```python
     elif self.path == '/style.css':
        file_path = os.path.join(os.path.dirname(__file__), '../client/style.css') # style.css 파일 경로 설정
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        except FileNotFoundError:
            self.send_error(404, "File not found")
            self.end_headers()
            self.wfile.write("404 오류".encode("utf-8"))
```

1. **서버 실행**

![스크린샷 2025-07-14 20.39.28.png](attachment:f62e3db6-6c8c-4975-8fd1-20d7b50e65a7:스크린샷_2025-07-14_20.39.28.png)
