import asyncio
import grpc.aio as grpcaio
from dataclasses import dataclass

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

from frequenz.client.reporting import ReportingClient

async def component_data_dict(
    client,
    microgrid_id: int,
    component_id: int,
    metrics,
    start_dt: datetime,
    end_dt: datetime,
    page_size: int,
):
    microgrid_components = [(microgrid_id, [component_id])]
    ret = {}
    async for response in client.iter_microgrid_components_data_pages(
        microgrid_components=microgrid_components,
        metrics=metrics,
        start_dt=start_dt,
        end_dt=end_dt,
        page_size=page_size,
    ):
        d = response.to_dict_simple()
        ret = {**ret, **d[microgrid_id][component_id]}
    return ret

async def component_data_gen(
    *,
    client,
    microgrid_id: int,
    component_id: int,
    metrics,
    start_dt: datetime,
    end_dt: datetime,
    page_size: int,
):
    microgrid_components = [(microgrid_id, [component_id])]
    async for response in client.iter_microgrid_components_data_pages(
        microgrid_components=microgrid_components,
        metrics=metrics,
        start_dt=start_dt,
        end_dt=end_dt,
        page_size=page_size,
    ):
        d = response.to_dict_simple()
        d = d[microgrid_id][component_id]
        for ts, mets in d.items():
            vals = [mets.get(k) for k in metrics]
            yield ts, *vals

async def component_data_df(*, metrics, **kwargs):
    import pandas as pd
    data = [cd async for cd in component_data_gen(metrics=metrics, **kwargs)]
    columns = ["ts"] + metrics
    return pd.DataFrame(data, columns=columns).set_index("ts")

async def main():

    service_address = "localhost:50051"
    client = ReportingClient(service_address)
    print("########################################################")
    print("Fetching dict")
    dct = await component_data_dict(
        client,
        microgrid_id=10,
        component_id=61,
        metrics=[
            metric_sample_pb2.Metric.METRIC_DC_POWER,
            metric_sample_pb2.Metric.METRIC_DC_CURRENT,
        ],
        start_dt=datetime.fromisoformat("2023-11-21T12:00:00.00+00:00"),
        end_dt=datetime.fromisoformat("2023-11-21T12:30:00.00+00:00"),
        page_size=10,
    )
    pprint(dct)

    print("########################################################")
    print("Fetching generator")
    async for samples in component_data_gen(
        client=client,
        microgrid_id=10,
        component_id=61,
        metrics=[
            metric_sample_pb2.Metric.METRIC_DC_POWER,
            metric_sample_pb2.Metric.METRIC_DC_CURRENT,
        ],
        start_dt=datetime.fromisoformat("2023-11-21T12:00:00.00+00:00"),
        end_dt=datetime.fromisoformat("2023-11-21T12:30:00.00+00:00"),
        page_size=10,
    ):
        print("Received:", samples)

    print("########################################################")
    print("Fetching df")
    df = await component_data_df(
        client=client,
        microgrid_id=10,
        component_id=61,
        metrics=[
            metric_sample_pb2.Metric.METRIC_DC_POWER,
            metric_sample_pb2.Metric.METRIC_DC_CURRENT,
        ],
        start_dt=datetime.fromisoformat("2023-11-21T12:00:00.00+00:00"),
        end_dt=datetime.fromisoformat("2023-11-21T12:30:00.00+00:00"),
        page_size=10,
    )
    pprint(df)



asyncio.run(main())
