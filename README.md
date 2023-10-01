# Future Car Price Prediction System


This repository contains   **Car Price Prediction System**. This application is designed to provide car dealers to predict the market values of cars yet to be released.


### System Requirements

1. Python 3.7+
2. pip3

### 1. Clone the repository:

``` bash
git clone https://github.com/malindupasan/car-price-predictor.git
```

### 2. Create a virtual environment:

``` bash
python3 -m venv venv
```

### 3. Activate the virtual environment:
``` bash
source venv/bin/activate
```

**windows**
``` bash
venv\Scripts\activate.bat
```
To deactivate the virtual environment use ```deactivate``` command.

### 4. Install dependencies:

``` bash
(venv) pip3 install -r requirements.txt 
```

### 5. Run the app:
``` bash
(venv) wave run app
```


### 6. View the app:
Go to any prefered browser http://localhost:10101/pricepredict

## Usecases

This app can be used by car dealers to predict the prices of upcoming cars.

## Train the DataSet using AutoML

Open model.py

you can modify the max_models parameter to specify the number of models . 

run model.py

## Model Evaluation 

ModelMetricsRegressionGLM: stackedensemble
**Reported on test data.**

MSE: 3462066125.440305<br>
RMSE: 58839.32465146337<br>
MAE: 16039.00313949049<br>
RMSLE: 0.1906881182807517<br>
Mean Residual Deviance: 3462066125.440305<br>
R^2: 0.9686852165071113<br>
Null degrees of freedom: 57790<br>
Residual degrees of freedom: 57787<br>
Null deviance: 6389196009728087.0<br>
Residual deviance: 200076263455320.7<br>
AIC: 1433400.6619283669<br>


## Learn More

Watch preview  : [preview](https://github.com/malindupasan/car-price-predictor/blob/main/preview/previewVid.mp4)

Watch preview on YouTube :[preview](https://youtu.be/0ncb9DIRstY) 

To learn more about H2O AutoML, check out the [docs](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html).

To learn more about H2O Wave, check out the [docs](https://wave.h2o.ai/).
