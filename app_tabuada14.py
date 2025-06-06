# -*- coding: utf-8 -*-
"""app_tabuada14.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hi6yfXn8PjflrqiySM3K18sedi8wC5Lx
"""

import streamlit as st
import random
from gtts import gTTS
import os
import time
import pandas as pd
import plotly.express as px

# --- Configurações Iniciais ---
TOTAL_PERGUNTAS = 10  # Mantido em 10 perguntas
# NUM_COLUMNS não é mais relevante para o modo uma a uma

# 1. O PRIMEIRO COMANDO STREAMLIT DEVE SER SEMPRE st.set_page_config()
st.set_page_config(
    page_title="Maratona das Tabuadas Divertida!",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🌟",
)


# --- Funções Auxiliares ---
def falar(texto):
    """
    Função para converter texto em voz.
    ATENÇÃO: Não está sendo usada neste modelo de 30 perguntas simultâneas.
    """
    try:
        tts = gTTS(text=texto, lang="pt", slow=False)
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        st.audio(audio_file, format="audio/mp3", start_time=0, loop=False)
        time.sleep(max(1.5, len(texto) * 0.08))
        if os.path.exists(audio_file):
            os.remove(audio_file)
    except Exception as e:
        print(f"Erro detalhado ao gerar/reproduzir áudio: {e}")
        st.warning(
            "Não foi possível reproduzir o áudio. Verifique sua conexão com a internet ou as permissões do navegador."
        )


def gerar_lista_perguntas():
    """Gera uma lista de perguntas de tabuada aleatórias e únicas."""
    perguntas = []
    perguntas_unicas = set()

    while len(perguntas) < TOTAL_PERGUNTAS:
        num1 = random.randint(2, 9)
        num2 = random.randint(1, 10)

        pergunta_par = (num1, num2)

        if pergunta_par not in perguntas_unicas:
            perguntas_unicas.add(pergunta_par)
            pergunta_texto = f"{num1} x {num2} = ?"
            resposta_correta = num1 * num2
            perguntas.append(
                {"id": len(perguntas), "pergunta": pergunta_texto, "resposta_correta": resposta_correta}
            )
    return perguntas


def inicializar_estado():
    """Inicializa as variáveis de estado da sessão do Streamlit."""
    if "iniciado" not in st.session_state:
        st.session_state.iniciado = False
    if "perguntas" not in st.session_state:
        st.session_state.perguntas = []
    if "respostas_usuario" not in st.session_state:
        st.session_state.respostas_usuario = {}
    if "mostrar_resultados_finais" not in st.session_state:
        st.session_state.mostrar_resultados_finais = False
    if "acertos" not in st.session_state:
        st.session_state.acertos = 0
    if "erros" not in st.session_state:
        st.session_state.erros = 0
    if "last_key" not in st.session_state:
        st.session_state.last_key = time.time()
    # Adicionado para controlar a pergunta atual no modo uma a uma
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0


def iniciar_maratona():
    """Reinicia a maratona de perguntas."""
    st.session_state.iniciado = True
    st.session_state.perguntas = gerar_lista_perguntas()
    st.session_state.respostas_usuario = {p["id"]: None for p in st.session_state.perguntas}
    st.session_state.mostrar_resultados_finais = False
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.last_key = time.time()
    st.session_state.current_question_index = 0 # Reinicia o índice da pergunta
    st.rerun()


# A função verificar_todas_respostas() não será mais necessária no fluxo "uma a uma",
# pois a verificação será feita a cada pergunta.
# Sua lógica será incorporada na ação do botão "Próxima Pergunta".


# --- Funções de Mensagens Motivacionais ---
def exibir_mensagem_motivacional(percentual):
    st.write("")  # Espaçamento
    if percentual == 100:
        st.balloons()  # Efeito de balões!
        st.markdown(
            "<h3 style='text-align: center; color: #28A745;'>🎉 Uau! Que demais! 100% de acerto! Você é um gênio da tabuada! Parabéns! 🎉</h3>",
            unsafe_allow_html=True,
        )
    elif percentual >= 80:
        st.success("🌟 Incrível! Você está mandando muito bem nas tabuadas! Continue assim!")
    elif percentual >= 50:
        st.info("👍 Muito bom! Você já acertou bastante. Um pouco mais de prática e você chega lá!")
    else:
        st.warning(
            "💪 Não desanime! Cada erro é uma chance de aprender. Continue praticando, você vai conseguir!"
        )
    st.write("")  # Espaçamento


# --- Estilo CSS Personalizado (para imagem de fundo e outros elementos) ---
# URL RAW da imagem do GitHub
BACKGROUND_IMAGE_RAW_URL = "https://raw.githubusercontent.com/marciaestudar/projeto_simulador/main/imagem_numeros5.jpeg" # Verifique se essa URL está correta ou se deveria ser .png

