import streamlit as st
import fitz  # PyMuPDF
import docx
import re
from io import BytesIO

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

            # Divide o texto por questões (ex: "1 ", "2 ", "3 ") usando regex
            questoes = re.split(r'\n?\s*(?:\d+)[\.\)\-]?\s+', texto)
            questoes = [q.strip() for q in questoes if q.strip()]
            questoes = questoes[:10]  # Limita a 10 questões

            # Cria o documento Word
            docx_file = docx.Document()
            docx_file.add_heading("Prova Adaptada", 0)

            for i, questao in enumerate(questoes):
                enunciado = re.sub(r'^\d+\s*[-.)]?\s*', '', questao)  # Remove numeração duplicada

                # Adiciona a questão
                p = docx_file.add_paragraph()
                p.add_run(f"QUESTÃO {i+1}\n").bold = True
                p.add_run(enunciado + "\n")

                # Adiciona dicas
                docx_file.add_paragraph("💡 Dicas para resolver essa questão:", style='List Bullet')
                for dica in dicas_por_tipo[tipo]:
                    docx_file.add_paragraph(dica, style='List Bullet')

            # Salvar em memória
            buffer = BytesIO()
            docx_file.save(buffer)
            buffer.seek(0)

            st.success("Prova adaptada gerada com sucesso!")
            st.download_button(label="📥 Baixar Prova Adaptada (.docx)", data=buffer, file_name="prova_adaptada.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        docx.save(buffer)
        buffer.seek(0)

        st.success("Prova adaptada gerada com sucesso!")
        st.download_button("📄 Baixar Prova Adaptada (DOCX)", buffer, file_name="prova_adaptada.docx")
