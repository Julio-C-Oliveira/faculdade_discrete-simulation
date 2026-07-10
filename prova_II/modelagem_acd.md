```mermaid
graph LR
    %% Definições de Estilo para o Padrão ACD (Corrigidas para texto preto e negrito)
    classDef queue fill:#f4f6f7,stroke:#7f8c8d,stroke-width:2px,color:#000000,font-weight:bold;
    classDef activity fill:#e8f8f5,stroke:#1abc9c,stroke-width:2px,color:#000000,font-weight:bold;
    classDef resource fill:#fef9e7,stroke:#f1c40f,stroke-width:2px,color:#000000,font-weight:bold;
    classDef system fill:#eaecee,stroke:#2c3e50,stroke-dasharray:5 5,color:#000000,font-weight:bold;

    %% --- RECURSOS DO SISTEMA (Centralizados dinamicamente entre os fluxos) ---
    R_PistasP(["Pistas Pequenas<br><b>(Disp: 2)</b>"])
    R_PistasG(["Pista Grande<br><b>(Disp: 1)</b>"])
    R_Plat(["Plataformas de Emb/Desemb<br><b>(Disp: 5)</b>"])
    R_Hangares(["Hangares de Preparação<br><b>(Disp: 3)</b>"])

    %% --- FLUXO LINEAR: AERONAVES DE PEQUENO PORTE (P) ---
    ChegadaP[Horário Chegada P] --> F_PousoP(("Fila Pouso P"))
    F_PousoP --> A_PousoP["Pouso P<br><b>(40 min)</b>"]
    A_PousoP --> F_DesembP(("Fila Desemb P"))
    F_DesembP --> A_DesembP["Desembarque P<br><b>(20 min)</b>"]
    A_DesembP --> F_HangarP(("Fila Hangar P"))
    F_HangarP --> A_HangarP["Hangar P<br><b>(Preparo)</b>"]
    A_HangarP --> F_EmbP(("Fila Embarque P"))
    F_EmbP --> A_EmbP["Embarque P<br><b>(30 min)</b>"]
    A_EmbP --> F_DecolP(("Fila Decolagem P"))
    F_DecolP --> A_DecolP["Decolagem P<br><b>(40 min)</b>"]
    A_DecolP --> SaidaP([Saída do Sistema P])

    %% --- FLUXO LINEAR: AERONAVES DE GRANDE PORTE (G) ---
    ChegadaG[Horário Chegada G] --> F_PousoG(("Fila Pouso G"))
    F_PousoG --> A_PousoG["Pouso G<br><b>(60 min)</b>"]
    A_PousoG --> F_DesembG(("Fila Desemb G"))
    F_DesembG --> A_DesembG["Desembarque G<br><b>(40 min)</b>"]
    A_DesembG --> F_HangarG(("Fila Hangar G"))
    F_HangarG --> A_HangarG["Hangar G<br><b>(Preparo)</b>"]
    A_HangarG --> F_EmbG(("Fila Embarque G"))
    F_EmbG --> A_EmbG["Embarque G<br><b>(60 min)</b>"]
    A_EmbG --> F_DecolG(("Fila Decolagem G"))
    F_DecolG --> A_DecolG["Decolagem G<br><b>(60 min)</b>"]
    A_DecolG --> SaidaG([Saída do Sistema G])

    %% --- INTERAÇÕES DE RECURSOS (Alocação e Liberação Simplificadas) ---
    %% Uso das Pistas
    A_PousoP <-->|Usa Pista P| R_PistasP
    A_DecolP <-->|Usa Pista P| R_PistasP
    A_PousoG <-->|Usa Pista G| R_PistasG
    A_DecolG <-->|Usa Pista G| R_PistasG

    %% Uso das Plataformas Compartilhadas
    A_DesembP <-->|Usa Plataforma| R_Plat
    A_EmbP <-->|Usa Plataforma| R_Plat
    A_DesembG <-->|Usa Plataforma| R_Plat
    A_EmbG <-->|Usa Plataforma| R_Plat

    %% Uso dos Hangares Compartilhados
    A_HangarP <-->|Usa Hangar| R_Hangares
    A_HangarG <-->|Usa Hangar| R_Hangares

    %% Aplicação das Classes de Estilo (Cores Claras Padrão ACD)
    class F_PousoP,F_DesembP,F_HangarP,F_EmbP,F_DecolP,F_PousoG,F_DesembG,F_HangarG,F_EmbG,F_DecolG queue;
    class A_PousoP,A_DesembP,A_HangarP,A_EmbP,A_DecolP,A_PousoG,A_DesembG,A_HangarG,A_EmbG,A_DecolG activity;
    class R_PistasP,R_PistasG,R_Plat,R_Hangares resource;
    class ChegadaP,ChegadaG,SaidaP,SaidaG system;