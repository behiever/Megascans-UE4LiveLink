#!/usr/bin/env python
# -*- coding: utf-8 -*-

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# ██╗   ██╗███████╗███████╗██████╗     ██╗███╗   ██╗████████╗███████╗██████╗ ███████╗ █████╗  ██████╗███████╗
# ██║   ██║██╔════╝██╔════╝██╔══██╗    ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝
# ██║   ██║███████╗█████╗  ██████╔╝    ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝█████╗  ███████║██║     █████╗  
# ██║   ██║╚════██║██╔══╝  ██╔══██╗    ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║     ██╔══╝  
# ╚██████╔╝███████║███████╗██║  ██║    ██║██║ ╚████║   ██║   ███████╗██║  ██║██║     ██║  ██║╚██████╗███████╗
#  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Quixel AB - Megascans Project
# The Megascans Integration for Unreal Engine 4 was written in Python, using the UnrealEnginePython plugin
# by 20Tab : https://github.com/20tab/UnrealEnginePython

# This integration gives you a LiveLink between Megascans Bridge and Unreal Engine 4. The source code is all exposed
# and documented for you to use it as you wish (within the Megascans EULA limits, that is).
# We provide a set of useful functions for importing data inside the engine, but you can use the default
# functions (of UnrealEnginePython) instead of Megascans modules if you want.

# We've tried to document the code as much as we could within a short timeframe, so if you're having any issues
# please send me an email (adnan@quixel.se) for support.

# The user interface was written using a custom PySide2 build. The particularity of this build is that it comes with just the basic
# UI DLLs provided by PySide2 for the sake of saving disk space.QtWidgets, QtCore and QtGui are the only available/fully tested
# modules. The PySide2 integration in unreal will be improved a lot during it's first 6 months, so you can expect a few
# changes here and there in the functions/classes declared in this file. With that said, it is very unlikely that we will
# add support for more DLLs/libraries for the PySide2 support.


with open(ms_return_path() + '/megascans/settings.json') as f:
    data = f.read()
settings_ = json.loads(data)

class ms_mainclass(object):

    main_win = None
    materials = settings_['CustomMaterial']
    # print(materials)

megascans_fldr = (ms_return_path() + 'megascans/ui')


try:
    # Create an instance of QApplication. This is used by PySide2.
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
except:
    ue.message_dialog_open(0, "C++ project detected, the integration UI is currently only available in a blueprint project.\n\
You can still use the plugin as normal, and expect C++ compatibility soon !")
    print('C++ Project Detected, UI not available in the current version.')
    pass


font_db = QFontDatabase()
font_path = (megascans_fldr)

for item_ in [file_ for file_ in os.listdir(font_path) if file_.endswith('.ttf')]:
    font_id = font_db.addApplicationFont(font_path + "/" + item_)
    families = font_db.applicationFontFamilies(font_id)

def ue_exception(_type, value, back):
    ue.log_error(value)
    tb_lines = traceback.format_exception(_type, value, back)
    for line in tb_lines:
        ue.log_error(line)

sys.excepthook = ue_exception




Action_Style = ("""
    QPushButton { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: transparent;color : #E6E6E6; }
    QPushButton:hover { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: transparent;color : #E6E6E6; }
        """)

Pause_Style = ("""
    QPushButton { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: #2B2B2B; border-radius: 3px; color : #E6E6E6; }
    QPushButton:hover { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: #2daae1; border-radius: 4px; color : #E6E6E6; }
        """)


# self.checker.setStyleSheet((checkbox_layout.replace("CheckedIMG", (megascans_fldr + '/Checked_Black.png'))))
checkbox_layout = ("""

QCheckBox {
    background: transparent;
    color: #E6E6E6;
    font-family: Source Sans Pro;
    font-size: 16px;
}

QCheckBox::indicator:hover
{
    border: 2px solid #2B98F0;
    background-color: transparent;
}

QCheckBox::indicator:checked:hover
{
    background-color: #73a5ce;
    border: 2px solid #73a5ce;
}


QCheckBox:indicator{
    color: #67696a;
    background-color: transparent;
    border: 2px solid #67696a;
    width: 18px;
    height: 16px;
    border-radius: 2px;
}

QCheckBox::indicator:checked
{
    border: 2px solid #2B98F0;
    image: url(CheckedIMG);
    background-color: #2B98F0;
    text-color: #ffffff;
 }


QCheckBox::hover {
    spacing: 12px;
    background: transparent;
    color: #ffffff;
}

QCheckBox::checked {
    color: #ffffff;
}


QCheckBox::indicator:disabled, QRadioButton::indicator:disabled
{
    border: 1px solid #444;

}

QCheckBox:disabled
{
    background: transparent;
    color: #414141;
    font-family: Source Sans Pro;
    font-size: 16px;    margin: 0px;
    text-align: center;
}

""")



