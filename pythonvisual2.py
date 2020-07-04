"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    join_dict = {}
    uncode_set = set()
    for code, country in plot_countries.items():
        if country in gdp_countries:
            join_dict[code] = country
        else:
            uncode_set.add(code)   
    tup = (join_dict, uncode_set)
    return tup


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

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
            gdp_dict[row[gdpinfo["country_name"]]] = row
    tup = reconcile_countries_by_name(plot_countries, gdp_dict) 
    joingdp_dict = {}
    nogdp_set = set()
    for code, country in tup[0].items():
        if gdp_dict[country][year] != '':
            gdp = math.log(float(gdp_dict[country][year]), 10)
            joingdp_dict[code] = gdp
        else:
            nogdp_set.add(code)
    final_tup = (joingdp_dict, tup[1], nogdp_set)
    return final_tup


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    final_tup = build_map_dict_by_name(gdpinfo, plot_countries, year)
    world_gdp = pygal.maps.world.World()
    title = "GDP by country for {} (log scale),unified by common country NAME".format(year)
    world_gdp.title = title
    world_gdp.add("GDP for {}".format(year), final_tup[0])
    world_gdp.add("Missing from world bank data", final_tup[1])
    world_gdp.add("NO GDP data", final_tup[2])
    world_gdp.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()
