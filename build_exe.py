import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "json_to_srt.py",
        "--onefile",
        "--noconsole",
    ]
)
