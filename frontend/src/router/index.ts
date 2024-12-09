import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import DefaultLayout from "@/layouts/DefaultLayout.vue";
import AboutView from "@/views/AboutView.vue";

const routes = [
    {
        path: "/",
        name: "Public",
        component: DefaultLayout,
        redirect: "/",
        children: [
            {
                path: "/",
                name: "home",
                component: HomeView,
            },
        ],
    },
    {
        path: "/about",
        name: "AboutLayout",
        component: DefaultLayout,
        children: [
            {
                path: "",
                name: "about",
                component: AboutView,
            },
        ],
    },
];
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;
