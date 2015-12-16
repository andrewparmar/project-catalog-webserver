from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output += "<html><body>"
                output += "<h1> Add a New Restaurant </h1>"
                output += "<form method='POST' enctype='multipar/form-data action='/restaurants/new'>"
                # output += "<input name='newReaurantAne'"
                output += "<a href='/restaurnat/new'>Add New Restaurant</a></br></br>"
                
                output += "</body></html>" 
                self.wfile.write(output)
                return               

            if self.path.endswith("/restaurants"):

                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Add New Restaurant</a></br></br>"
                
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href=#>Edit</a></br>"
                    output += "<a href=#>Delete</a></br></br>"

                output += "</body></html>" 
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)

    # def do_POST(self):
    #     try:
    #         self.send_response(301)
    #         self.end_headers()
    #         ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
            
    #         if ctype == 'multipart/form-data':
    #             fields = cgi.parse_multipart(self.rfile, pdict)
    #             messagecontent = fields.get('message')




def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webServerHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server ..."
        server.socket.close()

if __name__ == '__main__':
    main()