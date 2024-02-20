import webbrowser

#webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(r"C:\Users\Addy\AppData\Local\Google\Chrome\Application\chrome.exe"))

b = ""

def default(a, b):
	print(a)
	function_dict = {'help':help}
	if b != "":
		function_dict[b](a)
	else:
		a.insert("end-1c", "this is the store plugin write 'store help' for help" + '\n','warning')

def help(a):
	a.insert("end-1c", "this is the store plugin it will find an item you want on the web for the cheapest and best quality" + '\n','warning')
