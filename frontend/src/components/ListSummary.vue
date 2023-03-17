<template>
  <div
    id="list"
    style="overflow: scroll; height: 800px"
    class="position-relative d-flex flex-column"
  >
    <div id="title">
      <span class="fs-4" id="title_text">{{ summaryOfList.title }}</span>
    </div>
    <div id="completed">
      <span class="fs-4" id="completed"
        >Completed: {{ summaryOfList.completed }} / {{ summaryOfList.total }}
      </span>
    </div>
    <div id="deadline_passed">
      <span class="fs-4" id="deadline_passed"
        >Deadline Passed: {{ summaryOfList.deadline_passed }}
      </span>
    </div>

    <div id="chart">
      <v-frappe-chart
        type="bar"
        :labels="Array.from(summaryOfList.charts.keys())"
        :data="[{ values: Array.from(summaryOfList.charts.values()) }]"
        :colors="['red']"
      />
    </div>
  </div>
</template>

<script>
import { VFrappeChart } from "vue-frappe-chart";

export default {
  name: "ListSummaryComponent",
  props: ["summaryOfList"],
  components: {
    VFrappeChart,
  },
};
</script>

<style>
#list {
  width: 20%;
  margin-left: 3%;
  border-width: 2px;
  border-color: black;
  border-style: solid;
}
</style>
