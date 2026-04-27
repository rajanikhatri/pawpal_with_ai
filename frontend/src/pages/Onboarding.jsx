import { useState } from "react"

import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const initialProfile = {
  petType: "",
  petName: "",
  ageYears: "",
  ageMonths: "",
  sex: "",
  breed: "",
  source: "",
  role: "",
  commandsKnown: [],
  struggles: [],
}

const steps = [1, 2, 3, 4]

function Chip({ label, selected, onClick, variant = "green" }) {
  const selectedClass =
    variant === "amber"
      ? "border-[#F4A261] bg-[#F4A26115] text-[#854F0B]"
      : "border-[#4F7942] bg-[#4F794215] text-[#4F7942]"

  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "rounded-full border px-4 py-2 text-sm font-medium transition",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#4F7942]/30",
        selected ? selectedClass : "border-gray-200 bg-white text-gray-500 hover:border-gray-300"
      )}
    >
      {label}
    </button>
  )
}

function FieldLabel({ children }) {
  return <label className="text-sm font-medium text-gray-700">{children}</label>
}

function ProgressBar({ currentStep }) {
  return (
    <div className="mb-8 flex items-center">
      {steps.map((step, index) => {
        const done = step < currentStep
        const active = step === currentStep

        return (
          <div key={step} className="flex flex-1 items-center last:flex-none">
            <div
              className={cn(
                "flex h-9 w-9 items-center justify-center rounded-full text-sm font-semibold",
                done && "bg-[#4F7942] text-white",
                active && "bg-[#4F7942] text-white ring-4 ring-[#4F7942]/15",
                !done && !active && "border border-gray-200 bg-gray-100 text-gray-400"
              )}
            >
              {done ? "✓" : step}
            </div>
            {index < steps.length - 1 && (
              <div
                className={cn(
                  "mx-2 h-0.5 flex-1 rounded-full",
                  step < currentStep ? "bg-[#4F7942]" : "bg-gray-200"
                )}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}

function ReviewRow({ label, value }) {
  return (
    <div className="flex items-start justify-between gap-4 border-b border-gray-100 py-3 last:border-b-0">
      <span className="text-sm text-gray-500">{label}</span>
      <span className="text-right text-sm font-medium text-gray-800">{value || "Not provided"}</span>
    </div>
  )
}

export default function Onboarding({ onComplete }) {
  const [currentStep, setCurrentStep] = useState(1)
  const [petProfile, setPetProfile] = useState(initialProfile)

  const updateProfile = (field, value) => {
    setPetProfile((currentProfile) => ({
      ...currentProfile,
      [field]: value,
    }))
  }

  const toggleMultiSelect = (field, value) => {
    setPetProfile((currentProfile) => {
      const currentValues = currentProfile[field]
      const nextValues = currentValues.includes(value)
        ? currentValues.filter((item) => item !== value)
        : [...currentValues, value]

      return {
        ...currentProfile,
        [field]: nextValues,
      }
    })
  }

  const continueToNextStep = () => {
    setCurrentStep((step) => Math.min(step + 1, 4))
  }

  const goBack = () => {
    setCurrentStep((step) => Math.max(step - 1, 1))
  }

  const handleSubmit = () => {
    onComplete?.(petProfile)
  }

  const ageSummary = [
    petProfile.ageYears !== "" ? `${petProfile.ageYears} yr` : "",
    petProfile.ageMonths !== "" ? `${petProfile.ageMonths} mo` : "",
  ]
    .filter(Boolean)
    .join(" ")

  return (
    <main className="min-h-screen bg-[#FAFAF8] px-4 py-6 text-gray-900 sm:px-6">
      <div className="mx-auto flex min-h-[calc(100vh-3rem)] max-w-xl flex-col justify-center">
        <ProgressBar currentStep={currentStep} />

        <section className="rounded-lg border border-gray-100 bg-white p-5 shadow-sm sm:p-6">
          {currentStep === 1 && (
            <div className="space-y-6">
              <div>
                <p className="text-sm font-semibold text-[#4F7942]">Step 1 of 4</p>
                <h1 className="mt-2 text-2xl font-semibold tracking-tight">
                  What kind of pet do you have?
                </h1>
              </div>

              <div className="space-y-3">
                <FieldLabel>Pet type</FieldLabel>
                <div className="flex flex-wrap gap-2">
                  {["Dog", "Cat"].map((type) => (
                    <Chip
                      key={type}
                      label={type}
                      selected={petProfile.petType === type}
                      onClick={() => updateProfile("petType", type)}
                    />
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <FieldLabel>Pet name</FieldLabel>
                <input
                  type="text"
                  value={petProfile.petName}
                  onChange={(event) => updateProfile("petName", event.target.value)}
                  placeholder="e.g. Milo"
                  className="h-11 w-full rounded-lg border border-gray-200 bg-white px-3 text-sm outline-none transition placeholder:text-gray-400 focus:border-[#4F7942] focus:ring-2 focus:ring-[#4F7942]/15"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-2">
                  <FieldLabel>Age years</FieldLabel>
                  <input
                    type="number"
                    min="0"
                    value={petProfile.ageYears}
                    onChange={(event) => updateProfile("ageYears", event.target.value)}
                    className="h-11 w-full rounded-lg border border-gray-200 bg-white px-3 text-sm outline-none transition focus:border-[#4F7942] focus:ring-2 focus:ring-[#4F7942]/15"
                  />
                </div>
                <div className="space-y-2">
                  <FieldLabel>Age months</FieldLabel>
                  <input
                    type="number"
                    min="0"
                    max="11"
                    value={petProfile.ageMonths}
                    onChange={(event) => updateProfile("ageMonths", event.target.value)}
                    className="h-11 w-full rounded-lg border border-gray-200 bg-white px-3 text-sm outline-none transition focus:border-[#4F7942] focus:ring-2 focus:ring-[#4F7942]/15"
                  />
                </div>
              </div>

              <div className="space-y-3">
                <FieldLabel>Sex</FieldLabel>
                <div className="flex flex-wrap gap-2">
                  {["Male", "Female"].map((sex) => (
                    <Chip
                      key={sex}
                      label={sex}
                      selected={petProfile.sex === sex}
                      onClick={() => updateProfile("sex", sex)}
                    />
                  ))}
                </div>
              </div>

              <Button
                type="button"
                onClick={continueToNextStep}
                className="h-11 w-full bg-[#4F7942] text-white hover:bg-[#426738]"
              >
                Continue
              </Button>
            </div>
          )}

          {currentStep === 2 && (
            <div className="space-y-6">
              <div>
                <p className="text-sm font-semibold text-[#4F7942]">Step 2 of 4</p>
                <h1 className="mt-2 text-2xl font-semibold tracking-tight">
                  Tell us about the breed
                </h1>
              </div>

              <div className="space-y-2">
                <FieldLabel>Breed</FieldLabel>
                <input
                  type="text"
                  value={petProfile.breed}
                  onChange={(event) => updateProfile("breed", event.target.value)}
                  placeholder="e.g. Golden Retriever, Mixed breed"
                  className="h-11 w-full rounded-lg border border-gray-200 bg-white px-3 text-sm outline-none transition placeholder:text-gray-400 focus:border-[#4F7942] focus:ring-2 focus:ring-[#4F7942]/15"
                />
              </div>

              <div className="space-y-3">
                <FieldLabel>How did you get your pet?</FieldLabel>
                <div className="flex flex-wrap gap-2">
                  {["Adopted", "Breeder", "Rescue", "Gift"].map((source) => (
                    <Chip
                      key={source}
                      label={source}
                      selected={petProfile.source === source}
                      onClick={() => updateProfile("source", source)}
                    />
                  ))}
                </div>
              </div>

              <div className="space-y-3">
                <FieldLabel>Role</FieldLabel>
                <div className="flex flex-wrap gap-2">
                  {["Family member", "Companion", "Guard dog", "Working dog"].map((role) => (
                    <Chip
                      key={role}
                      label={role}
                      variant="amber"
                      selected={petProfile.role === role}
                      onClick={() => updateProfile("role", role)}
                    />
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Button
                  type="button"
                  onClick={continueToNextStep}
                  className="h-11 w-full bg-[#4F7942] text-white hover:bg-[#426738]"
                >
                  Continue
                </Button>
                <Button type="button" variant="ghost" onClick={goBack} className="h-11 w-full">
                  Back
                </Button>
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="space-y-6">
              <div>
                <p className="text-sm font-semibold text-[#4F7942]">Step 3 of 4</p>
                <h1 className="mt-2 text-2xl font-semibold tracking-tight">
                  Training and behavior
                </h1>
              </div>

              <div className="space-y-3">
                <FieldLabel>Commands already known</FieldLabel>
                <div className="flex flex-wrap gap-2">
                  {["Sit", "Stay", "Come", "Down", "Heel", "None yet"].map((command) => (
                    <Chip
                      key={command}
                      label={command}
                      selected={petProfile.commandsKnown.includes(command)}
                      onClick={() => toggleMultiSelect("commandsKnown", command)}
                    />
                  ))}
                </div>
              </div>

              <div className="space-y-3">
                <FieldLabel>Struggling with most</FieldLabel>
                <div className="flex flex-wrap gap-2">
                  {[
                    "Potty training",
                    "Biting/chewing",
                    "Separation anxiety",
                    "Feeding schedule",
                    "Not sure yet",
                  ].map((struggle) => (
                    <Chip
                      key={struggle}
                      label={struggle}
                      variant="amber"
                      selected={petProfile.struggles.includes(struggle)}
                      onClick={() => toggleMultiSelect("struggles", struggle)}
                    />
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Button
                  type="button"
                  onClick={continueToNextStep}
                  className="h-11 w-full bg-[#4F7942] text-white hover:bg-[#426738]"
                >
                  Continue
                </Button>
                <Button type="button" variant="ghost" onClick={goBack} className="h-11 w-full">
                  Back
                </Button>
              </div>
            </div>
          )}

          {currentStep === 4 && (
            <div className="space-y-6">
              <div>
                <p className="text-sm font-semibold text-[#4F7942]">Step 4 of 4</p>
                <h1 className="mt-2 text-2xl font-semibold tracking-tight">Almost done!</h1>
              </div>

              <div className="rounded-lg border border-gray-100 bg-[#FAFAF8] p-4">
                <div className="mb-4 flex items-center gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white text-2xl shadow-sm">
                    {petProfile.petType === "Cat" ? "🐱" : "🐶"}
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900">
                      {petProfile.petName || "Your pet"}
                    </h2>
                    <p className="text-sm text-gray-500">{petProfile.petType || "Pet profile"}</p>
                  </div>
                </div>

                <ReviewRow label="Breed" value={petProfile.breed} />
                <ReviewRow label="Age" value={ageSummary} />
                <ReviewRow label="Sex" value={petProfile.sex} />
                <ReviewRow label="Source" value={petProfile.source} />
                <ReviewRow label="Role" value={petProfile.role} />
                <ReviewRow label="Commands known" value={petProfile.commandsKnown.join(", ")} />
                <ReviewRow label="Struggles" value={petProfile.struggles.join(", ")} />
              </div>

              <div className="space-y-2">
                <Button
                  type="button"
                  onClick={handleSubmit}
                  className="h-11 w-full bg-[#4F7942] text-white hover:bg-[#426738]"
                >
                  Generate my care plan
                </Button>
                <Button type="button" variant="ghost" onClick={goBack} className="h-11 w-full">
                  Back
                </Button>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  )
}
