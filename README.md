
This is a child project of [Paper in Economics](https://github.com/yoji0806/paper_in_economics).

# paper_scraper
A Python code to do a web scraping of academic papers and data from various sites.
 

## about Directory & Files

- `sample` : store sample python code in .ipynb format.  
- `*.py` : Any python file in the root directory is almost identical to the cloud's running code.

### ※note: 

`*.py ` in the root directory is not 100% the same as the cloud's running code because DB-related codes is hidden for security.  
If you will implement another web scraping code, please follow `scrapers_journal_aer.py` structue.   
It should have DOI as a variable, and the return type should be dict.


## Potential Bugs

Please refere [potentialBugs.md](./potentialBug.md).


## Style

### Docstrings
Please follow Google Style Python Docstrings.

- [Example Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/)


# Future Work （no particular order）
- collect lectures of Economics.
- make & open a spreadsheet that everyone can put materials on. -> move this spreadsheet to DB in the cloud.
- add other journals as resources.
- collect non-paper information in economics like, open-data, experimental data, about a professor...etc
- Reccomend feature.
- Note feature.
- Export feature.
