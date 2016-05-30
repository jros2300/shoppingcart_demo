from __future__ import print_function

import boto3
import sys

ml = boto3.client('machinelearning')

model_id=None
try:
    response = ml.describe_ml_models(
            FilterVariable='Name',
            EQ='ShoppingCartModel'
        )
    for model in response['Results']:
        if model['Status'] != 'DELETED' and model['Status'] != 'FAILED':
            model_id=model['MLModelId']
            endpoint=model['EndpointInfo']['EndpointUrl']
except:
    print("No model ready")
    sys.exit()


if model_id != None:
    prediction = ml.predict(
        MLModelId=model_id,
        Record={
            'customer': '4634',
            'cart': '13661535770434',
            'duration': '761',
            'added': '9',
            'removed': '1',
            'thinking': '0',
            'productsadded': '8956-10134-10229-6903-8714-13720-6297-10636-8966',
            'productsremoved': '8956',
            'productlist': '10134-10229-6903-8714-13720-6297-10636-8966',
            'timestamp': '1464000379'
        },
        PredictEndpoint=endpoint
    )

    print(prediction['Prediction'])
else:
    print("No model ready")


