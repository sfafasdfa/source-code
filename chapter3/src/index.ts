window.global ||= window;
import { createApp } from 'vue'
import App from './components/App.vue'
import router from './router/index'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import VueAMap, {initAMapApiLoader} from '@vuemap/vue-amap';
// import VueAMapLoca from '@vuemap/vue-amap-loca';
// import VueAMapExtra from '@vuemap/vue-amap-extra';
import '@vuemap/vue-amap/dist/style.css'
initAMapApiLoader({
  key: 'YOUR_KEY',
  securityJsCode: 'securityJsCode', // 新版key需要配合安全密钥使用
  //Loca:{
  //  version: '2.0.0'
  //} // 如果需要使用loca组件库，需要加载Loca
})

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.use(VueAMap)
app.mount('#app')
