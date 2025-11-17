import cv2
import numpy as np

# Função 'vazia' para os trackbars
def nothing(x):
    pass

# Captura da webcam
cap = cv2.VideoCapture(0)

# Criar uma janela para os trackbars
cv2.namedWindow("Trackbars")

# Criar trackbars para os valores de HSV
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

print("--- Reprodução do Projeto Base (Pysource) ---")
print("Ajuste os sliders na janela 'Trackbars' para isolar a cor do fundo.")
print("Pressione 'ESC' para sair.")

while True:
    # Ler o frame da webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Converter para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Obter os valores atuais dos trackbars
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Definir o range da cor (lower e upper)
    lower_green = np.array([l_h, l_s, l_v])
    upper_green = np.array([u_h, u_s, u_v])

    # Criar a máscara com base no range
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Inverter a máscara (para pegar o primeiro plano)
    mask_inv = cv2.bitwise_not(mask)

    # Aplicar a máscara para obter o fundo
    bg = cv2.bitwise_and(frame, frame, mask=mask)

    # Aplicar a máscara invertida para obter o primeiro plano
    fg = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Mostrar resultados
    cv2.imshow("Webcam Original", frame)
    cv2.imshow("Fundo (BG)", bg)
    cv2.imshow("Primeiro Plano (FG)", fg)

    # Esperar pela tecla 'ESC' para sair
    key = cv2.waitKey(1)
    if key == 27:
        break

# Liberar a câmera e fechar janelas
cap.release()
cv2.destroyAllWindows()