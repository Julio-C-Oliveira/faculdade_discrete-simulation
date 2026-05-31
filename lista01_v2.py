import math
import statistics as st

import utils

# ==========================================
# Q02, Q03, Q04: MEDIDAS DE CENTRALIDADE
# ==========================================

def calcular_media(dados):
    """Calcula a média aritmética."""
    return st.mean(dados) if dados else 0

def calcular_mediana(dados):
    """Calcula a mediana."""
    return st.median(dados)

def calcular_quartis(dados):
    """
    Calcula os Quartis 1, 2 e 3 baseado na lógica do material da disciplina
    (fatiamento da lista e cálculo da mediana das metades).
    """
    dados_ord = sorted(dados)
    n = len(dados_ord)
    meio = n // 2
    
    q1 = st.median(dados_ord[:meio])
    q2 = st.median(dados_ord)
    
    if n % 2 == 0:
        q3 = st.median(dados_ord[meio:])
    else:
        q3 = st.median(dados_ord[meio + 1:])
        
    return q1, q2, q3

def calcular_moda(dados):
    """Retorna a moda (valor mais frequente)."""
    try:
        return st.mode(dados)
    except st.StatisticsError:
        # Fallback caso haja múltiplas modas e a versão do Python seja antiga
        contagens = {x: dados.count(x) for x in set(dados)}
        return max(contagens, key=contagens.get)

# ==========================================
# Q05: MEDIDAS DE DISPERSÃO
# ==========================================

def calcular_dispersao(dados):
    """Calcula Amplitude, Variância (populacional), Desvio-Padrão e CV."""
    media = calcular_media(dados)
    
    amplitude = max(dados) - min(dados)
    variancia = st.pvariance(dados)  # pvariance divide por N (conforme material)
    desvio_padrao = st.pstdev(dados)
    coef_variacao = (desvio_padrao / media) * 100 if media != 0 else 0
    
    return {
        "Amplitude": amplitude,
        "Variancia": variancia,
        "Desvio_Padrao": desvio_padrao,
        "Coeficiente_Variacao_Perc": coef_variacao
    }

# ==========================================
# Q06: FILTRAGEM DE OUTLIERS
# ==========================================

def gerenciar_outliers(dados, acao='ambos'):
    """
    Identifica e remove outliers.
    acao: 'moderados', 'extremos', 'ambos' ou 'identificar' (apenas lista os outliers).
    """
    q1, _, q3 = calcular_quartis(dados)
    aiq = q3 - q1
    
    lim_inf_mod, lim_sup_mod = q1 - 1.5 * aiq, q3 + 1.5 * aiq
    lim_inf_ext, lim_sup_ext = q1 - 3.0 * aiq, q3 + 3.0 * aiq
    
    dados_limpos = []
    outliers_mod = []
    outliers_ext = []
    
    for x in dados:
        is_extremo = x < lim_inf_ext or x > lim_sup_ext
        is_moderado = (x < lim_inf_mod or x > lim_sup_mod) and not is_extremo
        
        if is_extremo:
            outliers_ext.append(x)
        if is_moderado:
            outliers_mod.append(x)
            
        # Lógica de remoção
        if acao == 'ambos' and (is_extremo or is_moderado): continue
        if acao == 'extremos' and is_extremo: continue
        if acao == 'moderados' and is_moderado: continue
            
        dados_limpos.append(x)
        
    if acao == 'identificar':
        return {"Moderados": outliers_mod, "Extremos": outliers_ext}
        
    return dados_limpos

# ==========================================
# Q08: HISTOGRAMA
# ==========================================

def parametros_histograma(dados):
    """Retorna o número de classes (Sturges) e o tamanho da classe."""
    n = len(dados)
    amplitude = max(dados) - min(dados)
    
    k = round(1 + 3.3 * math.log10(n))
    h = amplitude / k
    
    return {"Numero_Classes": k, "Tamanho_Classe": h}

# ==========================================
# Q09: TESTE DE ADERÊNCIA K-S COMPLETO
# ==========================================

# -- Funções de Distribuição Acumulada (CDF) --
def cdf_uniforme(x, a, b):
    if x < a: return 0.0
    if x > b: return 1.0
    return (x - a) / (b - a)

def cdf_exponencial(x, lambd):
    if x < 0: return 0.0
    return 1.0 - math.exp(-lambd * x)

def cdf_normal(x, mu, sigma):
    # Usando a função Erro (math.erf) nativa para a CDF exata da Normal
    if sigma == 0: return 1.0 if x >= mu else 0.0
    return (1.0 + math.erf((x - mu) / (sigma * math.sqrt(2.0)))) / 2.0

def cdf_lognormal(x, mu_log, sigma_log):
    if x <= 0: return 0.0
    if sigma_log == 0: return 1.0 if math.log(x) >= mu_log else 0.0
    return (1.0 + math.erf((math.log(x) - mu_log) / (sigma_log * math.sqrt(2.0)))) / 2.0

