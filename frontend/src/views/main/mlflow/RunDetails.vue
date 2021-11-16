<template>
  <div>
  </div>
</template>

<script lang="ts">
import { dispatchQueryRunDetails } from '@/store/mlflow/actions';
import { readCurrentRun } from '@/store/mlflow/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class RunDetails extends Vue {

  public async mounted() {
    await dispatchQueryRunDetails(this.$store, { runId: this.$route.params.id });
  }

  get run() {
    return readCurrentRun(this.$store);
  }
}
</script>
