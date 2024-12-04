from client import *

def get_test(key:str):
    resp = Get(key)
    print(key, "->", resp.Value)

def set_test(key:str, value:str):
    resp = Set(key, value)
    print(key1, "<-", resp.Value)

def get_multiple_test(keys:list[str]):
    R : device_pb2.GetMultipleResponse
    R = GetMutiple(keys)
    for resp in R.Responses:
        print("{} -> {}".format(resp.Key, resp.Value))
        if resp.Error > 0 or resp.ErrorMsg:
            print("\terror_code {}: '{}'".format(resp.Error, resp.ErrorMsg))

def set_multiple_test(keys:list[tuple[str, str]]):
    R : device_pb2.SetMultipleResponse
    R = SetMultiple(keys)
    for resp in R.Responses:
        print("{} <- {}".format(resp.Key, resp.Value))
        if not resp.Ok:
            print("\tsuccess={}".format(resp.Ok))
        if resp.Error > 0 or resp.ErrorMsg:
            print("\terror {}: {}".format(resp.Error, resp.ErrorMsg))


if __name__ == "__main__":
    # set this in the client library
    DEST_ADDR = 'localhost:50063'
    
    # get test
    print("== Get tests ==")
    key1 = "http://virtual-device.local/co2"  # int
    get_test(key1)

    # get multiple test
    key2 = "http://virtual-device.local/air-temp" # float
    key3 = "http://virtual-device.local/air-temp-setpoint"  # float
    key4 = "http://virtual-device.local/humid"  # int
    key5 = "http://virtual-device.local/status"  # bool
    key6 = "http://virtual-device.local/power"  # float
    key7 = "http://virtual-device.local/start-time"  # time
    get_multiple_test([key2, key3, key4, key5, key6, key7])

    print("\n== set tests ==")
    # set test
    set_test(key1, str(400))

    # set multiple test    
    set_multiple_test([
        (key3, str(23.0)),
        (key5, str(True)),
        (key7, str(dt.datetime(2024, 1, 1, hour=12))),
        ])

    print("\n== check set succeeded ==")
    get_multiple_test([key1, key3, key5, key7])

    # mutate the statemachine
    print("\n== trigger mutation on statemachine ==")
    get_multiple_test([key1, key3, key5, key7])
