import streamlit as st



st.title("WELCOME TO PERFORMANTS!")
st.header("WHAT ARE FORMANTS?")


st.write("Formants are defined in different ways by different groups. For the purposes of " +
         "this app, formants are a naturally-occurring property of any tube (such as the " +
         "human vocal tract), that allow certain ranges of overtone frequencies to be reinforced.")
st.write("For example, if a column of air is excited at a frequency of 120 Hz, and the column has formants in the ranges of " +
         "250-350 Hz and 2200-3000 Hz, the overtones at 240 Hz and 2280 will be reinforced, and our ear will process this " +
         "composite sound as the vowel [ i ]. Classical vocal pedagogy is concerned with the first five formants, but formants " +
         "3, 4 and 5 cluster together to form the 'Singer's Formant,' while formants 1 and 2 are generally sufficient for distinguishing " +
         "one vowel from another.")
st.write("This app is designed both to explore your natural formants in your native language, and also to use formant values to help " +
         "you produce French vowels more correctly. Jump to page 1 to test your natural formant values, and then to page 2 to try some " +
         "French vowels.")

st.subheader("All feedback and criticism is welcome. Please email your comments to me at performantsdata@gmail.com.")
 
st.page_link("/Users/hobbsburgdynasty/Desktop/STREAMLIT/pages/International_Formants_Database.py", label = "Page 1: The International Formant Database")
st.page_link("/Users/hobbsburgdynasty/Desktop/STREAMLIT/pages/performants_page_2.py", label = "Page 2: Formants in French")

#""" 
#If you've two-step verification enabled, your regular password won't work. Instead, generate an app-specific password:#

#- Go to your Google Account.
#- On the left navigation panel, click on "Security."
#- Under "Signing in to Google," select "App Passwords." You might need to sign in again.
#- At the bottom, choose the app and device you want the app password for, then select "Generate."
#- Use this app password in your Streamlit app.


#"""

#import streamlit as st
#import smtplib
#from email.mime.text import MIMEText

#st.title('Send Streamlit SMTP Email 💌 🚀')

#st.markdown("""
#**Enter your email, subject, and email body then hit send to receive an email from `summittradingcard@gmail.com`!**
#""")

# Taking inputs
#email_sender = st.text_input('From', 'summittradingcard@gmail.com', disabled=True)
#email_receiver = st.text_input('To', 'hobbsburgempire@gmail.com')
#subject = st.text_input('Subject', "You suck")
#body = st.text_area('Body', "Big donkey dick")

# Hide the password input
#password = st.text_input('Password', type="password", disabled=True)  

#if st.button("Send Email"):
#    try:
 #       msg = MIMEText(body)
 #       msg['From'] = email_sender
  #      msg['To'] = email_receiver
  #      msg['Subject'] = subject

   #     server = smtplib.SMTP('smtp.gmail.com', 587)
  #      server.starttls()
  #      server.login(st.secrets["email"]["gmail"], st.secrets["email"]["password"])
  #      server.sendmail(email_sender, email_receiver, msg.as_string())
  #      server.quit()

   #     st.success('Email sent successfully! 🚀')
  #  except Exception as e:
    #    st.error(f"Failed to send email: {e}")
#"""
