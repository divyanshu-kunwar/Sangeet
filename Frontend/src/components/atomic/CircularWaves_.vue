<script setup>
import P5 from 'p5'
import { onMounted } from 'vue';

let a = 0;

onMounted(()=>{
    const script = p5 => {
        p5.setup = ()=>{
            p5.createCanvas(400, 400);
            p5.background(0)
        };
        p5.draw = () => {
            p5.background(0 , 0 , 0, 15);
            p5.noStroke()
            p5.translate(p5.width/2 , p5.height/2)
            p5.rotate(a)
            p5.fill(0,50,255 , 10)
            p5.ellipse(50*p5.cos(4*a),100, 300, 200*p5.cos(a))
            p5.fill(0,250,25 , 10)
            p5.ellipse(60*p5.cos(2*a),200, 300, 50*p5.cos(a*4))
            a += 0.05
      }; 
    }
    const p5canvas = new P5(script, 'canvas');
})


</script>
<template>
    <div>
        <div id="canvas"></div>
    </div>
</template>

<style scoped>

</style>