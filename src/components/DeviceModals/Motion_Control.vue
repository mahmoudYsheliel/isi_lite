<script setup lang="ts">

import { onMounted, ref } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

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
        const _device_state: string = args.device_state;
        device_name.value = _device_name;
        device_mqtt_id = _device_mqtt_id;
        dialog_visiable.value = true;
        motion_mode.value = _device_state
    });
    subscribe('data_response_motion_sensor_mode', 'data_response_motion_sensor_mode', args => {
       if (!args)
          return;
      const _motion_mode = JSON.parse(args.payload);
     
      motion_mode.value = _motion_mode
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
    const motion_0_mqtt_topic = `conf/${device_mqtt_id}/motion_sensor_mode`;
    const success = mqtt_publish(motion_0_mqtt_topic, mode,device_name.value);
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
        <p style="font-size: 14px; font-weight: bold; margin-top: 0px;">Select Mode:</p>
        <div id="motion_sensor_mode_cont">
            <Button label="Normal" outlined :class="{ motion_mode_active: motion_mode == 'NORMAL' }" @click="() => { send_mode('NORMAL') }" />
            <Button label="Security" outlined :class="{ motion_mode_active: motion_mode == 'SECURITY' }" @click="() => { send_mode('SECURITY') }" />
        </div>
        <div class="scene_btn_container">
            <Button label="Close" icon="pi pi-times" @click="dialog_visiable = false" />
        </div>
    </Dialog>
</template>

<style lang="css">
.motion_mode_active {
    background-color: var(--p-primary-color) !important;
    color: #FFFFFF !important;
    border-width: 0px !important;
}

#motion_sensor_mode_cont button {
    width: 120px;
    height: 40px;
    border-width: 2px;
}

#motion_sensor_mode_cont {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 8px;
}
</style>