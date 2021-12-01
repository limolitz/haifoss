PYBOARD_PATH=./Inkplate-micropython/pyboard.py
DEVICE=/dev/ttyUSB0
CALL=python $(PYBOARD_PATH) --device $(DEVICE)

run:
	$(CALL) screen.py

copy:
	$(CALL) -f cp __init__.py config.json screen.py ./Inkplate-micropython/inkplate10.py ./Inkplate-micropython/gfx.py ./Inkplate-micropython/gfx_standard_font_01.py ./Inkplate-micropython/sdcard.py ./Inkplate-micropython/mcp23017.py ./Inkplate-micropython/shapes.py boot.py :

.PHONY: run
