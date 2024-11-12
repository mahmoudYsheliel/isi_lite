export type DeviceType = "SWITCH_1CH" | "SWITCH_4CH" | "TEMP" | "HUMD" | "PLUG_1CH" | "RGB" | "SEC_LOCK" | "FLOOD" | "MOTION" | "DIMMER_2CH" | "DIMMER_4CH";
export type LinkType = "LIVE" | "SUSPEND";

export interface Room {
    room_id: number;
    room_name: string;
    temp: string;
    humd: string;
};

export interface DeviceConfig {
    config_name: string;
    config_val: string | number | boolean;
};

export interface Device {
    device_uuid: string;
    device_name: string;
    room_id: number;
    device_type: DeviceType;
    link_type: LinkType;
    is_online: boolean;
    device_config: DeviceConfig[];
};

export interface ISINetworkConfig {
    isi_net_username: string;
    isi_net_password: string;
    server_addr: string;
    server_port: string;
    enable_tls: boolean;
};