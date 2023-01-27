#Exemplo simples de desafio para criação sistema bancário
#Sistema permite operações de depósito,saque e extrato.
#Limite de 3 saques por dia e valor máximo de 500 reais para cada saque

LIMITE_SAQUE = 3
LIMITE_SAQUE_VALOR = 500.0

saldo = 0.0
extrato = ""
numero_saques = 0

def montar_menu() -> str:
    menu_dic= {
        "d" : "Depositar",
        "s" : "Sacar",
        "e" : "Extrato"
    }

    menu_formata = "\n".join(map(lambda key: f" [{key}] {menu_dic[key]}", menu_dic.keys()))

    menu = f"""
    ===== MENU =====

{menu_formata}
 [q] Sair

    => """
    return menu

while True:
    opcao = input(montar_menu())
    
    #estrutura semelhante ao switch utilizando match term:
    # implementado a partir da versão 3.10 
    match opcao:
        case "d":
            print("==== Depósito ====")
            while True:
                valor_deposito = float(input("Digite o valor do seu depósito:"))
                if valor_deposito <= 0:
                    print("Valor do depósito invalido")
                else:
                    saldo += valor_deposito
                    extrato += f"Depósito : R$ {valor_deposito:.2f}\n"
                    break
        case "s":
            print("==== Saque ====")
            while True:
                valor_saque = float(input("Digite o valor do seu saque:"))
                if valor_saque <= 0:
                    print("Valor invalido!")
                elif valor_saque > saldo:
                    print("Você não tem saldo suficiente para essa operação!")
                elif valor_saque > LIMITE_SAQUE_VALOR:
                    print(f"Ops! Limite máximo do valor por saque é de R$ {LIMITE_SAQUE_VALOR:.2f}!")
                elif numero_saques >= LIMITE_SAQUE:
                    print(f"Ops! Só podem serem feitos {LIMITE_SAQUE} saques por dia!")
                    break
                else:
                    saldo -= valor_saque
                    numero_saques+=1
                    print(f"Quantidade de saques realizados hoje: {numero_saques}")
                    extrato += f"Saque : R$ {valor_saque:.2f}\n"
                    break
        case "e":  
            print("=== Extrato ===")
            print("Não foram realizadas movimentações." if not extrato else extrato )
            print(f"Salto atual: R$ {saldo:.2f}") 
        case "q":
            break            
        case _:
            print("Opção inválida")
print("Finalizado. Obrigado por ser nosso cliente.")
