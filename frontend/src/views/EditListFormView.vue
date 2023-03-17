<template>
  <div class="addEditList">
    <div>
      <form @submit.prevent="submit">
        <div>
          <label for="title">Title:</label>
          <input type="text" name="title" v-model="form.title" />
        </div>
        <div>
          <label for="description">Description:</label>
          <input type="text" name="description" v-model="form.description" />
        </div>
        <button type="submit">Submit</button>
      </form>
      <p v-if="showError" id="error">title or description is incorrect</p>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "EditListFormView",
  components: {},
  data() {
    return {
      form: {
        title: "",
        description: "",
      },
      showError: false,
    };
  },
  methods: {
    ...mapActions(["getList", "putList"]),

    async submit() {
      const List = new FormData();

      List.append("title", this.form.title);
      List.append("description", this.form.description);

      const ListJSON = JSON.stringify(Object.fromEntries(List));

      try {
        await this.putList({ id: this.$route.params.list_id, data: ListJSON });

        this.showError = false;

        this.$router.push("/");
      } catch (error) {
        this.showError = true;
      }
    },
  },
  created: async function () {
    await this.getList(this.$route.params.list_id);
    this.form.title = this.$store.getters.list.title;
    this.form.description = this.$store.getters.list.description;
  },
};
</script>
