<template>
  <div class="EditCard">
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
        <button type="submit">Submit</button>
      </form>
      <p v-if="showError" id="error">title or content is incorrect</p>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "EditCardFormView",
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
    ...mapActions(["getCard", "putCard"]),

    async submit() {
      const Card = new FormData();

      Card.append("title", this.form.title);

      Card.append("content", this.form.content);

      Card.append("deadline", this.form.date + " " + this.form.time);

      const CardJSON = JSON.stringify(Object.fromEntries(Card));

      try {
        await this.putCard({ id: this.$route.params.card_id, data: CardJSON });

        this.showError = false;

        this.$router.push("/");
      } catch (error) {
        this.showError = true;
      }
    },
  },
  created: async function () {
    await this.getCard(this.$route.params.card_id);
    this.form.title = this.$store.getters.card.title;
    this.form.content = this.$store.getters.card.content;
    this.form.date = this.$store.getters.card.deadline.split(" ")[0];
    this.form.time = this.$store.getters.card.deadline.split(" ")[1];
  },
};
</script>
