#! /usr/bin/env python3


def get_sibling_directory_path(sibling_directory_name):
    '''
    returns path for a specified folder that is in the same parent directory as
        the current working directory
    '''
    import os
    current_path = os.getcwd()
    last_separator_position = current_path.rfind(os.sep)
    parent_directory_path = current_path[0:last_separator_position]
    sibling_directory_path = os.path.join(parent_directory_path,
                                          sibling_directory_name)
    return(sibling_directory_path)


def listdir_nohidden_nofolder(path):
    '''
    returns list of nonhidden files in the directory of the specified path
        excludes folders
    'os.listdir' includes hidden files, but this function excludes them
    '''
    import os
    file_list = next(os.walk(path))[2]
    for e in file_list:
        if e.startswith('.'):
            file_list.remove(e)
    return(file_list)


def get_sibling_directory_contents(sibling_directory):
    import os
    sibling_directory_path = get_sibling_directory_path(sibling_directory)
    contents_list = listdir_nohidden_nofolder(sibling_directory_path)
    return(contents_list)


def get_next_date_for_day_of_week(start_date, day_of_week):
    '''
    Starting at the 'start_date' find the next date that is a particular day of
        the week (e.g., Sunday)
    'start_date' is a 'date' object from 'datetime' package
    'day_of_week' designates the day of the week:  Monday = 0, Tuesday = 1, etc.
    '''
    #from datetime import weekday, timedelta
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
    date_list = [start_day_of_week + timedelta(days=x) for x in range(difference.days + 1)]
    date_list2 = [date_list[x].strftime('%Y-%m-%d') for x in range(0, len(date_list), 7)]
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
    All Peanuts comics from Oct 2, 1950 to Feb 13, 2000 were scraped from
        GoComics.com, but not all of those dates were included in the original
        Peanuts run.  Here are the dates of the original Peanuts run:

            dailies started Oct 2, 1950
            Sundays started Jan 6, 1952

            dailies ended Jan 3, 2000
            Sundays ended Feb 13, 2000
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
    scrape_folder = '01_scrape_peanuts/peanuts'
    scraped_list = get_sibling_directory_contents(scrape_folder)
    comics_to_cull = get_comics_to_cull()
    culled_comics = [x for i, x in enumerate(scraped_list)
                            if x not in comics_to_cull]
    return(culled_comics)


def write_list_to_text_file(a_list, text_file_name, overwrite_or_append = 'a'):
    '''
    writes a list of strings to a text file
    appends by default; change to overwriting by setting to 'w' instead of 'a'
    '''
    try:
        textfile = open(text_file_name, overwrite_or_append, encoding = 'utf-8')
        for element in a_list:
            textfile.write(element)
            textfile.write('\n')
    finally:
        textfile.close()
    return


culled_comics = get_culled_comics_list()
list_filename = 'peanuts_culled01.txt'
write_list_to_text_file(culled_comics, list_filename, overwrite_or_append = 'w')
