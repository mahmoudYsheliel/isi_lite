<script setup lang="ts">

import { onMounted, ref } from 'vue';
import Fieldset from 'primevue/fieldset';
import 'primeicons/primeicons.css'
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import { useToast } from 'primevue/usetoast';
import { subscribe, post_event } from '@src/lib/mediator';
import { mqtt_connect,mqtt_disconnect } from '@src/lib/mqtt';
import { ConnectionType } from '@src/lib/models';
import Paho from 'paho-mqtt';
import SettingsIcon from '../icons/SettingsIcon.vue';

const toast_service = useToast()
onMounted(() => {

    local_storage_keys = Object.keys(localStorage)
    setup_data()
    subscribe('mqtt_test_connection_ok', 'mqtt_test_connection_ok', (args) => {
        toast_service.add({ severity: 'success', summary: 'Success', detail: 'Test Connection Succeded', life: 3000 });
        connection_test_status.value[args.order] = 'SUCCESS'
    })
    subscribe('mqtt_test_connection_err', 'mqtt_test_connection_err', (args) => {
        toast_service.add({ severity: 'error', summary: 'Failure', detail: 'Test Connection Failed', life: 3000 });
        connection_test_status.value[args.order] = 'FAILED'
    })
    subscribe('mqtt_test_connection_time_out', 'mqtt_test_connection_time_out', (args) => {
        if (connection_test_status.value[args.order] == 'SUCCESS')
            return
        toast_service.add({ severity: 'error', summary: 'Failure', detail: 'Test Connection Failed', life: 3000 });
        connection_test_status.value[args.order] = 'FAILED'
    })
});


// profile name is xyz
// xyz_profile_name:xyz
// xyz_username:
// xyz_pasword
// xyz_broler

//  get all keys
let local_storage_keys: string[]
const profile_names = ref<string[]>([])
const usernames = ref<string[]>([])
const passwords = ref<string[]>([])
const brokers = ref<string[]>([])
const connection_test_status = ref<ConnectionType[]>([])

let old_values_profile_names: (string | null)[] = []
let old_values_usernames: (string | null)[] = []
let old_values_passwords: (string | null)[] = []
let old_values_brokers: (string | null)[] = []

const selected_profile_name = ref()


function reset_values() {
    profile_names.value = []
    usernames.value = []
    passwords.value = []
    brokers.value = []

    old_values_profile_names = []
    old_values_usernames = []
    old_values_passwords = []
    old_values_brokers = []
}
function setup_data() {
    const mqtt_username = localStorage.getItem('mqtt_username') ?? '';
    const mqtt_password = localStorage.getItem('mqtt_password') ?? '';
    reset_values()
    for (let i = 0; i < local_storage_keys.length; i++) {
        if (local_storage_keys[i].includes('_profile_name')) {
            const profile_name = local_storage_keys[i]?.replace('_profile_name', '')
            profile_names.value.push(localStorage.getItem(local_storage_keys[i]) ?? 'NONE')
            usernames.value.push(localStorage.getItem(`${profile_name}_username`) ?? 'NONE')
            passwords.value.push(localStorage.getItem(`${profile_name}_password`) ?? 'NONE')
            brokers.value.push(localStorage.getItem(`${profile_name}_broker`) ?? 'NONE')
            connection_test_status.value.push('NONE')

            old_values_profile_names.push(localStorage.getItem(local_storage_keys[i]))
            old_values_usernames.push(localStorage.getItem(`${profile_name}_username`))
            old_values_passwords.push(localStorage.getItem(`${profile_name}_password`))
            old_values_brokers.push(localStorage.getItem(`${profile_name}_broker`))

            if (localStorage.getItem(`${profile_name}_username`) == mqtt_username &&
                localStorage.getItem(`${profile_name}_password`) == mqtt_password
            ) {
                selected_profile_name.value = localStorage.getItem(local_storage_keys[i])
            }
        }
    }
}

function add_profile() {
    profile_names.value.push('')
    brokers.value.push('')
    usernames.value.push('')
    passwords.value.push('')
    connection_test_status.value.push('NONE')
}
function check_value_update(order: number) {
    if (profile_names.value[order] === old_values_profile_names[order] &&
        brokers.value[order] === old_values_brokers[order] &&
        usernames.value[order] === old_values_usernames[order] &&
        passwords.value[order] === old_values_passwords[order]
    )
        return true
    if (profile_names.value[order] === '' ||
        brokers.value[order] === '' ||
        usernames.value[order] === '' ||
        passwords.value[order] === ''
    )
        return true
    return false
}
function check_value(order: number) {
    if (profile_names.value[order] === '' ||
        brokers.value[order] === '' ||
        usernames.value[order] === '' ||
        passwords.value[order] === ''
    )
        return true
    return false
}

function save_profile(order: number) {
    if (profile_names.value[order] && brokers.value[order] && usernames.value[order] && passwords.value[order]) {
        let profile_name = profile_names.value[order].replace(/ /g, '_')
        localStorage.setItem(`${profile_name}_profile_name`, profile_names.value[order])
        localStorage.setItem(`${profile_name}_broker`, brokers.value[order])
        localStorage.setItem(`${profile_name}_username`, usernames.value[order])
        localStorage.setItem(`${profile_name}_password`, passwords.value[order])
    }
}

function delete_profile(order: number) {
    let profile_name = profile_names.value[order].replace(/ /g, '_')
    localStorage.removeItem(`${profile_name}_profile_name`)
    localStorage.removeItem(`${profile_name}_broker`)
    localStorage.removeItem(`${profile_name}_username`)
    localStorage.removeItem(`${profile_name}_password`)

    profile_names.value.splice(order, 1)
    brokers.value.splice(order, 1)
    usernames.value.splice(order, 1)
    passwords.value.splice(order, 1)
}

