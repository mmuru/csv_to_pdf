from pdf_mc_table import PDFMcTable
import csv

def csv_to_pdf_table(in_csv_file, pdf_output_file):
    pdf = PDFMcTable(orientation="L")
    pdf.add_page()
    pdf.set_font('Arial','',8.0)
    epw = pdf.w - 2*pdf.l_margin
    font_size = 8
    col_height = 5
    fields = []
    with open(in_csv_file, "rb") as csvfile:
        reader = csv.reader(csvfile)
        fields = reader.next()
        total_columns = len(fields)
        col_width = epw/total_columns
        print("epw={} col_width={}".format(epw, col_width))
        cell_widths = []
        for i in range(0,total_columns):
            cell_widths.append(int(col_width))
        #
        pdf.set_cell_widths(cell_widths)
        pdf.set_line_heights(col_height)
        pdf.write_row(fields)
        #
        for row in reader:
            pdf.write_row(row)

        pdf.output(pdf_output_file,'F')

if __name__ == '__main__':
    csv_to_pdf_table("test_sales_data.csv", "test_sales_data.pdf")

