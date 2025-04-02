rooms = [
    'Living Room',     
    'Bedroom',         
    'Children Room',  
    'Dining Room',    
    'Kichen',          
    'Gym',             
    'Garden',         
    'Office',           
    'Tv Room',          
]

devices = [
    {
        "device_uuid": "2667fbd5-c088-40d3-bb6e-d5b312dd21e8",
        "device_name": "Main Switch",
        "room_id": 0,
        "device_type": "SWITCH_1CH",
        "link_type": "LIVE",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "c69788ae-c1a3-4dc3-8c0d-85621b22dd72",
        "device_name": "Main Switch Panel",
        "room_id": 0,
        "device_type": "SWITCH_4CH",
        "link_type": "LIVE",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "a6ab47dc-deac-483f-8cf6-c3d678495aef",
        "device_name": "Main Plug",
        "room_id": 0,
        "device_type": "PLUG_1CH",
        "link_type": "LIVE",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "8026686d-d548-411f-a474-328bad24c2c5",
        "device_name": "Main Dimmer",
        "room_id": 0,
        "device_type": "DIMMER_2CH",
        "link_type": "LIVE",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "f3ee8839-a8d6-461d-b1fc-307e4bb28203",
        "device_name": "Main Dimmer Panel",
        "room_id": 0,
        "device_type": "DIMMER_4CH",
        "link_type": "LIVE",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "083a5491-b411-4052-ad28-909b6578aace",
        "device_name": "Main RGB",
        "room_id": 0,
        "device_type": "RGB",
        "link_type": "LIVE",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "f4e8140d-7de5-4270-b826-0ef275d4e789",
        "device_name": "Temperature Sensor",
        "room_id": 0,
        "device_type": "TEMP",
        "link_type": "SUSPEND",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "e938a34f-e807-451f-bdaa-c91dde181afd",
        "device_name": "Air Quality Sensor",
        "room_id": 0,
        "device_type": "AIR_Q",
        "link_type": "SUSPEND",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "829853cd-71ce-4840-a550-30a51551e1ac",
        "device_name": "Humidity Sensor",
        "room_id": 0,
        "device_type": "HUMD",
        "link_type": "SUSPEND",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "b65b2e54-68d0-4f4b-9cf7-f09d8e921106",
        "device_name": "Security Lock",
        "room_id": 0,
        "device_type": "SEC_LOCK",
        "link_type": "SUSPEND",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "100f08d5-b466-434b-be72-8bdbae5ea54d",
        "device_name": "Flood Sensor",
        "room_id": 0,
        "device_type": "FLOOD",
        "link_type": "SUSPEND",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "87bfb75b-4086-414a-a218-0173aff010b6",
        "device_name": "Motion Sensor",
        "room_id": 0,
        "device_type": "MOTION",
        "link_type": "LIVE",
        "device_config": {"motion_sensor_mode":'NORMAL'},
        "is_online": False
    },
    
    
    {
        "device_uuid": "bf7bd296-a185-4df4-80ac-1d9b019887a0",
        "device_name": "Temperature Sensor",
        "room_id": 1,
        "device_type": "TEMP",
        "link_type": "SUSPEND",
        "device_config": {},
        "is_online": False
    },
     {
        "device_uuid": "c8081956-85c1-4b6c-be3e-17b7f9c11c3e",
        "device_name": "Air Quality Sensor",
        "room_id": 1,
        "device_type": "AIR_Q",
        "link_type": "SUSPEND",
        "device_config": {},
        "is_online": False
    },
    {
        "device_uuid": "136109d5-c658-41ff-8ea9-3d131cc80221",
        "device_name": "Humidity Sensor",
        "room_id": 1,
        "device_type": "HUMD",
        "link_type": "SUSPEND",
        "device_config": {},
        "is_online": False
    },
]

mapped_devices = []
for room in rooms:
    mapped_devices.append([])
    
for  device in devices:
    mapped_devices[device['room_id']].append(device)