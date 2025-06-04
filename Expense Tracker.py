####################### LIBRARIES  ########################

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

# If you get a library related error, run the below code
# pip install tkcalendar

from tkcalendar import Calendar

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import datetime
######################## INITIATE THE MAIN DATAFRAME  ########################

# We are creating a pandas dataframe (df) which will be used globally by the app

# data type of each colum
df_dtype = {
    "date": "datetime64[ns]",
    "category": "category",
    "description": "str",
    "amount": "float"
}

# The different type of expense
category_ls = [
    "Transport",
    "Housing",
    "Health",
    "Food",
    "Entertainment",
    "Miscellaneous",
    "Education",
    "Utilities",
    "Shopping"
      ]

    

def convert_columns(df):
    """Convert the dataframe column into the expected format"""
    for key, value in df_dtype.items():
        if value == "datetime64[ns]":  # Special handling for datetime conversion
            df[key] = pd.to_datetime(df[key], errors='coerce')  # Safely handle invalid dates
        else:
            df[key] = df[key].astype(value)
    return df


# Create the main dataframe + apply data type conversion
df = pd.DataFrame(columns=df_dtype.keys())
df = convert_columns(df)


###########################  DATABASE FUNCTIONS  ###########################



def input_fake_data():
    """Generate fake data for testing and debugging functionalities""" 
    global df

    fake_data = {
        "date": ["2024-12-12", "2024-12-11", "2023-12-03"],
        "category": ["Food", "Transportation", "Entertainment"],
        "description": ["Lunch at restaurant", "Bus ticket", "Movie ticket"],
        "amount": [20.50, 30.00, 15.00]
    }

    fake_data_df = pd.DataFrame(fake_data)

    df = pd.concat([df, fake_data_df], ignore_index=True)
    df = df.astype(df_dtype)
    

def save_to_file():
    """Open a dialog allowing user to save the dataframe inside a CSV format only"""
    
    try:
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save as")

        if path:
            df.to_csv(path, index=False)
            messagebox.showinfo("Saved", "File Save")
        else:
            messagebox.showwarning("Error", "Operation cancelled")

    except Exception:
        messagebox.showerror("Error")



def load_from_file():
    """Open a dialog box allowing the user to load a csv file into the dataframe"""
    global df

    try:
        path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Load from")

        if path:
            # Read data from csv + convert + add to dataframe
            data_input = pd.read_csv(path)
            df = convert_columns(data_input)

            messagebox.showinfo("File loaded", "File loaded")
        else:
            messagebox.showwarning("Error", "Operation cancelled")

    except Exception:
        messagebox.showerror("Error")