page_bg_img_css = f"""
        <style>
        /* Estilo para o container principal do Streamlit */
        [data-testid="stAppViewContainer"] {{
            background-image: url("{BACKGROUND_IMAGE_RAW_URL}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}

        /* Garantir que o container principal do conteúdo seja transparente */
        [data-testid="stAppViewContainer"] > .main {{
            background-color: rgba(255, 255, 255, 0) !important; /* Totalmente transparente */
        }}

        /* Garantir que o bloco de conteúdo principal também seja transparente */
        [data-testid="stVerticalBlock"] {{
            background-color: rgba(255, 255, 255, 0) !important; /* Totalmente transparente */
        }}

        /* Estilos para o texto: cor, negrito, sem sombra */
        /* Geral para todos os textos, exceto os títulos principais que têm suas cores específicas */
        h3, p, span, div, .stTextInput > div > div > input {{
            color: #080404 !important; /* Preto */
            font-weight: bold !important; /* Texto em negrito */
        }}

        /* Ajustar cor do texto para títulos principais sem sombra, mantendo negrito */
        h1 {{
            color: #F20A1D !important; /* Vermelho Rosa/Fúcsia para h1 */
            font-weight: bold !important;
        }}
        /* Ajustar cor do texto do h2 (especificamente o "Vamos aprender e brincar muito!") para azul negrito */
        h2 {{
            color: #bf0f18 !important; /* vermelho céu profundo para h2 */
            font-weight: bold !important;
        }}

        /* Ajuste de cor do input de texto para contraste */
        .stTextInput > div > div > input {{
            background-color: rgba(255, 255, 255, 0.85) !important; /* Fundo semi-transparente para o input */
            color: #9E0303 !important; /* Cor do texto no input (vermelho escuro) */
            border-radius: 5px !important; /* Bordas arredondadas para o input */
            padding: 8px 12px !important; /* Espaçamento interno */
        }}

        /* Ajustar cor de fundo do st-emotion-cache para inputs e botões */
        /* Isso tenta forçar o fundo branco mesmo com tema escuro do Streamlit */
        div[data-testid="stTextInput"], div[data-testid="stButton"] {{
            background-color: white !important; /* Fundo branco para os elementos */
            border-radius: 8px !important; /* Manter bordas arredondadas */
        }}

        /* --- ESTILO PARA TODOS OS BOTÕES: FUNDO BRANCO (PADRÃO) E TEXTO PRETO NEGRITO --- */
        div > button {{
            color: black !important; /* Texto preto */
            font-weight: bold !important; /* Texto em negrito */
            border-radius: 8px; /* Bordas mais arredondadas */
            padding: 10px 20px; /* Mais espaçamento interno */
            font-size: 18px; /* Tamanho do texto do botão */
            border: 1px solid #333; /* Borda sutil para definir o botão */
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3); /* Sombra para dar profundidade */
            transition: all 0.2s ease-in-out; /* Transição suave para hover */
            background-color: white !important; /* Forçando o fundo branco padrão */
        }}

        /* Estilo para quando o mouse passa por cima de qualquer botão */
        div > button:hover {{
            background-color: #dc3545 !important; /* Vermelho no hover */
            color: white !important; /* Texto branco no hover para melhor contraste */
            transform: translateY(-2px); /* Pequeno movimento para cima */
            box-shadow: 4px 4px 10px rgba(0,0,0,0.4); /* Sombra maior no hover */
        }}

        /* Estilo para quando o botão está ativo (clicado) - opcional */
        div > button:active {{
            background-color: #c82333 !important; /* Vermelho mais escuro ao clicar */
            transform: translateY(0); /* Remove o movimento ao clicar */
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3); /* Restaura a sombra ao clicar */
        }}

        </style>
        """
st.markdown(page_bg_img_css, unsafe_allow_html=True)


# --- Layout do Streamlit ---

# Título principal com cores vibrantes
st.markdown("<h1 style='text-align: center;'>🌟 Maratona das Tabuadas Divertida! 🌟</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Vamos aprender e brincar muito!</h2>", unsafe_allow_html=True)

inicializar_estado()

