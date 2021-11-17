import { IMsg, IRegisteredModel, IRun, IRunInfo, ITaskPayload, IModelVersion, IEnetParam } from '@/interfaces';

export interface MLFlowState {
  runInfos: IRunInfo[];
  registeredModels: IRegisteredModel[];

  currentTrainingTask: IEnetParam;
  trainingTaskResult: ITaskPayload | null;

  currentRunId: string;
  currentRun: IRun | null;
  currentRegisteredModel: IModelVersion | null;
}
