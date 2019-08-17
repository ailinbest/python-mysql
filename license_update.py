# -*- coding:utf-8 -*-
from db_wrapper import MysqlDB
from record import AppLicenseRecord
import json

if __name__ == "__main__":
    sql = MysqlDB()
    Session = sql.create_session()
    session = Session()
    # 查询
    #records = session.query(AppLicenseRecord).filter(AppLicenseRecord.id == "1").all()
    records = session.query(AppLicenseRecord).all()

    switch_add = {'restful': {'start': 0, 'end': 0}}
    config_add = {"key_name":"TI_003_1I","status":0,"max_query_allowed":"3","start_time":"2019-08-16 00:00:00","end_time":"2020-08-16 00:00:00"}
    
    for record in records:
        if record:
            switch = record.logic_switch
            config = record.func_config
            if switch and config:
                swith_json = json.loads(switch)
                config_json = json.loads(config)
                #print(config_json)
                l = [c.get('key_name') == 'TI_003_1I' for c in config_json]
                if 'restful' in switch and sum(l)>0:
                    #print(config_json)
                    print(f'---------->{record.id} Already added!')
                else:
                    print('==========before==========')
                    print(swith_json)
                    print(config_json)
                    print('==========after=========')
                    # swith_start_time = swith_json.get('crash').get('start')
                    # swith_end_time = swith_json.get('crash').get('end')

                    # switch_add['restful']['start'] = swith_start_time
                    # switch_add['restful']['end'] = swith_end_time

                    if len(config_json)==0:
                        continue

                    config_start_time = config_json[0].get('start_time')
                    config_end_time = config_json[0].get('end_time')
                    config_add['start_time']=config_start_time
                    config_add['end_time'] = config_end_time

                    swith_json.update(switch_add)
                    config_json.append(config_add)

                    print(swith_json)
                    print(config_json)
                    print(f'----------update database {record.id}---------')

                    values = {
                        'logic_switch':json.dumps(swith_json,ensure_ascii=False),
                        'func_config':json.dumps(config_json,ensure_ascii=False)
                    }

                    print('values:',values)
                    # 更新操作 
                    session.query(AppLicenseRecord).filter(AppLicenseRecord.id==record.id).update(values)
                    session.commit()
                    
                    
