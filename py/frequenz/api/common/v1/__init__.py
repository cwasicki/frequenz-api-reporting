# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: frequenz/api/common/v1/location.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass

import betterproto


@dataclass(eq=False, repr=False)
class Location(betterproto.Message):
    """
    A pair of geographical co-ordinates, representing the location of a place.
    """

    latitude: float = betterproto.float_field(1)
    """Latitude ranges from -90 (South) to 90 (North)"""

    longitude: float = betterproto.float_field(2)
    """Longitude ranges from -180 (West) to 180 (East)"""

    country_code: str = betterproto.string_field(3)
    """Country ISO 3166-1 Alpha 2"""
