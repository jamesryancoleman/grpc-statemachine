# create the device
DEVICE_ID=$(mkd -n 'statemachine')
# add -driver.name grpc-example $DEVICE_ID
echo "created dev:$DEVICE_ID"

# add its points 
PT1=$(mkd -p -n co2 -t brick:CO2_Sensor $DEVICE_ID)
PT2=$(mkd -p -n air_temp -t brick:Air_Temperature_Sensor $DEVICE_ID)
PT3=$(mkd -p -n air_temp_setpoint -t brick:Air_Temperature_Setpoint $DEVICE_ID)
PT4=$(mkd -p -n humidity -t brick:Humidity_Sensor $DEVICE_ID)
PT5=$(mkd -p -n status -t brick:On_Off_Status $DEVICE_ID)
PT6=$(mkd -p -n power_draw -t brick:Power_Sensor $DEVICE_ID)

# add xrefs
add -xref http://virtual-device.local/co2 $PT1
add -xref http://virtual-device.local/air-temp $PT2
add -xref http://virtual-device.local/air-temp-setpoint $PT3
add -xref http://virtual-device.local/humid $PT4
add -xref http://virtual-device.local/status $PT5
add -xref http://virtual-device.local/power $PT6

echo "created dev:$DEVICE_ID/pts/$PT1"
echo "created dev:$DEVICE_ID/pts/$PT2"
echo "created dev:$DEVICE_ID/pts/$PT3"
echo "created dev:$DEVICE_ID/pts/$PT4"
echo "created dev:$DEVICE_ID/pts/$PT5"
echo "created dev:$DEVICE_ID/pts/$PT6"