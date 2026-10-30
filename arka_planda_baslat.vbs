Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Calisma dizinini ayarla
WshShell.CurrentDirectory = currentDir

' Flask sunucusunu arka planda, siyah pencere OLMADAN baslat
WshShell.Run "cmd /c python app.py", 0, False

' Sunucunun hazir olmasi icin 1.5 saniye bekle
WScript.Sleep 1500

' Tarayicida siteyi ac
WshShell.Run "http://127.0.0.1:5000"

