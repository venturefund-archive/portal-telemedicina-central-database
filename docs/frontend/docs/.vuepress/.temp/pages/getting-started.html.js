import comp from "/app/docs/.vuepress/.temp/pages/getting-started.html.vue"
const data = JSON.parse("{\"path\":\"/getting-started.html\",\"title\":\"Getting Started with the Frontend\",\"lang\":\"en-US\",\"frontmatter\":{},\"headers\":[{\"level\":2,\"title\":\"Prerequisites\",\"slug\":\"prerequisites\",\"link\":\"#prerequisites\",\"children\":[]},{\"level\":2,\"title\":\"Installation\",\"slug\":\"installation\",\"link\":\"#installation\",\"children\":[]},{\"level\":2,\"title\":\"Running the Development Server\",\"slug\":\"running-the-development-server\",\"link\":\"#running-the-development-server\",\"children\":[]},{\"level\":2,\"title\":\"Building for Production\",\"slug\":\"building-for-production\",\"link\":\"#building-for-production\",\"children\":[]},{\"level\":2,\"title\":\"Running Tests\",\"slug\":\"running-tests\",\"link\":\"#running-tests\",\"children\":[]},{\"level\":2,\"title\":\"Linting\",\"slug\":\"linting\",\"link\":\"#linting\",\"children\":[]},{\"level\":2,\"title\":\"Project Structure\",\"slug\":\"project-structure\",\"link\":\"#project-structure\",\"children\":[]},{\"level\":2,\"title\":\"Next Steps\",\"slug\":\"next-steps\",\"link\":\"#next-steps\",\"children\":[]}],\"git\":{},\"filePathRelative\":\"getting-started.md\"}")
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
