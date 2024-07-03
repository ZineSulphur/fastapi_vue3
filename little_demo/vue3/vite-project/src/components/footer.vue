<template>
    <h3>footer</h3> Props {{ props.user }}
    <p></p>
    <button @click="add">emits添加用户</button>
</template>

<script setup>
    // props
    const props = defineProps({
        user:Number,    // 指定数据类型
        url:{   //详细配置
            type:String,            // 数据类型
            required:true,          // 是否为必须传属性，不传在console中有warning
            default:'default.com'   //默认值
        }
    })
    console.log(props);

    // emits
    const emits = defineEmits(["getWeb","userAdd"])
    emits("getWeb",{name:"abcd",url:"abcd.com"})

    const add=()=>{
        emits("userAdd",10)
    }
</script>

<style scoped>

</style>