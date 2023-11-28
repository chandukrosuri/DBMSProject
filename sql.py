def assign_sql_query(query_type):
    if query_type == "education_gdp_ratio":
        # query = f"select rvarki.gdp.year,rvarki.gdp.gdp,rvarki.average_schooling_years.avg_yearsof_schooling from rvarki.gdp join rvarki.average_schooling_years on rvarki.gdp.countryname=rvarki.average_schooling_years.countryname and rvarki.gdp.year=rvarki.average_schooling_years.year where rvarki.gdp.countryname = {country} order by year;"
        query = """
        SELECT rvarki.gdp.year, rvarki.gdp.gdp, rvarki.average_schooling_years.avg_yearsof_schooling 
        FROM rvarki.gdp 
        JOIN rvarki.average_schooling_years 
        ON rvarki.gdp.countryname = rvarki.average_schooling_years.countryname 
        AND rvarki.gdp.year = rvarki.average_schooling_years.year 
        WHERE rvarki.gdp.countryname = :country 
        ORDER BY year
        """
        return query
    elif query_type == "debt_expen_ratio":
        query = """
        SELECT rvarki.government_debt.year, rvarki.government_debt.governmentdebt, rvarki.GOVERNMENT_EXPENDITURE.GOVERNMENT_EXPENDITURE 
        FROM rvarki.GOVERNMENT_DEBT
        JOIN rvarki.GOVERNMENT_EXPENDITURE 
        ON rvarki.GOVERNMENT_DEBT.countryname = rvarki.GOVERNMENT_EXPENDITURE.countryname 
        AND rvarki.GOVERNMENT_DEBT.year = rvarki.GOVERNMENT_EXPENDITURE.year 
        WHERE rvarki.GOVERNMENT_DEBT.countryname = :country
        ORDER BY year
        """
        return query
    elif query_type == "happiness_change":
        query = """
        WITH yearly_avg AS (
            SELECT c.continent, h.year, AVG(h.cantril_ladder_score) AS avg_happiness
            FROM rvarki.happiness h
            INNER JOIN rvarki.continent c ON h.countryname = c.country
            GROUP BY c.continent, h.year
        ),
        yearly_avg_lag AS (
            SELECT continent, year, avg_happiness, LAG(avg_happiness, 1) OVER (PARTITION BY continent ORDER BY year) AS prev_year_happiness
            FROM yearly_avg
        )
        SELECT continent, year, avg_happiness, prev_year_happiness, (avg_happiness - prev_year_happiness) / prev_year_happiness * 100 AS percent_change
        FROM yearly_avg_lag
        WHERE prev_year_happiness IS NOT NULL AND continent = :continent
        ORDER BY year
        """
        return query
    elif query_type == "obesity_change":
        query = """
        WITH yearly_avg_obesity AS (
            SELECT c.continent, o.year, AVG(o.bothsexes) AS avg_obesity
            FROM rvarki.obesity o
            INNER JOIN rvarki.continent c ON o.countryname = c.country
            GROUP BY c.continent, o.year
        ),
        yearly_avg_obesity_lag AS (
            SELECT continent, year, avg_obesity, LAG(avg_obesity, 1) OVER (PARTITION BY continent ORDER BY year) AS prev_year_obesity
            FROM yearly_avg_obesity
        )
        SELECT continent, year, ROUND(avg_obesity, 2) AS avg_obesity, ROUND(prev_year_obesity,2) AS prev_year_obesity, ROUND((avg_obesity - prev_year_obesity) / prev_year_obesity * 100, 2) AS percent_change
        FROM yearly_avg_obesity_lag
        WHERE prev_year_obesity IS NOT NULL AND continent = :continent
        ORDER BY continent, year
        """
        return query
    elif query_type == "dentist_change":
        query = """"""
    elif query_type == "suicide_mean":
        query = """
        WITH GlobalSuicideData AS (
            SELECT 
                YEAR,
                SUM(SUICIDE_NUMBER) AS TotalSuicides,
                SUM(POPULATION) AS TotalPopulation
            FROM 
                (SELECT DISTINCT YEAR, AGE, SEX, SUICIDE_NUMBER, POPULATION 
                FROM rvarki.suicide_rate)
            GROUP BY 
                YEAR
        ),
        GlobalSuicideRates AS (
            SELECT 
                YEAR,
                (TotalSuicides / TotalPopulation) * 100000 AS GlobalSuicideRate
            FROM 
                GlobalSuicideData
        ),
        CountrySuicideData AS (
            SELECT 
                YEAR,
                SUM(SUICIDE_NUMBER) AS TotalSuicides,
                SUM(POPULATION) AS TotalPopulation
            FROM 
                (SELECT DISTINCT YEAR, AGE, SEX, SUICIDE_NUMBER, POPULATION 
                FROM rvarki.suicide_rate
                WHERE COUNTRYNAME = :Country)
            GROUP BY 
                YEAR
        ),
        CountrySuicideRates AS (
            SELECT 
                YEAR,
                (TotalSuicides / TotalPopulation) * 100000 AS CountrySuicideRate
            FROM 
                CountrySuicideData
        ),
        YearlyDeviation AS (
            SELECT 
                g.YEAR,
                i.CountrySuicideRate - g.GlobalSuicideRate AS Deviation
            FROM 
                CountrySuicideRates i
            JOIN 
                GlobalSuicideRates g ON i.YEAR = g.YEAR
        )
        SELECT 
            YEAR,
            ROUND(AVG(Deviation), 2) AS MeanDeviation
        FROM 
            YearlyDeviation
        GROUP BY 
            YEAR
        ORDER BY 
            YEAR
            """
        return query
    
    elif query_type == "pollution_rank":
        query = """
        WITH RankedData AS (
            SELECT 
                YEAR,
                COUNTRYNAME,
                TOTAL,
                RANK() OVER (PARTITION BY YEAR ORDER BY TOTAL DESC) AS POLLUTION_RANK
            FROM 
                rvarki.DEATHS_DUETO_AIRPOLLUTION
        )
        SELECT 
            YEAR,
            COUNTRYNAME,
            TOTAL,
            POLLUTION_RANK
        FROM 
            RankedData
        WHERE 
            COUNTRYNAME = :country
        ORDER BY 
            YEAR
        """
        return query
    
