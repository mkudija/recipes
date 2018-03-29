PY?=python3

help:
	@echo '                                                                          '
	@echo 'Makefile to build static website                                          '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                                                              '
	@echo '   <verify you like the changes that were made>                           '
	@echo '   make publish                                                           '
	@echo '                                                                          '
	@echo 'Commands:                                                                 '
	@echo '   make html                regenerate the websites                       '
	@echo '   make publish             publish regenerated websites to GitHub        '
	@echo '                                                                          '

html:
	python build.py


publish:
	@echo ' '
	git pull origin master
	git add -A
	git commit -m "auto-regenerate from make"
	git push origin master

	@echo 'Done.'