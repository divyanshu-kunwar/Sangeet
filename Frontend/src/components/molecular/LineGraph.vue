<script setup>
import Plotly from 'plotly.js-dist-min'
import { onMounted } from 'vue';
import { ref } from 'vue'
import { watch } from 'vue';

const props = defineProps({
    title: String,
    data: Object,
    xTitle: String,
    yTitle: String,
    width: Number,
    height: Number
})

const layout = {
    margin: {
        l: 80,
        r: 20,
        b: 70,
        t: 70,
        pad: 0
    },
    title: {
        text: props.title,
    },
    xaxis: {
        visible: true,
        showticklabels: true,
        title: {
            text: props.xTitle,
            standoff: 25
        },
        ticks: "outside",
        showline: true
    },
    yaxis: {
        visible: true,
        showticklabels: true,
        title: {
            text: props.yTitle,
            standoff: 25
        },
        ticks: "outside",
        showline: true
    },
    plot_bgcolor: '#111',
    paper_bgcolor: '#111',
    font: {
        color: '#999'
    },
    showlegend: props.data.length > 1,
    legend: {
        x: 0.2,
        xanchor: 'right',
        y: 1
    }
}

const config = {
    responsive: true,
    displayModeBar: false
}

const eleme = ref(null)

onMounted(() => {
    Plotly.newPlot(eleme.value,
        props.data, layout, config
    )
})

</script>

<template>
    <div id="line_graph" ref="eleme" :style="{ width: width + 'px', height: height + 'px' }"></div>
</template>

<style scoped>
#line_graph {
    margin: 1rem;
    border-radius: 4px;
    overflow: hidden;
}
</style>
