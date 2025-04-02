import Paho from 'paho-mqtt';
import { post_event, subscribe } from '@src/lib/mediator';
import { RecordedCommand } from './models';
let connection_id: string | null = null;
let client: Paho.Client | null = null;
let mode = 'Normal'
let actions: RecordedCommand[] = []

function mqtt_read_handler(msg: Paho.Message) {
    // mqtt data requests
    if (msg.destinationName.startsWith(`data/${connection_id}/response`)) {
        const data_resource = msg.destinationName.split('/').slice(-1)[0];
        post_event('data_response_' + data_resource, { payload: msg.payloadString });
    }

    // mqtt device state
    else if (msg.destinationName.startsWith('state/')) {
        const [_, device_mqtt_id, device_pref] = msg.destinationName.split('/');
        post_event('sensor_state', { device_mqtt_id, device_pref, payload: msg.payloadString });
    }

    else if (msg.destinationName === 'telem/client/notif') {

        const parsed_msg = JSON.parse(msg.payloadString)

        const toast = {
            type: parsed_msg?.msg_lvl,
            body: parsed_msg?.msg_body,
            time: 0,
            title: `Room: ${parsed_msg?.room} \n Device: ${parsed_msg?.device}`
        }
        post_event('show_toast', toast);
    }
    else if (msg.destinationName === 'telem/client/smart_scene') {
        post_event('request_smart_scenes', {});
    }
    else if (msg.destinationName === 'telem/client/smart_scene_executed') {
        post_event('smart_scene_executed', {title:msg.payloadString})
    }
    else if (msg.destinationName === 'telem/client/smart_scene_updated') {
        post_event('smart_scene_updated', {})
    }
}

export function mqtt_publish(topic: string, payload: string, device_name?: string): boolean {
    if (!client?.isConnected())
        return false;

    let msg = new Paho.Message(payload);
    msg.destinationName = topic;
    client.send(msg);
    const motion_sensor_pattern = /^conf\/[a-zA-Z0-9_]+\/motion_sensor_mode$/;
    if ((topic.startsWith('rpc') || motion_sensor_pattern.test(topic)) && mode == 'Recording') {
        actions.push({ topic: topic, payload: payload, device_name: device_name })
    }
    return true;
}

export function mqtt_connect(broker: string, username: string, password: string) {
    if (client?.isConnected()) {
        post_event('mqtt_connection_ok', {});
        return;
    }

    const broker_ip = broker ?? '127.0.0.1';
    const broker_port = 9001
    const mqtt_username = username ?? 'isi_muser';
    const mqtt_password = password ?? 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX';
    const rand_seq = (Math.random() + 1).toString(36).slice(-8);
    const isi_username = (localStorage.getItem('isi_username') ?? 'NONE').replace(/\s/g, '_').toLowerCase(); // replace ' ' with '_'
    connection_id = `${isi_username}.${rand_seq}`;

    client = new Paho.Client(broker_ip, broker_port, 'isi_client.' + connection_id);
    client.connect({
        userName: mqtt_username,
        password: mqtt_password,
        onSuccess: () => { post_event('mqtt_connection_ok', {}); localStorage.setItem('mqtt_username', username); localStorage.setItem('mqtt_password', password); localStorage.setItem('broker_ip', broker) },
        onFailure: () => post_event('mqtt_connection_err', {}),
    });
    client.onMessageArrived = mqtt_read_handler;
    client.onConnectionLost = (err) => post_event('mqtt_connection_err', { err });
}

export function mqtt_disconnect(){
    if (client?.isConnected()) {
        client.disconnect()
    }
}
export function is_connected(){
    const mqtt_password = localStorage.getItem("mqtt_password")
    const mqtt_username = localStorage.getItem("mqtt_username")
    const broker_ip = localStorage.getItem("broker_ip")
    return (mqtt_password && mqtt_username && broker_ip)
}
export function delete_username_pass(){
    localStorage.removeItem('mqtt_username')
    localStorage.removeItem('mqtt_password')
    localStorage.removeItem('broker_ip')
}

export function attach_data_service() {
    if (!client?.isConnected())
        return;
    client.subscribe(`data/${connection_id}/response/#`);
    post_event('mqtt_data_service_ready', {});
}

export function attach_sensor_service() {
    if (!client?.isConnected())
        return;
    client.subscribe('state/#');
}
export function attach_telem_notification() {
    if (!client?.isConnected())
        return;
    client.subscribe("telem/client/#");
}

export function request_data_resource(data_resource: string, args: Object = {}): boolean {
    const data_resource_topic = `data/${connection_id}/request/${data_resource}`;
    return mqtt_publish(data_resource_topic, JSON.stringify(args));
}


subscribe('screen_record_start', 'screen_record_start_mqtt', (args) => {
    if (args.actions)
        actions = args.actions
    else
        actions = []
    mode = 'Recording'
})
subscribe('stop_recording', 'stop_recording_mqtt', () => {
    mode = 'Normal'
    post_event('actions_recorded', { actions: actions })
})