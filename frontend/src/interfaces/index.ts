declare global {
    type GObject = {
        [key: string]: any,
    };
}

export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IMsg {
    msg: string;
}

export interface WithTaskId {
    task_id: string;
}

export interface ITaskStatus {
    task_status: string;
    task_result: string;
}

export type ITaskPayload = ITaskStatus & WithTaskId;

export interface IWSMessage {
    scope: string;
    intent: string;
    by: string;
    message: string;
}

export interface IEnetParam {
    alpha: number;
    l1_ratio: number;
}

export interface IRunInfo {
    artifact_uri: string;
    start_time: number;
    end_time: number | null;
    run_id: string;
    status: string;
    user_id: string;
}

export interface IRunData {
    metrics: GObject;
    params: GObject;
    tags: GObject;
}

export interface IRun {
    data: IRunData;
    info: IRunInfo;
}

export interface IModelVersion {
    name: string;
    current_stage: string;
    description: string;
    run_id: string;
    run_link: string;
    source: string;
    status: string;
    status_message: string;
    user_id: string;
    version: string;
    creation_timestamp: number;
    last_updated_timestamp: number;
    tags: GObject;
}

export interface IRegisteredModel {
    latest_versions: IModelVersion[];
    name: string;
    description: string;
    creation_timestamp: number;
    last_updated_timestamp: number;
    tags: GObject;
}

export interface IModelCreateMeta {
    name: string;
}

export interface IInputData {
    age: number;
    sex: number;
    bmi: number;
    bp: number;
    s1: number;
    s2: number;
    s3: number;
    s4: number;
    s5: number;
    s6: number;
}
