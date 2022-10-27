<template>
  <div class="">
    <div class="flex justify-center">
      <div class="hidden relative bg-cover lg:block lg:w-2/3 z-10" style="background-image: url(unicef_bg.jpg)">
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
      

      <div class="mx-auto flex w-full max-w-md items-center lg:w-2/6 z-10">
        <div class="flex-1">
          <div class="">
            <div class="flex min-h-screen flex-col items-center justify-center gap-4 py-6">
              <div class="flex-shrink-0 -ml-10">
                <router-link :to="{ name: 'Dashboard' }">
                  <LogoFull class="h-16" />
                  <span class="sr-only">Dashboard</span>
                </router-link>
              </div>

              <main class="flex w-full flex-1 items-center sm:max-w-md">
                <div class="w-full overflow-hidden bg-white px-6 py-4 sm:rounded-lg">
                  <router-view></router-view>
                </div>
              </main>

              <!-- <PageFooter /> -->
            </div>

            <!-- <p class="mt-6 text-sm text-center text-gray-400">Ainda não esta cadastrado? <a href="#"
                                class="text-blue-500 focus:outline-none focus:underline hover:underline">Cadastrar</a>.
                        </p> -->
          </div>
        </div>
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
