import cv2
import numpy as np

# Usa câmera USB (troque o índice se necessário)
cap = cv2.VideoCapture(1)

# Coordenadas das mesas (x, y, w, h)
mesas = [
    (30, 53, 169, 93),
    (246, 3, 129, 77),
    (314, 84, 120, 77),
    (103, 159, 118, 99),
    (149, 261, 125, 102),
    (233, 379, 123, 96),
    (526, 297, 104, 86),
    (362, 166, 196, 126)
]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Converte para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Faixa de amarelo
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Faixa de azul
    lower_blue = np.array([90, 80, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Máscara combinada (amarelo OU azul)
    mask = cv2.bitwise_or(mask_yellow, mask_blue)

    # Verifica cada mesa
    for (x, y, w, h) in mesas:
        roi_mask = mask[y:y+h, x:x+w]
        colored_pixels = cv2.countNonZero(roi_mask)

        if colored_pixels > 50:  # Ajuste do limiar
            color = (0, 0, 255)  # vermelho
            status = "Ocupada"
        else:
            color = (0, 255, 0)  # verde
            status = "Vazia"

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, status, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Monitoramento Mesas", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
