<script setup lang="ts">

import { shallowRef, onMounted } from 'vue';

import { post_event,subscribe } from '@src/lib/mediator';
import { delete_username_pass ,mqtt_disconnect, is_connected} from '@src/lib/mqtt';
import HouseChimneyIcon from '@src/components/icons/HouseChimneyIcon.vue';
import ChartSimpleIcon from '@src/components/icons/ChartSimpleIcon.vue';
import MoonIcon from '@src/components/icons/MoonIcon.vue';
import SettingsIcon from '@src/components/icons/SettingsIcon.vue';
import SignOutAltIcon from '@src/components/icons/SignOutAltIcon.vue';
import { useToast } from "primevue/usetoast";

const toast_service = useToast()

const bottom_bar_icons: any[] = [
    HouseChimneyIcon,   // 0
    ChartSimpleIcon,    // 1
    MoonIcon,           // 2
    SettingsIcon,       // 3
    SignOutAltIcon,     // 4
];

subscribe('bottom_bar_page_move','bottom_bar_page_move',(args)=>{
    bottom_bar_button_click(args.index)
})

const icons_active_state = shallowRef(new Array(bottom_bar_icons.length).fill(false));

function __bbsmap(_active: boolean) {
    if (_active)
        return '--p-ripple-background: #FFFFFF;';
    else
        return '--p-ripple-background: #BDBDBD; background-color: white; border: 1px solid black;';
}

function __bbicmap(_active: boolean) {
    if (_active)
        return '#FFFFFF';
    else
        return 'var(--p-primary-color)';
}

function bottom_bar_button_click(indx: number) {
    if (!is_connected() && indx!=3){
        indx = 3
        toast_service.add({ severity: 'warn', summary: 'Not Connected', detail: 'Connect to ISI Device Network First', life: 3000 });
    }
    if (indx==4){
        console.log('Logout')
        delete_username_pass()
        mqtt_disconnect()
        indx = 3
    }
    const _active_state = new Array(bottom_bar_icons.length).fill(false);
    _active_state[indx] = true;
    icons_active_state.value = _active_state;
    post_event('select_screen', {indx,mode:'Normal'});
}

onMounted(() => {
    bottom_bar_button_click(0);
});

</script>

<template>
    <div id="bottom_bar_cont">
        <div v-for="(bb_icon, idx) in bottom_bar_icons" v-ripple class="bottom_bar_button" :style="__bbsmap(icons_active_state[idx])" @click="bottom_bar_button_click(idx)">
            <component :is="bb_icon" :fill_color="__bbicmap(icons_active_state[idx])" />
        </div>
    </div>
</template>

<style lang="css" scoped>
.bottom_bar_button {
    position: relative;
    overflow: hidden;
    width: 40px;
    height: 40px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    background-color: var(--p-primary-color);
    padding: 8px;
    border-radius: 4px;
}

#bottom_bar_cont {
    position: absolute;
    bottom: 8px;
    left: 2vw;
    width: 96vw;
    box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    border-radius: 4px;
    padding: 8px 0px;
    background-color: #FFFFFF;
}
</style>