def cdf_triangular(x, a, m, b):
    if x <= a: return 0.0
    if x >= b: return 1.0
    if x <= m:
        return ((x - a) ** 2) / ((b - a) * (m - a))
    return 1.0 - (((b - x) ** 2) / ((b - a) * (b - m)))

def teste_aderencia_ks(dados, alpha=0.05):
    """Realiza o Teste Kolmogorov-Smirnov para as distribuições do material."""
    dados_ord = sorted(dados)
    n = len(dados)
    
    # Estimação dos parâmetros da amostra
    media = calcular_media(dados)
    desvio = st.pstdev(dados)
    minimo, maximo = min(dados), max(dados)
    moda = calcular_moda(dados)
    
    lambd = 1.0 / media if media > 0 else 0
    dados_log = [math.log(x) for x in dados if x > 0]
    mu_log = calcular_media(dados_log) if dados_log else 0
    sigma_log = st.pstdev(dados_log) if dados_log else 1
    
    # Contagem de frequências e valores únicos
    frequencias = {x: dados_ord.count(x) for x in set(dados_ord)}
    valores_unicos = sorted(frequencias.keys())
    
    distribuicoes = {
        'Uniforme': lambda x: cdf_uniforme(x, minimo, maximo),
        'Exponencial': lambda x: cdf_exponencial(x, lambd),
        'Normal': lambda x: cdf_normal(x, media, desvio),
        'Lognormal': lambda x: cdf_lognormal(x, mu_log, sigma_log),
        'Triangular': lambda x: cdf_triangular(x, minimo, moda, maximo)
    }
    
    resultados = {}
    d_critico = 1.36 / math.sqrt(n) # Fórmula para alpha=0.05 e n>40
    
    for nome, cdf_func in distribuicoes.items():
        maior_d = 0.0
        freq_acumulada = 0
        
        for x in valores_unicos:
            freq_acumulada += frequencias[x]
            faon = freq_acumulada / n  # Freq. Acumulada Observada Normalizada
            fatn = cdf_func(x)         # Freq. Acumulada Teórica Normalizada
            
            d = abs(faon - fatn)
            if d > maior_d:
                maior_d = d
                
        resultados[nome] = {
            "D_Max": maior_d,
            "Adere": maior_d < d_critico
        }
        
    return {"D_Critico": d_critico, "Resultados": resultados}

# ==========================================
# TESTE (EXECUÇÃO)
# ==========================================
if __name__ == "__main__":
    amostra = utils.load_dataset("entrada-lista-1.txt")
    
    # 1. Identificar Outliers
    print("--- ANÁLISE DE OUTLIERS ---")
    outliers = gerenciar_outliers(amostra, acao='identificar')
    print(f"Moderados encontrados: {outliers['Moderados']}")
    print(f"Extremos encontrados: {outliers['Extremos']}")
    
    # Escolhendo remover apenas o outlier extremo
    amostra_limpa = gerenciar_outliers(amostra, acao='extremos')
    print(f"Tamanho da amostra após remover extremos: {len(amostra_limpa)}\n")
    
    # 2. Estatística Descritiva 
    print("--- ESTATÍSTICA DESCRITIVA ---")
    print(f"Média: {calcular_media(amostra_limpa):.2f}")
    q1, q2, q3 = calcular_quartis(amostra_limpa)
    print(f"Quartis -> Q1: {q1}, Mediana(Q2): {q2}, Q3: {q3}")
    
    disp = calcular_dispersao(amostra_limpa)
    print(f"Amplitude: {disp['Amplitude']}")
    print(f"Variância: {disp['Variancia']:.2f}")
    print(f"Desvio-Padrão: {disp['Desvio_Padrao']:.2f}")
    print(f"CV: {disp['Coeficiente_Variacao_Perc']:.2f}%\n")
    
    # 3. Histograma
    print("--- PARÂMETROS DO HISTOGRAMA ---")
    hist = parametros_histograma(amostra_limpa)
    print(f"Número de Classes (K): {hist['Numero_Classes']}")
    print(f"Tamanho da Classe (h): {hist['Tamanho_Classe']:.2f}\n")
    
    # 4. Teste de Aderência
    print("--- TESTE DE ADERÊNCIA K-S (alpha = 0.05) ---")
    ks = teste_aderencia_ks(amostra_limpa)
    print(f"D Crítico: {ks['D_Critico']:.4f}\n")
    
    for dist, dados_teste in ks['Resultados'].items():
        status = "ADERENTE" if dados_teste['Adere'] else "NÃO ADERENTE"
        print(f"{dist.ljust(15)}: D = {dados_teste['D_Max']:.4f} -> {status}")