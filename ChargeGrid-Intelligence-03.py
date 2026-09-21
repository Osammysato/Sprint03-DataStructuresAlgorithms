# --------- DADOS DO SISTEMA ---------

class Sessao:
    def __init__(self, id_sessao, nome, tipo, potencia, horas):
        self.id = id_sessao
        self.nome = nome
        self.tipo = tipo
        self.potencia = potencia
        self.horas = horas

        self.potencia_aplicada = 0
        self.tarifa = 0
        self.energia = 0
        self.custo = 0
        self.status = "Conectada"


sessoes = []
limite_estacao = 30.0
pico = False


# --------- ENTRADA DE DADOS ---------

# 1. nome e tipo de usuario
def nome_e_tipo_usuario():
    nome = input("Digite o nome do veiculo: ")

    print("\n Tipos de usuarios:")
    print("1 -- REGULAR")
    print("2 -- PREMIUM")
    print("3 -- CONDOMINIO")

    while True:
        try:
            tipo = int(input("Escolha (1, 2 ou 3): "))
            if tipo >= 1 and tipo <= 3:
                break
            else:
                print("Precisa ser numeros de 1 a 3 ")
        except:
            print("\nDigite apenas numeros!")
    return nome, tipo


# 2. carregador
def carregador_kw():
    print("\nTipos de carregador:")
    print("1 - Lento   (7.4 kW)")
    print("2 - Normal  (11 kW)")
    print("3 - Rapido  (22 kW)")

    while True:
        try:
            potencia_carregador = int(input("Escolha (1, 2 ou 3): "))
            if potencia_carregador >= 1 and potencia_carregador <= 3:
                break
            else:
                print("Precisa ser numeros de 1 a 3 ")
        except:
            print("\nDigite apenas numeros!")

    if potencia_carregador == 1:
        return 7.4
    if potencia_carregador == 2:
        return 11.0
    if potencia_carregador == 3:
        return 22.0


# 3. duracao da sessao
def duracao_sessao():
    while True:
        try:
            duracao = float(input("\nDuracao da sessao: "))
            if duracao > 0:
                break
            else:
                print("\nApenas numeros maiores que zero!")
        except:
            print("\nDigite apenas numeros!")

    while True:
        try:
            unidade = str(input("Unidade (h)oras ou (m)inutos: ")).lower()
            if unidade == "h" or unidade == "m":
                break
            else:
                print("Digite apenas as letra *h* ou *m* ")
        except:
            print("\nDigite somente a letra * h * para horas e a letra * m * para minutos")

    if unidade == "m":
        duracao_horas = duracao / 60
    else:
        duracao_horas = duracao

    return duracao_horas


# --------- CALCULO E TARIFACAO ---------

# 4. calcular tarifa (agora dinamica)
def calcular_tarifa(tipo, total_sessoes):
    if tipo == 1:
        tarifa = 1.50
    elif tipo == 2:
        tarifa = 1.20
    elif tipo == 3:
        tarifa = 1.35

    if pico:
        tarifa = tarifa + 0.40

    if total_sessoes >= 3:
        tarifa = tarifa + 0.30

    return tarifa


# 5. calcular energia e custo
def calcular(potencia, duracao_horas, tarifa):
    energia = potencia * duracao_horas
    custo = energia * tarifa
    return energia, custo


# --------- INTEGRACAO SIMULADA ---------

# 6. simulacao OCPP e MODBUS
def integracao(mensagem, nome, potencia):
    print(f"\n  [OCPP] Enviando -> {mensagem}")
    print(f"  [OCPP] Resposta <- {mensagem}.conf | Status: Accepted")
    print(f"  [MODBUS] Leitura 40001: {potencia:.1f} kW")
    print(f"  [MODBUS] Escrita 40010: {potencia:.1f} kW | OK")


# --------- CRIAR SESSAO ---------

# 7. criar uma sessao manualmente
def criar_sessao():
    while True:
        try:
            id_novo = int(input("Digite o ID da nova sessão: "))

            if id_novo <= 0:
                print("O ID precisa ser um numero inteiro maior que zero!")
                continue

            id_ja_existe = False
            for s in sessoes:
                if s.id == id_novo:
                    id_ja_existe = True
                    break

            if id_ja_existe:
                print("Esse ID ja existe! Tente outro.")
            else:
                break

        except ValueError:
            print("Por favor, digite um número inteiro válido para o ID.")

    nome, tipo = nome_e_tipo_usuario()
    potencia = carregador_kw()
    horas = duracao_sessao()

    nova_sessao = Sessao(id_novo, nome, tipo, potencia, horas)

    sessoes.append(nova_sessao)

    print(f"\nSessao {id_novo} criada com sucesso! ({nome})")


