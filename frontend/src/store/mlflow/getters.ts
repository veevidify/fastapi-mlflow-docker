import { MLFlowState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
  getRunInfos: (state: MLFlowState) => state.runInfos,
  getRegisteredModels: (state: MLFlowState) => state.registeredModels,
  currentTask: (state: MLFlowState) => state.currentTask,
  taskResult: (state: MLFlowState) => state.taskResult,
  currentRun: (state: MLFlowState) => state.currentRun,
};

const { read } = getStoreAccessors<MLFlowState, State>('');

export const readRunInfos = read(getters.getRunInfos);
export const getRegisteredModels = read(getters.getRegisteredModels);
export const readCurrentTask = read(getters.currentTask);
export const readTaskResult = read(getters.taskResult);
export const readCurrentRun = read(getters.currentRun);
