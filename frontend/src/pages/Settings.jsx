import {
  Bell,
  Calendar,
  DollarSign,
  Dumbbell,
  Home,
  MessageCircle,
  Settings as SettingsIcon,
} from "lucide-react"
import { NavLink, useNavigate } from "react-router-dom"

import { cn } from "@/lib/utils"

const navItems = [
  { label: "Home", to: "/dashboard", icon: Home },
  { label: "AI Chat", to: "/ai", icon: MessageCircle },
  { label: "Training", to: "/training", icon: Dumbbell },
  { label: "Settings", to: "/settings", icon: SettingsIcon },
]

const comingSoonFeatures = [
  {
    icon: Calendar,
    title: "Owner Calendar",
    description: "Sync your schedule to avoid conflicts with pet care tasks",
  },
  {
    icon: DollarSign,
    title: "Vet Expenses",
    description: "Track vet visits, medications, and pet care costs in one place",
  },
  {
    icon: Bell,
    title: "Food Recall Alerts",
    description: "Get notified if your pet food brand has a safety recall",
  },
]

function BottomNavigation() {
  return (
    <nav className="fixed inset-x-0 bottom-0 border-t border-gray-100 bg-white/95 px-4 py-2 shadow-[0_-8px_24px_rgba(17,24,39,0.06)] backdrop-blur">
      <div className="mx-auto grid max-w-2xl grid-cols-4">
        {navItems.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                cn(
                  "flex flex-col items-center gap-1 rounded-lg px-2 py-2 text-xs font-medium transition",
                  isActive ? "text-[#4F7942]" : "text-gray-400"
                )
              }
            >
              <Icon className="h-5 w-5" aria-hidden="true" />
              <span>{item.label}</span>
            </NavLink>
          )
        })}
      </div>
    </nav>
  )
}

function formatAge(petProfile) {
  const ageYears = Number(petProfile.ageYears || 0)
  const ageMonths = Number(petProfile.ageMonths || 0)

  if (ageYears > 0 && ageMonths > 0) {
    return `${ageYears} yr ${ageMonths} mo`
  }

  if (ageYears > 0) {
    return `${ageYears} yr`
  }

  if (ageMonths > 0) {
    return `${ageMonths} mo`
  }

  return "Age not set"
}

function FeatureCard({ feature }) {
  const Icon = feature.icon

  return (
    <article className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
      <div className="flex items-start gap-3">
        <div className="rounded-lg bg-[#EAF3DE] p-2 text-[#4F7942]">
          <Icon className="h-5 w-5" aria-hidden="true" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-3">
            <h3 className="font-medium text-gray-900">{feature.title}</h3>
            <span className="shrink-0 rounded-full bg-[#FAEEDA] px-2 py-0.5 text-xs text-[#854F0B]">
              Coming Soon
            </span>
          </div>
          <p className="mt-1 text-sm leading-6 text-gray-600">{feature.description}</p>
        </div>
      </div>
    </article>
  )
}

export default function Settings() {
  const navigate = useNavigate()
  const petProfile = JSON.parse(localStorage.getItem("pawpal_pet_profile") ?? "{}")
  const petType = petProfile.petType || "Dog"
  const petEmoji = petType === "Cat" ? "🐱" : "🐶"
  const petName = petProfile.petName || "Your pet"
  const breed = petProfile.breed || "Breed not set"
  const age = formatAge(petProfile)
  const sex = petProfile.sex || "Sex not set"

  const handleEditProfile = () => {
    window.alert("Edit profile coming soon")
  }

  const handleResetApp = () => {
    localStorage.removeItem("pawpal_pet_profile")
    navigate("/")
  }

  return (
    <main className="min-h-screen bg-[#FAFAF8] px-4 py-6 pb-24 text-gray-900 sm:px-6">
      <div className="mx-auto flex max-w-2xl flex-col gap-5">
        <header>
          <h1 className="text-3xl font-semibold tracking-tight text-gray-900">Settings</h1>
          <p className="mt-1 text-sm text-gray-500">Manage your pet profile</p>
        </header>

        <section className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between gap-4">
            <h2 className="font-medium text-gray-900">Pet Profile</h2>
            <button
              type="button"
              onClick={handleEditProfile}
              className="rounded-lg bg-[#4F7942] px-3 py-1.5 text-sm font-medium text-white transition hover:bg-[#426738]"
            >
              Edit Profile
            </button>
          </div>

          <div className="mt-5 flex items-center gap-3">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-[#4F7942] text-3xl">
              {petEmoji}
            </div>
            <div className="min-w-0">
              <h3 className="truncate text-lg font-semibold text-gray-900">{petName}</h3>
              <p className="truncate text-sm text-gray-500">{breed}</p>
            </div>
          </div>

          <div className="mt-4 rounded-lg bg-[#FAFAF8] px-4 py-3 text-sm text-gray-600">
            {age} · {sex}
          </div>
        </section>

        <section>
          <h2 className="mb-4 font-medium text-gray-900">Coming Soon</h2>
          <div className="space-y-3">
            {comingSoonFeatures.map((feature) => (
              <FeatureCard key={feature.title} feature={feature} />
            ))}
          </div>
        </section>

        <section>
          <h2 className="mb-4 font-medium text-gray-900">Account</h2>
          <button
            type="button"
            onClick={handleResetApp}
            className="w-full rounded-xl border border-red-200 bg-white p-4 text-sm font-medium text-red-500 transition hover:bg-red-50"
          >
            Reset App
          </button>
        </section>
      </div>

      <BottomNavigation />
    </main>
  )
}
