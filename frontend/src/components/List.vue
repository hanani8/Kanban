<template>
  <div
    id="list"
    style="overflow: scroll; height: 800px"
    class="position-relative d-flex flex-column"
  >
    <!-- Title -->
    <div id="title">
      <div class="dropdown">
        <a
          class="dropdown-toggle"
          href="#"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <span class="fs-4" id="title_text">{{ list.title }}</span>
        </a>

        <p>{{ list.description }}</p>

        <ul class="dropdown-menu">
          <li>
            <button class="dropdown-item" @click="editList(list.id)">
              <span class="px-2"> Edit </span>
            </button>
          </li>
          <li>
            <button class="dropdown-item" @click="deleteList_(list.id)">
              <span class="px-2"> Delete </span>
            </button>
          </li>
        </ul>
      </div>
    </div>
    <div class="d-flex flex-row justify-content-around"></div>

    <div v-for="card in list.cards" :key="card.id">
      <Card :card="card" :list-index="index" @move-card="move" />
    </div>

    <!-- Add -->
    <div class="">
      <div style="height: 50px" class="mt-3 mb-3" @click="addCard(list.id)">
        <img
          style="display: block"
          class="h-100 mx-auto border border-dark rounded-lg"
          src="../assets/add_black_24dp.svg"
        />
      </div>
      <!-- Export -->
      <button
        class="border border-dark bg-white mb-2"
        id="export"
        @click="exportList_(list.id)"
      >
        <span class="px-2">Export</span>
      </button>
    </div>
  </div>
</template>

<script>
import Card from "../components/Card.vue";
import { mapActions } from "vuex";

export default {
  name: "ListComponent",
  props: {
    list: {
      type: Object,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  components: {
    Card,
  },
  methods: {
    addCard(id) {
      this.$router.push(`card/add/${id}`);
    },
    editList(id) {
      this.$router.push(`list/edit/${id}`);
    },
    ...mapActions(["getList", "deleteList", "exportList"]),
    deleteList_(id) {
      const list = this.$store.getters.lists.find((ele) => {
        return ele.id == id;
      });
      if (list.cards.length > 0) {
        this.$alert("List is unempty! Either move or delete the cards.");
        this.deleteList(id);
      } else {
        this.deleteList(id);
      }
    },
    exportList_(id) {
      this.exportList(id);
    },
    move(cardId, fromListIndex, toListIndex) {
      this.$emit("move-card", cardId, fromListIndex, toListIndex);
    },
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
