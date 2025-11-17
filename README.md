# 1. Título do Trabalho
[Introdução à Visão Computacional: Estúdio Virtual com IA e MediaPipe]

---

# 2. Integrantes do Grupo
* **Nome:** [Seu Nome Completo]
* **Matrícula:** [Sua Matrícula]

---

# 3. Descrição do Projeto
Este trabalho aplica os fundamentos de programação Python na área de Visão Computacional, utilizando a biblioteca OpenCV e MediaPipe. O projeto evolui da "Tarefa Mínima" (reprodução de um tutorial) para um sistema robusto de "Estúdio Virtual", demonstrando as melhorias e aperfeiçoamentos exigidos para a nota máxima, incluindo o uso de IA para segmentação de imagem e a criação de uma interface de usuário otimizada.

---

# 4. Instruções de Instalação e Execução

Siga os passos abaixo para configurar e executar os projetos.

### 1. Clonar o Repositório
```bash
git clone [URL-DO-SEU-REPOSITÓRIO-AQUI]
cd [NOME-DO-SEU-REPOSITÓRIO]
```

### 2. Criar e Ativar Ambiente Virtual
É crucial usar um ambiente virtual para isolar as dependências:
```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate
```

### 3. Instalar as Dependências
Instale todas as bibliotecas necessárias usando o `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Executar os Projetos
O código está organizado em níveis de aperfeiçoamento:

**Nível 1: Tarefa Mínima (Reprodução HSV)**
> Este script representa a reprodução fiel do tutorial, usando detecção de cor (HSV) e OpenCV. Pressione 'ESC' para sair.

```bash
python projeto_base_hsv.py
```

**Nível 2: Melhoria (IA + OpenCV)**
> Primeiro aperfeiçoamento: substitui o método HSV por Inteligência Artificial (MediaPipe) para segmentação de selfie. O resultado é muito superior e não depende de um fundo verde. Pressione 'ESC' para sair.

```bash
python projeto_melhorado_ia.py
```

**Nível 3: Projeto Final (Estúdio Virtual com Streamlit)**
> Esta é a versão final, que atende aos critérios de excelência. É uma aplicação web completa, otimizada e com interface de usuário.

```bash
streamlit run app_estudio_virtual.py
```
* (Opcional) Adicione um arquivo `background.jpg` na pasta para testar o fundo virtual.

---

# 5. Melhorias Implementadas

[cite_start]Conforme solicitado[cite: 26], o foco do trabalho foi o **aperfeiçoamento** da ideia original. A evolução do projeto demonstra melhorias significativas em funcionalidade, eficiência e interface.

### 1. Melhoria de Funcionalidade: IA (MediaPipe) vs. Cor (HSV)
* **Problema Original:** O método HSV é frágil, depende de iluminação perfeita e exige um fundo de cor sólida (green screen).
* **Solução (`projeto_melhorado_ia.py`):** Substituímos o `cv2.inRange` (HSV) pelo modelo de **IA `SelfieSegmentation` do Google MediaPipe**.
* **Vantagem:** A IA entende o que é uma "pessoa" e a segmenta perfeitamente em **qualquer ambiente**, independente da cor do fundo ou da iluminação.

### 2. Melhoria de Interface: Streamlit
* **Problema:** A janela do OpenCV é uma interface de usuário básica, sem controles.
* **Solução (`app_estudio_virtual.py`):** Criamos uma interface web (UI) com **Streamlit**, permitindo:
    * Upload de fundos virtuais dinamicamente.
    * Controles interativos (sliders) para a interface "Picture-in-Picture" (PiP).

### 3. Melhoria de Eficiência e Otimização: WebRTC
* **Problema:** As primeiras versões do Streamlit travavam muito (alto *lag*), pois processavam o vídeo frame a frame no back-end (Python).
* **Solução (`app_estudio_virtual.py`):** Implementamos a biblioteca **`streamlit-webrtc`**.
* **Vantagem:** O stream de vídeo é gerenciado de forma assíncrona, e o processamento de IA ocorre em um *thread* separado. Isso resulta em uma aplicação **fluida, em tempo real e sem travamentos**, demonstrando uma otimização de eficiência crucial.

### 4. Melhoria de UI/UX: Estúdio Virtual
* **Solução (`app_estudio_virtual.py`):** Combinamos todas as melhorias em um "Estúdio Virtual", onde o usuário tem controle total:
    * **Controle de PiP:** Sliders para Zoom, Posição X e Posição Y.
    * **Design Polido:** Um tema escuro profissional foi aplicado com CSS customizado, escondendo elementos desnecessários do Streamlit para criar uma aparência de aplicativo de desktop.
