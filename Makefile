INTELLIJ_NAME='IntelliJ\ IDEA'
GOLAND_NAME='GoLand'
WEBSTORM_NAME='WebStorm'
CLION_NAME='CLion'
INTELLIJ_KEYWORD='idea'
GOLAND_KEYWORD='goland'
WEBSTORM_KEYWORD='webstorm'
CLION_KEYWORD='clion'
APPS=INTELLIJ GOLAND CLION WEBSTORM

.PHONY: clean build

all: clean build

clean:
	rm -fr out *.alfredworkflow

build: $(APPS)

$(APPS):%:
	mkdir -p out/$($@_KEYWORD)
	sed -e 's/%APPNAME%/$($@_NAME)/g;s/%KEYWORD%/$($@_KEYWORD)/g' alfred/info.plist > out/$($@_KEYWORD)/info.plist
	zip -j -r $($@_KEYWORD).alfredworkflow out/$($@_KEYWORD)/info.plist recent_projects.py

