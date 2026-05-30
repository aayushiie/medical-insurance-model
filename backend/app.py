from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal
import pickle
import pandas as pd

# import ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

# pydantic model
class UserInput(BaseModel):
    age: int = Field(..., gt=0, lt=120)
    gender: Literal['male', 'female'] = Field(...)
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    smokes: Literal['yes', 'no'] = Field(...)
    region: Literal['northeast', 'northwest', 'southeast', 'southwest'] = Field(...)
    charges: float = Field(..., gt=0)
    monthly_premium_est: float = Field(..., gt=0)
    charges_per_child: float = Field(..., gt=0)
    bmi_age_interaction: float = Field(..., gt=0)
    risk_score: float = Field(..., gt=0, lt=9)
    is_high_risk: bool = Field(...)
    num_children: int = Field(...)

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def age_group(self)-> str:
        if self.age in range(18, 26):
            return "Young Adult (18-25)"
        elif self.age in range(26, 36):
            return "Adult (26-35)"
        elif self.age in range(36, 46):
            return "Middle-Aged (36-45)"
        elif self.age in range(46, 56):
            return "Senior-Middle (46-55)"
        elif self.age > 56:
            return "Senior (56+)"
        
    @computed_field
    @property
    def sex(self)-> bool:
        if self.gender == 'female':
            return 1
        else:
            return 0
        
    @computed_field
    @property
    def smoker(self)-> bool:
        if self.smokes == 'no':
            return 0
        else:
            return 1

@app.post('/predict')
def predict_insurance(data: UserInput):

    # we want to give one row at a time as input 
    # and input should be in form of pandas dataframe

    input_df = pd.DataFrame([{
        'age_group': data.age_group,
        'sex': data.sex,
        'bmi': data.bmi,
        'children': data.num_children,
        'smoker': data.smoker,
        'is_high_risk': data.is_high_risk,
        'risk_score': data.risk_score,
        'region': data.region,
        'charges': data.charges,
        'monthly_premium_est': data.monthly_premium_est,
        'charges_per_child': data.charges_per_child,
        'bmi_age_interaction': data.bmi_age_interaction
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': prediction})
