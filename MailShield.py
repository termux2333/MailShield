import imaplib
import email
from email.header import decode_header
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords

# دانلود استاپ‌وردها
nltk.download('stopwords')

# اتصال به سرور ایمیل (Gmail)
username = "your_email@gmail.com"  # ایمیل خود را وارد کنید
password = "your_password"  # رمز عبور خود را وارد کنید
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)
mail.select("inbox")

# جستجوی ایمیل‌ها
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()


num_emails_to_analyze = 5
latest_email_ids = email_ids[-num_emails_to_analyze:]

emails = []
for email_id in latest_email_ids:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])
    
 
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                emails.append(body)
    else:
        body = msg.get_payload(decode=True).decode()
        emails.append(body)


data = {
    'text': [
        "Congratulations! You've won a free iPhone. Click here to claim.",
        "Your account has been compromised. Please update your information immediately.",
        "Meeting at 3 PM. Don't forget to bring the documents.",
        "Your Amazon order has been shipped. Track your package here.",
        "Limited-time offer! Get 50% off on all items in our store.",
        "Please review the attached invoice for your recent purchase."
    ],
    'label': [1, 1, 0, 0, 1, 0]  # 1 = فیشینگ، 0 = عادی
}

 DataFrame
df = pd.DataFrame(data)


vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(df['text'])
y = df['label']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


model = MultinomialNB()
model.fit(X_train, y_train)

new_emails_transformed = vectorizer.transform(emails)
predictions = model.predict(new_emails_transformed)


for i, prediction in enumerate(predictions):
    print(f"Email {i+1}: {'Phishing' if prediction == 1 else 'Legitimate'}")
