# Wallet-Risk-Scoring-from-Scratch
queries crypto subgraphs for details of a list of 100 wallets , uses heuristic based scoring for risk ( 1 being safest and 1000 being riskiest) and then trains a XGboost model for final predictive scoring. 

--- 

# Note : For Scoring ***1 is BEST*** and ***1000 is RISKIEST***

---

### Workflow : 

```mermaid
flowchart TD
    A[Start Input Wallet List]
    B[Introspect V2 and V3 Schemas]
    C{Is Data Available}
    D[Query V2 Subgraph Collect Data]
    E[Drop V3 Use V2 Only]
    F[Feature Engineering]
    G[engineered feature data csv]
    H[EDA Data Exploration]
    I[Data Cleaning and Preprocessing]
    J[engineered features cleaned csv]
    K[Heuristic Risk Scoring]
    L[engineered features with scores csv]
    M[Train ML Models XGBoost LightGBM RF]
    N{Select Best Model}
    O[Train Final XGBoost Model]
    P[Predict Model Scores]
    Q[final predictions csv]
    R[End Deliverable Risk Scores]

    A --> B
    B --> C
    C -- Yes V2 --> D
    C -- No V3 --> E
    D --> F
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    N -- XGBoost Best --> O
    O --> P
    P --> Q
    Q --> R

```
