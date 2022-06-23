ANDROIDSTUDIO_KEYWORD='androidstudio'
ANDROIDSTUDIO_NAME='Android\ Studio'
APPCODE_KEYWORD='appcode'
APPCODE_NAME='AppCode'
CLION_KEYWORD='clion'
CLION_NAME='CLion'
DATAGRIP_KEYWORD='datagrip'
DATAGRIP_NAME='DataGrip'
GOLAND_KEYWORD='goland'
GOLAND_NAME='GoLand'
INTELLIJ_KEYWORD='idea'
INTELLIJ_NAME='IntelliJ\ IDEA'
PYCHARM_KEYWORD='pycharm'
PYCHARM_NAME='PyCharm'
WEBSTORM_KEYWORD='webstorm'
WEBSTORM_NAME='WebStorm'
APPS=ANDROIDSTUDIO APPCODE CLION DATAGRIP GOLAND INTELLIJ PYCHARM WEBSTORM

.PHONY: clean build

all: clean build

clean:
	rm -fr out *.alfredworkflow

build: $(APPS)

$(APPS):%:
	mkdir -p out/$($@_KEYWORD)
	cp icons/$($@_KEYWORD).png ./out/$($@_KEYWORD)/icon.png
	cp icons/$($@_KEYWORD).png ./out/$($@_KEYWORD)/36E4312B-0CAB-4AE7-A8B6-E30EAF07B766.png
	sed -e 's/%APPNAME%/$($@_NAME)/g;s/%KEYWORD%/$($@_KEYWORD)/g' alfred/info.plist > out/$($@_KEYWORD)/info.plist
	zip -j -r $($@_KEYWORD).alfredworkflow out/$($@_KEYWORD)/* recent_projects.py products.json
