from utils.database import get_database
import pandas as pd

def load_data():
    db = get_database()
    collection = db["economic_data"]
    records = list(collection.find().sort([("Year", 1), ("Month", 1)]))
    if records:
        data = pd.DataFrame(records)
        data = data.drop(columns=["_id"])

        return data
    return pd.DataFrame()

