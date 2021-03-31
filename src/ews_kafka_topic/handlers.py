#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2021 John Mille<john@ews-network.net>

import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
    identifier_utils,
)

from .models import ResourceHandlerRequest, ResourceModel
from .topics_management import create_new_kafka_topic, update_kafka_topic, delete_topic

LOG = logging.getLogger(__name__)
TYPE_NAME = "EWS::Kafka::Topic"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


def get_cluster_config(model):
    """

    :param model:
    :param bool use_confluent:
    :return:
    """
    cluster_config = {}
    if bool(model.IsConfluentKafka):
        cluster_config["bootstrap.servers"] = model.BootstrapServers
        cluster_config["security.protocol"] = model.SecurityProtocol
        cluster_config["sasl.mechanism"] = model.SASLMechanism
        cluster_config["sasl.username"] = model.SASLUsername
        cluster_config["sasl.password"] = model.SASLPassword
    else:
        cluster_config["bootstrap_servers"] = model.BootstrapServers
        cluster_config["security_protocol"] = model.SecurityProtocol
        cluster_config["sasl_mechanism"] = model.SASLMechanism
        cluster_config["sasl_plain_username"] = model.SASLUsername
        cluster_config["sasl_plain_password"] = model.SASLPassword
    return cluster_config


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    cluster_config = get_cluster_config(model)
    try:
        primary_identifier = model.Name
        if primary_identifier is None:
            primary_identifier = identifier_utils.generate_resource_identifier(
                stack_id_or_name=request.stackId,
                logical_resource_id=request.logicalResourceIdentifier,
                client_request_token=request.clientRequestToken,
                max_length=255,
            )
        create_new_kafka_topic(
            primary_identifier,
            model.PartitionsCount,
            cluster_config,
            model.ReplicationFactor,
            bool(model.IsConfluentKafka),
        )
        progress.status = OperationStatus.SUCCESS
    except Exception as e:
        return ProgressEvent.failed(
            HandlerErrorCode.InternalFailure, f"was not expecting type {str(e)}"
        )
    model.Partitions = model.PartitionsCount
    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    cluster_config = get_cluster_config(model)
    update_kafka_topic(
        model.Name, model.PartitionsCount, cluster_config, bool(model.IsConfluentKafka)
    )
    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=None,
    )
    cluster_config = get_cluster_config(model)
    try:
        delete_topic(model.Name, cluster_config, bool(model.IsConfluentKafka))
        return progress
    except Exception as error:
        return ProgressEvent.failed(
            HandlerErrorCode.InternalFailure, f"was not expecting type {str(error)}"
        )


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    # TODO: put code here
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.LIST)
def list_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    # TODO: put code here
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=[],
    )
