from __future__ import absolute_import, division, print_function
import os
import BaseHTTPServer
import time
import logging

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s", datefmt="%Y/%m/%d %H:%M:%S")

LOGGER = logging.getLogger(__name__)


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    responseNum = 0
    
    def do_GET(self):
        LOGGER.info("Client_address = %s", self.client_address)
        LOGGER.info("Path = %s", self.path)
        headers = self.headers.headers
        for i in range(len(headers)):
            h = headers[i]
            LOGGER.info("%d: %s", i, h.rstrip())
 
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html>\n")
        self.wfile.write("    <head>\n")
        self.wfile.write("        <title>Title goes here.</title>\n")
        self.wfile.write("    </head>\n")
        self.wfile.write("    <body>\n")
        self.wfile.write("        <p>This is a test!</p>\n")
        self.wfile.write("        <p>Request count = {}</p>\n".format(MyHandler.responseNum))
        self.wfile.write("        <p>You accessed path: %s</p>\n" % (self.path))
        self.wfile.write("    </body>\n")
        self.wfile.write("</html>\n")
        
        MyHandler.responseNum += 1


if __name__ == '__main__':
    HOST_NAME = os.environ["C9_HOSTNAME"]
    HOST_IP = os.getenv("C9_IP", "0.0.0.0")
    HOST_PORT = int(os.getenv("C9_PORT", 8080))
    
    LOGGER.info("----------------------------")
    LOGGER.info("HOST_IP = %s", HOST_IP)
    LOGGER.info("HOST_PORT = %d", HOST_PORT)
    LOGGER.info("HOST_NAME = %s", HOST_NAME)
    LOGGER.info("----------------------------")

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_IP, HOST_PORT), MyHandler)
    LOGGER.info("Server Starts - %s:%d", HOST_NAME, HOST_PORT)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
 
    httpd.server_close()
    LOGGER.info("Server Stops - %s:%d", HOST_NAME, HOST_PORT)