run:
	poetry run python calc.py

view:
	jq . final-b.json | less
