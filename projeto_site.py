import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image
import threading

# 1. IMPORTAR A BIBLIOTECA WEBRTC
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# --- Configurações da Página e Resolução ---
BG_WIDTH = 1280
BG_HEIGHT = 720
# Define a página para layout "wide"
st.set_page_config(layout="wide", page_title="Estúdio Virtual")

# --- CSS COM O NOVO DESIGN ---
st.markdown(f"""
    <style>
        /* --- 1. Tema Dark Mode Global --- */
        body {{
            background-color: #1E1E1E; /* Fundo escuro principal */
            color: #FAFAFA; /* Texto claro */
        }}
        /* Aplica ao container principal do Streamlit */
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
            background-color: #1E1E1E;
        }}
        /* --- 2. Design da Barra Lateral (Sidebar) --- */
        [data-testid="stSidebar"] > div:first-child {{
            background-color: #2A2A2A; /* Cor de fundo da sidebar */
            border-right: 1px solid #333;
        }}
        [data-testid="stSidebar"] h1 {{
            color: #4A90E2; /* Cor de destaque (Azul) para o título */
            padding-top: 1rem;
        }}
        [data-testid="stSidebar"] h3 {{
            color: #FAFAFA; /* Títulos das seções */
        }}
        /* Estilo dos botões na sidebar */
        [data-testid="stSidebar"] .stButton > button {{
            background-color: #4A90E2;
            color: white;
            border: none;
            border-radius: 5px;
            width: 100%;
        }}
        [data-testid="stSidebar"] .stButton > button:hover {{
            background-color: #357ABD; /* Cor mais escura no hover */
            color: white;
        }}

        /* --- 3. Esconder "Poluição" do Streamlit --- */
        [data-testid="stHeader"] {{
            display: none; /* Esconde o menu do topo (deploy, etc.) */
        }}
        footer {{
            display: none; /* Esconde o rodapé "Made with Streamlit" */
        }}

        /* --- 4. Container do Vídeo (Polido) --- */
        .video-container {{
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: start;
            padding-top: 1rem; /* Menos espaço no topo */
            padding-bottom: 10px;
        }}
        .video-container video {{
            width: {BG_WIDTH}px !important;
            height: {BG_HEIGHT}px !important;
            object-fit: contain;
            border-radius: 12px; /* Bordas mais arredondadas */
            box-shadow: 0 8px 20px rgba(0,0,0,0.5); /* Sombra mais forte */
        }}
    </style>
""", unsafe_allow_html=True)

# --- 2. Classe Processadora de Vídeo ---
# (Exatamente como estava antes)
class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
        self.lock = threading.Lock()
        
        # Valores padrão
        self.scale_pct = 30
        self.pos_x_pct = 50
        self.pos_y_pct = 50
        self.background_image = None
    
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1) # Espelhar
        webcam_h, webcam_w = img.shape[:2]

        with self.lock:
            scale_pct = self.scale_pct
            pos_x_pct = self.pos_x_pct
            pos_y_pct = self.pos_y_pct
            background_image = self.background_image
        
        # 1. PREPARAR O FUNDO
        if background_image is not None:
            final_image = cv2.resize(background_image, (BG_WIDTH, BG_HEIGHT))
        else:
            final_image = np.zeros((BG_HEIGHT, BG_WIDTH, 3), dtype=np.uint8)

        # 2. PREPARAR OVERLAY (WEBCAM)
        new_h = int(webcam_h * (scale_pct / 100))
        new_w = int(webcam_w * (scale_pct / 100))
        small_frame = cv2.resize(img, (new_w, new_h))
        
        small_frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        results = self.segmentation.process(small_frame_rgb)
        mask_float = results.segmentation_mask
        condition = np.stack((mask_float,) * 3, axis=-1) > 0.1

        # 3. CALCULAR POSIÇÃO (BASEADO NOS SLIDERS DE %)
        x_offset = int((BG_WIDTH - new_w) * (pos_x_pct / 100))
        y_offset = int((BG_HEIGHT - new_h) * (pos_y_pct / 100))

        # 4. COMPOSIÇÃO
        x1, x2 = max(0, x_offset), min(BG_WIDTH, x_offset + new_w)
        y1, y2 = max(0, y_offset), min(BG_HEIGHT, y_offset + new_h)

        small_frame_crop = small_frame[
            max(0, -y_offset) : new_h - max(0, (y_offset + new_h) - BG_HEIGHT),
            max(0, -x_offset) : new_w - max(0, (x_offset + new_w) - BG_WIDTH)
        ]
        condition_crop = condition[
            max(0, -y_offset) : new_h - max(0, (y_offset + new_h) - BG_HEIGHT),
            max(0, -x_offset) : new_w - max(0, (x_offset + new_w) - BG_WIDTH)
        ]

        if x1 < x2 and y1 < y2 and small_frame_crop.shape[0] > 0 and small_frame_crop.shape[1] > 0:
            roi = final_image[y1:y2, x1:x2]
            if roi.shape == small_frame_crop.shape:
                combined_roi = np.where(condition_crop, small_frame_crop, roi)
                final_image[y1:y2, x1:x2] = combined_roi
        
        return final_image

