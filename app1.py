from fpdf import FPDF

# --- CONFIGURAÇÃO DO DOCUMENTO (CLASSE) ---
class PDF(FPDF):
    def header(self):
        # Seleciona a fonte Arial, Negrito, tamanho 12
        self.set_font('Arial', 'B', 12)
        # Cria uma célula de largura total (0), altura 10, texto, sem borda (0), quebra linha (1), centralizado ('C')
        self.cell(0, 10, 'ORÇAMENTO DE PRESTAÇÃO DE SERVIÇOS', 0, 1, 'C')
        # Desenha uma linha horizontal para separar o cabeçalho
        self.line(10, 20, 200, 20) 
        # Dá um espaço de 20mm para baixo
        self.ln(20)

    def footer(self):
        # Posiciona o cursor a 1.5cm do final da página
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Coloca o número da página
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# --- 1. DADOS DE ENTRADA ---
print("\n--- GERADOR DE ORÇAMENTO 2.0 ---")
cliente = input("Nome do Cliente: ")
projeto = input("Descrição do Projeto: ")
horas_estimadas = input("Horas estimadas (apenas números): ")
valor_hora = input("Valor da sua hora (apenas números): ")

# --- 2. CÁLCULO AUTOMÁTICO ---
# Convertendo o texto (string) para números (int ou float) para poder calcular
try:
    total = float(horas_estimadas) * float(valor_hora)
except ValueError:
    print("Erro: Você digitou letras no lugar de números. Tente novamente.")
    exit()

# --- 3. GERAÇÃO DO PDF ---
pdf = PDF() # Usamos a nossa classe personalizada
pdf.add_page()
pdf.set_font("Arial", size=12)

# Informações do Projeto
pdf.text(10, 40, f"Cliente: {cliente}")
pdf.text(10, 48, f"Projeto: {projeto}")

# Adicionando um espaço visual
pdf.ln(30)

# Tabela Simples (Cabeçalho da Tabela)
pdf.set_fill_color(200, 220, 255) # Cor de fundo (Azul claro)
pdf.set_font("Arial", 'B', 12)
pdf.cell(80, 10, "Descrição", 1, 0, 'C', fill=True)
pdf.cell(30, 10, "Horas", 1, 0, 'C', fill=True)
pdf.cell(40, 10, "Valor/Hora", 1, 0, 'C', fill=True)
pdf.cell(40, 10, "Total", 1, 1, 'C', fill=True)

# Tabela (Dados)
pdf.set_font("Arial", size=12)
pdf.cell(80, 10, "Desenvolvimento", 1, 0)
pdf.cell(30, 10, horas_estimadas, 1, 0, 'C')
pdf.cell(40, 10, f"R$ {valor_hora}", 1, 0, 'C')
pdf.cell(40, 10, f"R$ {total:.2f}", 1, 1, 'C')

# Valor Final destacado
pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, f"VALOR TOTAL DO ORÇAMENTO: R$ {total:.2f}", 0, 1, 'R')

# --- 4. SALVAR ---
pdf.output(f"orcamento_{cliente}.pdf")
print("PDF gerado com sucesso!")