<template>
  <div class="login">
    <div>
      <form @submit.prevent="submit">
        <div>
          <label for="username">Username:</label>
          <input type="text" name="username" v-model="form.username" />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" name="password" v-model="form.password" />
        </div>
        <button type="submit">Submit</button>
      </form>
      <p v-if="showError" id="error">Username or Password is incorrect</p>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "LoginView",
  components: {},
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      showError: false,
    };
  },
  methods: {
    ...mapActions(["Login"]),
    async submit() {
      const User = new FormData();
      User.append("username", this.form.username);
      User.append("password", this.form.password);
      try {
        await this.Login(User);
        this.showError = false;
        this.$router.push("/");
      } catch (error) {
        this.showError = true;
      }
    },
  },
};
</script>
