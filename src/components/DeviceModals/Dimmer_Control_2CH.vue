<script setup lang="ts">

import { onMounted, ref, computed, watch } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Slider from 'primevue/slider';
import PowerIcon from '../icons/PowerIcon.vue';
import { mqtt_publish } from '@src/lib/mqtt';

import { request_data_resource } from '@src/lib/mqtt';
import { subscribe } from '@src/lib/mediator';
import { dialog_pt } from '@src/lib/theme';
import { useToast } from 'primevue/usetoast';

const toast_service = useToast();
const dialog_visiable = ref(false);
const device_name = ref('Device Name');

const dimmer_0_slider_value = ref(0)
const dimmer_1_slider_value = ref(0)
const dimmer_0_active_switch = computed(() => {
    return Math.ceil(dimmer_0_slider_value.value / (100 / 3))
})
const dimmer_1_active_switch = computed(() => {
    return Math.ceil(dimmer_1_slider_value.value / (100 / 3))
})


let device_mqtt_id = '';

watch(dimmer_0_slider_value, () => {
    const dimmer_0_mqtt_topic = `rpc/${device_mqtt_id}/command_dimmer_0`;
    const success = mqtt_publish(dimmer_0_mqtt_topic, String(dimmer_0_slider_value.value));
    if (!success) {
        toast_service.add({ severity: 'error', summary: 'Device Error', detail: 'Device Unreachable', life: 3000 });
        return;
    }

})
watch(dimmer_1_slider_value, () => {
    const dimmer_1_mqtt_topic = `rpc/${device_mqtt_id}/command_dimmer_1`;
    const success = mqtt_publish(dimmer_1_mqtt_topic, String(dimmer_1_slider_value.value));
    if (!success) {
        toast_service.add({ severity: 'error', summary: 'Device Error', detail: 'Device Unreachable', life: 3000 });
        return;
    }

})
onMounted(() => {
    subscribe('show_device_dimmer_2ch_control_dialog', 'show_device_dimmer_2ch_control_dialog', args => {
        const _device_name: string = args.device_name;
        const _device_mqtt_id: string = args.device_mqtt_id;
        device_name.value = _device_name;
        device_mqtt_id = _device_mqtt_id;
        dialog_visiable.value = true;
        request_data_resource('dimmer_2ch_state', { device_mqtt_id })
    });
    subscribe('data_response_dimmer_2ch_state', 'data_response_dimmer_state', args => {
       
         if (!args)
            return;
        const dimmer = JSON.parse(args.payload);
        
        dimmer_0_slider_value.value = Number(dimmer.dimmer_0)
        dimmer_1_slider_value.value = Number(dimmer.dimmer_1)
    });

});

</script>

<template>
    <Dialog v-model:visible="dialog_visiable" modal style="width: 96vw; font-family: Avenir, Helvetica, Arial, sans-serif;" :pt="dialog_pt" dismissable-mask>
        <template #header>
            <span style="font-size: 16px; font-weight: bold; margin-top: 8px;">{{ device_name }}</span>
        </template>
        <div class="dimmers-container">
            <div class="dimmer_module_container">
            <p class="dimmer_state_view">Light Intensity: {{ dimmer_0_slider_value }}</p>
            <Slider class="dimmer_slider" v-model="dimmer_0_slider_value" />
            <div class="dimmer_btns_cont">

                <Button label=" " outlined :class="{ dimmer_btn_active: dimmer_0_active_switch == 0 }" @click="dimmer_0_slider_value = 0">
                    <PowerIcon :fill_color="(dimmer_0_active_switch == 0) ? '#FFFFFF' : 'var(--p-primary-color)'" style="width: 12px; height: 12px;" />
                </Button>
                <Button label="1" outlined :class="{ dimmer_btn_active: dimmer_0_active_switch == 1 }" @click="dimmer_0_slider_value = 33" />
                <Button label="2" outlined :class="{ dimmer_btn_active: dimmer_0_active_switch == 2 }" @click="dimmer_0_slider_value = 66" />
                <Button label="3" outlined :class="{ dimmer_btn_active: dimmer_0_active_switch == 3 }" @click="dimmer_0_slider_value = 100" />
            </div>
        </div>

        <div class="dimmer_module_container">
            <p class="dimmer_state_view">Light Intensity: {{ dimmer_1_slider_value }}</p>
            <Slider class="dimmer_slider" v-model="dimmer_1_slider_value" />
            <div class="dimmer_btns_cont">

                <Button label=" " outlined :class="{ dimmer_btn_active: dimmer_1_active_switch == 0 }" @click="dimmer_1_slider_value = 0">
                    <PowerIcon :fill_color="(dimmer_1_active_switch == 0) ? '#FFFFFF' : 'var(--p-primary-color)'" style="width: 12px; height: 12px;" />
                </Button>
                <Button label="1" outlined :class="{ dimmer_btn_active: dimmer_1_active_switch == 1 }" @click="dimmer_1_slider_value = 33" />
                <Button label="2" outlined :class="{ dimmer_btn_active: dimmer_1_active_switch == 2 }" @click="dimmer_1_slider_value = 66" />
                <Button label="3" outlined :class="{ dimmer_btn_active: dimmer_1_active_switch == 3 }" @click="dimmer_1_slider_value = 100" />
            </div>
        </div>

        </div>
        
    </Dialog>
</template>

<style lang="css">
.dimmer_slider {
    margin-bottom: 24px;
}

.dimmer_state_view {
    text-align: center;
    margin-top: 0;
}

.dimmer_btn_active {
    background-color: var(--p-primary-color) !important;
    color: #FFFFFF !important;
    border-width: 0px !important;
}

.dimmer_btns_cont button {
    width: 50px;
    height: 50px;
    border-width: 2px;
}

.dimmer_btns_cont {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
}
.dimmers-container{
display: flex;
flex-direction: column;
gap: 32px;
}
</style>