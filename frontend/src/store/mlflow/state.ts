import { IMsg, IRegisteredModel, IRun, IRunInfo, ITaskPayload } from '@/interfaces';

export interface MLFlowState {
  runInfos: IRunInfo[];
  registeredModels: IRegisteredModel[];
  currentTask: IMsg;
  taskResult: ITaskPayload | null;
  currentRun: IRun | null;
}
