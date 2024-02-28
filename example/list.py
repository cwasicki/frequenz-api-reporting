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
from frequenz.api.reporting.v1 import reporting_pb2

def dt2ts(dt):
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts

async def main():
    target="localhost:50051"

    grpc_channel = grpcaio.insecure_channel(target)

    stub = reporting_pb2_grpc.ReportingStub(grpc_channel)

    microgrid_components = [
        microgrid_pb2.MicrogridComponentIDs(
            microgrid_id=10,
            component_ids=[61],
        )
    ]

    metrics = [metric_sample_pb2.Metric.METRIC_DC_POWER]

    start_dt = datetime.fromisoformat("2023-11-21T05:20:50.52+00:00")
    end_dt = datetime.fromisoformat("2023-11-21T22:20:50.52+00:00")

    time_filter = reporting_pb2.TimeFilter(
        start=dt2ts(start_dt),
        end=dt2ts(end_dt),
    )

    page_token = None

    for i in range(3):
        pagination_params = pagination_params_pb2.PaginationParams(
            page_size=10,
            page_token=page_token,
        )

        response = await stub.ListMicrogridComponentsData(
            reporting_pb2.ListMicrogridComponentsDataRequest(
                microgrid_components=microgrid_components,
                metrics=metrics,
                filter=reporting_pb2.ListMicrogridComponentsDataRequest.ListFilter(
                    resampling_options=None,
                    time_filter=time_filter,
                    include_options=None,
                ),
                pagination_params=pagination_params,
            )
        )

        print(response)
        page_token = response.pagination_info.next_page_token

asyncio.run(main())
