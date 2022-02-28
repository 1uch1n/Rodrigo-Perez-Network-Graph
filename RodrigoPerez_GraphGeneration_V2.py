# Author : 1uch1n (1uch1n@protonmail.com)
# Creation date: 2022-02-04
# Last update: 2022-02-04
# Description: turns a Rodrigo Perez's theater plays & TV sets dataset into a dataset of the links between all castings
# and visualize it as a graph with Gephi software (https://gephi.org/), in order to produce a graph visualization of
# Perez's collaborators network

import pandas as pd
import itertools
import csv
import os
os.chdir('/home/luchin/Bureau/Proyecto Rodrigo Perez')

file = pd.ExcelFile('BBDD Rodrigo Pérex.xlsx')

# create a DataFrame for each sheet of the file
df1  = file.parse('Cuadro completo')
df2  = file.parse('Descriptivo obras')
df3 = file.parse('BBDD')
df4 = file.parse('Etiquetas roles')
df5 = file.parse('Prueba dirección')

# we'll focus on df3, which gathers data on who had a role (actor, director, etc.) in a play
# first, create dict to gather data on who's linked to each play
plays = {}

# df3 consists of one play per column, starting from the third one (first & second are person's name and gender)
for n in range(2,17):
    # fetching the name of the column
    col_name = df3.iloc[:, n].name
    # for each column, droping all null values to match only the rows with a link to a person
    # we extract the names of the people related to the play
    names = df3[df3[col_name].notnull()]['NOMBRE AGENTE']
    # and their respective function in the play (specified in the play's name column)
    functions = df3[df3[col_name].notnull()][col_name]
    # confirm the two pandas series can be zipped
    assert len(names)==len(functions)
    zipped = zip(names.values, functions.values)
    # the result is a dict with plays as keys, and a list of tuples (name, function)
    plays[col_name] = list(zipped)

# create empty lists to gather all links and nodes
links = []
nodes = []

for play_id, people in plays.items():
    # take the name of the play without its id
    play = play_id[4:]
    # and add it to the nodes files with its characteristics (name, class)
    nodes.append((play, "Play"))
    # for each key (ie the play), compute the length of the values (list of tuples people/function)
    # in order to extract them all one by one and add it to the corresponding list with their characteristics
    for l in range(len(people)):
        # take the name of the person
        person = people[l][0]
        # and its function
        func = people[l][1]
        # for each link play/person, make a tuple with a link label (function of the person in the play)
        triple = (play, person, func)
        # and add it to the links list
        links.append(triple)
        # for each person, create a pair name/class
        pair = (person, "Person")
        # and add it to the nodes file with its characteristics (name, class, link)
        nodes.append(pair)

# keeping only the unique values of nodes
nodes = set(nodes)

# turn the node and links datasets into a csv file
with open('links_v2.csv', 'w', newline='') as file:
    spamwriter = csv.writer(file, delimiter=',')
    spamwriter.writerow(["Source", "Target", "Label"])
    for play_name, person_name, function_as_link_label in links:
        spamwriter.writerow([play_name, person_name, function_as_link_label])
    file.close()
with open('nodes_v2.csv', 'w', newline='') as file:
    spamwriter = csv.writer(file, delimiter=',')
    spamwriter.writerow(["Id", "Label", "Class"])
    for name, name_class in nodes:
        # duplicate the name so that it is both the id and the label of the node
        spamwriter.writerow([name, name, name_class])
    file.close()