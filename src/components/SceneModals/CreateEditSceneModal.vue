<script setup lang="ts">

import { onMounted, ref, shallowRef } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';

import { post_event, subscribe } from '@src/lib/mediator';
import { dialog_pt } from '@src/lib/theme';
import { RecordedCommand } from '@src/lib/models';
import { mqtt_publish, request_data_resource } from '@src/lib/mqtt';

import Baby from '../scenes_icons/Baby.vue';
import EnergySave from '../scenes_icons/EnergySave.vue';
import Exercise from '../scenes_icons/Exercise.vue';
import Focus from '../scenes_icons/Focus.vue';
import Garden from '../scenes_icons/Garden.vue';
import Holiday from '../scenes_icons/Holiday.vue';
import Kite from '../scenes_icons/Kite.vue';
import Moon from '../scenes_icons/Moon.vue';
import Movie from '../scenes_icons/Movie.vue';
import Party from '../scenes_icons/Party.vue';
import Readning from '../scenes_icons/Readning.vue';
import Sunrise from '../scenes_icons/Sunrise.vue';
import RomanticEvening from '../scenes_icons/RomanticEvening.vue';
import Welcom from '../scenes_icons/Welcom.vue';
import Winter from '../scenes_icons/Winter.vue';
import WorkFromHome from '../scenes_icons/WorkFromHome.vue';
import Menu from 'primevue/menu';

const icon_map = [
    {
        label: 'Nature',
        items: [
            { label: 'Moon', scene_icon: Moon },
            { label: 'Sunrise', scene_icon: Sunrise },
            { label: 'Winter', scene_icon: Winter },
            { label: 'Garden', scene_icon: Garden },
            { label: 'Kite', scene_icon: Kite }
        ]
    },
    {
        label: 'Activities',
        items: [
            { label: 'Holiday', scene_icon: Holiday },
            { label: 'Party', scene_icon: Party },
            { label: 'Exercise', scene_icon: Exercise },
            { label: 'Readning', scene_icon: Readning },
            { label: 'WorkFromHome', scene_icon: WorkFromHome }
        ]
    },
    {
        label: 'Focus & Entertainment',
        items: [
            { label: 'Focus', scene_icon: Focus },
            { label: 'Movie', scene_icon: Movie },
            { label: 'RomanticEvening', scene_icon: RomanticEvening }
        ]
    },
    {
        label: 'Special Moments',
        items: [
            { label: 'Welcom', scene_icon: Welcom },
            { label: 'Baby', scene_icon: Baby },
            { label: 'EnergySave', scene_icon: EnergySave }
        ]
    }
];
const colors =['#e18fb5', '#ea9d6f','#efbe5f','#82c1b6','#88bf86','#7fa6e9','#c098f8','#0288d1','#9e9e9e','#607d8b','#01abff']


const selected_scene_icon = shallowRef(icon_map[0].items[0])
const selected_color = ref('#e18fb5')


const dialog_visiable = ref(false);
const dialog_title = ref('')
const scene_name = ref('')
const actions_list = ref<RecordedCommand[]>([])

onMounted(() => {
    subscribe('show_smart_scene_dialog', 'show_smart_scene_dialog', (args) => {
        dialog_title.value = args?.title
        if (!args.scene) {
            scene_name.value = ''
            actions_list.value = []
            selected_scene_icon.value = icon_map[0].items[0]
        }
        
        else if (Object.keys(args.scene).includes('actions') && Object.keys(args.scene).includes('title') && Object.keys(args.scene).includes('icon_label')) {
            actions_list.value = args.scene.actions
            scene_name.value = args.scene.title
            let label = args.scene.icon_label
            let icon = icon_map[0].items[0].scene_icon
            for (const group of icon_map) {
                const item = group.items.find((item: any) => item.label === label);
                if (item) {
                    icon = item.scene_icon;
                }
            }
            selected_scene_icon.value = { label: label, scene_icon: icon }
        }
        dialog_visiable.value = true;
    });
    subscribe('actions_recorded', 'actions_recorded_samrt_scene', (args) => {
        actions_list.value = args.actions
    })
});
function start_recording() {
    post_event('screen_record_start', { actions: actions_list.value })
    dialog_visiable.value = false
}

function create_scene() {
    let object_string = JSON.stringify({ actions: actions_list.value, title: scene_name.value, icon_label: selected_scene_icon.value.label,color:selected_color.value })
    mqtt_publish('smart_scenes/write_file', object_string)
    scene_name.value = ''
    actions_list.value = []
    dialog_visiable.value = false;
    request_data_resource('smart_scenes')
}
const menu = ref();
const toggle_function = (event: MouseEvent) => {
    menu.value.toggle(event);
};




