from rocksdict import Rdict
import kuzu
import pandas as pd
from collections import defaultdict
import constants

def import_graph_data():
    hetio_kuzu_db = kuzu.Database(constants.KUZU_DB_PATH)
    conn = kuzu.Connection(hetio_kuzu_db)

    for node in constants.NODE_TYPES:
        conn.execute(f"""
            CREATE NODE TABLE IF NOT EXISTS {node} (
                id STRING,
                name STRING,
                PRIMARY KEY(id)
            )
        """)

    for edge in constants.EDGE_TYPES:
        source, target = constants.EDGE_TYPES[edge]
        conn.execute(f""" 
            CREATE REL TABLE IF NOT EXISTS {edge} (
                FROM {source} TO {target}
            )
        """)

    nodes_df = pd.read_csv("./nodes.tsv", sep="\t", header=0)
    for node in constants.NODE_TYPES:
        curr_nodes_df = nodes_df.loc[nodes_df["kind"] == node, ["id", "name"]]
        conn.execute(f"COPY {node} FROM $df", {"df": curr_nodes_df})

    edges_df = pd.read_csv("./edges.tsv", sep="\t", header=0)
    for edge in constants.EDGE_TYPES:
        curr_edges_df = edges_df.loc[edges_df["metaedge"] == edge, ["source", "target"]]
        conn.execute(f"COPY {edge} FROM $df", {"df": curr_edges_df})

def import_query1():
    hetio_kuzu_db = kuzu.Database(constants.KUZU_DB_PATH)
    diseases = defaultdict(dict)
    with kuzu.Connection(hetio_kuzu_db) as conn:
        response = conn.execute(""" 
            MATCH (d:Disease)-[r1:CpD|CtD|DaG|DdG|DuG|DlA]-(n1)
            RETURN d.id, d.name, label(r1), collect(n1.name)
        """)

        for disease_id, disease_name, rel_label, names in response:
            diseases[disease_id]["name"] = disease_name
            diseases[disease_id][rel_label] = names
    
    db = Rdict(constants.ROCKS_DB_PATH)
    for disease_id in diseases:
        disease_store = {
            "name": diseases[disease_id]["name"],
            "drugs": sorted(list(
                set(diseases[disease_id].get("CpD", [])) | 
                set(diseases[disease_id].get("CtD", []))
            )),
            "genes": sorted(list(
                set(diseases[disease_id].get("DaG", [])) | 
                set(diseases[disease_id].get("Ddg", [])) |
                set(diseases[disease_id].get("DuG", []))
            )),
            "locations": sorted(list(
                set(diseases[disease_id].get("DlA", []))
            ))
        }
        db[disease_id] = disease_store

def import_query2():
    hetio_kuzu_db = kuzu.Database(constants.KUZU_DB_PATH)
    with (kuzu.Connection(hetio_kuzu_db) as conn, 
    Rdict(constants.ROCKS_DB_PATH) as rocks_db):
        response = conn.execute("""
            MATCH (c1:Compound)-[:CuG]->(:Gene)<-[:AdG]-(:Anatomy)<-[:DlA]-(d1:Disease)
            WHERE NOT EXISTS { MATCH (c1)-[:CtD|CpD]->(d1) }
            RETURN DISTINCT c1.name, c1.id, d1.name, d1.id 

            UNION

            MATCH (c2:Compound)-[:CdG]->(:Gene)<-[:AuG]-(:Anatomy)<-[:DlA]-(d2:Disease)
            WHERE NOT EXISTS { MATCH (c2)-[:CtD|CpD]->(d2) }
            RETURN DISTINCT c2.name, c2.id, d2.name, d2.id
        """)
        
        compound_disease = sorted([(compound_name, compound_id, disease_name, disease_id) 
            for compound_name, compound_id, disease_name, disease_id in response])
        rocks_db[constants.QUERY2_KEY] = compound_disease

def main():
    import_graph_data()
    import_query1()
    import_query2()

if __name__ == "__main__":
    main()