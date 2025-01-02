import comms_pb2_grpc
import comms_pb2
import grpc

import datetime as dt

DEST_ADDR = 'localhost:50061'

# Get takes a list of keys and returns a GetResponse
def Get(keys:list[str], addr=DEST_ADDR) -> comms_pb2.GetResponse:
    response: comms_pb2.GetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        response = stub.Get(comms_pb2.GetRequest(Keys=keys))
    return response

# Set takes a list of (key,value) tuples and returns a SetResponse
def Set(key_value_pairs:list[tuple[str,str]], addr=DEST_ADDR) -> comms_pb2.SetResponse:
    responses : comms_pb2.SetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        responses = stub.Set(
            comms_pb2.SetRequest(
                Pairs=[comms_pb2.Pair(Key=t[0], Value=t[1]) for t in key_value_pairs]
            )
        )
    return responses

# def Get(key:str, addr=DEST_ADDR) -> comms_pb2.GetResponse:
#     response: comms_pb2.GetResponse
#     with grpc.insecure_channel(addr) as channel:
#         stub = comms_pb2_grpc.GetSetRunStub(channel)
#         response = stub.Get(comms_pb2.GetRequest(
#             Key=key
#         ))
#         if response.Error > 0:
#             print("get '{}' error: {}".format(response.Response.Key,
#                                               response.Response.Error))
#     return response

# def Set(key:str, value:str, addr=DEST_ADDR) -> comms_pb2.SetResponse:
#     response: comms_pb2.SetResponse
#     with grpc.insecure_channel(addr) as channel:
#         stub = comms_pb2_grpc.GetSetRunStub(channel)
#         response = stub.Set(comms_pb2.SetRequest(
#             Pairs=[comms_pb2.Pair(Key=key, Value=value)]))
#         if not response.Ok:
#             print("set '{}' error: {}".format(response.Response.Key,
#                                               response.Response.Error))
#     return response
