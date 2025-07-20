import streamlit as st
import fitz  # PyMuPDF
import docx
import re
from io import BytesIO
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

st.set_page_config(page_title="AdaptaProva", layout="centered")

st.title("🧠 AdaptaProva - Provas Adaptadas para Alunos com Neurodivergência")
st.markdown("Envie uma prova em PDF com texto selecionável e selecione a neurodivergência do aluno para gerar uma versão adaptada.")

# Banco de dicas para cada neurodivergência
dicas_por_tipo = {
    "TDAH": [
        "Destaque palavras-chave da pergunta.",
        "Leia a pergunta duas vezes antes de escolher a resposta.",
        "Tente eliminar as alternativas claramente erradas primeiro."
    ],
    "TEA": [
        "Preste atenção nas palavras que indicam ordem, como 'primeiro', 'depois', 'por fim'.",
        "Leia com calma. Respire fundo antes de cada pergunta.",
        "Use rascunho para organizar o que entendeu da questão."
    ],
    "Ansiedade": [
        "Lembre-se: você pode fazer uma pergunta de cada vez com calma.",
        "Respire fundo antes de começar cada questão.",
        "Você está preparado. Confie no seu raciocínio!"
    ]
}

# Upload da prova em PDF
uploaded_file = st.file_uploader("📄 Envie a prova em PDF", type=["pdf"])

# Escolha da neurodivergência
tipo = st.selectbox("🧠 Neurodivergência do aluno:", ["TDAH", "TEA", "Ansiedade"])

if uploaded_file and tipo:
    if st.button("🔄 Gerar Prova Adaptada"):
        with st.spinner("Processando..."):

            # Lê o PDF com PyMuPDF
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            texto = ""
            for page in doc:
                texto += page.get_text()

            # Divide o texto por "QUESTÃO" usando regex
            blocos = re.split(r'\bQUESTÃO\s+\d+', texto)
            blocos = [b.strip() for b in blocos if b.strip()]

            # Remove o cabeçalho se ele aparecer antes da primeira questão real
            if len(blocos) > 10:
                blocos = blocos[1:]  # Remove o bloco inicial com cabeçalho

            blocos = blocos[:10]  # Pega até 10 questões

            # Cria o documento Word
            docx_file = docx.Document()
            docx_file.add_heading("Prova Adaptada", 0)

            # Fonte base
            style = docx_file.styles["Normal"]
            style.font.size = Pt(14)

            for i, bloco in enumerate(blocos):
                # Adiciona número da questão
                par = docx_file.add_paragraph()
                run = par.add_run(f"QUESTÃO {i+1}\n")
                run.bold = True
                par.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

                # Texto da questão
                questao_par = docx_file.add_paragraph(bloco.strip())
                questao_par.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
                for run in questao_par.runs:
                    run.font.size = Pt(14)

                # Espaço entre questão e dicas
                docx_file.add_paragraph("")

                # Dicas
                docx_file.add_paragraph("💡 Dicas para essa questão:", style="List Bullet")
                for dica in dicas_por_tipo[tipo]:
                    p = docx_file.add_paragraph(dica, style="List Bullet")
                    p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

                # Espaço antes da próxima questão
                docx_file.add_paragraph("")

            # Salvar em memória
            buffer = BytesIO()
            docx_file.save(buffer)
            buffer.seek(0)

            st.success("Prova adaptada gerada com sucesso!")
            st.download_button(
                label="📥 Baixar Prova Adaptada (.docx)",
                data=buffer,
                file_name="prova_adaptada.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

