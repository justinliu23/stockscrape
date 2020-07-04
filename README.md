# Stock Tracker

* Personalize a clipboard of stocks to track based on [Yahoo! Finance](https://finance.yahoo.com/) with 3 steps:
  1. Create a CSV file to serve as your stocks clipboard and when formatting/personalizing (Excel recommended), refer to `Stocks Clipboard.csv`
  2. Create a CSV file to store your notifying email accounts and when formatting/personalizing (Excel recommended), refer to `Notifying Email Accounts.csv`
  3. Open tracker.py and insert the file path of your stocks clipboard and notifying email accounts CSV files with directories seperated by '\\' (ex. C:\\Users\\John\\Stocks Clipboard.csv) where designated at lines 10 and 13, respectively

* Receive notifying emails if a stock on your clipboard falls or rises over 5% of your buying price with 4 steps:
  1. Enable [Google 2-Step Verification](https://support.google.com/accounts/answer/185839?co=GENIE.Platform%3DAndroid&hl=en)
  2. Generate a [Google App Password](https://support.google.com/accounts/answer/185833?hl=en) for your Gmail account
  3. Change the sample email addresses (someone@example.com) to your email
  4. Insert your generated Gmail App Password where it says, "Insert your generated Gmail App Password here"
  
* Run `main.py` after you've properly personalized your CSV control files and setup your Gmail Account 

* Automating `main.py` to notify you via email requires 2 steps:
  1. [Convert](https://www.youtube.com/watch?v=UZX5kH72Yx4&list=LLn2A3GlJT_vthodJ8G63-gA&index=3&t=303s) your python script (.py) to an executable file (.exe)
  2. Open Windows Task Scheduler to [schedule a new task](https://windowsreport.com/schedule-tasks-windows-10/) with the generated .exe file in the Actions tab - scheduling other parts of the task are based on personal preferences
