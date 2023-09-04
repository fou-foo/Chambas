from fastapi import FastAPI, HTTPException
from typing import Union, Optional
# BaseModel from Pydantic is used to define data objects
from pydantic import BaseModel
import pandas as pd
import os
import pickle
import joblib
from modelos import process_data


# Declare the data object with its components and their type.
class InputData(BaseModel):
    MONTHS_BALANCE: int
    CNT_CHILDREN: int
    AMT_INCOME_TOTAL: float
    DAYS_EMPLOYED: int
    CNT_FAM_MEMBERS: int
    CODE_GENDER: str
    FLAG_OWN_CAR: str
    FLAG_OWN_REALTY: str
    NAME_INCOME_TYPE: str
    NAME_EDUCATION_TYPE: str
    NAME_FAMILY_STATUS: str
    NAME_HOUSING_TYPE: str
    FLAG_WORK_PHONE: str
    FLAG_EMAIL: str
    FLAG_PHONE: str

    class Config:
        schema_extra = {
            "example": {
                'MONTHS_BALANCE': -17,
                'CNT_CHILDREN': 0,
                'AMT_INCOME_TOTAL': 165000.0,
                'DAYS_EMPLOYED': -1682,
                "DAYS_BIRTH": 0,
                'CNT_FAM_MEMBERS': 2,
                'CODE_GENDER': 'F',
                'FLAG_OWN_CAR': 'Y',
                'FLAG_OWN_REALTY': 'Y',
                'NAME_INCOME_TYPE': 'Working',
                'NAME_EDUCATION_TYPE': 'Incomplete higher',
                'NAME_FAMILY_STATUS': 'Single / not married',
                'NAME_HOUSING_TYPE': 'House / apartment',
                'FLAG_WORK_PHONE': 'str',
                'FLAG_EMAIL': 'str',
                'FLAG_PHONE': 'str'}
        }


description = """
# Tangelo API helps you do awesome [stuff](https://uploads-ssl.webflow.com/61eacada2d31db4a1d761030/61eacada2d31db2f2576105f_logo_full_color.svg). 🚀

## Doc de los parámetros del POST


You will be able to:

* **MONTHS_BALANCE** : **int** dentro del rangp [-60, 0] por deault la mediana -17
* **CNT_CHILDREN** : **int** dentro de [0, 19] por default 0
*    **AMT_INCOME_TOTAL** : **float** [2700, 1575000 ] por default 165000
*    **DAYS_EMPLOYED** : **int** [-15713, , 365243] por default -1682
*    **CNT_FAM_MEMBERS** : **int** [1, 20] por default 2
*    **CODE_GENDER** : **str** {'F', 'M'} por default "F"
*    **FLAG_OWN_CAR** : **str** {'Y', 'N'} por default "Y"
*    **FLAG_OWN_REALTY** : **str** {'Y', 'N'} por default "Y"
*    **NAME_INCOME_TYPE** : **str** {'Working', 'State servant', 'Pensioner', 'Commercial associate', 'Student'} por default 'Working'
*    **NAME_EDUCATION_TYPE** : **str** {'Secondary / secondary special', 'Higher education', 'Academic degree', 'Lower secondary', 'Incomplete higher'} por default 'Incomplete higher'
*    **NAME_FAMILY_STATUS** : **str** {'Single / not married', 'Separated', 'Civil marriage', 'Married', 'Widow'} por default 'Single / not married'
*    **NAME_HOUSING_TYPE** : **str**  {'Office apartment', 'With parents', 'House / apartment', 'Co-op apartment', 'Rented apartment', 'Municipal apartment'} por default 'House / apartment'
*    **FLAG_WORK_PHONE** : **str** {'0', '1'} por default '1'
*    **FLAG_PHONE** : **str** {'0', '1'}  por default '1'
*    **FLAG_EMAIL** : **str** {'0', '1'} por default '1'
"""

