# import dependencies
import os
import sqlite3
import pandas as pd
from flask import Flask, g, render_template
from contextlib import closing

app = Flask(__name__)

DATABASE = "nba.db"

app.config.from_object(__name__)


def connect_to_database():
    return sqlite3.connect(app.config["DATABASE"])


def get_db():
    db = getattr(g, "db", None)
    if db is None:
        db = g.db = connect_to_database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()


def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows


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
    return render_template("vis2.html")


@app.route("/vis3.html", methods=["GET"])
def vi3():
    return render_template("vis3.html")


@app.route("/vis4.html", methods=["GET"])
def vis4():
    return render_template("vis4.html")


# routes for databases
@app.route("/nba_2016_2017_100")
def nba_2016_2017_100():
    rows = execute_query("""SELECT * FROM nba_2016_2017_100""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_att_val")
def nba_2017_att_val():
    rows = execute_query("""SELECT * FROM nba_2017_att_val""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_att_val_elo")
def nba_2017_att_val_elo():
    rows = execute_query("""SELECT * FROM nba_2017_att_val_elo""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_att_val_elo_with_cluster")
def nba_2017_att_val_elo_with_cluster():
    rows = execute_query("""SELECT * FROM nba_2017_att_val_elo_with_cluster""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_attendance")
def nba_2017_attendance():
    rows = execute_query("""SELECT * FROM nba_2017_attendance""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_br")
def nba_2017_br():
    rows = execute_query("""SELECT * FROM nba_2017_br""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_elo")
def nba_2017_elo():
    rows = execute_query("""SELECT * FROM nba_2017_elo""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_endorsements")
def nba_2017_endorsements():
    rows = execute_query("""SELECT * FROM nba_2017_endorsements""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_nba_players_with_salary")
def nba_2017_nba_players_with_salary():
    rows = execute_query("""SELECT * FROM nba_2017_nba_players_with_salary""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_pie")
def nba_2017_pie():
    rows = execute_query("""SELECT * FROM nba_2017_pie""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_player_wikipedia")
def nba_2017_player_wikipedia():
    rows = execute_query("""SELECT * FROM nba_2017_player_wikipedia""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_players_stats_combined")
def nba_2017_players_stats_combined():
    rows = execute_query("""SELECT * FROM nba_2017_players_stats_combined""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_players_with_salary_wiki_twitter")
def nba_2017_players_with_salary_wiki_twitter():
    rows = execute_query("""SELECT * FROM nba_2017_players_with_salary_wiki_twitter""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_real_plus_minus")
def nba_2017_real_plus_minus():
    rows = execute_query("""SELECT * FROM nba_2017_real_plus_minus""")
    return "<br>".join(str(row) for row in rows)


@app.route("/nba_2017_team_valuations")
def nba_2017_team_valuations():
    rows = execute_query("""SELECT * FROM nba_2017_team_valuations""")
    return "<br>".join(str(row) for row in rows)


if __name__ == "__main__":
    app.run(debug=True)
