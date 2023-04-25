import main
from config import group_names, domains_names

domains = main.get_domains()
#for domain in domains:
    #print(domain['domain'])

for domain in domains_names:
    print(domain['name'])