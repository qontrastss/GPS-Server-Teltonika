import socket
import re
from threading import Thread
from parse_lib import Parse_Data


class ThreadedServer(Thread):
    def __init__(self, host, port, timeout=10, debug=1):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.debug = debug
        self.data = None
        self.parsed_data = None
        Thread.__init__(self)

    # run by the Thread object
    def run(self):
        if self.debug == 1 or self.debug == 2:
            print('SERVER Starting...', '\n')
        self.listen()

    def listen(self):
        # create an instance of socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to its host and port
        self.sock.bind((self.host, self.port))

        # make socket non blocking
        # self.sock.setblocking(False)

        if self.debug == 1 or self.debug == 2:
            print('SERVER Socket Bound', self.host, self.port, '\n')

        # start listening for a client
        self.sock.listen()
        if self.debug == 1 or self.debug == 2:
            print('SERVER Listening...', '\n')
        while True:
            # get the client object and address
            client, address = self.sock.accept()

            # set a timeout
            client.settimeout(self.timeout)

            if self.debug == 1 or self.debug == 2:
                print('\nCLIENT Connected:', client)

            # start a thread to listen to the client
            Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        size = 2048
        try:
            # try to receive data from the client
            imei = client.recv(size).decode('utf-8')
            if imei:
                if self.debug == 1 or self.debug == 2:
                    print('CLIENT IMEI Received', client)

                if self.debug == 1:
                    print('IMEI:', imei)

                if bool(re.match('(^[0-9]+$)', imei[4:]) and re.match('(^000F)', imei[:4])):
                    response = '01'
                    client.send(response.encode('utf-8'))
                    buffer = b''
                else:
                    response = '00'
                    client.send(response.encode('utf-8'))
                    if self.debug == 1 or self.debug == 2:
                        print("CLIENT IMEI Corrupted")
                        print('CLIENT Disconnected')
                    return
            else:
                if self.debug == 1 or self.debug == 2:
                    print('CLIENT Disconnected')
                return

            while True:
                data = client.recv(size).replace(b'\n', b'')
                if not data:
                    break
                buffer += data

                if self.debug == 1 or self.debug == 2:
                    print('CLIENT Data Received', client)
                if self.debug == 1:
                    print('Received Data:', buffer.decode('utf-8'))
                pars_obj = Parse_Data(buffer.decode('utf-8'))

                try:
                    self.parsed_data, buffer = pars_obj.parse_data()
                except Exception as err:
                    if self.debug == 1:
                        print(err)
                        print("Corrupted Data Inserted!")
                else:
                    pars_obj.save_data()
                    if self.debug == 1:
                        pars_obj.view_data()
        except Exception as err:
            if self.debug == 1 or self.debug == 2:
                print('CLIENT Disconnected:', client)
            client.close()
            return False


if __name__ == "__main__":
    # Debug types: 1 - all detailed info, 2 - prod info, 0 - without debug
    ThreadedServer('127.0.0.1', 8887, timeout=10, debug=1).start()