from http.server import BaseHTTPRequestHandler, HTTPServer  # Python 내장 HTTP 서버 모듈에서 요청 처리 클래스와 서버 클래스 가져옴

class Handler(BaseHTTPRequestHandler):  # 요청을 처리할 사용자 정의 핸들러 클래스 정의 (BaseHTTPRequestHandler 상속)
    def do_GET(self):  # 클라이언트가 GET 요청을 보냈을 때 호출되는 메서드
        self.send_response(200)  # HTTP 응답 코드 200(성공)을 클라이언트에 보냄
        self.send_header('Content-type', 'text/html; charset=utf-8')  # 응답 헤더 설정 (HTML 형식으로 응답)
        self.end_headers()  # 헤더 전송 완료 (이후부터는 본문 전송)
        self.wfile.write("<h1>안녕하세요. Python으로 서버 생성해보았습니다.</h1>".encode("utf-8"))  # 클라이언트에 HTML 본문 전송 (바이트 형식)

server = HTTPServer(('localhost', 8080), Handler)  # 서버 객체 생성 (localhost의 8080 포트에서 Handler로 요청 처리)
print("서버 도는 중... http://localhost:8080")  # 서버 실행 안내 메시지 출력
server.serve_forever()  # 서버를 무한 루프로 실행하여 계속 요청을 받도록 설정