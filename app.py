
import streamlit as st
import fitz  # PyMuPDF
import io
from docx import Document
from docx.shared import Pt

# Banco de dicas por neurodivergência
DICAS = {
    "TDAH": "🔍 DICA TDAH: Leia a pergunta com atenção. Sublinhe palavras-chave antes de olhar as alternativas.",
    "TEA": "🧩 DICA TEA: Concentre-se no que está sendo pedido, uma coisa de cada vez. Ignore detalhes desnecessários.",
    "Ansiedade": "🧘‍♂️ DICA ANSIEDADE: Respire fundo antes de cada questão. Foque apenas na pergunta atual."
}

st.title("Adaptador de Provas para Alunos Neurodivergentes")

# Upload do PDF
pdf_file = st.file_uploader("Faça o upload da prova em PDF (texto selecionável)", type=["pdf"])

# Seleção da neurodivergência
neuro = st.selectbox("Escolha a neurodivergência do aluno:", ["TDAH", "TEA", "Ansiedade"])

if pdf_file and neuro:
    if st.button("Gerar Prova Adaptada"):
        text = ""
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

        # Separar questões com base em "QUESTÃO"
        blocos = text.split("QUESTÃO ")
        blocos = blocos[1:11]  # Pega no máximo 10 questões

        docx = Document()
        style = docx.styles["Normal"]
        font = style.font
        font.size = Pt(14)

        for i, bloco in enumerate(blocos, start=1):
            paragrafo = docx.add_paragraph()
            run = paragrafo.add_run(f"QUESTÃO {i} ")
            run.bold = True
            paragrafo.add_run(bloco.strip())

            # Adicionar dica
            docx.add_paragraph(DICAS[neuro], style="Normal")

        buffer = io.BytesIO()
        docx.save(buffer)
        buffer.seek(0)

        st.success("Prova adaptada gerada com sucesso!")
        st.download_button("📄 Baixar Prova Adaptada (DOCX)", buffer, file_name="prova_adaptada.docx")
