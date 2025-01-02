import client as c

def get_test(key:str):
    resp = c.Get([key]) # get always takes a list of keys
    v = resp.Pairs[0]
    print(v.Key, "->", v.Value)

def set_test(key:str, value:str):
    resp = c.Set([(key, value)])
    p = resp.Pairs[0]
    print(key1, "<-", p.Value)

def get_multiple_test(keys:list[str]):
    R : c.comms_pb2.GetResponse
    R = c.Get(keys)
    for resp in R.Pairs:
        print("{} -> {}".format(resp.Key, resp.Value))
        if resp.Error > 0 or resp.ErrorMsg:
            print("\terror_code {}: '{}'".format(resp.Error, resp.ErrorMsg))

def set_multiple_test(keys:list[tuple[str, str]]):
    R : c.comms_pb2.SetMultipleResponse
    R = c.Set(keys)
    for resp in R.Pairs:
        print("{} <- {}".format(resp.Key, resp.Value))
        if not resp.Ok:
            print("\tsuccess={}".format(resp.Ok))
        if resp.Error > 0 or resp.ErrorMsg:
            print("\terror {}: {}".format(resp.Error, resp.ErrorMsg))


if __name__ == "__main__":    
    # get test
    print("== Get tests ==")
    key1 = "http://virtual-device/co2"  # int
    get_test(key1)

    # get multiple test
    key2 = "http://virtual-device/air-temp" # float
    key3 = "http://virtual-device/air-temp-setpoint"  # float
    key4 = "http://virtual-device/humid"  # int
    key5 = "http://virtual-device/status"  # bool
    key6 = "http://virtual-device/power"  # float
    key7 = "http://virtual-device/start-time"  # time
    get_multiple_test([key2, key3, key4, key5, key6, key7])

    print("\n== set tests ==")
    # set test
    set_test(key1, str(400))

    # set multiple test    
    set_multiple_test([
        (key3, str(23.0)),
        (key5, str(True)),
        (key7, str(c.dt.datetime(2024, 1, 1, hour=12))),
        ])

    print("\n== check set succeeded ==")
    get_multiple_test([key1, key3, key5, key7])

    # mutate the statemachine
    print("\n== trigger mutation on statemachine ==")
    get_multiple_test([key1, key3, key5, key7])
