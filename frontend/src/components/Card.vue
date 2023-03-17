<template>
  <div
    id="card"
    draggable="true"
    class="border border-dark mx-3"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
    @dragover.prevent="handleDragOver"
    @drop="handleDrop"
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
          <span class="fs-4" id="title_text">{{ card.title }}</span>
        </a>
        <span v-if="card.completed == true" class="fs-8" id="completed">
          <strong><em>Completed</em></strong>
        </span>

        <ul class="dropdown-menu">
          <li>
            <button class="dropdown-item" @click="editCard(card.id)">
              <span class="px-2"> Edit </span>
            </button>
          </li>
          <li>
            <button class="dropdown-item" @click="deleteCard_(card.id)">
              <span class="px-2"> Delete </span>
            </button>
          </li>
          <li v-if="card.completed !== true">
            <button class="dropdown-item" @click="completed(card.id)">
              <span class="px-2"> Mark as completed </span>
            </button>
          </li>
          <li>
            <button class="dropdown-item" @click="exportCard_(card.id)">
              <span class="px-2"> Export </span>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <!-- Content -->
    <div style="height: 50px" class="mt-3 mb-3">
      <h5>
        {{ card.content }}
      </h5>
    </div>
    <ul style="list-style: none">
      <li><em>Created At</em>: {{ card.created_at }}</li>
      <li>
        <em>Created At: {{ card.created_at }}</em>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "CardComponent",
  props: {
    card: {
      type: Object,
      required: true,
    },
    listIndex: {
      type: Number,
      required: true,
    },
  },
  components: {},
  methods: {
    editCard(id) {
      this.$router.push(`/card/edit/${id}`);
    },
    ...mapActions(["deleteCard", "exportCard", "markAsCompleted"]),
    deleteCard_(id) {
      this.deleteCard(id);
    },
    exportCard_(id) {
      this.exportCard(id);
    },
    completed(id) {
      this.markAsCompleted(id);
    },
    handleDragStart(event) {
      // Set the data that will be transferred with the drag and drop action
      event.dataTransfer.setData("cardId", this.card.id);
      event.dataTransfer.setData("fromListIndex", this.listIndex);
    },
    handleDragEnd(event) {
      // do something if necessary
      console.log(event);
    },
    handleDragOver(event) {
      // Allow the drop event to be fired
      event.preventDefault();
    },
    handleDrop(event) {
      // Get the data that was transferred with the drag and drop action
      const cardId = event.dataTransfer.getData("cardId");
      const fromListIndex = event.dataTransfer.getData("fromListIndex");
      const toListIndex = this.listIndex;

      // Emit the move-card event with the card id, from list index, and to list index
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
