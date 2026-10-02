import { useState } from "react"
import { Moon, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"

function getInitialDarkMode() {
	return document.documentElement.classList.contains("dark")
}

export function ThemeToggle() {
	const [dark, setDark] = useState(getInitialDarkMode)

	function toggleTheme() {
		const nextDark = !dark
		document.documentElement.classList.toggle("dark", nextDark)
		localStorage.setItem("theme", nextDark ? "dark" : "light")
		setDark(nextDark)
	}

	return (
		<Button
			type="button"
			variant="ghost"
			size="icon"
			onClick={toggleTheme}
			aria-label={dark ? "Switch to light mode" : "Switch to dark mode"}
			title={dark ? "Switch to light mode" : "Switch to dark mode"}
		>
			{dark ? <Sun /> : <Moon />}
		</Button>
	)
}

