import h2o
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


def predict(saved_model, params, num_years=5):
    """
    Predicts car prices for future years using a trained model.
    This function takes a trained model, parameters for prediction, and predicts car prices for a specified number of
    future years.
    Args:
        saved_model (H2OEstimator): The trained H2O model.
        params (dict): Dictionary containing input parameters for prediction.
        num_years (int, optional): The number of future years to predict (default is 5).
    Returns:
        list: A list of lists containing predicted prices for each future year.
    """
    year_model = int(params['year_model'][0])
    results = []

    for i in range(num_years):
        params['year_model'][0] = year_model+1 - i
        preds = saved_model.predict(h2o.H2OFrame(params))
        preds_df = preds.as_data_frame()
        predicted_value = round(preds_df.iloc[0, 0], 2)
        results.append([str(params['year_model'][0]), str(predicted_value)])

    return results


