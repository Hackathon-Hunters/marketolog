import { defineComponent, h } from 'vue'

// Базовый компонент карусели
export const Carousel = defineComponent({
  name: 'Carousel',
  setup(_, { slots }) {
    return () => h('div', { class: 'relative w-full' }, slots.default?.())
  }
})

// Контент карусели
export const CarouselContent = defineComponent({
  name: 'CarouselContent',
  setup(_, { slots }) {
    return () => h('div', { 
      class: 'relative flex overflow-hidden snap-x snap-mandatory' 
    }, slots.default?.())
  }
})

// Элемент карусели
export const CarouselItem = defineComponent({
  name: 'CarouselItem',
  props: {
    class: { type: String, default: '' }
  },
  setup(props, { slots }) {
    return () => h('div', { 
      class: `flex-shrink-0 flex-grow-0 snap-center p-4 w-full ${props.class}` 
    }, slots.default?.())
  }
})

// Кнопка "Предыдущий"
export const CarouselPrevious = defineComponent({
  name: 'CarouselPrevious',
  setup() {
    return () => h('button', { 
      class: 'absolute flex items-center justify-center h-8 w-8 rounded-full bg-white shadow-md border border-gray-200 left-2 top-1/2 -translate-y-1/2 z-10',
      onClick: () => {
        // Логика для прокрутки к предыдущему элементу
        const content = document.querySelector('.snap-x.snap-mandatory')
        if (content) {
          content.scrollBy({ left: -content.clientWidth, behavior: 'smooth' })
        }
      }
    }, [
      h('span', { class: 'sr-only' }, 'Предыдущий'), 
      h('svg', { 
        xmlns: 'http://www.w3.org/2000/svg', 
        fill: 'none', 
        viewBox: '0 0 24 24', 
        stroke: 'currentColor',
        class: 'h-4 w-4'
      }, [
        h('path', { 
          'stroke-linecap': 'round', 
          'stroke-linejoin': 'round', 
          'stroke-width': 2, 
          d: 'M15 19l-7-7 7-7' 
        })
      ])
    ])
  }
})

// Кнопка "Следующий"
export const CarouselNext = defineComponent({
  name: 'CarouselNext',
  setup() {
    return () => h('button', { 
      class: 'absolute flex items-center justify-center h-8 w-8 rounded-full bg-white shadow-md border border-gray-200 right-2 top-1/2 -translate-y-1/2 z-10',
      onClick: () => {
        // Логика для прокрутки к следующему элементу
        const content = document.querySelector('.snap-x.snap-mandatory')
        if (content) {
          content.scrollBy({ left: content.clientWidth, behavior: 'smooth' })
        }
      }
    }, [
      h('span', { class: 'sr-only' }, 'Следующий'), 
      h('svg', { 
        xmlns: 'http://www.w3.org/2000/svg', 
        fill: 'none', 
        viewBox: '0 0 24 24', 
        stroke: 'currentColor',
        class: 'h-4 w-4'
      }, [
        h('path', { 
          'stroke-linecap': 'round', 
          'stroke-linejoin': 'round', 
          'stroke-width': 2, 
          d: 'M9 5l7 7-7 7' 
        })
      ])
    ])
  }
})