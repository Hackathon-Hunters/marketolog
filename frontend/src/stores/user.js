export const useCounterStore = defineStore('counter', {
    state: () => ({ user: null, company: null }),
    getters: {
        doubleCount: (state) => state.count * 2,
    },
    actions: {
        increment()
        {
            this.count++
        },
    },
})