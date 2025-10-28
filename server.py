from concurrent import futures
import logging
import json
import sys

import statemachine as sm

import comms_pb2_grpc
import comms_pb2
import grpc

SERVE_PORT = "50061"

# the point_map is a collection of URIs that map to points in the internal namespace
point_map = {}

def LoadPointMap(path:str='known_points.json'):
    global point_map
    f = open(path, 'r')
    raw = f.read()
    tmp = json.loads(raw)
    point_map = tmp['known_points']
    print("known external points:")
    for k, v in point_map.items():
        print('\t',k, "->",v)

class GetSetRunServicer(comms_pb2_grpc.GetSetRunServicer):
    def Get(self, request:comms_pb2.GetRequest, context):
        print("received Get request: ")
        header = comms_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)
        
        # Get receives a bunch of point ids
        pairs = []
        for key in request.Keys:
            # only populate as needed
            value:str = "" # default to empty string
            error = None
            error_msg = None
            dtype = None

            if key in point_map:
                internal_addr = point_map[key] # request.Key is the bos point (e.g., "4.2")
                if internal_addr in registry:
                    ref = registry[internal_addr] # tuple[object, key:str]
                    value = ref[0].get_point(ref[1])
                    dtype = sm.GetDtype(value)

                    logging.info("{} -> '{}'".format(key, value))
                    ref[0].mutate_point(ref[1])

            else:
                error_msg = "key {} is unknown to grpc-server".format(key)
                error = comms_pb2.GET_ERROR_KEY_DOES_NOT_EXIST
                print("{} get error: not in registry".format(key))
            pairs.append(comms_pb2.GetPair(
                Key=key,
                Value=str(value),
                Dtype=dtype,
                Error=error,
                ErrorMsg=error_msg
            ))
        return comms_pb2.GetResponse(
            Header=header,
            Pairs=pairs
        )
        
    def Set(self, request:comms_pb2.SetRequest, context):
        print("received Set request:" )
        header = comms_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)        

        response_pairs:list[comms_pb2.SetPair] = []

        for p in request.Pairs:
            key = p.Key
            value = p.Value
            if key in point_map:
                internal_addr = point_map[key]
                if internal_addr in registry:
                    ref = registry[internal_addr]
                    ok = ref[0].set_point(ref[1], value)
                    if ok:
                        response_pairs.append(comms_pb2.SetPair(
                            Ok=True,
                            Key=key,
                            Value=value,
                        ))
                        print(key, "<-", value)
                    else:
                        err_msg = "unable to set key '{}' to value '{}'".format(key, value)
                        response_pairs.append(comms_pb2.SetPair(
                            Ok=False,
                            Key=key,
                            Value=value,
                            ErrorMsg=err_msg))
            else:
                response_pairs.append(comms_pb2.SetPair(
                    Ok=False,
                    Key=key,
                    Value=value,
                    Error=comms_pb2.SET_ERROR_KEY_DOES_NOT_EXIST,
                    ErrorMsg="key {} not known to grpc-example server".format(key)
                )) 
        return comms_pb2.SetResponse(
            Header=header,
            Pairs=response_pairs
        )  


if __name__ == "__main__":
    if len(sys.argv) > 1:
        SERVE_PORT = sys.argv[1]
        print("using custom server port {}".format(SERVE_PORT))
    else:
        print("using default server port")

    # load the external to internal map
    LoadPointMap()
    
    # example devices and their points
    d1 = sm.Device()
    d1.add_point('time', 'last-modified')
    d1.add_point('int', 'present-value')

    d2 = sm.Device()
    d2.add_point('str', 'note')

    d3 = sm.Device()
    d3.add_point('float', 'mean')
    d3.add_point('float', 'median')

    d5 = sm.Device()
    d5.add_point('int', 'co2')
    d5.add_point('float', 'air-temp')
    d5.add_point('float', 'air-temp-setpoint')
    d5.add_point('int', 'humid')
    d5.add_point('bool', 'status')
    d5.add_point('float', 'power')
    d5.add_point('time', 'start-time')

    d6 = sm.Device()
    d6.add_point('float', 'air-temp')
    d6.add_point('float', 'air-temp-setpoint')
    d6.add_point('int', 'humid')

    d7 = sm.Device()
    d7.add_point('float', 'air-temp')
    d7.add_point('float', 'air-temp-setpoint')
    d7.add_point('int', 'humid')

    # overwrite defaults
    d5.set_point('co2', 410)
    d5.set_point('air-temp', 18.0)
    d5.set_point('air-temp-setpoint', 21.0)
    d5.set_point('humid', 55)
    d5.set_point('power', 240)

    d6.set_point('air-temp', 19.0)
    d6.set_point('air-temp-setpoint', 21.0)
    d6.set_point('humid', 53)

    d7.set_point('air-temp', 20.0)
    d7.set_point('air-temp-setpoint', 21.0)
    d7.set_point('humid', 50)

    # create a flat mapping between internal point ids and an access method
    # the internal point keys are used to index internal to devices and points
    registry = {
        # device 1
        "1": (d1, 'last-modified'),
        "2": (d1, 'present-value'),

        # device 2
        "3": (d2, 'note'),

        # device 3
        "4": (d3, 'mean'),
        "5": (d3, 'median'),

        # device 5
        "6": (d5, 'co2'),
        "7": (d5, 'air-temp'),
        "8": (d5, 'air-temp-setpoint'),
        "9": (d5, 'humid'),
        "10": (d5, 'status'),
        "11": (d5, 'power'),
        "12": (d5, 'start-time'),

        # device 6
        "11": (d6, 'air-temp'),
        "12": (d6, 'air-temp-setpoint'),
        "13": (d6, 'humid'),

        # device 7
        "14": (d7, 'air-temp'),
        "15": (d7, 'air-temp-setpoint'),
        "16": (d7, 'humid'),

    }

    # implement grpc server
    def serve():
        port = SERVE_PORT
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        print("Starting server on:", "0.0.0.0:" + port)
        comms_pb2_grpc.add_GetSetRunServicer_to_server(GetSetRunServicer(), server)
        server.add_insecure_port("0.0.0.0:" + port)
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()

    logging.basicConfig()
    serve()

