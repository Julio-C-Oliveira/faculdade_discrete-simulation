01. Para que serve a aplicação de simulações? Em que contextos há vantagens em se utilizar simulações? Há desvantagens nesse tipo de abordagem?

    Finalidade e contextos da simulação: A simulação serve para a experimentação de um sistema real através de modelos, permitindo avaliar mudanças e o impacto de decisões sem interferir no sistema verdadeiro.
    - As vantagens incluem a capacidade de prever resultados, considerar variações aleatórias do sistema, estimular a criatividade na resolução de problemas e ser financeiramente viável
    - As desvantagens e limitações são que ela não prevê o futuro, não é uma fórmula matemática exata, não é uma ferramenta de otimização estrita e não substitui o processo humano de tomada de decisão.

02. Em termos estatísticos, o que significa “média”? Comente sobre as utilizações e os problemas relacionados com os usos.

    Significado estatístico de “média”: A média (ou média aritmética) é a soma dos valores de todos os elementos dividida pela quantidade de elementos, identificando o comportamento central ou médio do conjunto. Seus principais problemas estão relacionados à sensibilidade a outliers (valores discrepantes), que podem distorcer o resultado, tornando a média pouco representativa da maioria dos dados do conjunto.

03. Indique as fórmulas de cálculo da “mediana” e de que maneira o valor divide o conjunto de dados.

    Mediana e sua divisão do conjunto: A mediana é o valor que divide o conjunto de dados exatamente ao meio, criando dois subconjuntos onde 50% dos elementos são menores ou iguais a ela e 50% são maiores ou iguais.
    - Fórmula para n ímpar: É o valor do elemento que ocupa a posição central do conjunto ordenado.
    - Fórmula para n par: É a média aritmética entre os dois elementos centrais do conjunto ordenado.

04. Calcule os “quartis” 1, 2 e 3 do conjunto de dados.

    Quartis do conjunto de dados (exemplo das fontes): Com base no conjunto de 200 observações analisado nas fontes, os quartis calculados são:
    - Quartil 1 (Q1): 2
    - Quartil 2 (Q2/Mediana): 5
    - Quartil 3 (Q3): 9

05. Calcule, para o conjunto de dados, as seguintes medidas de dispersão:
    a. Amplitude: 728
    b. Variância: 2.643,81
    c. Desvio-Padrão: 51,41
    d. Coeficiente de Variação: 492,74% 

06.  O que é um “outlier” de um conjunto de dados? Há outliers no conjunto disponibilizado como exemplo? Indique os cálculos utilizados para a avaliação

    Outliers e avaliação no exemplo: Um outlier é um dado não usual ou discrepante em um conjunto. No exemplo das fontes, existem 11 outliers moderados e 2 outliers extremos (os valores 43 e 728). A avaliação é feita usando a Amplitude Interquartil (A = Q3 - Q1):
    - Moderado: valor < Q1−1,5A ou valor > Q3+1,5A.
    - Extremo: valor < Q1−3A ou valor > Q3+3A.

07. O que pode provocar a ocorrência de um “outlier”?

    Causas da ocorrência de um outlier: As razões mais comuns são erros na coleta de dados (falhas em sensores ou erros humanos na anotação e tabulação) ou a ocorrência real de eventos raros e inesperados durante a medição do fenômeno.

08. Crie o histograma do conjunto de dados, destacando o número de classes e o tamanho de cada classe.

    Histograma do conjunto de dados: Para o exemplo (após remover o outlier 728, restando 199 observações):
    -  Número de classes (K): Aproximadamente 9, calculado pela fórmula K=1+3,3log10n.
    - Tamanho de cada classe (h): Aproximadamente 4,8, obtido pela divisão da amplitude (43) pelo número de classes (9).

09. Dada as distribuições estudadas e o histograma da questão anterior, quais das distribuições mais adere ao conjunto de dados do exemplo?

    Distribuição com maior aderência: A partir da análise visual e do teste matemático de Kolmogorov-Smirnov (KS), a distribuição que mais adere ao conjunto de dados do exemplo é a Exponencial

10. Crie o modelo conceitual ACD independente para cada entidade e a integração entre eles para a seguinte descrição:
    Em um supermercado, os clientes fazem uma fila para serem atendidos nos caixas. Assim que algum caixa finaliza o atendimento, o cliente segue para fora da loja enquanto um outro cliente, que aguardava na fila, se encaminha para iniciar o atendimento.

    Modelo conceitual ACD (Supermercado): O diagrama integra o ciclo de vida das entidades Cliente e Caixa.
    - Ciclo do Cliente: Fila (Espera Atendimento) → Atividade (Atendimento no Caixa) → Fila (Fora da Loja).
    - Ciclo do Caixa: Fila (Livre) → Atividade (Atendimento no Caixa) → Fila (Livre)
    - Integração: A atividade central "Atendimento no Caixa" requer a presença simultânea de um cliente na fila e a disponibilidade de um caixa livre


11. Para o modelo da questão anterior, realize a simulação de três fases para a seguinte entrada de dados, em um sistema onde existem 2 caixas disponíveis:

    T=0: O Cliente 1 chega. O Caixa 1 inicia o atendimento de C1 (término previsto para T=3).
    T=1: Os Clientes 2 e 3 chegam. O Caixa 2 inicia o atendimento de C2 (término em T=5). O Cliente 3 entra na fila.
    T=2: O Cliente 4 chega e entra na fila atrás de C3.
    T=3: O Caixa 1 termina o atendimento de C1 e inicia imediatamente o de C3 (término em 3+6=T=9).
    T=5: O Caixa 2 termina o atendimento de C2 e inicia o de C4 (término em 5+4=T=9).
    T=9: Os atendimentos de C3 e C4 são finalizados simultaneamente, encerrando a simulação para esta entrada.