from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import joblib
import pandas as pd


app = FastAPI()


class WineFeatures(BaseModel):
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315_of_diluted_wines: float
    proline: float


forest_pipeline = joblib.load("./models/random_forest_pipeline.joblib")
encoder = joblib.load("./models/label_encoder.joblib")


@app.get('/')
def home():
    return {"Status Health": "Ok"}


@app.post('/predict_random_forest')
def random_forest_prediction(data: WineFeatures):
    # Convert model to a dictionary and then a dataframe
    df = pd.DataFrame([data.model_dump()])

    # Make predictions
    prediction = forest_pipeline.predict(df)

    # convert prediction to an int instead of an array
    prediction = int(prediction[0])

    # Decode using our encoder
    prediction = encoder.inverse_transform([prediction])[0]

    # Extract probabilities
    probability = forest_pipeline.predict_proba(df)

    # Convert probabilities to a list
    probabilities = probability.tolist()

    return {'Prediction': prediction, 'probabilities': probabilities}


@app.get('/documents')
def documentation():
    return {'description': 'All documentation'}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
