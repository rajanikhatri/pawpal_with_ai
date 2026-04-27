import { Dumbbell, Home, MessageCircle, Settings } from "lucide-react"
import { useState } from "react"
import { NavLink } from "react-router-dom"

import { cn } from "@/lib/utils"

const navItems = [
  { label: "Home", to: "/dashboard", icon: Home },
  { label: "AI Chat", to: "/ai", icon: MessageCircle },
  { label: "Training", to: "/training", icon: Dumbbell },
  { label: "Settings", to: "/settings", icon: Settings },
]

const initialSessions = [
  {
    id: 1,
    command: "Sit",
    duration: 10,
    date: "Today",
    notes: "Responded well, 8 out of 10 times",
    aiFeedback: "Great work! Sit is foundational. Once consistent, build on it with Stay.",
  },
  {
    id: 2,
    command: "Potty training",
    duration: 15,
    date: "Yesterday",
    notes: "Had 2 accidents inside",
    aiFeedback:
      "Accidents are normal at this stage. Try taking outside every 90 minutes and reward immediately after success outside.",
  },
]

const struggleGoalMap = {
  "Potty training": "Potty training",
  "Biting/chewing": "Bite inhibition",
  "Separation anxiety": "Alone time practice",
  "Feeding schedule": "Meal manners",
  "Not sure yet": "Basic commands",
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

function SessionCard({ session }) {
  return (
    <article className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-medium text-gray-900">{session.command}</h3>
          <p className="mt-1 text-xs text-gray-400">{session.date}</p>
        </div>
        <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-500">
          {session.duration} min
        </span>
      </div>

      <p className="mt-2 text-sm text-gray-600">{session.notes}</p>

      <div className="mt-4 border-t border-gray-100 pt-3">
        <div className="rounded-lg bg-[#EAF3DE] p-3">
          <div className="flex items-center gap-2 text-sm font-medium text-[#4F7942]">
            <span aria-hidden="true">🐾</span>
            <span>AI feedback</span>
          </div>
          <p className="mt-2 text-sm text-gray-600">{session.aiFeedback}</p>
        </div>
      </div>
    </article>
  )
}

export default function Training() {
  const petProfile = JSON.parse(localStorage.getItem("pawpal_pet_profile") ?? "{}")
  const petName = petProfile.petName || "your pet"
  const struggles = Array.isArray(petProfile.struggles) ? petProfile.struggles : []
  const focusGoals =
    struggles.length > 0
      ? struggles.map((struggle) => struggleGoalMap[struggle] || struggle).slice(0, 3)
      : ["Potty training", "Sit", "Stay"]
  const [showForm, setShowForm] = useState(false)
  const [successMessage, setSuccessMessage] = useState("")
  const [sessions, setSessions] = useState(initialSessions)
  const [formData, setFormData] = useState({
    command: "",
    duration: "",
    notes: "",
  })

  const updateFormData = (field, value) => {
    setFormData((currentData) => ({
      ...currentData,
      [field]: value,
    }))
  }

  const resetForm = () => {
    setFormData({
      command: "",
      duration: "",
      notes: "",
    })
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    const command = formData.command.trim()
    const duration = Number(formData.duration)
    const notes = formData.notes.trim()

    if (!command || !duration || duration < 1) {
      return
    }

    const session = {
      id: Date.now(),
      command,
      duration,
      notes,
      date: new Date().toLocaleDateString(),
      aiFeedback: `Great work! Consistency is key with ${command}. Try 2-3 short sessions per day for best results.`,
    }

    setSessions((currentSessions) => [session, ...currentSessions])
    setShowForm(false)
    resetForm()
    setSuccessMessage("Session saved.")

    window.setTimeout(() => {
      setSuccessMessage("")
    }, 2000)
  }

  const handleCancel = () => {
    setShowForm(false)
    resetForm()
  }

  return (
    <main className="min-h-screen bg-[#FAFAF8] px-4 py-6 pb-24 text-gray-900 sm:px-6">
      <div className="mx-auto flex max-w-2xl flex-col gap-5">
        <header className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-gray-900">
              Training Tracker
            </h1>
            <p className="mt-1 text-sm text-gray-500">Track {petName}'s progress</p>
          </div>
          <button
            type="button"
            onClick={() => setShowForm((visible) => !visible)}
            className="shrink-0 rounded-lg bg-[#4F7942] px-3 py-1.5 text-sm font-medium text-white transition hover:bg-[#426738]"
          >
            {showForm ? "Cancel" : "Log Session"}
          </button>
        </header>

        {successMessage && (
          <div className="rounded-lg border border-[#4F794230] bg-[#4F794215] px-4 py-3 text-sm font-medium text-[#4F7942]">
            {successMessage}
          </div>
        )}

        <section className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="font-medium text-gray-900">This week's focus</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            {focusGoals.map((goal) => (
              <span
                key={goal}
                className="rounded-full border border-[#4F794230] bg-[#4F794215] px-3 py-1 text-sm text-[#4F7942]"
              >
                {goal}
              </span>
            ))}
          </div>
        </section>

        {showForm && (
          <section className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Command practiced</label>
                <input
                  type="text"
                  value={formData.command}
                  onChange={(event) => updateFormData("command", event.target.value)}
                  placeholder="e.g. Sit, Stay, Come"
                  className="h-11 w-full rounded-lg border border-gray-200 bg-white px-3 text-sm outline-none transition placeholder:text-gray-400 focus:border-[#4F7942] focus:ring-2 focus:ring-[#4F7942]/15"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Duration</label>
                <input
                  type="number"
                  min="1"
                  max="60"
                  value={formData.duration}
                  onChange={(event) => updateFormData("duration", event.target.value)}
                  placeholder="Minutes"
                  className="h-11 w-full rounded-lg border border-gray-200 bg-white px-3 text-sm outline-none transition placeholder:text-gray-400 focus:border-[#4F7942] focus:ring-2 focus:ring-[#4F7942]/15"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Notes</label>
                <textarea
                  rows="3"
                  value={formData.notes}
                  onChange={(event) => updateFormData("notes", event.target.value)}
                  placeholder="How did it go?"
                  className="w-full resize-none rounded-lg border border-gray-200 bg-white px-3 py-3 text-sm outline-none transition placeholder:text-gray-400 focus:border-[#4F7942] focus:ring-2 focus:ring-[#4F7942]/15"
                />
              </div>

              <div className="space-y-2">
                <button
                  type="submit"
                  className="h-11 w-full rounded-lg bg-[#4F7942] text-sm font-medium text-white transition hover:bg-[#426738]"
                >
                  Save Session
                </button>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="h-11 w-full rounded-lg text-sm font-medium text-gray-500 transition hover:bg-gray-50"
                >
                  Cancel
                </button>
              </div>
            </form>
          </section>
        )}

        <section>
          <h2 className="mb-4 font-medium text-gray-900">Recent sessions</h2>
          <div className="space-y-3">
            {sessions.map((session) => (
              <SessionCard key={session.id} session={session} />
            ))}
          </div>
        </section>
      </div>

      <BottomNavigation />
    </main>
  )
}
