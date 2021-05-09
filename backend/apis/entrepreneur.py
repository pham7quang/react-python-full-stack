from flask import request
from flask_restx import Namespace, Resource
from dynaconf import settings
from functools import lru_cache
from datetime import datetime
import requests

api = Namespace("entrepreneur", "Entrepreneur Characteristics")


def _check_against_cache(cached_function, *args):
    """
    Check against the cached_function if:
     1. result is stale
     2. original call threw an exception
        If any of the above is true, clear the cache and run the request again
    Keyword arguments:
     cached_function -- cached function to call. Functino must use lru_cache and return the following Tuple: Results, Date ran, If An Error Appeared
     *args - arguments to pass to the cached_function
    Returns: the results of the cached_function and if the cached function errored out
    """
    results, date_result_found, errored = cached_function(*args)

    # call the function again if the cached value is old or resulted in an error
    age_of_results_seconds = (datetime.now() - date_result_found).total_seconds()
    if errored or age_of_results_seconds > (settings.API_CACHE_MINUTES * 60):
        cached_function.cache_clear()
        results, date_result_found, errored = cached_function(*args)
    return results, errored


@lru_cache(32)
def get_entrepreneur_variables(year):
    """
    Used for caching the variables used for the Census Data for: Annual Survey of Entrepreneurs - Characteristics of Business Owners
    Keyword arguments:
        year - the year which the survey was taken
    Returns:
        all_records - the records found in the census api, in an array of dictionaries
        date recorded - the date which the results were queried
        errored - boolean represenation of whether the API call failed
    """
    try:
        response = requests.get(
            f"https://api.census.gov/data/{year}/ase/cscbo/variables?key={settings.CENSUS_API_KEY}"
        )
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.RequestException as e:
        return (
            {
                "message": "unable to query census endpoint for the headers",
                "endpointError": response.text,
            },
            datetime.now(),
            True,
        )
    except Exception as exception:
        if response and not response.text:
            # response.json() errored since the api returned an empty results - return an empty array
            return [], datetime.now(), True
        else:
            return (
                {
                    "message": "unable to query census endpoint",
                    "endpointError": str(exception),
                },
                datetime.now(),
                True,
            )

    # The Census API returns a two-dimensional array, like an CSV, where the first array contains the headers and rest of the array are records
    # dictionary of headers and where in the array index is the record, e.g. {0: 'name', 1: 'label', 2: 'concept'} -> index 0 has name record
    headers = {index: val for index, val in enumerate(results[0])}
    # convert the array of arrays to a array of dictionary with the headers as attributes. e.g [{"name": "ABC", "label": "This is the alphabet"}]
    all_records = []
    for record in results[1:]:
        # do not add the un-queryable columns, check the "name" column
        if not record[0] in ["for", "in", "ucgid"]:
            all_records.append({headers[i]: value for i, value in enumerate(record)})

    return all_records, datetime.now(), False


@api.route("/variables/<int:year>")
class EntrepreneurVariablesApi(Resource):
    def get(self, year):
        """
        Grabs all the variables in the entrepreneur dataset. Can be found here: https://api.census.gov/data/2014/ase/cscbo/variables.html
        Keyword arguments:
            year - the year which the survey was taken
        returns: an array of dictionaries mapping the name and the labels.
        """
        results, is_error = _check_against_cache(get_entrepreneur_variables, year)
        if is_error:
            return results, 500

        return results


@lru_cache(32)
def get_entrepreneur_dataset(year, headers_csv):
    """
    Used for caching the dataset returned from the Census Data for: Annual Survey of Entrepreneurs - Characteristics of Business Owners
    Keyword arguments:
        year - the year which the survey was taken
        headers_csv - string of comma separated headers to return from the dataset
    Returns:
        all_records - the records found in the census api, in an array of dictionaries
        date recorded - the date which the results were queried
        errored - boolean represenation of whether the API call failed
    """
    try:
        response = requests.get(
            f"https://api.census.gov/data/{year}/ase/cscbo?get={headers_csv}&for=us:*&key={settings.CENSUS_API_KEY}"
        )
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.RequestException as e:
        return (
            {
                "message": "unable to query census dataset endpoint",
                "endpointError": response.text,
            },
            datetime.now(),
            True,
        )
    except Exception as exception:
        if response and not response.text:
            # response.json() errored since the api returned an empty results - return an empty array
            return [], datetime.now(), True
        else:
            return (
                {
                    "message": "unable to query census dataset endpoint",
                    "endpointError": str(exception),
                },
                datetime.now(),
                True,
            )

    # The Census API returns a two-dimensional array, like an CSV, where the first array contains the headers and rest of the array are records
    # dictionary of headers and where in the array index is the record, e.g. {0: 'name', 1: 'label', 2: 'concept'} -> index 0 has name record
    headers = {index: val for index, val in enumerate(results[0])}
    # convert the array of arrays to a array of dictionary with the headers as attributes. e.g [{"name": "ABC", "label": "This is the alphabet"}]
    all_records = []
    for record in results[1:]:
        all_records.append({headers[i]: value for i, value in enumerate(record)})

    return all_records, datetime.now(), False


@api.route("/<int:year>")
class EntrepreneurDataSetApi(Resource):
    @api.doc(
        params={
            "headers": {
                "description": "headers to grab from the records",
                "type": ["string"],
            }
        }
    )
    def get(self, year):
        """
        Returns the Census Data for: Annual Survey of Entrepreneurs - Characteristics of Business Owners
        https://www.census.gov/data/developers/data-sets/ase.html
        returns: an array of dictionaries mapping the name and the labels.
        """
        headers = request.args.getlist("headers")
        if not headers:
            headers = ["NAME", "NATION"]

        # sort the headers so the cache can properly cache the content if the headers are unchanged
        headers.sort()
        results, is_error = _check_against_cache(
            get_entrepreneur_dataset, year, ",".join(headers)
        )
        if is_error:
            return results, 500

        return results
