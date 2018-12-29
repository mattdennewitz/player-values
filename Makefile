run:
	poetry run python calc.py

viewb:
	jq . final-b.json | less

viewp:
	jq . final-p.json | less
