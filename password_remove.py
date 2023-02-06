import PyPDF2

password = input("Enter your password: ")


pdf_file = open('hi.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

if pdf_reader.isEncrypted:
    pdf_reader.decrypt(password)
    pdf_writer = PyPDF2.PdfFileWriter()
    for page_num in range(pdf_reader.numPages):
        pdf_writer.addPage(pdf_reader.getPage(page_num))
    output_file = open('unprotected.pdf', 'wb')
    pdf_writer.write(output_file)
    output_file.close()
else:
    print("The PDF is not encrypted.")

pdf_file.close()
