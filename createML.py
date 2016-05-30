from __future__ import print_function

import boto3
import argparse
import sys
import random
import string
import time


parser = argparse.ArgumentParser(description='Create the necessary resources to use the ShoppingCart Demo.')
parser.add_argument('-b', '--bucket', dest='bucket', action='store', required=True,
                    help='The bucket to store the events')
parser.add_argument('-r', '--region', dest='region', action='store', required=True,
                    help='The region to create the MachineLearning model')
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()    

ml = boto3.client('machinelearning', region_name=args.region)

def print_debug(response, debug):
    if debug:
        print(response)


try:
    response = ml.describe_evaluations(
        FilterVariable='Name',
        EQ='ShoppingCartEval'
    )
    for evaluation in response['Results']:
        if evaluation['Status'] != 'DELETED' and evaluation['Status'] != 'FAILED':
            response = ml.delete_evaluation(
                EvaluationId=evaluation['EvaluationId']
            )
            print_debug(response, args.debug)
except:
    pass

try:
    response = ml.describe_ml_models(
        FilterVariable='Name',
        EQ='ShoppingCartModel'
    )
    for model in response['Results']:
        if model['Status'] != 'DELETED' and model['Status'] != 'FAILED':
            response = ml.delete_realtime_endpoint(
                MLModelId=model['MLModelId']
            )
            print_debug(response, args.debug)
            response = ml.delete_ml_model(
                MLModelId=model['MLModelId']
            )
            print_debug(response, args.debug)
except:
    pass

try:
    response = ml.describe_data_sources(
        FilterVariable='Name',
        EQ='ShoppingCartAll'
    )
    for datasource in response['Results']:
        if datasource['Status'] != 'DELETED' and datasource['Status'] != 'FAILED':
            response = ml.delete_data_source(
                DataSourceId=datasource['DataSourceId']
            )
            print_debug(response, args.debug)
except:
    pass

try:
    response = ml.describe_data_sources(
        FilterVariable='Name',
        EQ='ShoppingCart70'
    )
    for datasource in response['Results']:
        if datasource['Status'] != 'DELETED' and datasource['Status'] != 'FAILED':
            response = ml.delete_data_source(
                DataSourceId=datasource['DataSourceId']
            )
            print_debug(response, args.debug)
except:
    pass

try:
    response = ml.describe_data_sources(
        FilterVariable='Name',
        EQ='ShoppingCart30'
    )
    for datasource in response['Results']:
        if datasource['Status'] != 'DELETED' and datasource['Status'] != 'FAILED':
            response = ml.delete_data_source(
                DataSourceId=datasource['DataSourceId']
            )
            print_debug(response, args.debug)
except:
    pass


datasorce_all_id = "ds-%s" % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

response = ml.create_data_source_from_s3(
    DataSourceId=datasorce_all_id,
    DataSourceName='ShoppingCartAll',
    DataSpec={
        'DataLocationS3': "s3://%s/ml/" % args.bucket,
        'DataSchema': '''{
  "version" : "1.0",
  "rowId" : "cart",
  "rowWeight" : null,
  "targetAttributeName" : "_Target_",
  "dataFormat" : "CSV",
  "dataFileContainsHeader" : false,
  "attributes" : [ {
    "attributeName" : "customer",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "cart",
    "attributeType" : "CATEGORICAL"
  }, {
    "attributeName" : "duration",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "_Target_",
    "attributeType" : "BINARY"
  }, {
    "attributeName" : "added",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "removed",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "thinking",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "productsadded",
    "attributeType" : "TEXT"
  }, {
    "attributeName" : "productsremoved",
    "attributeType" : "TEXT"
  }, {
    "attributeName" : "productlist",
    "attributeType" : "TEXT"
  }, {
    "attributeName" : "timestamp",
    "attributeType" : "NUMERIC"
  } ],
  "excludedAttributeNames" : [ ]
}'''
    },
    ComputeStatistics=True
)
print_debug(response, args.debug)

