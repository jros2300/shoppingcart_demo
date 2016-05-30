from __future__ import print_function

import boto3



ml = boto3.client('machinelearning')
prediction = ml.predict(
    MLModelId='ml-dZxbrDXAstA',
    Record={
        'Var01': '4634',
        'Var02': '13661535770434',
        'Var03': '761',
        'Var05': '9',
        'Var06': '1',
        'Var07': '0',
        'Var08': '8956-10134-10229-6903-8714-13720-6297-10636-8966',
        'Var09': '8956',
        'Var10': '10134-10229-6903-8714-13720-6297-10636-8966',
        'Var11': '1464000379'
    },
    PredictEndpoint='https://realtime.machinelearning.eu-west-1.amazonaws.com'
)

print(response)