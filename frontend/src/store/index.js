import { createStore } from 'vuex'

export default createStore({
  state: {
    userInfo: null,
    token: null
  },
  mutations: {
    setUserInfo(state, userInfo) {
      state.userInfo = userInfo
    },
    setToken(state, token) {
      state.token = token
    },
    clearUserInfo(state) {
      state.userInfo = null
      state.token = null
    }
  },
  actions: {
    login({ commit }, { userInfo, token }) {
      commit('setUserInfo', userInfo)
      commit('setToken', token)
    },
    logout({ commit }) {
      commit('clearUserInfo')
    }
  }
}) 