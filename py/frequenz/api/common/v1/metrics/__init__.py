# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: frequenz/api/common/v1/metrics/bounds.proto, frequenz/api/common/v1/metrics/metric_sample.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from datetime import datetime
from typing import (
    List,
    Optional,
)

import betterproto


class Metric(betterproto.Enum):
    """List of supported metrics."""

    METRIC_UNSPECIFIED = 0
    """Default value."""

    METRIC_DC_VOLTAGE = 1
    """DC electricity metrics"""

    METRIC_DC_CURRENT = 2
    METRIC_DC_POWER = 3
    METRIC_AC_FREQUENCY = 10
    """General AC electricity metrics"""

    METRIC_AC_VOLTAGE = 11
    METRIC_AC_VOLTAGE_PHASE_1 = 12
    METRIC_AC_VOLTAGE_PHASE_2 = 13
    METRIC_AC_VOLTAGE_PHASE_3 = 14
    METRIC_AC_APPARENT_CURRENT = 15
    METRIC_AC_APPARENT_CURRENT_PHASE_1 = 16
    METRIC_AC_APPARENT_CURRENT_PHASE_2 = 17
    METRIC_AC_APPARENT_CURRENT_PHASE_3 = 18
    METRIC_AC_APPARENT_POWER = 20
    """AC power metrics"""

    METRIC_AC_APPARENT_POWER_PHASE_1 = 21
    METRIC_AC_APPARENT_POWER_PHASE_2 = 22
    METRIC_AC_APPARENT_POWER_PHASE_3 = 23
    METRIC_AC_ACTIVE_POWER = 24
    METRIC_AC_ACTIVE_POWER_PHASE_1 = 25
    METRIC_AC_ACTIVE_POWER_PHASE_2 = 26
    METRIC_AC_ACTIVE_POWER_PHASE_3 = 27
    METRIC_AC_REACTIVE_POWER = 28
    METRIC_AC_REACTIVE_POWER_PHASE_1 = 29
    METRIC_AC_REACTIVE_POWER_PHASE_2 = 30
    METRIC_AC_REACTIVE_POWER_PHASE_3 = 31
    METRIC_AC_POWER_FACTOR = 40
    """AC Power factor"""

    METRIC_AC_POWER_FACTOR_PHASE_1 = 41
    METRIC_AC_POWER_FACTOR_PHASE_2 = 42
    METRIC_AC_POWER_FACTOR_PHASE_3 = 43
    METRIC_AC_APPARENT_ENERGY = 50
    """AC energy metrics"""

    METRIC_AC_APPARENT_ENERGY_PHASE_1 = 51
    METRIC_AC_APPARENT_ENERGY_PHASE_2 = 52
    METRIC_AC_APPARENT_ENERGY_PHASE_3 = 53
    METRIC_AC_ACTIVE_ENERGY = 54
    METRIC_AC_ACTIVE_ENERGY_PHASE_1 = 55
    METRIC_AC_ACTIVE_ENERGY_PHASE_2 = 56
    METRIC_AC_ACTIVE_ENERGY_PHASE_3 = 57
    METRIC_AC_ACTIVE_ENERGY_CONSUMED = 58
    METRIC_AC_ACTIVE_ENERGY_CONSUMED_PHASE_1 = 59
    METRIC_AC_ACTIVE_ENERGY_CONSUMED_PHASE_2 = 60
    METRIC_AC_ACTIVE_ENERGY_CONSUMED_PHASE_3 = 61
    METRIC_AC_ACTIVE_ENERGY_DELIVERED = 62
    METRIC_AC_ACTIVE_ENERGY_DELIVERED_PHASE_1 = 63
    METRIC_AC_ACTIVE_ENERGY_DELIVERED_PHASE_2 = 64
    METRIC_AC_ACTIVE_ENERGY_DELIVERED_PHASE_3 = 65
    METRIC_AC_REACTIVE_ENERGY = 66
    METRIC_AC_REACTIVE_ENERGY_PHASE_1 = 67
    METRIC_AC_REACTIVE_ENERGY_PHASE_2 = 69
    METRIC_AC_REACTIVE_ENERGY_PHASE_3 = 70
    METRIC_AC_THD_CURRENT = 80
    """AC harmonics"""

    METRIC_AC_THD_CURRENT_PHASE_1 = 81
    METRIC_AC_THD_CURRENT_PHASE_2 = 82
    METRIC_AC_THD_CURRENT_PHASE_3 = 83
    METRIC_BATTERY_CAPACITY = 101
    """General BMS metrics."""

    METRIC_BATTERY_SOC_PCT = 102
    METRIC_BATTERY_TEMPERATURE = 103
    METRIC_INVERTER_TEMPERATURE = 120
    """General inverter metrics."""

    METRIC_EV_CHARGER_TEMPERATURE = 140
    """EV charging station metrics."""

    METRIC_SENSOR_WIND_SPEED = 160
    """General sensor metrics"""

    METRIC_SENSOR_WIND_DIRECTION = 162
    METRIC_SENSOR_TEMPERATURE = 163
    METRIC_SENSOR_RELATIVE_HUMIDITY = 164
    METRIC_SENSOR_DEW_POINT = 165
    METRIC_SENSOR_AIR_PRESSURE = 166
    METRIC_SENSOR_IRRADIANCE = 167


