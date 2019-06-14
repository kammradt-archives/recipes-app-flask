<template>
  <v-app>
    <MainToolbar />
    <v-layout align-start justify-start row wrap>
      <template v-for="recipe in recipes">
        <RecipeCard :key="recipe.id" :on-delete="deleteRecipe" :recipe="recipe">
        </RecipeCard>
      </template>
    </v-layout>
  </v-app>
</template>

<script>
import RecipeCard from '~/components/RecipeCard'
import MainToolbar from '~/components/MainToolbar'

export default {
  components: {
    MainToolbar,
    RecipeCard
  },
  head() {
    return {
      title: 'Recipes list'
    }
  },
  data() {
    return {
      recipes: []
    }
  },
  async asyncData({ $axios, params, store }) {
    try {
      const headers = { Authorization: `JWT ${store.getters.token}` }
      const recipes = await $axios.$get(`/recipes/`, { headers })
      return { recipes }
    } catch (e) {
      return { recipes: [] }
    }
  },
  methods: {
    async deleteRecipe(RecipeId) {
      try {
        const headers = { Authorization: `JWT ${this.$store.getters.token}` }
        await this.$axios.$delete(`/recipes/${RecipeId}/`, { headers })

        const newRecipes = await this.$axios.$get('/recipes/', { headers })
        this.recipes = newRecipes
      } catch (e) {
        // eslint-disable-next-line no-console
        console.log(e)
      }
    }
  }
}
</script>