def input_data():
    """
    This function creates a new window for the user to manually input some data.
    When the SUBMIT button is clicked, data is saved into the dataframe.
    """
    # Create a new window called input_data_window
    input_data_window = tk.Toplevel(root)
    input_data_window.title("Add New Expense")
    input_data_window.geometry("350x200")
    
    # 1/ User choose the date of the expense via a calendar
    value_date = None # This variable is storing the selected date
    

    def input_data_calendar():
        """create a sub window where the user choose the date via a calendar"""

        calendar_window = tk.Toplevel(input_data_window)
        calendar_window.title("Select a Date")
        calendar_window.geometry("300x300")
        
        # Create the calendar widget
        today = datetime.date.today() # Set today date as defaut value on the calendar
        calendar_input = Calendar(calendar_window, selectmode='day',
                            year = today.year, month = today.month, day = today.day)
        calendar_input.pack(pady=20)


        def submit_date():
            """create a submission button for saving the date + close the calendar window"""
            nonlocal value_date
            value_date = pd.to_datetime( calendar_input.get_date() )
            
            # Dynamically replace the text of the button "Select the date button" with the new selected date
            value_date_text =  value_date.strftime('%Y-%m-%d')
            button_open_calendar.config(text = f"{value_date_text}")
            
            calendar_window.destroy()  # Close the calendar window
        
        # Create the button (location: sub window calendar). When click: save date and close the window
        button_submit_date = tk.Button(calendar_window, text="Select the date", command = submit_date)
        button_submit_date.pack(pady=10)


    # On the input window, create the label + button to open the calendar
    label_calendar = tk.Label(input_data_window, text="Date")
    label_calendar.grid(row =0, column=0)

    button_open_calendar = tk.Button(input_data_window, text="Add date", command=input_data_calendar, width=20, height=1)
    button_open_calendar.grid(row=0, column=1)
    
    # 2/ User choose the category of the expense via a drop down list

    # List of available category
    global category_ls
    
    label_category = tk.Label(input_data_window, text="Category") 
    label_category.grid(row=1, column=0)
    
    # Create the drop-down list
    dropdown_category = ttk.Combobox(input_data_window, values = category_ls, state ="readonly", font=("Arial", 10))
    dropdown_category.bind("<<ComboboxSelected>>") # Bind selection
    dropdown_category.grid(row=1, column=1)

    
    # 3/ User input Description of the expense via text entry
    label_description = tk.Label(input_data_window, text="Description")
    label_description.grid(row=2, column=0)
    entry_description = tk.Entry(input_data_window)
    entry_description.grid(row=2, column=1)

    # 4/ User input Amount of the expense via text entry
    label_amount = tk.Label(input_data_window, text="Amount")
    label_amount.grid(row=3, column=0)
    entry_amount = tk.Entry(input_data_window)
    entry_amount.grid(row=3, column=1)


    def submit_data():
        """submit the data to dataframe and check if field are compliant with the data type"""
        # Get value from the different input to save it on the data frame
        value_category = dropdown_category.get()
        value_description = entry_description.get()
        value_amount = entry_amount.get()
        
        # Check if date is selected
        if value_date is None:
            messagebox.showerror("Error", "Please select a date.")
            return
        
        # Check if category is selected
        if len(value_category) == 0:
            messagebox.showerror("Error", "Please select a category.")
            return
        
        # Check if amount is correctly put
        try:
            value_amount = float(value_amount)
        except ValueError as e:
            messagebox.showerror("Error", f"Please input a valid number for the amount.\n Error: {str(e)}")

        new_data = pd.Series({
            'date': value_date,
            'category': value_category,
            'description': value_description,
            'amount': value_amount
        })

        global df
        df = pd.concat([df, new_data.to_frame().T], ignore_index=True)
        df = df.astype(df_dtype)
        input_data_window.destroy()


    # Add a submit button to submit the form data
    submit_button = tk.Button(input_data_window, text="Submit", command=submit_data)
    submit_button.grid(row=4, columnspan=2, pady=10)


def clear_data():
    """Clear dataframe"""
    global df
    df = df.iloc[0:0]


