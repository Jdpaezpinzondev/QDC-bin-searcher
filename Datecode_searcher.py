import pandas as pd
import wx
import wx.grid as gridlib

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def get_bins_by_item_value(item_value):

    df = pd.read_csv('csv220424.csv', delimiter='\t')

    print("Loaded DataFrame:")
    print(df.head())  # Print the first few rows of the DataFrame for debugging

    # Check if 'Item' column exists in the DataFrame
    if 'Item' not in df.columns:
        print("'Item' column not found in DataFrame.")
        return None

    # Filter rows for exact match of item value
    filtered_data = df[df['Item'].str.match(item_value, case=False)]
    print("Filtered Data:")
    print(filtered_data)  # Print the filtered data for debugging

    return filtered_data[['Period', 'Destination Bin Number']]

def search_button_clicked(event):
    item_value = item_value_entry.GetValue()
    print("Searching for item:", item_value)  # Print the item value for debugging
    result = get_bins_by_item_value(item_value)
    if result is not None and not result.empty:
        print("Found data for item:", item_value)  # Print message if data is found
        if grid.GetNumberRows() > 0:
            grid.DeleteRows(0, grid.GetNumberRows())
        grid_data = result.to_numpy().tolist()
        for row in grid_data:
            grid.AppendRows(1)
            for col_index, value in enumerate(row):
                grid.SetCellValue(grid.GetNumberRows() - 1, col_index, str(value))
    else:
        wx.MessageBox("Check your SKU!", "Item not found", wx.OK | wx.ICON_ERROR)

def on_enter(event):
    search_button_clicked(event)

#main application
app = wx.App()
frame = wx.Frame(None, title="Canadian Energy QDC Bin Datecodes", size=(900, 700))

# GUI elements
panel = wx.Panel(frame)

item_label = wx.StaticText(panel, label="Enter Item:")
item_value_entry = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
search_button = wx.Button(panel, label="Search")
search_button.Bind(wx.EVT_BUTTON, search_button_clicked)

item_value_entry.Bind(wx.EVT_TEXT_ENTER, on_enter)  

grid = gridlib.Grid(panel)
grid.CreateGrid(0, 2)

# column labels
for col_index in range(2):
    grid.SetColLabelValue(col_index, ["DATE", "BIN"][col_index].upper())
    grid.SetColLabelAlignment(col_index, wx.ALIGN_CENTER)
    grid.SetLabelFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))  # Set font for labels

sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(item_label, 0, wx.ALL, 5)
sizer.Add(item_value_entry, 0, wx.ALL | wx.EXPAND, 5)
sizer.Add(search_button, 0, wx.ALL, 5)
sizer.Add(grid, 1, wx.ALL | wx.EXPAND, 5)

panel.SetSizer(sizer)

frame.Show()
app.MainLoop()
