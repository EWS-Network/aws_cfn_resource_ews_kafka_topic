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

Features
==========

CRUD support for Kafka topics against a kafka cluster.

Credits
========

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