def delete_entry():
    """Function to delete an entry based on date input"""
    global df

    if len(df) == 0:
        messagebox.showwarning("Error", "No data to delete!")
        return

    #Initiate the sub window
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Entry")
    delete_window.geometry("400x300")

    #Showing current entries to the user
    entries_text = tk.Text(delete_window, height=10, width=45)
    entries_text.pack(pady=10)

    #Displaying entries
    entries_text.insert(tk.END, "Current Entries:\n\n")
    for idx, row in df.iterrows():
        entry_str = f"{row['date'].strftime('%Y-%m-%d')}: {row['description']} (€{row['amount']:.2f})\n"
        entries_text.insert(tk.END, entry_str)

    entries_text.config(state='disabled')  # Make text read-only

    # User can input the date to search for the expense to delete
    date_label = tk.Label(delete_window, text="Enter date to delete (YYYY-MM-DD):")
    date_label.pack(pady=5)

    date_entry = tk.Entry(delete_window)
    date_entry.pack(pady=5)

    def try_delete():
        """Search for the corresponding expense to delete and manage records with the same date"""
        date_str = date_entry.get()
        try:
            #convert input to datetime
            delete_date = pd.to_datetime(date_str)

            #Find matches
            matches = df[df['date'].dt.date == delete_date.date()]

            if len(matches) == 0:
                messagebox.showerror("Error", "No entries found for this date!")
                return

            #handling an edge case of more entries on a single date
            if len(matches) > 1:
                # Create a simple selection window
                select_window = tk.Toplevel(delete_window)
                select_window.title("Select Entry")
                select_window.geometry("300x200")

                #Show available entries with numbers
                entries_text = tk.Label(select_window, text="Entries found for this date:\n")
                entries_text.pack(pady=5)

                for i, (_, row) in enumerate(matches.iterrows(), 1):
                    entry_label = tk.Label(select_window,
                                           text=f"Entry {i}: €{row['amount']:.2f} - {row['description']}")
                    entry_label.pack(pady=2)

                #Add entry selection input
                select_label = tk.Label(select_window, text=f"Enter entry number (1 to {len(matches)}):")
                select_label.pack(pady=5)
                entry_select = tk.Entry(select_window)
                entry_select.pack(pady=5)

                def confirm_selected():
                    """Delete the entry, in case of multiples records on the same date, ask for which one to delete"""
                    try:
                        #Get user selection
                        selection = int(entry_select.get())
                        if selection < 1 or selection > len(matches):
                            messagebox.showerror("Error",f"Please enter a number between 1 and {len(matches)}")
                            return

                        #Converting selection to index
                        idx_to_delete = matches.index[selection - 1]

                        #Deleting the entry
                        df.drop(idx_to_delete, inplace=True)
                        df.reset_index(drop=True, inplace=True)
                        messagebox.showinfo("Success", "Entry deleted!")
                        select_window.destroy()
                        delete_window.destroy()
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid number!")

                tk.Button(select_window, text="Delete Selected",
                          command=confirm_selected).pack(pady=10)

            else:
                #Single entry - delete directly
                if messagebox.askyesno("Confirm", "Delete this entry?"):
                    df.drop(matches.index[0], inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    messagebox.showinfo("Success", "Entry deleted!")
                    delete_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {str(e)}")

    #Adding delete button
    delete_button = tk.Button(delete_window, text="Delete", command=try_delete)
    delete_button.pack(pady=10)
    

######################## SHOW DATAFRAME  ########################


# Show the dataframe in the UI
def show_expense():
    """how the dataframe in a window"""
    
    def sort_treeview(col, reverse):
        """Sort the Treeview based on the clicked column."""
        data = []
        for child in treeview.get_children(''):
            row_data = treeview.item(child)['values']
            if col == "amount":
                value = float(row_data[3][1:])  # Remove the € symbol and convert to float
            else:
                value = row_data[columns.index(col)]
            data.append((value, child))

        # Perform sorting
        data.sort(reverse=reverse)

        # Rearrange items in sorted order
        for index, (_, item) in enumerate(data):
            treeview.move(item, '', index)

        # Toggle the sort order for future clicks
        treeview.heading(col, command=lambda: sort_treeview(col, not reverse))

    show_expense_wondow = tk.Toplevel(root)
    show_expense_wondow.title("Data viewer")
    show_expense_wondow.geometry("600x500")

    treeview = ttk.Treeview(show_expense_wondow)
    treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(show_expense_wondow, orient=tk.VERTICAL, command=treeview.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    treeview.configure(yscrollcommand=scrollbar.set)

    # Define column headers
    columns = ["date", "category", "description", "amount"]
    treeview["columns"] = columns
    treeview["show"] = "headings"

    # Set column headers and alignment
    treeview.heading("date", text="Date", command=lambda: sort_treeview("date", False))
    treeview.heading("category", text="Category", command=lambda: sort_treeview("category", False))
    treeview.heading("description", text="Description", command=lambda: sort_treeview("description", False))
    treeview.heading("amount", text="Amount (€)", command=lambda: sort_treeview("amount", False))

    for col in columns:
        treeview.column(col, width=150, anchor="center")

    # Create a tag for center alignment
    treeview.tag_configure('center', anchor='center')

    # Sort data by date initially
    sorted_df = df.sort_values(by="date")

    # Add rows to Treeview with formatted data
    for _, row in sorted_df.iterrows():
        formatted_date = row["date"].strftime("%Y-%m-%d")  # Format date without time
        formatted_amount = f"€{row['amount']:.2f}"  # Add euro symbol and format to 2 decimals
        treeview.insert(
            "", "end", values=(formatted_date, row["category"], row["description"], formatted_amount), tags=('center',)
        )


######################## UI HANDLING FUNCTION  ########################


def update_kpi_frame(kpi_frame, filtered_df):
    """Update the 3 KPIs in the (top side of) dashboard (KPI frame)."""
    # Clear existing widgets in the KPI frame
    for widget in kpi_frame.winfo_children():
        widget.destroy()

    # Calculate KPIs
    total_value = filtered_df['amount'].sum()
    avg_monthly_expenses = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['amount'].sum().mean()
    highest_expense_category = filtered_df.groupby('category')['amount'].sum().idxmax()

    # Total amount spend (on the filtered date period)
    kpi_total = tk.Label(
        kpi_frame,
        text=f"Total Expenses: {total_value:.2f} €",
        font=("Arial", 14),
        bg="white",
        anchor="center"
    )
    kpi_total.grid(row=0, column=0, padx=20, pady=2)

    # Average monthly spending (on the filtered date period)
    kpi_avg = tk.Label(
        kpi_frame,
        text=f"Average Monthly Expense: {avg_monthly_expenses:.2f} €",
        font=("Arial", 14),
        bg="white",
        anchor="center"
    )
    kpi_avg.grid(row=0, column=1, padx=20, pady=2)

    # Highest category of spending
    kpi_highest = tk.Label(
        kpi_frame,
        text=f"Highest Spending Category: {highest_expense_category}",
        font=("Arial", 14),
        bg="white",
        anchor="center"
    )
    kpi_highest.grid(row=0, column=2, padx=20, pady=2)

    # Configure grid for KPI frame
    kpi_frame.grid_columnconfigure(0, weight=1)
    kpi_frame.grid_columnconfigure(1, weight=1)
    kpi_frame.grid_columnconfigure(2, weight=1)



def create_pie_chart(chart_frame, filtered_df):
    """Create a pie chart showing the expense distribution by category given the 
    filtered date period set by user
    """
    # Clear existing widgets in the chart frame
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Create the chart
    category_totals = filtered_df.groupby('category')['amount'].sum()
    category_totals = category_totals[category_totals > 0]
    
    fig, ax = plt.subplots(figsize=(9, 6))
    wedges, texts, autotexts = ax.pie(
        category_totals,
        labels = category_totals.index,
        autopct = '%1.1f%%',
        startangle = 90,
        wedgeprops= {'width': 0.25}, # control the donut size
        colors = plt.cm.Dark2.colors,
        pctdistance = 0.88, # put label exactly in the graph
        labeldistance = 1.10  # outside of graph
    )
    
    plt.setp(autotexts, size=10, weight="bold", color='white') # label (percentage)
    plt.setp(texts, size=10, weight="bold", color = 'black') # label (name of the category)
    
    ax.legend(frameon=False, # no outline (box)
              bbox_to_anchor = (0, 1),
              labelspacing = 0.3, handlelength = 1.5)
    
    
    ax.set_title('Expense Distribution by Category', fontsize=14, weight = 'bold', loc = 'center' )
    plt.tight_layout()

    #Draw the pie_chart in the dashboard
    canvas_pie = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_pie.draw()
    canvas_pie.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


def create_bar_chart(chart_frame, filtered_df, selected_year):
    """
    Create a bar chart showing monthly expenses
    The bar chart has the specificity to be set to a 1 year period  with 12 bars showing each months
    It is the default barchart that appear in the dashboard without pre-selection
    """
    # Summarize expenses by month
    monthly_totals = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['amount'].sum()

    # Ensure all months are included for the selected year
    all_months = pd.period_range(start=f"{selected_year}-01", end=f"{selected_year}-12", freq='M')
    monthly_totals = monthly_totals.reindex(all_months, fill_value=0)

    # Create a bar chart
    fig_barchart, ax_barchart = plt.subplots(figsize=(8.5, 6))  
    bars = ax_barchart.bar(
        [month.strftime('%b') for month in all_months],
        monthly_totals.values,
        color='#4682B4',
        edgecolor='black',
        width = 0.7
    )

    # Annotate each bar with the value
    for bar in bars:
        height = bar.get_height()
        ax_barchart.annotate(f'{height:.2f} €',  # Show values with two decimals
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 5),  # Offset for readability
                             textcoords="offset points",
                             ha='center', va='bottom', fontsize=10)


    # Set chart titles and labels
    ax_barchart.set_title('Total Expense by Month', fontsize=16, pad=20,  weight = 'bold', loc = 'center')
    ax_barchart.set_xlabel('Month', fontsize=12, labelpad=10, weight = 'bold', loc = 'center')  # Label padding
    ax_barchart.set_ylabel('Amount (€)', fontsize=12, labelpad=10,  weight = 'bold', loc = 'center')
    
    # Add top buffer
    ax_barchart.set_ylim(0, monthly_totals.max() * 1.1)

    # Rotate x-axis labels for better readability
    ax_barchart.tick_params(axis='x', labelsize=11)
    ax_barchart.tick_params(axis='y', labelsize=11) 
    

    # Ensure layout adjusts dynamically
    fig_barchart.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.2)  # Explicit adjustments
    plt.tight_layout()

    # Render chart in the Tkinter canvas
    canvas_barchart = FigureCanvasTkAgg(fig_barchart, master=chart_frame)
    canvas_barchart.draw()
    canvas_barchart.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


