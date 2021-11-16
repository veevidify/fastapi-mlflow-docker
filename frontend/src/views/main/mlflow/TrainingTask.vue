<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Train Elasticnet Diabetes Model</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Model hyper-parameters</div>
            <div
              class="title primary--text text--darken-2"
              v-if="task"
            >alpha: {{task.alpha}} - l1_ratio: {{task.l1_ratio}}</div>
          </div>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
            <v-text-field
              label="alpha"
              name="alpha"
              v-model="alpha"
              required
            >
            </v-text-field>
            <v-text-field
              label="l1_ratio"
              name="l1_ratio"
              v-model="l1"
              required
            >
            </v-text-field>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="sendTrainingTask"
          :disabled="!valid"
        >
          Send
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Training Task (by celery)</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Task:</div>
            <div
              class="title primary--text text--darken-2"
              v-if="task"
            >{{task.task_id}}</div>
            <v-spacer></v-spacer>
            <div class="subheading secondary--text text--lighten-2">Status:</div>
            <div
              class="title primary--text text--darken-2"
              v-if="task"
            >{{task.task_status}}</div>
            <div class="subheading secondary--text text--lighten-2">Result (MLFlow run_id):</div>
            <div
              class="title primary--text text--darken-2"
              v-if="task"
            >{{task.task_result}}</div>
          </div>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="pollTask">
          Poll
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IEnetParam, IMsg, ITaskPayload, ITaskStatus, WithTaskId } from '@/interfaces';
import { dispatchSendTaskTrainModel, dispatchPollTaskResult, dispatchClearCurrentTask } from '@/store/mlflow/actions';
import { readCurrentTrainingTask, readTrainingTaskResult } from '@/store/mlflow/getters';

@Component
export default class TrainingTask extends Vue {
  public alpha: number = 0;
  public setAlpha = false;
  public l1: number = 0;
  public setL1 = false;

  public valid = true;
  public pollValid = true;

  public async mounted() {
    //
  }

  public reset() {
    this.alpha = 0;
    this.l1 = 0;
    dispatchClearCurrentTask(this.$store);
  }

  public async sendTrainingTask() {
    if (await this.$validator.validateAll()) {
      const payload: IEnetParam = {
        alpha: this.alpha,
        l1_ratio: this.l1,
      };

      //
      await dispatchSendTaskTrainModel(this.$store, payload);
    }
  }

  public async pollTask() {
    const taskId = this.task?.task_id;

    if (taskId) {
      await dispatchPollTaskResult(this.$store, { task_id: taskId });
    }
  }

  get task() {
    return readTrainingTaskResult(this.$store);
  }
}

</script>
