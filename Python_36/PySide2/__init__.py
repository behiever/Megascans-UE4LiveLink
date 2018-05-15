__all__ = list("Qt" + body for body in
    "Core;Gui;Widgets;PrintSupport;Sql;Network;Test;Concurrent;WinExtras;Xml;XmlPatterns;Help;Multimedia;MultimediaWidgets;OpenGL;Qml;Quick;QuickWidgets;Script;ScriptTools;TextToSpeech;Charts;Svg;DataVisualization;UiTools;AxContainer;WebChannel;WebEngineWidgets;WebSockets"
    .split(";"))
__version__         = "2.0.0~alpha0"
__version_info__    = (2, 0, 0, "alpha", 0)

__build_date__ = '2018-01-19T18:21:08+00:00'
__build_commit_date__ = '2018-01-19T15:07:49+00:00'
__build_commit_hash__ = '7e94cd36121d4060d673c7307514e255851b7f1c'
__build_commit_hash_described__ = '2.0.0.dev0-5125-g7e94cd36'

def _setupQtDirectories():
    import sys
    import os
    from . import _utils

    os.environ["PYSIDE_PACKAGE_DIR"] = os.path.abspath(os.path.dirname(__file__))

    pysideDir = _utils.get_pyside_dir()

    # Register PySide qt.conf to override the built-in
    # configuration variables, if there is no default qt.conf in
    # executable folder
    prefix = pysideDir.replace('\\', '/')
    _utils.register_qt_conf(prefix=prefix,
                            binaries=prefix,
                            plugins=prefix+"/plugins",
                            imports=prefix+"/imports",
                            translations=prefix+"/translations")

    # On Windows add the PySide\openssl folder (if it exists) to the
    # PATH so the SSL DLLs can be found when Qt tries to dynamically
    # load them.  Tell Qt to load them and then reset the PATH.
    if sys.platform == 'win32':
        opensslDir = os.path.join(pysideDir, 'openssl')
        if os.path.exists(opensslDir):
            path = os.environ['PATH']
            try:
                os.environ['PATH'] = opensslDir + os.pathsep + path
                try:
                    from . import QtNetwork
                except ImportError:
                    pass
                else:
                    QtNetwork.QSslSocket.supportsSsl()
            finally:
                os.environ['PATH'] = path

_setupQtDirectories()
