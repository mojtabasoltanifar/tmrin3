import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# مسیر فایل credentials.json
credentials_file = "C:/Users/FMstore.ir/tamrin3/my_expense_manager/credentials.json"

# تنظیمات گوگل شیت
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(credentials_file, scopes=scope)
client = gspread.authorize(creds)

# نمایش اسناد موجود در Google Drive
try:
    spreadsheet_list = client.openall()
    st.write("List of Spreadsheets:")
    for spreadsheet in spreadsheet_list:
        st.write(spreadsheet.title)
except Exception as e:
    st.error(f"An error occurred: {e}")

# باز کردن شیت
try:
    sheet = client.open("ExpenseManager").sheet1
except gspread.SpreadsheetNotFound:
    st.error("Spreadsheet not found. Please make sure the spreadsheet named 'ExpenseManager' exists and is shared with the service account.")
    st.stop()

# تابع برای خواندن داده‌ها از شیت
def load_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# تابع برای اضافه کردن داده‌ها به شیت
def add_data(date, category, amount, description):
    sheet.append_row([date, category, amount, description])

# رابط کاربری اپلیکیشن
st.title("مدیریت هزینه‌ها و درآمدها مجتبی سلطانی فر")

st.header("اضافه کردن تراکنش جدید")
date = st.date_input("تاریخ")
category = st.selectbox("دسته بندی", ["هزینه", "درآمد"])
amount = st.number_input("مقدار", min_value=0.0, format="%.2f")
description = st.text_input("توضیحات")

if st.button("اضافه کردن"):
    add_data(str(date), category, amount, description)
    st.success("تراکنش با موفقیت اضافه شد!")

st.header("نمایش تراکنش‌ها")
df = load_data()
st.write(df)

st.header("تحلیل داده‌ها")
if not df.empty:
    chart_data = df.groupby("category").sum()
    st.bar_chart(chart_data["amount"])
