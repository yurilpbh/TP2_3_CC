import pandas as pd, os

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Recommendation"}

def create_recommendation_model(df: pd.DataFrame):
    df = df.filter(items=['album_name','artist_name','duration_ms','pid','track_name'])
    grouped = (
        df.groupby("pid")
        .apply(lambda x: [f"{s}" for v, s in zip(x["artist_name"], x["track_name"])])
        .reset_index(name="Values")
    )
    itemSetList = grouped["Values"].to_list()

    # Gera tabela one hot encondig atraves da matriz computada anteriormente
    te = TransactionEncoder()
    te_ary = te.fit(itemSetList).transform(itemSetList, sparse=True)
    transactions_df = pd.DataFrame.sparse.from_spmatrix(te_ary, columns=te.columns_)

    frequent_itemsets = apriori(transactions_df, use_colnames=True, min_support=0.03, max_len=2)
    rules = association_rules(frequent_itemsets, num_itemsets=len(frequent_itemsets), metric="lift")
    supports = rules[rules['consequent support'] >= 0.1][['antecedents', 'consequents', 'consequent support']]
    sortValues = supports.sort_values(by='consequent support', ascending=False).reset_index()
    sortValues["antecedents"] = sortValues["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    sortValues["consequents"] = sortValues["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    sortValues["consequent support"] = sortValues["consequent support"].apply(lambda x: round(x, 2))
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './csv_model.csv')
    sortValues.to_csv(filename)

@app.get("/create_recommendation_model")
def initialize_recommendation():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../dataset/2023_spotify_ds1.csv.csv')
    with open(filename, encoding="utf8") as file:
        df = pd.read_csv(file)
    
    create_recommendation_model(df)

@app.get("/update_recommendation_model")
def retrain_recommendation():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../dataset/2023_spotify_ds2.csv.csv')
    with open(filename, encoding="utf8") as file:
        df = pd.read_csv(file)

    create_recommendation_model(df)