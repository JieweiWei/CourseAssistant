import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
import thread
from utils import monitor

from tornado.options import define, options
import sys

define('port', default = 8888, help = 'run on the given port', type = int)

class Application(tornado.web.Application):
    def __init__(self, isDebug):
        handlers = [
            (r'/', MainHandler),
            (r'/screenshot', ScreenshotHandler),
            (r'/chatRoom', ChatRoomHandler),
        ]
        settings = dict(
            cookie_secret = '__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__',
            template_path = os.path.join(os.path.dirname(__file__), 'templates'),
            static_path = os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies = True,
            debug = isDebug,
        )

        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', messages = ScreenshotHandler.cache)

class ScreenshotHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    # for tornado 4.x
    def check_origin(self, origin):
        return True

    # for iOS 5.0 Safari
    def allow_draft76(self):
        return True

    def open(self):
        print 'new client opened'
        ScreenshotHandler.waiters.add(self)

    def on_close(self):
        print 'old client closed'
        ScreenshotHandler.waiters.remove(self)

    @classmethod
    def update_cache(self, filename):
        print 'update cache'
        self.cache.append(filename)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]

    @classmethod
    def send_updates(self, filename):
        print 'send updates'
        logging.info('sending message to %d waiters', len(self.waiters))
        for waiter in self.waiters:
            try:
                waiter.write_message(filename)
            except:
                logging.error('Error sending message', exc_info=True)

    def on_message(self, message):
        logging.info('got message %r', message)
        ScreenshotHandler.send_updates(message)

class ChatRoomHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    # for tornado 4.x
    def check_origin(self, origin):
        return True
 
    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True
 
    def open(self):
        print "new client opened"
        ChatRoomHandler.waiters.add(self)
 
    def on_close(self):
        ChatRoomHandler.waiters.remove(self)
 
    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]
 
    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)
 
    def on_message(self, message):
        logging.info("got message %r", message)
 
        ChatRoomHandler.send_updates(message)

if __name__ == '__main__':
    _debug = False
    if len(sys.argv) == 2 and sys.argv[1] == 'debug':
        _debug = True
    if not _debug:
        # try to start the monitor
        try:
            thread.start_new_thread(monitor.main, ('.\\static\\screenshot\\', ScreenshotHandler))
        except:
            print 'Error: fail to start a thread'
    tornado.options.parse_command_line()
    app = Application(_debug)
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()