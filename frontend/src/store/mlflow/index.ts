import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { MLFlowState } from './state';

const defaultState: MLFlowState = {
  runInfos: [],
  registeredModels: [],
  currentTrainingTask: { alpha: 0, l1_ratio: 0 },
  trainingTaskResult: null,
  currentRunId: '',
  currentRun: null,
  currentRegisteredModel: null,
};

export const mlflowModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
