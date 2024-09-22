import comp from "/app/docs/.vuepress/.temp/pages/state-management.html.vue"
const data = JSON.parse("{\"path\":\"/state-management.html\",\"title\":\"State Management\",\"lang\":\"en-US\",\"frontmatter\":{},\"headers\":[{\"level\":2,\"title\":\"Store Structure\",\"slug\":\"store-structure\",\"link\":\"#store-structure\",\"children\":[]},{\"level\":2,\"title\":\"Store Implementation\",\"slug\":\"store-implementation\",\"link\":\"#store-implementation\",\"children\":[]},{\"level\":2,\"title\":\"Using Stores in Components\",\"slug\":\"using-stores-in-components\",\"link\":\"#using-stores-in-components\",\"children\":[]},{\"level\":2,\"title\":\"Key Features\",\"slug\":\"key-features\",\"link\":\"#key-features\",\"children\":[]},{\"level\":2,\"title\":\"Best Practices\",\"slug\":\"best-practices\",\"link\":\"#best-practices\",\"children\":[]}],\"git\":{},\"filePathRelative\":\"state-management.md\"}")
export { comp, data }

if (import.meta.webpackHot) {
  import.meta.webpackHot.accept()
  if (__VUE_HMR_RUNTIME__.updatePageData) {
    __VUE_HMR_RUNTIME__.updatePageData(data)
  }
}

if (import.meta.hot) {
  import.meta.hot.accept(({ data }) => {
    __VUE_HMR_RUNTIME__.updatePageData(data)
  })
}
