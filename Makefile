OUTDIR :=out
TSV:=resistors.tsv
all :
	./generate_svg_resistors.py $(OUTDIR)/ $(TSV)

readme.html : readme.md
	cmark "$<" > "$@"

clean :
	rm -- $(TSV) $(OUTDIR)/*.svg


INSTALLDIR:=$(HOME)/.local/share/Anki2/Nathaniel/collection.media
install :
	cp $(OUTDIR)/*.svg $(INSTALLDIR)/