app = FastAPI(
    title="TangeloApp",
    description=description,
    version="0.0.1",
    contact={
        "name": "Fou the Amazing",
        "url": "http://github.com/fou-foo"
    }  # ,  license_info={"name": "Apache 2.0",   "identifier": "MIT",   },
)

# load model artifacts on startup of the application to reduce latency


@app.on_event("startup")
async def startup_event():
    global model, encoder, lb
    # if saved model exits, load the model from disk
    model = joblib.load("modelo_rf.joblib")

    with open('ordinal.pkl', 'rb') as file:
        ordinal = pickle.load(file)

    with open('ohe.pkl', 'rb') as file:
        ohe = pickle.load(file)


# This allows sending of data (our InferenceSample) via POST to the API.
@app.post("/inference/")
async def ingest_data(inference: InputData):

    data = {'DAYS_BIRTH': 0,
            'MONTHS_BALANCE': inference.MONTHS_BALANCE,
            'CNT_CHILDREN': inference.CNT_CHILDREN,
            'AMT_INCOME_TOTAL': inference.AMT_INCOME_TOTAL,
            'DAYS_EMPLOYED': inference.DAYS_EMPLOYED,
            'CNT_FAM_MEMBERS': inference.CNT_FAM_MEMBERS,
            'CODE_GENDER': inference.CODE_GENDER,
            'FLAG_OWN_CAR': inference.FLAG_OWN_CAR,
            'FLAG_OWN_REALTY': inference.FLAG_OWN_REALTY,
            'NAME_INCOME_TYPE': inference.NAME_INCOME_TYPE,
            'NAME_EDUCATION_TYPE': inference.NAME_EDUCATION_TYPE,
            'NAME_FAMILY_STATUS': inference.NAME_FAMILY_STATUS,
            'NAME_HOUSING_TYPE': inference.NAME_HOUSING_TYPE,
            'FLAG_WORK_PHONE': inference.FLAG_WORK_PHONE,
            'FLAG_EMAIL': inference.FLAG_EMAIL,
            'FLAG_PHONE': inference.FLAG_PHONE
            }
    # prepare the sample for inference as a dataframe
    sample = pd.DataFrame(data, index=[0])

    # apply transformation to sample data
    cat_features = ['CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'NAME_INCOME_TYPE',
                    'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE',  'FLAG_WORK_PHONE',  'FLAG_EMAIL', 'FLAG_PHONE']
    num_features = ["DAYS_BIRTH",  "MONTHS_BALANCE",  "CNT_CHILDREN",
                    "AMT_INCOME_TOTAL",  "DAYS_EMPLOYED",  "CNT_FAM_MEMBERS"]
    model = joblib.load("modelo_rf.joblib")

    with open('ordinal.pkl', 'rb') as file:
        ordinal = pickle.load(file)

    with open('ohe.pkl', 'rb') as file:
        ohe = pickle.load(file)

    sample = process_data(sample,  categorical_features=cat_features,
                          num_features=num_features,   ohe=ohe, ordinal=ordinal)

    # get model prediction
    prediction = model.predict(sample)
    return prediction[0]


@app.get("/")
async def greetings():
    return "Tangelo Test API"


if __name__ == '__main__':
    pass


"""
test case
{
  "MONTHS_BALANCE": 0,
  "CNT_CHILDREN": 0,
  "AMT_INCOME_TOTAL": 0,
  "DAYS_EMPLOYED": 0,
  "CNT_FAM_MEMBERS": 0,
  "CODE_GENDER": "F",
  "FLAG_OWN_CAR": "Y",
  "FLAG_OWN_REALTY": "Y",
  "NAME_INCOME_TYPE": "Working",
  "NAME_EDUCATION_TYPE": "Incomplete higher",
  "NAME_FAMILY_STATUS": "Single / not married",
  "NAME_HOUSING_TYPE": "House / apartment",
  "FLAG_WORK_PHONE": "1",
  "FLAG_EMAIL": "1",
  "FLAG_PHONE": "1"
}
"""