material_style = ("""

QComboBox
{
    padding: 1px 1px 1px 10px;
    selection-background-color: #3b3b3b;
    background-color: #2c2c2c;
    /*border-style: none;
    /*border: 0px solid #1e1e1e;*/
    color: #ffffff;
    border-radius: 2px;
    font-family: Source Sans Pro;
    font-size: 16px;

}

QComboBox:hover
{
  border: 0px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #51626d, stop: 1 #4e5359);
  background-color: #3b3b3b;
}


QComboBox:on
{   padding: 1px 1px 1px 5px;
    background-color: #333435;
    color: #ffffff;
    selection-background-color: #232322;
}

QComboBox QAbstractItemView
{
    border: 2px;
    padding-left: 10px;
    background-color: #333435;
    padding-bottom: 5px;
    min-height: 30px;
    color: #ffffff;
    padding-top: 10px;
    background-color: #3b3b3b;
}

QComboBox::QAbstractItemView:item
{
    border: 0px;
    padding-left: 10px;
    min-height: 30px;
    color: #ffffff;
}

QComboBox::drop-down {
    border:20px;
    margin:0px;
    color: #ffffff;
    margin-right:0px;
}

QComboBox::down-arrow
{
  background-image: url(down_arr);
  background-repeat: none;
  color: #ffffff;
  margin-left: -1px;

}


 QScrollBar:vertical {
     border: 0px solid #1E1E1E;
     background: transparent;
     width: 8px;
     margin: 0 0 0 0;

 }
 QScrollBar::handle:vertical {
     background: #191919;
     border-radius: 3px;
     max-height: 20px;
 }
  QScrollBar::handle:vertical:hover {
     background: #252525;
     border-radius: 3px;
     max-height: 20px;
 }


 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
  border: none;
  background: none;
  background-color: none;
 }

QScrollBar::add-line:vertical {
  border: none;
  background: transparent;
  background-color: transparent;
}

QScrollBar::sub-line:vertical {
  border: none;
  background: transparent;
  background-color: transparent;
}

 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
     background: none;
 }

""")
material_style = material_style.replace("down_arr", (megascans_fldr + '/cursor_down.png'))
print((megascans_fldr + '/cursor_down.png'))

tiling_slider_style = ("""
QSlider::groove:horizontal {
border: 1px solid #bbb;
background: #1A1A1A;
height: 10px;
border-radius: 0px;
}

QSlider::sub-page:horizontal {
background: #1A1A1A;

border: 1px solid #444;
height: 10px;
border-radius: 0px;
}

QSlider::add-page:horizontal {
background: #262626;
border: 0px solid #777;
height: 10px;
border-radius: 0px;
}

QSlider::handle:horizontal {
background: #0D0D0D;
border: 0px solid #777;
width: 18px;
border-radius: 0px;
margin-top: -2px;
margin-bottom: -2px;
}

QSlider::handle:horizontal:hover {
background: #656565;
border: 0px solid #444;
}

QSlider{
background: none;
}
""")


PrefsMenuStyle = ("""
QMenu
{
    color: #f0f0f0;
    background-color: #1A1A1A;
    border: 3px solid #2c2d2e;
    border-radius: 4px;
    padding: 15px 15px 15px 15px;

    color: #f0f0f0;
    font-size: 15px;
    font-weight: normal;
    margin: 0px;
    text-align: center;
}

QMenu:pressed
{
    color: #f0f0f0;
    font-weight: normal;
    background-color: #1A1A1A;
    font-size: 18px;
    border: 0px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #51626d, stop: 1 #4e5359);
    padding-left: 4px;
    margin-left: 10px;
    margin-right: 5px;
}

QMenu::item:selected
{   
    color: #FFFFFF;
    background-color: #4E79A3;
    border: 0px;
    border-radius: 4px;
    padding: 3px 10px 3px 5px;

    font-size: 15px;
    font-weight: normal;
    margin: 0px;
    text-align: center;
}

QMenu::separator
{
    height: 1px;
    background-color: #313131;
    color: white;
    padding-left: 4px;
    margin-left: 2px;
    margin-right: 5px;
}

QMenu::item
{
    padding: 3px 25px 3px 5px;
}


""")










#check if an instance of the application is already running


# root_window = ue.get_editor_window()


# GWL_HWNDPARENT = 3
# SetWindowLongPtr = ctypes.windll.user32.SetWindowLongPtrW

# root_window = ue.get_editor_window()
# ue_editor_hwnd = (root_window.get_handle())



class QBaseButton(QPushButton):

    def __init__(self, request):
        super(QBaseButton, self).__init__(None)

        self.request = request

        self.setIcon( QIcon(QPixmap(megascans_fldr + '/' + self.request + '_icon.png')))
        self.setIconSize(QSize(22, 22))
        self.setStyleSheet(Action_Style)
        self.setMinimumHeight(22)
        # self.clicked.connect(self.cancel)
    def enterEvent(self, event):
        self.setIcon( QIcon(QPixmap(megascans_fldr + '/' + self.request + '_hover_icon.png')))
        self.setIconSize(QSize(22, 22))

    def leaveEvent(self, event):
        self.setIcon( QIcon(QPixmap(megascans_fldr + '/' + self.request + '_icon.png')))
        self.setIconSize(QSize(22, 22))





