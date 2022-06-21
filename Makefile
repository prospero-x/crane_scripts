
all: report

.PHONY: report
report:
	pdflatex -jobname="Rezazadeh_Mikhail_Module_3_Project" \
	-output-directory=report report/report.tex

.PHONY: dist
dist:
	./make_dist.sh

clean:
	rm -rf dist
