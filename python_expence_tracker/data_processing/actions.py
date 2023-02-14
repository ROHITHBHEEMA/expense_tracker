import tabula
import pandas as pd
import PyPDF2
import re
from .states import keywords


def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

## Finding the number of pages in a pdf

# Open the PDF file
pdf_file = open("bank_statement_2022_12.pdf", "rb")

# Create a PDF object
pdf = PyPDF2.PdfFileReader(pdf_file)

# Find the number of pages in the PDF file
num_pages = pdf.getNumPages()

# Print the number of pages
# print("Number of pages in the PDF file:", num_pages)

# Close the PDF file
pdf_file.close()

df_final = pd.DataFrame()

# Read only the part of the page specified by the area parameter
for i in range(1,num_pages+1):
    df = tabula.read_pdf("bank_statement_2022_12.pdf", pages=i,  area=(100,75,800,800))
    table = df[0]
    table.to_csv('table.txt', sep='\t', index=False)
    
    df = pd.read_csv('table.txt', sep='\t', header=None)
    df_final = pd.concat([df_final, df], axis=0,  ignore_index=True)

df_final=df_final[1:]
df_final.drop(1, axis=1, inplace=True)
df_final.columns = ['Narration', 'Date', 'Withdrawal', 'Deposit', 'Closing']

df_final.to_csv('statement.csv', index=False)

df = pd.read_csv("statement.csv")

# Loop through all the rows
for i in range(len(df)):
    df.loc[i, "Narration"]=preprocess_text(df.loc[i, "Narration"]) 
    text=df.loc[i, "Narration"]
    words = text.split() 
    for keyword in keywords:
        if keyword in words:
            df.loc[i, "Keyword"] = keyword
            break;
        else:
            df.loc[i, "Keyword"] = "UPI"
print(df)
df.to_csv('statement.csv', index=False)


def process_csv(request, **kwargs):
    pdf_file = open("bank_statement_2022_12.pdf", "rb")
    pdf = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pdf.getNumPages()
    pdf_file.close()
    df_final = pd.DataFrame()
    for i in range(1,num_pages+1):
        df = tabula.read_pdf("bank_statement_2022_12.pdf", pages=i,  area=(100,75,800,800))
        table = df[0]
        table.to_csv('table.txt', sep='\t', index=False)
        df = pd.read_csv('table.txt', sep='\t', header=None)
        df_final = pd.concat([df_final, df], axis=0,  ignore_index=True)
    df_final=df_final[1:]
    df_final.drop(1, axis=1, inplace=True)
    df_final.columns = ['Narration', 'Date', 'Withdrawal', 'Deposit', 'Closing']
    df_final.to_csv('statement.csv', index=False)
    for i in range(len(df)):
        df.loc[i, "Narration"]=preprocess_text(df.loc[i, "Narration"]) 
        text=df.loc[i, "Narration"]
        words = text.split() 
        for keyword in keywords:
            if keyword in words:
                df.loc[i, "Keyword"] = keyword
                break;
            else:
                df.loc[i, "Keyword"] = "UPI"
    print(df)
    df.to_csv('statement.csv', index=False)

PostUpdateAction = {
    'upload_data': process_csv,
}


    


