SVG :=out.svg
all :
	./generate_svg_resistors.py $(SVG)

clean :
	rm -- $(SVG)
