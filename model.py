import io

import h2o
import pandas as pd
from h2o.automl import H2OAutoML


def train_model():
    """
    Trains an H2O AutoML model on car price data.
    This function initializes H2O, imports car price data, preprocesses it, and trains an AutoML model.
    Args:
        None
    Returns:
        None
    """
    h2o.init()

    cars = h2o.import_file("datasets/fipe_cars.csv")
    cars = cars.drop(["year_of_reference", "month_of_reference", "fipe_code", "authentication", "model"])
    x = cars.columns
    y = "avg_price_brl"
    x.remove(y)

    train, test = cars.split_frame(ratios=[0.8], seed=1)

    aml = H2OAutoML(max_models=20, seed=1, max_runtime_secs=3600)
    aml.train(x=x, y=y, training_frame=train)

    model_path = h2o.save_model(model=aml.leader, path="models/fipe_model", force=True)
    print(model_path)


def predict(saved_model, params, num_years=4):
    """
    Predicts car prices for future years using a trained model.
    This function takes a trained model, parameters for prediction, and predicts car prices for a specified number of
    future years.
    Args:
        saved_model (H2OEstimator): The trained H2O model.
        params (dict | string): Dictionary containing input parameters for prediction.
        num_years (int, optional): The number of future years to predict (default is 5).
    Returns:
        list: A list of lists containing predicted prices for each future year.
    """
    year_model = int(params['year_model'][0])
    results = []

    for i in range(num_years):
        params['year_model'][0] = year_model - i
        preds = saved_model.predict(h2o.H2OFrame(params))
        preds_df = preds.as_data_frame()
        predicted_value = round(preds_df.iloc[0, 0], 2)
        results.append([str(params['year_model'][0] + 5), str(predicted_value)])
    return results


def predict_batch(saved_model, csv_path):
    """
    Function for batch prediction using a saved machine learning model
    Args:
        - saved_model: A pre-trained machine learning model (H2O model)
         - csv_path: Path to the CSV file containing data for prediction
     Returns:
         - results: A list of dictionaries, each containing the original data row
        along with the predicted value from the model
    """
    df = pd.read_csv(csv_path)
    results = []

    for i in range(len(df)):
        year_model = int(df.loc[i, 'year_model'])
        df.loc[i, 'year_model'] = year_model
        preds = saved_model.predict(h2o.H2OFrame(df.loc[i:i]))
        preds_df = preds.as_data_frame()
        predicted_value = round(preds_df.iloc[0, 0], 2)
        row_data = df.loc[i].to_dict()
        row_data['predicted_value'] = str(predicted_value)
        results.append(row_data)

    return results


if __name__ == '__main__':
    train_model()
