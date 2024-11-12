import Paho from 'paho-mqtt';
import { post_event } from '@src/lib/mediator';

let connection_id: string | null = null;
let client: Paho.Client | null = null;

function mqtt_read_handler(msg: Paho.Message) {
    if (msg.destinationName.startsWith(`data/${connection_id}/response`)) {
        const data_resource = msg.destinationName.split('/').slice(-1)[0];
        post_event('data_response_' + data_resource, { payload: msg.payloadString });
    } else if (msg.destinationName.startsWith('state/')) {
        const device_mqtt_id = msg.destinationName.split('/')[1];
        const device_pref = msg.destinationName.split('/')[2];
        const device_pref_type = device_pref.split('_')[0];
        post_event(`sensor_state_${device_pref_type}`, { device_mqtt_id, payload: msg.payloadString });
    }
}

function mqtt_publish(topic: string, payload: string): boolean {
    if (!client?.isConnected())
        return false;

    let msg = new Paho.Message(payload);
    msg.destinationName = topic;
    client.send(msg);
    return true;
}

export function mqtt_connect() {
    if (client?.isConnected())
        return;

    const broker_ip = localStorage.getItem('broker_ip') ?? '127.0.0.1';
    const broker_port = 9001
    const mqtt_username = localStorage.getItem('mqtt_username') ?? '';
    const mqtt_password = localStorage.getItem('mqtt_password') ?? '';
    const rand_seq = (Math.random() + 1).toString(36).slice(-8);
    const isi_username = (localStorage.getItem('isi_username') ?? 'NONE').replace(/\s/g, '_').toLowerCase(); // replace ' ' with '_'
    connection_id = `${isi_username}.${rand_seq}`;
    console.log(connection_id);

    client = new Paho.Client(broker_ip, broker_port, 'isi_client.' + connection_id);
    client.connect({
        userName: mqtt_username,
        password: mqtt_password,
        onSuccess: () => post_event('mqtt_connection_ok', {}),
        onFailure: () => post_event('mqtt_connection_err', {}),
    });
    client.onMessageArrived = mqtt_read_handler;
    client.onConnectionLost = () => post_event('mqtt_connection_err', {});
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

export function request_data_resource(data_resource: string, args: Object = {}): boolean {
    const data_resource_topic = `data/${connection_id}/request/${data_resource}`;
    return mqtt_publish(data_resource_topic, JSON.stringify(args));
}