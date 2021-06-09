from setuptools import setup

setup(
    name="apksideloader",
    version="0.2",
    license="GPLv3+",
    description="A tool to sideload Android packages onto Chromebooks",
    keywords="android apk sideload",
    # From https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Development status
        "Development Status :: 3 - Alpha",
        # Target audience
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        # Type of software
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Software Distribution",
        # Kind of software
        "Environment :: Console",
        "Environment :: X11 Applications :: GTK",
        # License (must match license field)
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        # Operating systems supported
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        # Supported Python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    url="http://github.com/sgallagher/apksideloader",
    author="Stephen Gallagher",
    author_email="Stephen@gallagherhome.com",
    packages=["apksideloader"],
    include_package_data=True,
    install_requires=[
        "Click>=7.0.0",
        "adb-shell",
        "PyGObject>=3.30.4",
    ],
    entry_points={
        "console_scripts": [
            "apksideloader = apksideloader.cli:main",
        ],
    },
    data_files=[
        ('share/applications', ['data/com.gallagherhome.apksideloader.desktop']),
        ('share/icons', ['data/icons/hicolor/192x192/android_icon.png']),
    ],
)
