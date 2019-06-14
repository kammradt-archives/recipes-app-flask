<template>
  <v-app>
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.type"
      :timeout="4000"
      class="mt-3"
      top
    >
      {{ snackbar.text }}
    </v-snackbar>
    <header>
      <div class="text-box ma-1">
        <h1 class="display-3">Receitinhas top 😋</h1>
        <p class="mt-3 font-weight-light headline">
          Recipes for the meals we love ❤️
        </p>

        <v-form class="pt-3">
          <v-text-field
            v-model="loginData.username"
            prepend-icon="person"
            label="Username"
            type="text"
            dark
          />
          <v-text-field
            v-model="loginData.password"
            prepend-icon="lock"
            label="Password"
            type="password"
            dark
          />
          <v-text-field
            v-show="showRegister"
            v-model="confirmPassword"
            prepend-icon="lock"
            label="Confirm Password"
            type="password"
            dark
          />
        </v-form>

        <v-layout row wrap>
          <v-flex xs12>
            <v-btn
              v-show="showRegister"
              outline
              block
              color="green"
              @click="onRegister"
            >
              Create account
            </v-btn>
          </v-flex>

          <v-btn outline block color="white" class="mr-1" @click="onLogin">
            login
            <v-icon right>person</v-icon>
          </v-btn>

          <v-btn
            outline
            block
            color="white"
            class="ml-1"
            @click="showRegister = !showRegister"
          >
            register
            <v-icon right>person_add</v-icon>
          </v-btn>
        </v-layout>
      </div>
    </header>
  </v-app>
</template>
<script>
export default {
  head() {
    return {
      title: 'Home page'
    }
  },
  data() {
    return {
      loginData: {
        username: '',
        password: ''
      },
      snackbar: {
        text: '',
        type: '',
        show: false
      },
      confirmPassword: '',
      showRegister: false
    }
  },
  computed: {
    arePasswordsEqual() {
      return this.loginData.password === this.confirmPassword
    }
  },
  methods: {
    async onLogin() {
      try {
        const authHeader = {
          auth: {
            username: this.loginData.username,
            password: this.loginData.password
          }
        }
        // eslint-disable-next-line no-unused-vars
        const response = await this.$axios.$get('/login', authHeader)
        this.$store.dispatch('updateToken', response.token)
        this.$router.push('/recipes')
      } catch (e) {
        this.showSnackbar('Verify your credencials!', 'warning')
      }
    },
    async onRegister() {
      if (this.loginData.username && this.loginData.password) {
        if (this.arePasswordsEqual) {
          const createUserPost = {
            username: this.loginData.username,
            password: this.loginData.password
          }
          try {
            const response = await this.$axios.$post('/user', createUserPost)
            this.showSnackbar(response.message, 'success')
            this.loginData = {
              username: this.loginData.username,
              password: this.loginData.password
            }
            this.showRegister = false
          } catch (e) {
            this.showSnackbar('Failed to create account!', 'error')
          }
        } else {
          this.showSnackbar('Password do not match!', 'info')
        }
      } else {
        this.showSnackbar('Fields cannot be empty!', 'info')
      }
    },
    showSnackbar(text, type) {
      this.snackbar = { text, type, show: true }
    }
  }
}
</script>
<style>
header {
  min-height: 100vh;
  background-image: linear-gradient(
      to right,
      rgba(0, 0, 0, 0.9),
      rgba(0, 0, 0, 0.55)
    ),
    url('/images/banner.jpg');
  background-position: center;
  background-size: cover;
  position: relative;
}
.text-box {
  position: absolute;
  top: 20%;
  transform: translateY(-50%);
  left: 50%;
  transform: translateX(-50%);
  color: #fff;
}
a {
  text-decoration: none;
}
</style>
