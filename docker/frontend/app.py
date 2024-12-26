import pandas as pd, os

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class Song(BaseModel):
    songs: list

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
    return {"message": "Recommendation"}

@app.post("/get_recommendation")
def get_recommendation(songs: Song):
    songs = songs['songs']
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../dataset/csv_model.csv')
    df = pd.read_csv(filename)
    songs_recommendation = []
    df_recommendation = pd.DataFrame()
    for song in songs:
        df_songs = df[df['antecedents'].str.lower() == song.lower()]
        df_recommendation = pd.concat([df_recommendation, df_songs])
        songs_recommendation.append(df_songs['consequents'].tolist())
    
    # Use set intersection to find common elements
    common_elements = set(songs_recommendation[0])
    for sublist in songs_recommendation[1:]:
        common_elements &= set(sublist)
    
    if len(common_elements) < 5:
        df = df[~df['consequents'].str.lower().isin(songs)]
        common_elements.update(df.sort_values('consequent support', ascending=False)['consequents'][0:(5-len(common_elements))].to_list())

    return {
        "songs": songs,
        "version": 1,
        "model_date": "2024-12-12",
    }


if __name__ == '__main__':
    app.run(debug=True)
