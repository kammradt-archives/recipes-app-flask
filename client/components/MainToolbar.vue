<template>
  <div>
    <v-toolbar dark class="primary">
      <nuxt-link to="/recipes">
        <v-btn outline block>
          Receitinhas top
          <v-icon right>home</v-icon>
        </v-btn>
      </nuxt-link>
      <v-spacer />
      <v-btn flat small>
        <v-switch
          v-model="showPublicRecipes"
          color="white"
          class="text-none"
          :label="switchText"
          @click="changeRecipes"
        />
      </v-btn>
      <nuxt-link to="/recipes/add">
        <v-btn outline>
          Add
          <v-icon right>add</v-icon>
        </v-btn>
      </nuxt-link>
    </v-toolbar>
    <br />
  </div>
</template>

<script>
export default {
  data() {
    return {
      showPublicRecipes: false
    }
  },
  computed: {
    switchText() {
      return this.showPublicRecipes
        ? 'Show only my recipes'
        : 'Show all public recipes'
    }
  },
  methods: {
    changeRecipes() {
      this.$emit('changeRecipes', this.showPublicRecipes)
    }
  }
}
</script>
