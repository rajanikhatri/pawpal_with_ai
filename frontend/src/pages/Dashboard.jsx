import { Dumbbell, Home, MessageCircle, Settings } from "lucide-react"
import { Link, NavLink } from "react-router-dom"

import { cn } from "@/lib/utils"

const taskItems = [
  {
    title: "Morning feeding",
    time: "7:00 AM",
    status: "done",
  },
  {
    title: "Potty break",
    time: "9:00 AM",
    status: "done",
  },
  {
    title: "Training session",
    time: "12:00 PM",
    subtitle: "Practice sit + stay · 10 min",
    status: "due",
  },
  {
    title: "Evening feeding",
    time: "6:00 PM",
    subtitle: "Puppy kibble · 1 cup",
    status: "upcoming",
  },
]

const navItems = [
  { label: "Home", to: "/dashboard", icon: Home },
  { label: "AI Chat", to: "/ai", icon: MessageCircle },
  { label: "Training", to: "/training", icon: Dumbbell },
  { label: "Settings", to: "/settings", icon: Settings },
]

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

function ageBadgeText(petProfile) {
  const ageYears = Number(petProfile.ageYears || 0)
  const ageMonths = Number(petProfile.ageMonths || 0)

  if (ageYears > 0 && ageMonths > 0) {
    return `${ageYears} yr ${ageMonths} mo old`
  }

  if (ageYears > 0) {
    return `${ageYears} yr old`
  }

  if (ageMonths > 0) {
    return `${ageMonths} months old`
  }

  return "Age not set"
}

function TaskStatusCircle({ status }) {
  if (status === "done") {
    return (
      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#4F7942]">
        <svg
          viewBox="0 0 20 20"
          fill="none"
          aria-hidden="true"
          className="h-4 w-4 text-white"
        >
          <path
            d="M5 10.5L8.2 13.5L15 6.5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    )
  }

  return (
    <div
      className={cn(
        "h-7 w-7 shrink-0 rounded-full border-2",
        status === "due" ? "border-[#4F7942]" : "border-gray-200"
      )}
    />
  )
}

function StatusBadge({ status }) {
  const label = status === "done" ? "Done" : status === "due" ? "Due" : "Upcoming"

  return (
    <span
      className={cn(
        "rounded-full px-2.5 py-1 text-xs font-medium",
        status === "done" && "bg-[#4F794215] text-[#4F7942]",
        status === "due" && "bg-[#FAEEDA] text-[#854F0B]",
        status === "upcoming" && "bg-gray-100 text-gray-400"
      )}
    >
      {label}
    </span>
  )
}

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

export default function Dashboard() {
  const petProfile = JSON.parse(localStorage.getItem("pawpal_pet_profile") ?? "{}")
  const petType = petProfile.petType || "Dog"
  const petEmoji = petType === "Cat" ? "🐱" : "🐶"
  const petName = petProfile.petName || "Your pet"
  const ageText = formatAge(petProfile)
  const subtitle = [petProfile.breed, ageText].filter(Boolean).join(" · ")
  const suggestion =
    petType === "Cat"
      ? "Kittens need feeding every 4-6 hours. Make sure fresh water is always available."
      : "Puppies need potty breaks every 2 hours. Consider adding a midday break around 1 PM."

  return (
    <main className="min-h-screen bg-[#FAFAF8] px-4 py-6 pb-24 text-gray-900 sm:px-6">
      <div className="mx-auto flex max-w-2xl flex-col gap-5">
        <section className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-full bg-[#4F7942] text-4xl">
              {petEmoji}
            </div>
            <div className="min-w-0 flex-1">
              <h1 className="truncate text-3xl font-semibold tracking-tight text-gray-900">
                {petName}
              </h1>
              <p className="mt-1 text-sm text-gray-500">{subtitle}</p>
              <div className="mt-3 inline-flex rounded-full bg-[#4F794215] px-3 py-1 text-xs font-medium text-[#4F7942]">
                {ageBadgeText(petProfile)}
              </div>
            </div>
          </div>
        </section>

        <section className="grid grid-cols-3 gap-3">
          <div className="rounded-xl border border-gray-100 bg-white p-4 text-center shadow-sm">
            <div className="text-2xl font-semibold text-[#4F7942]">4</div>
            <div className="mt-1 text-xs text-gray-500">Tasks today</div>
          </div>
          <div className="rounded-xl border border-gray-100 bg-white p-4 text-center shadow-sm">
            <div className="text-2xl font-semibold text-[#4F7942]">2</div>
            <div className="mt-1 text-xs text-gray-500">Completed</div>
          </div>
          <div className="rounded-xl border border-gray-100 bg-white p-4 text-center shadow-sm">
            <div className="text-2xl font-semibold text-[#4F7942]">5</div>
            <div className="mt-1 text-xs text-gray-500">Day streak</div>
          </div>
        </section>

        <section className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="mb-4 font-medium text-gray-900">Today's checklist</h2>
          <div className="space-y-4">
            {taskItems.map((task) => (
              <div key={`${task.title}-${task.time}`} className="flex items-start gap-3">
                <TaskStatusCircle status={task.status} />
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <h3
                        className={cn(
                          "text-sm font-medium",
                          task.status === "done"
                            ? "text-gray-400 line-through"
                            : "text-gray-900"
                        )}
                      >
                        {task.title}
                      </h3>
                      <p className="mt-0.5 text-xs text-gray-500">{task.time}</p>
                    </div>
                    <StatusBadge status={task.status} />
                  </div>
                  {task.subtitle && (
                    <p className="mt-1 text-sm text-gray-500">{task.subtitle}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-xl border border-gray-100 border-l-4 border-l-[#F4A261] bg-white p-5 shadow-sm">
          <p className="text-sm font-medium text-[#854F0B]">AI suggestion for {petName}</p>
          <p className="mt-2 text-sm leading-6 text-gray-600">{suggestion}</p>
          <Link
            to="/ai"
            className="mt-4 inline-flex text-sm font-medium text-[#4F7942] hover:text-[#426738]"
          >
            Ask AI assistant →
          </Link>
        </section>
      </div>

      <BottomNavigation />
    </main>
  )
}
