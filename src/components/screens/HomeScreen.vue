<script setup lang="ts">

import { onMounted, shallowRef, ref } from 'vue';
import Tabs from 'primevue/tabs';
import TabList from 'primevue/tablist';
import Tab from 'primevue/tab';
import ProgressSpinner from 'primevue/progressspinner';

import { subscribe } from '@src/lib/mediator';
import { request_data_resource } from '@src/lib/mqtt';
import { Room, Device, DeviceType } from '@src/lib/models';
import Button from 'primevue/button';

import TemperatureLowIcon from '@src/components/icons/TemperatureLowIcon.vue';
import HumidityIcon from '@src/components/icons/HumidityIcon.vue';
import ToggleOnIcon from '@src/components/icons/ToggleOnIcon.vue';
import SettingsSliders from '@src/components/icons/SettingsSliders.vue';
import WifiIcon from '@src/components/icons/WifiIcon.vue';
import SettingsIcon from '@src/components/icons/SettingsIcon.vue';
import PowerIcon from '@src/components/icons/PowerIcon.vue';
import PlugBoltIcon from '@src/components/icons/PlugBoltIcon.vue';
import SensorIcon from '@src/components/icons/SensorIcon.vue';
import HouseFloodIcon from '@src/components/icons/HouseFloodIcon.vue';
import HouseLockIcon from '@src/components/icons/HouseLockIcon.vue';
import ColorPaletteIcon from '@src/components/icons/ColorPaletteIcon.vue';
import BrightnessIcon from '@src/components/icons/BrightnessIcon.vue';

let devices_cache: Device[] = [];

const device_type_icon_map: Record<DeviceType, any> = {
    SWITCH_1CH: ToggleOnIcon,
    SWITCH_4CH: SettingsSliders,
    DIMMER_2CH: BrightnessIcon,
    DIMMER_4CH: BrightnessIcon,
    TEMP: TemperatureLowIcon,
    HUMD: HumidityIcon,
    PLUG_1CH: PlugBoltIcon,
    MOTION: SensorIcon,
    FLOOD: HouseFloodIcon,
    SEC_LOCK: HouseLockIcon,
    RGB: ColorPaletteIcon,
};

const ON_STATES = [
    'ON'
];

const rooms = shallowRef<Room[]>([])
const current_room_temp = ref('-- C');
const current_room_humd = ref('--%');
const devices = shallowRef<Device[]>([]);
const sensor_state_main_map = ref<Record<string, string | null>>({});

let current_room = 0;
const sensor_room_map: Record<string, number> = {};

function room_select(room_id: number) {
    current_room = room_id;
    current_room_temp.value = rooms.value[room_id].temp;
    current_room_humd.value = rooms.value[room_id].humd;
    devices.value = devices_cache.filter(d => d.room_id === room_id);
}

function compute_connection_icon_color(device: Device) {
    if (device.link_type === 'SUSPEND')
        return '#FFAB00';
    else if (device.link_type === 'LIVE' && device.is_online)
        return '#64DD17';
    else if (device.link_type === 'LIVE' && !device.is_online)
        return '#DD2C00';
    else
        return 'var(--p-primary-color)';
}

function device_power_click(_device_uuid: string) {
    // const device_mqtt_id = device_uuid.slice(-4);
    // const power_mqtt_topic = `rpc/${device_mqtt_id}/command_power_0`;
}

onMounted(() => {
    subscribe('data_response_rooms', 'data_response_rooms_home_screen', args => {
        const _rooms = JSON.parse(args.payload) as Room[];
        rooms.value = _rooms;
        current_room_temp.value = _rooms[0].temp;
        current_room_humd.value = _rooms[0].humd;
    });
    subscribe('data_response_devices', 'data_response_devices_home_screen', args => {
        const _devices = JSON.parse(args.payload) as Device[];
        devices_cache = _devices;

        _devices.forEach(d => {
            const device_mqtt_id = d.device_uuid.slice(-4);
            if (['TEMP', 'HUMD'].includes(d.device_type))
                sensor_room_map[device_mqtt_id] = d.room_id;
        });

        room_select(current_room);
    });
    subscribe('mqtt_data_service_ready', 'mqtt_data_service_ready_home_screen', () => {
        request_data_resource('rooms');
        request_data_resource('devices');
    });
    subscribe('sensor_state_main', 'sensor_state_main_home_screen', args => {
        const device_mqtt_id: string = args.device_mqtt_id;
        const payload: string = args.payload;
        sensor_state_main_map.value[device_mqtt_id] = payload;
    });

    // subscribe('sensor_state', 'sensor_state_home_screen', args => {
    //     // handle general sensor state
    //     const device_mqtt_id: string = args.device_mqtt_id;
    //     const payload: string = args.payload;
    //     sensor_state_map.value[device_mqtt_id] = payload;

    //     // handle temp humd sensors
    //     const sensor_type: SensorType = args.sensor_type;
    //     if (!(device_mqtt_id in sensor_room_map))
    //         return;
    //     const _room_id = sensor_room_map[device_mqtt_id];
    //     if (sensor_type === 'TEMP') {
    //         rooms.value[_room_id].temp = payload;
    //         if (_room_id === current_room)
    //             current_room_temp.value = payload;
    //     } else if (sensor_type === 'HUMD') {
    //         rooms.value[_room_id].humd = payload;
    //         if (_room_id === current_room)
    //             current_room_humd.value = payload;
    //     }
    // });
});

