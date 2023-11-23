# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/178MoTOW6XrS2WEaZr81j83g9-eXFDtYh

**Task 07: Querying RDF(s)**

**Assignment 4** \
Adrián Rejas Llamera
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
from rdflib.plugins.sparql import prepareQuery
from rdflib import XSD

# Defining namespace
ns = Namespace("http://somewhere#")

# RDFLib
print("RDFLib queries")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
  print(s)

# SPARQL
print("SPARQL queries")
q1 = prepareQuery('''
    SELECT ?subclass
    WHERE {
        ?subclass rdfs:subClassOf ns:LivingThing .
    }
''', initNs={"rdfs": RDFS, "ns": ns})

# Visualize the results

for r in g.query(q1):
   print(r.subclass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO

# RDFLib
print("RDFLib queries ")

for s,p,o in g.triples((None, RDF.type, ns.Person)):
  print(s)

for s,p,o in g.triples((None,RDFS.subClassOf, ns.Person)):
  for s1,p1,o1 in g.triples((None, RDF.type, s)):
    print(s1)

#SparQL
print("SparQL queries")
q2 = prepareQuery('''
    SELECT ?individual
    WHERE {
        ?individual a/rdfs:subClassOf* ns:Person .
    }
''', initNs={"rdf": RDF, "rdfs": RDFS, "ns": ns})

for r in g.query(q2):
   print(r.individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO

# RDFLib

print("RDFLib queries")
# Creating a list with "Person" and "Animal" classes
classes = [ns.Person, ns.Animal]

for class_uri in classes:
    for s, p, o in g.triples((None, RDF.type, class_uri)):
        print(f"Individual from {class_uri}: {s}")
        for s1, p1, o1 in g.triples((s, None, None)):
            print(f"Property: {p1}, Value: {o1}")
        print("\n")

#SparQL
print("SparQL queries of Person")

q3 = prepareQuery('''
    SELECT  ?individual ?property ?value ?class
    WHERE {
        ?individual rdf:type ns:Person .
        ?individual ?property ?value .
    }
''', initNs={"rdf": RDF, "ns": ns})

for r in g.query(q3):
 print(r.individual, r.property, r.value)

print("SparQL queries of Animal")

q4 = prepareQuery('''
    SELECT ?individual ?property ?value ?class
    WHERE {
        ?individual rdf:type ns:Animal .
        ?individual ?property ?value .
    }
''', initNs={"rdf": RDF, "ns": ns})

for r in g.query(q4):
 print(r.individual, r.property, r.value)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

#RDFLib
print("RDFLib queries")
for s, p, o in g.triples((None, FOAF.knows, ns.RockySmith)):
  for s1, p1, o1 in g.triples((s, VCARD.Given, None)):
      print(o1)

#SparQL
print("SparQL queries")
q5 = prepareQuery('''
  SELECT  ?Given  WHERE {
  ?Subject foaf:knows ?RockySmith;
            vcard:Given ?Given.
	?RockySmith vcard:FN ?RockySmithFullName .
  }
  ''',
  initNs = { "foaf": FOAF, "vcard": VCARD, "xsd":XSD}
)
for r in g.query(q5, initBindings = {'?RockySmithFullName' : Literal('Rocky Smith', datatype=XSD.string)}):
  print(r.Given)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# TO DO
q6 = prepareQuery('''
    SELECT ?entity  WHERE {
        ?entity foaf:knows ?person1 .
        ?entity foaf:knows ?person2 .
        ?entity vcard:Given ?Name.
        FILTER (?person1 != ?person2)
    }
    GROUP BY ?entity
    HAVING (COUNT(?person1) >= 2)
    ''', initNs={"foaf": FOAF, "vcard": VCARD})

for r in g.query(q6):
   print(r.entity)