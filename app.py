import pandas as pd
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
from jinja2 import Template
from streamlit_lottie import st_lottie
import requests
import json
from email.utils import formataddr

# Function to fetch Lottie animations from a URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None


def main():
    st.title('Gửi Email với nội dung HTML')
    # Lottie animation for an initial greeting
    with open("assets/intro.json", "r") as f:
        intro_data = json.load(f)
    st_lottie(intro_data, height=200)

    st.markdown(
        """
        Để gửi email cần bật xác minh 2 bước và tạo 
        [Mật khẩu ứng dụng](https://support.google.com/accounts/answer/185833?hl=en).
        Sau đó, nhập email và mật khẩu ứng dụng vào form bên dưới.
        """,
        unsafe_allow_html=True,
    )
    sender_email = st.text_input("Email gửi đi", placeholder="your_email@gmail.com")
    password = st.text_input("Mật khẩu", type="password", placeholder="123456")
    title = st.text_input("Tiêu đề email", placeholder="Email từ Python")
    html_file = st.file_uploader("Upload file HTML cho nội dung email", type=['html'])
    csv_file = st.file_uploader("Upload file CSV chứa danh sách người nhận", type=['csv'])

    if st.button('Gửi Email'):
        if sender_email and password and title and html_file and csv_file:
            # Đọc nội dung HTML từ file
            html_content = html_file.getvalue().decode("utf-8")
            template = Template(html_content)

            # Đọc nội dung từ file CSV
            df = pd.read_csv(csv_file, encoding='cp932')

            total_receivers = len(df)
            progress_text = "Đang gửi email..."
            my_bar = st.progress(0, text=progress_text)
            success_count = 0

            for idx in range(total_receivers):
                row = df.iloc[idx]
                try:
                    # Render the HTML content using Jinja2
                    populated_html_content = template.render(row.to_dict())

                    # Tạo đối tượng MIME
                    msg = MIMEMultipart()
                    
                    if sender_email.lower() == "contact_dtm@detomo.co.jp":
                        msg['From'] = formataddr(("デトモ株式会社", sender_email))
                    else:
                        msg['From'] = sender_email
                        
                    msg['To'] = row['メールアドレス']
                    msg['Subject'] = title
                    msg.attach(MIMEText(populated_html_content, 'html'))

                    # Tạo kết nối với server
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login(sender_email, password)
                    server.sendmail(sender_email, row['メールアドレス'], msg.as_string())
                    server.quit()

                    time.sleep(0.01)
                    my_bar.progress((idx + 1) / total_receivers, text=progress_text)
                    success_count += 1
                except Exception as e:
                    st.error(f'Không thể gửi email đến {row["メールアドレス"]}. Lỗi: {e}')

            time.sleep(1)
            my_bar.empty()

            if success_count == total_receivers:
                with open("assets/success.json", "r") as f:
                    success_data = json.load(f)
                st_lottie(success_data, height=200)
                st.success('Tất cả emails đã được gửi thành công!')
            else:
                with open("assets/warning.json", "r") as f:
                    error_data = json.load(f)
                st_lottie(error_data, height=200)
                st.warning(f'Chỉ có {success_count}/{total_receivers} emails đã được gửi thành công!')
        else:
            st.error('Vui lòng nhập đầy đủ thông tin!')


if __name__ == '__main__':
    main()
