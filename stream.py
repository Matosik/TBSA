# stream.py
import cv2
import requests
import time

# Адрес сервера (измените на IP вашего сервера в локальной сети)
SERVER_URL = "http://<SERVER_IP>:5000"  # <-- замените <SERVER_IP> на реальный IP
UPLOAD_ENDPOINT = SERVER_URL + "/upload"

def main():
    cap = cv2.VideoCapture(0)  # 0 — системная веб-камера
    if not cap.isOpened():
        print("Не удалось открыть камеру.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Кадр не получен, повтор...")
                time.sleep(0.1)
                continue

            # Кодируем кадр в JPEG
            ret2, buf = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not ret2:
                continue

            # Отправляем как multipart/form-data поле 'frame'
            files = {'frame': ('frame.jpg', buf.tobytes(), 'image/jpeg')}
            try:
                resp = requests.post(UPLOAD_ENDPOINT, files=files, timeout=1.0)
                # опционально: печатаем статус раз в N кадров
                # print(resp.status_code, resp.text)
            except requests.RequestException as e:
                print("Ошибка отправки кадра:", e)
                time.sleep(0.5)

            # Небольшая задержка, чтобы не перегружать сеть/камеру
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Остановка захвата.")
    finally:
        cap.release()

if __name__ == '__main__':
    main()
