from abc import ABC, abstractmethod, abstractclassmethod
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent

numero_conta = 1
LIMITE_SAQUES = 3
NUMERO_AGENCIA = 1
clientes = []


# Classe responsavel por iterar as contas
class ContaIterador:
    def __init__(self, contas):
        self._contas = contas
        self._contador = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self._contas[self._contador]
            return conta
        except IndexError:
            raise StopIteration
        finally:
            self._contador += 1


# Classe abstrata para servir como interface para as classes de Deposito e Saque
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta, **kw):
        pass


# Classe responsável por representar uma operação de Deposito em uma conta
class Deposito(Transacao):
    def __init__(self, valor, **kw):
        self._valor = valor

    # Função responsavel por obter o atributo valor do deposito
    @property
    def valor(self):
        return self._valor

    # Função resposável por realizar o deposito em uma conta
    def registrar(self, conta, **kw):
        Depositou = conta.depositar(valor=self.valor)
        if Depositou:
            conta.historico.adicionar_transacao(self)
            print("Deposito realizado com sucesso")
        else:
            print("Deposito Falhou")


# Classe responsável por representar uma operação de Saque de uma conta
class Saque(Transacao):
    def __init__(self, valor, **kw):
        self._valor = valor

    # Função responsavel por obter o atributo valor do saque
    @property
    def valor(self):
        return self._valor

    # Função resposável por realizar o saque em uma conta
    def registrar(self, conta, **kw):
        try:
            Sacou = conta.sacar(valor=self.valor)
            if Sacou:
                conta.historico.adicionar_transacao(self)
                print("Saque realizado com sucesso")
        except Exception as e:
            print("Exceção:" + e)
            print("Número inválido, por favor digite um número no formato 00.00")


# Classe responsável por manter os historico das transações feitas por uma conta
class Historico:

    def __init__(self, transacoes=[]):
        self._transacoes = transacoes

    # Função responsável por adicionar uma transação ao historico
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    # Função responsável por retornar a lista de transações de uma conta
    @property
    def transacoes(self):
        return self._transacoes

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self.transacoes:
            if not tipo_transacao:
                yield transacao
            elif tipo_transacao.lower() == transacao["tipo"].lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date
        transacoes = []
        for transacao in self.transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


# Classe conta onde um cliente pode realizar movimentações
class Conta:
    def __init__(self, numero, agencia, cliente, **kw):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    # Função responsavel por retornar o saldo atual de uma conta
    @property
    def saldo(self):
        return self._saldo

    # Função responsavel por retornar o numero atual de uma conta
    @property
    def numero(self):
        return self._numero

    # Função responsavel por retornar a agencia atual de uma conta
    @property
    def agencia(self):
        return self._agencia

    # Função responsavel por retornar o cliente responsavel por uma conta
    @property
    def cliente(self):
        return self._cliente

    # Função responsavel por retornar o historico atual de uma conta
    @property
    def historico(self):
        return self._historico

    # Função responsável por criar uma nova conta
    @classmethod
    def nova_conta(self, cliente, numero, **kw):
        global NUMERO_AGENCIA
        conta = Conta(numero=numero, agencia=NUMERO_AGENCIA, cliente=cliente)
        return conta

    # Função responsável por realizar o saque
    def sacar(self, valor, **kw):

        if valor > self._saldo:
            print("Saque inválido, limite de conta insuficiente para esta operação")
        elif valor < 0:
            print("Valor inválido, números negativos não são permitidos")
        else:
            self._saldo -= valor
            return True

        return False

    # Função responsável por realizar o deposito
    def depositar(self, valor, **kw):
        try:
            self._saldo = self._saldo + valor
            return True
        except:
            return False