# --- 3. Interface Principal (Sidebar) ---
# (Valores de estado são os mesmos)
if "scale" not in st.session_state:
    st.session_state.scale = 30
if "pos_x" not in st.session_state:
    st.session_state.pos_x = 50 # Posição X em %
if "pos_y" not in st.session_state:
    st.session_state.pos_y = 50 # Posição Y em %
if "background" not in st.session_state:
    st.session_state.background = None

# --- TÍTULOS DA SIDEBAR ATUALIZADOS ---
st.sidebar.title("Painel de Controle 🎙️")
st.sidebar.markdown("---")
st.sidebar.markdown("### 1. Posição da Câmera (PiP)")

scale_pct = st.sidebar.slider("Tamanho (Zoom %)", 10, 100, st.session_state.scale, key="scale")
pos_x_pct = st.sidebar.slider("Posição Horizontal (%)", 0, 100, st.session_state.pos_x, key="pos_x")
pos_y_pct = st.sidebar.slider("Posição Vertical (%)", 0, 100, st.session_state.pos_y, key="pos_y")

st.sidebar.markdown("---")
st.sidebar.markdown("### 2. Fundo Virtual")
uploaded_file = st.sidebar.file_uploader("Escolha sua imagem de fundo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.session_state.background = np.array(image)
    st.session_state.background = cv2.cvtColor(st.session_state.background, cv2.COLOR_RGB2BGR)
    st.sidebar.image(image, caption="Fundo Carregado")
elif st.sidebar.button("Remover Fundo"):
    st.session_state.background = None

# --- 4. Interface Principal (Canvas) ---
# --- TÍTULO PRINCIPAL ATUALIZADO ---
st.title("Meu Estúdio Virtual 🚀")
st.markdown("Controle sua cena usando o painel à esquerda e clique em **START** no player de vídeo.")

# Adiciona o container CSS para centralizar
st.markdown('<div class="video-container">', unsafe_allow_html=True)

# 5. INICIAR O STREAMER WEBRTC
# (Exatamente como estava antes)
ctx = webrtc_streamer(
    key="webrtc_stream",
    video_transformer_factory=VideoProcessor,
    media_stream_constraints={
        "video": {"width": 640, "height": 480}, # Webcam em 480p
        "audio": False
    },
    async_processing=True,
)

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. Atualiza a classe VideoProcessor com os novos valores ---
# (Exatamente como estava antes)
if ctx.video_transformer:
    with ctx.video_transformer.lock:
        ctx.video_transformer.scale_pct = st.session_state.scale
        ctx.video_transformer.pos_x_pct = st.session_state.pos_x
        ctx.video_transformer.pos_y_pct = st.session_state.pos_y
        ctx.video_transformer.background_image = st.session_state.background