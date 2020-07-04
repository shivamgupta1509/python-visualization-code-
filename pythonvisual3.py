"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    converter_dict = {}
    with open(codeinfo["codefile"], "rt", newline="") as csvfile:
        csvreader = csv.DictReader(csvfile,
                                   delimiter=codeinfo["separator"], quotechar=codeinfo["quote"])
        for row in csvreader:
            converter_dict[row[codeinfo["plot_codes"]]] = row[codeinfo["data_codes"]]
    return converter_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    converter_dict = build_country_code_converter(codeinfo)
    convert_dict = {}
    for pcode, gcode in converter_dict.items():
        pcod = pcode.lower()
        convert_dict[pcod] = gcode.lower()
        
    join_dict = {}
    uncode_set = set()
    for plotc in plot_countries:
        flag = 0
        lplotc = plotc.lower()
        gdpcc = convert_dict[str(lplotc)]
        for gdpc in gdp_countries:
            if gdpcc == gdpc.lower():
                join_dict[plotc] = gdpc
                flag = 1
                break
        if flag == 0:
            uncode_set.add(plotc)            
    return(join_dict, uncode_set)


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_dict = {}
    with open(gdpinfo["gdpfile"], "rt", newline='') as csvfile:
        csvreader = csv.DictReader(csvfile,
                                   delimiter=gdpinfo["separator"], quotechar=gdpinfo["quote"])
        for row in csvreader:
            gdp_dict[row[gdpinfo["country_code"]]] = row
    tup = reconcile_countries_by_code(codeinfo, plot_countries, gdp_dict)
    joingdp_dict = {}
    nogdp_set = set()
    for plotc, gdpc in tup[0].items():
        if gdp_dict[gdpc][year] != '':
            gdp = math.log(float(gdp_dict[gdpc][year]), 10)
            joingdp_dict[plotc] = gdp
        else:
            nogdp_set.add(plotc)
    final_tup = (joingdp_dict, tup[1], nogdp_set)
    return final_tup
    

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    final_tup = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
    world_gdp = pygal.maps.world.World()
    title = "GDP by country for {} (log scale),unified by common country CODE".format(year)
    world_gdp.title = title
    world_gdp.add("GDP for {}".format(year), final_tup[0])
    world_gdp.add("Missing from world bank data", final_tup[1])
    world_gdp.add("NO GDP data", final_tup[2])
    world_gdp.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()
