<script setup lang="ts">

import { onMounted, ref } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

import { request_data_resource } from '@src/lib/mqtt';
import { subscribe } from '@src/lib/mediator';
import { dialog_pt } from '@src/lib/theme';

const dialog_visiable = ref(false);
const device_name = ref('Device Name');
const switch_4ch_l1_state = ref(false);
const switch_4ch_l2_state = ref(false);
const switch_4ch_l3_state = ref(false);
const switch_4ch_l4_state = ref(false);

let device_mqtt_id = '';

function __sm(s: string): boolean {
    const _sm: Record<string, boolean> = {
        'OFF': false,
        'ON': true,
    };
    return _sm[s] ?? false;
}

onMounted(() => {
    subscribe('show_device_switch_4ch_control_dialog', 'show_device_switch_4ch_control_dialog', args => {
        const _device_name: string = args.device_name;
        const _device_mqtt_id: string = args.device_mqtt_id;
        device_name.value = _device_name;
        device_mqtt_id = _device_mqtt_id;
        dialog_visiable.value = true;
        request_data_resource('switch_4ch_state', { device_mqtt_id });
    });
    subscribe('data_response_switch_4ch_state', 'data_response_switch_4ch_state', args => {
        if (!args)
            return;

        const switch_4ch = JSON.parse(args.payload);
        switch_4ch_l1_state.value = __sm(switch_4ch.power_0);
        switch_4ch_l2_state.value = __sm(switch_4ch.power_1);
        switch_4ch_l3_state.value = __sm(switch_4ch.power_2);
        switch_4ch_l4_state.value = __sm(switch_4ch.power_3);
    });
});

</script>

<template>
    <Dialog v-model:visible="dialog_visiable" modal style="width: 96vw; font-family: Avenir, Helvetica, Arial, sans-serif;" :pt="dialog_pt" dismissable-mask>
        <template #header>
            <span style="font-size: 16px; font-weight: bold; margin-top: 8px;">{{ device_name }}</span>
        </template>
        <div id="switch_4ch_btns_cont">
            <Button label="L1" outlined :class="{ switch_4ch_btn_active: switch_4ch_l1_state }" />
            <Button label="L2" outlined :class="{ switch_4ch_btn_active: switch_4ch_l2_state }" />
            <Button label="L3" outlined :class="{ switch_4ch_btn_active: switch_4ch_l3_state }" />
            <Button label="L4" outlined :class="{ switch_4ch_btn_active: switch_4ch_l4_state }" />
        </div>
    </Dialog>
</template>

<style lang="css">
.switch_4ch_btn_active {
    background-color: var(--p-primary-color) !important;
    color: #FFFFFF !important;
    border-width: 0px !important;
}

#switch_4ch_btns_cont button {
    width: 50px;
    height: 50px;
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