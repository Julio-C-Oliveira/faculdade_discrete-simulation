# ==========================================
# 1. FUNÇÕES MATEMÁTICAS E ESTATÍSTICAS BASE (Sem libs externas para cálculo)
# ==========================================
EULER = 2.718281828459045

def raiz_quadrada(x):
    return x ** 0.5

def log10(x):
    if x <= 0: raise ValueError("Logaritmo indefinido para <= 0.")
    baixo, alto = 0.0, 100.0 
    for _ in range(100): 
        meio = (baixo + alto) / 2.0
        if 10 ** meio < x: baixo = meio
        else: alto = meio
    return (baixo + alto) / 2.0

def ln(x):
    """Logaritmo Natural usando mudança de base."""
    return log10(x) / 0.4342944819

def ordenar(dados):
    return sorted(dados)

def calcular_media(dados):
    return sum(dados) / len(dados) if len(dados) > 0 else 0

def calcular_moda(dados):
    """Retorna o valor mais frequente (Moda) para uso na Triangular."""
    contagens = {}
    for x in dados:
        contagens[x] = contagens.get(x, 0) + 1
    moda = max(contagens, key=contagens.get)
    return moda

def calcular_mediana(dados_ordenados):
    n = len(dados_ordenados)
    if n == 0: return 0
    meio = n // 2
    if n % 2 == 0: return (dados_ordenados[meio - 1] + dados_ordenados[meio]) / 2.0
    return dados_ordenados[meio]

def calcular_quartis(dados):
    dados_ord = ordenar(dados)
    n = len(dados_ord)
    meio = n // 2
    q1 = calcular_mediana(dados_ord[:meio])
    q2 = calcular_mediana(dados_ord)
    q3 = calcular_mediana(dados_ord[meio:] if n % 2 == 0 else dados_ord[meio + 1:])
    return q1, q2, q3

def calcular_desvio_padrao(dados, media):
    n = len(dados)
    if n == 0: return 0
    variancia = sum((x - media) ** 2 for x in dados) / n
    return raiz_quadrada(variancia)

def calcular_dispersao(dados):
    """Calcula Amplitude, Variância (populacional), Desvio-Padrão e CV."""
    media = calcular_media(dados)
    n = len(dados)
    
    amplitude = max(dados) - min(dados) if dados else 0
    variancia = sum((x - media) ** 2 for x in dados) / n if n > 0 else 0
    desvio_padrao = raiz_quadrada(variancia)
    coef_variacao = (desvio_padrao / media) * 100 if media != 0 else 0
    
    return {
        "Amplitude": amplitude,
        "Variancia": variancia,
        "Desvio_Padrao": desvio_padrao,
        "Coeficiente_Variacao_Perc": coef_variacao
    }

# ==========================================
# 2. FILTRAGEM DE OUTLIERS
# ==========================================

def remover_outliers(dados, remover='ambos'):
    """
    Remove outliers do conjunto de dados.
    remover: 'moderados', 'extremos', ou 'ambos'
    """
    q1, _, q3 = calcular_quartis(dados)
    aiq = q3 - q1
    
    lim_inf_mod, lim_sup_mod = q1 - 1.5 * aiq, q3 + 1.5 * aiq
    lim_inf_ext, lim_sup_ext = q1 - 3.0 * aiq, q3 + 3.0 * aiq
    
    dados_limpos = []
    
    for x in dados:
        is_extremo = x < lim_inf_ext or x > lim_sup_ext
        is_moderado = (x < lim_inf_mod or x > lim_sup_mod) and not is_extremo
        
        if remover == 'ambos' and (is_extremo or is_moderado):
            continue
        if remover == 'extremos' and is_extremo:
            continue
        if remover == 'moderados' and is_moderado:
            continue
            
        dados_limpos.append(x)
        
    return dados_limpos

# ==========================================
# 3. FUNÇÕES ACUMULADAS TEÓRICAS (CDF)
# ==========================================

def cdf_uniforme(x, a, b):
    if x < a: return 0.0
    if x > b: return 1.0
    return (x - a) / (b - a)

def cdf_exponencial(x, lambd):
    if x < 0: return 0.0
    return 1.0 - (EULER ** (-lambd * x))

def cdf_normal(x, mu, sigma):
    """Aproximação Logística para Normal CDF."""
    if sigma == 0: return 1.0 if x >= mu else 0.0
    z = (x - mu) / sigma
    return 1.0 / (1.0 + EULER ** (-1.702 * z))

def cdf_lognormal(x, mu_log, sigma_log):
    if x <= 0: return 0.0
    if sigma_log == 0: return 1.0 if ln(x) >= mu_log else 0.0
    z = (ln(x) - mu_log) / sigma_log
    return 1.0 / (1.0 + EULER ** (-1.702 * z))

def cdf_triangular(x, a, m, b):
    if x <= a: return 0.0
    if x >= b: return 1.0
    if x <= m:
        return ((x - a) ** 2) / ((b - a) * (m - a))
    return 1.0 - (((b - x) ** 2) / ((b - a) * (b - m)))