# Classe conta corrente onde são armazenadas alguma informações extras da conta
class Conta_corrente(Conta):
    def __init__(self, numero, agencia, cliente, limite, limite_saques, **kw):
        super().__init__(numero=numero, agencia=agencia, cliente=cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    # Função de saque da conta corrente
    def sacar(self, valor, **kw):
        saques = 0
        for transacao in self.historico.transacoes:
            if transacao["tipo"] == Saque.__name__:
                saques += 1

        if saques >= self._limite_saques:
            print("Número diário de saques atingido")
        elif valor > self._limite:
            print(f"Valor inválido, valor limite para um saque é de R${self._limite}")
        else:
            return super().sacar(valor=valor)

        return False

    def __repr__(self):
        return f"""<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"""

    # Função responsável por criar uma nova conta corrente
    @classmethod
    def nova_conta(self, numero, agencia, cliente, limite, limite_saques, **kw):
        conta = Conta_corrente(
            numero=numero, agencia=agencia, cliente=cliente, limite=limite, limite_saques=limite_saques
        )
        return conta


# Classe cliente onde é armazenado suas contas e seu endereço
class Cliente:
    def __init__(self, endereco, contas=[], **kw):
        self._endereco = endereco
        self._contas = contas

    # Função responsavel por realizar uma transação em uma conta especifica de um cliente
    def realizar_transacao(self, conta, transacao, **kw):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("Numero diario Limite de transações por dia atingido!!!")
            return
        transacao.registrar(conta)

    # Função responsavel por adicionar uma nova conta no perfil do cliente
    def adicionar_conta(self, conta, **kw):
        self._contas.append(conta)

    # Função responsavel por  obter o atributo endereço de cliente
    @property
    def endereco(self):
        return self._endereco

    # Função responsavel por  obter o atributo das contas de cliente
    @property
    def contas(self):
        return self._contas


# Classe pessoa fisica que filha de cliente onde guarda informações de maior segurança de um cliente
class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nasc, **kw):
        super().__init__(endereco=endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nasc = data_nasc

    # Função responsavel por  obter o atributo do cpf de pessoa fisica
    @property
    def cpf(self):
        return self._cpf

    # Função responsavel por  obter o atributo do cpf de pessoa fisica
    @property
    def nome(self):
        return self._nome

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.cpf}')"

    # Função responsavel por  obter o atributo do cpf de pessoa fisica
    @property
    def data_nasc(self):
        return self._data_nasc


# Menu para escolha de opções
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


# Verifica se o cpf já é existente e se foi digitado incorretamente
def erro_cpf(cpf, clientes):
    try:
        int(cpf)
        if existe_cpf(cpf, clientes):
            print("Já existe um cliente cadastrado com este cpf, por favor verifique e tente novamente")
            return True
        return False

    except:
        print("CPF inválido, digite apenas os números do CPF")
        return True


# Verifica se foi digitado um número inteiro como entrada
def erro_numero(numero):
    try:
        int(numero)
        return False
    except:
        print("Número inválido, digite um número inteiro válido")
        return True


# Função que verfica se existe um cliente com determinado cpf
def existe_cpf(cpf, clientes):
    if clientes:
        for cliente in clientes:
            if cliente.cpf == cpf:
                return cliente
    return False


# Função que verifica se existe uma conta associada ao número passado
def existe_conta(numero_conta, cliente):

    for conta in cliente.contas:
        if str(conta.numero) == numero_conta:
            return conta

    return False


# Função que lista os clientes
def listar_clientes(clientes):

    if clientes:
        print("===========CLIENTES===========")
        for cliente in clientes:
            print(
                f"Nome:{cliente.nome} data de Nascimento:{cliente.data_nasc} CPF:{cliente.cpf} Endereço:{cliente.endereco}"
            )
    else:
        print("Não existe nenhum cliente cadastrado")


# Função que lista as contas
def listar_contas(clientes):
    existe_conta = False
    if clientes:
        for cliente in clientes:
            for conta in ContaIterador(cliente.contas):
                if conta:
                    if not (existe_conta):
                        print("===========CONTAS===========")
                        existe_conta = True
                    print(f"Agência:{conta.agencia}  Número Conta:{conta.numero} Cliente:{conta.cliente.nome}")
    if not (existe_conta):
        print("Não existe nenhuma conta cadastrada")


# Função responsável por exibir o extrato no terminal
def exibir_extrato(conta):
    historico = conta.historico
    transacoes = historico.transacoes
    if transacoes:
        string_extrato = f"\nSaldo total: R${conta.saldo:.2f}"
        for transacao in historico.gerar_relatorio():
            string_extrato = f"\n{transacao['tipo']}: R${transacao['valor']:.2f}" + string_extrato
        print("===========EXTRATO===========")
        print(string_extrato)
    else:
        print("Não existem transações atreladas a essa conta")


