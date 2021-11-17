<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3" v-if="!model">
      <div class="primary--text text--lighten-3">
        Model not found or not been fetched. --Refresh <!-- wip refresh btn -->
      </div>
    </v-card>

    <v-card class="ma-3 pa-3" v-if="model">
      <v-card-title primary-title>
        <div class="headline primary--text">Model and version info</div>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Name</div>
          <div class="primary--text text--darken-2">{{model.name}}</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Created at</div>
          <div class="primary--text text--darken-2">{{model.creation_timestamp}}</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Updated at</div>
          <div class="primary--text text--darken-2">{{model.last_updated_timestamp}}</div>
        </div>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Version info</div>
          <div class="primary--text text--darken-2">{{JSON.stringify(model.latest_versions)}}</div>
        </div>
      </v-card-text>
    </v-card>
    <v-card class="ma-3 pa-3" v-if="model">
      <v-card-title primary-title>
        <div class="headline primary--text">Try model</div>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <!-- form data -->
        <v-form
          v-model="valid"
          ref="form"
          lazy-validation
        >
          <v-text-field
            label="age"
            name="age"
            v-model="inputData.age"
            type="number"
            required
          >
          </v-text-field>
          <v-text-field
            label="sex"
            name="sex"
            v-model="inputData.sex"
            type="number"
            required
          >
          </v-text-field>
          <v-text-field
            label="bmi"
            name="bmi"
            v-model="inputData.bmi"
            type="number"
            required
          >
          </v-text-field>
          <v-text-field
            label="bp"
            name="bp"
            v-model="inputData.bp"
            type="number"
            required
          >
          </v-text-field>
          <v-text-field
            label="s1"
            name="s1"
            v-model="inputData.s1"
            type="number"
            required
          >
          </v-text-field>
          <v-text-field
            label="s2"
            name="s2"
            v-model="inputData.s2"
            type="number"
            required
          >
          </v-text-field>
          <v-text-field
            label="s3"
            name="s3"
            v-model="inputData.s3"
            type="number"
            required
          >
          </v-text-field>
          <v-text-field
            label="s4"
            name="s4"
            v-model="inputData.s4"
            type="number"
            required
          >
          </v-text-field>
          <v-text-field
            label="s5"
            name="s5"
            v-model="inputData.s5"
            type="number"
            required
          >
          </v-text-field>
          <v-text-field
            label="s6"
            name="s6"
            v-model="inputData.s6"
            type="number"
            required
          >
          </v-text-field>
        </v-form>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn
          @click="requestPrediction"
          :disabled="!valid"
        >Submit</v-btn>
      </v-card-actions>
    </v-card>

    <v-card class="ma-3 pa-3" v-if="predictionResult">
      <v-card-text>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Result</div>
          <div class="primary--text text--darken-2">{{ predictionResult }}</div>
        </div>
      </v-card-text>
    </v-card>

    <v-card class="ma-3 pa-3" v-if="predictionError">
      <v-card-text>
        <div class="my-4">
          <div class="subheading secondary--text text--lighten-3">Error</div>
          <div class="primary--text text--darken-2">{{ predictionError }}</div>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { api } from '@/api';
import { IInputData } from '@/interfaces';
import { readToken } from '@/store/main/getters';
import { dispatchGetAllRegisteredModels } from '@/store/mlflow/actions';
import { readRegisteredModels } from '@/store/mlflow/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class ModelDetails extends Vue {
  public valid: boolean = true;
  public inputData: GObject = {};
  public predictionResult: number | null = null;
  public predictionError: string | null = null;

  public async requestPrediction() {
    try {
      const resp = await api.predictSingleDatapointWithModel(
        this.model.name,
        this.inputData as IInputData,
        this.authToken,
      );
      const { data } = resp;
      this.predictionResult = data[0];
    } catch (e) {
      this.predictionError = JSON.stringify(e);
    }
  }

  public async mounted() {
    if (this.models.length === 0) {
      await dispatchGetAllRegisteredModels(this.$store);
    }
  }

  get authToken() {
    return readToken(this.$store);
  }

  get models() {
    return readRegisteredModels(this.$store);
  }

  get model() {
    const modelName = this.$route.params.name;
    const models = this.models;

    return models.filter((model) => model.name === modelName)[0];
  }
}
</script>
