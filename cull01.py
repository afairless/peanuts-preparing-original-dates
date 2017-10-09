#! /usr/bin/env python3


def get_next_date_for_day_of_week(start_date, day_of_week):
    '''
    Taken from:
    https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-a-date
    Starting at the 'start_date' find the next date that is a particular day of
        the week (e.g., Sunday)
    'start_date' is a 'date' object from 'datetime' package
    'day_of_week' designates the day of the week:  Monday = 0, Tuesday = 1, etc.
    '''

    import datetime

    days_difference = day_of_week - start_date.weekday()

    if days_difference <= 0:
        days_difference += 7

    target_date = start_date + datetime.timedelta(days_difference)

    return(target_date)


def list_days_of_week_within_date_range(start_date, end_date, day_of_week):
    '''
    input:  start and end dates as strings in format of 'YYYY-MM-DD'
    output:  list of all dates that are Sundays within the range of dates,
        inclusive of start and end
    '''

    from datetime import datetime, timedelta

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    start_day_of_week = get_next_date_for_day_of_week(start_date, day_of_week)
    difference = end_date - start_day_of_week

    date_list = [start_day_of_week + timedelta(days=x)
                 for x in range(difference.days + 1)]
    date_list2 = [date_list[x].strftime('%Y-%m-%d')
                  for x in range(0, len(date_list), 7)]

    return(date_list2)


def generate_dates(start_date, end_date):
    '''
    input:  start and end dates as strings in format of 'YYYY-MM-DD'
    output:  list of all dates in the range of dates, inclusive of start and end
    '''

    from datetime import datetime, timedelta

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    difference = end_date - start_date

    date_list = [start_date + timedelta(days=x) for x in range(difference.days + 1)]
    date_list2 = [date_list[x].strftime('%Y-%m-%d') for x in range(len(date_list))]

    return(date_list2)


def get_comics_to_cull():
    '''
    Peanuts ran from Oct 2, 1950 to Feb 13, 2000, but not all of the dates in
        that range were included in the original run.  Here are the dates of the
        original Peanuts run:

            dailies started Oct 2, 1950
            Sundays started Jan 6, 1952

            dailies ended Jan 3, 2000
            Sundays ended Feb 13, 2000

    So, Sundays before Jan 6, 1952 and dailies after Jan 3, 2000 need to be
        culled from the list of all the dates.

    This function returns a list of these comics' dates for culling
    '''

    start_date = '1950-10-02'
    end_date = '1952-01-05'
    sunday = 6
    sundays1950s_to_cull = list_days_of_week_within_date_range(start_date,
                                                               end_date, sunday)
    start_date = '2000-01-04'
    end_date = '2000-02-13'
    sunday = 6
    sundays2000s_to_keep = list_days_of_week_within_date_range(start_date,
                                                               end_date, sunday)
    start_date = '2000-01-04'
    end_date = '2000-02-13'
    dailies2000s_to_cull = generate_dates(start_date, end_date)
    dailies2000s_to_cull = [x for i, x in enumerate(dailies2000s_to_cull)
                            if x not in sundays2000s_to_keep]

    comics_to_cull = sundays1950s_to_cull + dailies2000s_to_cull

    return(comics_to_cull)


def get_culled_comics_list():
    '''
    Returns list of Peanuts comics dates minus the comics that should be culled

    Peanuts ran from Oct 2, 1950 to Feb 13, 2000, but not all of the dates in
        that range were included in the original run.  Here are the dates of the
        original Peanuts run:

            dailies started Oct 2, 1950
            Sundays started Jan 6, 1952

            dailies ended Jan 3, 2000
            Sundays ended Feb 13, 2000

    So, Sundays before Jan 6, 1952 and dailies after Jan 3, 2000 need to be
        culled from the list of all the dates.
    '''

    start_date = '1950-10-02'
    end_date = '2000-02-13'
    full_date_list = generate_dates(start_date, end_date)

    comics_to_cull = get_comics_to_cull()

    culled_comics = [x for i, x in enumerate(full_date_list)
                     if x not in comics_to_cull]

    return(culled_comics)


def write_list_to_text_file(a_list, text_file_name, overwrite_or_append='a'):
    '''
    writes a list of strings to a text file
    appends by default; change to overwriting by setting to 'w' instead of 'a'
    '''

    try:
        textfile = open(text_file_name, overwrite_or_append, encoding='utf-8')
        for element in a_list:
            textfile.write(element)
            textfile.write('\n')

    finally:
        textfile.close()


def main():
    '''
    Creates list of dates of comics from original run of Peanuts and saves list
        as text file into current working directory
    '''

    culled_comics = get_culled_comics_list()
    list_filename = 'peanuts_culled01.txt'
    write_list_to_text_file(culled_comics, list_filename,
                            overwrite_or_append='w')


if __name__ == '__main__':
    main()
