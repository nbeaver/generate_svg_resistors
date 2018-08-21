OUTDIR :=out
all :
	./generate_svg_resistors.py $(OUTDIR)/

clean :
	rm -- $(OUTDIR)/*.svg
