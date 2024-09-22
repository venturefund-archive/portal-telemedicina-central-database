<template><div><h1 id="state-management" tabindex="-1"><a class="header-anchor" href="#state-management"><span>State Management</span></a></h1>
<p>This application uses Pinia for state management. Pinia is a store library for Vue, providing a straightforward and effective way to manage global state in the application.</p>
<h2 id="store-structure" tabindex="-1"><a class="header-anchor" href="#store-structure"><span>Store Structure</span></a></h2>
<p>The stores are located in the <code v-pre>frontend/src/stores</code> directory. Each store is responsible for managing a specific domain of the application. The main stores are:</p>
<ol>
<li><code v-pre>map.js</code>: Manages state related to map functionality.</li>
<li><code v-pre>patients.js</code>: Handles patient data and operations.</li>
<li><code v-pre>microregions.js</code>: Manages microregion data.</li>
<li><code v-pre>protocol.js</code>: Handles vaccine protocol data.</li>
<li><code v-pre>vaccines.js</code>: Manages vaccine-related state.</li>
<li><code v-pre>loggedUser.js</code>: Handles the logged-in user's state.</li>
<li><code v-pre>doses.js</code>: Manages vaccine doses data.</li>
</ol>
<h2 id="store-implementation" tabindex="-1"><a class="header-anchor" href="#store-implementation"><span>Store Implementation</span></a></h2>
<p>Each store is implemented using Pinia's <code v-pre>defineStore</code> function. The general structure of a store includes:</p>
<ul>
<li>State: Reactive data using <code v-pre>ref</code> or <code v-pre>reactive</code>.</li>
<li>Actions: Functions that can modify the state or perform asynchronous operations.</li>
<li>Getters: Computed properties based on the state (if needed).</li>
</ul>
<p>Here's an example of a typical store structure:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js" data-title="js"><pre v-pre><code><span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> defineStore <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'pinia'</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> ref <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'vue'</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> useStorage <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'@vueuse/core'</span></span>
<span class="line"><span class="token keyword">import</span> axios <span class="token keyword">from</span> <span class="token string">'axios'</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> errorToast <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'@/toast'</span></span>
<span class="line"><span class="token keyword">export</span> <span class="token keyword">const</span> useExampleStore <span class="token operator">=</span> <span class="token function">defineStore</span><span class="token punctuation">(</span><span class="token string">'example'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"><span class="token comment">// State</span></span>
<span class="line"><span class="token keyword">const</span> items <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">const</span> item <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token keyword">null</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token comment">// Actions</span></span>
<span class="line"><span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">fetchItems</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span></span>
<span class="line"><span class="token keyword">const</span> state <span class="token operator">=</span> <span class="token function">useStorage</span><span class="token punctuation">(</span><span class="token string">'app-store'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span> <span class="token literal-property property">token</span><span class="token operator">:</span> <span class="token string">''</span> <span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">try</span> <span class="token punctuation">{</span></span>
<span class="line"><span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span><span class="token keyword">import</span><span class="token punctuation">.</span>meta<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">VITE_API_URL</span> <span class="token operator">+</span> <span class="token string">'/api/items/'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span></span>
<span class="line"><span class="token literal-property property">headers</span><span class="token operator">:</span> <span class="token punctuation">{</span></span>
<span class="line"><span class="token string-property property">'Content-type'</span><span class="token operator">:</span> <span class="token string">'application/json'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token literal-property property">Authorization</span><span class="token operator">:</span> token $<span class="token punctuation">{</span>state<span class="token punctuation">.</span>value<span class="token punctuation">.</span>token<span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line">items<span class="token punctuation">.</span>value <span class="token operator">=</span> response<span class="token punctuation">.</span>data</span>
<span class="line"><span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>err<span class="token punctuation">)</span> <span class="token punctuation">{</span></span>
<span class="line"><span class="token function">errorToast</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">text</span><span class="token operator">:</span> err<span class="token punctuation">.</span>message <span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"><span class="token comment">// Return state and actions</span></span>
<span class="line"><span class="token keyword">return</span> <span class="token punctuation">{</span></span>
<span class="line">items<span class="token punctuation">,</span></span>
<span class="line">item<span class="token punctuation">,</span></span>
<span class="line">fetchItems<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="using-stores-in-components" tabindex="-1"><a class="header-anchor" href="#using-stores-in-components"><span>Using Stores in Components</span></a></h2>
<p>To use a store in a component:</p>
<ol>
<li>Import the store</li>
<li>Call the store function to get an instance</li>
<li>Use the state, actions, or getters from the store</li>
</ol>
<p>Example:</p>
<div class="language-vue line-numbers-mode" data-highlighter="prismjs" data-ext="vue" data-title="vue"><pre v-pre><code><span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>script</span> <span class="token attr-name">setup</span><span class="token punctuation">></span></span><span class="token script"><span class="token language-javascript"></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> useVaccinesStore <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'@/stores/vaccines'</span></span>
<span class="line"><span class="token keyword">const</span> vaccinesStore <span class="token operator">=</span> <span class="token function">useVaccinesStore</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token comment">// Use the store</span></span>
<span class="line">vaccinesStore<span class="token punctuation">.</span><span class="token function">fetchVaccines</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">console<span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>vaccinesStore<span class="token punctuation">.</span>items<span class="token punctuation">)</span></span>
<span class="line"></span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>script</span><span class="token punctuation">></span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="key-features" tabindex="-1"><a class="header-anchor" href="#key-features"><span>Key Features</span></a></h2>
<ul>
<li><strong>Centralized State Management</strong>: All global state is managed in one place, making it easier to track and update.</li>
<li><strong>TypeScript Support</strong>: Pinia provides excellent TypeScript support out of the box.</li>
<li><strong>Modular</strong>: Each store is a self-contained module, promoting code organization and reusability.</li>
<li><strong>DevTools Support</strong>: Pinia integrates with Vue DevTools, allowing for easy debugging and state inspection.</li>
<li><strong>Composition API</strong>: Stores are defined using the Composition API, aligning with Vue 3's preferred style.</li>
</ul>
<h2 id="best-practices" tabindex="-1"><a class="header-anchor" href="#best-practices"><span>Best Practices</span></a></h2>
<ol>
<li>Keep stores focused on a specific domain or feature.</li>
<li>Use actions for all state modifications, especially for asynchronous operations.</li>
<li>Leverage Vue's reactivity system by using <code v-pre>ref</code> and <code v-pre>reactive</code> for state.</li>
<li>Use the <code v-pre>useStorage</code> composable from VueUse for persisting state to local storage when needed.</li>
<li>Handle errors in actions and use toast notifications to inform users of issues.</li>
</ol>
<p>By following these patterns and best practices, the application maintains a clean and manageable state architecture, promoting scalability and maintainability.</p>
</div></template>


