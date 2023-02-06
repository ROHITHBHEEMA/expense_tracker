import tabula
import pandas as pd
import PyPDF2


## Finding the number of pages in a pdf

# Open the PDF file
pdf_file = open("bank_statement.pdf", "rb")

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
    df = tabula.read_pdf("bank_statement.pdf", pages=i,  area=(100,75,800,800))
    table = df[0]
    table.to_csv('table.txt', sep='\t', index=False)
    
    df = pd.read_csv('table.txt', sep='\t', header=None)
    df_final = pd.concat([df_final, df], axis=0,  ignore_index=True)

df_final=df_final[1:]
df_final.drop(1, axis=1, inplace=True)
df_final.columns = ['Narration', 'Date', 'Withdrawal', 'Deposit', 'Closing']
print(df_final)
df_final.to_csv('statement.csv', index=False)

df = pd.read_csv("statement.csv")

# Loop through all the rows
for i in range(len(df)):
    print(df.loc[i, "Narration"])



