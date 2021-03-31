#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2021 John Mille<john@ews-network.net>

"""
Module to handle Kafka topics management.
"""

from kafka import KafkaConsumer, errors
from kafka.admin import (
    KafkaAdminClient,
    NewTopic,
    NewPartitions,
)


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


def create_new_kafka_topic(
    name, partitions, cluster_info, replication_factor=None, is_confluent=False
):
    """
    Function to create new Kafka topic

    :param str name:
    :param int partitions:
    :param dict cluster_info: Dictionary with the Kafka information
    :param int replication_factor: Replication factor. Defaults to 3
    :param bool is_confluent:
    :return:
    """
    if not replication_factor:
        replication_factor = 1
    if is_confluent:
        # Import of confluent kafka lib errors within lambda. To fix later
        pass
    else:
        try:
            admin_client = KafkaAdminClient(**cluster_info)
            topic = NewTopic(name, partitions, replication_factor)
            admin_client.create_topics([topic])
            return name
        except errors.TopicAlreadyExistsError:
            raise errors.TopicAlreadyExistsError(f"Topic {name} already exists")


def delete_topic(name, cluster_info, is_confluent=False):
    """
    Function to delete kafka topic

    :param name: name of the topic to delete
    :param cluster_info: cluster information
    :param bool is_confluent:
    :return:
    """
    print(f"Deleting topic {name}")
    if is_confluent:
        # Import of confluent kafka lib errors within lambda. To fix later
        pass
    else:
        admin_client = KafkaAdminClient(**cluster_info)
        admin_client.delete_topics([name])


def update_kafka_topic(name, partitions, cluster_info, is_confluent=False):
    """
    Function to update existing Kafka topic

    :param name:
    :param partitions:
    :param cluster_info:
    :param is_confluent:
    :return:
    """
    if is_confluent:
        # Import of confluent kafka lib errors within lambda. To fix later
        pass
    else:
        consumer_client = KafkaConsumer(**cluster_info)
        curr_partitions = len(consumer_client.partitions_for_topic(name))
        if partitions == curr_partitions:
            print(
                f"Topic partitions is already set to {curr_partitions}. Nothing to update"
            )
        elif partitions < curr_partitions:
            raise ValueError(
                f"The number of partitions set {partitions} for topic "
                f"{name} is lower than current partitions count {curr_partitions}"
            )
        admin_client = KafkaAdminClient(**cluster_info)
        admin_client.create_partitions({name: NewPartitions(partitions)})
