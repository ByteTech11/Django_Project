import pandas as pd

def convert_excel_to_iif(excel_file, output_iif_path):
    try:
        df = pd.read_excel(excel_file, engine='openpyxl', skiprows=12)
    except Exception as e:
        return f"Error reading the Excel file: {str(e)}"

    date_from_row = '04-04-25'

    try:
        formatted_date = pd.to_datetime(date_from_row, format='%d-%m-%y').strftime('%m/%d/%Y')
    except Exception as e:
        return f"Error formatting the date: {str(e)}"

    df_cleaned = df[['Employee', 'Emp\nNum', 'Reg Hours', 'Total', 'Rate']]

    df_cleaned = df_cleaned.dropna(subset=['Employee', 'Emp\nNum', 'Reg Hours', 'Total'])

    iif_header = "!TIMEACT\tDATE\tJOB\tEMP\tITEM\tPITEM\tDURATION\tPROJ\tNOTE\tXFERTOPAYROLL\tBILLINGSTATUS\n"
    iif_data = [iif_header]

    for _, row in df_cleaned.iterrows():
        timeact = "TIMEACT"
        date = formatted_date  
        job = "Default Job"
        emp = row['Employee']
        item = "Hourly Rate"  
        pitem = "Regular Pay"  
        duration = row['Total'] if pd.notna(row['Total']) else row['Reg Hours']  
        proj = ""
        note = ""
        xfertopayroll = "Y"
        billingstatus = "1"

        iif_row = f"{timeact}\t{date}\t{job}\t{emp}\t{item}\t{pitem}\t{duration}\t{proj}\t{note}\t{xfertopayroll}\t{billingstatus}"
        iif_data.append(iif_row)

    iif_content = "\n".join(iif_data)

    try:
    
        with open(output_iif_path, 'w') as iif_file:
            iif_file.write(iif_content)
        print(f"IIF file successfully created: {output_iif_path}")
    except Exception as e:
        return f"Error saving the IIF file: {str(e)}"

    return iif_content


excel_file_path = 'path/to/your/excel_file.xlsx'  
output_iif_path = 'path/to/output_file.iif'  

convert_excel_to_iif(excel_file_path, output_iif_path)