# 8. simular sessoes desordenadas
def simular_sessoes_desordenadas():
    sessoes.append(Sessao(505, "Tesla Model S", 2, 50.0, 2.0))
    sessoes.append(Sessao(10, "Nissan Leaf", 1, 20.0, 1.5))
    sessoes.append(Sessao(999, "Porsche Taycan", 2, 150.0, 2.3))
    sessoes.append(Sessao(42, "BYD Sealion 7", 1, 22.0, 3.2))
    sessoes.append(Sessao(314, "BMW i3", 3, 11.0, 2.4))
    print("\nSessoes criadas, porém desordenas. Use a opção 3 para ordená-las, e após isso a opção 4 para processá-las")


# --------- PROCESSAR RECARGAS ---------

# 9. processar todas as sessoes conectadas
def processar():
    # contar sessoes conectadas
    conectadas = 0
    soma_potencia = 0
    for s in sessoes:
        if s.status == "Conectada":
            conectadas = conectadas + 1
            soma_potencia = soma_potencia + s.potencia

    if conectadas == 0:
        print("\nNenhuma sessao conectada.")
        return

    # controle de demanda
    if soma_potencia > limite_estacao:
        fator = limite_estacao / soma_potencia
    else:
        fator = 1.0

    print("\n═══════════════════════════════════════")
    print("         PROCESSANDO RECARGAS          ")
    print("═══════════════════════════════════════")
    print(f"Limite da estacao:     {limite_estacao:.1f} kW")
    print(f"Potencia solicitada:   {soma_potencia:.1f} kW")
    print(f"Sessoes conectadas:    {conectadas}")
    print(f"Horario de pico:       {'SIM' if pico else 'NAO'}")

    if fator < 1:
        print(">> Demanda acima do limite! Potencia dividida.")

    total_aplicada = 0

    for s in sessoes:
        if s.status == "Conectada":
            potencia_aplicada = s.potencia * fator
            tarifa = calcular_tarifa(s.tipo, conectadas)
            energia, custo = calcular(potencia_aplicada, s.horas, tarifa)

            s.potencia_aplicada = potencia_aplicada
            s.tarifa = tarifa
            s.energia = energia
            s.custo = custo
            s.status = "Finalizada"

            total_aplicada = total_aplicada + potencia_aplicada

            nome_tipo = ""
            if s.tipo == 1:
                nome_tipo = "REGULAR"
            elif s.tipo == 2:
                nome_tipo = "PREMIUM"
            elif s.tipo == 3:
                nome_tipo = "CONDOMINIO"

            print(f"\n--- ID: {s.id} | {s.nome} ({nome_tipo}) ---")
            integracao("StopTransaction", s.nome, potencia_aplicada)
            print(f"  Potencia solicitada: {s.potencia:.1f} kW")
            print(f"  Potencia aplicada:   {potencia_aplicada:.1f} kW")
            print(f"  Duracao:             {s.horas:.2f} horas")
            print(f"  Tarifa:              R$ {tarifa:.2f} /kWh")
            print(f"  Energia:             {energia:.2f} kWh")
            print(f"  Custo:               R$ {custo:.2f}")

    print(f"\nPotencia total aplicada: {total_aplicada:.1f} kW de {limite_estacao:.1f} kW")


# --------- EXIBICAO ---------

# 10. listar sessoes
def listar_sessoes():
    if len(sessoes) == 0:
        print("\nNenhuma sessao cadastrada.")
        return

    print("\n═══════════════════════════════════════")
    print("           LISTA DE SESSOES            ")
    print("═══════════════════════════════════════")

    for i in range(len(sessoes)):
        s = sessoes[i]
        print(f"Sessao {i+1}: | ID: {s.id} | Nome: {s.nome} | Potencia: {s.potencia_aplicada:.1f} kW | Tarifa: R$ {s.tarifa:.2f} | Energia: {s.energia:.2f} kWh | R$ {s.custo:.2f} | {s.status}")


