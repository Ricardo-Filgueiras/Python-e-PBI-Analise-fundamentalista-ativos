# Importando as bibliotecas
import fundamentus
import pandas as pd

# Definindo a carteira de ações
carteira_fund = ["ABEV3", "B3SA3", "ELET3", "GGBR4", "ITSA4",
                 "PETR4", "RENT3", "SUZB3", "VALE3", "WEGE3"]

# Criando um df com algumas infos da carteira
ind = []
for papel in carteira_fund:
  df = fundamentus.get_papel(papel)[['Setor', 'Cotacao', 'Min_52_sem', 'Max_52_sem', 'Valor_de_mercado',
                                            'Nro_Acoes', 'Patrim_Liq','Receita_Liquida_12m','Receita_Liquida_3m',
                                            'Lucro_Liquido_12m', 'Lucro_Liquido_3m']]
  ind.append(df)
ind = pd.concat(ind)


# Passando o ticker para uma coluna
ind = ind.reset_index()
ind.rename(columns = {'index':'Ativo'}, inplace=True)

# Alterando colunas object para numeric
colunas = ['Cotacao', 'Min_52_sem', 'Max_52_sem', 'Valor_de_mercado', 'Nro_Acoes', 'Patrim_Liq',
           'Receita_Liquida_12m', 'Receita_Liquida_3m', 'Lucro_Liquido_12m', 'Lucro_Liquido_3m']
ind[colunas] = ind[colunas].apply(pd.to_numeric, errors='coerce', axis=1)

# Criando um novo df com alguns indicadores da carteira
ind_2 = fundamentus.get_resultado_raw().reset_index()
ind_2 = ind_2.query("papel in @carteira_fund")
ind_2 = ind_2[['papel','P/L', 'Div.Yield','P/VP','ROE']].reset_index(drop=True)
ind_2.rename(columns={'papel': 'Ativo','Div.Yield':'DY'}, inplace= True)

# Concatenando os dfs em um só com as infos e indicadores
indicadores = pd.merge(ind, ind_2, on="Ativo")

# Criando uma coluna para LPA (Lucro por Ação) e VPA (Valor Patrimonial por ação)
# para calcular a fórmula de Graham  Valor intrínseco de uma ação (VI = √22,5 x LPA x VPA)
indicadores["LPA"] = (indicadores["Lucro_Liquido_12m"] / indicadores ["Nro_Acoes"]).round(2)
indicadores["VPA"] = (indicadores["Patrim_Liq"] / indicadores ["Nro_Acoes"]).round(2)

del ind, ind_2, carteira_fund, colunas