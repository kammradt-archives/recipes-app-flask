import vuex from 'vuex'

// eslint-disable-next-line no-unused-vars
const createStore = () => {
  return new vuex.Store({
    state: {
      token: ''
    },
    mutations: {
      updateToken(state, payload) {
        state.token = payload
      }
    },
    actions: {
      updateToken(context, payload) {
        context.commit('updateToken', payload)
      }
    },
    getters: {
      token(state) {
        return state.token
      }
    }
  })
}

export default createStore
