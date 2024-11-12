<script setup lang="ts">

import { onMounted, ref } from 'vue';
import Dialog from 'primevue/dialog';
import Fieldset from 'primevue/fieldset';

import { subscribe } from '@src/lib/mediator';

const dialog_pt = {
    header: { style: 'padding: 8px 16px; font-size: 14px;' },
    content: { style: 'padding: 8px 16px;' },
};

const dialog_visiable = ref(false);

onMounted(() => {
    subscribe('show_isi_network_config_dialog', 'show_isi_network_config_dialog', () => {
        dialog_visiable.value = true;
    });
});

</script>

<template>
    <Dialog v-model:visible="dialog_visiable" modal header="ISI Network Config" style="width: 96vw; font-family: Avenir, Helvetica, Arial, sans-serif;" :pt="dialog_pt">
        <Fieldset legend="Home LAN">

        </Fieldset>
        <Fieldset legend="Office LAN">

        </Fieldset>
        <Fieldset legend="Office WAN">

        </Fieldset>
    </Dialog>
</template>

<style lang="css" scoped></style>