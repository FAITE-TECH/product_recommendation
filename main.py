from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
item_similarity_df = joblib.load("item_similarity.pkl")


class ItemRequest(BaseModel):
    item: str
    num: int = 5


@app.post("/recommend")
def recommend_items(request: ItemRequest):
    item = request.item
    num = request.num

    if item not in item_similarity_df:
        return {"message": f"Item '{item}' not found."}

    recommendations = item_similarity_df[item].sort_values(ascending=False).iloc[1:num+1].index.tolist()
    return {"item": item, "recommendations": recommendations}