# 11. relatorio geral
def relatorio():
    if len(sessoes) == 0:
        print("\nNenhuma sessao para relatorio.")
        return

    energia_total = 0
    valor_total = 0
    finalizadas = 0
    maior_consumo = 0
    menor_consumo = float("inf")

    for s in sessoes:
        energia_total = energia_total + s.energia
        valor_total = valor_total + s.custo
        if s.status == "Finalizada":
            finalizadas = finalizadas + 1
            if s.energia > maior_consumo:
                maior_consumo = s.energia
            if s.energia < menor_consumo:
                menor_consumo = s.energia

    ticket_medio = 0
    if finalizadas > 0:
        ticket_medio = valor_total / finalizadas
    else:
        menor_consumo = 0

    print("\n═══════════════════════════════════════")
    print("     RELATORIO CHARGEGRID INTELLIGENCE ")
    print("═══════════════════════════════════════")
    print(f"Total de sessoes:        {len(sessoes)}")
    print(f"Sessoes finalizadas:     {finalizadas}")
    print(f"Energia total consumida: {energia_total:.2f} kWh")
    print(f"Valor total arrecadado:  R$ {valor_total:.2f}")
    print(f"Ticket Médio:            R$ {ticket_medio:.2f}")
    print(f"Maior consumo:           {maior_consumo:.2f} kWh")
    print(f"Menor consumo:           {menor_consumo:.2f} kWh")
    print(f"Limite da estacao:       {limite_estacao:.1f} kW")
    print("═══════════════════════════════════════")


# --------- ORDENAÇÃO E BUSCA ---------

# 12. ordenar sessoes (Bubble Sort)
def ordenar_sessoes():
    if len(sessoes) == 0:
        print("\nNenhuma sessao para ordenar")
        return

    n = len(sessoes)

    for i in range(n):
        for j in range(n - 1 - i):
            if sessoes[j].id > sessoes[j + 1].id:
                sessoes[j], sessoes[j + 1] = sessoes[j + 1], sessoes[j]

    print("\nSessões ordenadas com sucesso!")


# 13. buscar sessoes
def buscar_sessao():
    if len(sessoes) == 0:
        print("\nNenhuma sessao cadastrada.")
        return

    ordenar_sessoes()

    # Pedindo e validando o ID
    while True:
        try:
            id_busca = int(input("\nDigite o ID da sessao que deseja buscar: "))
            if id_busca > 0:
                break
            else:
                print("Não existem IDs com números decimais, menores ou iguais a 0! Digite um ID válido, por favor!")
        except ValueError:
            print("Digite apenas números inteiros!")

    # Buscando
    inicio = 0
    fim = len(sessoes) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        id_do_meio = sessoes[meio].id

        if id_do_meio == id_busca:
            print("\n--- SESSAO ENCONTRADA ---")
            print(f"ID: {sessoes[meio].id} | Nome: {sessoes[meio].nome} | Potencia Solicitada: {sessoes[meio].potencia:.1f} kW | Status: {sessoes[meio].status}")

            if sessoes[meio].energia > 0:
                print(f"--> RESULTADOS: Potencia Aplicada: {sessoes[meio].potencia_aplicada:.1f} kW | Tarifa: R$ {sessoes[meio].tarifa:.2f} | Energia: {sessoes[meio].energia:.2f} kWh | Custo: R$ {sessoes[meio].custo:.2f}")
            print("-------------------------")
            return

        elif id_busca > id_do_meio:
            inicio = meio + 1
        elif id_busca < id_do_meio:
            fim = meio - 1


    print(f"\nSessao com ID {id_busca} nao encontrada!")


# --------- MENU PRINCIPAL ---------

def menu():
    global pico

    while True:
        print("\n═══════════════════════════════════════")
        print("   CHARGEGRID INTELLIGENCE - SPRINT 03 ")
        print("═══════════════════════════════════════")
        print(f"Horario de pico: {'LIGADO' if pico else 'DESLIGADO'}")
        print("1 - Criar sessao")
        print("2 - Simular Sessões desordenas")
        print("3 - Ordenar Sessões (Bubble Sort)")
        print("4 - Listar sessoes")
        print("5 - Processar recargas")
        print("6 - Buscar Sessão")
        print("7 - Gerar relatorio")
        print("8 - Alternar horario de pico")
        print("9 - Sair")


        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            criar_sessao()
        elif opcao == "2":
            simular_sessoes_desordenadas()
        elif opcao == "3":
            ordenar_sessoes()
        elif opcao == "4":
            listar_sessoes()
        elif opcao == "5":
            listar_sessoes()
            processar()
        elif opcao == "6":
            buscar_sessao()
        elif opcao == "7":
            relatorio()
        elif opcao == "8":
            pico = not pico
            print(f"\nHorario de pico: {'LIGADO' if pico else 'DESLIGADO'}")
        elif opcao == "9":
            print("Encerrando o sistema...")
            break
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    menu()