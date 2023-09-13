SUBDIRS := $(wildcard */.)

export PYTHONPATH := ../../.:$(PYTHONPATH)

# all: generate build
all: build

generate:
	python3 -m corsair -t yaml

build:
	python3 -m corsair

clean:
	@rm -rf hw doc sw

.PHONY: all generate clean