<template>
    <div class="layout-container">
        <AppHeader />
        <RouterView />
        <AppFooter />
    </div>
</template>

<script setup lang="ts">
import AppHeader from "@/components/layouts/AppHeader.vue";
import AppFooter from "@/components/layouts/AppFooter.vue";
import { RouterView } from "vue-router";
</script>

<style scoped>
.layout-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

:deep(.footer) {
    margin-top: auto;
}
</style>
