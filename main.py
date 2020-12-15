# %%
import pikepdf
import tabula


# %%
def decrypt(input_filename, password, output_filename):
    pdf = pikepdf.open(input_filename, password=password)
    pdf.save(output_filename)


# %%
filename = "unencrypted/1.pdf"
df = tabula.read_pdf(filename, pages="1-10")
df

# %%
if __name__ == "__main__":
    pass