# Função responsavel por exibir o tipo de transação feita e a hora em que foi realizada
def log_transacao(func):

    def printar_data(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora_atual = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        with open(ROOT_PATH / "log.txt", "a", encoding="utf-8") as arquivo:
            arquivo.writelines(
                f"[{data_hora_atual}] Função '{func.__name__}' executada com {args} e {kwargs}. Retornou {resultado}\n"
            )

        return resultado

    return printar_data


# Função responsável pelo cadastro de clientes
@log_transacao
def cadastro_cliente(clientes):
    Nome = input("Digite o Nome do cliente: ")
    Data = input("Digite a data de nascimento do cliente no formato(XX/XX/XXXX): ")
    cpf = input("Digite o apenas o número do CPF: ")
    if erro_cpf(cpf, clientes):
        return "CPF incorreto"
    Logradouro = input("Digite o logradouro do endereço(Não contém Número, bairro, cidade e estado): ")
    Numero = input("Digite o número: ")
    if erro_numero(Numero):
        return "Número incorreto"
    Bairro = input("Digite o bairro: ")
    Cidade = input("Digite a cidade: ")
    Estado = input("Digite a sigla do estado: ")
    endereco = f"{Logradouro},{Numero} - {Bairro} - {Cidade}/{Estado}"

    cliente = PessoaFisica(endereco=endereco, cpf=cpf, nome=Nome, data_nasc=Data)

    clientes.append(cliente)
    print("\nCliente Cadastrado com sucesso!!!")


# Função responsável pelo cadastro de contas bancárias
@log_transacao
def cadastro_conta(clientes):
    global numero_conta, NUMERO_AGENCIA

    cpf = input("Digite o número de CPF do cliente que quer criar uma conta: ")
    agencia1 = f"000{NUMERO_AGENCIA}"

    cliente = existe_cpf(cpf, clientes)
    if cliente:
        conta = Conta_corrente(numero=numero_conta, agencia=agencia1, cliente=cliente, limite=500, limite_saques=3)
        cliente.adicionar_conta(conta=conta)
        numero_conta += 1
        print("\n Conta cadastrada com sucesso!!")
    else:
        print("\nNão existe nenhum cliente cadastrado com este CPF")


# Função responsável por identificar a conta para exibir o extrato
@log_transacao
def func_extrato(clientes):
    cpf = input("Digite o número de CPF do cliente para escolher conta: ")
    cliente = existe_cpf(cpf, clientes)
    if cliente:
        numero = input("Digite o número da conta que deseja ver o extrato: ")
        conta = existe_conta(numero, cliente)
        if conta:
            exibir_extrato(conta)
        else:
            print("\nNão existe nenhuma conta pertencente a este cliente com este número")
    else:
        print("\nNão existe nenhum cliente cadastrado com este CPF!!")


# Função responsável por realizar um deposito
@log_transacao
def deposito(clientes):
    cpf = input("Digite o número de CPF do cliente que deseja fazer um deposito: ")
    cliente = existe_cpf(cpf, clientes)
    if cliente:
        numero = input("Digite o número da conta que deseja fazer um deposito: ")
        conta = existe_conta(numero, cliente)
        if conta:
            valor = input("Digite o valor que deseja depositar: ")
            try:
                valornum = float(valor)
                if valornum < 0:
                    print("Valor inválido, números negativos não são permitidos")
                else:
                    deposito = Deposito(valornum)
                    cliente.realizar_transacao(conta, deposito)
            except Exception as e:
                print("Exceção:" + e)
                print("Número inválido, por favor digite um número no formato 00.00")
        else:
            print("\nNão existe nenhuma conta pertencente a este cliente com este número")
    else:
        print("\nNão existe nenhum cliente cadastrado com este CPF!!")


# Função responsável por realizar um saque
@log_transacao
def saque(clientes):
    cpf = input("Digite o número de CPF do cliente que deseja fazer um saque: ")
    cliente = existe_cpf(cpf, clientes)
    if cliente:
        numero = input("Digite o número da conta que deseja fazer um saque: ")
        conta = existe_conta(numero, cliente)
        if conta:
            valor = input("Digite o valor que deseja sacar: ")
            try:
                valornum = float(valor)
                if valornum < 0:
                    print("Valor inválido, números negativos não são permitidos")
                else:
                    saque = Saque(valornum)
                    cliente.realizar_transacao(conta, saque)
            except Exception as e:
                print("Exceção:" + e)
        else:
            print("\nNão existe nenhuma conta pertencente a este cliente com este número")
    else:
        print("\nNão existe nenhum cliente cadastrado com este CPF!!")


# Main do sistema
def main():
    global clientes, numero_conta

    while True:

        opcao = menu()

        if opcao == "1":
            cadastro_cliente(clientes)

        elif opcao == "2":
            cadastro_conta(clientes)

        elif opcao == "3":
            deposito(clientes)

        elif opcao == "4":
            saque(clientes)

        elif opcao == "5":
            func_extrato(clientes)

        elif opcao == "6":
            listar_clientes(clientes)

        elif opcao == "7":
            listar_contas(clientes)

        elif opcao == "8":
            break

        else:
            print("Opção inválida, tente novamente")


if __name__ == "__main__":
    main()
