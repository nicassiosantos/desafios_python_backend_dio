saldo = 0
limite = 500
extrato = ""
numero_saques = 0
numero_conta = 1
LIMITE_SAQUES = 3
NUMERO_AGENCIA = 1
clientes = []
contas = []

#Menu para escolha de opções 
def menu(): 
    menu = """
=======MENU SISTEMA BANCÁRIO=======

[1] Cadastrar cliente 
[2] Cadastrar conta bancaria
[3] Depositar
[4] Sacar
[5] Extrato
[6] Listar clientes 
[7] Listar contas
[8] Sair

=> """

    opcao = input(menu) 
    return opcao

#Verifica se o cpf já é existente e se foi digitado incorretamente
def erro_cpf(cpf):
    global clientes 

    try: 
        int(cpf) 
        if existe_cpf(cpf):
            print("Já existe um cliente cadastrado com este cpf, por favor verifique e tente novamente")
            return True 
        return False

    except: 
        print("CPF inválido, digite apenas os números do CPF")
        return True

#Verifica se foi digitado um número inteiro como entrada
def erro_numero(numero):
    try: 
        int(numero) 
        return False
    except: 
        print("Número inválido, digite um número inteiro válido")
        return True

#Função responsável pelo cadastro de clientes
def cadastro_cliente(): 
    global clientes 

    Nome = input("Digite o Nome do cliente: ")
    Data = input("Digite a data de nascimento do cliente no formato(XX/XX/XXXX): ")
    cpf = input("Digite o apenas o número do CPF: ")
    if erro_cpf(cpf): 
        return "CPF incorreto"
    Logradouro = input("Digite o logradouro do endereço(Não contém Número, bairro, cidade e estado): ")
    Numero = input("Digite o número: ")
    if erro_numero(Numero): 
        return "Número incorreto"
    Bairro = input("Digite o bairro: ")
    Cidade = input("Digite a cidade: ")
    Estado = input("Digite a sigla do estado: ")
    Endereco = f"{Logradouro},{Numero} - {Bairro} - {Cidade}/{Estado}" 

    cliente = { "nome": Nome, "data":Data, "cpf":cpf, "endereço":Endereco} 

    clientes.append(cliente)

#Função que verfica se existe um cliente com determinado cpf
def existe_cpf(cpf): 
    global clientes 

    if clientes: 
            for cliente in clientes: 
                if cliente['cpf'] == cpf: 
                    return True  

    return False

#Função responsável pelo cadastro de contas bancárias 
def cadastro_conta(): 
    global numero_conta 
    global NUMERO_AGENCIA 
    global contas

    cpf = input("Digite o número de CPF do cliente que quer criar uma conta: ") 

    if existe_cpf(cpf): 
        conta = { "agencia":f"000{NUMERO_AGENCIA}", "conta":numero_conta, "cliente":cpf }
        contas.append(conta)
        numero_conta += 1;
    else:
        print("Não existe nenhum cliente cadastrado com este CPF")

#Função responsável por realizar um depósito
def deposito(saldo, valor, extrato, /): 
    saldo += valor
    extrato = f"\nDepósito: R${valornum:.2f}" + extrato
    print("Deposito realizado com sucesso") 
    return saldo, extrato

#Função que lista os clientes
def listar_clientes(clientes): 

    if clientes: 
        print("===========CLIENTES===========")
        for cliente in clientes: 
            print(f"Nome:{cliente['nome']} data de Nascimento:{cliente['data']} CPF:{cliente['cpf']} Endereço:{cliente['endereço']}")
    else: 
        print("Não existe nenhum cliente cadastrado")

#Função que lista as contas
def listar_contas(contas): 

    if contas: 
        print("===========CONTAS===========")
        for conta in contas: 
            print(f"Agência:{conta['agencia']}  Conta:{conta['conta']} Cliente:{conta['cliente']}")
    else: 
        print("Não existe nenhuma conta cadastrada")

#Função responsável por realizar o saque na conta
def saque(*,saldo, valor, extrato, limite, numero_saques,limite_saques):
    if valor > limite: 
        print("Valor inválido, valor limite para um saque é de R$ 500.00")
    elif numero_saques == limite_saques: 
        print("Número diário de saques atingido") 
    elif valor > saldo: 
        print("Saque inválido, limite de conta insuficiente para esta operação") 
    elif valor < 0: 
        print("Valor inválido, números negativos não são permitidos")
    else: 
        saldo -= valor
        numero_saques += 1
        extrato = f"\nSaque: R${valornum:.2f}" + extrato 
        print("Saque realizado com sucesso")
        return saldo, extrato, numero_saques
    
    return saldo, extrato, numero_saques

#Função responsável por exibir o extrato
def func_extrato(saldo, /,*,extrato): 
    if extrato == "":
        print("\nNão foram realizadas movimentações")
    else: 
        string_saldo = f"\nSaldo total: R${saldo:.2f}"
        extrato = extrato + string_saldo
        print("===========EXTRATO===========")
        print(extrato)  
        extrato = extrato.replace(string_saldo, "")

while True: 

    opcao = menu(); 

    if opcao == "1": 
        cadastro_cliente();
    elif opcao == "2":
        cadastro_conta();
    elif opcao == "3":
        valor = input("\nDigite o valor que deseja depositar: ")
        try: 
            valornum = float(valor) 
            if valornum < 0: 
                print("Valor inválido, números negativos não são permitidos") 
            else: 
                saldo, extrato = deposito(saldo, valornum, extrato)
        except: 
            print("Número invalido, por favor digite um número no formato 00.00") 

    elif opcao == "4": 
        
        valor = input("\nDigite o valor que deseja sacar: ") 
        
        try: 
            valornum = float(valor) 
            saldo, extrato, numero_saques = saque(saldo=saldo, valor=valornum, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES,)
        except: 
            print("Número inválido, por favor digite um número no formato 00.00") 

    elif opcao == "5": 

        func_extrato(saldo,extrato=extrato)

    elif opcao == "6": 
        listar_clientes(clientes)

    elif opcao == "7": 
        listar_contas(contas)

    elif opcao == "8": 
        break
    else: 
        print("Opção inválida, tente novamente")