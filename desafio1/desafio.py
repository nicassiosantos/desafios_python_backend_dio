menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """



saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3 


while True: 

    opcao = input(menu) 

    if opcao == "d":

        valor = input("\nDigite o valor que deseja depositar: ")

        try: 
            valornum = float(valor) 
            if valornum < 0: 
                print("Valor inválido, números negativos não são permitidos")
            else: 
                saldo += valornum
                extrato = f"\nDepósito: R${valornum:.2f}" + extrato
                print("Deposito realizado com sucesso")
        except: 
            print("Número invalido, por favor digite um número no formato 00.00") 

    elif opcao == "s": 
        
        valor = input("\nDigite o valor que deseja sacar: ") 
        
        try: 
            valornum = float(valor) 
            if valornum > limite: 
                print("Valor inválido, valor limite para um saque é de R$ 500.00")
            elif numero_saques == LIMITE_SAQUES: 
                print("Número diário de saques atingido") 
            elif valornum > saldo: 
                print("Saque inválido, limite de conta insuficiente para esta operação") 
            elif valornum < 0: 
                print("Valor inválido, números negativos não são permitidos")
            else: 
                saldo -= valornum
                numero_saques += 1
                extrato = f"\nSaque: R${valornum:.2f}" + extrato
                print("Saque realizado com sucesso")
        except: 
            print("Número inválido, por favor digite um número no formato 00.00") 

    elif opcao == "e": 

        if extrato == "":
            print("\nNão foram realizadas movimentações")
        else: 
            string_saldo = f"\nSaldo total: R${saldo:.2f}"
            extrato = extrato + string_saldo
            print(extrato)  
            extrato = extrato.replace(string_saldo, "")

    elif opcao == "q": 
        break 

    else: 
        print("Opção inválida, tente novamente")