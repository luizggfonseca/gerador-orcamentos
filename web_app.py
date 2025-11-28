import streamlit as st
from fpdf import FPDF
import os

# --- CLASSE PDF CUSTOMIZADA ---
class PDF(FPDF):
    def __init__(self, nome_empresa, subtitulo):
        super().__init__()
        self.nome_empresa = nome_empresa
        self.subtitulo = subtitulo

    def header(self):
        self.set_font('Arial', 'B', 14)
        # Usa o nome da empresa que veio do formulário
        self.cell(0, 10, self.nome_empresa, 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, self.subtitulo, 0, 1, 'C')
        self.line(10, 30, 200, 30)
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# --- CONFIGURAÇÃO DA PÁGINA WEB ---
st.set_page_config(page_title="Gerador de Orçamentos", layout="wide")

st.title("📄 Gerador de Orçamentos Profissional")
st.write("Preencha os dados abaixo para gerar seu PDF.")

# --- BARRA LATERAL (CONFIGURAÇÕES DA EMPRESA) ---
st.sidebar.header("🏢 Dados da Sua Empresa")
empresa_nome = st.sidebar.text_input("Nome da Empresa", "Confecções da Tia")
empresa_sub = st.sidebar.text_input("Subtítulo / Contato", "Tel: (11) 99999-9999 | Email: contato@exemplo.com")

# --- DADOS DO CLIENTE ---
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Nome do Cliente")
with col2:
    telefone = st.text_input("Telefone do Cliente")

# --- CARRINHO DE COMPRAS (SESSION STATE) ---
# Na web, precisamos "lembrar" da lista quando a página atualiza.
if 'itens' not in st.session_state:
    st.session_state.itens = []

st.divider()
st.subheader("🛒 Adicionar Produtos")

# Formulário para adicionar itens
with st.form("form_add"):
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        desc = st.text_input("Descrição do Produto")
    with c2:
        qtd = st.number_input("Qtd", min_value=1, value=1)
    with c3:
        preco = st.number_input("Preço Unit.", min_value=0.0, format="%.2f")
    
    btn_adicionar = st.form_submit_button("Adicionar Item")

    if btn_adicionar:
        if desc:
            total_item = qtd * preco
            st.session_state.itens.append({
                "descricao": desc,
                "qtd": qtd,
                "preco": preco,
                "total": total_item
            })
            st.success(f"'{desc}' adicionado!")
        else:
            st.warning("Digite a descrição do produto.")

# --- MOSTRAR ITENS ADICIONADOS ---
if st.session_state.itens:
    st.write("### Itens no Orçamento:")
    # Mostra uma tabela bonitinha na tela
    st.dataframe(st.session_state.itens)
    
    # Botão para limpar a lista se errar
    if st.button("Limpar Lista"):
        st.session_state.itens = []
        st.rerun()

# --- BOTÃO FINAL: GERAR PDF ---
st.divider()
if st.button("🖨️ Gerar PDF do Orçamento"):
    if not cliente or not st.session_state.itens:
        st.error("Preencha o nome do cliente e adicione pelo menos um item!")
    else:
        # Lógica de criação do PDF (Igual ao passo anterior, mas usando variáveis da web)
        pdf = PDF(empresa_nome, empresa_sub) # Passamos os dados da Sidebar
        pdf.add_page()
        
        # Dados do Cliente
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Cliente: {cliente}", ln=1)
        pdf.cell(0, 10, f"Telefone: {telefone}", ln=1)
        pdf.ln(10)

        # Cabeçalho Tabela
        pdf.set_fill_color(220, 220, 220)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(90, 10, "Produto", 1, 0, 'L', fill=True)
        pdf.cell(20, 10, "Qtd", 1, 0, 'C', fill=True)
        pdf.cell(40, 10, "Preço Unit.", 1, 0, 'R', fill=True)
        pdf.cell(40, 10, "Total", 1, 1, 'R', fill=True)

        # Loop nos itens da memória (Session State)
        pdf.set_font("Arial", size=10)
        total_geral_qtd = 0
        total_geral_valor = 0.0

        for item in st.session_state.itens:
            pdf.cell(90, 10, item['descricao'], 1, 0, 'L')
            pdf.cell(20, 10, str(item['qtd']), 1, 0, 'C')
            pdf.cell(40, 10, f"R$ {item['preco']:.2f}", 1, 0, 'R')
            pdf.cell(40, 10, f"R$ {item['total']:.2f}", 1, 1, 'R')
            total_geral_qtd += item['qtd']
            total_geral_valor += item['total']

        # Totais
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(110, 10, "TOTAIS:", 0, 0, 'R')
        pdf.cell(20, 10, str(total_geral_qtd), 1, 0, 'C')
        pdf.cell(60, 10, f"R$ {total_geral_valor:.2f}", 1, 1, 'R')

        # Salvar e Disponibilizar Download
        nome_arquivo = f"orcamento_{cliente.replace(' ', '_')}.pdf"
        pdf.output(nome_arquivo)
        
        st.success("PDF Gerado com Sucesso!")
        
        # Botão para baixar o arquivo
        with open(nome_arquivo, "rb") as file:
            st.download_button(
                label="Baixar PDF",
                data=file,
                file_name=nome_arquivo,
                mime="application/pdf"
            )