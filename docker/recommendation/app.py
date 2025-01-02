import pandas as pd, os

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Create a recommendation model"}

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
    
    frequent_itemsets = apriori(transactions_df, use_colnames=True, min_support=0.1, max_len=2)
    rules = association_rules(frequent_itemsets, num_itemsets=len(frequent_itemsets), metric="lift")
    supports = rules[rules['consequent support'] >= 0.1][['antecedents', 'consequents', 'consequent support']]
    sortValues = supports.sort_values(by='consequent support', ascending=False).reset_index()
    sortValues["antecedents"] = sortValues["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    sortValues["consequents"] = sortValues["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    sortValues["consequent support"] = sortValues["consequent support"].apply(lambda x: round(x, 2))
    
    filename = '/data/csv_model.csv'
    sortValues.to_csv(filename)

@app.get("/create_recommendation_model")
def initialize_recommendation():
    filename = '/data/2023_spotify_ds1.csv'
    with open(filename, encoding="utf8") as file:
        df = pd.read_csv(file)
    print(df.iloc[:3])
    create_recommendation_model(df)
    # except:
    #     return 'Error creating recommendation model'
    # return 'Sucess creating recommendation model'
    return ''

@app.get("/update_recommendation_model")
def retrain_recommendation():
    try:
        filename = '/data/2023_spotify_ds2.csv'
        with open(filename, encoding="utf8") as file:
            df = pd.read_csv(file)

        create_recommendation_model(df)
    except:
        return 'Error re-training recommendation model'
    return 'Sucess re-training recommendation model'