CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    name varchar(255),
    price float,
    responsible_user_id int4,
    group_id int4,
    status_id int4,
    pipeline_id int4,
    loss_reason_id int4,
    created_by int4,
    updated_by int4,
    created_at timestamp,
    updated_at timestamp,
    closed_at timestamp,
    closest_task_at timestamp,
    is_deleted bool,
    account_id int4,
    labor_cost float
);

CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name varchar(100) UNIQUE,
    color varchar(100)
);

CREATE TABLE IF NOT EXISTS link_leads_tags (
    id_leads int4 REFERENCES leads(id),
    id_tags int4 REFERENCES tags(id),
    PRIMARY KEY (id_leads, id_tags)
);

CREATE TABLE IF NOT EXISTS custom_values (
    field_id SERIAL PRIMARY KEY,
    field_name varchar(100),
    field_code varchar(100),
    field_type varchar(20)
);

CREATE TABLE IF NOT EXISTS link_leads_custom_values (
    id_leads int4 REFERENCES leads(id),
    field_id int4 REFERENCES custom_values(field_id),
    PRIMARY KEY (id_leads, field_id)
);

CREATE TABLE IF NOT EXISTS value_from_customer_value (
    id_value SERIAL PRIMARY KEY,
    value varchar(100) UNIQUE,
    enum_id int4,
    enum_code varchar(255)
);

CREATE TABLE IF NOT EXISTS link_custom_values_value (
    id_value int4 REFERENCES value_from_customer_value(id_value),
    field_id int4 REFERENCES custom_values(field_id),
    PRIMARY KEY (id_value, field_id)
);
"""

GET_TABLE = """
SELECT t1.*, t3.*, t5.*, t7.*
FROM leads as t1
LEFT JOIN link_leads_tags as t2 on t1.id = t2.id_leads
LEFT JOIN tags as t3 on t2.id_tags = t3.id
left join  link_leads_custom_values as t4 on t1.id = t4.id_leads
LEFT JOIN custom_values as t5 on t4.field_id = t5.field_id
LEFT JOIN link_custom_values_value as t6 on t6.field_id = t5.field_id
LEFT JOIN value_from_customer_value as t7 on t7.id_value = t6.id_value
"""