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


import argparse
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

from pprint import pprint

from frequenz.client.reporting import ReportingClient
from frequenz.client.common.metric import Metric


async def main(microgrid_id, component_id):
    service_address = "localhost:50051"
    client = ReportingClient(service_address)

    microgrid_components = [(microgrid_id, [component_id])]
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
    df = pd.DataFrame(data).set_index("timestamp")
    pprint(df)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("microgrid_id", type=int, help="Microgrid ID")
    parser.add_argument("component_id", type=int, help="Component ID")

    args = parser.parse_args()
    asyncio.run(main(args.microgrid_id, args.component_id))
