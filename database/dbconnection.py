

from mongokit import Connection

class MongoConnection(Connection):
    connection = {}
    def __new__(self, *arg):
        if not self.connection:
            host_port = list(arg)
            self.connection = Connection(host_port[0], int(host_port[1]))
        return self.connection
        

def get_connection(host, port):
    '''
    returns a mongokit connection instance
    '''
    return MongoConnection("mongodb://mongo:27017", 27017)