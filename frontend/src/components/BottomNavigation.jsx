import { Dumbbell, Home, MessageCircle, Settings } from "lucide-react"
import { NavLink } from "react-router-dom"

import { cn } from "@/lib/utils"

const navItems = [
  { label: "Home", to: "/dashboard", icon: Home },
  { label: "AI Chat", to: "/ai", icon: MessageCircle },
  { label: "Training", to: "/training", icon: Dumbbell },
  { label: "Settings", to: "/settings", icon: Settings },
]

export default function BottomNavigation() {
  return (
    <nav className="fixed inset-x-0 bottom-0 z-20 border-t border-gray-100 bg-white/95 px-4 py-2 shadow-[0_-8px_24px_rgba(17,24,39,0.06)] backdrop-blur">
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
