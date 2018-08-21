OUTDIR :=out
TSV:=resistors.tsv
all :
	./generate_svg_resistors.py $(OUTDIR)/ $(TSV)

clean :
	rm -- $(OUTDIR)/*.svg