if not st.session_state.iniciado:
    # Frases uma embaixo da outra, com cores e tamanho ajustados
    st.markdown("<p style='font-size: 25px; color: #3366FF;'><b>Prepare-se para exercitar suas tabuadas de 2 a 9!</b></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 25px; color: #FF4500;'><b>Você terá {TOTAL_PERGUNTAS} perguntas aleatórias e únicas para resolver de uma vez.</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 25px; color: #8A2BE2;'><b>Ao final, poderá verificar seu percentual de acertos.</b></p>", unsafe_allow_html=True)

    st.write("")
    if st.button("🚀 Iniciar Maratona Agora!", key="btn_iniciar_tela_inicial", help="Começar o desafio de tabuadas"):
        iniciar_maratona()

    if st.session_state.mostrar_resultados_finais:
        st.divider()
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>🎉 Resultados da Última Maratona 🎉</h2>", unsafe_allow_html=True)

        # --- CHAMADA PARA MENSAGENS MOTIVACIONAIS (alocada aqui) ---
        percentual = (st.session_state.acertos / TOTAL_PERGUNTAS) * 100 if TOTAL_PERGUNTAS > 0 else 0
        exibir_mensagem_motivacional(percentual) # Chamada da função de mensagens motivacionais

        st.markdown(f"<p style='font-size: 20px; color: #28A745;'>Acertos: <b>{st.session_state.acertos}</b></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 20px; color: #DC3545;'>Erros: <b>{st.session_state.erros}</b></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 20px; color: #6F42C1;'>Percentual de Acertos: <b>{percentual:.2f}%</b></p>", unsafe_allow_html=True)

        data = {'Categoria': ['Acertos', 'Erros'],
                'Quantidade': [st.session_state.acertos, st.session_state.erros]}
        df = pd.DataFrame(data)

        fig = px.pie(df, values='Quantidade', names='Categoria',
                    title='Desempenho Geral',
                    color_discrete_sequence=['#4CAF50', '#F44336'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            if st.button("🔄 Reiniciar Maratona", key="btn_reiniciar_apos_finalizar", help="Começar um novo desafio"):
                iniciar_maratona()
        with col_res2:
            if st.button("🔴 Finalizar o Aplicativo", key="btn_finalizar", help="Finalizar o aplicativo"):
                st.write("Aplicativo finalizado. Você pode fechar esta aba.")
                st.stop()

        st.divider()
        st.markdown("<p style='text-align: center; font-size: 25px; color: #800080;'><b>Autora: Márcia Romanato</b></p>", unsafe_allow_html=True)

else:
    # --- Lógica para perguntas uma a uma ---
    if st.session_state.current_question_index < TOTAL_PERGUNTAS:
        pergunta_atual = st.session_state.perguntas[st.session_state.current_question_index]

        st.markdown("<h3 style='color: #008080;'>Responda a pergunta abaixo:</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 25px; color: #B22222;'><b>Atenção:</b> Digite apenas números. Digitar algo diferente será contado como erro.</p>", unsafe_allow_html=True)

        st.divider()

        # Usamos um formulário para que o input possa ser resetado após o submit
        with st.form(key=f"question_form_{st.session_state.current_question_index}"):
            st.markdown(f"<p style='font-size: 30px; font-weight: bold; color: #5F9EA0;'>{pergunta_atual['pergunta']}</p>", unsafe_allow_html=True)

            resposta_usuario = st.text_input(
                "Sua resposta:",
                key=f"resposta_input_{pergunta_atual['id']}_{st.session_state.last_key}",
                max_chars=3
            )

            # O botão de submissão do formulário
            submit_button_text = "Próxima Pergunta"
            if st.session_state.current_question_index == TOTAL_PERGUNTAS - 1:
                submit_button_text = "Verificar Resultados Finais"

            submitted = st.form_submit_button(submit_button_text)

            if submitted:
                resposta_correta = pergunta_atual["resposta_correta"]
                st.session_state.respostas_usuario[pergunta_atual["id"]] = resposta_usuario

                if not resposta_usuario or not resposta_usuario.strip():
                    st.session_state.erros += 1
                else:
                    try:
                        resposta_digitada = int(resposta_usuario)
                        if resposta_digitada == resposta_correta:
                            st.session_state.acertos += 1
                        else:
                            st.session_state.erros += 1
                    except ValueError:
                        st.session_state.erros += 1

                # Avança para a próxima pergunta ou finaliza
                st.session_state.current_question_index += 1
                if st.session_state.current_question_index < TOTAL_PERGUNTAS:
                    st.rerun() # Recarrega para mostrar a próxima pergunta
                else:
                    # Finaliza a maratona e mostra os resultados
                    st.session_state.mostrar_resultados_finais = True
                    st.session_state.iniciado = False
                    st.rerun() # Recarrega para ir para a tela de resultados

    else:
        # Quando todas as perguntas forem respondidas, mostra os resultados finais
        st.session_state.mostrar_resultados_finais = True
        st.session_state.iniciado = False
        st.rerun() # Recarrega para ir para a tela de resultados

    st.divider()
    st.markdown("<p style='text-align: center; font-size: 25px; color: #800080;'><b>Desenvolvido: Márcia Romanato</b></p>", unsafe_allow_html=True)