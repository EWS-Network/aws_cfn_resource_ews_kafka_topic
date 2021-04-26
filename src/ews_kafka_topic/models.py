# DO NOT modify this file by hand, changes will be overwritten
import sys
from dataclasses import dataclass
from inspect import getmembers, isclass
from typing import (
    AbstractSet,
    Any,
    Generic,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from cloudformation_cli_python_lib.interface import (
    BaseModel,
    BaseResourceHandlerRequest,
)
from cloudformation_cli_python_lib.recast import recast_object
from cloudformation_cli_python_lib.utils import deserialize_list

T = TypeVar("T")


def set_or_none(value: Optional[Sequence[T]]) -> Optional[AbstractSet[T]]:
    if value:
        return set(value)
    return None


@dataclass
class ResourceHandlerRequest(BaseResourceHandlerRequest):
    # pylint: disable=invalid-name
    desiredResourceState: Optional["ResourceModel"]
    previousResourceState: Optional["ResourceModel"]


@dataclass
class ResourceModel(BaseModel):
    Name: Optional[str]
    PartitionsCount: Optional[int]
    Partitions: Optional[int]
    Settings: Optional[MutableMapping[str, Any]]
    ReplicationFactor: Optional[int]
    BootstrapServers: Optional[str]
    SecurityProtocol: Optional[str]
    SASLMechanism: Optional[str]
    SASLUsername: Optional[str]
    SASLPassword: Optional[str]
    IsConfluentKafka: Optional[bool]

    @classmethod
    def _deserialize(
        cls: Type["_ResourceModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_ResourceModel"]:
        if not json_data:
            return None
        dataclasses = {n: o for n, o in getmembers(sys.modules[__name__]) if isclass(o)}
        recast_object(cls, json_data, dataclasses)
        return cls(
            Name=json_data.get("Name"),
            PartitionsCount=json_data.get("PartitionsCount"),
            Partitions=json_data.get("Partitions"),
            Settings=json_data.get("Settings"),
            ReplicationFactor=json_data.get("ReplicationFactor"),
            BootstrapServers=json_data.get("BootstrapServers"),
            SecurityProtocol=json_data.get("SecurityProtocol"),
            SASLMechanism=json_data.get("SASLMechanism"),
            SASLUsername=json_data.get("SASLUsername"),
            SASLPassword=json_data.get("SASLPassword"),
            IsConfluentKafka=json_data.get("IsConfluentKafka"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


