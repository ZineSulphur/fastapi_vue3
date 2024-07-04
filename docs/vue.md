# Vue 学习笔记

Vue (发音为 /vjuː/，类似 view) 是一款用于构建用户界面的 JavaScript 框架。它基于标准 HTML、CSS 和 JavaScript 构建，并提供了一套声明式的、组件化的编程模型，帮助你高效地开发用户界面。无论是简单还是复杂的界面，Vue 都可以胜任。

## 基础内容

### 创建一个应用

这里将创建一个hello world式的vue应用

这里使用[全局构建版本](https://cn.vuejs.org/guide/quick-start.html#using-the-global-build)，该版本的所有顶层 API 都以属性的形式暴露在了全局的 Vue 对象上。

我们先在head中的script中获得vue，比如使用vue的cdn`<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>`或者将其下载下来放到项目中使用。

然后我们在body中创建一个div指定`id="app"`，然后再script中使用`Vue.createApp()`来创建app，并且利用`.mount("#app")`挂载到之前指定的元素上。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <!-- 借助 script 标签直接通过 CDN 来使用 Vue -->
    <script src="vue.global.js"></script>
</head>
<body>
    <div id="app">
        <!-- 渲染msg -->
        {{ msg }}
        
        <h2>{{ web.title }}</h2>
        <h2>{{ web.url }}</h2>
    </div>

    <script>
        //将 Vue 对象中的 createApp、reactive 属性赋值给 createApp、reactive 变量
        const {createApp,reactive} = Vue

        // 创建一个 Vue 应用程序
        createApp({
            // Composition API(组合式 API) 的 setup选项 用于设置响应式数据和方法等
            setup() {
                const web = reactive({
                    title:"vue learning",
                    url:"url"
                })

                return {
                    msg:"success",
                    web
                }
            }
        }).mount("#app") //将 Vue 应用程序挂载(mount) 到 app 元素上
    </script>
</body>
</html>
```

[quickstart代码](../little_demo/vue3/part1/demo.html)

### 模块化开发

要进行模块化开发的时候，指定script的`type="module"`,在模块中引入文件`https://unpkg.com/vue@3/dist/vue.esm-browser.js`

使用模块化开发时，我们直接打开html文件，可以发现和传统模式不同的是变量都没有赋值。

此时我们需要使用服务器打开，比如使用LiveServer打开文件，就可以正常显示了。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div id="app">
        <!-- 渲染msg -->
        {{ msg }}
    </div>

    <script type="module">
        import {createApp,reactive} from "https://unpkg.com/vue@3/dist/vue.esm-browser.js"

        createApp({
            setup() {
                return {
                    msg:"success"
                }
            }
        }).mount("#app")
    </script>
</body>
</html>
```

[模块化开发quickstart代码](../little_demo/vue3/part1/demo_module.html)

### ref 和 reactive

ref 主要用于封装基本数据类型和单一引用类型值，如数字、字符串等。

reactive 则更适合定义复杂的数据类型，如对象和数组。

ref修改值需要调用value`a.value=1`进行修改，而reactive不需要`a=1`

首先导入ref和reactive，然后构造ref和reacitve作为变量即可使用。

```html
<body>
    <div id="app">
        msg: {{ msg }}
        
        <h3>web.title: {{ web.title }}</h3>
        <h3>web.url: {{ web.url }}</h3>
        <h3>web.number: {{ number }}</h3>
    </div>

    <script type="module">
        import {createApp,reactive,ref} from './vue.esm-browser.js'

        createApp({
            setup() {
                const number = ref(10) //ref用于存储单个基本类型的数据, 如:数字、字符串等
                number.value = 20 //使用ref创建的响应式对象, 需要通过.value属性来访问和修改其值

                const web = reactive({ //用于存储复杂数据类型, 如:对象或数组等
                    title:"vue learning",
                    url:"url"
                })
                web.url = "url" //使用reactive创建的响应式对象, 可以直接通过属性名来访问和修改值

                return {
                    msg:"success",
                    number,
                    web
                }
            }
        }).mount("#app")
    </script>
</body>
```

[ref和reactive代码](../little_demo/vue3/part1/ref_reactive.html)

### 绑定事件v-on

v-on指令用于注册事件，作用是添加监听与提供事件触发后对应的处理函数。

v-on有两种语法，在提供处理函数的时候既可以直接使用内联语句，也可以提供函数的名字。

```html
<body>
    <div id="app">
        <h2>{{ web.url }}</h2>

        <!-- v-on:click 表示在 button 元素上监听 click 事件 -->
        <button v-on:click="edit">edit</button>
        <!-- @click 简写形式 -->
        <button @click="edit">edit@</button>
        <hr>

        <h2>{{ web.user }}</h2>
        <!-- 
            enter space tab 按键修饰符
            keyup是在用户松开按键时才触发
            keydown是在用户按下按键时立即触发
        -->
        回车 <input type="text" @keyup.enter="add(40, 60)"> <br>
        空格 <input type="text" @keyup.space="add(20, 30)"> <br>
        Tab <input type="text" @keydown.tab="add(10, 20)"> <br>
        w <input type="text" @keyup.w="add(5, 10)"> <br>

        <!-- 组合快捷键 -->
        Ctrl + Enter <input type="text" @keyup.ctrl.enter="add(40, 60)"> <br>
        Ctrl + A <input type="text" @keyup.ctrl.a="add(20, 30)">
    </div>

    <script type="module">
        import {createApp,reactive} from './vue.esm-browser.js'

        createApp({
            setup() {
                const web = reactive({
                    url:"url",
                    user:0
                })

                const edit = () => {
                    web.url="edited-url"
                }

                const add = (a,b) => {
                    web.user += a+b
                }

                return {
                    web,
                    edit,
                    add
                }
            }
        }).mount("#app")
    </script>
</body>
```

[绑定事件v-on代码](../little_demo/vue3/part1/v-on.html)

### 显示和隐藏v-show

vue中v-show用于控制是否显示元素。v-show=true时显示，false时隐藏。

```html
<body>
    <div id="app">
        v-show:{{ web.show }}
        <hr>
        <p v-show="web.show">你看见我啦</p>

        <button @click="toggle">切换显示状态</button>
    </div>

    <script type="module">
        import {createApp,reactive} from './vue.esm-browser.js'

        createApp({
            setup() {
                const web = reactive({
                    show:true
                })

                const toggle = () => {
                    web.show = !web.show
                }

                return {
                    web,
                    toggle
                }
            }
        }).mount("#app")
    </script>
</body>
```

[v-show代码](../little_demo/vue3/part1/v-show.html)

### 条件渲染v-if

v-if也可以实现显示和隐藏。

如果频繁切换显示状态v-if会导致性能下降，此时需使用v-show。

同时可以结合`v-if`,`v-else-if`,`v-else`实现条件渲染。

```html
<body>
    <div id="app">
        v-show:{{ web.show }}
        <hr>
        <p v-show="web.show">你看见我啦</p>
        <p v-if="web.show">你又看见我啦</p>

        <button @click="toggle">切换显示状态</button>
        <hr>

        user:{{ web.user }}
        <p v-if="web.user < 1000">新网站</p>
        <p v-else-if="web.user >= 1000 & web.user < 10000">优秀网站</p>
        <p v-else>资深网站</p>
    </div>

    <script type="module">
        import {createApp,reactive} from './vue.esm-browser.js'

        createApp({
            setup() {
                const web = reactive({
                    show:true,
                    user:500
                })

                const toggle = () => {
                    web.show = !web.show
                }

                return {
                    web,
                    toggle
                }
            }
        }).mount("#app")
    </script>
</body>
```

[v-if代码](../little_demo/vue3/part1/v-if.html)

### 动态属性绑定v-bind

v-bind是用于绑定数据和元素属性的

```html
<body>
    <div id="app">
        <!-- :value -->
        <h3>value="abc.com"</h3>
        <input type="text" value="abc.com">
        <h3>v-bind:value="abc.com"</h3>
        <input type="text" v-bind:value="web.url">
        <h3>:value="abc.com"</h3>
        <input type="text" :value="web.url">

        <!-- :src -->
        <h3>src="abc.jpg"</h3>
        <img src="abc.jpg">
        <h3>:src="abc.jpg"</h3>
        <img :src="web.img">

        <!-- :class -->
        <h3>class="textColor"</h3>
        <b class="textColor">color</b>
        <h3>:class="{textColor:web.frontStatus}"</h3>
        <b :class="{textColor:web.frontStatus}">color</b>
    </div>

    <script type="module">
        import {createApp,reactive} from './vue.esm-browser.js'

        createApp({
            setup() {
                const web = reactive({
                    url:"abc.com",
                    img:"abc.jpg",
                    frontStatus: true
                })

                return {
                    web
                }
            }
        }).mount("#app")
    </script>
</body>
```

[v-bind代码](../little_demo/vue3/part1/v-bind.html)

### 遍历数组等对象v-for

```html
<body>
    <div id="app">
        <ul>
            <li v-for="value in data.number">
                {{ value }}
            </li>
        </ul>

        <ul>
            <li v-for="(value, index) in data.number">
                index = {{ index }} : value = {{ value }}
            </li>
        </ul>

        <ul>
            <li v-for="(value, key) in data.user">
                key = {{ key }} : value = {{ value }}
            </li>
        </ul>
        <ul>
            <li v-for="(value, key, index) in data.user">
                index = {{ index }} : key = {{ key }} : value = {{ value }}
            </li>
        </ul>

        <ul>
            <template v-for="(value, key, index) in data.user">
                <li v-if="index == 1">
                    index = {{ index }} : key = {{ key }} : value = {{ value }}
                </li>
            </template>
        </ul>

        <ul>
            <li v-for="(value, index) in data.teacher" :title="value.name" :key="value.id">
                index = {{ index }} : value.id = {{ value.id }} value.name={{ value.name }} value.web={{ value.web }}
            </li>
        </ul>
    </div>

    <script type="module">
        import {createApp,reactive} from './vue.esm-browser.js'

        createApp({
            setup() {
                const data = reactive({
                    number: ["十", "十一", "十二"], //数组
                    user: { //对象
                        name: "Luna",
                        gender: "女"
                    },
                    teacher: [ //包含两个对象的数组
                        { id: 100, name: "a", web: "a.com" },
                        { id: 101, name: "b", web: "b.com" }
                    ]
                })

                return {
                    data
                }
            }
        }).mount("#app")
    </script>
</body>
```

[v-for代码](../little_demo/vue3/part1/v-for.html)

### 双向数据绑定v-model

- 单向数据绑定v-bind 当数据发生改变时, 视图会自动更新. 但用户手动更改 input 的值, 数据不会自动更新
- 双向数据绑定v-model 当数据发生改变时, 视图会自动更新. 当用户手动更改 input 的值, 数据也会自动更新

```html
<body>
    <div id="app">
        <h3>文本框 {{ data.text }}</h3>
        <h3>单选框 {{ data.radio }}</h3>
        <h3>复选框 {{ data.checkbox }}</h3>
        <h3>记住密码 {{ data.remember }}</h3>
        <h3>下拉框 {{ data.select }}</h3>

        <!-- 单向数据绑定 当数据发生改变时, 视图会自动更新. 但用户手动更改 input 的值, 数据不会自动更新 -->
        单向数据绑定 <input type="text" :value="data.text">

        <hr>
        <!-- 
            双向数据绑定 当数据发生改变时, 视图会自动更新. 当用户手动更改 input 的值, 数据也会自动更新
            对于 <input type="text">, v-model 绑定的是 input 元素的 value 属性
        -->
        双向数据绑定 <input type="text" v-model="data.text">

        <hr>
        <!-- 
            单选框
            对于 <input type="radio">, v-model 绑定的是 input 元素的选中状态
        -->
        <input type="radio" v-model="data.radio" value="1">写作
        <input type="radio" v-model="data.radio" value="2">画画

        <hr>
        <!-- 
            复选框
            对于 <input type="checkbox">, v-model 绑定的是 input 元素的选中状态
        -->
        <input type="checkbox" v-model="data.checkbox" value="a">写作
        <input type="checkbox" v-model="data.checkbox" value="b">画画
        <input type="checkbox" v-model="data.checkbox" value="c">运动

        <hr>
        <!-- 记住密码 -->
        <input type="checkbox" v-model="data.remember">记住密码

        <hr>
        <!-- 
            下拉框
            对于 <select>, v-model 绑定的是 select 元素的选中状态
        -->
        <select v-model="data.select">
            <option value="">请选择</option>
            <option value="A">写作</option>
            <option value="B">画画</option>
            <option value="C">运动</option>
        </select>
    </div>

    <script type="module">
        import {createApp,reactive} from './vue.esm-browser.js'

        createApp({
            setup() {
                const data = reactive({
                    text: "text", //文本框
                    radio: "", //单选框
                    checkbox: [], //复选框
                    remember: false, //单个复选框-记住密码
                    select: "" //下拉框
                })

                return {
                    data
                }
            }
        }).mount("#app")
    </script>
</body>
```

[v-model代码](../little_demo/vue3/part1/v-model.html)

#### v-model修饰符

|修饰符|功能|
|---|---|
|lazy|失去焦点或者用户点击回车按钮时才会将后台的数据进行修改|
|number|将输入的数字转为number类型|
|trim|去掉字符串首部或者尾部的所有空格|

```html
<body>
    <div id="app">
        <h3>url: {{ web.url }}</h3>
        <h3>user: {{ web.user }}</h3>

        实时渲染 <input type="text" v-model="web.url"> <br>

        在失去焦点或按下回车键之后渲染 <input type="text" v-model.lazy="web.url"> <br>

        <!-- 输入 100人, web.user 的值仍为 100 -->
        输入框的值转换为数字类型 <input type="text" v-model.number="web.user"> <br>

        去除首尾空格 <input type="text" v-model.trim="web.url">
    </div>

    <script type="module">
        import {createApp,reactive} from './vue.esm-browser.js'

        createApp({
            setup() {
                const web = reactive({
                    url: "abc.com",
                    user: 10
                })

                return {
                    web
                }
            }
        }).mount("#app")
    </script>
</body>
```

[v-model2代码](../little_demo/vue3/part1/v-model2.html)

### 渲染数据v-text和v-html

v-text按照文件进行渲染，v-html按照html格式渲染

```html
<body>
    <div id="app">
        <h3>{{ web.title }}</h3>

        <!-- v-text 将数据解析为纯文本格式 -->
        <h3 v-text="web.title"></h3>

        <!-- v-html 将数据解析为 html 格式 -->
        <h3 v-html="web.url"></h3>
        </div>

    <script type="module">
        import {createApp,reactive} from './vue.esm-browser.js'

        createApp({
            setup() {
                const web = reactive({
                    title:"vue learning",
                    url:"<i style='color:aqua'>abc.com</i>"
                })

                return {
                    web
                }
            }
        }).mount("#app")
    </script>
</body>
```

[v-text_v-html代码](../little_demo/vue3/part1/v-text_v-html.html)

### 计算属性computed

Vue.js 中的计算属性是基于它的响应式系统来实现的，它可以根据 Vue 实例的数据状态来动态计算出新的属性值。在 Vue 组件中，计算属性常用于对数据进行处理和转换，以及动态生成一些需要的数据。

```html
<body>
    <div id="app">
        <h3>add: {{ add() }}</h3>
        <h3>add: {{ add() }}</h3>

        <h3>sum: {{ sum }}</h3>
        <h3>sum: {{ sum }}</h3>

        x <input type="text" v-model.number="data.x"> <br>
        y <input type="text" v-model.number="data.y">
    </div>

    <script type="module">
        import {createApp,reactive,computed} from './vue.esm-browser.js'

        createApp({
            setup() {
                const data = reactive({
                    x: 10,
                    y: 20
                })

                //方法-无缓存
                let add = () => {
                    console.log("add") //打印两次
                    return data.x + data.y
                }

                //计算属性-有缓存 [计算属性根据其依赖的响应式数据变化而重新计算]
                const sum = computed(() => {
                    console.log("sum") //打印一次
                    return data.x + data.y
                })

                return {
                    data,
                    sum,
                    add
                }
            }
        }).mount("#app")
    </script>
</body>
```

计算属性返回的是属性，如果需要返回可以调用函数则可以
```html
<script type="module">
    const sum = computed(() => {
        console.log("sum") //打印一次
            return function(){
                return data.x + data.y
            }
    })
</script>
```
然后在其它代码中使用sum()调用

[computed代码](../little_demo/vue3/part1/computed.html)

### 侦听器watch

vue 中 watch 是一种响应式函数，用于监听数据属性值的变化并执行回调函数。基本用法是 watch(property, handler)，其中 property 是要监视的属性或属性数组，handler 是回调函数。它还可以配置选项对象，例如 immediate（立即调用）和 deep（深度监听）。watch 适用于需要对数据属性值的变化做出反应的情况，例如更新 ui 或异步加载数据。

- watch显式指定依赖数据，依赖数据更新时执行回调函数
- 具有一定的惰性lazy 第一次页面展示的时候不会执行，只有数据变化的时候才会执行(设置immediate: true时可以变为非惰性，页面首次加载就会执行）
- 监视ref定义的响应式数据时可以获取到原值既要指明监视的属性，也要指明监视的回调

```html
<body>
    <div id="app">
        爱好
        <select v-model="hobby">
            <option value="">请选择</option>
            <option value="1">写作</option>
            <option value="2">画画</option>
            <option value="3">运动</option>
        </select>
        <hr>

        年
        <select v-model="date.year">
            <option value="">请选择</option>
            <option value="2023">2023</option>
            <option value="2024">2024</option>
            <option value="2025">2025</option>
        </select>

        月
        <select v-model="date.month">
            <option value="">请选择</option>
            <option value="10">10</option>
            <option value="11">11</option>
            <option value="12">12</option>
        </select>
    </div>

    <script type="module">
        import {createApp,reactive,ref,watch} from './vue.esm-browser.js'

        createApp({
            setup() {
                const hobby = ref("") //爱好
                const date = reactive({ //日期
                    year: "2023",
                    month: "10"
                })

                //监听 hobby
                watch(hobby, (newValue, oldValue) => {
                    console.log("oldValue", oldValue, "newValue", newValue)

                    if (newValue == "2") {
                        console.log("画画")
                    }
                })

                //监听 date
                watch(date, (newValue, oldValue) => {
                    /*
                        JS中对象和数组是通过引用传递的, 而不是通过值传递
                        当修改对象或数组的值时, 实际上修改的是对象或数组的引用, 而不是创建一个新的对象或数组
                        所以，如果修改了对象或数组的值，那么打印出来的结果则是修改后的值
                    */
                    console.log("oldValue", oldValue, "newValue", newValue)

                    if (newValue.year == "2025") {
                        console.log("2025")
                    }

                    if (newValue.month == "11") {
                        console.log("11")
                    }
                })

                //监听 date 中的某个属性 year
                watch(() => date.year, (newValue, oldValue) => {
                    console.log("oldValue", oldValue, "newValue", newValue)

                    if (date.year == "2024") {
                        console.log("2024")
                    }
                })

                return {
                    hobby,
                    date
                }
            }
        }).mount("#app")
    </script>
</body>
```

[watch代码](../little_demo/vue3/part1/watch.html)

### 自动侦听器watchEffect

无需指定监听属性的监听器，自动监听器watchEffect。

- watchEffect自动收集依赖数据，依赖数据更新时重新执行自身
- 立即执行，没有惰性，页面的首次加载就会执行
- 无法获取到原值，只能得到变化后的值
- 不用指明监视哪个属性，监视的回调中用到哪个属性就监视哪个属性

```html
<script type="module">
        import {createApp,reactive,ref,watchEffect} from './vue.esm-browser.js'

        createApp({
            setup() {
                const hobby = ref("") //爱好
                const date = reactive({ //日期
                    year: "2023",
                    month: "10"
                })

                //自动监听
                watchEffect(() => {
                    console.log("------ 监听开始")

                    if (hobby.value == "2") {
                        console.log("画画")
                    }

                    if (date.year == "2025") {
                        console.log("2025")
                    }

                    if (date.month == "11") {
                        console.log("11")
                    }

                    console.log("------ 监听结束")
                })

                return {
                    hobby,
                    date
                }
            }
        }).mount("#app")
    </script>
```

[watchEffect代码](../little_demo/vue3/part1/watchEffect.html)

## 案例

[图片轮播](../little_demo/vue3/part2/image_show.html)

[记事本](../little_demo/vue3/part2/note.html)

[购物车](../little_demo/vue3/part2/cart.html)

## 组件

### Vite

#### Vite创建vue3项目

首先按照node.js，然后在需要创建vue项目的文件夹下执行

```sh
npm create vite@latest
```

执行时指定项目名称，框架和类型，这里选默认名称，vue，JavaScript

完成之后按照提示执行

```sh
cd vite-project
npm install
npm run dev
```

默认项目创建完成，之后删除模板内容或者直接修改就可以开始开发了

#### 导入组件

这里将之前的[显示和隐藏](#显示和隐藏v-show)部分的学习代码迁入vue项目中，首先将模板内容放入template中，将script中除了return的内容也放入script中，import的对象改为vue

```vue
<script setup>
    import { reactive } from 'vue'

    const web = reactive({
        show:true
    })

    const toggle = () => {
        web.show = !web.show
    }
</script>

<template>
    <h3>v-show:{{ web.show }}</h3>
    <p v-show="web.show">你看见我啦</p>

    <button @click="toggle">切换显示状态</button>
</template>
```

然后在项目文件夹下使用`npm run dev`打开服务器就有网页了。

接下来导入组件，我们在components中创建组件header.vue和foot.vue在其中的template中添加h3

然后回到App.vue中，在script中import文件,然后再template中使用组件即可

header.vue
```vue
<template>
    <h3>header</h3>
</template>

<script setup>

</script>

<style scoped>

</style>
```

App.vue
```vue
<script setup>
    import Header from './components/header.vue'
    import Footer from './components/footer.vue'
</script>

<template>
    <Header/>

    <Footer/>
</template>

<style scoped>

</style>
```

#### 父传子 defineProps

父传子，即从父组件中往子组件中传递数值。

例如父组件App.vue引用了子组件Header，便可以在template的引用中声明属性`<Header name="abc" url="abc.com" />`，

然后在子组件中的script中使用defineProps获得传递的数值`const props = defineProps(["name","url"])`，我们可以在props中读到父组件传递来的name和url的值。

header.vue
```vue
<template>
    <h3>header</h3>
</template>

<script setup>
    const props = defineProps(["name","url"])
    console.log(props);
</script>
```

同理结构体也可以使用相同的方式传递数值。

在父组件App.vue的script中声明对象`const propsWeb = {user:10,url:"www.cba.com"}`，在template中使用v-bind传递`<Footer v-bind="propsWeb" />`，

然后在子组件footer.vue的script中接收数据`const props = defineProps({user:Number,url:String})`

如果需要传递响应式数据，即父组件中数据变化时可以即时传递，可以使用reactive。

App.vue
```vue
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
```

footer.vue
```vue
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
```

#### 子传父 defineEmits

子组件也可以传递数值给父组件，即使用defineEmits从子组件往父组件传递，但是defineEmits传递的是事件和对应的数据。

即子组件script中声明对象`const emits = defineEmits(["getWeb","userAdd"])`，执行函数传递方法和数据`emits("getWeb",{name:"abc",url:"abc.com"})`,

父组件template中使用@事件接收子组件传递的事件`<Footer @getWeb="emitsGetWeb" />`，然后再script中就可以得到相关的事件和值了`const emitsGetWeb = (data)=>{web.url = data.url}`

App.vue
```vue
<script setup>
    import { reactive, ref } from 'vue'
    import Footer from './components/footer.vue'
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
    <Footer @getWeb="emitsGetWeb" @userAdd="emitsUserAdd" />
    <p>{{ web.url }}</p>
    <p>Emits {{ user }}</p>
</template>
```

footer.vue
```vue
<template>
    <h3>footer</h3>
    <p></p>
    <button @click="add">emits添加用户</button>
</template>

<script setup>
    // emits
    const emits = defineEmits(["getWeb","userAdd"])
    emits("getWeb",{name:"abcd",url:"abcd.com"})

    const add=()=>{
        emits("userAdd",10)
    }
</script>
```

#### 跨组件通信 依赖注入

在 Vue 3 中，provide 和 inject 是两个用于实现依赖注入（Dependency Injection）的 API。依赖注入是一种编程技术，它允许你通过某个提供者（provider）向组件或其子组件注入依赖项（如数据、方法等），而无需显式地在每个组件之间传递它们。

provide和inject用于组件封装的时候，多层组件嵌套的传值问题。

在父组件中使用`provide("name",verb)`提供数据，子组件和子组件的子组件等组件中使用`const verb = inject("name")`接收数据。

同理函数也可以用这个方法注入。

但是这个方法没有办法从子组件传父组件。

App.vue
```vue
<script setup>
    import { reactive, ref,provide } from 'vue'
    import son from './components/son.vue';

    const user = ref(0)
    const web = reactive({
        name:'abc',
        url:'abc.com'
    })
    // provider
    provide("provideWeb",web)
    provide("provideUser",user)
    const puserAdd=()=>{
        user.value++
    }
    provide("provideFuncPUserAdd",puserAdd)
</script>

<template>
    <h3>App.vue Top</h3>
    user:{{ user }}
    <!-- 子组件 -->
    <son/>
</template>
```

son.vue
```vue
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
```

grandson.vue
```vue
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
```

## 参考

[Vue3 学习指南](https://www.dengruicode.com/study?uuid=58893cef7e824a02b16039129d59713c)

[vue.js官网](https://cn.vuejs.org/)