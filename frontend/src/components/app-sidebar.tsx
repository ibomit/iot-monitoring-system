import {
  ChevronRight,
  LayoutGrid,
  RadioTower,
} from "lucide-react"
import { NavLink, useLocation } from "react-router-dom"
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
        <div className="flex items-center gap-2 rounded-lg bg-sidebar-accent/60 px-3 py-2.5 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-2">
          <span className="size-2 rounded-full bg-emerald-500 shadow-[0_0_0_3px_color-mix(in_oklab,_#10b981_20%,_transparent)]" />
          <div className="min-w-0 group-data-[collapsible=icon]:hidden">
            <p className="text-xs font-medium">All systems operational</p>
            <p className="text-[11px] text-sidebar-foreground/60">API connected</p>
          </div>
          <ChevronRight className="ml-auto size-3.5 text-sidebar-foreground/40 group-data-[collapsible=icon]:hidden" />
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