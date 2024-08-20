from fastapi import FastAPI, File
from pydantic import BaseModel
import xgboost as xgb
import numpy as np
import pickle
import warnings
import base64
from PIL import Image
import io

warnings.simplefilter(action='ignore', category=DeprecationWarning)

app = FastAPI()

#Definição dos tipos de dados
class PredictionResponse(BaseModel):
  prediction: float

class Imagerequest(BaseModel):
  image: str

#Carregamento do Modelo de Machine Learning
def load_model():
  global xgb_model_carregado
  with open("xgboost_model.pkl", "rb") as f:
    xgb_model_carregado = pickle.load(f)

#Inicialização da Aplicação
@app.on_event("startup")
async def startup_event():
  load_model()

@app.post("/predict", response_model=PredicitionResponse)
async def predict(request: ImageRequest):
        img_bytes = base64.b64decode(request.image)
        img = Image.open(io.BytesIO(img_bytes))
        img = img.resize((8,8))
        img_array = np.array(img)

        img_array=np.dot(img_array[...,:3], [0.2989, 0.58870, 0.1140])

        img_array = img_array.reshape(1,-1)

        prediction = xgb_model_carregado.predict(img_array)

        return {"predictino": prediction}
#Endpoint de Healthcheck
@app.get("/healthcheck")
async def healthcheck():
  #retorna um objeto com um campo status com valor "ok" se a aplicação estiver funcionando corretamente
  return {"status": "ok"}
