import { MainState } from './main/state';
import { AdminState } from './admin/state';
import { MLFlowState } from './mlflow/state';

export interface State {
    main: MainState;
    admin: AdminState;
    mlflow: MLFlowState;
}
