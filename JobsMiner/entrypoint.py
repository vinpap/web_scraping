"""For deployment only"""


from server import Server

server = Server()
app = server.getApp()
