import {
  ChevronLeft,
  Send,
} from "lucide-react"
import { useEffect, useRef, useState } from "react"
import { useNavigate } from "react-router-dom"

import BottomNavigation from "@/components/BottomNavigation"
import { getPetProfile } from "@/lib/pet"

function buildInitialMessages(petProfile) {
  const petName = petProfile.petName || "your pet"
  const petType = petProfile.petType || "Dog"

  return [
    {
      id: Date.now(),
      role: "user",
      content: `How much should I feed ${petName} each day?`,
    },
    {
      id: Date.now() + 1,
      role: "ai",
      content:
        petType === "Cat"
          ? "Kittens under 6 months need 3-4 small meals per day. Choose kitten-specific wet or dry food with high protein content."
          : "For a puppy, aim for 3 meals per day. Look for puppy-specific kibble with at least 22% protein. Adjust portions based on the feeding guide on the bag.",
      confidence: 92,
      source: "Puppy nutrition guidelines",
    },
    {
      id: Date.now() + 2,
      role: "user",
      content: "How do I start potty training?",
    },
    {
      id: Date.now() + 3,
      role: "ai",
      content:
        petType === "Cat"
          ? "Place the litter box in a quiet, accessible location. Show your kitten where it is after meals and naps. Most kittens learn quickly with gentle guidance."
          : "Take your puppy outside every 2 hours and right after meals. Pick a consistent spot and reward immediately after they go. At this age puppies can only hold their bladder for about 3 hours.",
      confidence: 88,
      source: "Puppy development guidelines",
    },
  ]
}

function UserMessage({ content }) {
  return (
    <div className="ml-auto max-w-[80%] rounded-2xl rounded-br-sm bg-[#4F7942] px-4 py-3 text-sm text-white">
      {content}
    </div>
  )
}

function AIMessage({ content, confidence, source }) {
  return (
    <div className="flex items-start gap-2">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#EAF3DE] text-sm">
        🐾
      </div>
      <div className="max-w-[85%]">
        <div className="rounded-2xl rounded-bl-sm border border-gray-100 bg-white px-4 py-3 text-sm text-gray-800 shadow-sm">
          {content}
        </div>
        {confidence && source && (
          <div className="mt-2 inline-flex rounded-full bg-[#EAF3DE] px-2 py-1 text-xs text-[#3B6D11]">
            Confidence: {confidence}% · {source}
          </div>
        )}
      </div>
    </div>
  )
}

export default function AIAssistant() {
  const navigate = useNavigate()
  const messagesEndRef = useRef(null)
  const petProfile = getPetProfile()
  const petName = petProfile.petName || "your pet"
  const petType = petProfile.petType || "pet"
  const subtitle = `Personalized for ${petName} · ${petProfile.breed || "Mixed breed"}`
  const suggestedQuestions = [
    `What vaccinations does ${petName} need?`,
    `Best toys for a young ${petType}?`,
    "When to start leash training?",
  ]
  const [messages, setMessages] = useState(() => buildInitialMessages(petProfile))
  const [inputValue, setInputValue] = useState("")

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSend = (event) => {
    event.preventDefault()

    const trimmedInput = inputValue.trim()

    if (!trimmedInput) {
      return
    }

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: trimmedInput,
    }

    setMessages((currentMessages) => [...currentMessages, userMessage])
    setInputValue("")

    window.setTimeout(() => {
      const aiMessage = {
        id: Date.now(),
        role: "ai",
        content: `Thanks for your question about ${petName}! This feature will connect to our AI backend soon. For now here is a tip: always consult your vet for personalized advice.`,
        confidence: 85,
        source: "PawPal+ knowledge base",
      }

      setMessages((currentMessages) => [...currentMessages, aiMessage])
    }, 800)
  }

  return (
    <main className="min-h-screen bg-[#FAFAF8] pt-24 pb-52 text-gray-900">
      <header className="fixed inset-x-0 top-0 z-10 border-b border-gray-100 bg-white shadow-sm">
        <div className="mx-auto flex max-w-2xl items-center px-4 py-4">
          <button
            type="button"
            onClick={() => navigate("/dashboard")}
            className="flex h-10 w-10 items-center justify-center rounded-full text-gray-500 transition hover:bg-gray-50 hover:text-[#4F7942]"
            aria-label="Back to dashboard"
          >
            <ChevronLeft className="h-6 w-6" aria-hidden="true" />
          </button>
          <div className="min-w-0 flex-1 pr-10 text-center">
            <h1 className="text-base font-semibold text-gray-900">AI Care Assistant</h1>
            <p className="mt-0.5 truncate text-xs text-gray-500">{subtitle}</p>
          </div>
        </div>
      </header>

      <div className="mx-auto h-[calc(100vh-17rem)] max-w-2xl overflow-y-auto px-4 py-4">
        <div className="space-y-4">
          {messages.map((message) =>
            message.role === "user" ? (
              <UserMessage key={message.id} content={message.content} />
            ) : (
              <AIMessage
                key={message.id}
                content={message.content}
                confidence={message.confidence}
                source={message.source}
              />
            )
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="fixed inset-x-0 bottom-16 z-10">
        <div className="mx-auto max-w-2xl px-4">
          <div className="mb-2 flex gap-2 overflow-x-auto pb-1">
            {suggestedQuestions.map((question) => (
              <button
                key={question}
                type="button"
                onClick={() => setInputValue(question)}
                className="shrink-0 rounded-full border border-gray-200 bg-white px-3 py-1.5 text-xs text-gray-500 transition hover:border-[#4F7942] hover:text-[#4F7942]"
              >
                {question}
              </button>
            ))}
          </div>

          <form
            onSubmit={handleSend}
            className="flex gap-2 border-t border-gray-100 bg-white px-4 py-3 shadow-[0_-4px_12px_rgba(0,0,0,0.06)]"
          >
            <input
              type="text"
              value={inputValue}
              onChange={(event) => setInputValue(event.target.value)}
              placeholder={`Ask about ${petName}...`}
              className="h-10 flex-1 rounded-lg border border-gray-200 bg-white px-3 text-sm outline-none transition placeholder:text-gray-400 focus:border-[#4F7942] focus:ring-2 focus:ring-[#4F7942]/15"
            />
            <button
              type="submit"
              className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[#4F7942] text-white transition hover:bg-[#426738]"
              aria-label="Send message"
            >
              <Send className="h-5 w-5" aria-hidden="true" />
            </button>
          </form>
        </div>
      </div>

      <BottomNavigation />
    </main>
  )
}
