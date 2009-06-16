# All text files written in restructured text needs to go in the following list
SRC=host-spotlight-ui-spec.txt \
	scope-dom-interface.txt \
	scope-stp1-services.txt \
	scope-transport-protocol.txt \
	style-guide-stp1.txt \
	unified-message-structure.txt

OUTDIR=out/#/var/www/html/scope-interface
HTML=$(SRC:%.txt=$(OUTDIR)/%.html)

all: $(HTML)

$(OUTDIR)/%.html: %.txt
	@mkdir -p $(OUTDIR)
	rst2html --initial-header-level=2 --stylesheet-path="coredoc.css" --link-stylesheet $? > $@

clean:
	rm -f $(HTML)

