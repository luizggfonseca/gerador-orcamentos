from fpdf import FPDF

# --- CONFIGURAÇÃO DO PDF (CLASSE) ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'ORÇAMENTO', 0, 1, 'C')
        self.line(10, 20, 200, 20)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# --- 1. DADOS DO CLIENTE ---
print("\n--- NOVO PEDIDO ---")
cliente = input("Cliente: ")
telefone = input("Telefone: ")

# --- 2. LOOP DE PRODUTOS (O "CARRINHO") ---
itens = [] # Criamos uma lista vazia
adicionando = True

while adicionando:
    print(f"\n--- Adicionando item {len(itens) + 1} ---")
    descricao = input("Nome do produto (ex: Camiseta M): ")
    
    # Validação simples para garantir que quantidade é número
    while True:
        try:
            qtd = int(input("Quantidade: "))
            preco_unit = float(input("Preço unitário (apenas números e .)): "))
            break # Se der certo, sai desse laço de validação
        except ValueError:
            print("Erro: Digite apenas números para quantidade e preço (use ponto para centavos).")

    total_item = qtd * preco_unit
    
    # Salvamos esse item na nossa lista
    itens.append({
        "descricao": descricao,
        "qtd": qtd,
        "preco": preco_unit,
        "total": total_item
    })

    continuar = input("Adicionar mais um item? (s/n): ").lower()
    if continuar == 'n':
        adicionando = False

# --- 3. GERAÇÃO DO PDF ---
pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Cabeçalho do Cliente
pdf.cell(0, 10, f"Cliente: {cliente}", ln=1)
pdf.cell(0, 10, f"Telefone: {telefone}", ln=1)
pdf.ln(10)

# Cabeçalho da Tabela
pdf.set_fill_color(220, 220, 220) # Cinza claro
pdf.set_font("Arial", 'B', 10)
pdf.cell(90, 10, "Produto", 1, 0, 'L', fill=True)
pdf.cell(20, 10, "Quant.", 1, 0, 'C', fill=True)
pdf.cell(40, 10, "Preço unit.", 1, 0, 'R', fill=True)
pdf.cell(40, 10, "Total", 1, 1, 'R', fill=True)

# Preenchendo a Tabela (O Loop de Escrita)
pdf.set_font("Arial", size=10)
total_geral_qtd = 0
total_geral_valor = 0.0

for item in itens:
    pdf.cell(90, 10, item['descricao'], 1, 0, 'L')
    pdf.cell(20, 10, str(item['qtd']), 1, 0, 'C')
    pdf.cell(40, 10, f"R$ {item['preco']:.2f}", 1, 0, 'R')
    pdf.cell(40, 10, f"R$ {item['total']:.2f}", 1, 1, 'R')
    
    # Somando para o final
    total_geral_qtd += item['qtd']
    total_geral_valor += item['total']

# --- 4. TOTAIS FINAIS ---
pdf.ln(5)
pdf.set_font("Arial", 'B', 12)
pdf.cell(110, 10, "TOTAIS:", 0, 0, 'R')
pdf.cell(20, 10, str(total_geral_qtd), 1, 0, 'C') # Total de peças
pdf.cell(60, 10, f"R$ {total_geral_valor:.2f}", 1, 1, 'R') # Valor final

# Salvar
nome_arquivo = f"pedido_{cliente.replace(' ', '_')}.pdf"
pdf.output(nome_arquivo)
print(f"\nSucesso! PDF gerado: {nome_arquivo}")