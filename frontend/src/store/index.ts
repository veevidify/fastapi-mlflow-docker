import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';

import { State } from './state';
import { mainModule } from './main';
import { adminModule } from './admin';
import { mlflowModule } from './mlflow';

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
    admin: adminModule,
    mlflow: mlflowModule,
  },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
