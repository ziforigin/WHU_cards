# WHU_cards

1) Install Python3 on your mac like in this article:
https://docs.python-guide.org/starting/install3/osx/

2) run from terminal in WHU_Cards folder the following:
pip install -r requirements.txt

3) now you are ready to use the program! run:
pytest -s -v main.py

To add decks you want to download, add them to WHU_cards/resources/decks_list.json

To change width\height\number of cards on a sheet change settings in WHU_cards/resources/config.json

All output will be stored in WHU_cards/output
Sheets for printing in WHU_cards/output/for_printing
