import { api } from '@/api';
import { ActionContext } from 'vuex';
import { IUserProfileCreate, IUserProfileUpdate } from '@/interfaces';
import { State } from '../state';
import { MLFlowState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';

type MainContext = ActionContext<MLFlowState, State>;

export const actions = {};
const { dispatch } = getStoreAccessors<MLFlowState, State>('');
