import { IRun, IRunInfo, IRegisteredModel, IMsg, WithTaskId, ITaskPayload } from '@/interfaces';
import { MLFlowState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setRunInfos(state: MLFlowState, payload: IRunInfo[]) {
        state.runInfos = payload;
    },
    setRegisteredModels(state: MLFlowState, payload: IRegisteredModel[]) {
        state.registeredModels = payload;
    },
    setCurrentTask(state: MLFlowState, payload: IMsg) {
        state.currentTask = payload;
    },
    updateTaskId(state: MLFlowState, payload: IMsg & WithTaskId) {
        state.taskResult = {
        task_id: payload.task_id,
        task_status: 'pending',
        task_result: 'pending',
        };
    },
    updateTaskResult(state: MLFlowState, payload: ITaskPayload | null) {
        state.taskResult = payload;
    },
    setCurrentRun(state: MLFlowState, payload: IRun) {
        state.currentRun = payload;
    },
};

const { commit } = getStoreAccessors<MLFlowState, State>('');

export const commitSetRunInfos = commit(mutations.setRunInfos);
export const commitSetRegisteredModels = commit(mutations.setRegisteredModels);
export const commitSetCurrentTask = commit(mutations.setCurrentTask);
export const commitUpdateTaskId = commit(mutations.updateTaskId);
export const commitUpdateTaskResult = commit(mutations.updateTaskResult);
export const commitSetCurrentRun = commit(mutations.setCurrentRun);
