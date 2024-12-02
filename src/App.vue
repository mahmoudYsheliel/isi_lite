<script setup lang="ts">

import { onBeforeMount, onMounted } from 'vue';
import { useToast } from "primevue/usetoast";
import Toast from 'primevue/toast';

import { mqtt_connect, attach_data_service, attach_sensor_service } from '@src/lib/mqtt';
import TopBar from '@src/components/TopBar.vue';
import BottomBar from '@src/components/BottomBar.vue';
import HomeScreen from '@src/components/screens/HomeScreen.vue';
import { subscribe } from '@src/lib/mediator';
import ISINetworkConfigDialog from '@src/components/ISINetworkConfigDialog.vue';

const toast_service = useToast();

onBeforeMount(() => {
  mqtt_connect();
});

onMounted(() => {
  subscribe('mqtt_connection_ok', 'mqtt_connection_ok_main', () => {
    attach_data_service();
    attach_sensor_service();
    toast_service.add({ severity: 'success', summary: 'Connected', detail: 'Connected to ISI Device Network', life: 3000 });
  });
  subscribe('mqtt_connection_err', 'mqtt_connection_err_main', err => {
    console.log('MQTT-ERROR:');
    console.log(err);
    toast_service.add({ severity: 'error', summary: 'Diconnected', detail: 'Can not Connect to ISI Device Network', life: 3000 });
  });
});

</script>

<template>
  <div id="main_cont">
    <ISINetworkConfigDialog />
    <Toast position="top-center" style="font-family: Avenir, Helvetica, Arial, sans-serif; width: 96vw;" />
    <TopBar />
    <div id="app_screen_cont">
      <div style="height: 90px;"></div>
      <HomeScreen />
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
</style>
