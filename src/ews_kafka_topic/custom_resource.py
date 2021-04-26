#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2021 John Mille<john@ews-network.net>

"""Main module."""

import logging
from cfn_resource_provider import ResourceProvider
from .topics_management import (
    create_new_kafka_topic,
    update_kafka_topic,
    delete_topic,
)
from aws_cfn_custom_resource_resolve_parser import handle

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def keyisset(x, y):
    """
    Macro to figure if the the dictionary contains a key and that the key is not empty

    :param x: The key to check presence in the dictionary
    :type x: str
    :param y: The dictionary to check for
    :type y: dict

    :returns: True/False
    :rtype: bool
    """
    if isinstance(y, dict) and x in y.keys() and y[x]:
        return True
    return False


def keypresent(x, y):
    """
    Macro to figure if the the dictionary contains a key and that the key is not empty

    :param x: The key to check presence in the dictionary
    :type x: str
    :param y: The dictionary to check for
    :type y: dict

    :returns: True/False
    :rtype: bool
    """
    if isinstance(y, dict) and x in y.keys():
        return True
    return False


class KafkaTopic(ResourceProvider):
    def __init__(self):
        """
        Init method
        """
        self.cluster_info = {}
        super(KafkaTopic, self).__init__()
        self.request_schema = {
            "type": "object",
            "required": ["Name", "PartitionsCount", "BootstrapServers"],
            "properties": {
                "Name": {
                    "$comment": "The name of the kafka topic",
                    "type": "string",
                    "minLength": 1,
                    "pattern": "^[a-zA-Z0-9_.-]+$",
                    "description": "Kafka topic name",
                },
                "PartitionsCount": {
                    "type": "integer",
                    "default": 1,
                    "description": "Number of partitions for the new Kafka topic",
                },
                "ReplicationFactor": {
                    "type": "integer",
                    "default": 1,
                    "description": "Kafka topic replication factor",
                },
                "Settings": {"type": "object"},
                "BootstrapServers": {
                    "type": "string",
                    "minLength": 3,
                    "description": "Endpoint URL of the Kafka cluster (must route to brokers), format hostname:port",
                },
                "SecurityProtocol": {
                    "type": "string",
                    "default": "PLAINTEXT",
                    "description": "Kafka Security Protocol.",
                    "enum": ["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"],
                },
                "SASLMechanism": {
                    "type": "string",
                    "default": "PLAIN",
                    "description": "Kafka SASL mechanism for Authentication",
                    "enum": [
                        "PLAIN",
                        "GSSAPI",
                        "OAUTHBEARER",
                        "SCRAM-SHA-256",
                        "SCRAM-SHA-512",
                    ],
                },
                "SASLUsername": {
                    "type": "string",
                    "description": "Kafka SASL username for Authentication",
                },
                "SASLPassword": {
                    "type": "string",
                    "description": "Kafka SASL password for Authentication",
                },
            },
        }

    def convert_property_types(self):
        int_props = ["PartitionsCount", "ReplicationFactor"]
        boolean_props = ["IsConfluentKafka"]
        for prop in int_props:
            if keypresent(prop, self.properties) and isinstance(
                self.properties[prop], str
            ):
                try:
                    self.properties[prop] = int(self.properties[prop])
                except Exception as error:
                    self.fail(
                        f"Failed to get cluster information - {prop} - {str(error)}"
                    )
        for prop in boolean_props:
            if keypresent(prop, self.properties) and isinstance(
                self.properties[prop], str
            ):
                self.properties[prop] = self.properties[prop].lower() == "true"

    def define_cluster_info(self):
        """
        Method to define the cluster information into a simple format
        """
        try:
            self.cluster_info["bootstrap_servers"] = self.get("BootstrapServers")
            self.cluster_info["security_protocol"] = self.get("SecurityProtocol")
            self.cluster_info["sasl_mechanism"] = self.get("SASLMechanism")
            self.cluster_info["sasl_plain_username"] = self.get("SASLUsername")
            self.cluster_info["sasl_plain_password"] = self.get("SASLPassword")
        except Exception as error:
            self.fail(f"Failed to get cluster information - {str(error)}")

        for key, value in self.cluster_info.items():
            if isinstance(value, str) and value.find("resolve:secretsmanager") >= 0:
                try:
                    self.cluster_info[key] = handle(value)
                except Exception as error:
                    LOG.error("Failed to import secrets from SecretsManager")
                    self.fail(str(error))

    def create(self):
        """
        Method to create a new Kafka topic
        :return:
        """
        LOG.info(f"Attempting to create new topic {self.get('Name')}")
        self.define_cluster_info()
        cluster_url = (
            self.cluster_info["bootstrap.servers"]
            if self.get("IsConfluentKafka")
            else self.cluster_info["bootstrap_servers"]
        )
        LOG.info(f"Cluster is {cluster_url}")
        if not self.get("PartitionsCount") >= 1:
            self.fail("The number of partitions must be a strictly positive value >= 1")
        try:
            topic_name = create_new_kafka_topic(
                self.get("Name"),
                self.get("PartitionsCount"),
                self.cluster_info,
                replication_factor=self.get("ReplicationFactor"),
                settings=self.get("Settings"),
            )
            self.physical_resource_id = topic_name
            self.set_attribute("Name", self.get("Name"))
            self.set_attribute("Partitions", self.get("PartitionsCount"))
            self.set_attribute("BootstrapServers", self.get("BootstrapServers"))
            self.success(f"Created new topic {topic_name}")
        except Exception as error:
            self.physical_resource_id = "could-not-create"
            self.fail(f"Failed to create the topic {self.get('Name')}, {str(error)}")

    def update(self):
        """
        :return:
        """
        self.define_cluster_info()
        try:
            update_kafka_topic(
                self.get("Name"),
                self.get("PartitionsCount"),
                self.cluster_info,
            )
        except Exception as error:
            self.fail(str(error))

    def delete(self):
        """
        Method to delete the Topic resource
        :return:
        """
        self.define_cluster_info()
        LOG.info(self.get("Name"))
        LOG.info(self.get_old("Name"))
        if self.get_old("Name") is None and self.get("Name"):
            LOG.warning("Deleting failed create resource.")
            self.success("Deleting non-working resource")
            return
        try:
            delete_topic(self.get("Name"), self.cluster_info)
        except Exception as error:
            self.fail(
                f"Failed to delete topic {self.get_attribute('Name')}. {str(error)}"
            )


def lambda_handler(event, context):
    provider = KafkaTopic()
    provider.handle(event, context)
