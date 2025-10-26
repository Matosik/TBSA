import socket
import logging
from json import dumps, loads


def socket_send(sock: socket.socket, header: str, content: bytes = 'empty'.encode('utf-8')):
    """
    Accepts a string of headers separated by the `;` character and content as `bytes`
    """
    try:
        # send header
        header_data = header.encode('utf-8')
        header_len = len(header_data)
        sock.send(header_len.to_bytes(4, 'little'))
        sock.send(header_data)
        # send content
        content_len = len(content)
        sock.send(content_len.to_bytes(4, 'little'))
        sock.send(content)
    except Exception as e:
        logging.error(e)
        raise e


def socket_recv(sock: socket.socket):
    """
    Returns a list of headers, and content as `bytes`
    """
    try:
        # recv header
        data = sock.recv(4)
        header_len = int.from_bytes(data, 'little')
        data = sock.recv(header_len)
        header = data.decode('utf-8')
        # recv content
        data = sock.recv(4)
        content_len = int.from_bytes(data, 'little')
        content = sock.recv(content_len)
        return header.split(';'), content
    except Exception as e:
        logging.error(e)
        raise e


def send_json(sock: socket.socket, header: str, data: dict | list):
    """
    Accepts a string of headings separated by the `;` character and content in the form of a `dict` or `list`
    """
    try:
        # send header
        header_data = header.encode('utf-8')
        header_len = len(header_data)
        sock.send(header_len.to_bytes(4, 'little'))
        sock.send(header_data)
        # send content
        content = dumps(data, ensure_ascii=False).encode("utf-8")
        content_len = len(content)
        sock.send(content_len.to_bytes(4, 'little'))
        sock.send(content)
    except Exception as e:
        logging.error(e)
        raise e


def recv_json(sock: socket.socket):
    """
    Returns a list of titles, and content in the form of `dict` or `list`
    """
    try:
        # recv header
        data = sock.recv(4)
        header_len = int.from_bytes(data, 'little')
        data = sock.recv(header_len)
        header = data.decode('utf-8')
        # recv content
        data = sock.recv(4)
        content_len = int.from_bytes(data, 'little')
        content = sock.recv(content_len)
        return header.split(';'), loads(content.decode("utf-8"))
    except Exception as e:
        logging.error(e)
        raise e