export type DeviceType = "SWITCH_1CH" | "SWITCH_4CH" | "TEMP" | "HUMD" | "PLUG_1CH" | "RGB" | "SEC_LOCK" | "FLOOD" | "MOTION" | "DIMMER_2CH" | "DIMMER_4CH" | "AIR_Q";
export type LinkType = "LIVE" | "SUSPEND";
export type ConnectionType = "NONE" | "FAILED" | "SUCCESS" | "PENDDING";
export type Mode = 'Normal' | 'Recording'

export interface Room {
    room_id: number;
    room_name: string;
    temp: string;
    humd: string;
    air_q:string;
};


// export interface DeviceConfig {
//     config_name: string;
//     config_val: string | number | boolean;
// };

export interface Device {
    device_uuid: string;
    device_name: string;
    room_id: number;
    device_type: DeviceType;
    link_type: LinkType;
    is_online: boolean;
    device_config: object;
};

export interface ISINetworkConfig {
    isi_net_username: string;
    isi_net_password: string;
    server_addr: string;
    server_port: string;
    enable_tls: boolean;
};

export interface RecordedCommand {
    topic: string
    payload: string
    device_name?:string
    
}

export interface Scene {
    actions: RecordedCommand[]
    title: string
    icon_label: string
    color:string
}