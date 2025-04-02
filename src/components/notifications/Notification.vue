<script setup lang="ts">

import { onMounted } from 'vue';
import Toast from 'primevue/toast';

import { subscribe } from '../../lib/mediator';
import { useToast } from "primevue/usetoast";

type ToastPosition = 'g-tc' | 'g-c';

type ToastMsgType = 'success'
    | 'info'
    | 'warn'
    | 'success';

const toast_service = useToast();

onMounted(() => {

    subscribe('show_toast', 'show_toast_func', (args: any) => {
        const pos = args.pos as ToastPosition;
        const type = args.type as ToastMsgType;
        const title = args.title as string | undefined;
        const body = args.body as string;
        const time = args.time as number | undefined;

        toast_service.add({
            severity: type,
            detail: body,
            group: pos ?? 'g-c',
            summary: title ?? type.toUpperCase(),
            life: time ?? 3000,
        });
    });
});

</script>

<template>
    <Toast class="top_center_notif" position="top-center" group="g-tc" />
    <Toast class="center_notif" position="center" group="g-c" :pt="{
        root: { style: 'opacity: 1;font-family:Cairo;border-left:4px solid #FFFFFF' },
        message: { style: 'border-color: #FFFFFF;background-color: #000000' },
        messageText: { style: 'background-color: #000000; color: #FFFFFF' },
        messageIcon: { style: 'color: #FFFFFF;width:48px;height:48px;position:relative;top:8px' },
        summary: { style: 'display: inline-block;font-size:16px' },
        detail: { style: 'font-weight: bold; font-size: 24px;color: #FFFFFF;' },
        closeIcon: { style: 'color: #FFFFFF;height:16px;width:16px;' },
        closeButton:{style:'overflow:visible;margin-right:16px;;margin-top:16px'},
    }" />
</template>

<style scoped>

</style>