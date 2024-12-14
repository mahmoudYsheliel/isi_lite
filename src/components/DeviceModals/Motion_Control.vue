<script setup lang="ts">

import { onMounted, ref } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

import { request_data_resource } from '@src/lib/mqtt';
import { subscribe } from '@src/lib/mediator';
import { dialog_pt } from '@src/lib/theme';

const dialog_visiable = ref(false);
const device_name = ref('Device Name');
const motion_mode = ref('NORMAL');
import { mqtt_publish } from '@src/lib/mqtt';
import { useToast } from 'primevue/usetoast';

const toast_service = useToast();
let device_mqtt_id = '';


onMounted(() => {
    subscribe('show_device_motion_control_dialog', 'show_device_motion_control_dialog', args => {
        const _device_name: string = args.device_name;
        const _device_mqtt_id: string = args.device_mqtt_id;
        device_name.value = _device_name;
        device_mqtt_id = _device_mqtt_id;
        dialog_visiable.value = true;
        request_data_resource('motion_sensor_mode', { device_mqtt_id });
    });
    subscribe('data_response_motion_sensor_mode', 'data_response_motion_sensor_mode', args => {
        if (!args)
            return;
        const motion_mode_set = JSON.parse(args.payload);
        if (!['NORMAL', 'SECURITY'].includes(motion_mode_set.motion_sensor_mode))
            return;
        motion_mode.value = motion_mode_set.motion_sensor_mode
    });

    subscribe('sensor_state', 'sensor_state_motion_sensor', args => {
        const device_mqtt_id_recieved: string = args.device_mqtt_id;
        if(device_mqtt_id_recieved===device_mqtt_id){
            if (!['NORMAL', 'SECURITY'].includes(args.payload))
            return;
        motion_mode.value = args.payload
        }
    });
});

function send_mode(mode: string) {
    const motion_0_mqtt_topic = `rpc/${device_mqtt_id}/command_motion_0`;
    const success = mqtt_publish(motion_0_mqtt_topic, mode);
    if (!success) {
        toast_service.add({ severity: 'error', summary: 'Device Error', detail: 'Device Unreachable', life: 3000 });
        return;
    }
   
}

</script>

<template>
    <Dialog v-model:visible="dialog_visiable" modal style="width: 96vw; font-family: Avenir, Helvetica, Arial, sans-serif;" :pt="dialog_pt" dismissable-mask>
        <template #header>
            <span style="font-size: 16px; font-weight: bold; margin-top: 8px;">{{ device_name }}</span>
        </template>
        <div id="switch_4ch_btns_cont">
            <Button label="Normal" outlined :class="{ motion_mode_active: motion_mode == 'NORMAL' }" @click="() => { send_mode('NORMAL') }" />
            <Button label="Security" outlined :class="{ motion_mode_active: motion_mode == 'SECURITY' }" @click="() => { send_mode('SECURITY') }" />
        </div>
    </Dialog>
</template>

<style lang="css">
.motion_mode_active {
    background-color: var(--p-primary-color) !important;
    color: #FFFFFF !important;
    border-width: 0px !important;
}

#switch_4ch_btns_cont button {
    width: 120px;
    height: 40px;
    border-width: 2px;
}

#switch_4ch_btns_cont {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 8px;
}
</style>