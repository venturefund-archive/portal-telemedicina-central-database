<template><div><h1 id="getting-started-with-the-frontend" tabindex="-1"><a class="header-anchor" href="#getting-started-with-the-frontend"><span>Getting Started with the Frontend</span></a></h1>
<p>Welcome to the frontend of the Child Health Tracker project! This guide will help you set up and run the frontend on your local machine.</p>
<h2 id="prerequisites" tabindex="-1"><a class="header-anchor" href="#prerequisites"><span>Prerequisites</span></a></h2>
<p>Before you begin, ensure you have the following installed:</p>
<ul>
<li>Node.js 14 or higher</li>
<li>npm 6 or higher</li>
</ul>
<h2 id="installation" tabindex="-1"><a class="header-anchor" href="#installation"><span>Installation</span></a></h2>
<ol>
<li>
<p>Navigate to the frontend directory:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text" data-title="text"><pre v-pre><code><span class="line">cd frontend</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></li>
<li>
<p>Install dependencies:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text" data-title="text"><pre v-pre><code><span class="line">npm install</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></li>
</ol>
<h2 id="running-the-development-server" tabindex="-1"><a class="header-anchor" href="#running-the-development-server"><span>Running the Development Server</span></a></h2>
<p>To start the frontend development server:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text" data-title="text"><pre v-pre><code><span class="line">npm run dev</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>This will start the server and automatically open your default browser to <code v-pre>http://localhost:5173</code> (or another port if 5173 is in use).</p>
<h2 id="building-for-production" tabindex="-1"><a class="header-anchor" href="#building-for-production"><span>Building for Production</span></a></h2>
<p>To create a production build:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text" data-title="text"><pre v-pre><code><span class="line">npm run build</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>This will generate optimized files in the <code v-pre>dist</code> directory.</p>
<h2 id="running-tests" tabindex="-1"><a class="header-anchor" href="#running-tests"><span>Running Tests</span></a></h2>
<p>To run unit tests:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text" data-title="text"><pre v-pre><code><span class="line">npm run test:unit</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>For end-to-end tests:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text" data-title="text"><pre v-pre><code><span class="line">npm run test:e2e</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="linting" tabindex="-1"><a class="header-anchor" href="#linting"><span>Linting</span></a></h2>
<p>To lint your code:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text" data-title="text"><pre v-pre><code><span class="line">npm run lint</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="project-structure" tabindex="-1"><a class="header-anchor" href="#project-structure"><span>Project Structure</span></a></h2>
<ul>
<li><code v-pre>src/</code>: Contains the source code
<ul>
<li><code v-pre>components/</code>: Vue components</li>
<li><code v-pre>views/</code>: Vue views (pages)</li>
<li><code v-pre>router/</code>: Vue Router configuration</li>
<li><code v-pre>store/</code>: Vuex store (if used)</li>
<li><code v-pre>assets/</code>: Static assets like images and fonts</li>
</ul>
</li>
<li><code v-pre>public/</code>: Public files that are copied to the build directory</li>
</ul>
<h2 id="next-steps" tabindex="-1"><a class="header-anchor" href="#next-steps"><span>Next Steps</span></a></h2>
<ul>
<li>Explore the <code v-pre>src</code> directory to understand the project structure</li>
<li>Check out the <a href="https://vuejs.org/guide/introduction.html" target="_blank" rel="noopener noreferrer">Vue.js documentation</a> for more information on Vue 3</li>
<li>Review the <a href="https://vitejs.dev/guide/" target="_blank" rel="noopener noreferrer">Vite documentation</a> to learn about the build tool</li>
</ul>
<p>If you encounter any issues or have questions, please refer to our project's main README or open an issue on GitHub.</p>
<p>Happy coding!</p>
</div></template>


