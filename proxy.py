import requests
import wsgiref.util
import pprint
#wsgiref.util.request_uri(environ, include_query=1)

class ChangePath:
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        def start_change_path(status, response_headers):

            return start_response(status, response_headers)

        if environ['PATH_INFO'] == '/path':
           environ['PATH_INFO'] = '/new_path'

        return self.application(environ, start_change_path)

class ProxyIter:
    def __init__(self, result, proxied_response):
        self.proxied_response = proxied_response
        if hasattr(result, 'close'):
            self.close = result.close
        self._next = iter(result).next

    def __iter__(self):
        return self

    def next(self):
        if self.proxied_response['response'] is not None:
            return self.proxied_response['response']
        return self._next()

class Proxy:
    def __init__(self, application):
        self.proxy_host = "http://localhost:4567"
        self.application = application

    def __call__(self, environ, start_response):
        proxied_object = {'response': None}
        def start_proxy(status, response_headers):
            pprint.pprint(environ)
            if environ['CONTENT_LENGTH'] != '':
                print 'outputing input'
                print environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
            print 'getting:'  + self.proxy_host + environ['PATH_INFO'] + "?" + environ['QUERY_STRING']

            proxied_object = {'response': None}
            try:
                response = requests.get(self.proxy_host + environ['PATH_INFO'] + "?" + environ['QUERY_STRING'])
                if response.status_code < 400:
                    proxied_object['response'] = response.text
                    start_response(str(response.status_code), response_headers)
                    return lambda: response.text
            except Exception as ex:
                print ex

            return start_response(status, response_headers)

        return ProxyIter(self.application(environ, start_proxy), proxied_object)


