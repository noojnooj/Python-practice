from http.server import BaseHTTPRequestHandler, HTTPServer  # Python 내장 HTTP 서버 모듈에서 요청 처리 클래스와 서버 클래스 가져옴
import os # os 모듈 가져오기 (현재 코드에서는 사용되지 않지만, 파일 경로 처리 등에서 유용할 수 있음)

class Handler(BaseHTTPRequestHandler):  # 요청을 처리할 사용자 정의 핸들러 클래스 정의 (BaseHTTPRequestHandler 상속)
    def do_GET(self):  # 클라이언트가 GET 요청을 보냈을 때 호출되는 메서드
     if self.path == '/' or self.path == '/index.html':  # 요청 경로가 루트 또는 index.html인 경우
        file_path = os.path.join(os.path.dirname(__file__), '../client/index.html') # index.html 파일 경로 설정
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
            self.wfile.write("404 오류".encode("utf-8")) # 오류 메시지를 UTF-8로 인코딩하여 응답 본문에 작성

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
     else: 
        self.send_error(404, "File not found")  
        self.end_headers() 
        self.wfile.write("404 오류".encode("utf-8")) 

server = HTTPServer(('localhost', 8080), Handler)  # HTTP 서버 인스턴스 생성 (localhost:8000에서 요청을 처리하도록 설정)
print("서버 도는 중... http://localhost:8080")
server.serve_forever()