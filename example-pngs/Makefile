PNG :=resistor_00000000000.000ohm.png resistor_mirrored_00000004700.000ohm_5percent.png resistor_00000000100.000ohm_10percent.png
SVG :=$(patsubst %.png,../out/%.svg, $(PNG))
$(info $(SVG))

.PHONY : all
all: $(PNG)

%.png: ../out/%.svg Makefile
	convert -density 300 "$<" "$@"

.PHONY : clean
clean:
	rm -f -- $(PNG)
