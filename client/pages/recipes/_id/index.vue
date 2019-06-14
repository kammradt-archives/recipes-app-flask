<template>
  <v-app>
    <MainToolbar />
    <v-flex pa-1 text-xs-center display-3 v-text="recipe.name" />
    <v-layout justify-space-around row wrap fill-height>
      <v-flex text-xs-center xs12 md6 pa-1 pt-5>
        <img
          v-if="recipe.picture"
          style="width: 400px;"
          :src="recipe.picture"
        />
      </v-flex>
      <v-flex xs12 md6 pa-1 pt-5>
        <v-form @submit.prevent="submitRecipe">
          <v-text-field v-model="recipe.name" readonly label="Recipe name" />

          <v-text-field
            v-model="recipe.ingredients"
            readonly
            label="Ingredients"
          />

          <v-text-field
            v-model="recipe.difficulty"
            readonly
            label="Difficulty"
          />

          <label
            v-text="`Preparation time: ${recipe.preparation_time} minutes`"
          />
          <v-slider v-model="recipe.preparation_time" max="600" readonly />

          <v-textarea
            v-model="recipe.preparation_guide"
            label="Preparation guide"
            readonly
            rows="12"
            no-resize
          />
        </v-form>
      </v-flex>
    </v-layout>
  </v-app>
</template>

<script>
import MainToolbar from '~/components/MainToolbar'

export default {
  components: {
    MainToolbar
  },
  head() {
    return {
      title: 'View Recipe'
    }
  },
  data() {
    return {
      recipe: {
        name: '',
        picture: '',
        ingredients: '',
        difficulty: '',
        preparation_time: '',
        preparation_guide: ''
      }
    }
  },
  async asyncData({ $axios, params, store }) {
    try {
      const headers = { Authorization: `JWT ${store.getters.token}` }
      const recipe = await $axios.$get(`/recipes/${params.id}`, { headers })
      return { recipe }
    } catch (e) {
      return { recipe: [] }
    }
  }
}
</script>
