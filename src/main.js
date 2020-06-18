import Vue from 'vue';

import Test from './Components/Test.vue';
import Second from './Components/Second.vue';

new Vue({
    el: '#vue1',
    render: h => h(Test)
})

new Vue({
    el: '#vue2',
    render: h => h(Second)
})