<script setup>
import Card_ from '@/components/atomic/Card_.vue';
import Outer from "@/components/molecular/Outer.vue"


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
    <Outer>
        <div class="LRLayout">
            
            <div class="text">
                <h1>The<br/>World’s<br/>Destination<br/>For Music</h1>
            </div>



            <div class="musicgrid">
                <RouterLink :to="{name: 'Login'}">
                     <img  src="/sample/a.jpg" href="login"/>
                     <img  src="/sample/b.jpg" href="login"/>
                     <img  src="/sample/c.jpg" href="login"/>
                     <img  src="/sample/d.jpg" href="login"/>
                     <img  src="/sample/e.jpg" href="login"/>
                     <img  src="/sample/f.jpg" href="login"/>
                     <img  src="/sample/g.jpg" href="login"/>
                     <img  src="/sample/h.jpg" href="login"/>
                     <img  src="/sample/i.jpg" href="login"/>
                     <img  src="/sample/j.jpg" href="login"/>
                     <img  src="/sample/k.jpg" href="login"/>
                     <img  src="/sample/l.jpg" href="login"/>
                     <img  src="/sample/m.jpg" href="login"/>
                     <img  src="/sample/n.jpg" href="login"/>
                     <img  src="/sample/o.jpg" href="login"/>

                     <img  src="/sample/a.jpg" href="login"/>
                     <img  src="/sample/b.jpg" href="login"/>
                     <img  src="/sample/c.jpg" href="login"/>
                     <img  src="/sample/d.jpg" href="login"/>
                     <img  src="/sample/e.jpg" href="login"/>
                     <img  src="/sample/f.jpg" href="login"/>
                     <img  src="/sample/g.jpg" href="login"/>
                     <img  src="/sample/h.jpg" href="login"/>
                     <img  src="/sample/i.jpg" href="login"/>
                     <img  src="/sample/j.jpg" href="login"/>
                     <img  src="/sample/k.jpg" href="login"/>
                     <img  src="/sample/l.jpg" href="login"/>
                     <img  src="/sample/m.jpg" href="login"/>
                     <img  src="/sample/n.jpg" href="login"/>
                     <img  src="/sample/o.jpg" href="login"/>

                </RouterLink>
            </div>

        </div>
    </Outer>

</template>

<style scoped>

.LRLayout {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    height: 100%;
}


.text {
    max-width: 700px;
    display: flex;
    flex-direction: row;
    color: var(--fore-2);
    align-self: center;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-size: clamp(20px, 7vw, 60px);
    background-image: url('../assets/ghome.png');
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    color: var(--fore-2);
}

.text:hover{
    text-shadow: 0px 0px 50px rgba(199, 164, 255, 0.44);

}

h1{
    margin: 0%;
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

.musicgrid{
    display: flex;
    width: 98vw;
    overflow-x:hidden;
    margin: 0rem auto;
    rotate: 1deg;
    transform: translateY(-10px);
    justify-self: flex-end;
}

.musicgrid > a{
    position: relative;
    width: fit-content;
    display: flex;
    transform: translateX(-10%);
    animation: trans 10s ease-in-out 1s infinite alternate;
    padding-top: 10px;
    justify-self: flex-end;
}

.musicgrid > a > img{
    height: clamp(100px, 15vh, 200px);
    padding: 0% !important;
    border-radius: 16px;
    margin: 0px 4px;
    filter: grayscale(50%) blur(1px) hue-rotate(30deg);
    object-fit: cover;
    transition: all 0.3s ease;
}

.musicgrid > a > img:hover{
    filter: grayscale(10%);
}

@keyframes trans {
    from{
        transform:translateX(-10%);
    }
    to{
        transform:translateX(-30%);
    }
}

</style>
