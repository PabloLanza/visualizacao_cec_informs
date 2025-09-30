def filtro_comp_mando(c, m, df):
    if len(c) < 1:
        competicoes = ['Mineiro', 'Sul Americana', 'Brasileiro', 'Copa do Brasil']
    else:
        competicoes = c

    
    if len(m) < 1:
        mando = ['Casa', 'Fora']
    else:
        mando = m

    df = df[(df["competicao"].isin(competicoes)) & (df["mando"].isin(mando))]

    return df


def remover_espacos(df):
    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    for col in df.select_dtypes(include=["object", "string"]):
        df[col] = df[col].str.strip()

    return df

def gols(competicoes=[], mando=[]):

    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("escalacoes.xlsx")
    df_jogos = pd.read_excel("jogos.xlsx")

    #JUNÇÃO DOS DFs
    df_gols = pd.merge(df_escalacao[["id_jogo", "autor_gols_pro"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")
    
    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    df_gols = remover_espacos(df=df_gols)

    #CRIANDO UM FILTRO NOS FILTROS
    df_gols = filtro_comp_mando(c=competicoes, m=mando, df=df_gols)    
    
    #REMOVE JOGOS SEM GOLS
    df_gols = df_gols.dropna()


    #QUEBRA AS COLUNAS EM LISTAS
    df_gols["autor_gols_pro"] = df_gols["autor_gols_pro"].str.split(', ')

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_gols = sum(df_gols["autor_gols_pro"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_gols = [item.upper() for item in lista_gols]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "gols": lista_gols
    }

    df_resumo_gols = pd.DataFrame(dados)
    


    #CONTAGEM DE GOLS
    gols = df_resumo_gols["gols"].value_counts().reset_index()

    #RENOMEANDO AS COLUNAS
    gols = gols.rename(columns={'gols': 'jogador'})
    gols = gols.rename(columns={'count': 'gols'})

    return gols.sort_values(by=("gols"), ascending=False)


def assistencias(competicoes=[], mando=[]):

    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("escalacoes.xlsx")
    df_jogos = pd.read_excel("jogos.xlsx")

    #FAZENDO A JUNÇÃO DOS DFs
    df_ass = pd.merge(df_escalacao[["id_jogo", "assistencias"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")
    
    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    df_ass = remover_espacos(df=df_ass)
    
    #CRIANDO UM FILTRO NOS FILTROS
    df_ass = filtro_comp_mando(c=competicoes, m=mando, df=df_ass)

    #REMOVE JOGOS SEM GOLS
    df_ass = df_ass.dropna()

    #QUEBRA AS COLUNAS EM LISTAS
    df_ass["assistencias"] = df_ass["assistencias"].str.split(', ')

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_ass = sum(df_ass["assistencias"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_ass = [item.upper() for item in lista_ass]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "assistencias": lista_ass
    }

    df_resumo_ass = pd.DataFrame(dados)
    


    #CONTAGEM DE GOLS
    ass = df_resumo_ass["assistencias"].value_counts().reset_index()

    ass = ass.rename(columns={'assistencias': 'jogador'})
    ass = ass.rename(columns={'count': 'assistencias'})

    #REMOVENDO COLUNAS COM NONE, PENALTI E FALTA
    ass = ass[~ass["jogador"].isin(["NONE", "PÊNALTI", "FALTA"])]

    return ass.sort_values(by=("assistencias"), ascending=False)


def dobradinha(competicoes=[], mando=[]):
    import pandas as pd


    #TABELAS QUE SERÃO USADAS
    df_escalacao = pd.read_excel("escalacoes.xlsx")
    df_jogos = pd.read_excel("jogos.xlsx")

    #JUNÇÃO DOS DFs
    df_gol_ass = pd.merge(df_escalacao[["id_jogo", "autor_gols_pro", "assistencias"]], df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")

    #REMOVENDO ESPAÇOS ANTES E DEPOIS DOS NOMES
    df_gol_ass = remover_espacos(df=df_gol_ass)

    #CRIANDO UM FILTRO NOS FILTROS
    df_gol_ass = filtro_comp_mando(c=competicoes, m=mando, df=df_gol_ass)

    #REMOVENDO COLUNAS QUE NÃO SERÃO USADAS
    df_gol_ass = df_gol_ass[["autor_gols_pro", "assistencias"]]

    #REMOVENDO VALORES NULOS
    df_gol_ass = df_gol_ass.dropna()

    #QUEBRA AS COLUNAS EM LISTAS
    df_gol_ass["autor_gols_pro"] = df_gol_ass["autor_gols_pro"].str.split(', ')
    df_gol_ass["assistencias"] = df_gol_ass["assistencias"].str.split(', ')

    #CONCATENA CADA LISTA EM UMA LISTA APENAS
    lista_gol = sum(df_gol_ass["autor_gols_pro"], [])
    lista_ass = sum(df_gol_ass["assistencias"], [])

    #COLOCA TODOS OS JOGADORES EM LETRAS MAIUSCULAS
    lista_gol = [item.upper() for item in lista_gol]
    lista_ass = [item.upper() for item in lista_ass]

    #PREPARA OS DADOS PRA FAZER O DATA FRAME
    dados = {
        "gols": lista_gol,
        "assistencias": lista_ass
    }

    #CRIA O DATA FRAME
    df_dobradinha = pd.DataFrame(dados)

    #INDICA QUE NÃO IMPORTA A ORDEM DA DUPLA (A + B) OU (B + A)
    df_dobradinha["dupla"] = df_dobradinha.apply(lambda x: tuple(sorted([x["gols"], x["assistencias"]])), axis=1)

    #FAZ A CONTAGEM DE QUANTAS VEZES CADA DUPLA APARECEU
    contagem_duplas = df_dobradinha["dupla"].value_counts().reset_index()
    contagem_duplas.columns = ["dupla", "quantidade"]

    #REMOVENDO DADOS NÃO COERENTES
    contagem_duplas = contagem_duplas[contagem_duplas["dupla"].apply(lambda x: all(v not in ["NONE", "PÊNALTI", "FALTA"] for v in x))]

    #TRANFORMAR AS TUPLAS EM STRINGS
    contagem_duplas["dupla"] = contagem_duplas["dupla"].apply(lambda x: " - ".join(map(str, x)))

    return contagem_duplas.sort_values(by="quantidade", ascending=False)


def participacoes(competicoes=[], mando=[]):
    import pandas as pd

    df_gols = gols(competicoes=competicoes, mando=mando)
    df_ass = assistencias(competicoes=competicoes, mando=mando)

    df_participacoes = pd.merge(df_gols, df_ass, on="jogador", how="outer")

    #PREENCHER VALORES AUSENTES COM 0
    df_participacoes = df_participacoes.fillna(0)

    #CALCULA AS PARTICIPACOES (GOLS + ASSISTENCIAS)
    df_participacoes["participacoes"] = df_participacoes["gols"] + df_participacoes["assistencias"]

    #TRANSFORMANDOAS COLUNAS FLOAT DO DF PRO TIPO INT
    for c in df_participacoes.select_dtypes(include="float"):
        df_participacoes[c] = df_participacoes[c].astype(int)
    
    #REMOVENDO DADOS NÃO COERENTES
    df_participacoes = df_participacoes[~df_participacoes["jogador"].isin(["NONE", "PÊNALTI", "FALTA"])]

    return df_participacoes.sort_values(by="participacoes", ascending=False)    
    
    
def perfil_finalizacoes(competicoes=[], mando=[]):

    import pandas as pd
    import matplotlib.pyplot as plt

    #TABELAS QUE SERÃO USADAS
    df_jogos = pd.read_excel("jogos.xlsx")
    df_ataque = pd.read_excel("ataque.xlsx")

    #JUNÇÃO DOS DFs
    df_chutes = pd.merge(df_jogos[["id_jogo", "competicao", "mando"]], df_ataque[["id_jogo", "chutes_cruzeiro", "chutes_adv", "chutes_gol_cruzeiro", "chutes_gol_adv", "chutes_area_cruzeiro", "chutes_area_adv", "chutes_fora_area_cruzeiro", "chutes_fora_area_adv"]], on="id_jogo", how="inner")

    #REMOVENDO ESPAÇOS EM COLUNAS STRING
    df_chutes = remover_espacos(df=df_chutes)
    
    #CRIANDO UM FILTRO NOS FILTROS
    df_chutes = filtro_comp_mando(c=competicoes, m=mando, df=df_chutes)
    df_chutes["chutes_nao_gol_cruzeiro"] = df_chutes["chutes_cruzeiro"] - df_chutes["chutes_gol_cruzeiro"]
    df_chutes["chutes_nao_gol_adv"] = df_chutes["chutes_adv"] - df_chutes["chutes_gol_adv"]

    df_chutes_sum = df_chutes[["chutes_cruzeiro", "chutes_adv", "chutes_gol_cruzeiro", "chutes_gol_adv", "chutes_area_cruzeiro", "chutes_area_adv", "chutes_fora_area_cruzeiro", "chutes_fora_area_adv", "chutes_nao_gol_cruzeiro", "chutes_nao_gol_adv"]].sum().reset_index()
    df_chutes_sum.columns = ["stats", "soma"]
    df_chutes_sum["media"] = round(df_chutes_sum["soma"] / len(df_chutes), 0)


    df_chutes_sum = df_chutes_sum.set_index("stats")
    

    #GRAFICO PIZZA CHUTES DENTRO E FORA AREA
    valores1 = df_chutes_sum.loc[["chutes_nao_gol_cruzeiro", "chutes_gol_cruzeiro"], "soma"]
    valores2 = df_chutes_sum.loc[["chutes_nao_gol_adv", "chutes_gol_adv"], "soma"]
    valores3 = df_chutes_sum.loc[["chutes_area_cruzeiro", "chutes_fora_area_cruzeiro"], "soma"]
    valores4 = df_chutes_sum.loc[["chutes_area_adv", "chutes_fora_area_adv"], "soma"]

    fig1, ax1 = plt.subplots()
    ax1.pie(valores1,
            labels=["Chutes Sem Direção do Gol", "Chutes Ao Gol"], autopct="%.1f%%", startangle=90, colors=["#427ef5", "#f5ba67"],
            wedgeprops={"width": 0.4})
    ax1.set_title("Chutes Sem Direção x Chutes Ao Gol - Cruzeiro", color="#427ef5", fontweight="bold", fontsize=14)
    ax1.set_aspect("equal")

    fig2, ax2 = plt.subplots()
    ax2.pie(valores2,
            labels=["Chutes Sem Direção do Gol", "Chutes Ao Gol"], autopct="%.1f%%", startangle=90, colors=["#427ef5", "#f5ba67"],
            wedgeprops={"width": 0.4})
    ax2.set_title("Chutes Sem Direção x Chutes Ao Gol - Adversário", color="#427ef5", fontweight="bold", fontsize=14)
    ax2.set_aspect("equal")

    fig3, ax3 = plt.subplots()
    ax3.pie(valores3, 
            labels=["Dentro da Área", "Fora da Área"], autopct="%.1f%%", startangle=90, colors=["#427ef5", "#f5ba67"])
    ax3.set_title("Perfil das Finalizações do Cruzeiro", color="#427ef5", fontweight="bold", fontsize=14)

    fig4, ax4 = plt.subplots()
    ax4.pie(valores4,
            labels=["Dentro da Área", "Fora da Área"], autopct="%.1f%%", startangle=90, colors=["#427ef5", "#f5ba67"])
    ax4.set_title("Perfil das Finalizações do Adversário", color="#427ef5", fontweight="bold", fontsize=14)
    plt.tight_layout()

    return fig1, fig2, fig3, fig4
    

def passes_trocados(competicoes=[], mando=[]):

    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    #TABELAS QUE SERÃO USADAS
    df_jogos = pd.read_excel("jogos.xlsx")
    df_ataque = pd.read_excel("ataque.xlsx")

    #JUNÇÃO DOS DFs
    df_passes = pd.merge(df_jogos[["id_jogo", "adversario", "competicao", "mando"]], df_ataque[["id_jogo", "passes_cruzeiro", "passes_certos_cruzeiro", "passes_adv", "passes_certos_adv"]], on="id_jogo", how="inner")

    #REMOVENDO ESPAÇOS
    df_passes = remover_espacos(df=df_passes)

    #FILTRO DE COMPETIÇÕES E MANDOS
    df_passes = filtro_comp_mando(c=competicoes, m=mando, df=df_passes)

    #DECLARAÇÃO DAS VARIÁVEIS QUE SERÃO USADAS
    x = df_passes["id_jogo"]
    passes_cruzeiro = df_passes["passes_cruzeiro"]
    passes_certos_cruzeiro = df_passes["passes_certos_cruzeiro"]
    passes_adv = df_passes["passes_adv"]
    passes_certos_adv = df_passes["passes_certos_adv"]

    #GRÁFICOS DE LINHAS
    fig1, ax1 = plt.subplots(figsize=(10,5))

    ax1.plot(x, passes_cruzeiro, label="Passes Cruzeiro", marker="o", color="darkblue")
    ax1.plot(x, passes_adv, label="Passes Adversário", marker="o", color="lightblue")

    ax1.set_title("Passes Trocados Por Jogo", fontsize=16)
    ax1.legend()
    ax1.set_xlabel("Jogos")
    ax1.set_ylabel("Passes")
    ax1.grid(True)

    fig2, ax2 = plt.subplots(figsize=(10,5))

    ax2.plot(x, passes_certos_cruzeiro, label="Passes Certos Cruzeiro", marker="o", color="darkblue")
    ax2.plot(x, passes_certos_adv, label="Passes Certos Adversários", marker="o", color="lightblue")

    ax2.set_title("Passes Certos Por Jogo", fontsize=16)
    ax2.legend()
    ax2.set_xlabel("Jogos")
    ax2.set_ylabel("Passes")
    ax2.grid(True)

    return fig1, fig2
    

def normalizar(val):
    import pandas as pd
    import numpy as np

    #CASO 1 - LISTA JÁ PRONTA
    if isinstance(val, list):
        return [int(x) for x in val if x not in [0, None] and not pd.isna(x)]
    
    elif isinstance(val, str):
        return [int(x) for x in val.split(", ") if x.strip() not in ["", "0"]]

    elif pd.notna(val) and val != 0:
        return [int(val)]
    
    else:
        return []


def minutos_gols(competicoes=[], mando=[]):

    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    #TABELAS QUE SERÃO USADAS
    df_esc = pd.read_excel("escalacoes.xlsx")
    df_jogos = pd.read_excel("jogos.xlsx")

    #JUNÇÃO DOS DFs
    df_min = pd.merge(df_esc[["id_jogo", "minutos_gols_pro", "minutos_gols_contra"]], 
                      df_jogos[["id_jogo", "competicao", "mando"]], on="id_jogo", how="inner")

    #REMOVENDO ESPAÇOS
    df_min[["competicao", "mando"]] = remover_espacos(df=df_min[["competicao", "mando"]])

    #APLICANDO FILTROS
    df_min = filtro_comp_mando(c=competicoes, m=mando, df=df_min)

    #REMOVENDO AS COLUNAS QUE NÃO SERÃO USADAS
    df_min = df_min[["minutos_gols_pro", "minutos_gols_contra"]]

    #TRANSFORMANDO AS COLUNAS EM LISTAS
    lista_min_gols_pro = df_min["minutos_gols_pro"].apply(normalizar)
    lista_min_gols_contra = df_min["minutos_gols_contra"].apply(normalizar)

    #CONCATENANDO TUDO EM UMA SÓ LISTA
    lista_min_gols_pro = [x for sublist in lista_min_gols_pro for x in sublist]
    lista_min_gols_contra = [x for sublist in lista_min_gols_contra for x in sublist]
    
    #DEFININDO OS INTERVALOS
    bins = list(range(0, 100, 11))

    #CRIAR OS RÓTULOS DOS INTERVALOS
    labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]

    #TRANFORMANDO EM SERIES
    s = pd.Series(lista_min_gols_pro)
    s1 = pd.Series(lista_min_gols_contra)

    #CONTANDO A QUANTIDADE POR INTERVALO
    intervalos_pro = pd.cut(s, bins=bins, labels=labels, right=False).value_counts().sort_index()
    intervalos_contra = pd.cut(s1, bins=bins, labels=labels, right=False).value_counts().sort_index()

    df_pro = intervalos_pro.reset_index()
    df_pro.columns = ["intervalo", "gols_pro"]

    df_contra = intervalos_contra.reset_index()
    df_contra.columns = ["intervalo", "gols_contra"]

    #DF FINAL
    df_final = pd.merge(df_pro, df_contra, on="intervalo", how="inner")

    #PLOT
    intervalos = df_final["intervalo"]
    gols_cruzeiro = df_final["gols_pro"]
    gols_adv = df_final["gols_contra"]

    #LARGURA DAS BARRAS
    largura = 0.35

    #POSIÇÕES NO EIXO X
    x = np.arange(len(intervalos))

    #CRIANDO O GRÁFICO
    fig, ax = plt.subplots(figsize=(10, 6))
    barras1 = ax.bar(x - largura/2, gols_cruzeiro, width=largura, color="darkblue", label="Gols do Cruzeiro")

    barras2 = ax.bar(x + largura/2, gols_adv, width=largura, color="#fcba03", label="Gols do Adversário")

    ax.set_title("Gols por Intervalo de Minutos", fontsize=16, color="darkblue", fontweight="bold")
    ax.set_xlabel("Intervalo (Minutos)", color="darkblue", fontweight="bold")
    ax.set_ylabel("Gols", color="darkblue", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(intervalos)
    ax.legend()

    ax.bar_label(barras1, padding=3)
    ax.bar_label(barras2, padding=3)

    return fig







