#!/usr/bin/env python3
import http.server
import socketserver
import ssl
import os
import subprocess
import json
import urllib.request
import urllib.parse

PORT = 5000
API_KEY = 'AIzaSyAKS4a9rCu2hRTebc2lHA9o24BthtqyLjc'

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        # API endpoint kontrolü
        if self.path.startswith('/api/directions'):
            try:
                # Query parametrelerini parse et
                from urllib.parse import urlparse, parse_qs
                parsed = urlparse(self.path)
                params = parse_qs(parsed.query)
                
                origin = params.get('origin', [''])[0]
                destination = params.get('destination', [''])[0]
                
                print(f"📍 API çağrısı: origin={origin}, destination={destination}")
                
                if not origin or not destination:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = json.dumps({'error': 'origin ve destination parametreleri gerekli'})
                    self.wfile.write(error_response.encode('utf-8'))
                    return
                
                # Google Maps Directions API çağrısı
                api_url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}&language=tr&units=metric&mode=driving'
                print(f"🔗 Google Maps API çağrısı: {api_url[:100]}...")
                
                with urllib.request.urlopen(api_url) as response:
                    result = response.read().decode('utf-8')
                    print(f"✅ API başarılı, sonuç uzunluğu: {len(result)} karakter")
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(result.encode('utf-8'))
            except Exception as e:
                print(f"❌ API hatası: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = json.dumps({'error': str(e)})
                self.wfile.write(error_response.encode('utf-8'))
        else:
            # Normal dosya servisi
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/directions':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                origin = data.get('origin', '')
                destination = data.get('destination', '')
                
                # Google Maps Directions API çağrısı
                api_url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}&language=tr&units=metric&mode=driving'
                
                with urllib.request.urlopen(api_url) as response:
                    result = response.read().decode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(result.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = json.dumps({'error': str(e)})
                self.wfile.write(error_response.encode('utf-8'))
        else:
            super().do_POST()

Handler = MyHTTPRequestHandler

# HTTPS için self-signed sertifika oluştur
def create_self_signed_cert():
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("🔐 Self-signed sertifika oluşturuluyor...")
        try:
            # OpenSSL ile self-signed certificate oluştur
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
                '-keyout', key_file, '-out', cert_file,
                '-days', '365', '-nodes',
                '-subj', '/C=TR/ST=Istanbul/L=Istanbul/O=Local/CN=localhost'
            ], check=True, capture_output=True)
            print("✅ Sertifika oluşturuldu!")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ OpenSSL bulunamadı. HTTPS olmadan başlatılıyor...")
            print("⚠️ Google Maps API çalışmayabilir. HTTPS için OpenSSL yükleyin.")
            return None, None
    
    return cert_file, key_file

cert_file, key_file = create_self_signed_cert()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    if cert_file and key_file:
        # HTTPS aktif et
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"🔒 HTTPS sunucu başlatıldı: https://localhost:{PORT}")
        print("⚠️ Tarayıcıda sertifika uyarısı çıkabilir, 'Gelişmiş' > 'Devam et' ile geçin")
    else:
        print(f"⚠️ HTTP sunucu başlatıldı: http://localhost:{PORT}")
        print("⚠️ Google Maps API çalışmayabilir (HTTPS gerekiyor)")
    
    print("Çıkmak için Ctrl+C tuşlarına basın")
    httpd.serve_forever()
