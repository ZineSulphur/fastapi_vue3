<template>
    <h3>footer</h3> {{ props.user }}
</template>

<script setup>
    const props = defineProps({
        user:Number,    // 指定数据类型
        url:{   //详细配置
            type:String,            // 数据类型
            required:true,          // 是否为必须传属性，不传在console中有warning
            default:'default.com'   //默认值
        }
    })
    console.log(props);
</script>

<style scoped>

</style>