from fastapi import FastAPI
from typing import Optional
import requests
from pydantic import BaseModel


api_key="35f5fc6afa9c016157b207929ee52827"
url = "http://data.fixer.io/api/latest?access_key=" +api_key


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class CurCvt(BaseModel):
     firstCurrency: str
     secondCurrency: str
     amount: float



app = FastAPI()
@app.get('/')
def read_root():
    return "Server is running test"

@app.post("/")
def index():
        fistCurrency=request.form.get("firstCurrency")
        secondCurrency =request.form.get("secondCurrency")
        amount=request.form.get("amount")
        response = requests.get(url)
        app.logger.info(response)
        infos = response.json()
        firstValue=infos["rates"][fistCurrency]
        secondValue = infos["rates"][secondCurrency]
        result =(secondValue/firstValue)*float(amount)
        currencyInfo=dict()
        currencyInfo["firstCurrency"] =fistCurrency
        currencyInfo["secondCurrency"]=secondCurrency
        currencyInfo["amount"]=amount
        currencyInfo["result"]=result
        return {"data": currencyInfo}


@app.post("/items/")
def create_item(item: Item):
    return item

@app.post("/convertor/")
def create_convertor(item: CurCvt):
    fistCurrency=item.firstCurrency
    secondCurrency =item.secondCurrency
    amount=item.amount
    response = requests.get(url)
    infos = response.json()
    firstValue=infos["rates"][fistCurrency]
    secondValue = infos["rates"][secondCurrency]
    result =(secondValue/firstValue)*float(amount)
    currencyInfo=dict()
    currencyInfo["firstCurrency"] =fistCurrency
    currencyInfo["secondCurrency"]=secondCurrency
    currencyInfo["amount"]=amount
    currencyInfo["result"]=result
    return {"result": currencyInfo}