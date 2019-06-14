<template>
  <v-flex xs12 md4 lg3 pl-3 pr-3 pb-4>
    <v-card hover>
      <v-img :src="recipe.picture" height="200px" />

      <v-card-title>
        <p class="font-weight-medium headline">{{ recipe.name }}</p>
      </v-card-title>

      <v-card-text>
        <strong>Ingredients: </strong> {{ recipe.ingredients }}
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <nuxt-link :to="`/recipes/${recipe.id}/`" class="pr-2">
          <v-btn small color="success" v-text="'View'" />
        </nuxt-link>

        <nuxt-link :to="`/recipes/${recipe.id}/edit/`" class="pr-2">
          <v-btn small color="info" v-text="'Edit'" />
        </nuxt-link>

        <v-btn
          small
          color="primary"
          @click="onDelete(recipe.id)"
          v-text="'Delete'"
        >
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-flex>
</template>

<script>
export default {
  props: ['recipe', 'onDelete']
}
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
