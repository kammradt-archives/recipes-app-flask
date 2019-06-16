<template>
  <div>
    <v-toolbar dark class="primary">
      <v-toolbar-title>Receitinhas top</v-toolbar-title>
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
        <v-btn outline>Add</v-btn>
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
