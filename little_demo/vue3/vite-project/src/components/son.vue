<template>
    <h3>son.vue middle</h3>
    <!-- 子组件 -->
     <grandson/>
</template>

<script setup>
    import { inject } from 'vue'
    import grandson from './grandson.vue'

    const user = inject("provideUser")
    console.log("provideUser",user)
</script>

<style lang="scss" scoped>

</style>