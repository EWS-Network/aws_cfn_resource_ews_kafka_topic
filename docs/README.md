# EWS::Kafka::Topic

Resource to create Kafka topics in your cluster.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "EWS::Kafka::Topic",
    "Properties" : {
        "<a href="#name" title="Name">Name</a>" : <i>String</i>,
        "<a href="#partitionscount" title="PartitionsCount">PartitionsCount</a>" : <i>Integer</i>,
        "<a href="#settings" title="Settings">Settings</a>" : <i>Map</i>,
        "<a href="#replicationfactor" title="ReplicationFactor">ReplicationFactor</a>" : <i>Integer</i>,
        "<a href="#bootstrapservers" title="BootstrapServers">BootstrapServers</a>" : <i>String</i>,
        "<a href="#securityprotocol" title="SecurityProtocol">SecurityProtocol</a>" : <i>String</i>,
        "<a href="#saslmechanism" title="SASLMechanism">SASLMechanism</a>" : <i>String</i>,
        "<a href="#saslusername" title="SASLUsername">SASLUsername</a>" : <i>String</i>,
        "<a href="#saslpassword" title="SASLPassword">SASLPassword</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: EWS::Kafka::Topic
Properties:
    <a href="#name" title="Name">Name</a>: <i>String</i>
    <a href="#partitionscount" title="PartitionsCount">PartitionsCount</a>: <i>Integer</i>
    <a href="#settings" title="Settings">Settings</a>: <i>Map</i>
    <a href="#replicationfactor" title="ReplicationFactor">ReplicationFactor</a>: <i>Integer</i>
    <a href="#bootstrapservers" title="BootstrapServers">BootstrapServers</a>: <i>String</i>
    <a href="#securityprotocol" title="SecurityProtocol">SecurityProtocol</a>: <i>String</i>
    <a href="#saslmechanism" title="SASLMechanism">SASLMechanism</a>: <i>String</i>
    <a href="#saslusername" title="SASLUsername">SASLUsername</a>: <i>String</i>
    <a href="#saslpassword" title="SASLPassword">SASLPassword</a>: <i>String</i>
</pre>

## Properties

#### Name

Kafka topic name

_Required_: Yes

_Type_: String

_Minimum_: <code>1</code>

_Pattern_: <code>^[a-zA-Z0-9_.-]+$</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### PartitionsCount

Number of partitions for the new Kafka topic

_Required_: Yes

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Settings

_Required_: No

_Type_: Map

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### ReplicationFactor

Kafka topic replication factor

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### BootstrapServers

Endpoint URL of the Kafka cluster (must be reachable from VPC) in the format hostname:port

_Required_: Yes

_Type_: String

_Minimum_: <code>3</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### SecurityProtocol

Kafka Security Protocol.

_Required_: No

_Type_: String

_Allowed Values_: <code>PLAINTEXT</code> | <code>SSL</code> | <code>SASL_PLAINTEXT</code> | <code>SASL_SSL</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SASLMechanism

Kafka SASL mechanism for Authentication

_Required_: No

_Type_: String

_Allowed Values_: <code>PLAIN</code> | <code>GSSAPI</code> | <code>OAUTHBEARER</code> | <code>SCRAM-SHA-256</code> | <code>SCRAM-SHA-512</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SASLUsername

Kafka SASL username for Authentication

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SASLPassword

Kafka SASL password for Authentication

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Name.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Partitions

Number of partitions of the Kafka topic

