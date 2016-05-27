# Some simple testing tasks (sorry, UNIX only).

FLAGS=


runserver:
	python -m eight_coupons

runscraper:
	python -m eight_coupons.scraper

flake:
	pyflakes eight_coupons
	pep8 eight_coupons

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf htmlcov
	rm -rf dist

.PHONY: flake clean
