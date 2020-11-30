

class UI:
    line_width = 1
    updates_per_second = 5

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