def create_bar_chart_2(chart_frame, filtered_df):
    """
    Create the same bar chart but this one is not set on a 1 year period and is more flexible
    It is only called when the time period is selected via the calendar in the dashboard 
    
    """
    # Convert the 'date' column to datetime
    filtered_df.loc[:, 'date'] = pd.to_datetime(filtered_df['date'])
    # Create a new column for year and month in 'YYMM' format
    filtered_df.loc[:, 'year_month'] = filtered_df['date'].dt.strftime('%b%y')
    
    # Group by 'year_month' and sum the 'amount'
    spending_by_month = filtered_df.groupby('year_month')['amount'].sum()
    # Sort the data by the datetime order of the 'date' column
    spending_by_month = spending_by_month[filtered_df.groupby('year_month')['date'].min().sort_values().index]


    # Create a bar chart
    fig_barchart, ax_barchart = plt.subplots(figsize=(8.5, 6))  
    
    # Plot the bars
    bars = ax_barchart.bar(
        spending_by_month.index,  # x-axis: months in 'MMM. YYYY' format
        spending_by_month.values,  # y-axis: total spending
        color='#4682B4',
        edgecolor='black',
        width=0.7
    )
    
    # Annotate each bar with its value
    for bar in bars:
        height = bar.get_height()
        ax_barchart.annotate(f'{height:.2f} €',  # Show values with two decimals
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 5),  # Offset for readability
                             textcoords="offset points",
                             ha='center', va='bottom', fontsize=10)
    
    # Adding title and labels
    ax_barchart.set_title('Total Expense by Month & Year', fontsize=16, pad=20, weight='bold', loc='center')
    ax_barchart.set_xlabel('Month & Year', fontsize=12, labelpad=10, weight='bold', loc='center')
    ax_barchart.set_ylabel('Amount (€)', fontsize=12, labelpad=10, weight='bold', loc='center')
    
    # Add top buffer
    ax_barchart.set_ylim(0, spending_by_month.max() * 1.1)
    
    # Rotate x-axis labels for better readability
    ax_barchart.tick_params(axis='x', labelsize=11)
    ax_barchart.tick_params(axis='y', labelsize=11) 

    # Ensure layout adjusts dynamically
    fig_barchart.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.2)  # Explicit adjustments
    plt.tight_layout()

    # Render chart in the Tkinter canvas
    canvas_barchart = FigureCanvasTkAgg(fig_barchart, master=chart_frame)
    canvas_barchart.draw()
    canvas_barchart.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    


