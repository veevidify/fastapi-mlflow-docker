import { MLFlowState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
  getRunInfos: (state: MLFlowState) => state.runInfos,
  getRegisteredModels: (state: MLFlowState) => state.registeredModels,
  currentTrainingTask: (state: MLFlowState) => state.currentTrainingTask,
  trainingTaskResult: (state: MLFlowState) => state.trainingTaskResult,
  currentRunId: (state: MLFlowState) => state.currentRunId,
  currentRun: (state: MLFlowState) => state.currentRun,
  currentRegisteredModel: (state: MLFlowState) => state.currentRegisteredModel,
};

const { read } = getStoreAccessors<MLFlowState, State>('');

export const readRunInfos = read(getters.getRunInfos);
export const readRegisteredModels = read(getters.getRegisteredModels);
export const readCurrentTrainingTask = read(getters.currentTrainingTask);
export const readTrainingTaskResult = read(getters.trainingTaskResult);
export const readCurrentRunId = read(getters.currentRunId);
export const readCurrentRun = read(getters.currentRun);
export const readCurrentRegisteredModel = read(getters.currentRegisteredModel);
