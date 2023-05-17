import streamlit as st
import pandas as pd
#import dep
from PIL import Image
import io
import mysql.connector
cnx= mysql.connector.connect(user="root", password="root", host="localhost", database="auto")
crx= cnx.cursor()
print("connection established")

def main():

    st.title("BIG BOY TOYZ")
    image = Image.open('ccover.jpg')
    st.image(image)
    option=st.sidebar.selectbox("Ready to race? Choose an option",("Show My collection","Add a new car in the garage","Update your car","Remove Broken cars"))
    # st.markdown(
    #      f"""
    #      <style>
    #      .stApp {{
    #          background-image: url("https://images.pexels.com/photos/1037995/pexels-photo-1037995.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
    #          background-attachment: fixed;
    #          background-size: cover
    #      }}
    #      </style>
    #      """,
    #      unsafe_allow_html=True
    #  )
    if  option=="Show My collection":
        st.markdown("""---""")
        st.subheader("Discover every cars")
        audio_file = 'success.mp3'
        if st.button("Click Here!"):
            #audio_file = 'success.mp3'
            #st.audio(audio_file, format='audio/mp3')
            crx.execute("select c.*,cd.mileage,cd.engine_capacity,m.brand_name,m.country,cd.segment from cars c,car_details cd,manufacturers m where m.car_id=cd.car_id and m.car_id=c.car_id")
            data=crx.fetchall()
            hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            #fines = [{'Fine ID': row[0], 'Student Name': row[1], 'Fine Amount': row[2], 'Fine Reason': row[3], 'Offense Date': row[4],'Fine ID': row[5], 'Student Name': row[6], 'Fine Amount': row[7], 'Fine Reason': row[8],'Student Name': row[9]} for row in data]
            #st.table(fines)
            #patients = pd.read_sql('select c.*,cd.mileage,cd.engine_capacity,m.brand_name,m.country,cd.segment from cars c,car_details cd,manufacturers m where m.car_id=cd.car_id and m.manufacturer_id=c.manufacturer_id', cnx)
            # Display the patients data in an overlay
            #with st.expander(""):
            # st.table(patients)

            result=pd.DataFrame(data,columns=["car_id","manufacturer_id","model","price","launch_date","mileage","engine_capacity","brand_name","country","segment"])
            result2 = result[result.columns[2:]]
            st.table(result2)
        st.markdown("""---""")
        st.subheader("Search Cars By Budget")
        values = st.slider('',0, 10000000, (500000, 1000000))
        if st.button("Search"):
            query="select c.*,cd.mileage,cd.engine_capacity,m.brand_name,m.country,cd.segment from cars c,car_details cd,manufacturers m where m.car_id=cd.car_id and m.car_id=c.car_id and price >= %s and price <= %s"
            values3=(values[0],values[1])
            crx.execute(query,values3)
            data=crx.fetchall()
            hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            result=pd.DataFrame(data,columns=["car_id","manufacturer_id","model","price","launch_date","mileage","engine_capacity","brand_name","country","segment"])
            result2 = result[result.columns[2:]]
            st.table(result2)

        st.markdown("""---""")

        st.subheader("Search Cars By Brands")
        crx.execute("select distinct brand_name from manufacturers")
        values = [row[0] for row in crx.fetchall()]
        selected=st.selectbox("Select Brand",values)
        query="select c.*,cd.mileage,cd.engine_capacity,m.brand_name,m.country,cd.segment from cars c,car_details cd,manufacturers m where m.car_id=cd.car_id and m.car_id=c.car_id and brand_name=%s"
        crx.execute(query,(selected,))
        data=crx.fetchall()
        hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        result=pd.DataFrame(data,columns=["car_id","manufacturer_id","model","price","launch_date","mileage","engine_capacity","brand_name","country","segment"])
        result2 = result[result.columns[2:]]
        st.table(result2)

        st.markdown("""---""")

    elif option=="Add a new car in the garage":
        st.subheader("Add a new car in the garage")
        modell=st.text_input("Name of the CAR")
        launch_y=st.number_input("Launch Year")
        segmentt=st.selectbox("Enter Segment",("Hatchback","SUV","Sedan"))
        mileagee=st.number_input("KiloMeter runs on a litre")
        pricee=st.number_input("Enter Price")
        enginee=st.number_input("Engine Capacity in Litres")
        m_name=st.selectbox("Brand",("Maruti Suzuki","Mahindra & mahindra","Tata motors","Honda","Toyota","Hyundai","Nissan","Skoda","Wolkswagen","Porsche","Renault","Kia","MG Hector","Audi","BMW","Mercedes-Benz"))
        country_name=st.text_input("Country")
        if st.button("HIT ADD"):
            #dep.func(m_name,modell,pricee,launch_y,country_name,mileagee,enginee,segmentt)
            table_cars="insert into cars(manufacturer_id,model,price,launch_date) values(%s,%s,%s,%s)"
            subquery = "SELECT manufacturer_id FROM base where brand=%s"
            crx.execute(subquery,(m_name,))
            manufacturer_id = crx.fetchone()[0]
            val2 = (manufacturer_id, modell, pricee, launch_y)
            crx.execute(table_cars, val2)
            cnx.commit()

            crx.execute("SELECT LAST_INSERT_ID()")
            car_id = crx.fetchone()[0]

            table_manufacturer="insert into manufacturers(manufacturer_id,car_id,brand_name,country) values(%s,%s,%s,%s)"
            subquery = "SELECT manufacturer_id FROM base where brand=%s"
            crx.execute(subquery,(m_name,))
            manufacturer_id = crx.fetchone()[0]
            val1=(manufacturer_id,car_id,m_name,country_name)
            crx.execute(table_manufacturer, val1)
            cnx.commit()
            table_details="insert into car_details(car_id,mileage,engine_capacity,segment) values(%s,%s,%s,%s)"
            val3=(car_id,mileagee,enginee,segmentt)
            crx.execute(table_details, val3)
            cnx.commit()
            st.success("Record Inserted")

    elif option=="Update your car":
        st.subheader("Upgrade your car")

        m_name=st.selectbox("Brand",("Maruti Suzuki","Mahindra & mahindra","Tata motors","Honda","Toyota","Hyundai","Nissan","Skoda","Wolkswagen","Porsche","Renault","Kia","MG Hector","Audi","BMW","Mercedes-Benz"))

        subquery2="select c.model from cars c join manufacturers m on c.car_id=m.car_id where m.brand_name=%s"
        crx.execute(subquery2,(m_name,))
        values1 = [row[0] for row in crx.fetchall()]
        modell=st.selectbox("select model",values1)
        
        launch_y=st.number_input("Launch Year")
        segmentt=st.selectbox("Enter Segment",("Hatchback","SUV","Sedan"))
        mileagee=st.number_input("KiloMeter runs on a litre")
        pricee=st.number_input("Enter Price")
        enginee=st.number_input("Engine Capacity in Litres")
        country_name=st.text_input("Country")
        if st.button("UPDATE"):
            #dep.func(m_name,modell,pricee,launch_y,country_name,mileagee,enginee,segmentt)
            table_cars="update cars set price=%s,launch_date=%s where model=%s"
            val3 = (pricee, launch_y,modell)
            crx.execute(table_cars, val3)
            cnx.commit()
            table_manufacturer="update manufacturers m join cars c on c.car_id=m.car_id set m.country=%s where c.model=%s"
            val2=(country_name,modell)
            crx.execute(table_manufacturer, val2)
            cnx.commit()
            table_details="update car_details cd join manufacturers m on cd.car_id=m.car_id join cars c on c.car_id=m.car_id set mileage=%s,engine_capacity=%s,segment=%s where c.model=%s "
            val3=(mileagee,enginee,segmentt,modell)
            crx.execute(table_details, val3)
            cnx.commit()
            st.success("Changes Successfully Done!!!")


    elif option=="Remove Broken cars":
        st.subheader("Remove a car")
        m_name=st.selectbox("Brand",("Maruti Suzuki","Mahindra & mahindra","Tata motors","Honda","Toyota","Hyundai","Nissan","Skoda","Wolkswagen","Porsche","Renault","Kia","MG Hector","Audi","BMW","Mercedes-Benz"))

        subquery2="select c.model from cars c join manufacturers m on c.car_id=m.car_id where m.brand_name=%s"
        crx.execute(subquery2,(m_name,))
        values1 = [row[0] for row in crx.fetchall()]
        modell=st.selectbox("select model",values1)

        # subquery="select distinct brand_name from manufacturers"
        # crx.execute(subquery)
        # values = [row[0] for row in crx.fetchall()]
        # st.write(values)
        # selected=st.selectbox("Select Brand",values)
        # st.write(selected)

        # subquery2="select c.model from cars c join manufacturers m on c.manufacturer_id=m.manufacturer_id where m.brand_name=%s"
        # crx.execute(subquery2,(selected,))
        # values2 = [row[0] for row in crx.fetchall()]
        # st.write(values2)
        # selected_model=st.selectbox("select model",values2)
        # st.write(selected_model)
        if st.button("DELETE"):
                
                subquery3="delete cd.* from car_details cd,manufacturers m,cars c where cd.car_id=m.car_id and c.car_id=m.car_id and c.model=%s"
                subquery4="delete m.* from manufacturers m,cars c where c.car_id=m.car_id and c.model=%s"
                subquery5="delete cars.* from cars where model=%s"
                crx.execute(subquery3,(modell,))
                cnx.commit()
                crx.execute(subquery4,(modell,))
                cnx.commit()
                crx.execute(subquery5,(modell,))
                cnx.commit()
                st.success("Successfully deleted record")   
                
if __name__=="__main__":
    main()