def show_dashboard():
    """ 
    The dashboard with some metrics, a pie chart, a barchart, and some tools to select the date
    It will call some function from above code to create the chart & the metrics
    """
    # Throw back an error if no data to display
    if len(df) == 0:
        messagebox.showerror("Error", "No data to show.")
        return
        
    show_dashboard_window = tk.Toplevel(root)
    show_dashboard_window.title("Dashboard")
    show_dashboard_window.geometry("1500x750")
    
    # It serves as a temporary dataframe for the detail window
    df_for_detail = df


    def open_calendar():
        """Open a window with 2 calendar for selecting a period with a start date & endate"""
        open_calendar_window = tk.Toplevel(show_dashboard_window)
        open_calendar_window.title("calendar")
        open_calendar_window.geometry("800x350")
        
        # Add calendar
        today = datetime.date.today() # Initiate today to be the standard date
        
        def update_graph():
            """When click on the UPDATE button, update the filtered data and recreate all KPI + charts"""
            start_date = pd.to_datetime( calendar_start_date.get_date() )
            end_date = pd.to_datetime( calendar_end_date.get_date() ) 
            
            # Safe check 
            if start_date > end_date:
                messagebox.showerror("Error", "Please select a valid period.")
                return
            
            filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
            # recreate all the graph on the dashboard with the new filtered data
            update_kpi_frame(kpi_frame, filtered_df)
            create_pie_chart(chart_frame, filtered_df)
            create_bar_chart_2(chart_frame, filtered_df)
            
            value_date_text = f"From {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            label_show_period.config(text = f"{value_date_text}")
            
            nonlocal df_for_detail
            df_for_detail = filtered_df
            
            open_calendar_window.destroy()  # Close the calendar window  
        
        # Add label on top of calendar
        label_start_calendar = tk.Label(open_calendar_window, text="Choose starting date", font=("Arial", 14), anchor = "center")
        label_start_calendar.grid(row =0, column=1)
        label_end_calendar = tk.Label(open_calendar_window, text="Choose ending date", font=("Arial", 14), anchor = "center")
        label_end_calendar.grid(row =0, column=4)
        
        # Create calendar for start date
        calendar_start_date = Calendar(open_calendar_window, selectmode='day',
                            year = today.year, month = today.month, day = today.day)
        calendar_start_date.grid(row=1, column=0, columnspan=2)

        
        # Create calendar for end date
        calendar_end_date = Calendar(open_calendar_window, selectmode='day',
                            year = today.year, month = today.month, day = today.day)
        calendar_end_date.grid(row=1, column=3, columnspan=2)
        
        # Add button UPDATE at the bottom, on click, update graph on dashboard and close calendar
        button_calendar_update = tk.Button(open_calendar_window, command= update_graph,
                                           text="UPDATE", font=("Arial", 13), width=15)
        button_calendar_update.grid(row=1, column=2, padx=7)
    
             
    #Add calendar button on the dashboard window
    button_open_calendar = tk.Button(show_dashboard_window, text="Open Calendar", command=open_calendar, width=20, height=1)
    button_open_calendar.grid(row = 0, column = 0)
    
    

    def on_year_selected(selected_year):
        """Update when dropdrown for Year Filter is changed"""
        
        filtered_df = df[df['date'].dt.year == int(selected_year)]
        
        # Recreate the KPI + dashboard
        update_kpi_frame(kpi_frame, filtered_df)
        create_pie_chart(chart_frame, filtered_df)
        create_bar_chart(chart_frame, filtered_df, selected_year)
        
        value_date_text = f"From 01.01.{selected_year} to 31.12.{selected_year}"
        label_show_period.config(text = f"{value_date_text}")
        
        nonlocal df_for_detail
        df_for_detail = filtered_df

    
    # Get list of year
    available_years = sorted(df['date'].dt.year.unique().astype(str))
    year_label = tk.Label(show_dashboard_window, text="Select Year:", font=("Arial", 12))
    year_label.grid(row=0, column=0, padx=3, pady=5, sticky="w")

    # Create the drop-down list on the dashboard. On selection, will update the graph
    year_combobox = ttk.Combobox(show_dashboard_window, values=available_years, state="readonly", font=("Arial", 12))
    year_combobox.set(available_years[0])  # Default to the first year
    year_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    year_combobox.bind("<<ComboboxSelected>>", lambda event: on_year_selected(year_combobox.get()))

    label_show_period = tk.Label(show_dashboard_window, text = "", font=("Arial", 14))
    label_show_period.grid(row=1, column=0)
    
    
    # KPI and chart frames
    kpi_frame = tk.Frame(show_dashboard_window, bg="white", relief="solid", bd=2)
    kpi_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 5))

    chart_frame = tk.Frame(show_dashboard_window)
    chart_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    
    # Add the additional info
    
    def open_detail():
        """Open a window showing the spending by category, orderer by highest spending"""
        show_detail_window = tk.Toplevel(show_dashboard_window)
        show_detail_window.title("Dashboard")
        show_detail_window.geometry("400x500")
        
        grouped_data = df_for_detail.groupby("category")["amount"].sum()
        result = grouped_data.reindex(category_ls, fill_value=0)
        
        sorted_data = result.sort_values(ascending=False)
        total_amount = sum(sorted_data)
        
        # Create labels manually for each category, sorted by their values (ascending order)
        for index, (category, amount) in enumerate(sorted_data.items()):
            # Calculate the percentage
            percentage = (amount / total_amount) * 100
            
            # Create the label text with both amount and percentage
            label_text = f"{category}: {amount:.2f} € ({percentage:.1f}%)"
            
            # Create and display the label
            label_widget = tk.Label(show_detail_window, text=label_text, font=("Arial", 14))
            label_widget.grid(row=index, column=1, padx=10, pady=5, sticky='w')
    
    # Add the button opening the detail of spending by category (ascending order)
    button_detail = tk.Button(show_dashboard_window, text="Details", command=open_detail, width=20, height=1)
    button_detail.grid(row = 4, column = 0)

    # Initial update for the default year
    on_year_selected(available_years[0])


