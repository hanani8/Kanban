<template>
  <div class="home">
    <div class="d-flex flex-row">
      <List
        v-for="(list, index) in lists"
        :key="list.id"
        :list="list"
        :index="index"
        @move-card="move"
      />

      <!-- Add List -->
      <div class="d-flex mt-3 mb-3" @click="addList()">
        <img
          class="align-self-center h-25 mx-auto border border-dark rounded-lg"
          src="../assets/add_black_24dp.svg"
        />
      </div>
    </div>
  </div>
</template>
<script>
import List from "../components/List.vue";
import { mapActions } from "vuex";

export default {
  name: "HomeView",
  components: {
    List,
  },
  computed: {
    lists: function () {
      return this.$store.getters.lists;
    },
  },
  methods: {
    ...mapActions(["getLists", "moveCard"]),
    addList() {
      this.$router.push("/list");
    },
    move(cardId, fromListIndex, toListIndex) {
      // Find the list that the card is being moved from
      const fromList = this.lists[fromListIndex];

      // Find the list that the card is being moved to
      const toList = this.lists[toListIndex];

      // Find the card that is being moved
      const card = fromList.cards.find((card) => card.id == cardId);

      console.log(fromList, toList, card);

      // // Remove the card from the fromList
      fromList.cards = fromList.cards.filter((c) => c.id != cardId);

      // // Add the card to the toList
      toList.cards.push(card);

      const data = {
        list_id: toList.id,
        card_id: cardId,
      };

      this.moveCard(data).then((d) => console.log(d));
    },
  },
  created: function () {
    this.getLists();
  },
};
</script>
