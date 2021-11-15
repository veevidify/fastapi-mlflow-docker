import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { MLFlowState } from './state';

const defaultState: MLFlowState = {
  runInfos: [],
  registeredModels: [],
  currentTask: { msg: '' },
  taskResult: null,
  currentRun: null,
};

export const mlflowModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
