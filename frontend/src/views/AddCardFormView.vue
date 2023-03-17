<template>
  <div class="AddCard">
    <div>
      <form @submit.prevent="submit">
        <div>
          <label for="title">Title:</label>
          <input type="text" name="title" v-model="form.title" />
        </div>
        <div>
          <label for="content">Content:</label>
          <input type="text" name="content" v-model="form.content" />
        </div>
        <div>
          <label for="date">Deadline's Date:</label>
          <input type="date" name="date" v-model="form.date" />
        </div>
        <div>
          <label for="time">Deadline's Time:</label>
          <input type="time" name="time" v-model="form.time" />
        </div>
        <div>
          <label for="completed">Completed: </label>
          <input
            name="completed"
            id="completed"
            type="checkbox"
            v-model="form.completed"
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      <p v-if="showError" id="error">title or content is incorrect</p>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "AddCardFormView",
  components: {},
  data() {
    return {
      form: {
        title: "",
        content: "",
      },
      showError: false,
    };
  },
  methods: {
    ...mapActions(["createCard"]),

    async submit() {
      const Card = new FormData();

      Card.append("title", this.form.title);

      Card.append("content", this.form.content);

      Card.append("deadline", this.form.date + " " + this.form.time);

      Card.append("completed", this.form.completed);

      Card.append("list_id", this.$route.params.list_id);

      const CardJSON = JSON.stringify(Object.fromEntries(Card));

      try {
        await this.createCard(CardJSON);

        this.showError = false;

        this.$router.push("/");
      } catch (error) {
        this.showError = true;
      }
    },
  },
};
</script>
