import pandas as pd

def convert_excel_to_iif(excel_file, output_iif_path):
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
    except Exception as e:
        return f"Error reading the Excel file: {str(e)}"

    date_from_row = '04-04-25'  
    
    try:
        formatted_date = pd.to_datetime(date_from_row, format='%d-%m-%y').strftime('%m/%d/%Y')  #  MM/DD/YYYY
    except Exception as e:
        return f"Error formatting the date: {str(e)}"

    df_cleaned = df.iloc[12:, [3, 6, 10, 12, 16]]  
    df_cleaned.columns = ['Date', 'Employee Name', 'Employee ID', 'Reg Hours', 'Total Worked']  

    df_cleaned['New Column'] = '' 

    df_cleaned = df_cleaned.dropna(subset=['Employee Name', 'Employee ID', 'Reg Hours', 'Total Worked'])


    iif_header = "!TIMEACT\tDATE\tJOB\tEMP\tITEM\tPITEM\tDURATION\tPROJ\tNOTE\tXFERTOPAYROLL\tBILLINGSTATUS\n"

    iif_data = [iif_header]

    for _, row in df_cleaned.iterrows():
        timeact = "TIMEACT"
        date = formatted_date  
        job = "Default Job"
        emp = row['Employee Name']
        item = "Hourly Rate"
        pitem = "Hourly Wage"
        duration = row['Total Worked'] if pd.notna(row['Total Worked']) else row['Reg Hours']  
        proj = ""
        note = ""
        xfertopayroll = "Y"
        billingstatus = "1"
        new_column_value = row['New Column'] 

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


excel_file_path = '/mnt/data/Warman_SK_Payroll_Listing.xlsx'
output_iif_path = '/mnt/data/output_file.iif'  

convert_excel_to_iif(excel_file_path, output_iif_path)