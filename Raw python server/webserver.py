from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

########## Impert CRUD operations ##########
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

########## Connect to database ##########
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine 
DBSession = sessionmaker(bind = engine)  
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):    
                self.send_response(200)         
                self.send_header('Content-type', 'text/html')     
                self.end_headers()        

                restauranList = session.query(Restaurant).all()
                output = ""                     
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Make a new restorant here</a></br></br>"
                for restauran in restauranList:
                    output += restauran.name
                    output += "</br><a href='/restaurants/%s/edit'>Edit</a>" % restauran.id
                    output += "</br><a href='/restaurants/%s/delete'>Delete</a></br>" % restauran.id
                    output += "</br>"                
                output += "</body></html>"
                self.wfile.write(output)    
                print "Output sent"
                return

            if self.path.endswith("/restaurants/new"):    
                self.send_response(200)         
                self.send_header('Content-type', 'text/html')     
                self.end_headers()        

                restauranList = session.query(Restaurant).all()
                output = ""                     
                output += "<html><body>"
                output += "<h1>Make a new restorant</h1>"
                output += """<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                             <input name='newRestaurantName' type='text' placeholder='New Restaurant name'>
                             <input type='submit' value='Create'> </form>"""          
                output += "</body></html>"
                self.wfile.write(output)    
                print "Output sent"
                return  

            if self.path.endswith("/edit"):    
                restaurantId = int(self.path[self.path.index('/restaurants/')+13 : self.path.index('/edit')])
                restaurantForChange = session.query(Restaurant).filter_by(id = restaurantId).one()

                if restaurantForChange:
                    self.send_response(200)         
                    self.send_header('Content-type', 'text/html')     
                    self.end_headers()

                    output = ""                     
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % restaurantForChange.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantId
                    output += "<input name='changedRestaurantName' type='text' placeholder='%s'>" % restaurantForChange.name
                    output += "<input type='submit' value='Rename'> </form>"          
                    output += "</body></html>"

                    self.wfile.write(output)    
                    print "Output sent"
                    return  

            if self.path.endswith("/delete"):    
                restaurantId = int(self.path[self.path.index('/restaurants/')+13 : self.path.index('/delete')])
                restaurantForDelete = session.query(Restaurant).filter_by(id = restaurantId).one()

                if restaurantForDelete:
                    self.send_response(200)         
                    self.send_header('Content-type', 'text/html')     
                    self.end_headers()

                    output = ""                     
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % restaurantForDelete.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantId                    
                    output += "<input type='submit' value='Delete'> </form>"          
                    output += "</body></html>"

                    self.wfile.write(output)    
                    print "Output sent"
                    return                   

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):      
        try:
            if self.path.endswith("/restaurants/new"):                                  
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))     
                if ctype == 'multipart/form-data':                                          
                    fields = cgi.parse_multipart(self.rfile, pdict)                               
                    newRestaurantName = fields.get('newRestaurantName')                                   
                
                ##### Create new restaurant #####
                newRestaurant = Restaurant(name = newRestaurantName[0])
                session.add(newRestaurant) 
                session.commit()  
                print "New restourant %s added to database" % newRestaurantName[0]

                ##### Redirection to start page #####
                self.send_response(301)     
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')     
                self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))     
                if ctype == 'multipart/form-data':                                          
                    fields = cgi.parse_multipart(self.rfile, pdict)                               
                    changedRestaurantName = fields.get('changedRestaurantName')                                   
                
                restaurantId = int(self.path[self.path.index('/restaurants/')+13 : self.path.index('/edit')])                
                restaurantForEdit = session.query(Restaurant).filter_by(id = restaurantId).one()

                if restaurantForEdit != []:
                    ##### Change restaurant name #####                
                    restaurantForEdit.name = changedRestaurantName[0]
                    session.add(restaurantForEdit) 
                    session.commit()  
                    print "Changed restaurant name"

                    ##### Redirection to start page #####
                    self.send_response(301)     
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')     
                    self.end_headers()

            if self.path.endswith("/delete"):  
                restaurantId = int(self.path[self.path.index('/restaurants/')+13 : self.path.index('/delete')])                
                restaurantForDelete = session.query(Restaurant).filter_by(id = restaurantId).one()

                if restaurantForDelete != []:
                    ##### Delete restaurant from database #####  
                    session.delete(restaurantForDelete) 
                    session.commit()  
                    print "Removed restaurant from db"

                    ##### Redirection to start page #####
                    self.send_response(301)     
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')     
                    self.end_headers()

        except:  
            pass         

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)   
        print "Web server running on port %s" % port
        server.serve_forever()                              

    except KeyboardInterrupt:        
        print "^C entered, stopping web setver..."
        server.socket.close()                               

########## End of file ##########

if __name__ == '__main__':
    """
    Immediately run the main method when the Python
    interpreter executes my script
    """
    main()