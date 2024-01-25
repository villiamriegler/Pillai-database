
keys = set()


def write_ddl(content):
    with open("DDL.sql", "a") as out_file:
        # Gets page names 'bipacksedel' etc
        for page in content.keys():
            for table_name in content[page].keys():
                full_name = page + '_' + table_name if page != "product_name" else "product_name" 
                full_name = full_name.replace("-", "_") # I'm tired will fix later 
                full_name = full_name.replace("å", "a")
                full_name = full_name.replace("ä", "a")
                full_name = full_name.replace("ö", "o")
                if full_name in keys:
                    continue

                keys.add(full_name)
                out_file.write(f"CREATE TABLE IF NOT EXISTS {full_name} (\n\tnplID INT PRIMARY KEY,\n\tcontent TEXT NOT NULL\n);\n\n")


def write_dml(nplid, content):
    with open("DML.sql", "a") as out_file:
        for page in content.keys():
            for table_name in content[page].keys():
                full_name = page + '_' + table_name if page != "product_name" else "product_name" 
                full_name = full_name.replace("-", "_")
                full_name = full_name.replace("å", "a")
                full_name = full_name.replace("ä", "a")
                full_name = full_name.replace("ö", "o")
                out_file.write(f"INSERT INTO {full_name} (nplID, content) VALUES ({nplid}, \"{content[page][table_name]}\");\n")
