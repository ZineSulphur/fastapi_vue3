<script setup>
    import { reactive, ref } from 'vue'
    import Header from './components/header.vue'
    import Footer from './components/footer.vue'

    // props
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

    // emits
    const user = ref(0)

    const web = reactive({
        name:'abc',
        url:'abc.com'
    })

    const emitsGetWeb = (data)=>{
        console.log(data)
        web.url = data.url
    }

    const emitsUserAdd=(data)=>{
        console.log(data)
        user.value += data
    }
</script>

<template>
    <Header name="abc" url="abc.com" />

    <p>a text</p>

    <button @click="userAdd">props添加用户</button>

    <!-- <Footer v-bind="propsWeb" /> -->
    <Footer :="propsWeb" @getWeb="emitsGetWeb" @userAdd="emitsUserAdd" />
    <p>{{ web.url }}</p>
    <p>Emits {{ user }}</p>
</template>

<style scoped>

</style>
