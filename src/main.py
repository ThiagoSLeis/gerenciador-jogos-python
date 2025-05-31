import sys
import os 

try:
    import pandas as pd
except ImportError:
    print('Erro: A biblioteca pandas não foi encontrada!')
    print('Execute no terminal: pip install -r requirements.txt')
    sys.exit(1)
try:
    import openpyxl
except ImportError:
    print('Erro: openpyxl não encotrado!')
    print('Execute no terminal: pip install -r requirements.txt')
    sys.exit(1)

from func_games import Funcoes_jogos

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\n  Pressione Enter para continuar...")

def mostrar_menu():
    print("""
==================================================
           GERENCIADOR DE JOGOS          
==================================================
1.  Listar todos os jogos
2.  Adicionar novo jogo
3.  Alterar jogo existente
4.  Remover jogo
5.  Buscar jogo por código
6.  Sair do programa
--------------------------------------------------
""")

def obter_dados_jogos():
    print("\n--- ADICIONAR NOVO JOGO ---")
    
    codigo = input("Código do jogo: ").strip()
    if not codigo:
        return None, "Código não pode estar vazio!"
    
    nome = input("Nome do Jogo: ").strip()
    if not nome:
        return None, "Nome não pode estar vazio!"
    
    estudio = input("Estúdio: ").strip()
    if not estudio:
        return None, "Estúdio não pode estar vazia!"
    
    try:
        ano = int(input("Ano de publicação: "))
        if ano < 1900 or ano > 2030:
            return None, "Ano deve estar entre 1900 e 2030!"
    except ValueError:
        return None, "Ano deve ser um número válido!"
    
    try:
        valor = float(input("Valor pago (R$): "))
        if valor < 0:
            return None, "Valor não pode ser negativo!"
    except ValueError:
        return None, "Valor deve ser um número válido!"
    
    return (codigo, nome, estudio, ano, valor), None

def main():
    jogos = Funcoes_jogos()
    
    while True:
        try:
            limpar_tela()
            mostrar_menu()
            
            opcao = input(" Escolha uma opção (1-6): ").strip()
            
            if opcao == '1':
                print("\n---  LISTA DE JOGOS ---")
                resultado = jogos.listar_jogos()
                print(resultado)
                pausar()
            
            elif opcao == '2':
                dados, erro = obter_dados_jogos()
                if erro:
                    print(erro)
                else:
                    codigo, nome, estudio, ano, valor = dados
                    resultado = jogos.adicionar_jogo(codigo, nome, estudio, ano, valor)
                    print(f"\n{resultado}")
                pausar()
            
            elif opcao == '3':
                print("\n--- ALTERAR JOGO ---")
                
                codigos = jogos.get_codigos_existentes()
                if not codigos:
                    print(" Nenhum Jogo cadastrado!")
                    pausar()
                    continue
                
                print(f"📋 Códigos disponíveis: {', '.join(codigos)}")
                
                codigo = input("Código do jogo para alterar: ").strip()
                if not codigo:
                    print("Código não pode estar vazio!")
                    pausar()
                    continue
                
                info_jogo = jogos.buscar_jogo(codigo)
                print(f"\n{info_jogo}")
                
                if "não encontrado" in info_jogo:
                    pausar()
                    continue
                
                print("\n Campos disponíveis: Nome, Estúdio, Ano, ValorPago")
                campo = input(" Campo para alterar: ").strip()
                
                if campo not in ['Nome', 'Estúdio', 'Ano', 'ValorPago']:
                    print(" Campo inválido!")
                    pausar()
                    continue
                
                novo_valor = input(f" Novo valor para {campo}: ").strip()
                if not novo_valor:
                    print(" Novo valor não pode estar vazio!")
                    pausar()
                    continue
                
                resultado = jogos.alterar_jogo(codigo, campo, novo_valor)
                print(f"\n{resultado}")
                pausar()

            elif opcao == '4':
                print("\n--- REMOVER JOGO ---")
                
                codigos = jogos.get_codigos_existentes()
                if not codigos:
                    print("Nenhum jogo cadastrado!")
                    pausar()
                    continue
                
                print(f"Códigos disponíveis: {', '.join(codigos)}")
                
                codigo = input("📝 Código do jogo para remover: ").strip()
                if not codigo:
                    print(" Código não pode estar vazio!")
                    pausar()
                    continue
                
                info_jogo = jogos.buscar_jogo(codigo)
                print(f"\n{info_jogo}")
                
                if "não encontrado" in info_jogo:
                    pausar()
                    continue
                
                confirmacao = input(f"\n  Tem certeza que deseja remover este jogo? (s/N): ").strip().lower()
                
                if confirmacao == 's':
                    resultado = jogos.remover_jogo(codigo)
                    print(f"\n{resultado}")
                else:
                    print(" Operação cancelada!")
                pausar()

            elif opcao == '5':
                print("\n---  BUSCAR JOGO ---")
                
                codigos = jogos.get_codigos_existentes()
                if not codigos:
                    print(" Nenhum jogo cadastrado!")
                    pausar()
                    continue
                
                print(f"📋 Códigos disponíveis: {', '.join(codigos)}")
                
                codigo = input("📝 Código do jogo: ").strip()
                if codigo:
                    resultado = jogos.buscar_jogo(codigo)
                    print(f"\n{resultado}")
                else:
                    print(" Código não pode estar vazio!")
                pausar()
            
            elif opcao == '6':
                print("\n Obrigado por usar o Gerenciador de Jogos!")
                print(" Seus dados foram salvos em 'jogos.xlsx'")
                break
            
            else:
                print("Opção inválida! Escolha entre 1 e 6.")
                pausar()

        except KeyboardInterrupt:
            print("\n\n Programa interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"\n Erro inesperado: {e}")
            print("🔧 Se o erro persistir, verifique o arquivo 'jogos.xlsx'")
            pausar()

if __name__ == "__main__":
    main()