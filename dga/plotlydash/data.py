from flask import current_app
import pandas as pd
from datetime import datetime
from dga import db
from dga.rtdatabase import get_current_user

def create_dataframe():
    with current_app.app_context():
        user = get_current_user()

        all_records = db.child("records").child(user["localId"]).get()

        transformer_list = []
        timestamp_list = []
        fault_type_list = []
        record_tag_list = []
        gaseous_list = []

        # Each TX
        for record in all_records.each():
            inner_record = (
                db.child("records").child(user["localId"]).child(record.key()).get()
            )

            if inner_record.each() is not None:
                # Each DGA under TX1(example)
                for data in inner_record.each():
                    transformer_list.append(record.key()) # [TX1, TX1, TX1, ..]
                    print(transformer_list)
                    record_tag_list.append(data.key()) # [DGA1, DGA2, DGA3, ..]

                    timestamp = pd.to_datetime(data.val()["timestamp"], unit="s")
                    print(timestamp)
                    timestamp_list.append(timestamp)

                    fault_type = [
                        data.val()["fault_type"].get(tool)
                        for tool in data.val()["fault_type"]
                    ]
                    fault_type_list.append(fault_type)

                    gaseous = [
                        data.val()["gaseous_data"].get(gas)
                        for gas in data.val()["gaseous_data"]
                    ]
                    gaseous_list.append(gaseous)

        df = pd.DataFrame(
            {
                "transformerList": all_records,
                "transformerKey": transformer_list,
                "Record": record_tag_list,
                "Gas Concentration (Acetylene)": [gas[0] for gas in gaseous_list],
                "Gas Concentration (Carbon Dioxide)": [gas[1] for gas in gaseous_list],
                "Gas Concentration (Carbon Monoxide)": [gas[2] for gas in gaseous_list],
                "Gas Concentration (Ethane)": [gas[3] for gas in gaseous_list],
                "Gas Concentration (Ethylene)": [gas[4] for gas in gaseous_list],
                "Gas Concentration (Hydrogen)": [gas[5] for gas in gaseous_list],
                "Gas Concentration (Methane)": [gas[6] for gas in gaseous_list],
                "Date (January)": [ts.dt for ts in timestamp_list if ts.month == 1],
                "Date (February)": [ts.dt for ts in timestamp_list if ts.month == 2],
                "Date (March)": [ts.dt for ts in timestamp_list if ts.month == 3],
                "Date (April)": [ts.dt for ts in timestamp_list if ts.month == 4],
                "Date (May)": [ts.dt for ts in timestamp_list if ts.month == 5],
                "Date (June)": [ts.dt for ts in timestamp_list if ts.month == 6],
                "Date (July)": [ts.dt for ts in timestamp_list if ts.month == 7],
                "Date (August)": [ts.dt for ts in timestamp_list if ts.month == 8],
                "Date (September)": [ts.dt for ts in timestamp_list if ts.month == 9],
                "Date (October)": [ts.dt for ts in timestamp_list if ts.month == 10],
                "Date (November)": [ts.dt for ts in timestamp_list if ts.month == 11],
                "Date (December)": [ts.dt for ts in timestamp_list if ts.month == 12]
            }
        )

        df_new = df._append()

        print(df)

        return df
