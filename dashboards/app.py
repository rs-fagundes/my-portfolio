import streamlit as st
import pandas as pd

st.title("Incrementality Analysis Tool 📈")

# Upload do CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview do arquivo:")
    st.dataframe(df.head())

    # Escolher coluna de Segmento (grupo)
    group_col = st.selectbox("Selecione a coluna de Segmento (grupo)", df.columns)

    # Converter métricas numéricas (exemplo)
    metric_cols = st.multiselect(
        "Selecione as métricas para comparar",
        df.select_dtypes(include="number").columns.tolist(),
    )

    # Calcular agregados por grupo
    if group_col and metric_cols:
        grouped = df.groupby(group_col)[metric_cols].sum().reset_index()
        st.subheader("Valores agregados por grupo:")
        st.dataframe(grouped)

        # Supondo dois grupos: controle e teste
        if grouped.shape[0] == 2:
            base = grouped.iloc[0]
            test = grouped.iloc[1]

            inc_data = {
                "Metric": [],
                "Group 1": [],
                "Group 2": [],
                "Incrementality (Abs)": [],
                "Incrementality (%)": [],
            }

            for col in metric_cols:
                val_1 = base[col]
                val_2 = test[col]
                inc_data["Metric"].append(col)
                inc_data["Group 1"].append(val_1)
                inc_data["Group 2"].append(val_2)
                inc_data["Incrementality (Abs)"].append(val_2 - val_1)
                inc_data["Incrementality (%)"].append(
                    round(100 * (val_2 - val_1) / val_1, 2) if val_1 else None
                )

            st.subheader("Incrementality Result:")
            st.dataframe(pd.DataFrame(inc_data))
        else:
            st.warning(
                "O dataset precisa ter exatamente 2 grupos distintos para comparar."
            )
