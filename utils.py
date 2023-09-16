from exceptions import NegativeTitlesError, ImpossibleTitlesError, InvalidYearCupError
from datetime import datetime


def data_processing(dic):
    if dic["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")

    first_year_cup = 1930
    possible_year_cup = datetime.strptime(dic["first_cup"], "%Y-%m-%d")
    current_year_cup = int(possible_year_cup.strftime("%Y"))
    year_diference = current_year_cup - first_year_cup
    if year_diference < 0:
        year_diference * (-1)

    if (year_diference % 4) != 0:
        raise InvalidYearCupError("there was no world cup this year")
    if current_year_cup < first_year_cup:
        raise InvalidYearCupError("there was no world cup this year")

    current_year = int(datetime.now().strftime("%Y"))
    possible_number_of_titles = (
        current_year - int(possible_year_cup.strftime("%Y"))
    ) / 4

    if dic["titles"] > (possible_number_of_titles):
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
