<script setup>
    import { reactive } from 'vue'
    import Header from './components/header.vue'
    import Footer from './components/footer.vue'

    // const propsWeb = {
    //     user:10,
    //     url:"www.cba.com"
    // }

    const propsWeb = reactive({
        user:10,
        url:"www.cba.com"
    })


    const userAdd = ()=>{
        propsWeb.user++
        console.log(propsWeb.user)
    }
</script>

<template>
    <Header name="abc" url="abc.com" />

    <p>a text</p>

    <button @click="userAdd">添加用户</button>

    <!-- <Footer v-bind="propsWeb" /> -->
    <Footer :="propsWeb" />
</template>

<style scoped>

</style>
