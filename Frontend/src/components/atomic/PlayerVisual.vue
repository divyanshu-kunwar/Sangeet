<script setup>

defineProps({
    isPlaying: Boolean,
    amplitude: Number,
})

</script>

<template>
    <div>
        <svg @click="$emit('changePlayState', isPlaying)" width="70%" height="auto" viewBox="0 0 287 282" fill="none"
            xmlns="http://www.w3.org/2000/svg">

            <!-- ----------pause button-------->
            <g v-if="isPlaying" filter="url(#filter0_d_174_2)">
                <path
                    d="M123.5 109C120.463 109 118 111.463 118 114.5V160.076C118 163.113 120.463 165.576 123.5 165.576H134.501C137.539 165.576 140.002 163.113 140.002 160.076V114.5C140.002 111.463 137.539 109 134.501 109H123.5ZM151.789 109C148.751 109 146.288 111.463 146.288 114.5V160.076C146.288 163.113 148.751 165.576 151.789 165.576H162.789C165.827 165.576 168.29 163.113 168.29 160.076V114.5C168.29 111.463 165.827 109 162.789 109H151.789Z"
                    fill="url(#paint0_linear_174_2)" />
            </g>

            <!-- ----------play button-------->
            <g v-else filter="url(#filter0_d_174_2)">
                <path
                    d="M116 113.464C116 107.81 122.05 104.214 127.017 106.917L167.969 129.2C173.157 132.023 173.157 139.471 167.969 142.295L127.017 164.578C122.05 167.28 116 163.684 116 158.03V113.464Z"
                    fill="url(#paint0_linear_174_2)" />
            </g>

            <!-- ----------circular waves visual-------->
            <g :class="isPlaying?'scaleAnim':''" filter="url(#filter1_d_174_2)">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M140.505 16.2221C128.439 15.679 118.096 15.2134 104.247 19.7151C95.2624 22.6357 82.2453 29.7731 82.2453 29.7731C82.2453 29.7731 66.0614 41.0663 57.1004 
                49.889C45.3785 61.4301 38.6052 68.4541 31.3268 83.2061C24.2389 97.572 22.1029 106.857 20.6402 122.809C18.5763 145.318 21.5007 158.852 29.4409 180.014C35.8163 
                197.006 40.8642 206.489 52.7 220.246C62.5812 231.732 68.9752 238.079 82.2453 245.391C104.055 257.408 120.234 257.258 145.108 256.078C161.075 255.32 170.307 
                253.971 185.34 248.534C204.941 241.444 216.565 235.656 230.601 220.246C241.489 208.291 245.167 197.514 249.59 184.552C251.205 179.822 252.918 174.802 255.117
                 169.328C256.068 166.96 257.001 164.699 257.9 162.52C265.183 144.875 270.244 132.612 264.546 112.751C260.253 97.7881 258.106 93.8221 248.831 81.3202C244.936
                  76.0714 242.054 71.5023 239.293 67.1256C235.207 60.6473 231.387 54.5905 224.943 47.3745C222.211 44.3154 219.8 41.347 217.506 38.5239C209.481 28.6453 202.901
                   20.5468 189.111 16.572C181.176 14.2847 175.246 14.9544 168.477 15.7188C165.185 16.0906 161.695 16.4847 157.68 16.572C151.341 16.7098 145.76 16.4586 140.505
                    16.2221ZM140.707 234.704C194.52 234.704 238.144 191.08 238.144 137.268C238.144 83.4548 194.52 39.831 140.707 39.831C86.8946 39.831 43.2707 83.4548 43.2707
                     137.268C43.2707 191.08 86.8946 234.704 140.707 234.704Z" fill="url(#paint2_linear_174_2)" />

            </g>

            <!-- ----------circular waves difference visual-------->
            <g :class="isPlaying ? 'scaleAnim' : '' " style="mix-blend-mode:difference" filter="url(#filter2_d_174_2)">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M140.899 18.4039C128.984 17.8676 118.77 17.4079 105.095 21.8531C96.223 24.7372 83.3689 31.7851 83.3689 31.7851C83.3689 31.7851 67.3877 42.9369 58.539 
                51.6491C46.9639 63.0455 40.2755 69.9816 33.0882 84.5488C26.0891 98.7347 23.9799 107.904 22.5355 123.656C20.4975 145.882 23.3852 159.247 31.226 180.144C37.5215 
                196.923 42.5061 206.287 54.1937 219.872C63.9511 231.214 70.265 237.482 83.3689 244.702C104.906 256.568 120.882 256.421 145.444 255.255C161.211 254.506 170.328 
                253.175 185.172 247.806C204.527 240.805 216.007 235.089 229.866 219.872C240.618 208.067 244.25 197.425 248.618 184.625C250.212 179.955 251.904 174.997 254.075 
                169.591C255.014 167.254 255.936 165.021 256.824 162.869C264.015 145.445 269.013 133.336 263.386 113.724C259.147 98.9481 257.027 95.0319 247.868 82.6866C244.022 
                77.5034 241.176 72.9916 238.45 68.6697C234.415 62.2726 230.642 56.2917 224.279 49.1661C221.582 46.1453 219.2 43.2141 216.936 40.4264C209.011 30.6714 202.514 
                22.6744 188.896 18.7494C181.06 16.4908 175.204 17.1521 168.521 17.9069C165.27 18.274 161.824 18.6632 157.859 18.7494C151.599 18.8855 146.088 18.6374 140.899 
                18.4039ZM141.099 234.149C194.237 234.149 229.866 206.139 229.866 153C229.866 99.8614 194.237 41.717 141.099 41.717C87.96 41.717 44.8826 84.7944 44.8826 
                137.933C44.8826 191.072 87.96 234.149 141.099 234.149Z" fill="url(#paint4_radial_174_2)" />
            </g>

            <defs>
                <filter id="filter0_d_174_2" x="98" y="94" width="90.29" height="96.5761" filterUnits="userSpaceOnUse"
                    color-interpolation-filters="sRGB">
                    <feFlood flood-opacity="0" result="BackgroundImageFix" />
                    <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                        result="hardAlpha" />
                    <feOffset dy="5" />
                    <feGaussianBlur stdDeviation="10" />
                    <feComposite in2="hardAlpha" operator="out" />
                    <feColorMatrix type="matrix" values="0 0 0 0 0.325 0 0 0 0 0.352 0 0 0 0 1 0 0 0 0.25 0" />
                    <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_174_2" />
                    <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_174_2" result="shape" />
                </filter>
                <filter id="filter1_d_174_2" x="0" y="0" width="287" height="281.596" filterUnits="userSpaceOnUse"
                    color-interpolation-filters="sRGB">
                    <feFlood flood-opacity="0" result="BackgroundImageFix" />
                    <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                        result="hardAlpha" />
                    <feOffset dy="5" />
                    <feGaussianBlur stdDeviation="10" />
                    <feComposite in2="hardAlpha" operator="out" />
                    <feColorMatrix type="matrix" values="0 0 0 0 0.325 0 0 0 0 0.352 0 0 0 0 1 0 0 0 0.25 0" />
                    <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_174_2" />
                    <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_174_2" result="shape" />
                </filter>
                <filter id="filter2_d_174_2" x="1.90332" y="2.19711" width="283.906" height="278.57"
                    filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                    <feFlood flood-opacity="0" result="BackgroundImageFix" />
                    <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                        result="hardAlpha" />
                    <feOffset dy="5" />
                    <feGaussianBlur stdDeviation="10" />
                    <feComposite in2="hardAlpha" operator="out" />
                    <feColorMatrix type="matrix" values="0 0 0 0 0.325 0 0 0 0 0.352 0 0 0 0 1 0 0 0 0.25 0" />
                    <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_174_2" />
                    <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_174_2" result="shape" />
                </filter>
                <linearGradient id="paint0_linear_174_2" x1="118" y1="115.789" x2="172.018" y2="149.4"
                    gradientUnits="userSpaceOnUse">
                    <stop stop-color="#105BDB" />
                    <stop offset="1" stop-color="#50FEFE" />
                </linearGradient>
                <linearGradient id="paint2_linear_174_2" x1="20" y1="43.9915" x2="263.379" y2="218.168"
                    gradientUnits="userSpaceOnUse">
                    <stop stop-color="#105BDB" />
                    <stop offset="1" stop-color="#50FEFE" />
                </linearGradient>
                <radialGradient id="paint4_radial_174_2" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse"
                    gradientTransform="translate(143.856 129.325) rotate(34.3988) scale(147.799 146.653)">
                    <stop />
                    <stop offset="0.546875" />
                    <stop offset="1" stop-color="white" />
                </radialGradient>
            </defs>

        </svg>
    </div>
</template>

<style scoped>
div{
    display: flex;
    align-items: center;
    justify-content: center;
}

.scaleAnim{
    animation: animate 0.2s ease-in-out infinite alternate;
}

@keyframes animate{
    from{
        transform: scale(1);
        transform-origin: center center;
    }
    to{
        transform: scale(0.9);
        transform-origin: center center;
    }
}
</style>