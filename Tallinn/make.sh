#!/bin/bash
rm *.aux *.log *.lot *.lof *.toc
pdflatex main && pdflatex main && bibtex main && bibtex main && pdflatex main &&pdflatex main&& pdflatex main
