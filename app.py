import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


def main():
    # Giao diện người dùng
    st.title('Gửi Email với nội dung HTML')
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
    receiver_emails = st.text_input("Vui lòng nhập địa chỉ email của người nhận, tách biệt bởi dấu phẩy "
                                   "(,) nếu có nhiều hơn một người nhận.",
                                   placeholder="receiver@gmail.com")
    title = st.text_input("Tiêu đề email", placeholder="Email từ Python")
    html_file = st.file_uploader("Upload file HTML cho nội dung email", type=['html'])

    # Khi người dùng nhấn nút gửi
    if st.button('Gửi Email'):
        if sender_email and password and receiver_emails and html_file:
            # Đọc nội dung HTML từ file
            html_content = html_file.getvalue().decode("utf-8")
            receivers = [email.strip() for email in receiver_emails.split(',')]
            progress_text = "Đang gửi email..."
            my_bar = st.progress(0, text=progress_text)
            total_receivers = len(receivers)
            # Thiết lập kết nối SMTP và gửi email
            success_count = 0
            for email_index in range(total_receivers):
                try:
                    # Tạo đối tượng MIME
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = receivers[email_index]
                    msg['Subject'] = title
                    # Đính kèm nội dung HTML
                    msg.attach(MIMEText(html_content, 'html'))

                    # Tạo kết nối với server
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receivers[email_index], msg.as_string())
                    server.quit()
                    time.sleep(0.01)
                    my_bar.progress((email_index + 1) / total_receivers, text=progress_text)
                    success_count += 1
                except Exception as e:
                    st.error(f'Không thể gửi email {receivers[email_index]}. Lỗi: {e}')

            time.sleep(1)
            my_bar.empty()
            time.sleep(0.5)
            if success_count == total_receivers:
                st.success('Tất cả emails đã được gửi thành công!')
            else:
                st.warning(f'Chỉ có {success_count}/{total_receivers} emails đã được gửi thành công!')
        else:
            st.error('Vui lòng nhập đầy đủ thông tin!')


if __name__ == '__main__':
    main()
