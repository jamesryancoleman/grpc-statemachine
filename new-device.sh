# create the device
DEVICE_ID=$(mkd -n example-device -l SouthSt)
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
add -xref http://virtual-device/co2 $PT1
add -xref http://virtual-device/air-temp $PT2
add -xref http://virtual-device/air-temp-setpoint $PT3
add -xref http://virtual-device/humid $PT4
add -xref http://virtual-device/status $PT5
add -xref http://virtual-device/power $PT6

echo "created dev:$DEVICE_ID/pts/$PT1"
echo "created dev:$DEVICE_ID/pts/$PT2"
echo "created dev:$DEVICE_ID/pts/$PT3"
echo "created dev:$DEVICE_ID/pts/$PT4"
echo "created dev:$DEVICE_ID/pts/$PT5"
echo "created dev:$DEVICE_ID/pts/$PT6"