function connect(order: number) {
    const broker_port = 9001
    let rand_seq = (Math.random() + 1).toString(36).slice(-8);
    let test_connection_id = `test_connection.${rand_seq}`;
    let test_client = new Paho.Client(brokers.value[order], broker_port, 'isi_client.' + test_connection_id);

    test_client.connect({
        userName: usernames.value[order],
        password: passwords.value[order],
        onSuccess: () => {
            test_client.subscribe(`data/${test_connection_id}/response/nodered_connection`);
            test_client.onMessageArrived = (msg: Paho.Message) => {
                if (msg.destinationName == `data/${test_connection_id}/response/nodered_connection`) {
                    mqtt_disconnect()
                    mqtt_connect(brokers.value[order], usernames.value[order], passwords.value[order])
                }
            }
            let msg = new Paho.Message('X');
            msg.destinationName = `data/${test_connection_id}/request/nodered_connection`;
            test_client.send(msg);
        },
        onFailure: () => {
            post_event('mqtt_test_connection_err', { order: order })
        },
    });
    test_client.disconnect()
    
}

function test(order: number) {
    connection_test_status.value[order] = 'PENDDING'
    const broker_port = 9001
    let rand_seq = (Math.random() + 1).toString(36).slice(-8);
    let test_connection_id = `test_connection.${rand_seq}`;
    let test_client = new Paho.Client(brokers.value[order], broker_port, 'isi_client.' + test_connection_id);

    test_client.connect({
        userName: usernames.value[order],
        password: passwords.value[order],
        onSuccess: () => {
            test_client.subscribe(`data/${test_connection_id}/response/nodered_connection`);
            test_client.onMessageArrived = (msg: Paho.Message) => {
                if (msg.destinationName == `data/${test_connection_id}/response/nodered_connection`) {
                    post_event('mqtt_test_connection_ok', { order: order })
                }
            }
            let msg = new Paho.Message('X');
            msg.destinationName = `data/${test_connection_id}/request/nodered_connection`;
            test_client.send(msg);
            setTimeout(() => { post_event('mqtt_test_connection_time_out', { order: order }) }, 3000)
        },
        onFailure: () => {
            post_event('mqtt_test_connection_err', { order: order })
        },
    });
    test_client.disconnect()
}




</script>

<template>
   
    <div class="ISINet_con">
        <div class="isi_network_config_header">
            <SettingsIcon fill_color="white" style="height: 32px;"/>
            <p style="font-size: 20px;">Network Configuration</p>

        </div>
        
        <div class="ISInetwork_profile"  v-for="( profile_name, i) in profile_names" :class="{ selected: profile_name == selected_profile_name }">
            <Fieldset style="border: none;" legend="Home LAN" itemscope="pi pi-plus">
                <template #legend>
                    <div class="fieldset_header">
                        <i class="pi pi-trash" outlined rounded severity="danger" style="color: #dc3545; border: none; width: fit-content;" @click="delete_profile(i)" />
                        <span v-if="profile_names[i]">{{ profile_names[i] }}</span>
                        <span style="color: gray;" v-if="!profile_names[i]"> Untitled</span>
                    </div>
                </template>
                <div class="field_container">
                    <div class="element">
                        <p>Profile Name: </p>
                        <InputText v-model="profile_names[i]" class="input" />
                    </div>
                    <div class="element">
                        <p>Broker IP: </p>
                        <InputText v-model="brokers[i]" class="input" />
                    </div>
                    <div class="element">
                        <p>Username: </p>
                        <InputText v-model="usernames[i]" class="input" />
                    </div>
                    <div class="element">
                        <p>Password: </p>
                        <InputText v-model="passwords[i]" class="input" />

                    </div>
                </div>
                <div class="field_actions">
                    <Button label="Connect" icon="pi pi-link" :disabled="check_value(i)" @click="connect(i)" />
                    <Button label="Save" icon="pi pi-save" :disabled="check_value_update(i)" @click="save_profile(i)" />
                    <Button label="Test" icon="pi pi-wifi" :disabled="check_value(i)" @click="test(i)" v-if="connection_test_status[i] == 'NONE'" />
                    <Button label="Test" icon="pi pi-times" :disabled="check_value(i)" @click="test(i)" severity="danger" v-if="connection_test_status[i] == 'FAILED'" />
                    <Button label="Test" icon="pi pi-spinner" :disabled="check_value(i)" @click="test(i)" severity="warn" v-if="connection_test_status[i] == 'PENDDING'" />
                    <Button label="Test" icon="pi pi-check" :disabled="check_value(i)" @click="test(i)" severity="success" v-if="connection_test_status[i] == 'SUCCESS'" />
                </div>

            </Fieldset>
        </div>


    </div>
    <div class="add_button_con">
        <Button class="add_button" icon="pi pi-plus" @click="add_profile" />
    </div>


</template>

<style lang="css" scoped>
.isi_network_config_header {
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
.ISInetwork_profile {
    background-color: white;
    border-radius: 8px;
    padding: 4px;
}

.selected {
    border: black 2px solid;
    box-shadow: rgba(0, 0, 0, 0.24) 0px 4px 8px;
}


.field_actions {
    margin-top: 24px;
    display: flex;
    justify-content: space-between;
    width: 100%;


}

.ISINet_con {
    overflow-y: scroll;
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 30px;
    height: 100%;

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