datasorce_70_id = "ds-%s" % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
response = ml.create_data_source_from_s3(
    DataSourceId=datasorce_70_id,
    DataSourceName='ShoppingCart70',
    DataSpec={
        'DataLocationS3': "s3://%s/ml/" % args.bucket,
        'DataRearrangement': '''{
  "splitting": {
    "percentBegin": 0,
    "percentEnd": 70,
    "strategy": "sequential",
    "complement": false,
    "strategyParams": {}
  }
}''',
        'DataSchema': '''{
  "version" : "1.0",
  "rowId" : "cart",
  "rowWeight" : null,
  "targetAttributeName" : "_Target_",
  "dataFormat" : "CSV",
  "dataFileContainsHeader" : false,
  "attributes" : [ {
    "attributeName" : "customer",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "cart",
    "attributeType" : "CATEGORICAL"
  }, {
    "attributeName" : "duration",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "_Target_",
    "attributeType" : "BINARY"
  }, {
    "attributeName" : "added",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "removed",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "thinking",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "productsadded",
    "attributeType" : "TEXT"
  }, {
    "attributeName" : "productsremoved",
    "attributeType" : "TEXT"
  }, {
    "attributeName" : "productlist",
    "attributeType" : "TEXT"
  }, {
    "attributeName" : "timestamp",
    "attributeType" : "NUMERIC"
  } ],
  "excludedAttributeNames" : [ ]
}'''
    },
    ComputeStatistics=True
)
print_debug(response, args.debug)

datasorce_30_id = "ds-%s" % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
response = ml.create_data_source_from_s3(
    DataSourceId=datasorce_30_id,
    DataSourceName='ShoppingCart30',
    DataSpec={
        'DataLocationS3': "s3://%s/ml/" % args.bucket,
        'DataRearrangement': '''{
  "splitting": {
    "percentBegin": 70,
    "percentEnd": 100,
    "strategy": "sequential",
    "complement": false,
    "strategyParams": {}
  }
}''',
        'DataSchema': '''{
  "version" : "1.0",
  "rowId" : "cart",
  "rowWeight" : null,
  "targetAttributeName" : "_Target_",
  "dataFormat" : "CSV",
  "dataFileContainsHeader" : false,
  "attributes" : [ {
    "attributeName" : "customer",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "cart",
    "attributeType" : "CATEGORICAL"
  }, {
    "attributeName" : "duration",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "_Target_",
    "attributeType" : "BINARY"
  }, {
    "attributeName" : "added",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "removed",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "thinking",
    "attributeType" : "NUMERIC"
  }, {
    "attributeName" : "productsadded",
    "attributeType" : "TEXT"
  }, {
    "attributeName" : "productsremoved",
    "attributeType" : "TEXT"
  }, {
    "attributeName" : "productlist",
    "attributeType" : "TEXT"
  }, {
    "attributeName" : "timestamp",
    "attributeType" : "NUMERIC"
  } ],
  "excludedAttributeNames" : [ ]
}'''
    },
    ComputeStatistics=True
)
print_debug(response, args.debug)

model_id = "ds-%s" % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
response = ml.create_ml_model(
    MLModelId=model_id,
    MLModelName='ShoppingCartModel',
    MLModelType='BINARY',
    Parameters={
        "sgd.maxPasses": "10",
        "sgd.l2RegularizationAmount": "1e-6",
        "sgd.maxMLModelSizeInBytes": "104857600",
        "sgd.l1RegularizationAmount": "0.0"
    },
    TrainingDataSourceId=datasorce_70_id
)
print_debug(response, args.debug)

evaluation_id = "ds-%s" % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
response = ml.create_evaluation(
    EvaluationId=evaluation_id,
    EvaluationName='ShoppingCartEval',
    MLModelId=model_id,
    EvaluationDataSourceId=datasorce_30_id
)
print_debug(response, args.debug)

while True:
    response = ml.get_ml_model(
        MLModelId=model_id,
        Verbose=False
    )
    if response['Status'] == 'COMPLETED':
        response = ml.create_realtime_endpoint(
            MLModelId=model_id
        )
        break
    if response['Status'] == 'FAILED' or response['Status'] == 'DELETED':
        print('Failed creating the model')
    time.sleep(5)
print_debug(response, args.debug)

