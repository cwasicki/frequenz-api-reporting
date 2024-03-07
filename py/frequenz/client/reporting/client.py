import asyncio
from dataclasses import dataclass
from datetime import datetime
from pprint import pprint

import grpc.aio as grpcaio
from frequenz.api.common.v1.metrics import metric_sample_pb2
from frequenz.api.common.v1.microgrid import microgrid_pb2
from frequenz.api.common.v1.pagination import pagination_params_pb2
from frequenz.api.reporting.v1 import reporting_pb2, reporting_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp

from typing import Self

###############################################################################
# To be replaced with:
# https://github.com/frequenz-floss/frequenz-client-common-python/pull/21
from enum import Enum
# pylint: disable=no-name-in-module
from frequenz.api.common.v1.metrics.metric_sample_pb2 import Metric as PBMetric
# pylint: enable=no-name-in-module
class Metric(Enum):
    UNSPECIFIED = PBMetric.METRIC_UNSPECIFIED
    DC_VOLTAGE = PBMetric.METRIC_DC_VOLTAGE
    DC_CURRENT = PBMetric.METRIC_DC_CURRENT
    DC_POWER = PBMetric.METRIC_DC_POWER
    @classmethod
    def from_proto(cls, metric: PBMetric.ValueType) -> Self:
        if not any(m.value == metric for m in cls):
            return Metric.UNSPECIFIED
        return cls(metric)
    def to_proto(self) -> PBMetric.ValueType:
        return self.value
###############################################################################


@dataclass(frozen=True)
class MicrogridComponentsDataPage:

    _data_pb: reporting_pb2.ListMicrogridComponentsDataResponse

    def to_dict_simple(self):

        data = self._data_pb

        ret = {}
        for mdata in data.microgrids:
            mid = mdata.microgrid_id
            ret[mid] = {}
            for cdata in mdata.components:
                cid = cdata.component_id
                if cid not in ret[mid]:
                    ret[mid][cid] = {}
                for msample in cdata.metric_samples:
                    ts = msample.sampled_at.ToDatetime()
                    met = msample.metric
                    if ts not in ret[mid][cid]:
                        ret[mid][cid][ts] = {}
                    ret[mid][cid][ts][met] = msample.sample.simple_metric.value
        return ret

    @property
    def next_page_token(self):
        return self._data_pb.pagination_info.next_page_token


class ReportingClient:
    def __init__(self, service_address):
        self._grpc_channel = grpcaio.insecure_channel(service_address)
        self._stub = reporting_pb2_grpc.ReportingStub(self._grpc_channel)

    async def iter_microgrid_components_data_pages(
        self,
        *,
        microgrid_components: list[tuple[int, list[int]]],
        metrics: list[Metric],
        start_dt: datetime,
        end_dt: datetime,
        page_size: int = 1000,
    ):
        microgrid_components = [
            microgrid_pb2.MicrogridComponentIDs(
                microgrid_id=mid,
                component_ids=cids,
            )
            for mid, cids in microgrid_components
        ]

        def dt2ts(dt):
            ts = Timestamp()
            ts.FromDatetime(dt)
            return ts

        time_filter = reporting_pb2.TimeFilter(
            start=dt2ts(start_dt),
            end=dt2ts(end_dt),
        )

        list_filter = reporting_pb2.ListMicrogridComponentsDataRequest.ListFilter(
            resampling_options=None,
            time_filter=time_filter,
            include_options=None,
        )

        page_token = None

        while True:
            pagination_params = pagination_params_pb2.PaginationParams(
                page_size=page_size,
                page_token=page_token,
            )

            response = await self.fetch_page(
                microgrid_components=microgrid_components,
                metrics=metrics,
                list_filter=list_filter,
                pagination_params=pagination_params,
            )

            if not response:
                break

            yield response

            page_token = response.next_page_token
            if not page_token:
                break

    async def fetch_page(
        self, microgrid_components, metrics, list_filter, pagination_params
    ):
        try:
            response = await self._stub.ListMicrogridComponentsData(
                reporting_pb2.ListMicrogridComponentsDataRequest(
                    microgrid_components=microgrid_components,
                    metrics=metrics,
                    filter=list_filter,
                    pagination_params=pagination_params,
                )
            )
        except grpcaio.AioRpcError as e:
            print(f"RPC failed: {e}")
            return None
        return MicrogridComponentsDataPage(response)

    async def close(self):
        await self._grpc_channel.close()
