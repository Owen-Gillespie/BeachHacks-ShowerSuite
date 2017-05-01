import seek
DOMAIN = "seek.com"

start = seek.StartModule("""<p> HI!</p><img src="/static/img/beach_hacks_logo.png" alt="Giant Glass Pyramid">""", "test1")
test1 = seek.TextModule('test1', "textinput", "BYE!")
test2 = seek.TextInputModule("textinput", "showersuite", "Test!")
test2 = seek.GPSModule("showersuite", "findtest", "1.775", "2.7775")
test3 = seek.FindObjectModule("findtest", "matchtest", "dog")
test4 = seek.ImageMatchModule("matchtest", "qrtest", "image/base.JPG")
test5 = seek.QRModule("qrtest", "<p>This page should have no continue button</p>", "end", DOMAIN)

seek.save_module_data()
