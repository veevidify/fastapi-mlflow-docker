import axios from 'axios';
import { apiUrl } from '@/env';
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IMsg,
  WithTaskId,
  ITaskPayload,
  IEnetParam,
  IRunInfo,
  IModelVersion,
  IRegisteredModel,
  IRun,
  IModelCreateMeta,
  IInputData,
} from './interfaces';

function configWithAuthHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    withCredentials: true,
  };
}

const apiPrefix = apiUrl + '/api/v1';

export const api = {
  // == auth == //
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiPrefix}/login/access-token`, params);
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiPrefix}/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiPrefix}/reset-password/`, {
      new_password: password,
      token,
    });
  },

  // == basic crud == //
  async getMe(token: string) {
    return axios.get<IUserProfile>(
      `${apiPrefix}/users/me`,
      configWithAuthHeaders(token),
    );
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(
      `${apiPrefix}/users/me`,
      data,
      configWithAuthHeaders(token),
    );
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(
      `${apiPrefix}/users/`,
      configWithAuthHeaders(token),
    );
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(
      `${apiPrefix}/users/${userId}`,
      data,
      configWithAuthHeaders(token),
    );
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(
      `${apiPrefix}/users/`,
      data,
      configWithAuthHeaders(token),
    );
  },

  // == bg tasks == //
  async queueTask(taskParam: IMsg, token: string) {
    return axios.post<IMsg & WithTaskId>(
      `${apiPrefix}/utils/queue-celery-task/`,
      taskParam,
      configWithAuthHeaders(token),
    );
  },
  async getTaskStatus(taskId: string, token: string) {
    return axios.get<ITaskPayload>(
      `${apiPrefix}/utils/task-status/${taskId}`,
      configWithAuthHeaders(token),
    );
  },

  // == mlflow == //
  async trainModel(enetParam: IEnetParam, token: string) {
    return axios.post<IMsg & WithTaskId>(
      `${apiPrefix}/ml/train-model`,
      enetParam,
      configWithAuthHeaders(token),
    );
  },
  async getRuns(token: string) {
    return axios.get<IRunInfo[]>(
      `${apiPrefix}/ml/runs`,
      configWithAuthHeaders(token),
    );
  },
  async getSingleRun(runId: string, token: string) {
    return axios.get<IRun>(
      `${apiPrefix}/ml/run/${runId}`,
      configWithAuthHeaders(token),
    );
  },
  async getRegisteredModels(token: string) {
    return axios.get<IRegisteredModel[]>(
      `${apiPrefix}/ml/registered-models`,
      configWithAuthHeaders(token),
    );
  },
  async registerAModel(runId: string, modelMeta: IModelCreateMeta, token: string) {
    return axios.post<IModelVersion>(
      `${apiPrefix}/ml/run/${runId}/register-model`,
      modelMeta,
      configWithAuthHeaders(token),
    );
  },
  async archiveModel(modelName: string, token: string) {
    return axios.get(
      `${apiPrefix}/ml/model/${modelName}/archive`,
      configWithAuthHeaders(token),
    );
  },
  async restoreModel(modelName: string, token: string) {
    return axios.get(
      `${apiPrefix}/ml/model/${modelName}/unarchive`,
      configWithAuthHeaders(token),
    );
  },
  async predictWithModel(modelName: string, inputData: IInputData, token: string) {
    return axios.post(
      `${apiPrefix}/ml/model/${modelName}/predict`,
      inputData,
      configWithAuthHeaders(token),
    );
  },
};
