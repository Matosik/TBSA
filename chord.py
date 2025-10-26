from socketmessage import *
from datetime import datetime


def get_addr(id: int):
    return ("127.0.0.1", 5000 + id)


class ChordNode:
    M = 4

    def __init__(self, id: int) -> None:
        self.id = id
        self.log("I was born!")
        self.prev = None
        self.finger = [{} for _ in range(self.M)]
        for i in range(self.M):
            self.finger[i]["start"] = (self.id + 2 ** i) % 2 ** self.M

    def log(self, msg: str):
        now = datetime.now()
        log_time = now.strftime("%H:%M:%S.%f")
        with open(f"{self.id}.log", "a", encoding="utf-8") as f:
            f.write(f"{log_time} {msg}\n")

    def network_create(self):
        """New node initialization"""
        self.prev = self.id
        for i in range(self.M):
            self.finger[i]["successor"] = self.id

    def network_join(self, id: int):
        """Request to the node to connect to the network"""
        self.log(f"Joining network by #{id}...")

        with socket.socket() as sock:
            sock.connect(get_addr(id))
            # connection request, send your id
            socket_send(sock, "connect", self.id.to_bytes(16, "little"))
            headers, content = socket_recv(sock)
            if headers[0] == "connect":
                if headers[1] == "redirect":
                    self.log(f"Connection denied, redirect on id {int.from_bytes(content, 'little')}")
                elif headers[1] == "ok":
                    prev_id = int.from_bytes(content, "little")
                    self.log(f"Connection accepted, my predecessor is {prev_id}")
                    self.prev = prev_id
                elif headers[1] == "deny":
                    self.log("Connection denied, id collision detected")
        self.find_fingers()

    def ping_node(self, id: int):
        is_alive = False
        sock = None

        try:
            sock = socket.create_connection(get_addr(id), source_address=("127.0.0.1", 6000 + self.id))
            socket_send(sock, "ping")
            headers, _ = socket_recv(sock)
            if headers[0] == "pong":
                is_alive = True
        except TimeoutError as err:
            pass
        finally:
            if sock is not None:
                sock.close()

        return is_alive

    def find_fingers(self):
        for i in range(self.M):
            logging.info(f"Finding successor for #{self.finger[i]['start']}")
            succ_id = self.finger[i]["start"]

            while True:
                logging.info(f"ping #{succ_id}")

                if succ_id == self.id:
                    self.finger[i]["successor"] = succ_id
                    break
                is_alive = self.ping_node(succ_id)
                if is_alive:
                    self.finger[i]["successor"] = succ_id
                    break
                succ_id = (succ_id + 1) % 16