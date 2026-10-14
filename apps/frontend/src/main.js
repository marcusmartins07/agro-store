// Estilos globais primeiro: Bootstrap, depois os tokens do projeto; assim os estilos dos componentes vêm por último
import 'bootstrap/dist/css/bootstrap.min.css'
import './assets/main.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.mount('#app')
