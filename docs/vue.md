# Vue 学习笔记

Vue (发音为 /vjuː/，类似 view) 是一款用于构建用户界面的 JavaScript 框架。它基于标准 HTML、CSS 和 JavaScript 构建，并提供了一套声明式的、组件化的编程模型，帮助你高效地开发用户界面。无论是简单还是复杂的界面，Vue 都可以胜任。

## 创建一个应用

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

## 模块化开发

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

## ref 和 reactive

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

## 绑定事件v-on

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

## 显示和隐藏v-show

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

## 条件渲染v-if

v-if也可以实现显示和隐藏。

