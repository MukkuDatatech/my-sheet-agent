import pandas as pd

def detect_duplicates(df):
    # Check for duplicates based on email and phone
    duplicate_emails = df[df.duplicated(['email'], keep=False)]
    duplicate_phones = df[df.duplicated(['phone'], keep=False)]

    # Combine the results
    duplicates = pd.concat([duplicate_emails, duplicate_phones]).drop_duplicates()

    return duplicates

if __name__ == '__main__':
    # Example usage
    data = {
        'email': ['test@example.com', 'test@example.com', 'user@example.com'],
        'phone': ['1234567890', '0987654321', '1234567890']
    }
    df = pd.DataFrame(data)
    duplicate_leads = detect_duplicates(df)
    print(duplicate_leads)