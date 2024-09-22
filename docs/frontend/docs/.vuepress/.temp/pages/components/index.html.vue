<template><div><h1 id="components" tabindex="-1"><a class="header-anchor" href="#components"><span>Components</span></a></h1>
<p>This directory contains the Vue components used in the Child Development Analyzer frontend application. The components are organized into different categories based on their complexity and purpose.</p>
<h2 id="directory-structure" tabindex="-1"><a class="header-anchor" href="#directory-structure"><span>Directory Structure</span></a></h2>
<p>The components are organized into the following subdirectories:</p>
<ul>
<li><code v-pre>atoms/</code>: Basic building blocks of the application</li>
<li><code v-pre>molecules/</code>: Combinations of atoms to form more complex UI elements</li>
<li><code v-pre>organisms/</code>: Complex components that combine multiple molecules and atoms</li>
<li><code v-pre>icons/</code>: SVG icons used throughout the application</li>
</ul>
<h2 id="key-components" tabindex="-1"><a class="header-anchor" href="#key-components"><span>Key Components</span></a></h2>
<h3 id="atoms" tabindex="-1"><a class="header-anchor" href="#atoms"><span>Atoms</span></a></h3>
<ol>
<li><code v-pre>Button.vue</code>: A reusable button component with various styles and variants.</li>
<li><code v-pre>Input.vue</code>: A customizable input component.</li>
<li><code v-pre>Logo.vue</code>: Displays the UNICEF logo.</li>
<li><code v-pre>VaccineAlertInfo.vue</code>: Shows vaccine alert information.</li>
</ol>
<h3 id="organisms" tabindex="-1"><a class="header-anchor" href="#organisms"><span>Organisms</span></a></h3>
<ol>
<li><code v-pre>Navbar.vue</code>: The main navigation bar component.</li>
<li><code v-pre>PatientListCard.vue</code>: Displays patient information in a card format.</li>
</ol>
<h3 id="sidebar" tabindex="-1"><a class="header-anchor" href="#sidebar"><span>Sidebar</span></a></h3>
<p>The sidebar components are crucial for the application's layout:</p>
<ol>
<li><code v-pre>Sidebar.vue</code>: The main sidebar component that includes the header, content, and footer.</li>
<li><code v-pre>SidebarContent.vue</code>: Contains the main navigation links.</li>
<li><code v-pre>SidebarFooter.vue</code>: Displays information at the bottom of the sidebar.</li>
<li><code v-pre>SidebarHeader.vue</code>: Shows the logo and other header information.</li>
</ol>
<h3 id="icons" tabindex="-1"><a class="header-anchor" href="#icons"><span>Icons</span></a></h3>
<p>Custom icon components are defined in the <code v-pre>icons/outline.jsx</code> file. These include:</p>
<ul>
<li><code v-pre>MenuFoldLineRightIcon</code></li>
<li><code v-pre>MenuFoldLineLeftIcon</code></li>
<li><code v-pre>DashboardIcon</code></li>
</ul>
<h2 id="usage" tabindex="-1"><a class="header-anchor" href="#usage"><span>Usage</span></a></h2>
<p>Components are typically imported and used in Vue files. For example:</p>
<div class="language-vue line-numbers-mode" data-highlighter="prismjs" data-ext="vue" data-title="vue"><pre v-pre><code><span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>template</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>Navbar</span> <span class="token punctuation">/></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>Sidebar</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>SidebarContent</span> <span class="token punctuation">/></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>SidebarFooter</span> <span class="token punctuation">/></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>Sidebar</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>Button</span> <span class="token attr-name">variant</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>primary<span class="token punctuation">"</span></span><span class="token punctuation">></span></span>Click me<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>Button</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>template</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>script</span> <span class="token attr-name">setup</span><span class="token punctuation">></span></span><span class="token script"><span class="token language-javascript"></span>
<span class="line"><span class="token keyword">import</span> Navbar <span class="token keyword">from</span> <span class="token string">'@/components/organisms/Navbar.vue'</span></span>
<span class="line"><span class="token keyword">import</span> Sidebar <span class="token keyword">from</span> <span class="token string">'@/components/sidebar/Sidebar.vue'</span></span>
<span class="line"><span class="token keyword">import</span> SidebarContent <span class="token keyword">from</span> <span class="token string">'@/components/sidebar/SidebarContent.vue'</span></span>
<span class="line"><span class="token keyword">import</span> SidebarFooter <span class="token keyword">from</span> <span class="token string">'@/components/sidebar/SidebarFooter.vue'</span></span>
<span class="line"><span class="token keyword">import</span> Button <span class="token keyword">from</span> <span class="token string">'@/components/atoms/Button.vue'</span></span>
<span class="line"></span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>script</span><span class="token punctuation">></span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="styling" tabindex="-1"><a class="header-anchor" href="#styling"><span>Styling</span></a></h2>
<p>The components use Tailwind CSS for styling. Custom styles are defined in the <code v-pre>frontend/src/tailwind.css</code> file and the Tailwind configuration is in <code v-pre>frontend/tailwind.config.js</code>.</p>
<h2 id="state-management" tabindex="-1"><a class="header-anchor" href="#state-management"><span>State Management</span></a></h2>
<p>Some components interact with the Pinia stores located in <code v-pre>frontend/src/stores/</code>. For example, the <code v-pre>Navbar.vue</code> component uses the <code v-pre>useLoggedUserStore</code> to display user information.</p>
<h2 id="internationalization" tabindex="-1"><a class="header-anchor" href="#internationalization"><span>Internationalization</span></a></h2>
<p>The components support internationalization using the Vue I18n plugin. Translations are stored in JSON files in the <code v-pre>frontend/src/locales/</code> directory.</p>
<h2 id="contributing" tabindex="-1"><a class="header-anchor" href="#contributing"><span>Contributing</span></a></h2>
<p>When adding new components or modifying existing ones, please follow these guidelines:</p>
<ol>
<li>Use appropriate naming conventions (PascalCase for component names).</li>
<li>Place components in the correct subdirectory based on their complexity.</li>
<li>Use Tailwind CSS classes for styling when possible.</li>
<li>Ensure components are responsive and accessible.</li>
<li>Add appropriate props and emit events for component communication.</li>
<li>Document any complex logic or important information in comments.</li>
</ol>
<p>For more detailed information on the project structure and development guidelines, please refer to the main project README and CONTRIBUTING files.</p>
</div></template>


