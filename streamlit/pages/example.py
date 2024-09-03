import streamlit as st


st.write("Hello world")

num = st.number_input("Enter a number")
num2 = st.number_input("Enter another number")

buttonclicked = st.button("run math")


if (buttonclicked and num and num2):
    st.write(f"The sum of {num} and {num2} is {int(num) + int(num2)}")