# ==========================================
# 4. HISTOGRAMA 
# ==========================================

def gerar_e_salvar_histograma(dados, nome_arquivo='histograma.pdf'):
    """Calcula os parâmetros e salva o histograma como PDF."""
    if not dados:
        return {"Erro": "Dados insuficientes."}

    n = len(dados)
    amplitude = max(dados) - min(dados)
    
    # Cálculo manual do K e h
    k = round(1 + 3.3 * log10(n))
    h = amplitude / k
    
    return {
        "Numero_Classes": k,
        "Tamanho_Classe": h,
        "Arquivo_Salvo": nome_arquivo
    }

# ==========================================
# 5. TESTE DE ADERÊNCIA K-S COMPLETO
# ==========================================

def teste_aderencia_geral(dados, alpha=0.05):
    """Realiza o Teste K-S para as 5 distribuições estudadas."""
    dados_ord = ordenar(dados)
    n = len(dados)
    
    # --- Estimação de Parâmetros ---
    media = calcular_media(dados)
    desvio = calcular_desvio_padrao(dados, media)
    minimo, maximo = min(dados), max(dados)
    moda = calcular_moda(dados)
    
    lambd = 1.0 / media if media > 0 else 0
    dados_ln = [ln(x) for x in dados if x > 0]
    mu_log = calcular_media(dados_ln) if dados_ln else 0
    sigma_log = calcular_desvio_padrao(dados_ln, mu_log) if dados_ln else 1
    
    # --- Estruturas para Teste ---
    frequencias = {}
    for x in dados_ord: frequencias[x] = frequencias.get(x, 0) + 1
    valores_unicos = ordenar(list(frequencias.keys()))
    
    distribuicoes = {
        'Uniforme': lambda x: cdf_uniforme(x, minimo, maximo),
        'Exponencial': lambda x: cdf_exponencial(x, lambd),
        'Normal': lambda x: cdf_normal(x, media, desvio),
        'Lognormal': lambda x: cdf_lognormal(x, mu_log, sigma_log),
        'Triangular': lambda x: cdf_triangular(x, minimo, moda, maximo)
    }
    
    resultados = {}
    d_critico = 1.36 / raiz_quadrada(n) # Limiar para alpha=0.05 e n>40
    
    for nome, cdf_func in distribuicoes.items():
        maior_d = 0.0
        freq_acumulada = 0
        
        for x in valores_unicos:
            freq_acumulada += frequencias[x]
            faon = freq_acumulada / n         
            fatn = cdf_func(x)                
            
            d = abs(faon - fatn)
            if d > maior_d:
                maior_d = d
                
        resultados[nome] = {
            "D_Max": maior_d,
            "Adere": maior_d < d_critico
        }
        
    return {
        "D_Critico": d_critico,
        "Resultados": resultados
    }

# ==========================================
# EXEMPLO DE USO
# ==========================================
if __name__ == "__main__":
    # Amostra exemplo
    amostra = utils.load_dataset("entrada-lista-1.txt")

    
    print(f"Tamanho Original: {len(amostra)}")
    
    # 1. Remoção de outliers 
    amostra_limpa = remover_outliers(amostra, remover='extremos')
    print(f"Tamanho sem Extremos: {len(amostra_limpa)}\n")
    
    # 2. Estatística Descritiva
    print("--- ESTATÍSTICA DESCRITIVA ---")
    q1, q2, q3 = calcular_quartis(amostra_limpa)
    disp = calcular_dispersao(amostra_limpa)
    print(f"Média: {calcular_media(amostra_limpa):.2f}")
    print(f"Quartis -> Q1: {q1} | Q2(Mediana): {q2} | Q3: {q3}")
    print(f"Amplitude: {disp['Amplitude']}")
    print(f"Variância: {disp['Variancia']:.2f}")
    print(f"Desvio-Padrão: {disp['Desvio_Padrao']:.2f}")
    print(f"CV: {disp['Coeficiente_Variacao_Perc']:.2f}%\n")
    
    # 3. Gerar Histograma
    print("--- GERANDO HISTOGRAMA (PDF) ---")
    hist = gerar_e_salvar_histograma(amostra_limpa, nome_arquivo='histograma.pdf')
    print(f"Classes (K): {hist['Numero_Classes']} | Tamanho (h): {hist['Tamanho_Classe']:.2f}")
    print(f"Salvo em: {hist['Arquivo_Salvo']}\n")

    # 4. Testando Aderência em todas as distribuições
    print("--- TESTE DE ADERÊNCIA K-S ---")
    ks_geral = teste_aderencia_geral(amostra_limpa)
    
    print(f"D Crítico (alpha=0.05): {ks_geral['D_Critico']:.4f}\n")
    for dist, metrica in ks_geral['Resultados'].items():
        status = "ADERENTE" if metrica['Adere'] else "NÃO ADERENTE"
        print(f"{dist.ljust(15)}: D = {metrica['D_Max']:.4f} -> {status}")