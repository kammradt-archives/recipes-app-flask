<template>
  <v-app>
    <MainToolbar />
    <v-flex pa-1 text-xs-center display-3 v-text="recipe.name" />
    <v-layout justify-space-around row wrap fill-height>
      <v-flex text-xs-center xs12 md6 pa-1 pt-5>
        <img v-if="!preview" style="width: 400px;" :src="recipe.picture" />
        <img else style="width: 400px;" :src="preview" />
      </v-flex>
      <v-flex xs12 md6 pa-1 pt-5>
        <v-form @submit.prevent="submitRecipe">
          <v-text-field
            v-model="recipe.name"
            :counter="120"
            type="text"
            label="Recipe name"
            :rules="rules.recipeNameRule"
            required
          />

          <v-text-field
            v-model="recipe.ingredients"
            :counter="400"
            type="text"
            label="Ingredients"
            :rules="rules.recipeIngredientsRule"
            required
          />

          <span pb-3 body-1 v-text="'Food picture'" />
          <input label="Food picture" type="file" @change="onFileChange" />

          <v-select
            v-model="recipe.difficulty"
            :items="difficultyOptions"
            label="Difficulty"
            :rules="rules.recipeDifficultyRule"
            required
          />

          <label for>
            Preperation time
            <small>
              (
              <input v-model="recipe.preparation_time" type="number" />
              minutes)</small
            >
          </label>
          <v-slider v-model="recipe.preparation_time" max="600" />

          <v-textarea
            v-model="recipe.preparation_guide"
            label="Preparation guide"
            hint="Describe how to prepare your recipe here!"
            :counter="600"
            :rules="rules.recipePreparationGuideRule"
            required
          />

          <v-btn color="primary" type="submit">Update</v-btn>
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
      title: 'Edit Recipe'
    }
  },
  data() {
    return {
      recipe: {
        name: '',
        picture: '',
        ingredients: '',
        difficulty: '',
        preparation_time: 5,
        preparation_guide: ''
      },
      preview: '',
      rules: {
        recipeNameRule: [
          v => v.length >= 5 || 'Minimum length is 5 characters',
          v => v.length <= 120 || 'Maximum length is 120 characters'
        ],
        recipeIngredientsRule: [
          v => v.length >= 10 || 'Minimum length is 10 characters',
          v => v.length <= 400 || 'Maximum length is 400 characters'
        ],
        recipeDifficultyRule: [
          v => v !== '' || 'Select how difficult your recipe is'
        ],
        recipePreparationGuideRule: [
          v => v.length >= 10 || 'Minimum length is 10 characters',
          v => v.length <= 600 || 'Maximum length is 600 characters'
        ]
      },
      difficultyOptions: ['Easy', 'Medium', 'Hard']
    }
  },
  async asyncData({ $axios, params, store }) {
    const headers = { Authorization: `JWT ${store.getters.token}` }
    try {
      const recipe = await $axios.$get(`/recipes/${params.id}`, { headers })
      return { recipe }
    } catch (e) {
      return { recipe: [] }
    }
  },
  methods: {
    onFileChange(e) {
      const files = e.target.files || e.dataTransfer.files
      if (!files.length) {
        return
      }
      this.recipe.picture = files[0]
      this.createImage(files[0])
    },
    createImage(file) {
      const reader = new FileReader()
      const vm = this
      reader.onload = e => {
        vm.preview = e.target.result
      }
      reader.readAsDataURL(file)
    },
    async submitRecipe() {
      const editedRecipe = this.recipe
      if (editedRecipe.picture.indexOf('http://') !== -1) {
        delete editedRecipe.picture
      }
      const config = {
        headers: {
          'content-type': 'multipart/form-data',
          Authorization: `JWT ${this.$store.getters.token}`
        }
      }
      const formData = new FormData()
      for (const data in editedRecipe) {
        formData.append(data, editedRecipe[data])
      }
      try {
        // eslint-disable-next-line no-unused-vars
        const response = await this.$axios.$patch(
          `/recipes/${editedRecipe.id}/`,
          formData,
          config
        )
        this.$router.push('/recipes/')
      } catch (e) {
        // eslint-disable-next-line no-console
        console.log(e)
      }
    }
  }
}
</script>