const menu_menu_pt = {
    root: { style: 'padding: 0px;' },
    menu: { style: 'padding: 0px;' },
    submenuHeader: { style: 'padding: 0px;margin:0' },
    submenulabel: { style: 'padding: 0px;margin:0' },
    list: { style: 'padding: 0px;margin:0' },
};

function update_slected_icon(item: any) {
    selected_scene_icon.value = { label: item.label, scene_icon: item.scene_icon }
}
</script>

<template>
    <Dialog v-model:visible="dialog_visiable" modal style="width: 96vw; font-family: Avenir, Helvetica, Arial, sans-serif;" :pt="dialog_pt" dismissable-mask>
        <template #header>
            <h4 style="margin: 0;margin-top: 8px;">{{ dialog_title }}</h4>
        </template>
        <div class="scene_dialog_container">
            <InputText v-model="scene_name" placeholder="Scene Name" class="inp" />
            <div class="scelect_icon">
                <div class="selecct_icon_button">
                    <div class="selecct_icon_text"> <span>Selected Icon:</span>
                        <component :style="{backgroundColor:selected_color}" :is="selected_scene_icon.scene_icon" style=" height: 32px;width: 32px; border-radius: 100%; padding: 4px;" fill_color="white" />
                    </div>
                    <Button type="button" icon="pi pi-ellipsis-v" @click="toggle_function" aria-haspopup="true" aria-controls="overlay_menu" />
                </div>
                <Menu :pt="menu_menu_pt" :model="icon_map" id="overlay_menu" class="w-full md:w-60" ref="menu" popup>

                    <template #submenuheader="{ item }">
                        <p class="text-primary">{{ item.label }}</p>
                    </template>
                    <template #item="{ item, props }">
                        <a v-ripple class="flex items-center" v-bind="props.action" @click="() => { update_slected_icon(item) }">
                            <component fill_color="black" style="width: 14px; height: 14px;"  v-if="item.scene_icon" :is="item.scene_icon" />
                            <span>{{ item.label }}</span>
                        </a>
                    </template>

                </Menu>
                <div class="colors_wrapper">
                    <div class="color" v-for="color in colors" :style="{backgroundColor:color}" @click="selected_color=color">

                    </div>
                </div>
            </div>

            <div v-if="actions_list?.length > 0" class="action_list_con">
                <h4 style="margin-bottom: 0;">Scene Actions List</h4>
                <div class="action_list">
                    <div v-for="action, i in actions_list" class="scene_action">
                        <div class="message_field">
                            <div class="command_field">
                                <p>Device</p>
                                <p>{{ action.device_name }}</p>
                            </div>
                            <div class="command_field">
                                <p>Command</p>
                                <p>{{ action.payload }}</p>
                            </div>
                        </div>

                        <i class="pi pi-times-circle" @click="actions_list.splice(i, 1)" />
                    </div>

                </div>
            </div>
            <Button label="Record Actions" icon="pi pi-stop-circle" @click="start_recording" style="margin-top: 24px;" />
            <div class="scene_btn_container">
                <Button label="Close" icon="pi pi-times" @click="dialog_visiable = false" />
                <Button label="Create" icon="pi pi-check" :disabled="!scene_name || (!actions_list?.length || actions_list?.length == 0)" @click="create_scene" />
            </div>
        </div>

    </Dialog>
</template>

<style lang="css">
.colors_wrapper{
    display: flex;
    width: 100%;
    justify-content: space-between;
}
.color{
    width:24px ;
    height: 24px;
    border-radius: 100%;

}
.text-primary {
    color: white;
    background-color: black;
    width: 100%;
    margin: 0;
    padding: 8px 12px;
    border-radius: 4px;
}

#overlay_menu {
    padding: 0;
    margin: 0;
    height: 30vh;
    overflow-y: scroll;
}

.selecct_icon_button {
    margin-block: 8px;
}

.selecct_icon_button,
.selecct_icon_text {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
}

.scene_action {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 8px;
    padding: 4px 8px;
    box-shadow: rgba(0, 0, 0, 0.25) 0px 0px 10px 0px;
    margin-block: 16px;
}

.command_field {
    display: flex;

}

.command_field>p {
    margin-block: 6px;
}

.command_field>:first-child {
    width: 100px;
    font-weight: bold;
}

.scene_btn_container {
    display: flex;
    justify-content: end;
    gap: 8px;
    margin-top: 16px;
}

.motion_mode_active {
    background-color: var(--p-primary-color) !important;
    color: #FFFFFF !important;
    border-width: 0px !important;
}

.scene_dialog_container {
    max-height: 40vh;
    overflow-y: scroll;
    padding: 4px;
    width: 100%;
}
.inp{
    width: 100%;
}
</style>