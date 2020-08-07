## Los Angeles County Data by cities/communities

Data are collected daily from [@lapublichealth dashboard](http://publichealth.lacounty.gov/media/Coronavirus/locations.htm). 

- Copy CITY/COMMUNITY / Case / Case Rate / Deaths / Death Rate data (without the header), and save them to a text file ``%m-%d-%Y.txt``, e.g., ``07-26-2020.txt``. Also copy Long Beach and Pasadena numbers and save them to ``lb_pas.txt``, in sequence ``[lb_case, pas_case, lb_death, pas_death]``.

- Run ``python3 lac.py [07-26-2020.txt]`` to generate/update various csv files. If ``date.txt`` is not given, the program searches for the current day. 
 
