<script setup>
import Header from '@/components/molecular/Header.vue'
import Footer from '@/components/molecular/Footer.vue'

import { ref } from 'vue';

const x_val = ref(0);
const y_val = ref(0);


// style binding
const position_style = ref({
    top: y_val,
    left: x_val
});

const updateCoordinates = (event) => {
    x_val.value = event.clientX;
    y_val.value = event.clientY;
    position_style.value = {
        top: y_val.value + 'px',
        left: x_val.value + 'px'
    };
}
window.addEventListener('mousemove', updateCoordinates);

</script>

<template>
    <div id="home">
        <div id="circle" v-bind:style="position_style">
        </div>
        <Header></Header>
        <slot></slot>
        <Footer></Footer>
    </div>
</template>

<style scoped>
#home{
    height: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: space-between;
    justify-content: space-between;
}
/* width */
#home::-webkit-scrollbar {
  width: 5px;
}

/* Track */
#home::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--fore-2);
  border-radius: 5px;
}

/* Handle */
#home::-webkit-scrollbar-thumb {
  background: var(--gradient);
  border-radius: 5px;
}

#circle {
    position: absolute;
    z-index: -5;
    opacity: 0.5;
    width: 0px;
    height: 0px;
    background: rgb(0, 153, 255);
    box-shadow: 0px 0px 233px 233px rgba(0, 128, 247, 0.2);
}

</style>
