from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Handles all GET requests our web server recives.
        """
        try:
            """
            Figuring out which resource you are trying to access
            we use simple pattern matching plan that only looks
            for the ending of URL path
            """
            if self.path.endswith("/hello"):    # $path contain the URS sent by the client to the server as a string
                self.send_response(200)         # indicating successful get request
                self.send_header('Content-type', 'text/html')   # indicate that server is replying with text in the form of HTML to client  
                self.end_headers()                              # alnog with end_header command which sends a blank line indicating the end of HTTP headers in the response

                output = ""                     # content that will be sent back to client
                output += "<html><body>"
                output += "Hello!"
                output += """<form method='POST' enctype='multipart/form-data' action='/>
                       hello'><h2>What would you like me to say?</h2><input name='message'
                       type='text'><input type='submit' value='Submit'> </form>"""
                output += "</body></html>"
                self.wfile.write(output)    # send message back to client
                print output
                return                      # exit if statement

            if self.path.endswith("/hola"):    
                self.send_response(200)        
                self.send_header('Content-type', 'text/html')  
                self.end_headers()                              

                output = ""                    
                output += "<html><body>&#161Hola! <a href='/hello'>Back to Hello</a>"
                output += """<form method='POST' enctype='multipart/form-data' action='/>
                       hello'><h2>What would you like me to say?</h2><input name='message'
                       type='text'><input type='submit' value='Submit'> </form>"""
                output += "</body></html>"
                self.wfile.write(output)   
                print output
                return                      


        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):      # overwrite method in BaseHTTPRequestHandler
        try:
            self.send_response(301)     # indicates a successful POST
            self.end_headers()
                                                                                        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))     # parse HTML form header into a main value and dictonary of parameters
            if ctype == 'multipart/form-data':                                          # check and see if this is form data being recived
                fields = cgi.parse_multipart(self.rfile, pdict)                         # collect all of the filds in a form       
                messagecontent = fields.get('message')                                   # get value of a specific field or set of fields and store them in an array

            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]

            output += """<form method='POST' enctype='multipart/form-data' action='/>
                       hello'><h2>What would you like me to say?</h2><input name='message'
                       type='text'><input type='submit' value='Submit'> </form>"""
            output += "</body></html>"

            self.wfile.write(output)
            print output
        
        except:  
            pass         

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)   # create instance of HTTP server class
        print "Web server running on port %s" % port
        server.serve_forever()                              # keep server constantly listening until you call 'CTRL + C'

    except KeyboardInterrupt:
        # trigered when user use 'CTRL + C' 
        # and exit try block
        print "^C entered, stopping web setver..."
        server.socket.close()                               # shut down server

########## End of file ##########

if __name__ == '__main__':
    """
    Immediately run the main method when the Python
    interpreter executes my script
    """
    main()