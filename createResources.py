from __future__ import print_function

import boto3
import argparse
import sys


parser = argparse.ArgumentParser(description='Create the necessary resources to use the ShoppingCart Demo.')
parser.add_argument('-b', '--bucket', dest='bucket', action='store', required=True,
                    help='The bucket to store the events')
args = parser.parse_args()    

iam = boto3.client('iam')
try:
    response = iam.create_role(
        RoleName='ShoppingCartFirehose',
        AssumeRolePolicyDocument='{"Version": "2012-10-17", "Statement": [{"Sid": "", "Effect": "Allow", "Principal": {"Service": "firehose.amazonaws.com"}, "Action": "sts:AssumeRole", "Condition": {"StringEquals": {"sts:ExternalId": "731348316595"}}}]}'
    )
except:
    response = iam.get_role(
        RoleName='ShoppingCartFirehose'
    )

roleArn = response['Role']['Arn'] 


response = iam.put_role_policy(
    RoleName='ShoppingCartFirehose',
    PolicyName='ShoppingCartFirehosePolicy',
    PolicyDocument='''{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::''' + args.bucket + '''",
        "arn:aws:s3:::''' + args.bucket + '''/*"
      ]
    },
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "logs:PutLogEvents"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}'''
)

print("Created/Updated role: %s" % roleArn)

fh = boto3.client('firehose')

try:
    response = fh.create_delivery_stream(
        DeliveryStreamName='ShoppingCart',
        S3DestinationConfiguration={
            'RoleARN': roleArn,
            'BucketARN': "arn:aws:s3:::%s" % args.bucket,
            'Prefix': 'streams/',
            'BufferingHints': {
                'SizeInMBs': 5,
                'IntervalInSeconds': 300
            },
            'CompressionFormat': 'GZIP'
        }
    )

    print("Created Firehose stream ShoppingCart")
except:
    print("Error creating the Firhose stream ShoppingCart")

