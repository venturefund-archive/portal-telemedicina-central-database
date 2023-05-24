<template>
  <PageWrapper>
    <div class="flex flex-col items-center justify-center p-20">
    <img src="@/assets/images/search-patient.png" class="w-64 h-64" />
      <p class="font-semibold">{{ $t('patient-details.no-selected') }}</p>
      <form class="flex w-full flex-col items-center justify-center pt-16 sm:w-96">
        <span class="py-3">{{ $t('patient-details.no-patient-selected-text') }}</span>
        <label for="default-search" class="sr-only mb-2 text-sm font-medium text-gray-900">Procurar</label>
        <InputIconWrapper>
          <template #icon>
            <SearchIcon aria-hidden="true" class="h-5 w-5" />
          </template>
          <AutoComplete class="w-96" is-in-page v-model="queryText" :suggestions="filteredResults" />
        </InputIconWrapper>
      </form>
    </div>

    <!-- <VaccinesList id="0" /> -->
  </PageWrapper>
</template>

<script setup>
import { SunIcon, MoonIcon, SearchIcon, LogoutIcon, MenuIcon, XIcon, ArrowsExpandIcon } from '@heroicons/vue/outline'
import { onMounted, ref, computed } from 'vue'
import { useVaccinesStore } from '@/stores/vaccines'
import { useDosesStore } from '@/stores/doses'
import { useLoggedUserStore } from '@/stores/loggedUser'
import { usePatientsStore } from '@/stores/patients'
const loggedUserStore = useLoggedUserStore()
const dosesStore = useDosesStore()
const vaccinesStore = useVaccinesStore()
const patientsStore = usePatientsStore()
const queryText = ref('')

const filteredResults = computed(() => {
  if (queryText.value === '') {
    return []
  }

  let matches = 0

  return patientsStore.items.filter((patient) => {
    if (
      (patient.name.toLowerCase().includes(queryText.value.toLowerCase()) ||
        patient.id.toLowerCase().includes(queryText.value.toLowerCase())) &&
      matches < 10
    ) {
      matches++
      return patient
    }
  })
})

onMounted(async () => {
  // if (0 == vaccinesStore.items.length) {
  //   const vaccineResponse = await vaccinesStore.fetchVaccines()
  // }
  // await dosesStore.fetchDoses()
  loggedUserStore.isLoading = false
})
</script>
