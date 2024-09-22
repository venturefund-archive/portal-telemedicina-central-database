export const themeData = JSON.parse("{\"navbar\":[{\"text\":\"Home\",\"link\":\"/\"},{\"text\":\"Getting Started\",\"link\":\"/getting-started.html\"},{\"text\":\"Components\",\"link\":\"/components/\"},{\"text\":\"Views\",\"link\":\"/views/\"},{\"text\":\"State Management\",\"link\":\"/state-management.html\"},{\"text\":\"API Integration\",\"link\":\"/api-integration.html\"}],\"sidebar\":[\"/\",\"/getting-started\",{\"text\":\"Components\",\"children\":[\"/components/\",\"/components/component1\",\"/components/component2\"]},{\"text\":\"Views\",\"children\":[\"/views/\",\"/views/view1\",\"/views/view2\"]},\"/state-management\",\"/api-integration\"],\"locales\":{\"/\":{\"selectLanguageName\":\"English\"}},\"colorMode\":\"auto\",\"colorModeSwitch\":true,\"logo\":null,\"repo\":null,\"selectLanguageText\":\"Languages\",\"selectLanguageAriaLabel\":\"Select language\",\"sidebarDepth\":2,\"editLink\":true,\"editLinkText\":\"Edit this page\",\"lastUpdated\":true,\"lastUpdatedText\":\"Last Updated\",\"contributors\":true,\"contributorsText\":\"Contributors\",\"notFound\":[\"There's nothing here.\",\"How did we get here?\",\"That's a Four-Oh-Four.\",\"Looks like we've got some broken links.\"],\"backToHome\":\"Take me home\",\"openInNewWindow\":\"open in new window\",\"toggleColorMode\":\"toggle color mode\",\"toggleSidebar\":\"toggle sidebar\"}")

if (import.meta.webpackHot) {
  import.meta.webpackHot.accept()
  if (__VUE_HMR_RUNTIME__.updateThemeData) {
    __VUE_HMR_RUNTIME__.updateThemeData(themeData)
  }
}

if (import.meta.hot) {
  import.meta.hot.accept(({ themeData }) => {
    __VUE_HMR_RUNTIME__.updateThemeData(themeData)
  })
}
