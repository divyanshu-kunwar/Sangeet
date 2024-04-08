<script setup>
import { ref } from 'vue';

const emit = defineEmits(['seekTo'])
const isdragged = ref(false)

const props = defineProps({
    totalLength:Number,
    seekLength:Number,
    strokeWidth:Number,
    bufferedLength:Number
})

const getProgressWidth = (seekLength,totalLength) => {
    return seekLength*1000/totalLength
}

function dragstarted(e){
    isdragged.value = true
    let ewidth = e.srcElement.getBoundingClientRect().width;
    let ix = e.x 
    document.onmouseup = stopDrag
    document.onmousemove = (e) =>{
        let nx = e.x
        let diff = (nx - ix)*props.totalLength / ewidth;
        diff = Math.min(props.totalLength , Math.max(0,props.seekLength+diff))
        emit('seekTo' , diff)
        ix = nx
    }
}

function stopDrag(){
    isdragged.value = false
    document.onmousemove = null;
    document.onmouseup = null;
}

function dragToThisPos(e){
    let ewidth = e.srcElement.getBoundingClientRect().width;
    let ix = e.srcElement.getBoundingClientRect().x
    let diff = (e.x - ix)*props.totalLength / ewidth;
    diff = Math.min(props.totalLength , Math.max(0,diff))
    emit('seekTo' , diff)
}

</script>

<template>
    <svg id="seeksvg" @mousedown="dragstarted" class="cursor" height="16" viewBox="0 0 1000 16" fill="none"
        xmlns="http://www.w3.org/2000/svg">
        <path @click="dragToThisPos" id="bar_length" d="M15 5.4824L990 5.4824" 
            stroke-linecap="round" :stroke-width="strokeWidth" />
            <path  id="progress" v-if="bufferedLength" class="graybar"
                :d="'M15 5.4824L' + getProgressWidth(bufferedLength, totalLength) + ' 5.4824'" 
                stroke-linecap="round"  :stroke-width="strokeWidth"/>
        <path @click="dragToThisPos" id="progress" :class="isdragged ? 'bluebar' : 'whitebar'"
            :d="'M15 5.4824L' + getProgressWidth(seekLength, totalLength) + ' 5.4824'" 
            stroke-linecap="round"  :stroke-width="strokeWidth"/>
        <circle :class="isdragged ? 'circleop' : 'circlenp'" id="seekcircle" :cx="getProgressWidth(seekLength, totalLength)"
            cy="7" :r="strokeWidth" fill="#D9D9D9" />
    </svg>
</template>

<style scoped>
#seeksvg{
    width: calc(100% - 8rem);
}

#seekcircle{
    fill: var(--fore-2);
}

.circleop{
    opacity: 1;
}

.circlenp{
    opacity: 0;
}

#seeksvg:hover .circlenp{
    opacity: 1;
}

#seeksvg:hover .whitebar{
    stroke: var(--primary);
}
.whitebar{
    stroke: var(--fore-2);
}
.bluebar{
    stroke: var(--primary);
}

.graybar{
    stroke: var(--fore-2);
    opacity: 0.2;
}

#bar_length {
    stroke: var(--back-2);
}
</style>