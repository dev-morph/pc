<template>
    <div class="picture">
        <img :src="getImageUrl(path)" alt="picture" />
    </div>
</template>

<script setup lang="ts">
defineProps({
    path: {
        type: String,
        required: true,
    },
});

const getImageUrl = (path: string) => {
    console.log(new URL(path, import.meta.url).href);
    return new URL(`/src/assets/images/${path}.png`, import.meta.url).href;
};
</script>

<style scoped lang="scss">
.picture {
    width: 100%;
    height: 100%;
}
</style>
