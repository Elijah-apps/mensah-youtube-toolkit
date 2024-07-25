from cx_Freeze import setup, Executable

# Define the application executable
executables = [
    Executable(
        'app.py',  # Path to your main script
        base='Win32GUI',  # Use Win32GUI for a GUI application
        target_name='MensahYouTubeToolKit.exe',  # Correct argument for naming the output executable
        icon='icon.ico'
    )
]

# Include additional files or modules if needed
build_options = {
    'packages': ['PySide6', 'pytube', 'youtube_transcript_api'],  # Include necessary packages
    'excludes': [],
    'includes': [],
    'include_files': []  # Include any additional files here, if needed
}

# Setup the build
setup(
    name='MensahYouTubeToolKit',
    version='1.0',
    description='A tool for downloading YouTube videos, transcripts, and audio.',
    options={'build_exe': build_options},
    executables=executables
)
