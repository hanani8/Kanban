<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <span v-if="isLoggedIn === true">
      <button type="button" class="btn btn-light" @click="logout">Logout</button> |
    </span>
    <span v-else>
      <router-link to="/login">Login</router-link>
    </span>
    <span v-if="isLoggedIn === true">
      <router-link to="/summary">Summary</router-link>
    </span>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "NavBar",
  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    ...mapActions(["Logout"]),
    async logout() {
      await this.Logout();

      this.$router.push("/login");
    },
  },
};
</script>

<style>
#nav {
  padding: 30px;
}
#nav a {
  font-weight: bold;
  color: #2c3e50;
}
a:hover {
  cursor: pointer;
}
#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
