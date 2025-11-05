import flet as ft
import asyncio


class CountdownTimer:
    def __init__(self, timer_id):
        self.timer_id = timer_id
        self.seconds = 0
        self.running = False
        self.paused = False
        self.initial_seconds = 0
        self.page = None
        
    def build(self):
        # Timer input field
        self.timer_input = ft.TextField(
            label="Timer value (seconds)",
            value="60",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        # Timer display
        self.timer_display = ft.Text(
            value="00:00",
            size=48,
            weight=ft.FontWeight.BOLD
        )
        
        self.remaining_text = ft.Text(
            value="Remaining: 0s",
            size=16
        )
        
        # Progress indicators
        self.progress_bar = ft.ProgressBar(
            width=300,
            value=0,
            bar_height=10
        )
        
        self.progress_ring = ft.ProgressRing(
            width=80,
            height=80,
            value=0
        )
        
        # Buttons
        self.start_button = ft.ElevatedButton(
            text="Start",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.start_timer
        )
        
        self.pause_button = ft.ElevatedButton(
            text="Pause",
            icon=ft.Icons.PAUSE,
            on_click=self.pause_timer,
            disabled=True
        )
        
        self.reset_button = ft.ElevatedButton(
            text="Reset",
            icon=ft.Icons.REFRESH,
            on_click=self.reset_timer,
            disabled=True
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text(f"Timer {self.timer_id}", size=24, weight=ft.FontWeight.BOLD),
                self.timer_input,
                ft.Row([
                    ft.Column([
                        self.timer_display,
                        self.remaining_text,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    self.progress_ring
                ], alignment=ft.MainAxisAlignment.CENTER),
                self.progress_bar,
                ft.Row([
                    self.start_button,
                    self.pause_button,
                    self.reset_button
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            padding=20,
            border=ft.border.all(2, "blue"),
            border_radius=10
        )
    
    def update(self):
        if self.page:
            self.page.update()
    
    def start_timer(self, e):
        if not self.running:
            try:
                self.seconds = int(self.timer_input.value)
                self.initial_seconds = self.seconds
                self.running = True
                self.paused = False
                self.timer_input.disabled = True
                self.start_button.disabled = True
                self.pause_button.disabled = False
                self.reset_button.disabled = False
                self.update()
                self.page.run_task(self.update_timer)
            except ValueError:
                pass
        elif self.paused:
            self.paused = False
            self.start_button.disabled = True
            self.pause_button.disabled = False
            self.update()
    
    def pause_timer(self, e):
        self.paused = True
        self.start_button.disabled = False
        self.pause_button.disabled = True
        self.update()
    
    def reset_timer(self, e):
        self.running = False
        self.paused = False
        self.seconds = self.initial_seconds
        self.timer_input.disabled = False
        self.start_button.disabled = False
        self.pause_button.disabled = True
        self.reset_button.disabled = True
        self.update_display()
        self.update()
    
    async def update_timer(self):
        while self.seconds > 0 and self.running:
            if not self.paused:
                self.seconds -= 1
                self.update_display()
                self.update()
            await asyncio.sleep(1)
        
        if self.seconds == 0 and self.running:
            self.running = False
            self.timer_input.disabled = False
            self.start_button.disabled = False
            self.pause_button.disabled = True
            self.reset_button.disabled = True
            self.update()
    
    def update_display(self):
        mins, secs = divmod(self.seconds, 60)
        self.timer_display.value = "{:02d}:{:02d}".format(mins, secs)
        self.remaining_text.value = f"Remaining: {self.seconds}s"
        
        # Update progress bar and ring
        if self.initial_seconds > 0:
            progress = 1 - (self.seconds / self.initial_seconds)
            self.progress_bar.value = progress
            self.progress_ring.value = progress


def main(page: ft.Page):
    page.title = "Multi Countdown Timer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Create three timer instances
    timer1 = CountdownTimer(1)
    timer1.page = page
    timer2 = CountdownTimer(2)
    timer2.page = page
    timer3 = CountdownTimer(3)
    timer3.page = page
    
    # Create tabs
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Timer 1",
                icon=ft.Icons.TIMER,
                content=ft.Container(
                    content=timer1.build(),
                    alignment=ft.alignment.center,
                    padding=20
                )
            ),
            ft.Tab(
                text="Timer 2",
                icon=ft.Icons.TIMER,
                content=ft.Container(
                    content=timer2.build(),
                    alignment=ft.alignment.center,
                    padding=20
                )
            ),
            ft.Tab(
                text="Timer 3",
                icon=ft.Icons.TIMER,
                content=ft.Container(
                    content=timer3.build(),
                    alignment=ft.alignment.center,
                    padding=20
                )
            ),
        ],
        expand=1
    )
    
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TIMER_OUTLINED,
                selected_icon=ft.Icons.TIMER,
                label="Timer 1"
            ),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TIMER_OUTLINED,
                selected_icon=ft.Icons.TIMER,
                label="Timer 2"
            ),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TIMER_OUTLINED,
                selected_icon=ft.Icons.TIMER,
                label="Timer 3"
            ),
        ],
    )
    
    def handle_drawer_change(e):
        tabs.selected_index = e.control.selected_index
        page.close(drawer)
        page.update()
    
    drawer.on_change = handle_drawer_change
    
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=lambda e: page.open(drawer)
        ),
        title=ft.Text("Multi Countdown Timer"),
        center_title=True,
        bgcolor="blue"
    )
    
    page.add(tabs)


ft.app(target=main)
