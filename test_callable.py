def start_reponse(status, headers):
    pass

class TestStuff:
    def __init__(self, environ, start_reponse):
        print 'in init'
        self.environ = environ
        self.start_reponse = start_reponse

    def __iter__(self):
        print 'itterating'


TestStuff([('test', 'stuff')], start_reponse)
