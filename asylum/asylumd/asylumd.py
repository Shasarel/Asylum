import serial
import socket
import sys
import os
import shutil

from concurrent.futures import ThreadPoolExecutor

from asylum import log
from asylum import config
from asylum.asylumd import jsonrpc


logger = log.setup_logger('asylumd')

SHUTTER_REPEAT_COUNT = [6, 5, 5, 5, 5, 5, 7, 7, 7]
GATE_REPEAT_COUNT = 3


class Arduino:
    def __init__(self):
        try:
            self.serial = serial.Serial("/dev/serial0", 115200, timeout=1)
        except serial.SerialException:
            logger.error("Failed to open serial port")
            sys.exit(1)

    def ping(self):
        logger.debug("called ping")
        data = "0"
        self.serial.write((data + '\n').encode())
        logger.debug(self.serial.readline())
        return "pong"

    # action 0-open 1-close 2-stop
    def shutterAction(self, id, action):
        logger.debug("called shutter %d with action %d", id, action)
        data = "1"
        data += (str(id))
        data += (str(action))
        data += (str(SHUTTER_REPEAT_COUNT[id]))
        self.serial.write((data + '\n').encode())
        logger.debug(self.serial.readline())
        logger.debug(self.serial.readline())

    def gateAction(self, id, repeatCount=GATE_REPEAT_COUNT):
        logger.debug("called gate %d", id)
        data = "2"
        data += (str(id))
        data += (str(repeatCount))
        self.serial.write((data + '\n').encode())
        logger.debug(self.serial.readline())
        logger.debug(self.serial.readline())

    def writeMemory(self, type, id, hex_data):
        data = "3"
        data += (str(type))
        data += (str(id))
        data += hex_data
        self.serial.write((data + '\n').encode())
        logger.debug(self.serial.readline())
        logger.debug(self.serial.readline())

    def readMemory(self, type, id):
        data = "4"
        data += (str(type))
        data += (str(id))
        self.serial.write((data + '\n').encode())
        res = self.serial.readline()
        logger.debug(res)
        return res.decode()[:-2]


class Server:
    def __init__(self, socket_loc):
        if(os.path.exists(socket_loc)):
            os.remove(socket_loc)

        self.executor = ThreadPoolExecutor(max_workers=1)
        self.service = jsonrpc.JsonRpcService()

        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(socket_loc)
        os.chmod(socket_loc, 0o775)

    def addMethod(self, f, is_notification=False):
        def decorated_function(*args, **kwargs):
            future = self.executor.submit(f, *args, **kwargs)
            if not is_notification:
                return future.result()
            return None

        self.service.add_method(decorated_function, f.__name__)

    def serve(self):
        self.server.listen(1)
        while True:
            conn, addr = self.server.accept()
            self.handleConnection(conn)

    def handleConnection(self, conn):
        data = conn.recv(1024)
        resp = self.service.handle(data)
        if resp is not None:
            conn.send(resp.json().encode())
        conn.close()


def main():
    logger.info("Starting asylumd")
    arduino = Arduino()
    server = Server(config['ASYLUMD']['socket_loc'])
    server.addMethod(arduino.ping)
    server.addMethod(arduino.shutterAction, True)
    server.addMethod(arduino.gateAction, True)
    server.addMethod(arduino.writeMemory, True)
    server.addMethod(arduino.readMemory)
    server.serve()


if __name__ == '__main__':
    main()
