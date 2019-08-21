import BaseHTTPServer, SimpleHTTPServer
import ssl


httpd = BaseHTTPServer.HTTPServer(('localhost', 4443),
        SimpleHTTPServer.SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile="/Users/jm/Documents/Scripts/Zang/certs/localhostKey.pem",
        certfile="/Users/jm/Documents/Scripts/Zang/certs/localhostCert.pem", server_side=True)

httpd.serve_forever()
