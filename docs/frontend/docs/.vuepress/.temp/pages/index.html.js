import comp from "/app/docs/.vuepress/.temp/pages/index.html.vue"
const data = JSON.parse("{\"path\":\"/\",\"title\":\"Frontend Documentation\",\"lang\":\"en-US\",\"frontmatter\":{},\"headers\":[{\"level\":2,\"title\":\"Table of Contents\",\"slug\":\"table-of-contents\",\"link\":\"#table-of-contents\",\"children\":[]},{\"level\":2,\"title\":\"Project Setup\",\"slug\":\"project-setup\",\"link\":\"#project-setup\",\"children\":[]},{\"level\":2,\"title\":\"Components\",\"slug\":\"components\",\"link\":\"#components\",\"children\":[]},{\"level\":2,\"title\":\"Views\",\"slug\":\"views\",\"link\":\"#views\",\"children\":[]},{\"level\":2,\"title\":\"Testing\",\"slug\":\"testing\",\"link\":\"#testing\",\"children\":[]},{\"level\":2,\"title\":\"Linting\",\"slug\":\"linting\",\"link\":\"#linting\",\"children\":[]}],\"git\":{},\"filePathRelative\":\"README.md\"}")
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
