<script setup>
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
    <div id="circle" v-bind:style="position_style">
    </div>
</template>

<style scoped>

#circle {
    position: absolute;
    z-index: 2;
    opacity: 0.4;
    width: 0px;
    height: 0px;
    background: rgb(0, 153, 255, 0.2);
    box-shadow: 0px 0px 233px 233px rgba(0, 25, 247, 0.1);
}
</style>