</script>

<template>
    <div id="home_screen_cont">
        <div id="temp_humd_section">
            <div class="th_section">
                <div class="ths_icon_cont">
                    <TemperatureLowIcon :fill_color="'#FFFFFF'" style="width: 36px; height: 36px;" />
                </div>
                <div class="ths_text_cont" style="color: #FFFFFF;">
                    <div style="font-size: 20px; font-weight: bold;">{{ current_room_temp }}</div>
                    <div style="font-size: 14px; font-weight: normal;">Temprature</div>
                </div>
            </div>
            <div class="th_section">
                <div class="ths_icon_cont">
                    <HumidityIcon :fill_color="'#FFFFFF'" style="width: 36px; height: 36px;" />
                </div>
                <div class="ths_text_cont" style="color: #FFFFFF;">
                    <div style="font-size: 20px; font-weight: bold;">{{ current_room_humd }}</div>
                    <div style="font-size: 14px; font-weight: normal;">Humidity</div>
                </div>
            </div>
        </div>
        <ProgressSpinner v-if="rooms.length === 0" />
        <Tabs v-else :value="0" scrollable style="max-width: 96vw;" @update:value="room_select">
            <TabList :pt="{ tabList: { style: 'background-color: transparent;' } }">
                <Tab v-for="r in rooms" :value="r.room_id">{{ r.room_name }}</Tab>
            </TabList>
        </Tabs>
        <h4 v-if="devices.length === 0">No Devices Found in This Room</h4>
        <div v-else id="devices_cont">
            <div v-for="device in devices" class="device_card" v-ripple>
                <div class="card_header">
                    <component :is="device_type_icon_map[device.device_type]" class="card_icon" fill_color="var(--p-primary-color)" style="width: 24px; height: 24px;" />
                    <div style="width: 12px;"></div>
                    <WifiIcon :fill_color="compute_connection_icon_color(device)" style="width: 18px; height: 18px;" />
                    <div style="flex-grow: 1;"></div>
                    <div class="device_quick_controls">
                        <Button outlined style="margin-right: 8px;">
                            <SettingsIcon fill_color="var(--p-primary-color)" style="width: 16px; height: 16px;" />
                        </Button>
                        <Button outlined :style="`background-color: ${ON_STATES.includes(sensor_state_main_map[device.device_uuid.slice(-4)] ?? '--') ? 'var(--p-primary-color)' : '#FFFFFF'};`" @click="device_power_click(device.device_uuid)">
                            <PowerIcon :fill_color="ON_STATES.includes(sensor_state_main_map[device.device_uuid.slice(-4)] ?? '--') ? '#FFFFFF' : 'var(--p-primary-color)'" style="width: 16px; height: 16px;" />
                        </Button>
                    </div>
                </div>
                <h4 class="device_name">{{ device.device_name }}</h4>
                <h4 class="device_state">{{ sensor_state_main_map[device.device_uuid.slice(-4)] ?? '--' }}</h4>
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped>
.device_quick_controls button {
    width: 36px;
    height: 36px;
    padding: 0px;
}

.device_state {
    margin: 0px;
    margin-top: 8px;
    font-size: 14px;
    color: var(--p-zinc-500);
}

.device_name {
    margin: 0px;
    margin-top: 16px;
    font-size: 14px;
}

.device_card .card_header {
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
}

.device_card {
    width: 180px;
    height: 120px;
    margin: auto;
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid var(--p-zinc-300);
    box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
    padding: 8px;
}

#devices_cont {
    display: grid;
    grid-template-columns: 186px 186px;
    grid-auto-rows: 136px;
    width: 100%;
    max-height: calc(100vh - 280px);
    overflow-y: scroll;
    background-color: transparent;
    padding: 8px 0px;
}

.ths_icon_cont {
    width: 56px;
    height: 56px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    background-color: var(--p-zinc-700);
}

.ths_text_cont {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    margin-left: 8px;
}

.th_section {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
}

#temp_humd_section {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    border-radius: 4px;
    height: fit-content;
    background-color: var(--p-primary-color);
    padding: 12px 24px;
}

#home_screen_cont {
    width: 96vw;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
}
</style>