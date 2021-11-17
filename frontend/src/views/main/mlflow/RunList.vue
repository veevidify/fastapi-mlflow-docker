<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Recorded Training Runs
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/mlflow/train">New Training Run</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="runs">
      <template slot="items" slot-scope="props">
        <td>
          <router-link :to="{name: 'main-mlflow-run-details', params: {id: props.item.run_id}}">
            {{ props.item.run_id }}
          </router-link>
        </td>
        <td>{{ props.item.start_time }}</td>
        <td>{{ props.item.end_time }}</td>
        <td>{{ props.item.status }}</td>
        <td>{{ props.item.artifact_uri }}</td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { dispatchGetAllRunInfos } from '@/store/mlflow/actions';
import { readRunInfos } from '@/store/mlflow/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class RunList extends Vue {
  public headers = [
    {
      text: 'Run ID',
      value: 'run_id',
      align: 'left',
    },
    {
      text: 'Start Time',
      sortable: true,
      value: 'start_time',
      align: 'left',
    },
    {
      text: 'End Time',
      sortable: true,
      value: 'end_time',
      align: 'left',
    },
    {
      text: 'Status',
      sortable: true,
      value: 'status',
      align: 'left',
    },
    {
      text: 'Artifact',
      sortable: true,
      value: 'artifact_uri',
      align: 'left',
    },
  ];

  public async mounted() {
    await dispatchGetAllRunInfos(this.$store);
  }

  get runs() {
    return readRunInfos(this.$store);
  }
}
</script>
