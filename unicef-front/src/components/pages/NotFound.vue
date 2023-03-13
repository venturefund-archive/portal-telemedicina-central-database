<template>
  <div
    class="flex items-center justify-center gap-16 px-4 py-24 md:gap-28 md:py-20 md:px-44 lg:flex-row lg:px-24 lg:py-24"
  >
    <div class="relative w-full pb-12 lg:pb-0 xl:w-1/2 xl:pt-24">
      <div class="relative">
        <div class="absolute">
          <div class="">
            <h1 class="my-2 text-2xl font-bold text-gray-800">{{ $t('dashboard.ops-something-went-wrong') }}</h1>
            <p class="my-2 text-gray-800">{{ $t('dashboard.sorry') }}</p>
            <div class="mt-10 flex justify-center">
              <a
                href="/"
                class="md my-2 rounded border bg-blue-600 py-4 px-8 text-center text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:ring-opacity-50 sm:w-full lg:w-auto"
                >{{ $t('dashboard.take-me-there') }}</a
              >
            </div>
          </div>
        </div>
        <div>
          <img src="" />
        </div>
      </div>
    </div>
  </div>
</template>
