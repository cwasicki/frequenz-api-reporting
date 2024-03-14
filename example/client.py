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
from frequenz.client.common.metric import Metric

async def component_data_df(*, metrics, **kwargs):
    import pandas as pd
    data = [cd async for cd in component_data_gen(metrics=metrics, **kwargs)]
    columns = ["ts"] + metrics
    return pd.DataFrame(data, columns=columns).set_index("ts")

async def main():

    service_address = "localhost:50051"
    client = ReportingClient(service_address)

    # Request parameters
    MICROGRID_ID = 10
    COMPONENT_ID = 61
    microgrid_components = [(MICROGRID_ID, [COMPONENT_ID])]
    metrics = [
        Metric.DC_POWER,
        Metric.DC_CURRENT,
    ]

    start_dt = datetime.fromisoformat("2023-11-21T12:00:00.00+00:00")
    end_dt = datetime.fromisoformat("2023-11-21T12:01:00.00+00:00")

    page_size = 10


    print("########################################################")
    print("Iterate over generator")
    gen = lambda: client.components_data_iter(
        microgrid_components=microgrid_components,
        metrics=metrics,
        start_dt=start_dt,
        end_dt=end_dt,
        page_size=page_size,
    )
    async for sample in gen():
        print("Received:", sample)

    print("########################################################")
    print("Dumping all data as a single dict")
    dct = await client.components_data_dict(
        microgrid_components=microgrid_components,
        metrics=metrics,
        start_dt=start_dt,
        end_dt=end_dt,
        page_size=page_size,
    )
    pprint(dct)


    print("########################################################")
    print("Turn data into a pandas DataFrame")
    import pandas as pd
    data = [cd async for cd in gen()]
    columns = ["ts", "mid", "cid", "metric", "value"]
    df = pd.DataFrame(data, columns=columns).set_index("ts")

    pprint(df)

asyncio.run(main())
