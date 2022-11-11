<template>
  <div class="w-[30rem] rounded-xl border-2 border-b-4 border-gray-200 hover:bg-gray-50">
    <div class="grid grid-cols-6 gap-y-2 p-5">
      <div>
        <img src="https://picsum.photos/seed/2/200/200" class="max-w-20 max-h-20 rounded-full" />
      </div>

      <div class="col-span-5 ml-4 md:col-span-4">
        <p class="cursor-pointer font-bold text-gray-600 hover:underline">Joana Freitas Silva</p>
        <div class="text-gray-400">
          <p>Blood Type: <span class="cursor-pointer hover:underline">B+</span></p>
          <p>Document: <span class="cursor-pointer hover:underline">064.964.967-53</span></p>
          <p>Region: <span class="cursor-pointer hover:underline">Minas South</span></p>
          <p>Contact: <span class="cursor-pointer hover:underline">(00) 00 000-000</span></p>
        </div>
      </div>
      <div class="col-start-2 ml-4 flex md:col-start-auto md:ml-0 md:justify-end">
        <p class="h-fit w-fit rounded-lg bg-sky-200 py-1 px-3 text-sm font-bold text-sky-600">Age:06</p>
      </div>
    </div>
  </div>
</template>
