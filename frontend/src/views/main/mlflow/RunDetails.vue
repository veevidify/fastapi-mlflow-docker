<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3" v-if="!run">
      <div class="primary--text text--lighten-3">
        Run not found or not been fetched. --Refresh <!-- wip refresh btn -->
      </div>
    </v-card>

    <v-card class="ma-3 pa-3" v-if="run">
      <v-card-title primary-title>
        <div class="headline primary--text">Run Info</div>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">ID</div>
          <div class="primary--text text--darken-2">{{run.info.run_id}}</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Start time</div>
          <div class="primary--text text--darken-2">{{run.info.start_time}}</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">End time</div>
          <div class="primary--text text--darken-2">{{run.info.end_time}}</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Status</div>
          <div class="primary--text text--darken-2">{{run.info.status}}</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Artifacts root</div>
          <div class="primary--text text--darken-2">{{run.info.artifact_uri}}</div>
        </div>
      </v-card-text>
    </v-card>
    <v-card class="ma-3 pa-3" v-if="run">
      <v-card-title primary-title>
        <div class="headline primary--text">Run Data</div>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Metrics</div>
          <div class="primary--text text--darken-2">{{JSON.stringify(run.data.metrics)}}</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Training params</div>
          <div class="primary--text text--darken-2">{{JSON.stringify(run.data.params)}}</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Assigned tags</div>
          <div class="primary--text text--darken-2">{{JSON.stringify(run.data.tags)}}</div>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn
          @click="registerThisModel"
        >Register this model</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { dispatchQueryRunDetails, dispatchRegisterAModelFromRun } from '@/store/mlflow/actions';
import { readCurrentRun } from '@/store/mlflow/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class RunDetails extends Vue {

  public async mounted() {
    await dispatchQueryRunDetails(this.$store, { runId: this.$route.params.id });
  }

  public async registerThisModel() {
    const runId = this.run?.info.run_id;
    if (runId) {
      dispatchRegisterAModelFromRun(this.$store, {
        runId,
        modelMeta: {
          name: 'test from vue ui', // ideally pops a modal to enter name
        },
      });
    }
  }

  get run() {
    return readCurrentRun(this.$store);
  }
}
</script>
