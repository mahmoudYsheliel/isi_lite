<script setup lang="ts">

import { onMounted,ref } from 'vue';
import { useToast } from "primevue/usetoast";
import Toast from 'primevue/toast';
import {  attach_data_service, attach_sensor_service,attach_telem_notification } from '@src/lib/mqtt';
import TopBar from '@src/components/TopBar.vue';
import BottomBar from '@src/components/BottomBar.vue';
import HomeScreen from '@src/components/screens/HomeScreen.vue';
import { post_event, subscribe } from '@src/lib/mediator';
import ScenesScreen from './components/screens/ScenesScreen.vue';
import ISINetworkConfigScreen from '@src/components/screens/ISINetworkConfigScreen.vue';
const toast_service = useToast();
const active_view = ref<0|1|2|3>(0)

const all_views = {
  0:HomeScreen,
  1:ISINetworkConfigScreen,
  2:ScenesScreen,
  3:ISINetworkConfigScreen,
}


onMounted(() => {
  subscribe('mqtt_connection_ok', 'mqtt_connection_ok_main', () => {
    attach_data_service();
    attach_sensor_service();
    attach_telem_notification();
    toast_service.add({ severity: 'success', summary: 'Connected', detail: 'Connected to ISI Device Network', life: 3000 });
  });
  subscribe('mqtt_connection_err', 'mqtt_connection_err_main', err => {
    console.log('MQTT-ERROR:');
    console.log(err);
    post_event('bottom_bar_page_move',{index:3})
    toast_service.add({ severity: 'error', summary: 'Diconnected', detail: 'Can not Connect to ISI Device Network', life: 3000 });
  });
  subscribe('smart_scene_executed', 'smart_scene_executed', (args) => {
        toast_service.add({ severity: 'success', summary: 'Executed', detail: `${args.title} Executed Succesfully`, life: 3000 });
    })
    subscribe('smart_scene_updated', 'smart_scene_updated', () => {
        toast_service.add({ severity: 'success', summary: 'Updated', detail: `Smart Scenes Updated Succesfully`, life: 3000 });
    })
  subscribe('select_screen', 'select_screen_main', args => {
    active_view.value = args.indx
  });
  
});

</script>

<template>
  <div id="main_cont">
    <Toast position="top-center" style="font-family: Avenir, Helvetica, Arial, sans-serif; width: 96vw;" />
    <TopBar />
    <div id="app_screen_cont">
      <div style="height: 90px;"></div>
      <component :is="all_views[active_view]" />
      <div style="height: 90px;"></div>
    </div>
    <BottomBar />
  </div>
</template>

<style>
#app_screen_cont {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}

#main_cont {
  width: 100%;
  height: 100%;
}

body,
html {
  width: 100%;
  height: 100%;
  margin: 0;
}

#app {
  background-color: var(--p-zinc-100);
  font-family: Avenir, Helvetica, Arial, sans-serif;
  /* font-family: "Cairo", sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c2c2c;
  width: 100%;
  height: 100%;
}
*{
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>
