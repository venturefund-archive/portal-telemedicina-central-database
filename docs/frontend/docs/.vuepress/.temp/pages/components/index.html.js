import comp from "/app/docs/.vuepress/.temp/pages/components/index.html.vue"
const data = JSON.parse("{\"path\":\"/components/\",\"title\":\"Components\",\"lang\":\"en-US\",\"frontmatter\":{},\"headers\":[{\"level\":2,\"title\":\"Directory Structure\",\"slug\":\"directory-structure\",\"link\":\"#directory-structure\",\"children\":[]},{\"level\":2,\"title\":\"Key Components\",\"slug\":\"key-components\",\"link\":\"#key-components\",\"children\":[{\"level\":3,\"title\":\"Atoms\",\"slug\":\"atoms\",\"link\":\"#atoms\",\"children\":[]},{\"level\":3,\"title\":\"Organisms\",\"slug\":\"organisms\",\"link\":\"#organisms\",\"children\":[]},{\"level\":3,\"title\":\"Sidebar\",\"slug\":\"sidebar\",\"link\":\"#sidebar\",\"children\":[]},{\"level\":3,\"title\":\"Icons\",\"slug\":\"icons\",\"link\":\"#icons\",\"children\":[]}]},{\"level\":2,\"title\":\"Usage\",\"slug\":\"usage\",\"link\":\"#usage\",\"children\":[]},{\"level\":2,\"title\":\"Styling\",\"slug\":\"styling\",\"link\":\"#styling\",\"children\":[]},{\"level\":2,\"title\":\"State Management\",\"slug\":\"state-management\",\"link\":\"#state-management\",\"children\":[]},{\"level\":2,\"title\":\"Internationalization\",\"slug\":\"internationalization\",\"link\":\"#internationalization\",\"children\":[]},{\"level\":2,\"title\":\"Contributing\",\"slug\":\"contributing\",\"link\":\"#contributing\",\"children\":[]}],\"git\":{},\"filePathRelative\":\"components/README.md\"}")
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
