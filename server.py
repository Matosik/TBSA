# server.py
from flask import Flask, Response, send_from_directory, request, abort
import threading

app = Flask(__name__, static_folder='.')

# Общая переменная для последнего кадра (JPEG bytes)
latest_frame = None
cond = threading.Condition()

@app.route('/')
def index():
    # отдать клиентскую html (client.html лежит в той же папке)
    return send_from_directory('.', 'client.html')

@app.route('/upload', methods=['POST'])
def upload_frame():
    """
    Ожидается multipart/form-data с полем 'frame' (файл jpeg).
    stream.py отправляет кадры сюда.
    """
    global latest_frame
    if 'frame' not in request.files:
        return "No frame", 400
    f = request.files['frame']
    data = f.read()
    if not data:
        return "Empty frame", 400

    # Обновляем кадр и оповещаем потребителей
    with cond:
        latest_frame = data
        cond.notify_all()
    return "OK", 200

def mjpeg_generator():
    """
    Генератор отдаёт multipart/x-mixed-replace с последними кадрами.
    Ждём появления нового кадра и отдаем его.
    """
    boundary = "--frame"
    while True:
        with cond:
            # Ждём пока появится кадр
            cond.wait()
            frame = latest_frame
        if frame is None:
            continue
        # Формирование части MJPEG
        part = (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n"
            b"Content-Length: " + str(len(frame)).encode() + b"\r\n\r\n"
            + frame + b"\r\n"
        )
        yield part

@app.route('/video_feed')
def video_feed():
    return Response(mjpeg_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Запуск сервера на всех интерфейсах (доступ в локальной сети)
    # Порт 5000 (можно изменить при необходимости)
    app.run(host='0.0.0.0', port=5000, threaded=True)
