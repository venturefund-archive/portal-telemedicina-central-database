export const redirects = JSON.parse("{}")

export const routes = Object.fromEntries([
  ["/", { loader: () => import(/* webpackChunkName: "index.html" */"/app/docs/.vuepress/.temp/pages/index.html.js"), meta: {"title":"Frontend Documentation"} }],
  ["/getting-started.html", { loader: () => import(/* webpackChunkName: "getting-started.html" */"/app/docs/.vuepress/.temp/pages/getting-started.html.js"), meta: {"title":"Getting Started with the Frontend"} }],
  ["/state-management.html", { loader: () => import(/* webpackChunkName: "state-management.html" */"/app/docs/.vuepress/.temp/pages/state-management.html.js"), meta: {"title":"State Management"} }],
  ["/components/", { loader: () => import(/* webpackChunkName: "components_index.html" */"/app/docs/.vuepress/.temp/pages/components/index.html.js"), meta: {"title":"Components"} }],
  ["/views/", { loader: () => import(/* webpackChunkName: "views_index.html" */"/app/docs/.vuepress/.temp/pages/views/index.html.js"), meta: {"title":"Views"} }],
  ["/404.html", { loader: () => import(/* webpackChunkName: "404.html" */"/app/docs/.vuepress/.temp/pages/404.html.js"), meta: {"title":""} }],
]);

if (import.meta.webpackHot) {
  import.meta.webpackHot.accept()
  if (__VUE_HMR_RUNTIME__.updateRoutes) {
    __VUE_HMR_RUNTIME__.updateRoutes(routes)
  }
  if (__VUE_HMR_RUNTIME__.updateRedirects) {
    __VUE_HMR_RUNTIME__.updateRedirects(redirects)
  }
}

if (import.meta.hot) {
  import.meta.hot.accept(({ routes, redirects }) => {
    __VUE_HMR_RUNTIME__.updateRoutes(routes)
    __VUE_HMR_RUNTIME__.updateRedirects(redirects)
  })
}
