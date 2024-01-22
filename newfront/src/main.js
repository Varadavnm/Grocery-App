import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
// import { BootstrapVue } from "bootstrap-vue";
import { createApp } from "vue";
import App from "./App.vue"; // adjust the path based on your file structure
import router from "./router"; // adjust the path based on your file structure
import store from "./store"; // adjust the path based on your file structure
createApp(App).use(router).use(store).mount("#app");
