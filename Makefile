NAME := nethserver-zabbix-agent-checks
VER := 1.0.0
FILES := $(shell cat filelist)

default: build

pack:
	rm -f $(NAME)-$(VER).tar.gz
	tar czf $(NAME)-$(VER).tar.gz $(FILES)

build:
	drone exec .drone.yml

clean:
	rm -f $(NAME)-$(VER).tar.gz
	rm -rf out

.PHONY: pack build clean
