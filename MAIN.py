import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import requests
import json
import time
import streamlit as st
import pandas as pd
import plotly.express as px
from distutils import errors
from distutils.log import error
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import pandas as pd
import pandas_profiling
import streamlit as st

# from streamlit_gallery.utils.readme import readme
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(layout="wide")




# import streamlit as st

# Everything is accessible via the st.secrets dict:

# st.write("API_KEY:", st.secrets["API_KEY"])


# And the root-level secrets are also accessible as environment variables:

import os

st.write(
    "Has environment variables been set:",
    os.environ["API_KEY"] == st.secrets["API_KEY"],
)

API_KEY = os.environ["API_KEY"]
API_KEY = st.secrets["API_KEY"]



copy_this_ex = """select * from aave.liquidations limit 543"""

st.code(copy_this_ex)
# content = """ """ 
def ace():
    c1, c2 = st.columns([3, 1])
    c2.subheader("Parameters")
    with c1:
        content = st_ace(
            placeholder=c2.text_input("Editor placeholder", value="Write your code here"),
            language=c2.selectbox("Language mode", options=LANGUAGES, index=145),
            theme=c2.selectbox("Theme", options=THEMES, index=35),
            keybinding=c2.selectbox("Keybinding mode", options=KEYBINDINGS, index=3),
            font_size=c2.slider("Font size", 5, 24, 20),
            tab_size=c2.slider("Tab size", 1, 8, 5),
            show_gutter=c2.checkbox("Show gutter", value=True),
            show_print_margin=c2.checkbox("Show print margin", value=False),
            wrap=c2.checkbox("Wrap enabled", value=False),
            auto_update=c2.checkbox("Auto update", value=True),
            readonly=c2.checkbox("Read-only", value=False),
            min_lines=45,
            key="ace",
        )

        if content:
            # st.subheader("Content")
            st.code(content)
            
            SQL_QUERY = content
            # st.write(SQL_QUERY)
            # st.code(SQL_QUERY)

            TTL_MINUTES = 15

            def create_query():
                r = requests.post(
                    'https://node-api.flipsidecrypto.com/queries', 
                    data=json.dumps({
                        "sql": SQL_QUERY,
                        "ttlMinutes": TTL_MINUTES
                    }),
                    headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": API_KEY},
                )
                if r.status_code != 200:
                    raise Exception("Error creating query, got response: " + r.text + "with status code: " + str(r.status_code))
                
                return json.loads(r.text)    


            def get_query_results(token):
                r = requests.get(
                    'https://node-api.flipsidecrypto.com/queries/' + token, 
                    headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": API_KEY}
                )
                if r.status_code != 200:
                    raise Exception("Error getting query results, got response: " + r.text + "with status code: " + str(r.status_code))
                
                data = json.loads(r.text)
                if data['status'] == 'running':
                    time.sleep(10)
                    return get_query_results(token)

                return data
            # run_query = st.button("Run query")
            # if run_query:

            run_query = st.checkbox("Run query")
            if run_query:
                query = create_query()
                token = query.get('token')
                data = get_query_results(token)

                # print(data['columnLabels'])
                # for row in data['results']:
                #     print(row)
                # return data
                # placeholder = st.empty()
                # with placeholder:
                df = pd.DataFrame(data['results'], columns=data['columnLabels'])
                st.write(df.head())
                st.write(df.columns)
                def convert_df(df):
                    return df.to_csv().encode('utf-8')


                csv = convert_df(df)

                st.download_button(
                "Press to Download",
                csv,
                "file.csv",
                "text/csv",
                key='download-csv'
                )
                see_full = st.checkbox("See full data")
                if see_full:
                    st.write(df)
                # df = df.fillna('null')

            # df = df
                # df = df.fillna('null')

                chart_type = st.selectbox("Chart type", ["line", "bar", "scatter"])


                number_of_y_axis = st.number_input("Number of y values to plot", value=1, min_value=1, max_value=3)
                color = st.checkbox("Color sort?")
                log_y = st.checkbox("Log scale  Y ?")
                log_x = st.checkbox("Log scale  X ?")



                if number_of_y_axis == 1:
                    x = st.selectbox("X axis", df.columns, index = 0)
                    y = st.selectbox("Y axis", df.columns, index = 3)
                    if color:
                        color_sort = st.selectbox("Color by", df.columns)
                        if chart_type == "line":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =y, x ="{x}", color=color_sort, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =y, x =x, color=color_sort, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
                                st.plotly_chart(px.line(df, y =y, x =x, color=color_sort), use_container_width=True)
                        if chart_type == "bar":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =y, x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =y, x =x, color=color_sort, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
                                st.plotly_chart(px.bar(df, y =y, x =x, color=color_sort), use_container_width=True)
                        if chart_type == "scatter":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =y, x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =y, x =x, color=color_sort, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", color="{color_sort}"), use_container_width=True)')
                                st.plotly_chart(px.scatter(df, y =y, x =x, color=color_sort), use_container_width=True)
                    else:
                        if chart_type == "line":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =y, x =x, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =y, x =x, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.line(df, y ="{y}", x ="{x}"), use_container_width=True)')
                                st.plotly_chart(px.line(df, y =y, x =x), use_container_width=True)
                        if chart_type == "bar":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =y, x =x, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =y, x =x, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.bar(df, y ="{y}", x ="{x}"), use_container_width=True)')
                                st.plotly_chart(px.bar(df, y =y, x =x), use_container_width=True)
                        if chart_type == "scatter":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =y, x =x, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =y, x =x, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.scatter(df, y ="{y}", x ="{x}"), use_container_width=True)')
                                st.plotly_chart(px.scatter(df, y =y, x =x), use_container_width=True)
                if number_of_y_axis == 2:
                    x = st.selectbox("X-axis", df.columns)
                    y1 = st.selectbox("Y-axis 1", df.columns)
                    y2 = st.selectbox("Y-axis 2", df.columns)
                    if color:
                        color_sort = st.selectbox("Color", df.columns)
                        if chart_type == "line":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =[y1, y2], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =[y1, y2], x =x, color=color_sort, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                                st.plotly_chart(px.line(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
                        if chart_type == "bar":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =[y1, y2], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =[y1, y2], x =x, color=color_sort, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                                st.plotly_chart(px.bar(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
                        if chart_type == "scatter":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, color=color_sort, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                                st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, color=color_sort), use_container_width=True)
                    else:
                        if chart_type == "line":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =[y1, y2], x =x, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =[y1, y2], x =x, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}"], x ="{x}"), use_container_width=True)')
                                st.plotly_chart(px.line(df, y =[y1, y2], x =x), use_container_width=True)
                        if chart_type == "bar":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =[y1, y2], x =x, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =[y1, y2], x =x, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}"], x ="{x}"), use_container_width=True)')
                                st.plotly_chart(px.bar(df, y =[y1, y2], x =x), use_container_width=True)
                        if chart_type == "scatter":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =[y1, y2], x =x, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}"], x ="{x}"), use_container_width=True)')
                                st.plotly_chart(px.scatter(df, y =[y1, y2], x =x), use_container_width=True)
                if number_of_y_axis == 3:
                    x = st.selectbox("X-axis", df.columns)
                    y1 = st.selectbox("Y-axis 1", df.columns)
                    y2 = st.selectbox("Y-axis 2", df.columns)
                    y3 = st.selectbox("Y-axis 3", df.columns)
                    if color:
                        color_sort = st.selectbox("Color", df.columns)
                        if chart_type == "line":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                                st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
                        if chart_type == "bar":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                                st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
                        if chart_type == "scatter":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, color=color_sort, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", color="{color_sort}"), use_container_width=True)')
                                st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, color=color_sort), use_container_width=True)
                    else:
                        if chart_type == "line":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.line(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}"), use_container_width=True)')
                                st.plotly_chart(px.line(df, y =[y1, y2, y3], x =x), use_container_width=True)
                        if chart_type == "bar":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.bar(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}"), use_container_width=True)')
                                st.plotly_chart(px.bar(df, y =[y1, y2, y3], x =x), use_container_width=True)
                        if chart_type == "scatter":
                            if log_y:
                                if log_x:
                                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True, log_x=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, log_y=True, log_x=True), use_container_width=True)
                                else:
                                    st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}", log_y=True), use_container_width=True)')
                                    st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x, log_y=True), use_container_width=True)
                            else:
                                st.code(f'st.plotly_chart(px.scatter(df, y =["{y1}", "{y2}", "{y3}"], x ="{x}"), use_container_width=True)')
                                st.plotly_chart(px.scatter(df, y =[y1, y2, y3], x =x), use_container_width=True)



ace()


# st.set_page_config(layout="wide")

# variable = st.text_input("Enter your date_variable", "day")


