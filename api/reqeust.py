def params():
    r = requests.get("https://www.metoffice.gov.uk/research/climate/maps-and-data/uk-and-regional-series")
    soup = BeautifulSoup(r.content, 'html.parser')
    region = soup.find(id='region')
    region_list = region.find_all("option")
    for i in region_list:
        print(i['value'])
    parameter = soup.find(id='parameter')
    param_list = parameter.find_all("option")
    for i in param_list:
        print(i['value'])
    