import asyncio
import grpc.aio as grpcaio

from frequenz.api.reporting.v1 import (
    reporting_pb2_grpc,
    reporting_pb2,
)

from frequenz.api.common.v1.metrics import metric_sample_pb2
from frequenz.api.common.v1.microgrid import microgrid_pb2

from frequenz.api.common.v1.pagination import (
    pagination_params_pb2,
)


from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

from pprint import pprint

def dt2ts(dt):
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


class ReportingClient:
    def __init__(self, service_address):
        self._grpc_channel = grpcaio.insecure_channel(service_address)
        self._stub = reporting_pb2_grpc.ReportingStub(self._grpc_channel)

    async def list_microgrid_components_data(
        self,
        microgrid_components: list[tuple[int, list[int]]],
        metrics,
        start_dt,
        end_dt,
        page_size,
    ):
        microgrid_components = [
            microgrid_pb2.MicrogridComponentIDs(
                microgrid_id=mid,
                component_ids=cids,
            )
            for mid, cids in microgrid_components
        ]

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

        for i in range(300):
            pagination_params = pagination_params_pb2.PaginationParams(
                page_size=page_size,
                page_token=page_token,
            )

            response = await self._list_microgrid_components_data_page(
                microgrid_components,
                metrics,
                list_filter,
                pagination_params,
            )

            page_token = response.pagination_info.next_page_token
            yield self._parse_response(response)
            print("Next page token:", page_token)
            if not page_token:
                break

    async def _list_microgrid_components_data_page(
        self,
        microgrid_components,
        metrics,
        list_filter,
        pagination_params,
    ):
        response = await self._stub.ListMicrogridComponentsData(
            reporting_pb2.ListMicrogridComponentsDataRequest(
                microgrid_components=microgrid_components,
                metrics=metrics,
                filter=list_filter,
                pagination_params=pagination_params,
            )
        )

        return response

    @staticmethod
    def _parse_response(data):

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

    async def close(self):
        await self._grpc_channel.close()


async def main():

    service_address = "localhost:50051"
    client = ReportingClient(service_address)
    async for response in client.list_microgrid_components_data(
            microgrid_components=[
                (10, [61]),
            ],
            metrics=[
                metric_sample_pb2.Metric.METRIC_DC_POWER,
                metric_sample_pb2.Metric.METRIC_DC_CURRENT,
            ],
            start_dt=datetime.fromisoformat("2023-11-21T12:00:00.00+00:00"),
            end_dt=datetime.fromisoformat("2023-11-21T12:30:00.00+00:00"),
            page_size=10,
        ):
        pprint(response)

asyncio.run(main())
