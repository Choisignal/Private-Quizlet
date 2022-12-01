import pikepdf
import os
for f_name in os.listdir("./"):
    if f_name.endswith(".pdf"):
        try:
            input_pdf = pikepdf.Pdf.open(f_name)
            pdf = pikepdf.Pdf.new()

            for n, page in enumerate(input_pdf.pages):
                pdf.pages.append(page)

            pdf.save(f_name)
            print(f"Success===========! {f_name}")
        except:
            print(f"Error! {f_name}")