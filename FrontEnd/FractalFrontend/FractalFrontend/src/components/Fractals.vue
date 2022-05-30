<template>
    <div class="fractals_container">
        <h1>Fractals</h1>
        <div class="container">
            <div class="col" v-for="fractals in columns">
                <div v-for="fractal in fractals" class="item-container">
                    <div class="block">
                        <img v-bind:src="fractal.path" height="100" width="100" alt="">
                    </div>
                    <div class="block">
                        <div class="slider">
                            <span v-text="values[fractal.id]"></span>
                        </div>
                        <div>
                            <input type="range" min="0" max="100" step="1" class="slider" v-bind:id="fractal.id"
                                v-model="values[fractal.id]">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <button @click="eval()" :disabled="disable_button">Eval</button>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            values: {},
            fractals: [],
            cols: 2,
            disable_button: false,
        }
    }, 
    methods: {
        async eval() {
            this.disable_button= true;
            let ids = []
            let evaluations = []
            for (const [key, value] of Object.entries(this.values)) {
                ids.push(key)
                evaluations.push(value)
            }
            let res = {
                "ids": ids,
                "evaluations": evaluations
            }
            const allEqual = arr => arr.every(val => val === arr[0]);
            if (!allEqual(evaluations)) {
                try {

                    const response = await axios.post('http://127.0.0.1:8000/Images', res)
                    self.disable_button = false
                    await this.getData()
                    //location.reload()
                } catch (error) {
                    console.error(error);
                    self.disable_button = false
                }
            }
        },
        fetchValues() {
            this.fractals.forEach(fractal => {
                this.values[fractal.id] = 0
            });
        },

        async getData() {
            try {

                const response = await axios.get('http://127.0.0.1:8000/Images');

                for (let i = 0; i < response.data.paths.length; i++) {
                    this.fractals[i] = {
                        path: response.data.paths[i],
                        id: response.data.ids[i],
                    }

                }

                this.fetchValues()
            } catch (error) {
                // log the error
                console.log(error);
            }
        },
    },
    computed: {
        columns() {
            let columns = []
            let mid = Math.ceil(this.fractals.length / this.cols)
            for (let col = 0; col < this.cols; col++) {
                columns.push(this.fractals.slice(col * mid, col * mid + mid))
            }
            return columns
        },
    },

    created() {
        // Fetch tasks on page load
        this.getData();
    }

}
</script>


<style scoped>
.col {
    margin: 10px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.item-container {
    padding: 5px;
    margin: 5px;
}

.slider {
    display: block;
}

.block {
    padding: 5px;
    margin: 5px;
    display: inline-block;
}

.fractalsContainer {
    margin: 10px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.container {
    display: flex;
}
</style>