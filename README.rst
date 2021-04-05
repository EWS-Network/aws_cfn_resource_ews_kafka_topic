==========================
CFN Kafka - Topic provider
==========================

AWS CFN Provider for Kafka Topics

How to use
==========

Using AWS Private registry resource
------------------------------------

The original plan with this project was to use a new Resource published in AWS Private Registry and have CFN templates
such as

.. code-block:: yaml

    Resources:
      NewTopic:
        Type: EWS::Kafka::Topic
        Properties:
          Name: new-topic.v1
          Partitions: 3
          BootstrapServers: my-cluster-endpoint.internal

However, due to the fact that AWS hosts the functions which are used then to create the resources in their own account,
there is no access to clusters which are located inside a VPC unless you provide with public access.

If you aim to use that and deploy it to your account, refer to the docs/README.md which is generated through the
cloudformation SDK for properties, and return values.

Using a lambda function + Custom resource
-------------------------------------------

Due to the limitation mentioned above (VPC), I adapted the project to use a very similar format of definition to stay consistent,
but this time to use that resource, you will be creating the Lambda function yourselves, in your VPC if you so need to, and will be able to
use it as follows:

.. code-block:: yaml

    Resources:
      NewTopic:
        Type: Custom::KafkaTopic
        Properties:
          ServiceToken: !Sub "arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:kafka-topic-provider
          Name: my-new-kafka-topic
          Partitions: 6
          BootstrapServers: my-cluster-endpoint.internal


Return Values
==============

Name
-----

The name of the topic

Partitions
------------

The number of partitions used for the cluster.
Useful when you need to define auto-scaling rules (cannot have more consumers that partitions)

Install
=========

Via AWS SAR
------------

Deploy the lambda function with the latest publised code by heading to `AWS Serverless Application Repository <https://serverlessrepo.aws.amazon.com/applications/eu-west-1/965289391954/cfn-ews-kafka-topic>`__



From source code to AWS
-------------------------

.. code-block:: bash

    # You will need to override the bucket name to upload it to your bucket
    BUCKET=cf-templates-1imn09kcv6429-eu-west-1 make upload

    # Once the function.yaml file is generated, deploy.
    # For example, with MSK, given you need access to secrets in SecretsManager for SASL_SSL + SCRAM
    # and the KMS Key needs to be non-default

    aws cloudformation deploy --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
        --template-file function.yaml --stack-name cfn-msk-topic-provider \
        --parameter-overrides VpcId=vpc-081a6d0e40d676bcc \
        Subnets=subnet-0ceb9b9cc5e8f4980,subnet-07dda1c2ee4b0b64b,subnet-0dd7757424349314f \
        SecretArn=arn:aws:secretsmanager:eu-west-1:012345678912:secret:AmazonMSK_*  \
        SecretKmsKeyArn=arn:aws:kms:eu-west-1:012345678912:key/91862207-c017-4cd8-9966-0530568e518d

Credits
========

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
