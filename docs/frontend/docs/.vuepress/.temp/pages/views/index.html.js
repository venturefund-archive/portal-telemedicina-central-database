import comp from "/app/docs/.vuepress/.temp/pages/views/index.html.vue"
const data = JSON.parse("{\"path\":\"/views/\",\"title\":\"Views\",\"lang\":\"en-US\",\"frontmatter\":{},\"headers\":[{\"level\":2,\"title\":\"Directory Structure\",\"slug\":\"directory-structure\",\"link\":\"#directory-structure\",\"children\":[]},{\"level\":2,\"title\":\"Key Views\",\"slug\":\"key-views\",\"link\":\"#key-views\",\"children\":[]},{\"level\":2,\"title\":\"Router Integration\",\"slug\":\"router-integration\",\"link\":\"#router-integration\",\"children\":[]},{\"level\":2,\"title\":\"State Management\",\"slug\":\"state-management\",\"link\":\"#state-management\",\"children\":[]},{\"level\":2,\"title\":\"Internationalization\",\"slug\":\"internationalization\",\"link\":\"#internationalization\",\"children\":[]},{\"level\":2,\"title\":\"Styling\",\"slug\":\"styling\",\"link\":\"#styling\",\"children\":[]},{\"level\":2,\"title\":\"Best Practices\",\"slug\":\"best-practices\",\"link\":\"#best-practices\",\"children\":[]},{\"level\":2,\"title\":\"Example View Structure\",\"slug\":\"example-view-structure\",\"link\":\"#example-view-structure\",\"children\":[]}],\"git\":{},\"filePathRelative\":\"views/README.md\"}")
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
