import { useEffect, useState } from "react"
import {
  LayoutGrid,
  RadioTower,
} from "lucide-react"
import { NavLink, useLocation } from "react-router-dom"
import { checkApiHealth } from "@/services/api"
import { ThemeToggle } from "@/components/ThemeToggle"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarSeparator,
} from "@/components/ui/sidebar"

const navigation = [
  {
    label: "Workspace",
    items: [{ title: "Devices", url: "/devices", icon: LayoutGrid }],
  },
]

export function AppSidebar() {
  const [apiStatus, setApiStatus] = useState<"checking" | "connected" | "unavailable">("checking")

  useEffect(() => {
    let cancelled = false

    async function updateApiStatus() {
      const isHealthy = await checkApiHealth()
      if (!cancelled) {
        setApiStatus(isHealthy ? "connected" : "unavailable")
      }
    }

    void updateApiStatus()
    const intervalId = window.setInterval(updateApiStatus, 10000)

    return () => {
      cancelled = true
      window.clearInterval(intervalId)
    }
  }, [])

  const statusCopy = {
    checking: { title: "Checking API", detail: "Connecting..." },
    connected: { title: "All systems operational", detail: "API connected" },
    unavailable: { title: "API unavailable", detail: "Connection failed" },
  }[apiStatus]

  return (
    <Sidebar collapsible="icon" className="border-sidebar-border/70">
      <SidebarHeader className="border-b border-sidebar-border/70 px-3 py-4">
        <div className="flex items-center gap-3 group-data-[collapsible=icon]:justify-center">
          <div className="flex size-9 shrink-0 items-center justify-center rounded-xl bg-sidebar-primary text-sidebar-primary-foreground shadow-sm">
            <RadioTower className="size-4" />
          </div>
          <div className="min-w-0 group-data-[collapsible=icon]:hidden">
            <p className="truncate text-sm font-semibold tracking-tight">Pulse</p>
            <p className="truncate text-xs text-sidebar-foreground/60">IoT command center</p>
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent>
        {navigation.map((group) => (
          <SidebarGroup key={group.label} className="px-2 py-4">
            <SidebarGroupLabel>{group.label}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {group.items.map((item) => (
                  <NavigationItem key={item.title} {...item} />
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}

      </SidebarContent>

      <SidebarSeparator />
      <SidebarFooter className="p-3">
        <div className="mb-2 flex justify-end group-data-[collapsible=icon]:justify-center">
          <ThemeToggle />
        </div>
        <div className="flex items-center gap-2 rounded-lg bg-sidebar-accent/60 px-3 py-2.5 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-2">
          <span className={`size-2 rounded-full ${apiStatus === "connected" ? "bg-emerald-500 shadow-[0_0_0_3px_color-mix(in_oklab,_#10b981_20%,_transparent)]" : apiStatus === "unavailable" ? "bg-red-500 shadow-[0_0_0_3px_color-mix(in_oklab,_#ef4444_20%,_transparent)]" : "bg-amber-500 shadow-[0_0_0_3px_color-mix(in_oklab,_#f59e0b_20%,_transparent)]"}`} />
          <div className="min-w-0 group-data-[collapsible=icon]:hidden">
            <p className="text-xs font-medium">{statusCopy.title}</p>
            <p className="text-[11px] text-sidebar-foreground/60">{statusCopy.detail}</p>
          </div>
        </div>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}

function NavigationItem({
  title,
  url,
  icon: Icon,
}: {
  title: string
  url: string
  icon: typeof LayoutGrid
}) {
  const { pathname } = useLocation()
  const isActive = pathname === url || pathname.startsWith(`${url}/`)

  return (
    <SidebarMenuItem>
      <SidebarMenuButton
        render={<NavLink to={url} />}
        isActive={isActive}
        tooltip={title}
      >
        <Icon />
        <span>{title}</span>
      </SidebarMenuButton>
    </SidebarMenuItem>
  )
}