<template>
  <v-app>
    <MainToolbar @changeRecipes="changeRecipes" />
    <v-layout align-start justify-start row wrap>
      <template v-for="recipe in recipes">
        <RecipeCard
          :key="recipe.id"
          :is-public="showingPublic"
          :on-delete="deleteRecipe"
          :recipe="recipe"
        >
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
      recipes: [],
      showingPublic: null
    }
  },
  async asyncData({ $axios, params, store }) {
    try {
      const config = {
        headers: {
          'x-access-token': store.getters.token
        }
      }
      const response = await $axios.$get(`/recipe`, config)
      const recipes = response.recipes
      return { recipes }
    } catch (e) {
      return { recipes: [] }
    }
  },
  methods: {
    async deleteRecipe(RecipeId) {
      try {
        const config = {
          headers: { 'x-access-token': this.$store.getters.token }
        }
        await this.$axios.$delete(`/recipe/${RecipeId}`, config)
        const newRecipes = await this.$axios.$get('/recipe', config)
        this.recipes = newRecipes.recipes
      } catch (e) {
        // eslint-disable-next-line no-console
        console.log(e)
      }
    },
    async changeRecipes(showPublic) {
      if (showPublic) {
        this.showingPublic = true
        const publicRecipes = await this.$axios.$get('/recipes')
        this.recipes = publicRecipes.recipes
      } else {
        this.showingPublic = false
        const config = {
          headers: { 'x-access-token': this.$store.getters.token }
        }
        const newRecipes = await this.$axios.$get('/recipe', config)
        this.recipes = newRecipes.recipes
      }
    }
  }
}
</script>
