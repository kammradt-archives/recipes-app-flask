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
          class="elevation-10"
        />
      </v-flex>

      <v-flex xs12 md6 pa-1 pt-5>
        <v-form ref="addForm" @submit.prevent="submitRecipe">
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

          <v-text-field
            v-model="recipe.picture"
            type="text"
            label="Picture url"
            required
          />

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

          <v-switch
            v-model="recipe.is_public"
            label="Public recipe?"
            color="primary"
          />

          <v-textarea
            v-model="recipe.preparation_guide"
            label="Preparation guide"
            hint="Describe how to prepare your recipe here!"
            :counter="600"
            :rules="rules.recipePreparationGuideRule"
            required
          />

          <v-btn color="primary" type="submit">Save</v-btn>
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
      title: 'Add Recipe'
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
        preparation_guide: '',
        is_public: false
      },
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
  methods: {
    async submitRecipe() {
      if (this.$refs.addForm.validate()) {
        try {
          const config = {
            headers: {
              'x-access-token': this.$store.getters.token
            }
          }
          // eslint-disable-next-line no-unused-vars
          const response = await this.$axios.$post(
            '/recipe',
            this.recipe,
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
}
</script>