######################## GUI  ########################


# Start the main page
root = tk.Tk()
root.geometry("300x500")
root.title("EXPENSE TRACKER")

# Button for showing dataframe
button_view_expense = tk.Button(root, text="1. View expense", command=show_expense, width=20, height=1)
button_view_expense.pack(padx=10, pady=10)

# Button to display dashboard
button_dashboard = tk.Button(root, text="2. Dashboard", command=show_dashboard, width=20, height=1)
button_dashboard.pack(padx=10, pady=10)

# Button for adding a data entry
button_add_expense = tk.Button(root, text="3. Add expense", command=input_data, width=20, height=1)
button_add_expense.pack(padx=10, pady=10)

button_delete = tk.Button(root, text="4. Delete Entry", command=delete_entry, width=20, height=1)
button_delete.pack(padx=10, pady=10)

# Button to clear the dataframe
button_clear_data = tk.Button(root, text="5. Clear data", command=clear_data, width=20, height=1)
button_clear_data.pack(padx=10, pady=10)

# Button to export data to computer
button_save_file = tk.Button(root, text="6. Save to File", command=save_to_file, width=20, height=1)
button_save_file.pack(padx=10, pady=10)

# Button to import data from computer
button_load_file = tk.Button(root, text="7. Load from file", command=load_from_file, width=20, height=1)
button_load_file.pack(padx=10, pady=10)

# Button to input fake data for testing
button_input_fake_data = tk.Button(root, text="10. Input fake data", command=input_fake_data, width=20, height=1)
button_input_fake_data.pack(padx=10, pady=10)
# Launch
root.mainloop()
