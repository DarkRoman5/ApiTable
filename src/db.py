import psycopg2

from config import DB_PARAMS
from src.sql import CREATE_TABLES


def connect_db():
    return psycopg2.connect(**DB_PARAMS)

def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(CREATE_TABLES)
    conn.commit()
    cur.close()
    conn.close()

def insert_lead(cur, lead):
    cur.execute(
        """
        INSERT INTO leads (id, name, price, responsible_user_id, group_id, status_id, pipeline_id, loss_reason_id, 
                           created_by, updated_by, created_at, updated_at, closed_at, closest_task_at, is_deleted, 
                           account_id, labor_cost)
        SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), to_timestamp(%s), to_timestamp(%s), 
                to_timestamp(%s), %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM leads WHERE id = %s);
        """,
        (
            lead['id'], lead['name'], lead['price'], lead['responsible_user_id'], lead['group_id'],
            lead['status_id'], lead['pipeline_id'], lead['loss_reason_id'], lead['created_by'], lead['updated_by'],
            lead['created_at'], lead['updated_at'], lead.get('closed_at'), lead.get('closest_task_at'),
            lead['is_deleted'], lead['account_id'], lead.get('labor_cost'), lead['id']
        )
    )

def insert_tag(cur, lead):
    for tag in lead['_embedded'].get('tags', []):
        cur.execute("INSERT INTO tags (name, color) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET color = EXCLUDED.color;", (tag['name'], tag.get('color')))
        cur.execute("INSERT INTO link_leads_tags (id_leads, id_tags) SELECT %s, id FROM tags WHERE name = %s ON CONFLICT DO NOTHING;", (lead['id'], tag['name']))

def insert_custom_values(cur, lead):
    for field in (lead.get('custom_fields_values') or []):
        cur.execute(
            """INSERT INTO custom_values (field_id, field_name, field_code, field_type) VALUES (%s, %s, %s, %s) 
             ON CONFLICT (field_id) DO NOTHING;""",
            (field['field_id'], field['field_name'], field.get('field_code'), field.get('field_type', 'text'))
        )
        for value in field.get('values', []):
            cur.execute("SELECT id_value FROM value_from_customer_value WHERE value = %s;",
                        (value['value'],))
            result = cur.fetchone()
            if result:
                id_value = result[0]
            else:
                cur.execute("INSERT INTO value_from_customer_value (value, enum_id, enum_code) VALUES (%s, %s, %s) RETURNING id_value;",
                            (value['value'], value.get('enum_id'), value.get('enum_code')))
                id_value = cur.fetchone()[0]
            cur.execute("INSERT INTO link_custom_values_value (id_value, field_id) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM link_custom_values_value WHERE id_value = %s AND field_id = %s);",
                        (id_value, field['field_id'], id_value, field['field_id']))
            cur.execute("INSERT INTO link_leads_custom_values (id_leads, field_id) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM link_leads_custom_values WHERE id_leads = %s AND field_id = %s);",
                        (lead['id'], field['field_id'], lead['id'], field['field_id']))
            

def write_db(leads: list) -> None:
    conn = connect_db()
    cur = conn.cursor()
    
    for lead in leads:
        insert_lead(cur, lead)
        insert_tag(cur, lead)
        insert_custom_values(cur, lead)
    
    conn.commit()
    cur.close()
    conn.close()