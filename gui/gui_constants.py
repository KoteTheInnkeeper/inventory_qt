class Color:
    CONTENT_BACKGROUND = "#fbfbfb"
    CONTENT_TEXT = "#484848"
    
    LEFT_MENU = "#86a9c6"
    VERSION_LABEL_BG = "#e5f0f9"
    VERSION_LABEL_TEXT = "#484848"
    BTN_HOVER = "#aaccff"
    BTN_ACTIVE = "#b1cef0"
    BTN_ACTIVE_BORDER = "#325a9f"
    BTN_TEXT = "#4b4b4b"
    BTN_BG = LEFT_MENU
    BTN_PRESSED = LEFT_MENU

    TOP_BAR = "#d8e7f8"
    TOP_BAR_FONT = "#555761"
    TOP_BAR_BORDER = "#e5e5e8"
    
    BOT_BAR = "#e5f0f9"   
    BOT_BAR_TEXT = TOP_BAR_FONT

    STOCK_LEFT_MENU = "#f2f2f2"

    MINOR_BTN_BG = STOCK_LEFT_MENU
    MINOR_BTN_ACTIVE = "#f2f2f2"
    MINOR_BTN_HOVER = BTN_HOVER
    MINOR_BTN_PRESSED = BTN_PRESSED

    FORM_BUTTON_DEF_COLOR = BTN_HOVER
    FORM_BUTTON_DEF_HOVER = TOP_BAR
    FORM_BUTTON_DEF_PRESSED = BTN_PRESSED
    FORM_BUTTON_TEXT = "black"

    LINE_EDIT_DEF_BG_COLOR = CONTENT_BACKGROUND
    LINE_EDIT_DEF_HOVER_COLOR = TOP_BAR

    COMBOBOX_DEF_COLOR = CONTENT_BACKGROUND
    COMBOBOX_DEF_HOVER_COLOR = TOP_BAR
    COMBOBOX_BORDER_COLOR = "black"
    COMBOBOX_DEF_SELECT_BG_COLOR = LEFT_MENU
    COMBOBOX_DEF_SELECT_TEXT_COLOR = "white"


class Dimension:
    TOP_BAR_HEIGHT = 30
    LEFT_MENU_WIDTH = 50
    BOTTOM_BAR_HEIGHT = 30

    BTN_DEF_HEIGHT = 40
    BTN_TEXT_PADDING = 55
    BTN_WIDTH = LEFT_MENU_WIDTH

    LEFT_MENU_EXPANDED_WIDTH = 150

    STOCK_LEFT_MENU_WIDTH = 130

    COMBOBOX_MIN_WIDTH = 200
    COMBOBOX_MIN_HEIGHT = 18

    LINE_EDIT_DEF_HEIGHT = COMBOBOX_MIN_HEIGHT
    LINE_EDIT_DEF_WIDTH = COMBOBOX_MIN_WIDTH
    
    FORM_BUTTON_DEF_HEIGHT = 40
    FORM_BUTTON_DEF_WIDTH = 120
