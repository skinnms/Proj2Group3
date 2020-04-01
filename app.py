# import dependencies
import os
import sqlite3
import pandas as pd
from flask import Flask, g, render_template
from contextlib import closing

## list of tables from nba.db
# nba_2016_2017_100
# nba_2017_att_val
# nba_2017_att_val_elo
# nba_2017_att_val_elo_with_cluster
# nba_2017_attendance
# nba_2017_br
# nba_2017_elo
# nba_2017_endorsements
# nba_2017_nba_players_with_salary
# nba_2017_pie
# nba_2017_player_wikipedia
# nba_2017_players_stats_combined
# nba_2017_players_with_salary_wiki_twitter
# nba_2017_real_plus_minus
# nba_2017_team_valuations


# create application
app = Flask(__name__)

# configuration
app.config.update(dict(DATABASE=os.path.join(app.root_path, "nba.db"),))


def connect_db():
    return sqlite3.connect(app.config["DATABASE"])


# routes for each page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/ppt.html", methods=["GET"])
def ppt():
    return render_template("ppt.html")


@app.route("/vis1.html", methods=["GET"])
def vis1():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("nba.db")
    df = pd.read_sql_query("SELECT * from nba_2017_nba_players_with_salary", con)
    # verify that result of SQL query is stored in the dataframe
    print(df.to_json())
    con.close()
    # define the varibles and render to page
    labels = df["SALARY_MILLIONS"].values.tolist()
    values = df["POINTS"].values.tolist()
    return render_template("vis1.html", labels=labels, values=values)


@app.route("/vis2.html", methods=["GET"])
def vis2():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("nba.db")
    df = pd.read_sql_query("SELECT * from nba_2017_att_val", con)
    # verify that result of SQL query is stored in the dataframe
    print(df.to_json())
    con.close()
    # define the variables and render to page
    values = df["PCT"].values.tolist()  # x axis
    labels = df["TEAM"].values.tolist()
    data2 = df["VALUE_MILLIONS"].values.tolist()
    return render_template("vis2.html", labels=labels, values=values, data2=data2)


@app.route("/vis3.html", methods=["GET"])
def vi3():
    con = sqlite3.connect("nba.db")
    df = pd.read_sql_query(
        "SELECT CASE WHEN SALARY_MILLIONS < 10 THEN 'Under 10 Million' WHEN SALARY_MILLIONS >= 10 AND SALARY_MILLIONS < 20 THEN '10-20 Million' WHEN SALARY_MILLIONS >= 20 AND SALARY_MILLIONS < 30 THEN '20-30 Million' ELSE 'Over 30 Million' END AS Salary_Bucket, SUM(CASE WHEN TWITTER_FAVORITE_COUNT = '' OR TWITTER_FAVORITE_COUNT IS NULL THEN 0 ELSE TWITTER_FAVORITE_COUNT END) AS TWITTER_FAVORITE_COUNT from nba_2017_players_with_salary_wiki_twitter GROUP BY CASE WHEN SALARY_MILLIONS < 10 THEN 'Under 10 Million' WHEN SALARY_MILLIONS >= 10 AND SALARY_MILLIONS < 20 THEN '10-20 Million' WHEN SALARY_MILLIONS >= 20 AND SALARY_MILLIONS < 30 THEN '20-30 Million' ELSE 'Over 30 Million' END",
        con,
    )
    # verify that result of SQL query is stored in the dataframe
    print(df.to_json())
    con.close()
    # define the varibles and render to page
    labels = df["Salary_Bucket"].values.tolist()  # x axis
    values = df["TWITTER_FAVORITE_COUNT"].values.tolist()
    return render_template("vis3.html", labels=labels, values=values)


@app.route("/vis4.html", methods=["GET"])
def vis4():
    con = sqlite3.connect("nba.db")
    df = pd.read_sql_query("SELECT TEAM, AVG(AGE) from nba_2017_pie GROUP BY TEAM", con)
    # verify that result of SQL query is stored in the dataframe
    print(df.to_json())
    con.close()
    # define the varibles and render to page
    labels = df["TEAM"].values.tolist()  # x axis
    values = df["AVG(AGE)"].values.tolist()
    return render_template("vis4.html", labels=labels, values=values)


if __name__ == "__main__":
    app.run(debug=True)
