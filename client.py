import device_pb2_grpc
import device_pb2
import grpc

import datetime as dt

DEST_ADDR = 'localhost:50063'

def Get(key:str, addr=DEST_ADDR) -> device_pb2.GetResponse:
    response: device_pb2.GetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)
        response = stub.Get(device_pb2.GetRequest(
            Key=key
        ))
        if response.Error > 0:
            print("get '{}' error: {}".format(response.Response.Key,
                                              response.Response.Error))
    return response

def Set(key:str, value:str, addr=DEST_ADDR) -> device_pb2.SetResponse:
    response: device_pb2.SetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)
        response = stub.Set(device_pb2.SetRequest(
            Key=key, 
            Value=value,
        ))
        if not response.Ok:
            print("set '{}' error: {}".format(response.Response.Key,
                                              response.Response.Error))
    return response

def GetMutiple(keys:list[str], addr=DEST_ADDR) -> device_pb2.GetMultipleResponse:
    responses: device_pb2.GetMultipleResponse
    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)
        responses = stub.GetMultiple(
            device_pb2.GetMultipleRequest(
                Keys=keys
            )
        )
    return responses

def SetMultiple(key_value_pairs:tuple[str,str], addr=DEST_ADDR) -> device_pb2.SetMultipleResponse:
    responses : device_pb2.SetMultipleResponse
    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)
        responses = stub.SetMultiple(
            device_pb2.SetMultipleRequest(
                Requests=[device_pb2.SetRequest(Key=t[0], Value=t[1]) for t in key_value_pairs]
            )
        )
    return responses

