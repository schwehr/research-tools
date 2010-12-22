ORGS := 
ORGS += introduction.org
ORGS += communication.org
ORGS += choosing-a-text-editor.org
ORGS += choosing-a-programming-language.org
ORGS += command-line.org
# ORGS += concept.org
ORGS += databases.org
# ORGS += intro-to-python-part2.org
ORGS += python-intro.org
ORGS += intro-to-python-part2.org
ORGS += python-binary-files.org
ORGS += revision-control.org

HTMLS := $(ORGS:.org=.html)

list_html:
	@for html in ${HTMLS}; do echo $$html; done

default:
	scp command-line.{org,html} vislab-ccom:www/Classes/2011/esci895-researchtools/
