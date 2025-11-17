import cv2
import numpy as np
import mediapipe as mp

# --- 1. Inicialização ---

# Inicializar o MediaPipe Selfie Segmentation
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=0) 
# model_selection=0: Modelo geral (mais rápido)
# model_selection=1: Modelo de paisagem (mais preciso)

# Inicializar o OpenCV para webcam
cap = cv2.VideoCapture(0)

# Tentar carregar a imagem de fundo
try:
    background = cv2.imread('background.jpg')
    print("Imagem de fundo 'background.jpg' carregada.")
    
    # Obter dimensões da webcam para redimensionar o fundo UMA VEZ
    ret, frame_teste = cap.read()
    if ret:
        bg_height, bg_width = frame_teste.shape[:2]
        background = cv2.resize(background, (bg_width, bg_height))
    else:
        raise Exception("Não foi possível ler a webcam.")
        
    use_image_bg = True

except Exception as e:
    print(f"Aviso: {e}")
    print("Usando um fundo preto.")
    use_image_bg = False
    background = None # Será criado um fundo preto dinamicamente

print("--- Projeto Melhorado com IA (MediaPipe) ---")
print("Não é necessário fundo verde nem ajustes.")
print("Pressione 'ESC' para sair.")

# --- 2. Loop Principal ---

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Erro ao ler frame da webcam.")
        break

    # Se não carregou imagem, cria um fundo preto do tamanho do frame
    if not use_image_bg:
        background = np.zeros_like(frame)

    # --- 3. Processamento com IA ---
    
    # O MediaPipe espera cores RGB, o OpenCV usa BGR
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Processar o frame e obter a máscara de segmentação
    results = segmentation.process(frame_rgb)

    # 'results.segmentation_mask' é uma matriz (H, W) com valores de 0.0 (fundo) a 1.0 (pessoa)
    mask_float = results.segmentation_mask
    
    # Criar a máscara invertida (para o fundo)
    mask_inv_float = 1.0 - mask_float

    # --- 4. Composição (Blending) ---
    # Esta é uma forma mais eficiente (vetorizada com NumPy) de fazer o 'bitwise_and'

    # Expandir as máscaras de 1 canal (H, W) para 3 canais (H, W, 3) para multiplicar pelas imagens
    mask_3d = np.stack((mask_float,) * 3, axis=-1)
    mask_inv_3d = np.stack((mask_inv_float,) * 3, axis=-1)

    # Multiplicar o frame pela máscara da pessoa
    # (Converte para float, multiplica, e converte de volta para uint8)
    foreground = (frame * mask_3d).astype(np.uint8)

    # Multiplicar a imagem de fundo pela máscara invertida
    background_part = (background * mask_inv_3d).astype(np.uint8)

    # Combinar o primeiro plano (da webcam) com o fundo (da imagem)
    final_frame = cv2.add(foreground, background_part)

    # --- 5. Exibição ---
    cv2.imshow("Webcam Original", frame)
    cv2.imshow("Resultado Final com IA", final_frame)

    key = cv2.waitKey(5) & 0xFF
    if key == 27:  # ESC
        break

# --- 6. Liberação ---
cap.release()
cv2.destroyAllWindows()