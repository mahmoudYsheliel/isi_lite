<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import 'primeicons/primeicons.css'
import Button from 'primevue/button';
import { post_event, subscribe } from '@src/lib/mediator';
import CreateEditSceneModal from '../SceneModals/CreateEditSceneModal.vue';
import HomeScreen from './HomeScreen.vue';
import { Scene } from '@src/lib/models';
import { mqtt_publish, request_data_resource } from '@src/lib/mqtt';
import { fuzzySearch } from '@src/lib/helpers';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';

import MoonIcon from '../icons/MoonIcon.vue';


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

function map_label_icon(label: string) {
    for (const group of icon_map) {
        const item = group.items.find((item: any) => item.label === label);
        if (item) {
            return item.scene_icon;
        }
    }
}



const scenes = ref<Scene[]>([])
const filtered_scenes = ref<Scene[]>([])
const mode = ref('Normal')
const search_value = ref('')
onMounted(() => {
    subscribe('screen_record_start', 'screen_record_start', () => {
        mode.value = 'Recording'
    })
    subscribe('data_response_smart_scenes', 'data_response_smart_scene', (args) => {
        scenes.value = JSON.parse(args.payload)
        filtered_scenes.value = JSON.parse(args.payload)
        search_value.value = ''
    })
    subscribe('request_smart_scenes', 'request_smart_scenes', () => {
        request_data_resource('smart_scenes')
    })
    request_data_resource('smart_scenes')
})


function add_scene() {
    post_event('show_smart_scene_dialog', { title: 'Create Scene' })
}
function stop_recording() {
    post_event('stop_recording', {})
    mode.value = 'Normal'
    post_event('show_smart_scene_dialog', { title: 'Create Scene', scene: {} })

}
function show_smart_scene(i: number) {
    post_event('show_smart_scene_dialog', { title: 'View Scene', scene: scenes.value[i] })
}
function delete_scene(i: number) {
    mqtt_publish(`smart_scene/delete/${i}`, 'X')
}

function execute_smart_scene(i: number) {
    const executed_scene = filtered_scenes.value[i]
    const order = scenes.value.indexOf( executed_scene)

    mqtt_publish(`smart_scene/execute/${order}`, 'X')

}
watch(search_value, () => {
    const titles = scenes.value.map(scene => scene.title)
    if (search_value.value === '') {
        filtered_scenes.value = scenes.value
        return
    }
    const search_result = fuzzySearch(search_value.value, titles)
    filtered_scenes.value = []
    search_result.forEach((title: string) => {
        let scene = scenes.value.find(scene => scene.title == title) ?? scenes.value[0]
        filtered_scenes.value.push(scene)
    })
})
</script>

<template>
    <CreateEditSceneModal />
    <div class="scene_normal_mode" v-if="mode == 'Normal'">
        <div class="smart_scene_header">
            <MoonIcon fill_color="white" style="height: 32px;" />
            <p style="font-size: 20px;">Smart Scenes</p>
        </div>

        <div id="smart_scene_search">
            <IconField style="height: 100%;">
                <InputIcon class="pi pi-search" />
                <InputText style="height: 100%;" v-model="search_value" placeholder="Scenes Search" />
            </IconField>
            <i class="pi pi-search search_icon" />
        </div>
        <div id="devices_cont">
            <div class="device_card" v-ripple v-for="scene, i in filtered_scenes" @click="() => { execute_smart_scene(i) }">
                <div class="card_header">
                    <component style="width: 40px; height: 40px;padding: 8px;border-radius: 100%;" fill_color="white" :is="map_label_icon(scene.icon_label)" class="card_icon" :style="{ backgroundColor: scene.color }" />
                    <div style="width: 12px;"></div>
                    <div style="flex-grow: 1;"></div>
                    <div class="device_quick_controls">
                        <Button outlined style="width: 32px;height: 32px;">
                            <i style="color: #99CC33;" class="pi pi-pencil" @click.stop="() => { show_smart_scene(i) }" />
                        </Button>
                        <Button outlined style="width: 32px;height: 32px;">

                            <i style="color:red" class="pi pi-trash" @click.stop="() => { delete_scene(i) }" />
                        </Button>
                    </div>
                </div>
                <h4 class="device_name">{{ scene.title }}</h4>
            </div>
        </div>

        <div class="add_button_con">
            <Button class="add_button" icon="pi pi-plus" @click.stop="add_scene" />
        </div>

    </div>






    <div class="scene_recording_mode" v-if="mode == 'Recording'">
        <HomeScreen />
        <div class="record_btn_container">
            <Button label="Stop Recording" icon="pi pi-pause-circle" @click.stop="stop_recording" />
        </div>
    </div>
</template>

<style lang="css" scoped>
.device_quick_controls {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.device_state {
    margin: 0px;
    margin-top: 8px;
    font-size: 14px;
    color: var(--p-zinc-500);
}

.device_name {
    margin: 0px;
    font-size: 14px;
}

.device_card .card_header {
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: start;
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







.scene_normal_mode {
    height: 100%;
}

#smart_scene_search {
    height: 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    gap: 16px;
}

.search_icon {
    height: 100%;
    width: 100%;
    background-color: black;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bolder;
    border-radius: 8px;
    font-size: 20px;
}

.icon_text {
    display: flex;
    flex-direction: column;
    justify-content: end;
    align-items: center;
    gap: 16px;
}

.scene {
    display: grid;
    grid-template-rows: 1fr 4fr;
    padding: 16px 8px;
    margin: 8px;
    box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
    border-radius: 8px;
    background-color: white;
    width: 180px;
    aspect-ratio: 1/1;
}

.scene>* {
    padding: 0;
    margin: 0;
}

.actions {
    display: flex;
    justify-content: end;
    gap: 16px;
}

.record_btn_container {
    position: fixed;
    bottom: 80px;
    right: 24px;
}

.scenes_container {
    max-height: 60vh;
    overflow-y: scroll;
    display: grid;
    grid-template-columns: 186px 186px;
    width: 100%;
    max-height: calc(100vh - 280px);
    overflow-y: scroll;
    background-color: transparent;
    padding: 8px 0px;
}

.selected {
    border: black 2px solid;
}


.field_actions {
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.smart_scene_header {
    background-color: black;
    height: 72px;
    display: flex;
    align-items: center;
    color: white;
    font-size: 16px;
    font-weight: bolder;
    width: 96vw;
    border-radius: 4px;
    margin: 0 0 8px 0;
    margin-top: 2px;
    gap: 16px;
    padding-inline: 16px;
}

.field_actions>button {
    font-size: 14px;
    width: 96px;
}

.field_container {
    display: flex;
    flex-direction: column;
    gap: 4px;

    overflow: scroll;
}

.fieldset_header {
    font-size: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
}

.add_button_con {
    width: fit-content;
    height: fit-content;
    position: absolute;
    bottom: 80px;
    right: 16px;

}

.add_button {
    border-radius: 100%;
    width: 48px;
    aspect-ratio: 1/1;
}

.element {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.element>p {
    width: 90px;
    font-size: 14px;
    padding: 0;
    margin: 0;
}

.input {
    height: fit-content;
    font-size: 14px;
}
</style>