import { api } from '@/api';
import { ActionContext } from 'vuex';
import { IEnetParam, WithTaskId, IModelCreateMeta } from '@/interfaces';
import { State } from '../state';
import { MLFlowState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import {
    commitUpdateCurrentRunId,
    commitUpdateTaskId,
    commitUpdateTaskResult,
    commitSetRunInfos,
    commitSetCurrentRegisteredModel,
    commitSetCurrentRun,
    commitSetCurrentTask,
    commitSetRegisteredModels,
} from './mutations';

import { dispatchCheckApiError } from '../main/actions';

type MainContext = ActionContext<MLFlowState, State>;

export const actions = {
    async actionSendTaskTrainModel(context: MainContext, payload: IEnetParam) {
        commitSetCurrentTask(context, payload);
        const authToken = context.rootState.main.token;
        try {
            const taskHandle = await api.trainModel(payload, authToken);
            const data = taskHandle.data;
            commitUpdateTaskId(context, data);
        } catch (e) {
            const err = { msg: e, task_id: e };
            commitUpdateTaskId(context, err);
            await dispatchCheckApiError(context, e);
        }
    },
    async actionPollTaskResult(context: MainContext, payload: {} & WithTaskId) {
        const currentTaskId = context.state.trainingTaskResult?.task_id || '';

        const authToken = context.rootState.main.token;
        if (! currentTaskId) {
            const err = { msg: 'No task_id' , task_id: currentTaskId };
            commitUpdateTaskId(context, err);
        } else {
            try {
                const resultData = await api.getTaskStatus(currentTaskId, authToken);
                const { data } = resultData;

                commitUpdateTaskResult(context, data);
            } catch (e) {
                const err = {
                    task_id: currentTaskId,
                    task_result: e,
                    task_status: 'failed',
                };
                commitUpdateTaskResult(context, err);
                await dispatchCheckApiError(context, e);
            }
        }
    },
    // remove current task's info to refresh the view
    async actionClearCurrentTask(context: MainContext) {
        commitSetCurrentTask(context, { alpha: 0, l1_ratio: 0 });
        commitUpdateTaskResult(context, null);
    },
    async actionQueryRunDetails(context: MainContext, payload: { runId: string }) {
        const authToken = context.rootState.main.token;
        try {
            const resp = await api.getSingleRun(payload.runId, authToken);
            const { data } = resp;
            commitSetCurrentRun(context, data);
        } catch (e) {
            // wip: update the view
            await dispatchCheckApiError(context, e);
        }
    },
    async actionGetAllRunInfos(context: MainContext) {

    },
    async actionGetAllRegisteredModels(context: MainContext) {

    },
    async actionRegisterAModelFromRun(context: MainContext, payload: { runId: string, modelMeta: IModelCreateMeta }) {

    },
};

const { dispatch } = getStoreAccessors<MLFlowState, State>('');

export const dispatchSendTaskTrainModel = dispatch(actions.actionSendTaskTrainModel);
export const dispatchPollTaskResult = dispatch(actions.actionPollTaskResult);
export const dispatchClearCurrentTask = dispatch(actions.actionClearCurrentTask);
export const dispatchQueryRunDetails = dispatch(actions.actionQueryRunDetails);
export const dispatchGetAllRunInfos = dispatch(actions.actionGetAllRunInfos);
export const dispatchGetAllRegisteredModels = dispatch(actions.actionGetAllRegisteredModels);
export const dispatchRegisterAModelFromRun = dispatch(actions.actionRegisterAModelFromRun);
