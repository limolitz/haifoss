PYBOARD_PATH=./Inkplate-micropython/pyboard.py
DEVICE=/dev/ttyUSB0
CALL=python $(PYBOARD_PATH) --device $(DEVICE)

run:
	$(CALL) screen.py

copy:
	$(CALL) config.json screen.py ./Inkplate-micropython/inkplate10.py :

.PHONY: run
