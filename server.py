from threading import Thread
import socket
import chord
from socketmessage import socket_recv, socket_send

socket.setdefaulttimeout(1)

node: chord.ChordNode = None
exit_flag = False
node_id = None


def get_addr(id: int):
    return ("127.0.0.1", 5000 + id)


def handle_client(sock: socket.socket, addr: tuple):
    global node
    client_addr_str = f"{addr[0]}:{addr[1]}"
    headers, content = socket_recv(sock)

    if headers[0] == "connect":
        new_id = int.from_bytes(content, "little")
        node.log(f"From {client_addr_str}: connect {new_id}")
        # if prev == id: ok
        # if prev > new: redirect prev
        # if prev < new and id > new: ok
        # if id < new: redirect finger[0]
        # if prev == new or id == new: deny
        if node.prev == node.id:
            socket_send(sock, "connect;ok", node.id.to_bytes(4, "little"))
        elif node.prev > new_id:
            socket_send(sock, "connect;redirect", node.prev.to_bytes(4, "little"))
        elif node.prev < new_id and node.id > new_id:
            socket_send(sock, "connect;ok", node.prev.to_bytes(4, "little"))
        elif node.id < new_id:
            redirect_id = node.finger[0]["successor"]
            socket_send(sock, "connect;redirect", redirect_id.to_bytes(4, "little"))
        else:
            socket_send(sock, "connect;deny")
    elif headers[0] == "ping":
        socket_send(sock, "pong")

    sock.close()


def listener():
    global node
    sock = socket.socket()
    sock.bind(get_addr(node.id))
    sock.listen(16)

    while True:
        if exit_flag:
            sock.close()
            break
        try:
            client_sock, client_addr = sock.accept()
            client_thread = Thread(target=handle_client, args=[client_sock, client_addr])
            client_thread.start()
        except TimeoutError as err:
            pass


def start():
    server_thread = Thread(target=listener)
    server_thread.start()