# from rec_sys.rec_func import recommender
from h2o_wave import Q, main, app, ui
import h2o

from model import predict
import pandas as pd
# from fuzzywuzzy import process
from typing import Any

h2o.init()
saved_model = h2o.load_model("models/fipe_model/StackedEnsemble_AllModels_1_AutoML_1_20231001_14406")


@app("/pricepredict")
async def serve(q: Q):
    """
    Main app endpoint.

    Displays the recommended books according to the input.
    If the user cannot find the book, user can find the books that matches to the given input.
    """

    if not q.client.initialized:
        add_form_card(q)
        add_header(q)
        add_footer(q)
        q.client.initialized = True

    if q.args.predict:
        params = {
            'brand': [q.args.brand],
            'fuel': [q.args.fuel],
            'gear': [q.args.gear],
            'engine_size': [float(q.args.enginesize)],
            'year_model': [int(q.args.year)],
        }
        predicted_values = predict(saved_model, params)
        add_table(q, predicted_values)

    if q.args.predictagain:
        del q.page["table_card"]
        del q.page["predict_btn"]
        add_form_card(q)
        add_header(q)
        add_footer(q)

    await q.page.save()


def add_header(q: Q):
    """
    Adds the header card to the page.
    """

    q.page['header'] = ui.header_card(
        box='1 1 9 1',
        title='Car Price Predictor',
        subtitle='',
        image='https://wave.h2o.ai/img/h2o-logo.svg',
    )


def add_form_card(q: Q):
    """
    Adds the form card for user input to the page.
    Loads unique car brands from the dataset and creates a dropdown for them.
    """
    df = pd.read_csv('datasets/fipe_cars.csv')
    unique_brands = df['brand'].unique()

    dropdown_choices = [
        ui.choice(name=brand.lower(), label=brand.capitalize())
        for brand in unique_brands
    ]

    q.page['example'] = ui.form_card(
        box='2 3 4',
        items=[
            ui.text('<h3><b>Enter Car Details:</b></h3>'),
            ui.inline(items=[
                ui.textbox(name='year', label='Year of the Model', value=q.args.year, required=True),
                ui.dropdown(
                    name='brand',
                    value=q.args.dropdown,
                    label='Car Brand',
                    required=True,
                    choices=dropdown_choices
                ),
            ]),
            ui.inline(items=[
                ui.textbox(name='enginesize', label='Size of the Engine', value=q.args.enginesize, required=True),

                ui.dropdown(
                    name='gear',
                    value=q.args.dropdown,
                    label='Gear type',
                    required=True,
                    choices=[
                        ui.choice(name='auto', label="Automatic Gear"),
                        ui.choice(name='manual', label="Manual Gear")
                    ]
                ),
            ]),
            ui.dropdown(
                name='fuel',
                value=q.args.dropdown,
                label='Fuel type',
                required=True,
                choices=[
                    ui.choice(name='diesel', label="Diesel"),
                    ui.choice(name='gasoline', label="Gasoline")
                ]
            ),
            ui.button(name='predict', label='Predict')
        ]
    )


def add_table(q: Q, rows):
    """
    Adds the table card to the page to display predictions.
    Args:
        - rows (Any): The rows of data (predictions) to display in the table.
    """

    table_rows = [ui.table_row(name=f'row{i}', cells=row) for i, row in enumerate(rows)]
    q.page['table_card'] = ui.form_card(box='6 3 3 4', items=[
        ui.text('<h3><b>Predictions</b></h3>'),
        ui.table(
            name='table',
            columns=[
                ui.table_column(name='year', label="Year"),
                ui.table_column(name='price', label='Price (USD)'),
            ],
            rows=table_rows
        )
    ])


def add_footer(q: Q):
    """
    Adds the footer card to the page.
    """
    q.page['footer'] = ui.footer_card(
        box='2 8',
        caption='''Made with 💛 by Malindu.'''
    )
