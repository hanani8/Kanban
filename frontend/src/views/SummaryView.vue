<template>
  <div class="home">
    <div class="d-flex flex-row">
      <ListSummary
        v-for="summaryOfList in summaryOfLists"
        :key="summaryOfList.id"
        :summaryOfList="summaryOfList"
      />
    </div>
  </div>
</template>
<script>
import ListSummary from "../components/ListSummary.vue";
import { mapActions } from "vuex";

export default {
  name: "SummaryView",
  components: {
    ListSummary,
  },
  computed: {
    summaryOfLists: function () {
      return this.$store.getters.summaryOfLists;
    },
  },
  methods: {
    ...mapActions(["getLists"]),
  },
  created: function () {
    this.getLists();
  },
};
</script>
