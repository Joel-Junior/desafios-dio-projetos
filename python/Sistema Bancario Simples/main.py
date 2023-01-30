#Exemplo simples de desafio para criação sistema bancário
#Sistema permite operações de depósito,saque e extrato.
#Limite de 3 saques por dia e valor máximo de 500 reais para cada saque

'''
*Novas regras e otimização versão 2.0
 - separar as operações bancarias existentes (saque,deposito e extrato) em funções
        -> Regra função saque : argumentos recebido apenas por nome (keyword only)
            ex: saque(saldo=30,valor=400,extrato='',limite=500.00,numero_saques=3,limite_saques=3). Sugestão retorno saldo e extrato.
       
        -> Regra função deposito: argumentos recebidos apenas por posição (positional only)
            ex.: def deposito(saldo,valor,extrato) chamada deposito(30,400,extrato).

        -> Regra função extrato : argumentos recebidos por posição (positional only e keyword only)
            ex.: argumentos posicionais:saldo e argumentos normeados:extrato : extrato(saldo=300,"extrato")
 - criar duas novas funções : cadastrar usuário(cliente) e conta corrente(vinculada ao usuário)
       -> Regra função cadastrar usuario:
        - Armazenar usuários num lista: usuario composto por nome,data de nascimento,cpf(somente numeros) e endereço(string formada de logradouro,numero - bairro - Cidade/UF)
        - 1 usuário cadastrado por cpf
       -> Regra função criar conta corrente do usuário: conta composta por: agencia,numero da conta e usuario
        - Numero da conta é sequencia baseada na ultima cadastrada no sistema
        - Numero da agencia é fixa "0001"
        - Usuario pode ter mais de uma conta, mas uma conta só pode estar associada a um usuário
  
'''
import textwrap

def montar_menu():
    menu_dic= {
        "d" : "Depositar",
        "s" : "Sacar",
        "e" : "Extrato",
        "c" : "Nova Conta",
        "lc" : "Listar Contas",
        "u" : "Novo Usuário",
        "lu" : "Listar Usuários",
        "q" : "Sair"
    }

    menu_formata = "\n".join(map(lambda key: f" [{key}]\t{menu_dic[key]}", menu_dic.keys()))

    menu = f"""\n===== MENU =====
{menu_formata}
=> """
    return input(textwrap.dedent(menu))

#argumentos recebidos apenas por posição (positional only)
def depositar(saldo,valor_deposito,extrato,/):
    saldo += valor_deposito
    print(f"Depósito realizado com sucesso!")       
    extrato += f"Depósito : R$ {valor_deposito:.2f}\n"
    return saldo,extrato    

#argumentos recebidos apenas por nome (keyword only)
def sacar(*,saldo,valor_saque,limite_saque_valor,limite_saque,numero_saques,extrato):
    
    if numero_saques >= limite_saque:
        print(f"Ops! Só podem serem feitos {limite_saque} saques por dia!")
    elif valor_saque > saldo:
        print("Você não tem saldo suficiente para essa operação!")
    elif valor_saque > limite_saque_valor:
        print(f"Ops! Limite máximo do valor por saque é de R$ {limite_saque_valor:.2f}!")
    else:                
        saldo -= valor_saque
        numero_saques += 1
        print(f"Saque realizado com sucesso!")        
        print(f"Quantidade de saques realizados hoje: {numero_saques}")
        extrato  += f"Saque : R$ {valor_saque:.2f}\n"
    return saldo,extrato,numero_saques  

def exibir_extrato(saldo,/,*,extrato):
    print("=== Extrato ===")
    print("Não foram realizadas movimentações." if not extrato else extrato )
    print(f"Salto atual: R$ {saldo:.2f}")

def filtrar_usuario(chave,valor_chave,usuarios):
    usuario_encontrado = [usuario for usuario in usuarios if usuario[chave] == valor_chave] 
    return usuario_encontrado[0] if usuario_encontrado else None 

def listar_contas(contas,usuarios):
    print(f"===============")
    for conta in contas:
        usuario = filtrar_usuario("id",conta["id_usuario"],usuarios)
        
        print(f'''Conta número: {conta["numero"]}
        Agência: {conta["agencia"]}
        Usuario: {usuario["nome"]}
        ''')
        print(f"----------------\n")
    

def listar_usuarios(usuarios):
    print(f"====================")
    for usuario in usuarios:    
        print(f'''Codigo Usuário: {usuario["id"]}
        Nome: {usuario["nome"]}
        CPF: {usuario["cpf"]}
        Data Nascimento: {usuario["data nascimento"]}
        Endereço: {usuario["endereco"]}
        ''')

        if usuario.get("conta"):
            for conta in usuario["conta"]:
                print(f"------------------")
                print(f'''Conta número: {conta["numero"]}
                Agência: {conta["agencia"]}
                ''')
        print(f"===============\n")

def cadastrar_usuario(usuarios):
    cpf = input("Informe o cpf do usuário (somente numeros)")
    usuario = filtrar_usuario("cpf",cpf,usuarios)

    if usuario:
        print("Já existe um usuário cadastrado com este CPF!")
        return
    
    nome = input("Informe o nome do usuário:")
    data_nascimento = input("Informe a data de nascimento:")
    endereco = input("Informe o endereço (logradouro,numero - bairro - Cidade/UF):")
    id_usuario = len(usuarios) + 1

    usuarios.append({"id" : id_usuario ,"nome": nome,"data nascimento": data_nascimento,"endereco":endereco,"cpf":cpf})

    print("Usuário cadastrado com sucesso!")
    return usuarios

def cadastrar_conta(agencia,contas,usuarios):
    cpf = input("Informe o CPF usuário cadastrado:")
    usuario = filtrar_usuario("cpf",cpf,usuarios)

    if usuario:
        numero_conta = len(contas) + 1
        conta = { "agencia" : agencia, "numero" : numero_conta ,"id_usuario": usuario["id"] }
        contas.append(conta)

        usuario.setdefault("conta", [])
        
        usuario["conta"].append(conta)

        for user in usuarios:
            if user["id"] == usuario["id"]:
                user = usuario
        return contas,usuarios
    
    print("Usuário não existe cadastrado com esse CPF!")
    return contas,usuarios

def main():
    
    LIMITE_SAQUE = 3
    LIMITE_SAQUE_VALOR = 500.0
    AGENCIA = "0001"
    saldo = 0.0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = montar_menu()
        
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
                        saldo,extrato = depositar(saldo,valor_deposito,extrato)
                        break
            case "s":
                print("==== Saque ====")
                while True:
                    valor_saque = float(input("Digite o valor do seu saque:"))
                    if valor_saque <= 0:
                        print("Valor invalido!")                
                    else:
                        saldo,extrato,numero_saques = sacar(saldo = saldo,valor_saque= valor_saque,limite_saque_valor = LIMITE_SAQUE_VALOR,
                                              limite_saque=LIMITE_SAQUE,numero_saques=numero_saques,extrato=extrato)
                        break
            case "e":  
                exibir_extrato(saldo,extrato = extrato)
            case "u":  
                print("==== Cadastro de Usuário ====")
                usuarios = cadastrar_usuario(usuarios)                
            case "c":  
                print("==== Cadastro de Conta ====")
                contas,usuarios = cadastrar_conta(AGENCIA ,contas,usuarios)
            case "lc":
                print("==== Listar Contas ====")
                listar_contas(contas,usuarios)
            case "lu":
                print("==== Listar Usuários ====")
                listar_usuarios(usuarios)
            case "q":
                break            
            case _:
                print("Opção inválida")
    print("Finalizado. Obrigado por ser nosso cliente.")

main()
