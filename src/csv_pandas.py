import pandas as pd


def create_dataframes(leads):
    df_leads = pd.DataFrame([{key: lead.get(key) for key in ['id', 'name', 'price', 'responsible_user_id', 'group_id',
                                                              'status_id', 'pipeline_id', 'loss_reason_id', 'created_by',
                                                              'updated_by', 'created_at', 'updated_at', 'closed_at',
                                                              'closest_task_at', 'is_deleted', 'account_id', 'labor_cost']}
                              for lead in leads])
    
    df_tags = pd.DataFrame([{ 'id_leads': lead['id'], 'tag_name': tag['name'], 'color': tag.get('color') }
                              for lead in leads for tag in lead['_embedded'].get('tags', [])])
    
    df_custom_values = pd.DataFrame([{ 'id_leads': lead['id'], 'field_id': field['field_id'], 'field_name': field['field_name'],
                                       'field_code': field.get('field_code'), 'field_type': field.get('field_type', 'text') }
                                      for lead in leads for field in (lead.get('custom_fields_values') or [])])
    
    df_custom_values_values = pd.DataFrame([{ 'field_id': field['field_id'], 'value': value['value'],
                                              'enum_id': value.get('enum_id'), 'enum_code': value.get('enum_code') }
                                             for lead in leads for field in (lead.get('custom_fields_values') or [])
                                             for value in field.get('values', [])])
    
    return df_leads, df_tags, df_custom_values, df_custom_values_values


def pandas_csv(data: list):
    all_leads = {lead['id']: lead for lead in data}.values()
    df_leads, df_tags, df_custom_values, df_custom_values_values = create_dataframes(all_leads)
    
    df_final = df_leads.merge(df_tags, how='left', left_on='id', right_on='id_leads').drop(columns=['id_leads']) \
                       .merge(df_custom_values, how='left', left_on='id', right_on='id_leads').drop(columns=['id_leads']) \
                       .merge(df_custom_values_values, how='left', on='field_id')
    
    df_final.to_csv('full_data.csv', index=False, encoding='utf-8')
    print(df_final.count())