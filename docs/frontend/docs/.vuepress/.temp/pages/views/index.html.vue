<template><div><h1 id="views" tabindex="-1"><a class="header-anchor" href="#views"><span>Views</span></a></h1>
<p>This directory contains the Vue components that represent entire pages or major sections of the application. These views are typically rendered by the router and may contain multiple smaller components.</p>
<h2 id="directory-structure" tabindex="-1"><a class="header-anchor" href="#directory-structure"><span>Directory Structure</span></a></h2>
<p>The views are organized in the <code v-pre>frontend/src/views</code> directory. Each view is a Vue component file (.vue) that represents a specific page or major section of the application.</p>
<h2 id="key-views" tabindex="-1"><a class="header-anchor" href="#key-views"><span>Key Views</span></a></h2>
<ol>
<li><code v-pre>HomeView.vue</code>: The main landing page of the application.</li>
<li><code v-pre>LoginView.vue</code>: Handles user authentication and login.</li>
<li><code v-pre>PatientDetailsView.vue</code>: Displays detailed information about a specific patient.</li>
<li><code v-pre>PatientListView.vue</code>: Shows a list of patients.</li>
<li><code v-pre>VaccineBookletView.vue</code>: Displays the vaccine booklet for a patient.</li>
</ol>
<h2 id="router-integration" tabindex="-1"><a class="header-anchor" href="#router-integration"><span>Router Integration</span></a></h2>
<p>These views are integrated with the Vue Router, which is configured in:</p>
<p><code v-pre>typescript:frontend/src/router/index.js</code></p>
<h2 id="state-management" tabindex="-1"><a class="header-anchor" href="#state-management"><span>State Management</span></a></h2>
<p>Views often interact with the Pinia stores to manage global state. The stores are located in:</p>
<p><code v-pre>typescript:frontend/src/stores</code></p>
<h2 id="internationalization" tabindex="-1"><a class="header-anchor" href="#internationalization"><span>Internationalization</span></a></h2>
<p>Views support internationalization using the Vue I18n plugin. Translations are stored in JSON files in the <code v-pre>frontend/src/locales/</code> directory.</p>
<h2 id="styling" tabindex="-1"><a class="header-anchor" href="#styling"><span>Styling</span></a></h2>
<p>Views use Tailwind CSS for styling. Custom styles are defined in:</p>
<p><code v-pre>css:frontend/src/tailwind.css</code></p>
<h2 id="best-practices" tabindex="-1"><a class="header-anchor" href="#best-practices"><span>Best Practices</span></a></h2>
<p>When creating or modifying views:</p>
<ol>
<li>Keep views focused on layout and composition of smaller components.</li>
<li>Use components from <code v-pre>@/components</code> for reusable UI elements.</li>
<li>Implement page-specific logic in the view or in a dedicated composable.</li>
<li>Use Pinia stores for managing global state.</li>
<li>Implement proper error handling and loading states.</li>
<li>Ensure responsive design using Tailwind CSS classes.</li>
<li>Use Vue Router for navigation between views.</li>
<li>Implement proper accessibility features (ARIA attributes, keyboard navigation, etc.).</li>
</ol>
<h2 id="example-view-structure" tabindex="-1"><a class="header-anchor" href="#example-view-structure"><span>Example View Structure</span></a></h2>
<p>Here's a basic structure of a view component:</p>
<div class="language-vue line-numbers-mode" data-highlighter="prismjs" data-ext="vue" data-title="vue"><pre v-pre><code><span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>template</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token comment">&lt;!-- Layout and composition of smaller components --></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>Header</span> <span class="token punctuation">/></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>main</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>ComponentA</span> <span class="token punctuation">/></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>ComponentB</span> <span class="token punctuation">/></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>main</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>Footer</span> <span class="token punctuation">/></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>template</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>script</span> <span class="token attr-name">setup</span><span class="token punctuation">></span></span><span class="token script"><span class="token language-javascript"></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> ref<span class="token punctuation">,</span> onMounted <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'vue'</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> useStore <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'@/stores/someStore'</span></span>
<span class="line"><span class="token keyword">import</span> Header <span class="token keyword">from</span> <span class="token string">'@/components/Header.vue'</span></span>
<span class="line"><span class="token keyword">import</span> Footer <span class="token keyword">from</span> <span class="token string">'@/components/Footer.vue'</span></span>
<span class="line"><span class="token keyword">import</span> ComponentA <span class="token keyword">from</span> <span class="token string">'@/components/ComponentA.vue'</span></span>
<span class="line"><span class="token keyword">import</span> ComponentB <span class="token keyword">from</span> <span class="token string">'@/components/ComponentB.vue'</span></span>
<span class="line"><span class="token keyword">const</span> store <span class="token operator">=</span> <span class="token function">useStore</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token comment">// View-specific logic</span></span>
<span class="line"><span class="token keyword">const</span> someData <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token keyword">null</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token function">onMounted</span><span class="token punctuation">(</span><span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"><span class="token comment">// Fetch data or perform other initialization</span></span>
<span class="line">someData<span class="token punctuation">.</span>value <span class="token operator">=</span> <span class="token keyword">await</span> store<span class="token punctuation">.</span><span class="token function">fetchSomeData</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"></span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>script</span><span class="token punctuation">></span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>For more detailed information on the project structure and development guidelines, please refer to the main project README and CONTRIBUTING files.</p>
</div></template>


