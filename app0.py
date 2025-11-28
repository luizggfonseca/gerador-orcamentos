from fpdf import FPDF

# 1. Coletar dados do usuário
print("--- GERADOR DE ORÇAMENTO ---")
cliente = input("Nome do cliente: ")
descricao = input("Descrição do serviço: ")
valor_total = input("Valor total do serviço (apenas números): ")

# 2. Configurar o PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# 3. Escrever no PDF
# Título
pdf.set_font("Arial", style="B", size=16)
pdf.cell(200, 10, txt="ORÇAMENTO DE SERVIÇO", ln=1, align="C")

# Pula uma linha
pdf.cell(200, 10, txt="", ln=1) 

# Corpo do texto
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=1)
pdf.cell(200, 10, txt=f"Serviço: {descricao}", ln=1)
pdf.cell(200, 10, txt=f"Valor Total: R$ {valor_total}", ln=1)

# Rodapé simples
pdf.cell(200, 10, txt="", ln=1)
pdf.cell(200, 10, txt="Gerado automaticamente pelo sistema.", ln=1, align="C")

# 4. Salvar o arquivo
nome_arquivo = f"orcamento_{cliente}.pdf"
pdf.output(nome_arquivo)

print(f"Sucesso! O arquivo '{nome_arquivo}' foi criado na sua pasta.")