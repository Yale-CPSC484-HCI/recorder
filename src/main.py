"""Script for single-gpu/multi-gpu demo."""
import sys, os

import argparse
import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.gen

import time
import pathlib
import pickle
import glob

parser = argparse.ArgumentParser(description='AlphaPose Demo')
parser.add_argument('--websocket-server', type=str, help='ip address of websocker server')
parser.add_argument('--local-port', type=int, default=4444, help="this server's local port")
parser.add_argument('--mode', required=True, choices=['record', 'play'], help='record or play')
parser.add_argument('--data-path', default='data', help='record to or playback from this directory')
parser.add_argument('--fps', type=int, default=5, help='framerate')

root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

def ms():
    return int(round(time.time() * 1000))

class Application(tornado.web.Application):
    def __init__(self, args):
        self.args = args
        self.last_frame = None
        self.last_sp2tx = None

        handlers = [
            (r"/", DemoHandler),
            (r"/frames", FrameHandler),
            (r"/twod", TwoDHandler),
            (r"/sp2tx", Sp2txHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": "templates", "default_filename": "index.html"})
        ]
        settings = dict(
            cookie_secret="0*D&G^SYKJ@rfakljsdhfs89dFdiauhg9S&G928u3htrbkajbvsdkjsdlp",
            template_path=os.path.join(root_path, "templates"),
            static_path=os.path.join(root_path, "static"),
            xsrf_cookies=True,
        )

        if args.mode == 'play':
            self.i = 0
            self.pkls = []
            for pkl in sorted(list(glob.iglob(os.path.join(self.args.data_path, f"*.pkl")))):
                self.pkls.append(pkl)
            if not self.pkls:
                raise RuntimeError(f"No pkl files found in {self.args.data_path}")

        super().__init__(handlers, **settings)

    @tornado.gen.coroutine
    def subscribe_frames(self):
        ''' Subscribe to /frames via a websocket client connection '''
        websocket_server = f"ws://{self.args.websocket_server}/frames"
        print(f"connecting to: {websocket_server}")
        conn = yield tornado.websocket.websocket_connect(websocket_server)
        while True:
            msg = yield conn.read_message()
            if msg is None: break
            self.last_frame = msg

    @tornado.gen.coroutine
    def subscribe_sp2tx(self):
        ''' Subscribe to /sp2tx via a websocket client connection '''
        websocket_server = f"ws://{self.args.websocket_server}/sp2tx"
        print(f"connecting to: {websocket_server}")
        conn = yield tornado.websocket.websocket_connect(websocket_server)
        while True:
            msg = yield conn.read_message()
            if msg is None: break
            self.last_sp2tx = msg

    @tornado.gen.coroutine
    def subscribe_twod(self):
        ''' Subscribe to /twod via a websocket client connection '''
        websocket_server = f"ws://{self.args.websocket_server}/twod"
        print(f"connecting to: {websocket_server}")
        conn = yield tornado.websocket.websocket_connect(websocket_server)
        while True:
            msg = yield conn.read_message()
            if msg is None: break
            if self.last_frame is None: break
            if self.last_sp2tx is None: break
            FrameHandler.send_updates(self.last_frame)
            TwoDHandler.send_2d(msg)
            Sp2txHandler.send_sp2tx(self.last_sp2tx)
            with open(os.path.join(self.args.data_path, f"{ms()}.pkl"), 'wb') as f:
                # this read should be threadsafe as we have should be threadsafe until the yield
                pickle.dump({'frame': self.last_frame, 'sp2tx': self.last_sp2tx, 'twod': msg}, f, protocol=pickle.HIGHEST_PROTOCOL)

    def playback(self):
        with open(self.pkls[self.i], 'rb') as f:
            res = pickle.load(f)
            TwoDHandler.send_2d(res['twod'])
            FrameHandler.send_updates(res['frame'])
            if 'sp2tx' in res.keys():
                Sp2txHandler.send_sp2tx(res['sp2tx'])
        self.i += 1
        if self.i >= len(self.pkls):
            self.i = 0


class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class TwoDHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def check_origin(self, origin):
        '''Allow from all origins'''
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        TwoDHandler.waiters.add(self)
        logging.info("connect: there are now %d connections", len(self.waiters))

    def on_close(self):
        TwoDHandler.waiters.remove(self)
        logging.info("disconnect: there are now %d connections", len(self.waiters))

    @classmethod
    def send_2d(cls, image):
        for waiter in cls.waiters:
            try:
                waiter.write_message(image)
            except:
                logging.error("Error sending message", exc_info=True)


class FrameHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def check_origin(self, origin):
        '''Allow from all origins'''
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        FrameHandler.waiters.add(self)
        logging.info("connect: there are now %d connections", len(self.waiters))

    def on_close(self):
        FrameHandler.waiters.remove(self)
        logging.info("disconnect: there are now %d connections", len(self.waiters))

    @classmethod
    def send_updates(cls, frame):
        for waiter in cls.waiters:
            try:
                waiter.write_message(frame)
            except:
                logging.error("Error sending message", exc_info=True)


class Sp2txHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def check_origin(self, origin):
        '''Allow from all origins'''
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        Sp2txHandler.waiters.add(self)
        logging.info("connect: there are now %d connections", len(self.waiters))

    def on_close(self):
        Sp2txHandler.waiters.remove(self)
        logging.info("disconnect: there are now %d connections", len(self.waiters))

    @classmethod
    def send_sp2tx(cls, sp2tx):
        for waiter in cls.waiters:
            try:
                waiter.write_message(sp2tx)
            except:
                logging.error("Error sending message", exc_info=True)

def main():
    args = parser.parse_args()

    app = Application(args)
    app.listen(args.local_port, '0.0.0.0')
    print(f"open http://127.0.0.1:{args.local_port} in your browser to preview the data")
    if args.mode == 'record':
        if not args.websocket_server:
            raise RuntimeError("Please specify the server to connect to with --websocket-server")
        pathlib.Path(args.data_path).mkdir(parents=True, exist_ok=True)
        tornado.ioloop.IOLoop.current().spawn_callback(app.subscribe_frames)
        tornado.ioloop.IOLoop.current().spawn_callback(app.subscribe_twod)
        tornado.ioloop.IOLoop.current().spawn_callback(app.subscribe_sp2tx)
    else:
        if args.websocket_server:
            raise RuntimeError("Please remove the --websocker-server flag when playing back locally recorded data")
        tornado.ioloop.PeriodicCallback(app.playback, (1/args.fps) * 1000).start()

    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        if args.mode == 'record':
            print(f"recording is in {args.data_path}, switch to '--mode play' to play the recording")
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    main()