@dataclass(eq=False, repr=False)
class Bounds(betterproto.Message):
    """
    A set of lower and upper bounds for any metric. The units of the bounds are
    always the same as the related metric.
    """

    lower: Optional[float] = betterproto.float_field(1, optional=True, group="_lower")
    """The lower bound. If absent, there is no lower bound."""

    upper: Optional[float] = betterproto.float_field(2, optional=True, group="_upper")
    """The upper bound. If absent, there is no upper bound."""


@dataclass(eq=False, repr=False)
class SimpleMetricSample(betterproto.Message):
    """
    Represents a single sample of a specific metric, the value of which is
    either measured or derived at a particular time.
    """

    value: float = betterproto.float_field(2)
    """The value of the metric, which could be either measured or derived."""


@dataclass(eq=False, repr=False)
class AggregatedMetricSample(betterproto.Message):
    """
    Encapsulates derived statistical summaries of a single metric. The message
    allows for the reporting of statistical summaries — minimum, maximum, and
    average values - as well as the complete list of individual samples if
    available. This message represents derived metrics and contains fields for
    statistical summaries—minimum, maximum, and average values. Individual
    measurements are are optional, accommodating scenarios where only subsets
    of this information are available.
    """

    avg_value: float = betterproto.float_field(2)
    """The derived average value of the metric."""

    min_value: Optional[float] = betterproto.float_field(
        3, optional=True, group="_min_value"
    )
    """The minimum measured value of the metric."""

    max_value: Optional[float] = betterproto.float_field(
        4, optional=True, group="_max_value"
    )
    """The maximum measured value of the metric."""

    raw_values: List[float] = betterproto.float_field(5)
    """Optional array of all the raw individual values."""


@dataclass(eq=False, repr=False)
class MetricSampleVariant(betterproto.Message):
    """
    MetricSampleVariant serves as a union type that can encapsulate either a
    `SimpleMetricSample` or an `AggregatedMetricSample`. This message is
    designed to offer flexibility in capturing different granularities of
    metric samples—either a simple single-point measurement or an aggregated
    set of measurements for a metric. A `MetricSampleVariant` can hold either a
    `SimpleMetricSample` or an `AggregatedMetricSample`, but not both
    simultaneously. Setting one will nullify the other.
    """

    simple_metric: "SimpleMetricSample" = betterproto.message_field(
        1, group="metric_sample_type"
    )
    aggregated_metric: "AggregatedMetricSample" = betterproto.message_field(
        2, group="metric_sample_type"
    )


@dataclass(eq=False, repr=False)
class MetricSample(betterproto.Message):
    """
    Representation of a sampled metric along with its value. !!! note     This
    represents a single sample of a specific metric, the value of which     is
    either measured or derived at a particular time. The real-time     system-
    defined bounds are optional and may not always be present or set. !!! note
    ### Relationship Between Bounds and Metric Samples     Suppose a metric
    sample for active power has a lower-bound of -10,000 W,     and an upper-
    bound of 10,000 W. For the system to accept a charge     command, clients
    need to request current values within the bounds.
    """

    sampled_at: datetime = betterproto.message_field(1)
    """The UTC timestamp of when the metric was sampled."""

    metric: "Metric" = betterproto.enum_field(2)
    """The metric that was sampled."""

    sample: "MetricSampleVariant" = betterproto.message_field(3)
    """The value of the sampled metric."""

    bounds: List["Bounds"] = betterproto.message_field(4)
    """
    List of bounds that apply to the metric sample. These bounds adapt in real-
    time to reflect the operating conditions at the time of aggregation or
    derivation. #### Multiple Bounds In the case of certain components like
    batteries, multiple bounds might exist. These multiple bounds collectively
    extend the range of allowable values, effectively forming a union of all
    given bounds. In such cases, the value of the metric must be within at
    least one of the bounds. In accordance with the passive sign convention,
    bounds that limit discharge would have negative numbers, while those
    limiting charge, such as for the State of Power (SoP) metric, would be
    positive. Hence bounds can have positive and negative values depending on
    the metric they represent. #### Example The diagram below illustrates the
    relationship between the bounds. ```      bound[0].lower
    bound[1].upper
    <-------|============|------------------|============|--------->
    bound[0].upper      bound[1].lower ``` ---- values here are disallowed and
    will be rejected ==== values here are allowed and will be accepted
    """
