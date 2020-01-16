#!/usr/bin/env python3
"""
Thanks to mdonkers for the inspiration at https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7

"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, ssl, time, argparse


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self._set_cors_response()
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _set_cors_response(self):
        if 'Origin' in self.headers.keys():
            self.send_header('Access-Control-Allow-Origin', self.headers.get('Origin'))
            self.send_header('Access-Control-Allow-Credentials', 'true')
            self.send_header('Vary', 'Origin')
        if 'Access-Control-Request-Headers' in self.headers.keys():
            self.send_header('Access-Control-Allow-Headers', self.headers.get('Access-Control-Request-Headers'))
        if 'Access-Control-Request-Method' in self.headers.keys():
            self.send_header('Access-Control-Allow-Methods', self.headers.get('Access-Control-Request-Method'))

    def do_OPTIONS(self):
        logging.info("OPTIONS request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self.send_response(200)
        self.send_header('Allow', 'GET, HEAD, POST, OPTIONS, DELETE, PUT, PUSH')
        self.send_header('Content-type', 'text/html')
        self._set_cors_response()
        self.end_headers()
        #self.wfile.write("OPTIONS request for {}".format(self.path).encode('utf-8'))

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        if 'redirect.htm' in self.path:
            # TO-DO: dynamically pull the redirect parameter, currently must be 'redirect_url'
            self._set_response()
            self.wfile.write(bytes('<!DOCTYPE html>\n<html lang="en">\n<head>\n</head>\n<body>\n  <script>\n    '
                                   'var u = new URLSearchParams(window.location.search);\n    '
                                   'var redirect = u.get("redirect_url");\n    if (redirect) {\n      '
                                   'window.location.href = redirect;\n    }\n  </script>\n</body>\n</html>','UTF-8'))
            logging.info("\n--->  Responded with redirect page...\n")
        else:
            self._set_response()
            self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(port, domain, cert, key, outfile, is_ssl=False, server_class=HTTPServer, handler_class=S):
    logging.basicConfig(filename=outfile, filemode='a', level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    if is_ssl:
        try:
            httpd.socket = ssl.wrap_socket (httpd.socket, keyfile=key, certfile=cert, server_side=True)
            print('Serving https://' + domain + ':' + str(port) + '...')
        except:
            print('\nCertificate files not found at ' + cert +'...\n')
            exit(2)
    else:
        print('Serving http://' + domain + ':' + str(port) + '...')
    logging.info('Starting httpd...\n')
    logging.info('Serving on port ' + str(port) + '...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nCaught Interrupt... Stopping Server...')
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', action='store', default='localhost')
    parser.add_argument('-p', '--port', action='store', default=8080)
    parser.add_argument('--ssl', action='store_true', default=False)
    #parser.add_argument('-s', '--serve',
    #                    help='Any request for the supplied filename, in any path, will return the file')
    parser.add_argument('-o', '--outfile', action='store', default=str('requests_' + str(int(time.time())) + '.log'))

    args = parser.parse_args()

    parser.add_argument('--cert', action='store', default='/etc/letsencrypt/live/' + args.domain + '/fullchain.pem')
    parser.add_argument('--key', action='store', default='/etc/letsencrypt/live/' + args.domain + '/privkey.pem')

    args = parser.parse_args()

    run(port=int(args.port), domain=args.domain, is_ssl=args.ssl, outfile=args.outfile, key=args.key, cert=args.cert)

