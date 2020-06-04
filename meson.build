project(
    'apksideloader',
    version : '0.1',
    license : 'GPL3+',
    meson_version : '>=0.47.0',
)

pymod = import('python')
py = pymod.find_installation()

desktop_cdata = configuration_data()
desktop_cdata.set('PREFIX', get_option('prefix'))
desktop_cdata.set('BINDIR', get_option('bindir'))

configure_file(
    input: 'data/com.gallagherhome.apksideloader.desktop.in',
    output: 'com.gallagherhome.apksideloader.desktop',
    configuration: desktop_cdata,
    install_dir: join_paths(get_option('datadir'), 'applications'),
)

install_data(files('data/icons/hicolor/192x192/android_icon.png'), install_dir: 'share/icons/hicolor/192x192')

apksideloader_py_files = files(
    'apksideloader/__init__.py',
    'apksideloader/adb.py',
    'apksideloader/apk.py',
    'apksideloader/cli.py',
    'apksideloader/gui.py',
)

py.install_sources(apksideloader_py_files, subdir: 'apksideloader')
