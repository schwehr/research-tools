ORGS := 
ORGS += HEADER.org
ORGS += introduction.org
ORGS += communication.org
ORGS += choosing-a-text-editor.org
ORGS += choosing-a-programming-language.org
ORGS += command-line.org
ORGS += databases.org
ORGS += python-intro.org
ORGS += python-intro-from-matlab.org
ORGS += python-binary-files.org
ORGS += revision-control.org

HTMLS := $(ORGS:.org=.html)

list_html:
	@for html in ${HTMLS}; do echo $$html; done

CLASS_SCP := vislab-ccom.unh.edu:www/Classes/2011/esci895-researchtools/
push: 
	scp HEADER.html ${CLASS_SCP}
# FIX: Make this rsync!
#	scp ${HTMLS} ${ORGS} vislab-ccom:www/Classes/2011/esci895-researchtools/
#	scp figures/*.png vislab-ccom:www/Classes/2011/esci895-researchtools/figures/

missing:
	echo "Missing html files:"
	@for file in ${HTMLS}; do if [ ! -f $$file ]; then echo $$file; fi; done
