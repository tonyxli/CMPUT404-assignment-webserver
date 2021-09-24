#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    # Receive requests and extract data, then sends the data to decode_data(), open and send back the files requested
    def handle(self):  
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        file_name = self.decode_data(self.data)
        if file_name != None:
            if file_name.endswith("html"):
                content = "text/html"
            elif file_name.endswith("css"):
                content = "text/css"
            else: 
                content = "application/octet-stream"
            try:
                f = open("www" + file_name, "r")
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n", "utf-8"))
                self.request.sendall(bytearray("Content-Type: " + content + "\r\n\n", "utf-8"))
                self.request.sendall(bytearray(f.read(), "utf-8"))
                f.close()
            except:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\nError 404 Could not find the page you were looking for", "utf-8"))


    # decode the requests and return the directories and file names
    def decode_data(self, data):
        data = data.decode()  #decoding data
        if data == "":
            return None
        data_list = data.split(" ")
        #checking if method is allowed 
        method = data_list[0]
        if method != "GET":
            return self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", "utf-8"))

        file_name = data_list[1]
        if file_name == "/" or file_name.endswith("deep/"):
            return file_name + "index.html"
        elif file_name != "/" and (not file_name.endswith("/")):
            return self.request.sendall(bytearray("HTTP/1.1 301 Moved Permenantly\r\nLocation: http://127.0.0.1:8080" + file_name + "/\r\n", "utf-8"))
        elif file_name.endswith("deep.css/"):
            file_name.replace("index.html", "")
        else:
            return file_name[:-1]
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
