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
..* A VPC to store all the other resources, with the subnets and security groups
..*  a Redshit cluster where you can find the final table with the carts information, the DataPipeline to process the events with Pig and copy the data to Redshift, the 