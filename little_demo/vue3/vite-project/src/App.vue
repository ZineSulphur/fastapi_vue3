<script setup>
    import { reactive, ref,provide } from 'vue'
    import Header from './components/header.vue'
    import Footer from './components/footer.vue'
    import son from './components/son.vue';

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

    // provider
    provide("provideWeb",web)
    provide("provideUser",user)
    const puserAdd=()=>{
        user.value++
    }
    provide("provideFuncPUserAdd",puserAdd)
</script>

<template>
    <Header name="abc" url="abc.com" />
    <p>a text</p>
    <button @click="userAdd">props添加用户</button>

    <!-- <Footer v-bind="propsWeb" /> -->
    <Footer :="propsWeb" @getWeb="emitsGetWeb" @userAdd="emitsUserAdd" />
    <p>{{ web.url }}</p>
    <p>Emits {{ user }}</p>

    <hr>
    <h3>App.vue Top</h3>
    user:{{ user }}
    <!-- 子组件 -->
    <son/>
</template>

<style scoped>

</style>