class QMaterialDisplay(QLabel):

    def __init__(self, request, parent):
        super(QMaterialDisplay, self).__init__(None)

        self.request = request
        self.parent = parent

        self.setText(self.request)
        self.setMinimumHeight(32)
        self.setMinimumWidth(200)
        self.setStyleSheet("""QLabel {background-color: #2c2f31; border-radius: 3px;
         font-size: 16px; font-family: Source Sans Pro;
          border: 2px solid #505B63; color: #a2a2a2; padding: 1px 1px 1px 5px;}""")


    def mousePressEvent(self, event):
        megascans_livelink_ui.sync_mtl_browser(self.parent)





class QCustomCheckBox(QWidget):

    def __init__(self, request, checkstate, parent):
        super(QCustomCheckBox, self).__init__(None)

        self.unchecked_style = ("""
        QPushButton#QCustomCheckBox
        {
            border: 0px solid #67696A;
            border-radius: 2px;
            background-color: transparent;
        }        """)

        self.setStyleSheet(self.unchecked_style)

        self.Checked = checkstate
        self.path_ = (megascans_fldr + '/Checked_Black.png')
        self.request = request
        self.parent = parent

        # Set the main layout
        self.mainlayout = QHBoxLayout()
        self.setLayout(self.mainlayout)
        # self.mainlayout.setAlignment(Qt.AlignCenter)
        self.mainlayout.setSpacing(12)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)

        self.check_icon = QPixmap(self.path_)
        self.check_icon.scaled(QSize(20, 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.icon_ = QLabel()
        self.icon_.setStyleSheet("QLabel {background-color: #2B98F0; border-radius: 2px;border: 0px; color: #a2a2a2;}")
        self.icon_.setFixedSize(20, 20)
        self.icon_.setScaledContents(True)
        self.icon_.setPixmap(QPixmap(self.path_))
        self.mainlayout.addWidget(self.icon_)

        self.text_ = QLabel(self.request)
        self.text_.setStyleSheet("QLabel {background-color: transparent;font-size: 16px; font-family: Source Sans Pro; border: 0px; color: #ffffff;}")
        # self.text_.setFixedHeight(30)
        self.mainlayout.addWidget(self.text_)

        if self.Checked:
            self.icon_.setPixmap(QPixmap(self.path_))
            self.icon_.setStyleSheet("QLabel {background-color: transparent; border-radius: 2px;border: 2px solid #6F6F6F; color: #a2a2a2;}")

        else:
            self.icon_.setPixmap(QPixmap(None))
            self.icon_.setStyleSheet("QLabel {background-color: #2B98F0; border-radius: 2px;border: 0px; color: #a2a2a2;}")

        self.leaveEvent(self)
        self.update()


    def enterEvent(self, event):
        if self.Checked:
            self.icon_.setStyleSheet("QLabel {background-color: #3183c5; border-radius: 2px;border: 0px; color: #a2a2a2;}")
        else:
            self.icon_.setStyleSheet("QLabel {background-color: transparent; border-radius: 2px;border: 2px solid #2B98F0; color: #a2a2a2;}")


    def leaveEvent(self, event):
        if self.Checked:
            self.icon_.setStyleSheet("QLabel {background-color: #2B98F0; border-radius: 2px;border: 0px; color: #a2a2a2;}")
        else:
            self.icon_.setStyleSheet("QLabel {background-color: transparent; border-radius: 2px;border: 2px solid #6F6F6F; color: #a2a2a2;}")

    def mousePressEvent(self, event):
        if self.Checked:
            self.Checked = 0
            self.icon_.setPixmap(QPixmap(None))
            self.icon_.setStyleSheet("QLabel {background-color: #2B98F0; border-radius: 2px;border: 0px; color: #a2a2a2;}")
        else:
            self.Checked = 1
            self.icon_.setPixmap(QPixmap(self.path_))
            self.icon_.setStyleSheet("QLabel {background-color: transparent; border-radius: 2px;border: 2px solid #6F6F6F; color: #a2a2a2;}")

        self.enterEvent(self)
        self.update()

        self.parent.write_settings()


def widgets_at(pos):
    widgets = []
    widget_at = app.widgetAt( pos )

    while widget_at:
        widgets.append( widget_at )

        # Make widget invisible to further enquiries
        widget_at.setAttribute( Qt.WA_TransparentForMouseEvents )
        widget_at = app.widgetAt( pos )

    # Restore attribute
    for widget in widgets:
        widget.setAttribute( Qt.WA_TransparentForMouseEvents, False )
    return widgets





class ms_about_win(QDialog):

    def __init__(self, parent=None):
        super(ms_about_win,self).__init__(parent)

        self.setMinimumWidth(480)
        self.setMinimumHeight(260)
        self.setObjectName('PolygonFlowTool')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)


        self.StandardStyle = ("""
        QDialog#PolygonFlowTool
        {
            background-color: #1A1A1A;
            border-radius: 8px;
            border: 3px solid #2c2d2e;
        }        """)

        self.setStyleSheet(self.StandardStyle)


        # Set the main layout
        self.MainLayout = QVBoxLayout()
        self.setLayout(self.MainLayout)
        # self.MainLayout.setAlignment(Qt.AlignTop)
        self.MainLayout.setSpacing(0)
        self.MainLayout.setContentsMargins(20, 20, 20, 20)


        # Set the top layout
        self.top_layout = QHBoxLayout()
        #self.top_layout.setAlignment(Qt.AlignTop)
        self.MainLayout.addLayout(self.top_layout)
        self.top_layout.setSpacing(8)
        self.top_layout.setContentsMargins(0, 0, 0, 0)

        # Set the top layout
        self.close_layout = QHBoxLayout()
        self.top_layout.addLayout(self.close_layout)
        self.close_layout.setAlignment(Qt.AlignRight)
        self.close_layout.setSpacing(8)
        self.close_layout.setContentsMargins(0, 0, 0, 0)

        self.close_ui = QBaseButton("close")
        self.close_layout.addWidget(self.close_ui)
        self.close_ui.clicked.connect(self.cancel)

        style_ = ("QLabel {background-color: transparent; font-size: 11pt; font-family: Ubuntu; Source Sans Pro: 0px;color: #ffffff;}")
        style_2 = ("QLabel {background-color: transparent; font-size: 11pt; font-family: Ubuntu; Source Sans Pro: 0px;color: #a4a4a4;}")

        self.a_01 = QLabel("Quixel Megascans - Unreal Engine Integration")
        self.a_01.setAlignment(Qt.AlignTop|Qt.AlignCenter)
        self.a_01.setStyleSheet(style_)
        self.MainLayout.addWidget(self.a_01)

        self.a_02 = QLabel("Adnan Chaumette - Fahad Yaqub - Umar Farooq - Teddy Bergsman\n - Zuneira Elahi - Mohammed Hassan - Wiktor Öhman\n and all the Quixel staff")
        self.a_02.setAlignment(Qt.AlignTop|Qt.AlignCenter)
        self.a_02.setStyleSheet(style_2)
        self.MainLayout.addWidget(self.a_02)

        self.a_03 = QLabel()
        self.a_03.setText("<a href=\"https://github.com/20tab/UnrealEnginePython\" style=\"color: #2B98F0;\">Made in Python with UnrealEnginePython</a>")
        self.a_03.setOpenExternalLinks(True)
        self.a_03.setAlignment(Qt.AlignTop|Qt.AlignCenter)
        self.a_03.setStyleSheet(style_)
        self.MainLayout.addWidget(self.a_03)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def cancel(self):
        self.close()

    def paintEvent(self, pe):
        opt = QStyleOption()
        opt.init(self)
        p = QPainter(self)
        s = self.style()
        s.drawPrimitive(QStyle.PE_Widget, opt, p, self)









class megascans_livelink_ui(QDialog):

    def __init__(self):
        super(megascans_livelink_ui, self).__init__(None)

        self.UI_Win = None

        self.State = True
        # self.parent_hwnd = ue_editor_hwnd
        # self.hwnd = self.winId()
        # print(self.hwnd)
        # self._parent_to_main_window()
        self.StandardStyle = ("""
        QDialog#megascans_livelink_ui
        {
            background-color: #1A1A1A;
            border-radius: 0px;
            font-size: 16px;
            border: 3px solid #2c2d2e;
        }
        QToolTip
{
    border: 1px solid #2c2d2e;
    text-align: center;
    color: #ffffff;
    padding: 2px 2px 2px 2px;
    font-size: 16px;
    font-family: Source Sans Pro;
    background-color: #333333;
    border-radius: 5px;
    min-height: 30px;

}        """)


        self.setStyleSheet(self.StandardStyle)

        self.setFixedWidth(270)
        self.setFixedHeight(260)

        self.setObjectName('megascans_livelink_ui')
        self.setWindowIcon(QIcon((megascans_fldr + '/MS_Logo.png')))
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setMask(self.geometry())
        self.setWindowOpacity(1)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set the main layout
        self.MainLayout = QVBoxLayout()
        self.setLayout(self.MainLayout)
        # self.MainLayout.setAlignment(Qt.AlignTop)
        self.MainLayout.setSpacing(12)
        self.MainLayout.setContentsMargins(15, 15, 15, 15)


        # Set the top layout
        self.top_layout = QHBoxLayout()
        self.top_layout.setAlignment(Qt.AlignTop)
        self.MainLayout.addLayout(self.top_layout)
        self.top_layout.setSpacing(8)
        self.top_layout.setContentsMargins(0, 0, 0, 0)

        self.top_icon_layout = QHBoxLayout()
        self.top_layout.addLayout(self.top_icon_layout)
        self.top_icon_layout.setAlignment(Qt.AlignLeft)
        self.top_icon_layout.setSpacing(8)
        self.top_icon_layout.setContentsMargins(0, 0, 0, 0)

        self.logo_ = QPushButton("")
        self.logo_.setIcon( QIcon(QPixmap(megascans_fldr + '/MS_Logo.png')))
        self.logo_.setIconSize(QSize(35, 35))
        self.logo_.setStyleSheet(Action_Style)
        self.logo_.clicked.connect(self.ms_menu)
        self.top_icon_layout.addWidget(self.logo_)

        # self.log = QLabel("Megascans LiveLink 1.0")
        # self.log.setAlignment(Qt.AlignLeft|Qt.AlignCenter)
        # # self.log.setFixedWidth(175)
        # self.log.setStyleSheet("QLabel {background-color: transparent; font-size: 11pt; font-family: Source Sans Pro; border: 0px; color: #ffffff;}")
        # self.top_layout.addWidget(self.log)

        # Set the top layout
        self.close_layout = QHBoxLayout()
        self.top_layout.addLayout(self.close_layout)
        self.close_layout.setAlignment(Qt.AlignRight)
        self.close_layout.setSpacing(8)
        self.close_layout.setContentsMargins(0, 0, 0, 0)

        self.minimizewin_ = QBaseButton("minimize")
        self.minimizewin_.setToolTip("Minimize the Megascans LiveLink window")
        self.close_layout.addWidget(self.minimizewin_)
        self.minimizewin_.clicked.connect(lambda: self.showMinimized())

        self.close_ui = QBaseButton("close")
        self.close_ui.setToolTip("Close the Megascans LiveLink window. You can reopen it \nby clicking on the Megascans icon in the toolbar")
        self.close_layout.addWidget(self.close_ui)
        self.close_ui.clicked.connect(self.cancel)


        # Set the material layout
        self.mtrl_layout = QHBoxLayout()
        self.MainLayout.addLayout(self.mtrl_layout)
        self.mtrl_layout.setSpacing(5)
        self.mtrl_layout.setContentsMargins(0, 0, 0, 0)


        self.assets_layout = QHBoxLayout()
        self.mtrl_layout.addLayout(self.assets_layout)
        self.assets_layout.setAlignment(Qt.AlignLeft)
        self.assets_layout.setSpacing(5)
        self.assets_layout.setContentsMargins(0, 0, 0, 0)

        self.obj_type = QComboBox()
        self.obj_type.setToolTip("Scroll or click over to show the \nsupported material types per category")
        self.obj_type.setStyleSheet(material_style)
        self.assets_layout.addWidget(self.obj_type)
        self.obj_type.setMinimumHeight(32)
        self.obj_type.currentIndexChanged.connect(self.Change_Material_ui)
        for item in [item[0] for item in ms_mainclass.materials]:
            self.obj_type.addItem(item)


        self.mat_layout = QHBoxLayout()
        self.mtrl_layout.addLayout(self.mat_layout)
        self.mat_layout.setAlignment(Qt.AlignRight)
        self.mat_layout.setSpacing(5)
        self.mat_layout.setContentsMargins(0, 0, 0, 0)

        self.set_new = QBaseButton("set")
        self.set_new.setToolTip("Use the selected material in the content browser a\n as the default material for the current asset type.")
        self.mat_layout.addWidget(self.set_new)
        self.set_new.clicked.connect(self.set_new_mat)

        self.locate_browser = QBaseButton("search")
        self.locate_browser.setToolTip("Highlight the material in the content browser")
        self.mat_layout.addWidget(self.locate_browser)
        self.locate_browser.clicked.connect(self.sync_mtl_browser)


        self.reset_mat = QBaseButton("reset")
        self.reset_mat.setToolTip("Reset the selected type to it's default material")
        self.mat_layout.addWidget(self.reset_mat)
        self.reset_mat.clicked.connect(self.reset_new_mat)


        self.mtl_name = QMaterialDisplay(ms_mainclass.materials[0][1], self)
        self.mtl_name.setToolTip("This material is currently used for all assets\n of the currently selected type")
        # self.mtl_name.setMinimumHeight(32)
        # self.mtl_name.setMinimumWidth(200)
        # self.mtl_name.setStyleSheet("QLabel {background-color: #2c2f31; border-radius: 3px; font-size: 16px; font-family: Source Sans Pro; border: 2px solid #505B63; color: #a2a2a2; padding: 1px 1px 1px 5px;}")
        self.MainLayout.addWidget(self.mtl_name)

        with open(ms_return_path() + '/megascans/settings.json') as f:
                    data = f.read()
        settings_ = json.loads(data)

        # Set the checkbox list layout
        self.options_layout = QVBoxLayout()
        self.MainLayout.addLayout(self.options_layout)
        # self.options_layout.setAlignment(Qt.AlignRight)
        self.options_layout.setSpacing(10)
        self.options_layout.setContentsMargins(0, 0, 0, 0)

        self.apply_2_sel = QCustomCheckBox('  Apply Surfaces to Selection', settings_['Surface2Selection'], self)
        self.apply_2_sel.setToolTip('Automatically apply imported surfaces to the current selection in the editor')
        self.options_layout.addWidget(self.apply_2_sel)

        self.auto_foliage = QCustomCheckBox('  Auto-Populate Foliage Painter', settings_['AutoFoliage'], self)
        self.auto_foliage.setToolTip('Automatically import foliage assets in the foliage editor')
        self.options_layout.addWidget(self.auto_foliage)

        # self.blend_mat = QCustomCheckBox('  Enable Blended Materials Workflow', self)
        # self.blend_mat.setToolTip('Create material blends for surfaces and 3D assets on import.\n This combines n imported assets into a blend material, giving you an ideal\n workflow for vertex painting')
        # self.options_layout.addWidget(self.blend_mat)

        # self.lod_setup = QCustomCheckBox('  Auto-Create LOD Setup', self)
        # self.lod_setup.setToolTip('Create the LOD setup of 3D imported Megascans assets')
        # self.options_layout.addWidget(self.lod_setup)

        # Set the Tiling layout
        # self.tile_layout = QHBoxLayout()
        # self.MainLayout.addLayout(self.tile_layout)
        # self.tile_layout.setAlignment(Qt.AlignBottom)
        # self.tile_layout.setSpacing(12)
        # self.tile_layout.setContentsMargins(0, 0, 0, 0)

        # self.tile = QLabel('Tiling')
        # self.tile.setToolTip('Get all material instances in selection and change their "Tiling" parameter')
        # self.tile.setStyleSheet("QLabel {background-color: transparent; font-size: 16px; font-family: Source Sans Pro; border: 0px; color: #ffffff;}")
        # self.tile_layout.addWidget(self.tile)

        # self.Tiling_Sldr = QSlider(Qt.Horizontal)
        # self.Tiling_Sldr.setToolTip('Get all material instances in selection and change their "Tiling" parameter')
        # self.Tiling_Sldr.setStyleSheet(tiling_slider_style)
        # self.Tiling_Sldr.setMinimum(1)
        # self.Tiling_Sldr.setMaximum(50)
        # self.Tiling_Sldr.setTickInterval(1)
        # self.Tiling_Sldr.setValue(1)
        # self.Tiling_Sldr.sliderMoved.connect(self.update_tiling)
        # self.Tiling_Sldr.valueChanged.connect(self.update_tiling)

        # self.tile_layout.addWidget(self.Tiling_Sldr)

        # # Set the Scaling layout
        # self.scale_layout = QHBoxLayout()
        # self.MainLayout.addLayout(self.scale_layout)
        # self.scale_layout.setAlignment(Qt.AlignBottom)
        # self.scale_layout.setSpacing(12)
        # self.scale_layout.setContentsMargins(0, 0, 0, 0)

        # self.scale_ = QLabel('Scale')
        # self.scale_.setToolTip('Scale selected assets')
        # self.scale_.setStyleSheet("QLabel {background-color: transparent; font-size: 16px; font-family: Source Sans Pro; border: 0px; color: #ffffff;}")
        # self.scale_layout.addWidget(self.scale_)

        # self.scale_Sldr = QSlider(Qt.Horizontal)
        # self.scale_Sldr.setToolTip('Scale selected assets')
        # self.scale_Sldr.setStyleSheet(tiling_slider_style)
        # self.scale_Sldr.setMinimum(1)
        # self.scale_Sldr.setMaximum(50)
        # self.scale_Sldr.setTickInterval(1)
        # self.scale_Sldr.setValue(1)
        # self.scale_Sldr.sliderMoved.connect(self.update_scale)
        # self.scale_Sldr.valueChanged.connect(self.update_scale)

        # self.scale_layout.addWidget(self.scale_Sldr)



        # Set the livelink layout
        self.blend_workflow = QHBoxLayout()
        self.MainLayout.addLayout(self.blend_workflow)
        self.blend_workflow.setAlignment(Qt.AlignBottom)
        self.blend_workflow.setSpacing(8)
        self.blend_workflow.setContentsMargins(0, 0, 0, 0)

        # self.pause_l_link = QPushButton("Create Blend")
        # self.pause_l_link.setStyleSheet(Pause_Style)
        # self.blend_workflow.addWidget(self.pause_l_link)
        # self.pause_l_link.setMinimumHeight(30)
        # self.pause_l_link.clicked.connect(self.LiveLink_State)

        self.create_blend = QPushButton("Create Material Blend")
        self.create_blend.setStyleSheet(Pause_Style)
        self.blend_workflow.addWidget(self.create_blend)
        self.create_blend.setMinimumHeight(30)
        self.create_blend.clicked.connect(self.create_blend_mat)


    # def get_hwnd(self):
    #     """Get the HWND window handle from this QtWidget."""
    #     ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
    #     ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
    #     wdgt_ptr = ctypes.pythonapi.PyCObject_AsVoidPtr(self.winId())
    #     return wdgt_ptr

    # def _parent_to_main_window(self):
        # SetWindowLongPtr(self.hwnd, GWL_HWNDPARENT, self.parent_hwnd)

    def show_win(self):
        if self.UI_Win is None:
            self.UI_Win = megascans_livelink_ui()
        self.UI_Win.show()

    def create_blend_mat(self):
        ms_materialblend_setup("create")

    def update_blend_mat(self):
        ms_materialblend_setup("update")

    def LiveLink_State(self):
        if self.pause_l_link.text().lower() == 'pause livelink':
            self.pause_l_link.setText('Start LiveLink')
        else:
            self.pause_l_link.setText('Pause LiveLink')

    def widgets_under_cursor(pos):
        widgets = []
        widget_at = app.widgetAt( pos )

        while widget_at:
            widgets.append( widget_at )

            # Make widget invisible to further enquiries
            widget_at.setAttribute( Qt.WA_TransparentForMouseEvents )
            widget_at = app.widgetAt( pos )

        # Restore attribute
        for widget in widgets:
            widget.setAttribute( Qt.WA_TransparentForMouseEvents, False )
        return widgets

    def mousePressEvent(self, event):
        try:
            self.mouselock = None
            if megascans_livelink_ui.widgets_under_cursor(QCursor.pos())[0] == self:
                self.mouselock = True
                self.offset = event.pos()
            else:
                self.mouseReleaseEvent()
        except:
            pass

    def mouseMoveEvent(self, event):
        try:
            if self.mouselock == True:
                x=event.globalX()
                y=event.globalY()
                x_w = self.offset.x()
                y_w = self.offset.y()
                self.move(x-x_w, y-y_w)
        except:
            pass

    def mouseReleaseEvent(self, event):
        try:
            self.mouselock = None
            self.offset = event.pos()
        except:
            pass

    def cancel(self):
        self.State = False
        self.close()

    def closeEvent(self, event):
        self.State = False
        self.close()

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(megascans_livelink_ui, self).keyPressEvent(event)

    def paintEvent(self, pe):
        opt = QStyleOption()
        opt.init(self)
        p = QPainter(self)
        s = self.style()
        s.drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def write_settings(self):

        with open(ms_return_path() + '/megascans/settings.json') as f:
                    data = f.read()
        settings_ = json.loads(data)

        settings_['Surface2Selection'] = self.apply_2_sel.Checked
        settings_['AutoFoliage'] = self.auto_foliage.Checked
        #settings_['BlendMaterial'] = self.blend_mat.Checked
        #settings_['LODSetup'] = self.lod_setup.Checked
        #settings_['Tiling'] = float(self.Tiling_Sldr.value())/10

        Export_ = json.dumps(settings_, sort_keys=True, ensure_ascii=False, indent=2)

        file_ = open((ms_return_path() + '/megascans/settings.json'), "w+")
        file_.write(Export_)
        file_.close()

    def Change_Material_ui(self):

        try:
            indx_ = self.obj_type.currentIndex()
            self.mtl_name.setText(ms_mainclass.materials[indx_][1])
        except:
            pass

    def sync_mtl_browser(self):

        try:
            cur_ = ms_mainclass.materials[self.obj_type.currentIndex()]
            parent_path = '/Game/Megascans/Master_Materials/' if len(cur_) <= 2 else cur_[2]
            mastermat_ = (self.mtl_name.text())
            folder_content = ue.get_assets('/Game/Megascans/Master_Materials')

            end_array = []

            for mat_ in folder_content:
                if mat_.is_a(Material) and mat_.get_name().lower() == mastermat_.lower():
                    end_array.append(mat_)
                    break

            ue.sync_browser_to_assets(end_array)

        except:
            print('error in Change_Material_ui function...')
            pass

    def update_scale(self):

        try:
            value_ = self.scale_Sldr.value()
            scaledValue = float(value_)/10

            actors_ = ue.editor_get_selected_actors()
            if len(actors_) >= 1:
                for actor_ in actors_:
                    if actor_.is_a(StaticMeshActor):
                        actor_.set_actor_scale(scaledValue, scaledValue, scaledValue)

            self.write_settings()

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(' Error Info : ' + str(exc_value))
            print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            pass


    def update_tiling(self):

        get_sel = ue.editor_get_selected_actors()

        value_ = self.Tiling_Sldr.value()
        scaledValue = float(value_)/10

        if len(get_sel) >= 1:
            for sel in get_sel:
                try:
                    if sel.is_a(StaticMeshActor):
                        mtl = sel.get_property('StaticMeshComponent').get_property('OverrideMaterials')
                        if len(mtl) >= 1:
                            mtl = mtl[0]
                            mtl.set_material_scalar_parameter('Tiling', 1)
                            mtl.set_material_scalar_parameter('Tiling', scaledValue)

                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print(' Error Info : ' + str(exc_value))
                    print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    pass


    def set_new_mat(self):

        indx_ = self.obj_type.currentIndex()
        input_ = (ms_mainclass.materials[indx_][0])


        with open(ms_return_path() + '/megascans/settings.json') as f:
            settings_ = json.loads(f.read())

        actors = ue.get_selected_assets()

        package_, package_name = None, None

        if len(actors) >= 1:
            for actor in actors:
                package_name, package_ = actor.get_outer().get_name(), actor

        if package_ != None and package_.is_a(Material):

            obj_mat = [item for item in settings_['CustomMaterial'] if item[0].lower() == input_.lower()][0]

            mat_indx = settings_['CustomMaterial'].index(obj_mat)

            if package_name != None and len(obj_mat) >= 2:

                obj_mat[1] = os.path.basename(package_name)
                if len(obj_mat) == 3:
                    obj_mat[2] = (os.path.dirname(package_name)) + '/'
                else:
                    obj_mat.append(os.path.dirname(package_name) + '/')

            settings_['CustomMaterial'][mat_indx] = obj_mat

            Export_ = json.dumps((dict(settings_)), sort_keys=True, ensure_ascii=False, indent=2)

            file_ = open((ms_return_path() + '/megascans/settings.json'), "w+")
            file_.write(Export_)
            file_.close()

            print(obj_mat[0] + ' is now the default material of object type ' + obj_mat[1])

            ms_mainclass.materials[indx_][1] = obj_mat[1]
            self.mtl_name.setText(ms_mainclass.materials[indx_][1])


    def reset_new_mat(self):

        indx_ = self.obj_type.currentIndex()
        input_ = (ms_mainclass.materials[indx_][0])

        with open(ms_return_path() + '/megascans/settings.json') as f:
            settings_ = json.loads(f.read())

        obj_mat = [item for item in settings_['CustomMaterial'] if item[0].lower() == input_.lower()][0]

        mat_indx = settings_['CustomMaterial'].index(obj_mat)

        settings_['CustomMaterial'][mat_indx] = settings_['DefaultMaterials'][mat_indx]

        Export_ = json.dumps((dict(settings_)), sort_keys=True, ensure_ascii=False, indent=2)

        file_ = open((ms_return_path() + '/megascans/settings.json'), "w+")
        file_.write(Export_)
        file_.close()

        ms_mainclass.materials[indx_][1] = obj_mat[1]
        self.mtl_name.setText('')
        self.mtl_name.setText(ms_mainclass.materials[indx_][1])


    def ms_menu(self):

        menu = QMenu(self)
        menu.setStyleSheet(PrefsMenuStyle)

        always_top =  QAction('Toggle Always On Top', self)

        open_ms_se =  QAction('Visit Megascans.se', self)

        open_doc =  QAction('Documentation', self)

        about_ =  QAction('About', self)

        menu.addAction(always_top)
        # menu.addSeparator()
        menu.addAction(open_ms_se)
        # menu.addSeparator()
        menu.addAction(open_doc)
        # menu.addSeparator()
        menu.addAction(about_)


        action = menu.exec_(QCursor.pos())

        if action == always_top:
            self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)
            self.show()

        if action == open_ms_se:
            webbrowser.open('https://megascans.se/')

        if action == open_doc:
            webbrowser.open('https://d3uwib8iif8w1p.cloudfront.net/bridge/plugins/Megascans_Bridge_Unreal_Integration.pdf')

        if action == about_:
            self.aboutwin = ms_about_win()
            self.aboutwin.show()



