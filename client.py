import common_pb2_grpc
import common_pb2
import grpc

import datetime as dt

DEST_ADDR = 'localhost:50061'

# Get takes a list of keys and returns a GetResponse
def Get(keys:list[str], addr=DEST_ADDR) -> common_pb2.GetResponse:
    response: common_pb2.GetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = common_pb2_grpc.DeviceControlStub(channel)
        response = stub.Get(common_pb2.GetRequest(Keys=keys))
    return response

# Set takes a list of (key,value) tuples and returns a SetResponse
def Set(key_value_pairs:list[tuple[str,str]], addr=DEST_ADDR) -> common_pb2.SetResponse:
    responses : common_pb2.SetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = common_pb2_grpc.DeviceControlStub(channel)
        responses = stub.Set(
            common_pb2.SetRequest(
                Pairs=[common_pb2.SetPair(Key=t[0], Value=t[1]) for t in key_value_pairs]
            )
        )
    return responses
