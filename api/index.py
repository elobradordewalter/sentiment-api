from http.server import BaseHTTPRequestHandler
import anthropic
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        texto = body.get('texto', '')

        client = anthropic.Anthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
        )
        msg = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=10,
            messages=[{
                'role': 'user',
                'content': f'Respondé SOLO con una palabra: POSITIVO, NEGATIVO o NEUTRO. Texto: {texto}'
            }]
        )
        resultado = msg.content[0].text.strip().upper()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'sentimiento': resultado}).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'estado': 'funcionando'}).encode())
