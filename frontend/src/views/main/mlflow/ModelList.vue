<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Registered Enet Models for Diabetes data
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <!-- <v-btn color="primary" to="/main/mlflow/train">New Training Run</v-btn> -->
    </v-toolbar>
    <v-data-table :headers="headers" :items="models">
      <template slot="items" slot-scope="props">
        <td>
          <router-link :to="{name: 'main-mlflow-model-details', params: {name: props.item.name}}">
            {{ props.item.name }}
          </router-link>
        </td>
        <td>
          <router-link :to="{name: 'main-mlflow-run-details', params: {id: props.item.latest_versions[0].run_id}}">
            {{ props.item.latest_versions[0].run_id }}
          </router-link>
        </td>
        <td>{{ props.item.latest_versions[0].version }}</td>
        <td>{{ props.item.creation_timestamp }}</td>
        <td>{{ props.item.last_updated_timestamp }}</td>
        <td>{{ props.item.latest_versions[0].source }}</td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { dispatchGetAllRegisteredModels } from '@/store/mlflow/actions';
import { readRegisteredModels } from '@/store/mlflow/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class ModelList extends Vue {
  public headers = [
    {
      text: 'Model name',
      value: 'model_name',
      sortable: true,
      align: 'left',
    },
    {
      text: 'Run ID',
      value: 'run_id',
      sortable: true,
      align: 'left',
    },
    {
      text: 'Version',
      value: 'version',
      sortable: true,
      align: 'left',
    },
    {
      text: 'Created at',
      value: 'created_at',
      sortable: true,
      align: 'left',
    },
    {
      text: 'Updated at',
      value: 'updated_at',
      sortable: true,
      align: 'left',
    },
    {
      text: 'Source',
      value: 'source',
      sortable: true,
      align: 'left',
    },
  ];

  public async mounted() {
    await dispatchGetAllRegisteredModels(this.$store);
  }

  get models() {
    return readRegisteredModels(this.$store);
  }
}
</script>
