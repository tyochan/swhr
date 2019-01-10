# Import your application as:
# from wsgi import application
# Example:

from swhr.wsgi import application

# Import CherryPy
import cherrypy
import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# print(BASE_DIR)

if __name__ == '__main__':
    # Mount the application
    cherrypy.tree.graft(application, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    cherrypy.config.update({
        'log.screen': True,
        'log.error_file': 'log/errors.log',
        'log.access_file': 'log/access.log',
        'engine.autoreload.on': False
    })

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = "0.0.0.0"
    server.socket_port = 8080
    server.thread_pool = 30

    # For SSL Support
    # server.ssl_module            = 'pyopenssl'
    # server.ssl_certificate       = 'ssl/certificate.crt'
    # server.ssl_private_key       = 'ssl/private.key'
    # server.ssl_certificate_chain = 'ssl/bundle.crt'

    # Subscribe this server
    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