##########################################################################################
##########################################################################################
##########################################################################################



#time.sleep(2)
# handle = ctypes.windll.user32.GetForegroundWindow()
# PID = ctypes.windll.kernel32.GetProcessId(handle)

def ui_ticker_loop(delta_time):
    try:
        loop.stop()
        loop.run_forever()
    except Exception as e:
        ue.log_error(e)
    return True


async def ui_simple_timer(frequency, base_handle, window):
    while True:
        try:
            await asyncio.sleep(frequency)

            if not window.State:
                print("Megascans UI closed...")
                break
                
            handle = ctypes.windll.user32.GetForegroundWindow()
            if handle != base_handle and handle != window.winId():
                try:
                    #print(handle, base_handle)
                    window.hide()
                    #window.setWindowState(Qt.WindowMinimized)
                except:
                    pass
            else:
                try:
                    #print(handle, base_handle)
                    #window.setWindowState(Qt.WindowNoState)
                    window.show()
                except:
                    pass

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(' Error Info : ' + str(exc_value))
            print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            print("Encountered error during asyncIO listener, closing all open ports...")
            break





for win in app.topLevelWidgets():
    win.close()

# Set our PySide2 event loop.

def _qt_event_loop():
    app.processEvents()
    app.sendPostedEvents(None, 0)

ue.add_ticker(_qt_event_loop, 10)


win = megascans_livelink_ui()

# ms_mainclass.main_win = win

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)

# ticker = ue.add_ticker(ui_ticker_loop)

# cur_handle = ctypes.windll.user32.GetForegroundWindow()

# asyncio.ensure_future(ui_simple_timer(0.1, cur_handle, win))

win.show_win()

# ms_form_base_structure()






