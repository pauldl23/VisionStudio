' ===========================================================================
' VisionStudio | Premium Web Launcher
' ===========================================================================
' This script launches the VisionStudio Dashboard in the background and
' opens your default web browser to the application interface.
' ===========================================================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
strPath = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strPath

' Launch the application via the batch file (hidden)
WshShell.Run "cmd /c run.bat", 0, False

' Wait for the server to initialize
' We wait slightly longer to ensure the old process is killed and new one starts
WScript.Sleep 5000

' Open the application in the default web browser
WshShell.Run "http://localhost:8501"

' Optional: Show a small notification
' WshShell.Popup "VisionStudio is now running in the background.", 3, "VisionStudio Launcher", 64
