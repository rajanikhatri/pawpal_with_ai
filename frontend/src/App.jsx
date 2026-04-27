import { BrowserRouter, Navigate, Route, Routes, useNavigate } from "react-router-dom"

import AIAssistant from "@/pages/AIAssistant"
import { PET_PROFILE_KEY } from "@/lib/pet"
import Dashboard from "@/pages/Dashboard"
import Onboarding from "@/pages/Onboarding"
import Settings from "@/pages/Settings"
import Training from "@/pages/Training"

function AppRoutes() {
  const navigate = useNavigate()
  const hasPetProfile = Boolean(localStorage.getItem(PET_PROFILE_KEY))

  const handleOnboardingComplete = (petProfile) => {
    localStorage.setItem(PET_PROFILE_KEY, JSON.stringify(petProfile))
    navigate("/dashboard")
  }

  return (
    <Routes>
      <Route
        path="/"
        element={
          hasPetProfile ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Onboarding onComplete={handleOnboardingComplete} />
          )
        }
      />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/ai" element={<AIAssistant />} />
      <Route path="/training" element={<Training />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  )
}
