<script setup>
    import { reactive, ref,provide,onMounted,onUpdated } from 'vue'
    import Header from './components/header.vue'
    import Footer from './components/footer.vue'
    import son from './components/son.vue';
    import learnslot1 from './components/learnslot1.vue';
    import learnslot2 from './components/learnslot2.vue';

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

    // lifefunc
    onMounted(() => {
        console.log("onMounted")
    })
    onUpdated(() => {
        console.log("onUpdated")
    })
    console.log("user:",user.value)
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

    <hr>
    <h3>App.vue</h3>
    <!-- 匿名插槽 -->
    <learnslot1>
        <a href="abcd.com">abcd</a>
    </learnslot1>
    <!-- 具名插槽 -->
    <learnslot2>
        <!-- <template v-slot:url> -->
        <!-- <template #url="data">
            {{ data.title }}
            {{ data.user }} -->
        <template #url={title,user}>
            {{ title }}
            {{ user }}
            <a href="abcd.com">网址</a>
        </template>
    </learnslot2>

    <hr>
    {{ user }}
    <button @click="user++">添加用户</button>
</template>

<style scoped>

</style>
