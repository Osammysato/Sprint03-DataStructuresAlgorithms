# Sprint-Data-Structures-and-Algorithms

## ChargeGrid Intelligence - Sprint 03

Sistema Inteligente de Gerenciamento de Recarga de Veiculos Eletricos.

Continuacao da Sprint 02: o sistema agora foi aprimorado para utilizar estruturas de dados baseadas em classes (Orientação a Objetos básica), garantindo identificadores únicos para cada sessão de recarga. Além disso, foram implementados algoritmos clássicos de ordenação (Bubble Sort) e busca (Busca Binária) para otimizar o gerenciamento do pátio de recarga.

## Requisitos

- Python 3 (sem bibliotecas externas)

## Como executar

```bash
python Sprint-03.py
```

## Menu do sistema

```text
1 - Criar sessao                      (Cria uma sessao com ID unico e dados informados)
2 - Simular Sessões desordenas        (Cria 5 sessoes automaticas com IDs misturados para teste)
3 - Ordenar Sessões (Bubble Sort)     (Ordena a lista de sessoes crescentemente pelo ID)
4 - Listar sessoes                    (Mostra todas as sessoes em memoria)
5 - Processar recargas                (Calcula energia, tarifa e custo, e simula a integracao)
6 - Buscar Sessão                     (Localiza uma sessao especifica pelo ID usando busca binaria)
7 - Gerar relatorio                   (Mostra o resumo geral com novos indicadores de consumo)
8 - Alternar horario de pico          (Liga/desliga o acrescimo de pico na tarifa)
9 - Sair
```

## Fluxo recomendado para demonstracao

1. Executar o programa.
2. Escolher a Opcao **2** (Simular Sessões desordenadas).
3. Escolher a Opcao **4** (Listar sessoes) -> Observe que os IDs estao fora de ordem (505, 10, 999...).
4. Escolher a Opcao **3** (Ordenar Sessões) -> O Bubble Sort organizará as sessões pelo ID.
5. Escolher a Opcao **4** novamente para confirmar a nova ordem.
6. Escolher a Opcao **5** (Processar recargas) -> O sistema fará o controle de demanda, divisão de potência e calculará as tarifas.
7. Escolher a Opcao **6** (Buscar Sessão) e digitar um ID existente (ex: 42 ou 314) para testar a Busca Binária.
8. Escolher a Opcao **7** (Gerar relatorio) -> Para visualizar os totais e os novos indicadores (Ticket Médio e Consumo Máx/Mín).
9. (Opcional) Testar a criacao de uma sessao manual na Opcao **1**, tentando usar um ID repetido para validar o bloqueio do sistema.

## O que foi mantido da Sprint 02

- Regras de negócio originais: Tipos de usuário (REGULAR, PREMIUM, CONDOMINIO) e carregadores (Lento 7.4 kW, Normal 11 kW, Rápido 22 kW).
- Controle de demanda com limite estático (30 kW).
- Tarifação dinâmica influenciada por horário de pico e alta demanda (3+ veículos).
- Simulação dos logs de integração OCPP e MODBUS.

## O que foi adicionado na Sprint 03

- **Classe Sessao:** Transição para um modelo estruturado orientado a objetos.
- **Validação de ID Único:** O sistema não permite a criação de duas sessões com o mesmo identificador.
- **Bubble Sort:** Algoritmo implementado do zero para ordenação das sessões baseada nos IDs.
- **Busca Binária:** Pesquisa rápida de sessões por ID (exige que a lista esteja ordenada).
- **Novas Métricas de Relatório:** Inclusão do Ticket Médio, Maior consumo registrado e Menor consumo registrado.
- **Menu Expandido:** Agora com 9 opções interativas para suportar as novas funcionalidades de busca e ordenação.

## Arquivos

- `Sprint-03.py` ................. código fonte principal do sistema
- `Documentacao_Sprint03.pdf` .... documento técnico com o descritivo de mudanças e cenários
- `README.md` .................... este arquivo

## Integrantes

Equipe ChargeGrid Intelligence
