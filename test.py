import pandas as pd

df = pd.read_csv('メール配信用リスト_test1.csv', encoding='cp932')
# df.rename(columns={'メールアドレス1': 'メールアドレス'}, inplace=True)
df.iloc[0, 2] = 'chien_vm@detomo.co.jp'
df.iloc[1, 2] = 'vumichien1692@gmail.com'
print(df.head())
df.to_csv('メール配信用リスト_test1.csv', index=False, encoding='cp932')