
class UI:
    line_width = 1
    updates_per_second = 10
    menu_shown = True

    @staticmethod
    def get_line_width():
        return UI.line_width

    @staticmethod
    def set_line_width(width: int):
        UI.line_width = width

    @staticmethod
    def get_updates_per_second():
        return UI.updates_per_second

    @staticmethod
    def set_updates_per_second(ups: int):
        UI.updates_per_second = ups

    @staticmethod
    def get_menu_shown():
        return UI.menu_shown

    @staticmethod
    def set_menu_shown(status: bool):
        UI.menu_shown = status