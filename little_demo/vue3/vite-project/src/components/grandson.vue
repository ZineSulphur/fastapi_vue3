<template>
    <h3>grandson.vue bottom</h3>

    <button @click="funcPUserAdd">添加用户</button>
</template>

<script setup>
    import { inject } from 'vue';

    const web = inject("provideWeb")
    console.log("provideWeb",web)

    const funcPUserAdd = inject("provideFuncPUserAdd")
</script>

<style lang="scss" scoped>

</style>