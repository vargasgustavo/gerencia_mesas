import cv2
import numpy as np
import os

# Câmera USB (troque o índice se necessário)
cap = cv2.VideoCapture(1)

mesas = []
desenhando = False
x_inicial, y_inicial = -1, -1

# Função de callback do mouse para selecionar mesas
def selecionar_mesa(event, x, y, flags, param):
    global x_inicial, y_inicial, desenhando, mesas

    if event == cv2.EVENT_LBUTTONDOWN:
        desenhando = True
        x_inicial, y_inicial = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        desenhando = False
        x_final, y_final = x, y
        w, h = abs(x_final - x_inicial), abs(y_final - y_inicial)
        x0, y0 = min(x_inicial, x_final), min(y_inicial, y_final)
        mesas.append((x0, y0, w, h))
        print(f"Mesa adicionada: {(x0, y0, w, h)}")

# Carregar mesas salvas, se existir
if os.path.exists("mesas.npy"):
    mesas = np.load("mesas.npy", allow_pickle=True).tolist()
    print("Mesas carregadas:", mesas)

cv2.namedWindow("Monitoramento Mesas")
cv2.setMouseCallback("Monitoramento Mesas", selecionar_mesa)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detecção de amarelo (ajustar se necessário)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Verificação de ocupação para cada mesa
    for (x, y, w, h) in mesas:
        roi_mask = mask[y:y+h, x:x+w]
        yellow_pixels = cv2.countNonZero(roi_mask)

        if yellow_pixels > 50:
            color = (0, 0, 255)
            status = "Ocupada"
        else:
            color = (0, 255, 0)
            status = "Vazia"

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, status, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, color, 2)

    cv2.imshow("Monitoramento Mesas", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # sair
        break
    elif key == ord('s'):  # salvar mesas
        np.save("mesas.npy", np.array(mesas))
        print("Mesas salvas!")

cap.release()
cv2.destroyAllWindows()
    