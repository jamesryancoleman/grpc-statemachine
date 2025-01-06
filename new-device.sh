# create the first device
DEVICE_ID=$(mkd -n example-device-1 -l home)
add -driver.name grpc-example -addr localhost:50061 $DEVICE_ID
echo "created dev:$DEVICE_ID"

# add its points 
PT1=$(mkd -p -n co2 -t brick:CO2_Sensor $DEVICE_ID)
PT2=$(mkd -p -n air_temp -t brick:Air_Temperature_Sensor $DEVICE_ID)
PT3=$(mkd -p -n air_temp_setpoint -t brick:Air_Temperature_Setpoint $DEVICE_ID)
PT4=$(mkd -p -n humidity -t brick:Humidity_Sensor $DEVICE_ID)
PT5=$(mkd -p -n status -t brick:On_Off_Status $DEVICE_ID)
PT6=$(mkd -p -n power_draw -t brick:Power_Sensor $DEVICE_ID)

# add xrefs
add -xref http://test-device-1/co2 $PT1
add -xref http://test-device-1/air-temp $PT2
add -xref http://test-device-1/air-temp-setpoint $PT3
add -xref http://test-device-1/humid $PT4
add -xref http://test-device-1/status $PT5
add -xref http://test-device-1/power $PT6

echo "created dev:$DEVICE_ID/pts/$PT1"
echo "created dev:$DEVICE_ID/pts/$PT2"
echo "created dev:$DEVICE_ID/pts/$PT3"
echo "created dev:$DEVICE_ID/pts/$PT4"
echo "created dev:$DEVICE_ID/pts/$PT5"
echo "created dev:$DEVICE_ID/pts/$PT6"

# create the second device
DEVICE_ID=$(mkd -n example-device-2 -l home)
add -driver.name grpc-example $DEVICE_ID
echo "created dev:$DEVICE_ID"

PT1=$(mkd -p -n air_temp_west -t brick:Air_Temperature_Sensor $DEVICE_ID)
PT2=$(mkd -p -n air_temp_stpt_west -t brick:Air_Temperature_Setpoint $DEVICE_ID)
PT3=$(mkd -p -n humidity_west -t brick:Humidity_Sensor $DEVICE_ID)

add -xref http://test-device-2/air-temp $PT1
add -xref http://test-device-2/air-temp-setpoint $PT2
add -xref http://test-device-2/humid $PT3

echo "created dev:$DEVICE_ID/pts/$PT1"
echo "created dev:$DEVICE_ID/pts/$PT2"
echo "created dev:$DEVICE_ID/pts/$PT3"

# create the third device
DEVICE_ID=$(mkd -n example-device-3 -l home)
add -driver.name grpc-example $DEVICE_ID
echo "created dev:$DEVICE_ID"

PT1=$(mkd -p -n air_temp_east -t brick:Air_Temperature_Sensor $DEVICE_ID)
PT2=$(mkd -p -n air_temp_stpt_east -t brick:Air_Temperature_Setpoint $DEVICE_ID)
PT3=$(mkd -p -n humidity_east -t brick:Humidity_Sensor $DEVICE_ID)

add -xref http://test-device-3/air-temp $PT1
add -xref http://test-device-3/air-temp-setpoint $PT2
add -xref http://test-device-3/humid $PT3

echo "created dev:$DEVICE_ID/pts/$PT1"
echo "created dev:$DEVICE_ID/pts/$PT2"
echo "created dev:$DEVICE_ID/pts/$PT3"