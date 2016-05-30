# Shopping Cart Demo
## Introduction
This repository contains an example of a Big Data pipeline to process a stream of event from a Shopping Cart. With the scripts and templates contained in this repository you can create an AWS environment to generate and process this stream of events.

If you run these scripts and templates, you're going to create resources in your AWS account, and that's going to have a cost. Please review the content before you use it.

## Installation
To create all the resources you should follow these steps:

1. Create a S3 bucket to store the events and all the processed files
2. Use the script createResources.py to generate the Kinesis Firehose stream and the required IAM role for it.
>python createResources.py -b \<bucket_name\>

3. Create all the other resources using the CloudFormation template ShoppingCart.cform. This stack creates:
  * VPC to store all the other resources, with the subnets and security groups
  * Redshit cluster where you can find the final table with the carts information
  * DataPipeline to process the events with Pig and copy the data to Redshift. This pipeline runs every hour.
  * DataPipeline to process the events with Pig and train the Machine Learning Model. You can run this pipeline manually.
  * EC2 Instance generating random events every five minutes

## Details
The generation of events is done with the DataGeneration.go application, it generates cart interactions randomly and send the events to AWS Firehose.

AWS Firehose then stores the stream of events to the S3 bucket automatically.

The first DataPipeline runs every hour and gets the events of the previous hour from S3, processing them with an EMR cluster using a Pig script, then it stores the result into the S3 bucket, and run a COPY command in the Redshift cluster to append the new information in the the shoppingcart table.

The second DataPipeline can be run manually from the DataPipeline console, when you run it, it gets the events from the previous day, and process them with another Pig script in an EMR cluster. Then store the result to S3, and use it to train a new model. To create the model and train it, uses the createML.py script.

There is an example of how to use the MachineLearning model to get a prediction using the MachineLearning endpoint in the script testPrediction.py


