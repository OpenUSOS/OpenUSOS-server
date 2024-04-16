import flet as ft

class Schedule:
    data = ''
    def display(self):
        pass

class Emails:
    data = ''
    def display(self):
        pass
    def display_send(self):
        pass
    def send_email(self):
        pass

class Grades:
    def display(self):
        pass

class Exams:
    def display(self):
        pass
    def display_send(self):
        pass

class Reminders:
    def set_reminders(self):
        pass
    def unset_reminders(self):
        pass


def main(page: ft.Page):
    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))


ft.app(main)
