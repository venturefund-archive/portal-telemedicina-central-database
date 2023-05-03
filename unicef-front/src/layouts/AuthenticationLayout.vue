<template>
  <div class="">
    <div class="flex justify-center">
      <div class="relative z-10 hidden bg-cover lg:block lg:w-2/3" style="background-image: url(/unicef_bg.jpg)">
        <div class="flex h-full items-center px-20">
          <div>
            <div class="overlay"></div>
            <h1 class="hidden">UNICEF</h1>
            <!--     <h2 class="text-4xl font-bold text-white">Brand</h2>

                        <p class="max-w-xl mt-3 text-gray-300">Lorem ipsum dolor sit, amet consectetur adipisicing elit.
                            In autem ipsa, nulla laboriosam dolores, repellendus perferendis libero suscipit nam
                            temporibus molestiae</p> -->
          </div>
        </div>
      </div>

      <div class="z-10 mx-auto flex min-h-screen w-full max-w-md flex-col items-center lg:w-2/6">
        <div class="flex justify-center pt-32">
          <div class="-ml-10 flex-shrink-0">
            <router-link to="/">
              <img src="@/assets/portal_logo.png" alt="unicef logo" class="h-16" />
              <span class="sr-only">Dashboard</span>
            </router-link>
          </div>
        </div>
        <main class="flex w-full flex-1 items-center sm:max-w-md">
          <div class="w-full overflow-hidden bg-white px-6 py-4 sm:rounded-lg">
            <div class="flex justify-center py-5">
              <LanguageSwitcher />
            </div>
            <router-view></router-view>
          </div>
        </main>
        <!-- <PageFooter /> -->

        <!-- <p class="mt-6 text-sm text-center text-gray-400">Ainda não esta cadastrado? <a href="#"
                              class="text-blue-500 focus:outline-none focus:underline hover:underline">Cadastrar</a>.
                      </p> -->
      </div>
    </div>
  </div>
</template>
<style type="text/css">
.overlay {
  position: absolute;
  top: 0;
  right: -32%;
  width: 50%;
  height: 100%;
  clip-path: ellipse(25% 70% at 50% 50%);
  background-color: white;
  overflow: hidden;
  z-index: 1;
}
</style>
