import socket
from controller import controls
from threading import Thread


class Server:
    host = "192.168.16.103"
    port = 9999

    def __init__(self):
        self.connection = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        self.server.setblocking(True)
        self.state_control = None
        self.message_sent = 1

    def decode_the_command(self, byteCommand):
        command = str(byteCommand.decode("utf-8"))
        detached = command.split("|")
        # action | params
        print(len(detached))
        if detached[0] in controls.routines:
            print("chill")
            pass
        else:
            return [1, "error"]

        if len(detached) == 2:
            print("chill 1")
            return [2, detached[0], detached[1]]
        elif len(detached) == 1:
            print("chill 2")
            return [1, detached[0]]
        else:
            print("chill 3")
            return [1, "error"]

    def test(self):
        strin = "asfasf"
        print(strin.split("|"))

    def set_init_state(self):
        try:
            controls.state_status = False
            self.state_control.join()
            controls.request_in_progress = 0
            self.message_sent = 1
            controls.languages = dict()
            controls.quality = dict()
            controls.speed = dict()
            controls.subtitles = dict()
            controls.initialed = False
            controls.age_skipped = False
            controls.driver.quit()

        except Exception as e:
            pass
    def handshake(self,conn):
        while True:
            data = conn.recv(1024).replace(b'\n', b'').decode("utf-8")
            if(data=="hello"):
                conn.sendall(bytes("hello","utf-8"))
                break

    def create(self):
        print("Waiting for the connection...")
        self.set_init_state()
        conn, addr = self.server.accept()
        print("Connection Established!!")
        self.state_control = Thread(target=controls.state_stream, args=[conn])
        while self.connection:
            if self.message_sent == 0:
                self.handshake(conn)
                self.message_sent += 1
                break
            try:
                data = conn.recv(1024).replace(b'\n', b'')
            except ConnectionAbortedError as e:
                return self.create()
            except ConnectionResetError:
                return self.create()
            print(data)
             # and str(data.decode("utf-8")) == "hello":
             #    print("hi there")
             #    conn.sendall(bytes("hello","utf-8"))
             #    self.message_sent += 1
             #    return self.create()

            if not data:
                try:
                    conn.sendall(bytes("", "utf-8"))
                except ConnectionAbortedError:
                    return self.create()
                except ConnectionResetError:
                    return self.create()

            command_list = self.decode_the_command(data)
            if command_list[0] == 2:
                th = Thread(target=controls.run, args=[command_list[1], command_list[2]])
                th.start()
                if command_list[1] == "url":
                    if controls.state_status == False:
                        self.state_control.start()
            elif command_list[0] == 1:
                if command_list[1] != "error":
                    th = Thread(target=controls.run, args=[command_list[1]])
                    th.start()
                else:
                    print("Command not recognized")


if __name__ == "__main__":
    obj = Server()
    obj.create()

# todo send constant messages about state of the video

# todo send keep alive packets

# todo create data file for: password

# todo create two way encryption algorithm for password
