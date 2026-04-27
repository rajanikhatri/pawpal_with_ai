export const PET_PROFILE_KEY = "pawpal_pet_profile"

export function getPetProfile() {
  try {
    return JSON.parse(
      localStorage.getItem(PET_PROFILE_KEY) ?? "{}"
    )
  } catch {
    return {}
  }
}

export function formatAge(petProfile) {
  const ageYears = Number(petProfile.ageYears || 0)
  const ageMonths = Number(petProfile.ageMonths || 0)
  if (ageYears > 0 && ageMonths > 0) return `${ageYears} yr ${ageMonths} mo`
  if (ageYears > 0) return `${ageYears} yr`
  if (ageMonths > 0) return `${ageMonths} mo`
  return "Age not set"
}
