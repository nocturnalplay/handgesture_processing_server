import websocket
from handGesture import hand
import cv2
import mediapipe as mp
import json
import math

def on_message(ws, message):
    ws.send(json.dumps(message))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket connected")

def findPercents(inp, mi, ma, v):
    va = (inp - mi) * 100 / (ma - mi)
    if v == 100:
        va = v - va
    if va > 100:
        return 100
    elif va < 0:
        return 0
    else:
        return int(va)


def RGB(right,img):
    print("RGB Effect like Doctor Strange")
    # rgb x and y axis point
    x0, y0 = right[0][0], right[0][1]
    rx, ry = right[4][0], right[4][1]
    gx, gy = right[8][0], right[8][1]
    bx, by = right[12][0], right[12][1]

    # circle shape x and y axis point
    cv2.circle(img, (rx, ry), 8, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (gx, gy), 8, (0, 255, 0), cv2.FILLED)
    cv2.circle(img, (bx, by), 8, (255, 0, 0), cv2.FILLED)

     # lines for the eache shape in rgb
    cv2.line(img, (x0, y0), (rx, ry), (0, 0, 255), 2)
    cv2.line(img, (x0, y0), (gx, gy), (0, 255, 0), 2)
    cv2.line(img, (x0, y0), (bx, by), (255, 0, 0), 2)
    # connect in bellow bottom point of index 0
    cv2.circle(img, (x0, y0), 8, (255, 255, 255), cv2.FILLED)
    Rlen = [findPercents(math.hypot(rx - x0, ry - y0), 155, 185, 0),
                    findPercents(math.hypot(rx - x0, ry - y0), 155, 185, 100)]
    Glen = [findPercents(math.hypot(gx - x0, gy - y0), 140, 240, 0),
                    findPercents(math.hypot(gx - x0, gy - y0), 140, 240, 100)]
    Blen = [findPercents(math.hypot(bx - x0, by - y0), 120, 260, 0),
                    findPercents(math.hypot(bx - x0, by - y0), 120, 260, 100)]

    rgb = [Rlen[1], Glen[1], Blen[1]]
    return rgb


if __name__ == "__main__":
    # Specify the WebSocket server URL
    ws_url = "ws://192.168.1.5:80"

    # Create a WebSocket connection
    ws = websocket.WebSocket()
    ws.connect(ws_url)
    ws.on_open = on_open

    # Start the WebSocket connection and keep it running
    ws.run_forever()

    hands = hand.Hand(max_hands=1)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        res = hand.DetectHands(frame, hands)
        if not res['status']:
            break
        img = res["image"]
        data = (res["data"])

        if "right" in data:
            ws.send(json.dumps(RGB(data["right"])))

        # Display the resulting image
        cv2.imshow('Hand Gestures', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    sys.exit()