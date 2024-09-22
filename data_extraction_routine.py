# import psycopg2
# import pandas as pd
# from google.cloud import bigquery
# # Connect to PostgreSQL
# pg_conn = psycopg2.connect(
#     "dbname=esus user=esus_leitura password=kmHJK*}Jc9vPz+b{L4o?796d9rW host=200.137.166.148 port=5433")
# cursor = pg_conn.cursor()

# # Execute query
# cursor.execute("""SELECT
#     fatovacina1_.nu_cpf_cidadao AS identifier_cpf,
#     fatovacina1_.nu_cns AS identifier_cns,
#     fatovacina1_.co_fat_cidadao_pec,
#     dimensaouf13_.sg_uf AS UF,
#     fatovacina1_.dt_nascimento AS birthDate,
#     dimensaomu3_.no_municipio AS address_city,
#     dimensaose7_.ds_sexo AS gender,
#     dimensaotp14_.dt_registro AS occurrenceDateTime,
#     dimensaoim10_.no_imunobiologico AS vaccineCode_description,
#     dimensaoim10_.nu_identificador AS vaccineCode_code,
#     dimensaoim10_.sg_imunobiologico AS vaccineCode_display,
#     dimensaoes11_.no_estrategia_vacinacao,
#     dimensaodo12_.no_dose_imunobiologico AS protocolApplied_doseNumberDescription,
#     dimensaodo12_.sg_dose_imunobiologico AS protocolApplied_doseNumberString
# FROM tb_fat_vacinacao_vacina fatovacina0_
# INNER JOIN tb_fat_vacinacao fatovacina1_ ON fatovacina0_.co_fat_vacinacao = fatovacina1_.co_seq_fat_vacinacao
# INNER JOIN tb_dim_municipio dimensaomu3_ ON fatovacina0_.co_dim_municipio = dimensaomu3_.co_seq_dim_municipio
# INNER JOIN tb_dim_sexo dimensaose7_ ON fatovacina1_.co_dim_sexo = dimensaose7_.co_seq_dim_sexo
# INNER JOIN tb_dim_imunobiologico dimensaoim10_ ON fatovacina0_.co_dim_imunobiologico = dimensaoim10_.co_seq_dim_imunobiologico
# INNER JOIN tb_dim_estrategia_vacinacao dimensaoes11_ ON fatovacina0_.co_dim_estrategia_vacinacao = dimensaoes11_.co_seq_dim_estrategia_vacnacao
# INNER JOIN tb_dim_dose_imunobiologico dimensaodo12_ ON fatovacina0_.co_dim_dose_imunobiologico = dimensaodo12_.co_seq_dim_dose_imunobiologico
# INNER JOIN tb_dim_uf dimensaouf13_ ON dimensaomu3_.co_dim_uf = dimensaouf13_.co_seq_dim_uf
# INNER JOIN tb_dim_tempo dimensaotp14_ ON fatovacina0_.co_dim_tempo_vacina_aplicada = dimensaotp14_.co_seq_dim_tempo
# WHERE 1=1
# AND dimensaouf13_.co_seq_dim_uf = 19
# AND fatovacina1_.dt_nascimento > '2009-09-20'
# AND dimensaomu3_.no_municipio = 'COCAL';"""
# )
# data = cursor.fetchall()

# # Convert to DataFrame
# df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

# cursor.close()
# pg_conn.close()

# breakpoint()
# Initialize BigQuery client
# bq_client = bigquery.Client()

# # Define BigQuery dataset and table
# dataset_id = "immunization_data"
# table_id = "cocal_vaccination_data_raw"

# # Load DataFrame to BigQuery
# job_config = bigquery.LoadJobConfig()
# job_config.autodetect = True
# job = bq_client.load_table_from_dataframe(df, f"{dataset_id}.{table_id}", job_config=job_config)
# job.result()


import pandas as pd

# Read the CSV file
df = pd.read_csv('processed_cpf_cns_birthdate.csv', dtype={'CPF': str, 'CNS': str})

# Function to create a unique identifier for each row
def create_identifier(row):
    if pd.notna(row['CPF']) and pd.notna(row['CNS']):
        return f"{row['CPF']}_{row['CNS']}"
    elif pd.notna(row['CPF']):
        return f"CPF_{row['CPF']}"
    elif pd.notna(row['CNS']):
        return f"CNS_{row['CNS']}"
    else:
        return None

# Create a new column with the unique identifier
df['identifier'] = df.apply(create_identifier, axis=1)

# Remove duplicates based on the identifier
df_deduplicated = df.drop_duplicates(subset=['identifier'])

# Remove the temporary identifier column
df_deduplicated = df_deduplicated.drop(columns=['identifier'])

# Save the processed data to a new CSV file
df_deduplicated.to_csv('processed_cpf_cns_birthdate_v2.csv', index=False)

# Calculate the difference between the original and deduplicated datasets
diff_df = df[df.duplicated(keep=False)]
breakpoint()
print(f"Original rows: {len(df)}")
print(f"Rows after deduplication: {len(df_deduplicated)}")
print("Processed data saved to 'processed_cpf_cns_birthdate_v2.csv'")