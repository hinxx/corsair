SUBDIRS := $(wildcard */.)

export PYTHONPATH := ../../../.:$(PYTHONPATH)

all: run

run:
	python3 top.py

clean:
	@rm -rf *.v *.md *_img __pycache__

.PHONY: all run clean