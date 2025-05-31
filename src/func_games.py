import pandas as pd

class Funcoes_jogos:
    def __init__(self, arquivo='jogos.xlsx'):
        self.arquivo = arquivo
        self.carregar_dados()

    def carregar_dados(self):
        try:
            self.df = pd.read_excel(self.arquivo)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['Código', 'Nome', 'Estúdio', 'Ano', 'ValorPago'])
            self.salvar()
    def listar_jogos(self):
        if self.df.empty:  # .empty retorna bool
            return "Nenhum jogo foi cadastrado no sistema!"
        
        resultado = "\n" + "="*80 + "\n"
        resultado += f"{'CÓDIGO':<8} {'NOME':<25} {'ESTÚDIO':<15} {'ANO':<6} {'VALOR':<10}\n"
        resultado += "="*80 + "\n"
        
        for _, jogo in self.df.iterrows():
            resultado += f"{jogo['Código']:<8} {jogo['Nome']:<25} {jogo['Estúdio']:<15} {jogo['Ano']:<6} R$ {jogo['ValorPago']:>6.2f}\n"
        
        resultado += "="*80 + "\n"

        resultado += (
    f"\n Estatísticas:\n"
    f"• Total de Jogos: {len(self.df)}\n"
    f"• Valor total investido: R$ {self.df['ValorPago'].sum():.2f}\n"
    f"• Valor médio por jogo: R$ {self.df['ValorPago'].mean():.2f}\n"
    f"• Ano médio de publicação: {self.df['Ano'].mean():.0f}\n"
    f"• Jogo mais caro: R$ {self.df['ValorPago'].max():.2f}\n"
    f"• Jogo mais barato: R$ {self.df['ValorPago'].min():.2f}\n"
)
        
        return resultado
    
    def adicionar_jogo(self, codigo, nome, estudio, ano, valor):
        if codigo in self.df['Código'].values:
            return "Erro: Código já existe!"
        
        novo_jogo = pd.DataFrame([{
            'Código': codigo,
            'Nome': nome,
            'Estúdio': estudio,
            'Ano': ano,
            'ValorPago': valor
        }])
        self.df = pd.concat([self.df, novo_jogo], ignore_index=True)
        self.salvar()
        return "Jogo adicionado com sucesso!"
    
    def alterar_jogo(self, codigo, campo, novo_valor):
        if codigo not in self.df['Código'].values:
            return "Erro: Código não encontrado!"
        
        if campo not in ['Nome', 'Estúdio', 'Ano', 'ValorPago']:
            return "Erro: Campo inválido! Use: Nome, Estúdio, Ano, ValorPago"
        
        try:
            if campo == 'Ano':
                novo_valor = int(novo_valor)
            elif campo == 'ValorPago':
                novo_valor = float(novo_valor)
            
            self.df.loc[self.df['Código'] == codigo, campo] = novo_valor
            self.salvar()
            return "Jogo alterado com sucesso!"
            
        except ValueError:
            return "Erro: Valor inválido para o campo especificado!"
        
    def remover_jogo(self, codigo):
        if codigo not in self.df['Código'].values:
            return "Erro: Código não encontrado!"
        
        self.df = self.df[self.df['Código'] != codigo]
        self.salvar()
        return "Jogo removido com sucesso!"
    
    def buscar_jogo(self, codigo):
        if codigo in self.df['Código'].values:
            jogo = self.df[self.df['Código'] == codigo].iloc[0]
            return f"Jogo encontrado: {jogo['Nome']} - {jogo['Estúdio']} ({jogo['Ano']}) - R$ {jogo['ValorPago']:.2f}"
        return "Jogo não encontrado!"
    
    def salvar(self):
        self.df.to_excel(self.arquivo, index=False)
        
    def get_codigos_existentes(self):
        return self.df['Código'].tolist()
    


        