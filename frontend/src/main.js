import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import ja from 'element-plus/dist/locale/ja.mjs'
import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)

app.use(ElementPlus, {
  locale: ja,
})
app.use(router)
app.use(store)

app.mount('#app') 