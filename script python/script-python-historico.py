# Código completo da obtenção dos dados históricos das cotações da carteira de 01/08/2023 à 30/08/2024

# Importando a biblioteca
import yfinance as yf

# Definindo a carteira de ações
carteira_yf = ['ABEV3.SA', 'B3SA3.SA', 'ELET3.SA', 'GGBR4.SA', 'ITSA4.SA',
               'PETR4.SA', 'RENT3.SA', 'SUZB3.SA', 'VALE3.SA', 'WEGE3.SA']

# Carregando os dados da carteira
df = yf.download(carteira_yf, start="2023-08-01", end="2024-08-30")

# Passando os ativos para o multindex do df
cotacoes = df.stack(level=1)

# Resetando os índices e renomenado a coluna dos ativos
cotacoes = cotacoes.reset_index().rename(columns={'Ticker': 'Ativo'})

# Organizando o df
cotacoes = cotacoes[["Date", "Open", "High", "Low", "Close", "Ativo"]]

del carteira_yf, df